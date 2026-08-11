#!/usr/bin/env python3
"""Validate the standalone Prompt Architect repository and release archive."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath


REQUIRED_FILES = (
    ".editorconfig",
    ".gitattributes",
    ".github/workflows/ci.yml",
    ".gitignore",
    "CONTRIBUTING.md",
    "pyproject.toml",
    "requirements-dev.txt",
    "SECURITY.md",
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "evals/evals.json",
    "references/template.md",
    "references/domain_rules.md",
    "references/formatting_standards.md",
    "references/patent_prompt_framework.md",
    "references/pharma_prompt_framework.md",
    "references/client_format_profile_framework.md",
    "references/client_format_profiles.json",
    "scripts/validate_patent_prompt.py",
    "scripts/validate_pharma_prompt.py",
    "scripts/validate_skill_package.py",
    "scripts/package_skill.py",
    "tests/test_validate_patent_prompt.py",
    "tests/test_validate_pharma_prompt.py",
    "tests/test_validate_skill_package.py",
)

REQUIRED_ARCHIVE_FILES = (
    "SKILL.md",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "agents/openai.yaml",
    "references/template.md",
    "references/domain_rules.md",
    "references/formatting_standards.md",
    "references/patent_prompt_framework.md",
    "references/pharma_prompt_framework.md",
    "references/client_format_profile_framework.md",
    "references/client_format_profiles.json",
    "scripts/validate_patent_prompt.py",
    "scripts/validate_pharma_prompt.py",
)

FORBIDDEN_PARTS = {
    ".codex",
    ".agents",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "projects",
    "local",
    "private",
    "scratch",
    "tmp",
    "dist",
    "build",
}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".pdf",
    ".zip",
    ".skill",
}
RESOURCE_REFERENCE_RE = re.compile(
    r"`((?:references|scripts|examples)/[^`\r\n]+)`"
)


def is_forbidden_path(path_text: str) -> bool:
    path = PurePosixPath(path_text.replace("\\", "/"))
    lowered_parts = {part.casefold() for part in path.parts}
    if lowered_parts & FORBIDDEN_PARTS:
        return True
    return path.suffix.casefold() in FORBIDDEN_SUFFIXES


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def validate_frontmatter(skill_text: str) -> list[str]:
    errors: list[str] = []
    if not skill_text.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter."]
    end = skill_text.find("\n---\n", 4)
    if end < 0:
        return ["SKILL.md frontmatter is not closed."]
    frontmatter = skill_text[4:end]
    if not re.search(r"^name:\s*prompt-architect\s*$", frontmatter, re.M):
        errors.append("SKILL.md frontmatter must declare name: prompt-architect.")
    if not re.search(r"^description:\s*(?:\||>)?", frontmatter, re.M):
        errors.append("SKILL.md frontmatter must include a description.")
    return errors


def validate_repository(root: Path, check_git: bool = True) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8-sig")
        errors.extend(validate_frontmatter(skill_text))
        for reference in sorted(set(RESOURCE_REFERENCE_RE.findall(skill_text))):
            relative = reference.split("#", 1)[0]
            if not (root / PurePosixPath(relative)).is_file():
                errors.append(f"SKILL.md references a missing resource: {reference}")

    registry_path = root / "references" / "client_format_profiles.json"
    if registry_path.is_file():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid client profile registry JSON: {exc}")
        else:
            if registry.get("selection_policy") != "explicit_only":
                errors.append("Client profile registry must use explicit_only selection.")
            if not isinstance(registry.get("profiles"), list):
                errors.append("Client profile registry profiles must be a list.")

    if check_git:
        try:
            tracked = tracked_files(root)
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f"Cannot inspect Git tracked files: {exc}")
        else:
            for relative in tracked:
                if is_forbidden_path(relative):
                    errors.append(f"Forbidden local/generated file is tracked: {relative}")

    return errors


def validate_archive(archive_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with zipfile.ZipFile(archive_path) as archive:
            names = [name for name in archive.namelist() if not name.endswith("/")]
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Cannot read archive: {exc}"]

    normalized: list[str] = []
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"Unsafe archive member: {name}")
            continue
        relative = PurePosixPath(*path.parts[1:]) if len(path.parts) > 1 else path
        relative_text = relative.as_posix()
        normalized.append(relative_text)
        if is_forbidden_path(relative_text):
            errors.append(f"Forbidden file in archive: {name}")

    for relative in REQUIRED_ARCHIVE_FILES:
        if relative not in normalized:
            errors.append(f"Archive is missing required file: {relative}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the Prompt Architect source tree or a .skill archive."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--archive", action="store_true")
    parser.add_argument("--no-git-check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = args.path.resolve()
    errors = (
        validate_archive(path)
        if args.archive
        else validate_repository(path, check_git=not args.no_git_check)
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"VALIDATION=PASS path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
