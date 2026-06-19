from __future__ import annotations

import subprocess
from typing import Any

import requests


def _run(command: list[str]) -> str | None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def collect_runtime_metadata(endpoint: str, model: str) -> dict[str, Any]:
    gpu = _run(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total",
            "--format=csv,noheader,nounits",
        ]
    )
    ollama_version = _run(["ollama", "--version"])
    details: dict[str, Any] = {}
    try:
        response = requests.post(
            f"{endpoint}/api/show",
            json={"model": model},
            timeout=10,
        )
        response.raise_for_status()
        details = response.json().get("details", {})
    except requests.RequestException:
        details = {}
    return {
        "backend": "ollama",
        "ollama_version": ollama_version,
        "gpu": gpu,
        "model_details": details,
    }


def collect_vllm_runtime_metadata(endpoint: str, model: str) -> dict[str, Any]:
    gpu = _run(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total",
            "--format=csv,noheader,nounits",
        ]
    )
    versions = {
        name: _run(["python", "-c", f"import {name}; print({name}.__version__)"])
        for name in ("torch", "vllm")
    }
    try:
        response = requests.get(f"{endpoint}/v1/models", timeout=10)
        response.raise_for_status()
        served_models = response.json()
    except requests.RequestException:
        served_models = {}
    return {
        "backend": "vllm",
        "model": model,
        "gpu": gpu,
        "versions": versions,
        "served_models": served_models,
    }
