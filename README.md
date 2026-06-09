# Kokoro Speak Demo

A high-performance Text‑to‑Speech CLI for Apple Silicon built on the Kokoro 82M vocoder‑based model. Optimized for Apple Silicon GPUs with MPS acceleration, it installs a `speak` command that reads arbitrary text with selectable voices, plays audio by default, and keeps output quiet and clean.

## Features
- Simple CLI: `speak "Your text" -v <voice>`
- **Command pipe support** - pipe text from other commands or files
- **Apple Silicon GPU acceleration** with MPS (Metal Performance Shaders)
- **Auto-device detection** - automatically uses GPU when available
- Voices and languages (e.g., `af_heart`, US English `-l a`)
- Quiet output by default; audio auto‑plays (use `--no-play` to skip)
- Optional offline mode using a local HF cache (`.hf_cache`)

## Requirements
- macOS on Apple Silicon (arm64), Python 3.11+
- PyTorch with MPS support and Kokoro

## Setup
- Create a venv and install the CLI in editable mode:
  - `python3.11 -m venv .venv && source .venv/bin/activate`
  - `pip install -e .`
- Optional: prefetch model files into local cache for offline runs:
  - `export HF_HOME="$(pwd)/.hf_cache"`
  - `make prefetch`

> **iCloud / synced-folder users:** if the repo lives under `~/Documents` or `~/Desktop`
> with iCloud Drive enabled, prefer a **copy install** over editable — see Troubleshooting.

## Troubleshooting

### `ModuleNotFoundError: No module named 'speak_cli'`
This usually means the editable install's `.pth` link is being ignored by Python, **not** that
anything is wrong with the code.

**Why it happens:** modern CPython (3.11.13+, 3.12+) hardened `site.py` to silently skip `.pth`
files that carry the macOS **hidden** filesystem flag. iCloud Drive (and some backup/sync tools)
likes to set that flag on files inside synced folders such as `~/Documents` — including the
editable-install `.pth` in your `.venv`. Once it's hidden, the `speak_cli` package becomes
invisible and the `speak` entry point can't import it.

**Diagnose:**
```bash
ls -lO .venv/lib/python3.11/site-packages/*.pth        # a "hidden" flag is the culprit
python -v -c pass 2>&1 | grep -i "skipping hidden"     # CPython tells you it skipped them
```

**Fix (recommended — install by copy, no `.pth` to hide):**
```bash
pip uninstall -y kokoro-speak-demo
pip install . --no-deps      # or: make install-copy
```
The package is copied straight into `site-packages`, so there's nothing for iCloud to hide.
Trade-off: edits to `src/` require re-running the install to take effect.

**Quick fix (keep editable install):**
```bash
chflags nohidden .venv/lib/python3.11/site-packages/*.pth
```
This works immediately but can recur if the sync service re-hides the file.

## Usage
- Basic (playback + quiet by default):
  - `speak -v af_heart "Hello from Kokoro"`
- **Piped input from commands or files:**
  - `echo "Hello world" | speak -v af_heart`
  - `cat article.txt | speak -v am_adam --no-play --out article.wav`
  - `fortune | speak -v af_bella`
  - `pbpaste | speak -v af_sky` (speak clipboard contents on macOS)
- Show output file path:
  - `speak --print-path -v af_heart "Hello"` → writes `out.wav`
- Skip playback:
  - `speak --no-play -v af_heart "Hello"`
- Specify language or repo explicitly:
  - `speak -l a -v af_heart "US English"`
  - `speak --repo-id hexgrad/Kokoro-82M-v1.1-zh -l z -v zf_xxx "你好"`
- Offline once cached:
  - `HF_HUB_OFFLINE=1 speak -v af_heart "Local cache run"`
- Device selection:
  - `speak --device auto "Auto-detect best device"` (default)
  - `speak --device mps "Force GPU acceleration"`
  - `speak --device cpu "Force CPU-only"`

Makefile helpers: `make install-copy`, `make run`, `make prefetch`.

## System-Wide Installation (Optional)

