#!/usr/bin/env python3
"""Structural validation only; does not verify live URLs, license grants, or code claims."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

REPO_ID = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-fA-F]{40}$")
LEVELS = {"D0", "D1", "D2", "D3"}
DECISIONS = {
    "use_dependency_or_service", "copy_or_adapt", "port_or_translate",
    "study_pattern_or_tests", "defer", "reject",
}
UNKNOWN_LICENSES = {"unknown", "none", "unlicensed", "no license", "no-license", "n/a", "unspecified"}
# Local artifact safety bound, not a limit on the number of research candidates.
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_JSON_DEPTH = 64


def read_text(path: Path):
    try:
        with path.open("rb") as stream:
            content = stream.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            raise ValueError(f"exceeds {MAX_FILE_BYTES} byte artifact limit; split the research batch")
        return content.decode("utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f"{path}: {error}") from error


def load(path: Path):
    try:
        document = json.loads(read_text(path))
        pending = [(document, 0)]
        while pending:
            value, depth = pending.pop()
            if depth > MAX_JSON_DEPTH:
                raise ValueError(f"exceeds {MAX_JSON_DEPTH} levels of JSON nesting")
            if isinstance(value, dict):
                pending.extend((child, depth + 1) for child in value.values())
            elif isinstance(value, list):
                pending.extend((child, depth + 1) for child in value)
        return document
    except (ValueError, RecursionError) as error:
        raise ValueError(f"{path}: invalid, oversized, or excessively nested JSON: {error}") from error


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, *, allow_empty=False):
    return (isinstance(value, list) and (allow_empty or bool(value))
            and all(nonempty_string(item) for item in value))


def relative_path(value):
    """Portable repository-relative file path, never a URL or machine path."""
    return (nonempty_string(value) and not value.startswith("/")
            and not any(char in value for char in ("\\", ":", "\x00", "\n", "\r"))
            and all(part not in {"", ".", ".."} for part in value.split("/")))


def contained_file(root: Path, value, *, directory=None):
    if not relative_path(value):
        raise ValueError("expected a portable relative file path")
    if directory and PurePosixPath(value).parts[0] != directory:
        raise ValueError(f"expected a file under {directory}/")
    try:
        path = (root / value).resolve()
        # Keep the boundary lexical: resolving the boundary itself would allow a
        # symlinked dossiers/ directory to redefine it outside the atlas.
        path.relative_to(root / directory if directory else root)
        if not path.is_file():
            raise ValueError("file does not exist")
        return path
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError(f"{value}: file must exist inside {directory or 'atlas'}/ ({error})") from error


def pinned_paths(text, repository_id, pin):
    """Extract structurally pinned citations; no network or semantic validation."""
    paths = set()
    if not isinstance(pin, str) or not SHA.fullmatch(pin):
        return paths
    for link in re.findall(r"https://github\.com/[^\s<>\])]+", text):
        parts = urlsplit(link).path.lstrip("/").split("/", 4)
        if (len(parts) == 5 and "/".join(parts[:2]).casefold() == repository_id.casefold()
                and parts[2] == "blob" and parts[3].casefold() == pin.casefold()):
            path = unquote(parts[4])
            if relative_path(path):
                paths.add(path)
    return paths


def check(root: Path):
    root = root.resolve()
    errors = []
    for required in ("README.md", "capability-map.md", "research-gaps.md",
                     "repositories.json", "reuse-decisions.json", "progress.json"):
        try:
            contained_file(root, required)
        except ValueError as error:
            errors.append(f"missing or unsafe {required}: {error}")
    if errors:
        return errors, {}

    repos_doc = load(root / "repositories.json")
    decisions_doc = load(root / "reuse-decisions.json")
    progress = load(root / "progress.json")
    repos = repos_doc.get("repositories") if isinstance(repos_doc, dict) else None
    decisions = decisions_doc.get("decisions") if isinstance(decisions_doc, dict) else None
    if not isinstance(repos, list) or not isinstance(decisions, list):
        return ["repositories.json needs repositories[]; reuse-decisions.json needs decisions[]"], {}

    by_id = {}
    citations = {}
    for index, record in enumerate(repos):
        key = f"repositories[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{key} must be an object")
            continue
        rid, level = record.get("id"), record.get("evidence_level")
        if not isinstance(rid, str) or not REPO_ID.fullmatch(rid):
            errors.append(f"{key}: invalid owner/repository id")
            continue
        if rid.casefold() in by_id:
            errors.append(f"{key}: duplicated repository {rid}")
            continue
        by_id[rid.casefold()] = record
        if record.get("url") != f"https://github.com/{rid}":
            errors.append(f"{key}: canonical GitHub URL must match id")
        if record.get("group") not in ("direct", "component", "adjacent"):
            errors.append(f"{key}: invalid group")
        if not isinstance(level, str) or level not in LEVELS:
            errors.append(f"{key}: invalid evidence level")
        if level in ("D2", "D3"):
            pin = record.get("pinned_commit")
            if not isinstance(pin, str) or not SHA.fullmatch(pin):
                errors.append(f"{key}: D2/D3 needs a full 40-character commit SHA")
            try:
                dossier = contained_file(root, record.get("dossier"), directory="dossiers")
                citations[rid.casefold()] = pinned_paths(read_text(dossier), rid, pin)
                if not citations[rid.casefold()]:
                    errors.append(f"{key}: dossier needs a blob/file citation matching repository and commit")
            except ValueError as error:
                errors.append(f"{key}: invalid dossier: {error}")
        if not nonempty_string(record.get("license")):
            errors.append(f"{key}: nonempty license string required (use 'unknown' if unknown)")

    counts_by_status = {"selected": 0, "deferred": 0, "rejected": 0}
    seen = set()
    for index, decision_record in enumerate(decisions):
        key = f"decisions[{index}]"
        if not isinstance(decision_record, dict):
            errors.append(f"{key} must be an object")
            continue
        rid = decision_record.get("repository_id")
        if not isinstance(rid, str) or rid.casefold() not in by_id:
            errors.append(f"{key}: unknown repository_id {rid!r}")
            continue
        if rid.casefold() in seen:
            errors.append(f"{key}: duplicate decision for {rid}")
        seen.add(rid.casefold())
        decision, status = decision_record.get("decision"), decision_record.get("status")
        if not isinstance(decision, str) or decision not in DECISIONS:
            errors.append(f"{key}: invalid decision")
            continue
        expected = "deferred" if decision == "defer" else "rejected" if decision == "reject" else "selected"
        if status != expected:
            errors.append(f"{key}: status should be {expected} for {decision}")
            continue
        counts_by_status[status] += 1
        if status != "selected":
            continue
        record = by_id[rid.casefold()]
        if record.get("evidence_level") not in ("D2", "D3"):
            errors.append(f"{key}: selected source {rid} needs D2/D3 inspection")
        if decision_record.get("pinned_commit") != record.get("pinned_commit"):
            errors.append(f"{key}: selected decision pin does not match registry pin")
        if not nonempty_string(decision_record.get("why")):
            errors.append(f"{key}: selected decision needs a nonempty why string")
        for field in ("not_proven", "possible_equivalence_checks"):
            if not string_list(decision_record.get(field)):
                errors.append(f"{key}: {field} must be a nonempty list of nonempty strings")
        for field in ("upstream_files", "upstream_tests"):
            values = decision_record.get(field, [] if field == "upstream_tests" else None)
            if not string_list(values, allow_empty=field == "upstream_tests"):
                errors.append(f"{key}: {field} must be a list of file paths")
                continue
            for value in values:
                if not relative_path(value):
                    errors.append(f"{key}: {field} contains an invalid repository-relative path")
                elif value not in citations.get(rid.casefold(), set()):
                    errors.append(f"{key}: {value} needs a matching pinned citation in its dossier")
        license_name = record.get("license")
        if decision in {"copy_or_adapt", "port_or_translate"} and (
                not nonempty_string(license_name) or license_name.strip().casefold() in UNKNOWN_LICENSES):
            errors.append(f"{key}: cannot recommend copying/porting without known reuse license")

    counts = {
        "discovered": len(by_id),
        "metadata_verified_or_more": sum(r.get("evidence_level") in ("D1", "D2", "D3") for r in by_id.values()),
        "code_inspected_or_more": sum(r.get("evidence_level") in ("D2", "D3") for r in by_id.values()),
        "reproduced": sum(r.get("evidence_level") == "D3" for r in by_id.values()),
        **counts_by_status,
    }
    recorded = progress.get("counts") if isinstance(progress, dict) else None
    if not isinstance(recorded, dict):
        errors.append("progress.json needs counts{}")
    else:
        for name, value in counts.items():
            if type(recorded.get(name)) is not int or recorded[name] != value:
                errors.append(f"progress counts.{name}={recorded.get(name)!r}; actual={value}")
    if (root / "implementation-roadmap.md").exists():
        errors.append("implementation-roadmap.md is outside research-only scope")
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="path to docs/research/reuse (or chosen atlas folder)")
    args = parser.parse_args()
    try:
        errors, counts = check(Path(args.root))
    except (ValueError, OSError, RecursionError, RuntimeError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 2
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(json.dumps({"ok": not errors, "counts": counts, "issues": len(errors)}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
