"""Load sample healthcare policies from the samples directory."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"
PLACEHOLDER_TEXT = "[PASTE REAL POLICY TEXT HERE]"


class SamplePolicy(BaseModel):
    id: str
    title: str
    source_name: str
    source_url: str
    source_type: str
    date_accessed: str
    notes: str
    text: str


def _pair_paths(meta_path: Path) -> tuple[Path, Path]:
    """Return (txt_path, meta_path) for a metadata sidecar."""
    stem = meta_path.name.removesuffix(".meta.json")
    return SAMPLES_DIR / f"{stem}.txt", meta_path


def _load_pair(txt_path: Path, meta_path: Path) -> SamplePolicy | None:
    """Load one sample from a .txt / .meta.json pair, or None if unusable."""
    if not meta_path.exists():
        print(f"Warning: missing metadata file: {meta_path}")
        return None
    if not txt_path.exists():
        print(f"Warning: missing policy text file: {txt_path}")
        return None

    text = txt_path.read_text(encoding="utf-8")
    if PLACEHOLDER_TEXT in text:
        print(
            f"Warning: skipping {txt_path.name} - still contains "
            f"{PLACEHOLDER_TEXT!r} placeholder"
        )
        return None

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Warning: invalid JSON in {meta_path.name}: {exc}")
        return None

    return SamplePolicy(**meta, text=text)


def load_sample(policy_id: str) -> SamplePolicy | None:
    """Load a single sample by id (e.g. ``policy_01``).

    Returns None (with a console warning) if files are missing or the
    text file still has the paste placeholder.
    """
    if not SAMPLES_DIR.is_dir():
        print(f"Warning: samples directory not found: {SAMPLES_DIR}")
        return None

    meta_matches = sorted(SAMPLES_DIR.glob(f"{policy_id}_*.meta.json"))
    if not meta_matches:
        print(f"Warning: no sample found for policy_id={policy_id!r}")
        return None
    if len(meta_matches) > 1:
        print(
            f"Warning: multiple metadata files for {policy_id!r}; "
            f"using {meta_matches[0].name}"
        )

    txt_path, meta_path = _pair_paths(meta_matches[0])
    return _load_pair(txt_path, meta_path)


def list_samples() -> list[SamplePolicy]:
    """Return all loadable samples by scanning the samples folder."""
    if not SAMPLES_DIR.is_dir():
        print(f"Warning: samples directory not found: {SAMPLES_DIR}")
        return []

    samples: list[SamplePolicy] = []
    for meta_path in sorted(SAMPLES_DIR.glob("*.meta.json")):
        txt_path, meta_path = _pair_paths(meta_path)
        sample = _load_pair(txt_path, meta_path)
        if sample is not None:
            samples.append(sample)
    return samples


if __name__ == "__main__":
    loaded = list_samples()
    if not loaded:
        print("No samples loaded (all missing, or still placeholders).")
    else:
        print(f"Loaded {len(loaded)} sample(s):\n")
        for sample in loaded:
            print(f"  - {sample.id}: {sample.title!r} ({len(sample.text)} chars)")
