#!/usr/bin/env python3

"""Validate the mandatory visual-reference corpus packaged with the skill."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_COUNTS = {
    "site-sondaven": 55,
    "site-lando-norris": 22,
    "site-indigo-laboratory": 11,
    "site-noth": 40,
    "site-mr-black": 14,
    "site-santioni-spirits": 30,
    "site-become-a-yogi": 38,
    "site-mesh3d": 44,
    "site-haoqi": 17,
    "site-ride-radian": 15,
    "site-pear": 35,
    "video-QUI6Ug4cHnE": 22,
    "video-39IlNR-P3-Q": 23,
    "video-GJxchJkk4Lk": 9,
    "video-ubH1ulaK-t4": 18,
}


def jpeg_is_complete(path):
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9") and b"\xff\xda" in data


def validate(skill_root):
    errors = []
    corpus_root = skill_root / "assets" / "reference-corpus"
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
    by_id = {reference.get("id"): reference for reference in references if isinstance(reference, dict)}
    if set(by_id) != set(EXPECTED_COUNTS):
        errors.append(
            "reference IDs differ: expected "
            + ", ".join(sorted(EXPECTED_COUNTS))
            + "; got "
            + ", ".join(sorted(str(item) for item in by_id))
        )

    observed_total = 0
    observed_hashes = set()
    for reference_id, expected_count in EXPECTED_COUNTS.items():
        reference = by_id.get(reference_id)
        if not reference:
            continue
        frames = reference.get("frames")
        if not isinstance(frames, list):
            errors.append(f"{reference_id}: frames must be a list")
            continue
        if len(frames) != expected_count or reference.get("frameCount") != expected_count:
            errors.append(
                f"{reference_id}: expected {expected_count} frames; "
                f"manifest reports {reference.get('frameCount')} and lists {len(frames)}"
            )
        observed_total += len(frames)
        for frame in frames:
            relative = frame.get("file", "")
            frame_path = corpus_root / relative
            if not frame_path.is_file():
                errors.append(f"{reference_id}: missing frame {relative}")
                continue
            if not jpeg_is_complete(frame_path):
                errors.append(f"{reference_id}: undecodable JPEG {relative}")
            digest = hashlib.sha256(frame_path.read_bytes()).hexdigest()
            if digest != frame.get("sha256"):
                errors.append(f"{reference_id}: checksum mismatch {relative}")
            if frame.get("bytes") != frame_path.stat().st_size:
                errors.append(f"{reference_id}: byte-count mismatch {relative}")
            observed_hashes.add(digest)

        overview = corpus_root / reference.get("overview", "")
        if not overview.is_file() or not jpeg_is_complete(overview):
            errors.append(f"{reference_id}: missing or undecodable overview {overview}")

    if observed_total != 393 or manifest.get("frameCount") != 393:
        errors.append(
            f"complete corpus must contain 393 frames; observed {observed_total}, "
            f"manifest reports {manifest.get('frameCount')}"
        )
    if len(observed_hashes) < 391:
        errors.append(f"unexpected duplicate collapse: only {len(observed_hashes)} unique frame hashes")

    master = corpus_root / "corpus-overview.jpg"
    if not master.is_file() or not jpeg_is_complete(master):
        errors.append("missing or undecodable corpus-overview.jpg")

    readable_manifest = skill_root / "references" / "visual-reference-manifest.md"
    if not readable_manifest.is_file():
        errors.append("missing references/visual-reference-manifest.md")
    else:
        readable = readable_manifest.read_text()
        for reference_id in EXPECTED_COUNTS:
            if reference_id not in readable:
                errors.append(f"readable manifest omits {reference_id}")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", nargs="?", default=Path(__file__).parent.parent)
    args = parser.parse_args()
    skill_root = Path(args.skill_root).resolve()
    errors = validate(skill_root)
    if errors:
        print("Visual corpus validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Visual corpus valid: 15 references, 393 frames, 15 overview sheets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
