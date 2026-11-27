#!/usr/bin/env python3
"""Check explicit slice contracts without expanding ownership globs."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path, PurePosixPath
import re


HEADER = re.compile(r"^#{2,4} (L(\d+)([A-Z]+))(?: (\S+))?\. (.+)$", re.M)
STATUS_ROW = re.compile(r"^\|\s*`?(L\d+[A-Z]+)`?\s*\|(.*)$", re.M)
HEAVY_ABOVE = 15
LABELS = ("easy", "easy-ui", "hard", "hard-ui")
SHARED = {"AGENTS.md", "lessons.md"}
SHARED_PREFIXES = (".github/", "scripts/ci/", "lessons/", "backend/alembic/versions/", "migrations/")
LOCKFILES = {"Cargo.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock"}
OUTSIDE_LAYER = re.compile(
    r"\bparent[- ](?:PRs?|queues?|lanes?|controlled|owned|slices?|migrations?|work)\b"
    r"|\brouter lanes?\b|\bmigration lanes?\b"
    r"|\bsetup (?:steps?|PRs?|queues?|lanes?|layers?|slices?|work|phase)\b"
    r"|^#{1,6}[ \t]+setup\b|\bPQ\d+\b"
    r"|^#{1,6}[ \t]+(?!L\d)[A-Z]{1,3}\d+[A-Z]?\.[ \t]"
    r"|^\|\s*(?!L\d+[A-Z]+\s*\|)[A-Z]+\d+[A-Z]?\s*\|\s*(?:parent|easy|easy-ui|hard|hard-ui)\s*\|",
    re.I | re.M,
)
KIND_LINE = re.compile(r"^Kind:[ \t]*([a-z-]+)", re.M)
LENS_LINE = re.compile(r"^Lens:[ \t]*([a-z-]+)", re.M)
BENCH_LINE = re.compile(r"^Bench:[ \t]*`?(L\d+[A-Z]+)\b", re.M)
KINDS = ("build", "review", "climb", "bench", "port")
SOLO_KINDS = {"review", "climb", "bench"}
UNCOUNTED_KINDS = {"bench"}
LENSES = {
    "full-tests": "audit/references/full-tests.md",
    "silent-failures": "audit/references/silent-failure-hunter.md",
    "test-quality": "audit/references/pr-test-analyzer.md",
    "type-design": "audit/references/type-design-analyzer.md",
    "thermo-nuclear": "audit/references/thermo-nuclear-code-quality-review.md",
    "performance": "audit/references/performance-profiler.md",
    "security": "security/SKILL.md",
    "ui-polish": "audit/references/ui-polish.md",
    "formal-verification": "audit/references/formal-verification.md",
    "port-proof": "build/references/port-proof.md",
    "area": "audit/SKILL.md",
}
REQUIRED_LENSES = ("full-tests",)
MAX_BUILD_RUN = 3
MANIFESTS = {"package.json", "Cargo.toml", "pyproject.toml"}
SOURCE_TEXT_PROOF = re.compile(r"static dead[- ]owner absence|source[- ]text (?:deleted[- ]name absence|syntax)", re.I)
SCHEDULE_LINE = re.compile(r"^Schedule:[ \t]*needs-graph\s*$", re.M)
MODEL_LINE = re.compile(r"^Model:[ \t]*\S", re.M)
NEEDS_LINE = re.compile(r"^Needs:[ \t]*(.+)$", re.M)
DEPENDS_LINE = re.compile(r"^Depends:[ \t]*(.+)$", re.M)
SLICE_ID = re.compile(r"L\d+[A-Z]+")


def letter_number(letters: str) -> int:
    value = 0
    for letter in letters:
        value = value * 26 + ord(letter) - ord("A") + 1
    return value


def shared_group(file: str) -> str | None:
    """Shared control paths: one slice per layer may own each group."""
    name = Path(file).name
    if file in SHARED or name in SHARED:
        return name
    if name in LOCKFILES:
        return file
    for prefix in SHARED_PREFIXES:
        if file.startswith(prefix):
            return prefix
    return None


def slice_kind(body: str) -> str:
    match = KIND_LINE.search(body)
    return match.group(1) if match else "build"


def is_manifest(file: str) -> bool:
    name = Path(file).name
    return name in MANIFESTS or name in LOCKFILES or (name.startswith("requirements") and name.endswith((".txt", ".lock")))


def slice_bodies(texts: list[str]) -> dict[str, tuple[int, str]]:
    found: dict[str, tuple[int, str]] = {}
    for text in texts:
        headers = list(HEADER.finditer(text))
        for index, match in enumerate(headers):
            end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
            found.setdefault(match.group(1), (int(match.group(2)), text[match.end():end]))
    return found


def layer_kinds(texts: list[str]) -> dict[int, set[str]]:
    kinds: dict[int, set[str]] = defaultdict(set)
    for layer, body in slice_bodies(texts).values():
        kinds[layer].add(slice_kind(body))
    return kinds


def kind_errors(slice_id: str, layer: int, kind: str, body: str, every: dict[str, tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    if kind not in KINDS:
        errors.append(f"{slice_id}: kind {kind} is not one of {', '.join(KINDS)}")
    if kind == "climb":
        errors.extend(f"{slice_id}: climb slice missing {label}" for label in ("Rubric", "Baseline") if not re.search(rf"^{label}:[ \t]*\S", body, re.M))
    if kind == "bench" and not re.search(r"^Measures:[ \t]*\S", body, re.M):
        errors.append(f"{slice_id}: bench slice missing Measures")
    if kind == "review":
        lens = LENS_LINE.search(body)
        if not lens:
            errors.append(f"{slice_id}: review slice missing Lens; use one of {', '.join(LENSES)}")
        elif lens.group(1) not in LENSES:
            errors.append(f"{slice_id}: lens {lens.group(1)} is not one of {', '.join(LENSES)}")
    if kind == "port":
        bench = BENCH_LINE.search(body)
        target = every.get(bench.group(1)) if bench else None
        if not bench:
            errors.append(f"{slice_id}: port slice missing 'Bench: <bench slice id>' from an earlier layer")
        elif target is None or slice_kind(target[1]) != "bench" or target[0] >= layer:
            errors.append(f"{slice_id}: Bench {bench.group(1)} must be a Kind: bench slice in an earlier layer")
    return errors


def cadence_errors(kinds: dict[int, set[str]], bodies: dict[int, list[str]]) -> list[str]:
    errors: list[str] = []
    run: list[int] = []
    for layer in sorted(kinds):
        found = kinds[layer]
        if "review" in found and found & {"build", "port"}:
            errors.append(f"L{layer}: mixes review and build slices; a review layer holds only review, climb and bench slices")
        if "review" in found:
            lenses = {match.group(1) for body in bodies[layer] for match in LENS_LINE.finditer(body)}
            missing = [lens for lens in REQUIRED_LENSES if lens not in lenses]
            if missing:
                errors.append(f"L{layer}: review layer needs slices with Lens: {', '.join(missing)}")
            run = []
            continue
        if found <= UNCOUNTED_KINDS:
            continue
        run.append(layer)
        if len(run) == MAX_BUILD_RUN + 1:
            errors.append(f"L{run[0]}-L{run[-1]}: {len(run)} build layers in a row; add a review layer (Kind: review) after every two or three")
    return errors


def identity(root: Path | None, file: str) -> str:
    if root is None:
        return file
    path = root / file
    if not path.is_symlink():
        return file
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def marker_needs_graph(texts: list[str]) -> bool:
    return any(SCHEDULE_LINE.search(text) for text in texts)


def id_set(raw: str) -> set[str] | None:
    text = raw.strip().strip("`")
    if text.lower() == "none":
        return set()
    parts = [part.strip().strip("`") for part in text.split(",") if part.strip()]
    if not parts or any(SLICE_ID.fullmatch(part) is None for part in parts):
        return None
    return set(parts)


def ancestors_of(needs: dict[str, set[str]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = list(needs.get(start, ()))
    while stack:
        node = stack.pop()
        if node in seen or node == start:
            continue
        seen.add(node)
        stack.extend(needs.get(node, ()))
    return seen


def graph_errors(needs: dict[str, set[str]], owned: dict[str, list[str]], root: Path | None) -> list[str]:
    errors: list[str] = []
    known = set(needs)
    for slice_id, wanted in needs.items():
        for other in sorted(wanted):
            if other not in known:
                errors.append(f"{slice_id}: Needs unknown id {other}")
    color = {slice_id: 0 for slice_id in known}
    trail: list[str] = []

    def walk(node: str) -> None:
        color[node] = 1
        trail.append(node)
        for nxt in sorted(needs.get(node, ())):
            if nxt not in known:
                continue
            if color[nxt] == 1:
                cycle = trail[trail.index(nxt):] + [nxt]
                errors.append("needs cycle: " + " -> ".join(cycle))
            elif color[nxt] == 0:
                walk(nxt)
        trail.pop()
        color[node] = 2

    for slice_id in sorted(known):
        if color[slice_id] == 0:
            walk(slice_id)
    anc = {slice_id: ancestors_of(needs, slice_id) for slice_id in known}
    owners: dict[str, list[str]] = defaultdict(list)
    for slice_id, files in owned.items():
        for raw in files:
            owners[identity(root, raw)].append(slice_id)
    reported: set[tuple[str, str, str]] = set()

    def report(left: str, right: str, path: str) -> None:
        if left == right or left in anc.get(right, ()) or right in anc.get(left, ()):
            return
        pair = tuple(sorted((left, right)))
        key = (pair[0], pair[1], path)
        if key in reported:
            return
        reported.add(key)
        errors.append(f"{pair[0]} overlaps {pair[1]} without a Needs edge: {path}")

    for path, holders in owners.items():
        unique = list(dict.fromkeys(holders))
        for index, left in enumerate(unique):
            for right in unique[index + 1:]:
                report(left, right, path)
        parent = path
        while "/" in parent:
            parent = parent.rsplit("/", 1)[0]
            for other in owners.get(parent, ()):
                for holder in unique:
                    report(holder, other, path)
    return errors


def check(paths: list[Path], root: Path | None = None) -> tuple[int, list[str]]:
    errors: list[str] = []
    layers: dict[int, list[tuple[int, str, str]]] = defaultdict(list)
    owners: dict[tuple[int, str], str] = {}
    shared_owner: dict[tuple[int, str], str] = {}
    ids: set[str] = set()
    texts = [path.read_text(encoding="utf-8") for path in paths]
    graph = marker_needs_graph(texts)
    kinds = layer_kinds(texts)
    every = slice_bodies(texts)
    bodies: dict[int, list[str]] = defaultdict(list)
    needs_of: dict[str, set[str]] = {}
    owned_files: dict[str, list[str]] = defaultdict(list)
    for path, text in zip(paths, texts):
        for match in OUTSIDE_LAYER.finditer(text):
            errors.append(f"{path.name}: work outside a layer ({match.group(0).strip()}); make it a slice in a layer")
        headers = list(HEADER.finditer(text))
        file_rows: dict[int, list[tuple[int, str, str]]] = defaultdict(list)
        valid_starts = {match.start() for match in headers}
        for candidate in re.finditer(r"^#{2,4} L\d+[A-Z]+\b.*$", text, re.M):
            if candidate.start() not in valid_starts:
                errors.append(f"{path.name}: malformed slice heading {candidate.group(0)}")
        for index, match in enumerate(headers):
            slice_id, layer_text, letters, tier, _ = match.groups()
            layer = int(layer_text)
            end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
            body = text[match.end():end]
            if slice_id in ids:
                errors.append(f"duplicate slice {slice_id}")
            ids.add(slice_id)
            row = (letter_number(letters), tier or "", slice_id)
            layers[layer].append(row)
            file_rows[layer].append(row)
            bodies[layer].append(body)
            kind = slice_kind(body)
            solo = kinds[layer] <= SOLO_KINDS and kinds[layer] != {"bench"}
            errors.extend(kind_errors(slice_id, layer, kind, body, every))
            required = ("Owns", "Forbidden", "Done when", "Needs" if graph else "Depends")
            for label in required:
                if not re.search(rf"^{label}:[ \t]*\S", body, re.M):
                    errors.append(f"{slice_id}: missing {label}")
            if graph:
                needs_match = NEEDS_LINE.search(body)
                parsed = id_set(needs_match.group(1)) if needs_match else set()
                if needs_match and parsed is None:
                    errors.append(f"{slice_id}: Needs must be none or a comma-separated list of slice ids")
                    parsed = set()
                needs_of[slice_id] = parsed
                depends_match = DEPENDS_LINE.search(body)
                if depends_match and id_set(depends_match.group(1)) != parsed:
                    errors.append(f"{slice_id}: Depends and Needs must list the same slice ids")
            if tier is None:
                errors.append(f"{slice_id}: missing difficulty label; put one of {', '.join(LABELS)} after the id")
            elif tier not in LABELS:
                errors.append(f"{slice_id}: label {tier} is not one of {', '.join(LABELS)}")
            size_line = re.search(r"^Size:[ \t]*(\S+?)\.[ \t]*\S", body, re.M)
            if not size_line:
                errors.append(f"{slice_id}: missing 'Size: {tier or '<label>'}. <reason>'")
            elif tier and size_line.group(1) != tier:
                errors.append(f"{slice_id}: Size line says {size_line.group(1)}, header says {tier}")
            if MODEL_LINE.search(body):
                errors.append(f"{slice_id}: Model line is not allowed; slices inherit the caller's default model")
            done = re.search(r"^Done when:[ \t]*(.+)$", body, re.M)
            if done and SOURCE_TEXT_PROOF.search(done.group(1)):
                errors.append(f"{slice_id}: source-text deletion/syntax is not behavior proof; follow the test policy in build/references/tests.md")
            owns_line = re.search(r"^Owns:[ \t]*(.+)$", body, re.M)
            files = re.findall(r"`([^`]+)`", owns_line.group(1)) if owns_line else []
            if not files:
                errors.append(f"{slice_id}: Owns needs exact backticked paths")
            if any(is_manifest(file) for file in files) and not re.search(r"^Dependencies:[ \t]*\S", body, re.M):
                errors.append(f"{slice_id}: owns a dependency manifest or lockfile; add 'Dependencies: <what it removes, or what it adds and why>'")
            for file in files:
                if PurePosixPath(file).is_absolute() or str(PurePosixPath(file)) != file or ".." in PurePosixPath(file).parts:
                    errors.append(f"{slice_id}: noncanonical owner path {file}")
                    continue
                if "*" in file or "?" in file:
                    errors.append(f"{slice_id}: ownership glob {file}")
                if graph:
                    owned_files[slice_id].append(file)
                if solo:
                    continue
                candidate = root / file if root is not None else Path(file)
                if not candidate.is_symlink() and candidate.is_dir():
                    errors.append(f"{slice_id}: directory ownership {file}")
                group = shared_group(file)
                if group:
                    holder = shared_owner.get((layer, group))
                    if holder and holder != slice_id:
                        errors.append(f"{slice_id} and {holder} both own shared {group} in L{layer}; give it to one slice and move the other to the next layer")
                    shared_owner.setdefault((layer, group), slice_id)
                if graph:
                    continue
                for (other_layer, other_file), other_id in owners.items():
                    if layer != other_layer:
                        continue
                    left, right = identity(root, file), identity(root, other_file)
                    if other_id != slice_id and file != other_file and left == right:
                        errors.append(f"{slice_id} overlaps {other_id}: {file} resolves to {left}")
                    if file.startswith(other_file + "/") or other_file.startswith(file + "/"):
                        errors.append(f"{slice_id} has ancestor ownership overlap with {other_id}: {file}, {other_file}")
                    elif other_id != slice_id and (left, right) != (file, other_file) and (left.startswith(right + "/") or right.startswith(left + "/")):
                        errors.append(f"{slice_id} has ancestor ownership overlap with {other_id}: {left}, {right}")
                key = layer, file
                if key in owners:
                    errors.append(f"{slice_id} overlaps {owners[key]}: {file}")
                owners[key] = slice_id
            if not graph:
                depends = DEPENDS_LINE.search(body)
                if depends and re.search(rf"\bL{layer}[A-Z]+\b", depends.group(1)):
                    errors.append(f"{slice_id}: same-layer dependency")
        if graph:
            for layer_number, rows in file_rows.items():
                if rows != sorted(rows):
                    errors.append(f"{path.name}: L{layer_number} slice letters are not in order")
    if graph:
        errors.extend(graph_errors(needs_of, owned_files, root))
    else:
        for layer, rows in sorted(layers.items()):
            if rows != sorted(rows):
                errors.append(f"L{layer}: slice letters are not in order")
    errors.extend(cadence_errors(kinds, bodies))
    if not ids:
        errors.append("no slice contracts found")
    return len(ids), errors


def slices_left(paths: list[Path]) -> int:
    ids: set[str] = set()
    merged: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        ids.update(match.group(1) for match in HEADER.finditer(text))
        for row in STATUS_ROW.finditer(text):
            if any(cell.strip().strip("`").lower() == "merged" for cell in row.group(2).split("|")):
                merged.add(row.group(1))
    return len(ids - merged)


def execution_format(left: int) -> str:
    return "heavy orchestrator" if left > HEAVY_ABOVE else "light orchestrator"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parts", nargs="+", type=Path)
    args = parser.parse_args()
    count, errors = check(args.parts, Path.cwd())
    for error in errors:
        print(error)
    left = slices_left(args.parts)
    print(f"{left} slices left; format: {execution_format(left)}; manual also available")
    print(f"{count} slices; {len(errors)} errors")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
