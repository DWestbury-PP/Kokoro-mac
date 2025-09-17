# Repository Guidelines

## Project Structure & Module Organization
- **Source:** `src/kokoro/` (text processing, acoustic model, vocoder). Typical modules: `text/`, `acoustic/`, `vocoder/`, `cli.py`.
- **Models:** `models/` for the 82M Kokoro checkpoints and vocoder weights (gitignored; use download scripts).
- **Assets:** `assets/` for lexicons, phoneme maps, and default voices.
- **Scripts:** `scripts/` for conversion, export, and benchmarking.
- **Tests:** `tests/` mirroring `src/` packages; include small audio fixtures where necessary.

## Build, Test, and Development Commands
- `python3 -m venv .venv && source .venv/bin/activate`: Create/activate Apple Silicon (arm64) venv.
- `pip install -e .[dev]`: Install Kokoro and dev tools (ruff/black/pytest/mypy).
- `pip install torch --index-url https://download.pytorch.org/whl/cpu` or `pip install onnxruntime`: Choose backend (CPU-only).
- `pytest -q`: Run unit tests. Add `-k <name>` to filter.
- `python -m kokoro.cli --text "Hello, world" --voice en_US/neutral --out out.wav`: Synthesize speech locally.
- `make setup | make test | make synth`: Prefer if a `Makefile` is present.

## Coding Style & Naming Conventions
- **Language:** Python 3.10+; 4-space indent; target 100–120 cols.
- **Names:** lower_snake_case for functions/vars; UpperCamelCase for classes; SCREAMING_SNAKE_CASE for constants.
- **Formatting/Linting:** `ruff check .`, `black .`, `mypy src/` before committing.
- **Model code:** Keep acoustic and vocoder layers separate; avoid side effects in `__init__.py`.

## Testing Guidelines
- **Framework:** `pytest`. Place tests in `tests/<module>/test_*.py`.
- **Determinism:** Seed via `KOKORO_SEED=0` and disable randomness in tests.
- **Coverage:** Focus on text normalization, phonemization, batching, and streaming. Aim ≥80% on core logic.
- **Golden audio:** Use short (<1s) clips; store in `tests/data/` and check basic metrics (shape, RMS).

## Commit & Pull Request Guidelines
- **Commits:** Imperative mood; small, focused changes. Conventional Commits welcome (`feat:`, `fix:`, `perf:`).
- **PRs:** Include a summary, sample command/output (`out.wav` as artifact, not committed), and linked issues. Ensure tests, lint, and format pass.

## Apple Silicon (CPU) Performance Tips
- Ensure arm64 Python (not Rosetta): `python -c "import platform;print(platform.machine())"` → `arm64`.
- Set threads: `export OMP_NUM_THREADS=$(sysctl -n hw.physicalcpu_max)`; optionally `VECLIB_MAXIMUM_THREADS=$OMP_NUM_THREADS`.
- Batch phoneme sequences; prefer float16 weights where supported by backend even on CPU if safe.

## Security & Model Assets
- Do not commit weights; use Git LFS or scripted downloads into `models/`.
- Keep any API keys/voices private; store in `.env` and reference via `KOKORO_*` environment variables.
