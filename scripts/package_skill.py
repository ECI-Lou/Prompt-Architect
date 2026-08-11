#!/usr/bin/env python3
"""Build a deterministic standalone Prompt Architect .skill archive."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

from validate_skill_package import validate_archive, validate_repository


PACKAGE_ROOT = "prompt-architect"
ROOT_FILES = ("SKILL.md", "README.md", "CONTRIBUTING.md", "SECURITY.md")
RESOURCE_DIRECTORIES = ("agents", "examples", "references")
RUNTIME_SCRIPTS = (
    "scripts/validate_patent_prompt.py",
    "scripts/validate_pharma_prompt.py",
)
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def package_members(root: Path) -> list[Path]:
    members = [root / relative for relative in ROOT_FILES]
    members.extend(root / relative for relative in RUNTIME_SCRIPTS)
    for directory in RESOURCE_DIRECTORIES:
        members.extend(path for path in (root / directory).rglob("*") if path.is_file())
    return sorted(set(members), key=lambda path: path.relative_to(root).as_posix())


def build_archive(root: Path, output: Path) -> Path:
    errors = validate_repository(root, check_git=False)
    if errors:
        raise ValueError("\n".join(errors))

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for source in package_members(root):
            relative = PurePosixPath(source.relative_to(root).as_posix())
            member = PurePosixPath(PACKAGE_ROOT) / relative
            info = zipfile.ZipInfo(member.as_posix(), date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compresslevel=9)

    archive_errors = validate_archive(output)
    if archive_errors:
        output.unlink(missing_ok=True)
        raise ValueError("\n".join(archive_errors))
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the standalone Prompt Architect .skill archive."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Default: <root>/dist/prompt-architect.skill",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = (
        args.output.resolve()
        if args.output
        else root / "dist" / "prompt-architect.skill"
    )
    try:
        built = build_archive(root, output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"PACKAGE={built}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
