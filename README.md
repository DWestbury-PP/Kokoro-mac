# Kokoro Speak Demo

A minimal, CPU‑only Text‑to‑Speech CLI for Apple Silicon built on the Kokoro 82M vocoder‑based model. It installs a `speak` command that reads arbitrary text with selectable voices, plays audio by default, and keeps output quiet and clean.

## Features
- Simple CLI: `speak "Your text" -v <voice>`
- Voices and languages (e.g., `af_heart`, US English `-l a`)
- Quiet output by default; audio auto‑plays (use `--no-play` to skip)
- Optional offline mode using a local HF cache (`.hf_cache`)

## Requirements
- macOS on Apple Silicon (arm64), Python 3.11+
- CPU‑only Torch and Kokoro

## Setup
- Create a venv and install the CLI (non‑editable):
  - `python3.11 -m venv .venv && source .venv/bin/activate`
  - `pip install . --no-deps --no-build-isolation`
  - Install runtime deps (if not yet installed): `pip install torch kokoro`
- Optional: prefetch model files into local cache for offline runs:
  - `export HF_HOME="$(pwd)/.hf_cache"`
  - `make prefetch`

## Usage
- Basic (playback + quiet by default):
  - `speak -v af_heart "Hello from Kokoro"`
- Show output file path:
  - `speak --print-path -v af_heart "Hello"` → writes `out.wav`
- Skip playback:
  - `speak --no-play -v af_heart "Hello"`
- Specify language or repo explicitly:
  - `speak -l a -v af_heart "US English"`
  - `speak --repo-id hexgrad/Kokoro-82M-v1.1-zh -l z -v zf_xxx "你好"`
- Offline once cached:
  - `HF_HUB_OFFLINE=1 speak -v af_heart "Local cache run"`

Makefile helpers: `make install-copy`, `make run`, `make prefetch`.

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
