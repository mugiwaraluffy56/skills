#!/usr/bin/env python3
"""Structural validation only. Does not verify GitHub URLs, copyrights, or code claims."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ID = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-fA-F]{40}$")
LEVELS = {"D0", "D1", "D2", "D3"}
DECISIONS = {
    "use_dependency_or_service", "copy_or_adapt", "port_or_translate",
    "study_pattern_or_tests", "defer", "reject"
}
ACTIONABLE = DECISIONS - {"defer", "reject"}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as e:
        raise ValueError(f"{path}: {e}") from e


def check(root: Path):
    errors = []
    for req in ("README.md", "capability-map.md", "research-gaps.md",
                "repositories.json", "reuse-decisions.json", "progress.json"):
        if not (root / req).is_file():
            errors.append(f"missing {req}")
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
    for i, r in enumerate(repos):
        key = f"repositories[{i}]"
        if not isinstance(r, dict):
            errors.append(f"{key} must be an object")
            continue
        rid = r.get("id")
        level = r.get("evidence_level")
        if not isinstance(rid, str) or not REPO_ID.fullmatch(rid):
            errors.append(f"{key}: invalid owner/repository id")
            continue
        if rid.lower() in by_id:
            errors.append(f"{key}: duplicated repository {rid}")
        by_id[rid.lower()] = r
        if r.get("url") != f"https://github.com/{rid}":
            errors.append(f"{key}: canonical GitHub URL must match id")
        if r.get("group") not in {"direct", "component", "adjacent"}:
            errors.append(f"{key}: invalid group")
        if level not in LEVELS:
            errors.append(f"{key}: invalid evidence level")
        if level in {"D2", "D3"}:
            if not SHA.fullmatch(str(r.get("pinned_commit") or "")):
                errors.append(f"{key}: D2/D3 needs a real full 40-character commit SHA")
            dossier = r.get("dossier")
            if not isinstance(dossier, str) or not dossier.startswith("dossiers/") or not (root / dossier).is_file():
                errors.append(f"{key}: D2/D3 needs existing relative dossier under dossiers/")
        if r.get("license") is None:
            errors.append(f"{key}: license required (use 'unknown' if unknown)")

    count_selected = count_deferred = count_rejected = 0
    seen = set()
    for i, d in enumerate(decisions):
        key = f"decisions[{i}]"
        if not isinstance(d, dict):
            errors.append(f"{key} must be an object")
            continue
        rid = d.get("repository_id")
        if not isinstance(rid, str) or rid.lower() not in by_id:
            errors.append(f"{key}: unknown repository_id {rid!r}")
            continue
        if rid.lower() in seen:
            errors.append(f"{key}: duplicate decision for {rid}")
        seen.add(rid.lower())
        decision = d.get("decision")
        status = d.get("status")
        if decision not in DECISIONS:
            errors.append(f"{key}: invalid decision")
        expected = "deferred" if decision == "defer" else "rejected" if decision == "reject" else "selected"
        if status != expected:
            errors.append(f"{key}: status should be {expected} for {decision}")
        if status == "selected":
            count_selected += 1
            r = by_id[rid.lower()]
            if r.get("evidence_level") not in {"D2", "D3"}:
                errors.append(f"{key}: selected source {rid} needs D2/D3 inspection")
            if d.get("pinned_commit") != r.get("pinned_commit"):
                errors.append(f"{key}: selected decision pin does not match registry pin")
            for f in ("why", "upstream_files", "not_proven", "possible_equivalence_checks"):
                if not d.get(f):
                    errors.append(f"{key}: selected decision missing {f}")
            if decision in {"copy_or_adapt", "port_or_translate"} and r.get("license") in {"unknown", "none", "UNLICENSED"}:
                errors.append(f"{key}: cannot recommend copying/porting without known reuse license")
        elif status == "deferred":
            count_deferred += 1
        elif status == "rejected":
            count_rejected += 1

    counts = {
        "discovered": len(by_id),
        "metadata_verified_or_more": sum(r.get("evidence_level") in {"D1", "D2", "D3"} for r in by_id.values()),
        "code_inspected_or_more": sum(r.get("evidence_level") in {"D2", "D3"} for r in by_id.values()),
        "reproduced": sum(r.get("evidence_level") == "D3" for r in by_id.values()),
        "selected": count_selected,
        "deferred": count_deferred,
        "rejected": count_rejected,
    }
    recorded = progress.get("counts") if isinstance(progress, dict) else None
    if not isinstance(recorded, dict):
        errors.append("progress.json needs counts{}")
    else:
        for k, v in counts.items():
            if recorded.get(k) != v:
                errors.append(f"progress counts.{k}={recorded.get(k)!r}; actual={v}")
    if (root / "implementation-roadmap.md").exists():
        errors.append("implementation-roadmap.md is outside research-only scope")
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="path to docs/research/reuse (or chosen atlas folder)")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        errors, counts = check(root)
    except ValueError as e:
        print(f"INVALID: {e}", file=sys.stderr)
        return 2
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
    print(json.dumps({"ok": not errors, "counts": counts, "issues": len(errors)}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
