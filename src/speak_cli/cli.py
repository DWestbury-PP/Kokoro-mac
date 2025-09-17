import argparse
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


def synth_results(text: str, lang: str, voice: str, speed: float, repo_id: str | None = None):
    """Yield Kokoro synthesis results using the upstream KPipeline."""
    from kokoro import KPipeline  # type: ignore

    if not voice.startswith(lang):
        print(f"[warn] Voice '{voice}' may not match language '{lang}'.", file=sys.stderr)
    pipeline = KPipeline(lang_code=lang, repo_id=repo_id)
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
        description="Synthesize speech with Kokoro (CPU-only, Apple Silicon)",
    )
    parser.add_argument("text", help="Quoted text to speak")
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
    parser.add_argument(
        "--repo-id",
        default=None,
        help="Hugging Face repo id (default: hexgrad/Kokoro-82M)",
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="Play the WAV after synthesis using macOS 'afplay'",
    )
    args = parser.parse_args(argv)

    lang = args.language or args.voice[:1]
    if lang not in LANG_CODES:
        parser.error(
            f"Cannot infer language from voice '{args.voice}'. Supply --language one of {sorted(LANG_CODES)}"
        )

    frames = synth_results(args.text, lang=lang, voice=args.voice, speed=args.speed, repo_id=args.repo_id)
    write_wav(args.out, frames)
    print(f"Wrote: {args.out}")
    if args.play:
        maybe_play(args.out)


if __name__ == "__main__":
    main()
