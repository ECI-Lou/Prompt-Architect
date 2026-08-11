#!/usr/bin/env python3
"""Validate deterministic contract boundaries in a patent translation prompt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
OUTPUT_ONLY_RE = re.compile(
    r"\b(?:output|respond)\s+only\s+(?:with\s+)?(?:the\s+)?translation\b"
    r"|\btranslation\s+only\b",
    re.IGNORECASE,
)
UNRESOLVED_PLACEHOLDER_RE = re.compile(
    r"\[[A-Z][A-Z0-9_ /-]{1,}\]"
)
UNKNOWN_TERMINOLOGY_META_RE = re.compile(
    r"\b(?:no|without)\b.{0,80}\b(?:approved\s+)?"
    r"(?:glossar(?:y|ies)|term\s*base|termbase|term list)\b"
    r"|\b(?:glossar(?:y|ies)|term\s*base|termbase|term list)\b.{0,80}\b"
    r"(?:not\s+(?:provided|supplied|available|visible|accessible)|"
    r"absent|unknown|unconfirmed|external[- ]only|post[- ]check|"
    r"binding|runtime variable|model[- ]visible)\b"
    r"|\b(?:model[- ]visible|model visibility|runtime variable|"
    r"platform binding)\b.{0,80}\b"
    r"(?:glossar(?:y|ies)|term\s*base|termbase|terminology|term list)\b"
    r"|\b(?:invent|infer|assume access to)\b.{0,60}\b"
    r"(?:glossar(?:y|ies)|term\s*base|termbase|terminology binding)\b",
    re.IGNORECASE | re.DOTALL,
)
TERMINOLOGY_TOKEN_RE = re.compile(
    r"\{[A-Z0-9_]*(?:GLOSSARY|TERMBASE|TERMINOLOGY|APPROVED_TERMS|TERMS)"
    r"[A-Z0-9_]*\}",
    re.IGNORECASE,
)
GENERIC_RUNTIME_TOKEN_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_-]*\}")
WORKFLOW_META_RE = re.compile(
    r"\b(?:output|provide|submit|raise)\s+"
    r"(?:(?:notes?|comments?|explanations?|alternatives?)\s*,?\s*"
    r"(?:or\s+)*)*(?:an?\s+|any\s+)?quer(?:y|ies)\b"
    r"(?!\s+(?:result|plan|language|processor|execution|optimizer)s?\b)"
    r"|\b(?:output|provide|return|submit)\b.{0,60}\b"
    r"(?:issue[- ](?:list|report)s?|review[- ](?:report|workflow)s?|"
    r"error taxonomy|severity(?: level)?|pass/fail verdict|"
    r"revised translation)\b"
    r"|\b(?:ask|request|contact)\b.{0,60}\b"
    r"(?:clarification|user|client|reviewer)\b"
    r"|^#{4,}\s+.*\b(?:qa|quality review|issue report|review report|"
    r"verdict|revision)\b",
    re.IGNORECASE | re.MULTILINE,
)
FIXED_DATE_RE = re.compile(
    r"\b(?:MM/DD/YYYY|DD/MM/YYYY|YYYY/MM/DD|YYYY-MM-DD|MM-DD-YYYY|"
    r"DD-MM-YYYY|DD\.MM\.YYYY|MM\.DD\.YYYY|YYYY\.MM\.DD|"
    r"month/day/year|day/month/year|year/month/day|"
    r"month-day-year|day-month-year|year-month-day)\b",
    re.IGNORECASE,
)
PROJECT_COUNT_RE = re.compile(
    r"\b(?:claims?|figures?|figs?\.?|tables?)\s+\d+\s*"
    r"(?:[-–—]|through|to)\s*\d+\b"
    r"|\b\d+\s+(?:claims?|figures?|tables?)\b",
    re.IGNORECASE,
)
MANNER_INSTRUCTION_RE = re.compile(
    r"\b(?:preserv(?:e|es|ed|ing)|retain(?:s|ed|ing)?|keep|keeps|kept|"
    r"protect(?:s|ed|ing)?|maintain(?:s|ed|ing)?|"
    r"do not (?:omit|drop|remove|lose)|must remain)\b.{0,220}\b"
    r"(?:manner qualifiers?|slowly|dropwise|portionwise)\b"
    r"|\b(?:slowly|dropwise|portionwise)\b.{0,220}\b"
    r"(?:must be (?:preserved|retained|kept)|do not (?:omit|drop|remove|lose))\b",
    re.IGNORECASE | re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Lint a saved patent Role/Style translation prompt. "
            "The default terminology mode assumes an external-only or "
            "unconfirmed termbase."
        )
    )
    parser.add_argument("prompt", type=Path, help="Path to the Markdown prompt")
    parser.add_argument(
        "--terminology-mode",
        choices=("unknown", "visible"),
        default="unknown",
        help="Whether approved terminology is explicitly visible to the model",
    )
    parser.add_argument(
        "--allowed-runtime-token",
        action="append",
        default=[],
        help=(
            "Exact terminology token explicitly confirmed by the user or "
            "platform; repeat for multiple tokens. Valid only in visible mode."
        ),
    )
    parser.add_argument(
        "--allowed-source-literal",
        action="append",
        default=[],
        help=(
            "Exact placeholder-like token verified in the current source and "
            "required to be copied literally; repeat for multiple literals."
        ),
    )
    parser.add_argument(
        "--require-procedure-manner",
        action="store_true",
        help=(
            "Require explicit slowly/dropwise/portionwise protection because "
            "the inspected source contains experimental addition or dispensing "
            "steps where manner qualifiers may occur"
        ),
    )
    parser.add_argument(
        "--allow-fixed-date-format",
        action="store_true",
        help="Allow a fixed numeric date pattern confirmed by an authority",
    )
    parser.add_argument(
        "--allow-project-counts",
        action="store_true",
        help="Allow exact claim/table/figure ranges required operationally",
    )
    return parser.parse_args()


def lint(text: str, args: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    allowed_source_literals = set(args.allowed_source_literal)
    headings = [heading.strip() for heading in H3_RE.findall(text)]

    if headings != ["Role prompt", "Style prompt"]:
        errors.append(
            "Structure: expected exactly '### Role prompt' followed by "
            "'### Style prompt', with no other H3 blocks."
        )

    role_match = re.search(r"^###\s+Role prompt\s*$", text, re.MULTILINE)
    style_match = re.search(r"^###\s+Style prompt\s*$", text, re.MULTILINE)
    if role_match and text[: role_match.start()].strip():
        errors.append("Structure: content appears before the Role prompt block.")

    if role_match and style_match and role_match.end() <= style_match.start():
        role_body = text[role_match.end() : style_match.start()].strip()
        style_body = text[style_match.end() :].strip()
        if not role_body:
            errors.append("Structure: the Role prompt block is empty.")
        if not style_body:
            errors.append("Structure: the Style prompt block is empty.")
        if role_body and not OUTPUT_ONLY_RE.search(role_body):
            errors.append(
                "Contract: the Role prompt must state the translation-only "
                "output contract."
            )
        if style_body and not OUTPUT_ONLY_RE.search(style_body[-800:]):
            errors.append(
                "Contract: restate the translation-only contract near the end "
                "of the Style prompt."
            )
    elif not OUTPUT_ONLY_RE.search(text):
        errors.append("Contract: no clear translation-only output instruction found.")

    unresolved_placeholders = [
        match.group(0)
        for match in UNRESOLVED_PLACEHOLDER_RE.finditer(text)
        if match.group(0) not in allowed_source_literals
    ]
    if unresolved_placeholders:
        errors.append(
            "Placeholder: unresolved template token found: "
            f"{unresolved_placeholders[0]!r}."
        )

    runtime_tokens = {
        *GENERIC_RUNTIME_TOKEN_RE.findall(text),
        *TERMINOLOGY_TOKEN_RE.findall(text),
    }
    runtime_tokens -= allowed_source_literals
    if args.terminology_mode == "unknown":
        if runtime_tokens:
            errors.append(
                "Terminology boundary: external/unconfirmed terminology mode "
                "must not contain unconfirmed brace-delimited runtime tokens "
                f"({', '.join(sorted(runtime_tokens))})."
            )
        meta = UNKNOWN_TERMINOLOGY_META_RE.search(text)
        if meta:
            errors.append(
                "Terminology boundary: external/unconfirmed terminology mode "
                f"must not leak authoring metadata ({meta.group(0)!r})."
            )
    else:
        allowed_tokens = set(args.allowed_runtime_token)
        unexpected_tokens = sorted(runtime_tokens - allowed_tokens)
        if unexpected_tokens:
            errors.append(
                "Terminology boundary: visible mode contains unconfirmed "
                "terminology runtime tokens "
                f"({', '.join(unexpected_tokens)}). Pass each exact confirmed "
                "token with --allowed-runtime-token."
            )

    workflow = WORKFLOW_META_RE.search(text)
    if workflow:
        errors.append(
            "Production boundary: remove query/review/issue-report interaction "
            f"language ({workflow.group(0)!r}); require translation-only output."
        )

    if not args.allow_fixed_date_format:
        for date_pattern in FIXED_DATE_RE.finditer(text):
            if date_pattern.group(0) in allowed_source_literals:
                continue
            window_start = max(0, date_pattern.start() - 180)
            window_end = min(len(text), date_pattern.end() + 180)
            window = text[window_start:window_end]
            pattern = re.escape(date_pattern.group(0))
            prescriptive = bool(
                re.search(
                    rf"\bdate format\b.{{0,60}}{pattern}"
                    rf"|\b(?:render|format|convert|normalize|present|write|"
                    rf"express|change|set|adopt|standardize|force|require)"
                    rf"\b.{{0,100}}\bdates?\b.{{0,100}}{pattern}"
                    rf"|\b(?:use|apply|follow)\b.{{0,60}}{pattern}.{{0,60}}"
                    rf"\b(?:for (?:all )?dates|as (?:the )?date format|"
                    rf"date format)\b"
                    rf"|{pattern}.{{0,60}}\b(?:date format|for (?:all )?dates)\b",
                    window,
                    re.IGNORECASE | re.DOTALL,
                )
            )
            is_protected_literal = bool(
                re.search(
                    r"\b(?:copy|preserve|retain|keep|use)\b",
                    window,
                    re.IGNORECASE,
                )
                and re.search(
                    r"\b(?:source[- ]fixed|literal|verbatim|token|string|notation)\b",
                    window,
                    re.IGNORECASE,
                )
            )
            if prescriptive or not is_protected_literal:
                errors.append(
                    "Date boundary: fixed numeric date format requires explicit "
                    f"authority ({date_pattern.group(0)!r})."
                )
                break

    if not args.allow_project_counts:
        count = PROJECT_COUNT_RE.search(text)
        if count:
            errors.append(
                "Project-profile boundary: exact claim/table/figure ranges "
                f"require an operational justification ({count.group(0)!r})."
            )

    if args.require_procedure_manner:
        manner_is_protected = False
        blocks = re.split(
            r"(?<=[.!?])\s+|\n\s*\n|(?=^\s*[-*]\s+)",
            text,
            flags=re.MULTILINE,
        )
        for block in blocks:
            has_all_terms = all(
                re.search(rf"\b{term}\b", block, re.IGNORECASE)
                for term in ("slowly", "dropwise", "portionwise")
            )
            if has_all_terms and MANNER_INSTRUCTION_RE.search(block):
                manner_is_protected = True
                break
        if not manner_is_protected:
            errors.append(
                "Procedure coverage: one executable instruction must explicitly "
                "preserve slowly/dropwise/portionwise manner qualifiers."
            )

    return errors


def main() -> int:
    args = parse_args()
    try:
        text = args.prompt.read_text(encoding="utf-8-sig")
    except OSError as exc:
        print(f"ERROR: cannot read {args.prompt}: {exc}", file=sys.stderr)
        return 2

    errors = lint(text, args)
    if errors:
        print(f"FAIL: {args.prompt}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {args.prompt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
