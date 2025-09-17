#!/usr/bin/env python3
"""
Prefetch Kokoro model and voices into the local Hugging Face cache.

Downloads only the required files (config, checkpoint, voices) for CPU use.
Respects HF_HOME; defaults to ./.hf_cache to keep binaries out of your home dir.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from huggingface_hub import snapshot_download


def main() -> None:
    repo_id = os.environ.get("KOKORO_REPO", "hexgrad/Kokoro-82M")
    hf_home = os.environ.get("HF_HOME")
    if not hf_home:
        hf_home = str(Path.cwd() / ".hf_cache")
        os.environ["HF_HOME"] = hf_home
        print(f"[info] HF_HOME not set. Using local cache: {hf_home}")

    # Optionally speed up downloads (requires `pip install hf_transfer`)
    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")

    print(f"[info] Prefetching {repo_id} into HF cache at {os.environ['HF_HOME']}")
    path = snapshot_download(
        repo_id=repo_id,
        allow_patterns=[
            "config.json",
            "kokoro-v1_0.pth",
            "kokoro-v1_1-zh.pth",
            "voices/*.pt",
        ],
        local_dir=None,  # use HF cache structure under HF_HOME
        local_dir_use_symlinks=False,
        max_workers=8,
        tqdm_class=None,  # use default progress
        ignore_patterns=None,
    )
    print(f"[ok] Cached model files under: {path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[warn] Prefetch cancelled by user.")
        sys.exit(1)

