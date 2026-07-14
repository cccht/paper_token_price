from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pickle

import numpy as np

CACHE_FORMAT_VERSION = 1


def cache_signature(identity: dict, source_paths: tuple[Path, ...]) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode())
    for path in source_paths:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _vector_key(vector: np.ndarray) -> tuple[float, ...]:
    return tuple(float(value) for value in np.asarray(vector, dtype=float))


def write_vector_pair_cache(
    path: Path,
    signature: str,
    grid: np.ndarray,
    records: dict[tuple[int, int], dict],
) -> None:
    path = Path(path)
    vector_records = {
        (_vector_key(grid[row]), _vector_key(grid[col])): record
        for (row, col), record in records.items()
    }
    payload = {
        "format_version": CACHE_FORMAT_VERSION,
        "signature": signature,
        "records": vector_records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
    temporary.replace(path)


def load_vector_pair_cache(
    path: Path, signature: str, grid: np.ndarray
) -> dict[tuple[int, int], dict]:
    path = Path(path)
    if not path.exists():
        return {}
    with path.open("rb") as stream:
        payload = pickle.load(stream)
    if (
        payload.get("format_version") != CACHE_FORMAT_VERSION
        or payload.get("signature") != signature
    ):
        return {}
    indices = {_vector_key(vector): index for index, vector in enumerate(grid)}
    output = {}
    records = payload["records"]
    while records:
        (row_vector, col_vector), record = records.popitem()
        if row_vector in indices and col_vector in indices:
            output[(indices[row_vector], indices[col_vector])] = record
    return output
