PY ?= python3.11
VENV := .venv
PYBIN := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install synth

venv: $(PYBIN)
$(PYBIN):
	$(PY) -m venv $(VENV)

install: venv
	$(PIP) install -U pip
	$(PIP) install -e .
	$(PIP) install kokoro

simpler-install-cli: venv
	$(PIP) install -e . --no-deps

prefetch:
	HF_HOME="$(PWD)/.hf_cache" $(VENV)/bin/python scripts/prefetch_kokoro.py

synth:
	$(VENV)/bin/speak -v af_heart --play "Hello from Kokoro on Apple Silicon"
