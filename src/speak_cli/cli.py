import argparse
import os
import warnings
import shutil
import subprocess
import sys
import wave
from pathlib import Path
from typing import Generator, Optional



LANG_CODES = {
    # From upstream Kokoro CLI (`kokoro.__main__`)
    "a": "American English",
    "b": "British English",
    "h": "Hindi",
    "e": "Spanish",
    "f": "French",
    "i": "Italian",
    "p": "Brazilian Portuguese",
    "j": "Japanese",
    "z": "Mandarin Chinese",
}


def synth_results(text: str, lang: str, voice: str, speed: float, repo_id: str | None = None, device: str = "auto"):
    """Yield Kokoro synthesis results using the upstream KPipeline."""
    import torch
    from kokoro import KPipeline  # type: ignore

    # Auto-detect best device if not specified
    if device == "auto":
        if torch.backends.mps.is_available():
            device = "mps"
            print(f"[info] Using Apple Silicon GPU (MPS) for acceleration", file=sys.stderr)
        else:
            device = "cpu"
            print(f"[info] Using CPU (MPS not available)", file=sys.stderr)
    elif device == "mps" and not torch.backends.mps.is_available():
        print(f"[warn] MPS requested but not available, falling back to CPU", file=sys.stderr)
        device = "cpu"
    else:
        print(f"[info] Using device: {device}", file=sys.stderr)

    if not voice.startswith(lang):
        print(f"[warn] Voice '{voice}' may not match language '{lang}'.", file=sys.stderr)
    
    pipeline = KPipeline(lang_code=lang, repo_id=repo_id, device=device)
    yield from pipeline(text, voice=voice, speed=speed, split_pattern=r"\n+")


def write_wav(path: Path, frames: Generator, samplerate: int = 24000) -> None:
    import numpy as np  # Local import to avoid dependency at import-time
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit PCM
        wav.setframerate(samplerate)
        for result in frames:
            audio = getattr(result, "audio", None)
            if audio is None:
                continue
            # Convert to 16-bit PCM
            audio_bytes = (audio.numpy() * 32767).astype(np.int16).tobytes()
            wav.writeframes(audio_bytes)


def maybe_play(path: Path) -> None:
    afplay = shutil.which("afplay")
    if not afplay:
        print("[info] 'afplay' not found; skipping playback.")
        return
    try:
        subprocess.run([afplay, str(path)], check=True)
    except subprocess.CalledProcessError as exc:
        print(f"[warn] Playback failed: {exc}", file=sys.stderr)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        prog="speak",
        description="Synthesize speech with Kokoro (Apple Silicon GPU-optimized)",
    )
    parser.add_argument("text", nargs='?', help="Quoted text to speak (or read from stdin if piped)")
    parser.add_argument(
        "-v",
        "--voice",
        default="af_heart",
        help="Voice ID (e.g., 'af_heart'). Must exist in Kokoro model set.",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=sorted(LANG_CODES.keys()),
        help="Language code (defaults to first letter of voice)",
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=float,
        default=1.0,
        help="Speech speed multiplier (default: 1.0)",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=Path("out.wav"),
        help="Output WAV path (default: out.wav)",
    )
    default_repo = os.environ.get("KOKORO_REPO", "hexgrad/Kokoro-82M")
    parser.add_argument(
        "--repo-id",
        default=default_repo,
        help=f"Hugging Face repo id (default: {default_repo})",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "mps"],
        default="auto",
        help="Device to use for inference: 'auto' (default, uses MPS if available), 'cpu', or 'mps'",
    )
    # Quiet by default; allow opt-out with --no-quiet
    parser.add_argument(
        "--no-quiet",
        dest="quiet",
        action="store_false",
        help="Show non-critical warnings (torch RNN dropout, weight_norm deprecation)",
    )
    parser.set_defaults(quiet=True)
    parser.add_argument(
        "--print-path",
        action="store_true",
        help="Print the output WAV path after synthesis",
    )
    # Play by default; allow opt-out with --no-play
    parser.add_argument(
        "--no-play",
        dest="play",
        action="store_false",
        help="Do not play the WAV after synthesis",
    )
    parser.set_defaults(play=True)
    args = parser.parse_args(argv)

    # Read from stdin if no text argument provided (piped input)
    if args.text is None:
        if not sys.stdin.isatty():
            args.text = sys.stdin.read().strip()
        else:
            parser.error("No text provided. Either provide text as an argument or pipe it via stdin.")

    if args.quiet:
        # Suppress common, non-actionable warnings from upstream deps
        warnings.filterwarnings(
            "ignore",
            message=r"dropout option adds dropout.*num_layers greater than 1",
            category=UserWarning,
            module=r"torch\.nn\.modules\.rnn",
        )
        warnings.filterwarnings(
            "ignore",
            message=r"`torch\.nn\.utils\.weight_norm` is deprecated",
            category=FutureWarning,
            module=r"torch\.nn\.utils\.weight_norm",
        )

    lang = args.language or args.voice[:1]
    if lang not in LANG_CODES:
        parser.error(
            f"Cannot infer language from voice '{args.voice}'. Supply --language one of {sorted(LANG_CODES)}"
        )

    frames = synth_results(args.text, lang=lang, voice=args.voice, speed=args.speed, repo_id=args.repo_id, device=args.device)
    write_wav(args.out, frames)
    if args.print_path:
        print(f"Wrote: {args.out}")
    if args.play:
        maybe_play(args.out)


if __name__ == "__main__":
    main()