For convenient access to the `speak` command from anywhere in your terminal without needing to navigate to this directory or activate the virtual environment:

### Option 1: Global System Command (Recommended)
```bash
./install_global_speak.sh
```
- Creates `/usr/local/bin/speak` that works from any directory
- Automatically handles virtual environment activation
- Requires sudo for installation
- Most seamless "set and forget" experience

### Option 2: Shell Alias
```bash
./setup_shell_alias.sh
```
- Adds an alias to your `~/.zshrc`
- Works from any directory after shell restart (`source ~/.zshrc`)
- No sudo required
- Requires terminal restart or manual sourcing

After either installation, you can use `speak` globally:
```bash
speak "Hello from anywhere!" --voice af_heart
speak "Testing voices" --voice am_adam --out ~/Desktop/test.wav --no-play
echo "Piped text works too" | speak --voice af_bella
cat ~/Documents/book.txt | speak --voice am_liam --no-play --out ~/audiobook.wav
```

## Performance

The tool automatically detects and uses the best available device:

- **Apple Silicon GPU (MPS)**: Optimized for M1/M2/M3 chips with Metal Performance Shaders
- **CPU fallback**: Uses optimized CPU inference when GPU is unavailable
- **Auto-detection**: Automatically selects the fastest available option

GPU acceleration provides significant performance improvements for longer texts and batch processing.

## Available Voices
The following voices are available in the default Kokoro repository (`hexgrad/Kokoro-82M`). Use with `-v <voice>`; language is inferred from the prefix.

| Voice ID        | Language            |
|-----------------|---------------------|
| af_alloy        | American English    |
| af_aoede        | American English    |
| af_bella        | American English    |
| af_heart        | American English    |
| af_jessica      | American English    |
| af_kore         | American English    |
| af_nicole       | American English    |
| af_nova         | American English    |
| af_river        | American English    |
| af_sarah        | American English    |
| af_sky          | American English    |
| am_adam         | American English    |
| am_echo         | American English    |
| am_eric         | American English    |
| am_fenrir       | American English    |
| am_liam         | American English    |
| am_michael      | American English    |
| am_onyx         | American English    |
| am_puck         | American English    |
| am_santa        | American English    |
| bf_alice        | British English     |
| bf_emma         | British English     |
| bf_isabella     | British English     |
| bf_lily         | British English     |
| bm_daniel       | British English     |
| bm_fable        | British English     |
| bm_george       | British English     |
| bm_lewis        | British English     |
| ef_dora         | Spanish             |
| em_alex         | Spanish             |
| em_santa        | Spanish             |
| ff_siwis        | French              |
| hf_alpha        | Hindi               |
| hf_beta         | Hindi               |
| hm_omega        | Hindi               |
| hm_psi          | Hindi               |
| if_sara         | Italian             |
| im_nicola       | Italian             |
| jf_alpha        | Japanese            |
| jf_gongitsune   | Japanese            |
| jf_nezumi       | Japanese            |
| jf_tebukuro     | Japanese            |
| jm_kumo         | Japanese            |
| pf_dora         | Brazilian Portuguese|
| pm_alex         | Brazilian Portuguese|
| pm_santa        | Brazilian Portuguese|
| zf_xiaobei      | Mandarin Chinese    |
| zf_xiaoni       | Mandarin Chinese    |
| zf_xiaoxiao     | Mandarin Chinese    |
| zf_xiaoyi       | Mandarin Chinese    |
| zm_yunjian      | Mandarin Chinese    |
| zm_yunxi        | Mandarin Chinese    |
| zm_yunxia       | Mandarin Chinese    |
| zm_yunyang      | Mandarin Chinese    |

## What’s Ignored (safe to push)
- Virtualenvs, caches, build artifacts, audio, and model assets (see `.gitignore`): `.venv/`, `.hf_cache/`, `*.wav`, `models/`, `checkpoints/`, `downloads/`, `__pycache__/`, `*.egg-info/`, `build/`, `dist/`.

## Acknowledgements
- Built against the official Kokoro repo: https://github.com/hexgrad/kokoro
