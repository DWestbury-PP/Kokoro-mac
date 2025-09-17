PY ?= python3.11
VENV := .venv
PYBIN := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install synth simpler-install-cli dev-reinstall install-copy prefetch run

venv: $(PYBIN)
$(PYBIN):
	$(PY) -m venv $(VENV)

install: venv
	$(PIP) install -U pip
	$(PIP) install -e .
	$(PIP) install kokoro

simpler-install-cli: venv
	$(PIP) install -e . --no-deps

dev-reinstall: venv
	$(PIP) install -e . --no-deps

install-copy: venv
	$(PIP) install . --no-deps

prefetch:
	HF_HOME="$(PWD)/.hf_cache" $(VENV)/bin/python scripts/prefetch_kokoro.py

run:
	$(VENV)/bin/speak -v af_heart "Hello from Kokoro on Apple Silicon"

synth: run
