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

synth:
	$(VENV)/bin/speak -v af_heart --play "Hello from Kokoro on Apple Silicon"

