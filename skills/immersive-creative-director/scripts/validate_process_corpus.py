#!/usr/bin/env python3

"""Validate the process-video corpus without assigning it visual-taste authority."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_COUNTS = {
    "video-QUI6Ug4cHnE": 22,
    "video-39IlNR-P3-Q": 23,
    "video-GJxchJkk4Lk": 9,
    "video-ubH1ulaK-t4": 18,
}


def validate(skill_root):
    errors = []
    corpus_root = skill_root / "assets" / "process-corpus"
    manifest_path = corpus_root / "manifest.json"
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid manifest: {error}"]

    references = manifest.get("references")
    if not isinstance(references, list):
        return ["manifest.references must be a list"]
    by_id = {item.get("id"): item for item in references if isinstance(item, dict)}
    if set(by_id) != set(EXPECTED_COUNTS):
        errors.append("process corpus must contain exactly the four declared video IDs")

    total = 0
    for reference_id, expected_count in EXPECTED_COUNTS.items():
        reference = by_id.get(reference_id)
        if not reference:
            continue
        if reference.get("visualAuthority") != "demonstration-only":
            errors.append(f"{reference_id}: visualAuthority must be demonstration-only")
        frames = reference.get("frames")
        if not isinstance(frames, list) or len(frames) != expected_count:
            errors.append(f"{reference_id}: expected {expected_count} archived demonstration frames")
            continue
        total += len(frames)
        for frame in frames:
            path = corpus_root / frame.get("file", "")
            if not path.is_file():
                errors.append(f"{reference_id}: missing demonstration frame {path}")
        transcript = corpus_root / reference.get("transcript", "")
        if not transcript.is_file():
            errors.append(f"{reference_id}: missing transcript {transcript}")
            continue
        data = transcript.read_bytes()
        if not data.startswith(b"WEBVTT") or len(data) < 1_000:
            errors.append(f"{reference_id}: transcript is not a substantive WebVTT file")
        if reference.get("transcriptBytes") != len(data):
            errors.append(f"{reference_id}: transcript byte-count mismatch")
        if reference.get("transcriptSha256") != hashlib.sha256(data).hexdigest():
            errors.append(f"{reference_id}: transcript checksum mismatch")

    if total != 72 or manifest.get("frameCount") != 72:
        errors.append(f"process corpus must retain 72 demonstration frames; observed {total}")

    readable = skill_root / "references" / "process-reference-manifest.md"
    if not readable.is_file():
        errors.append("missing references/process-reference-manifest.md")
    else:
        text = readable.read_text()
        for reference_id in EXPECTED_COUNTS:
            if reference_id not in text:
                errors.append(f"readable process manifest omits {reference_id}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", nargs="?", default=Path(__file__).parent.parent)
    args = parser.parse_args()
    errors = validate(Path(args.skill_root).resolve())
    if errors:
        print("Process corpus validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Process corpus valid: 4 videos, 4 full transcripts, 72 archived demonstration frames.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
