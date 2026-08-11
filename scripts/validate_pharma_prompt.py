#!/usr/bin/env python3
"""Validate deterministic contract boundaries in a Pharma translation prompt."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DOCUMENT_PROFILES = (
    "general-pharma",
    "clinical-protocol",
    "clinical-statistical",
    "regulatory-label",
    "pharmacovigilance",
    "patient-facing",
    "cmc-quality",
    "nonclinical",
    "medical-scientific",
)

FEATURES = (
    "derivation-logic",
    "partial-dates",
    "assessor-provenance",
    "tag-span",
    "protected-syntax",
)

H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
H4_RE = re.compile(r"^####\s+(.+?)\s*$", re.MULTILINE)
PHARMA_ROLE_RE = re.compile(
    r"\b(?:pharma(?:ceutical)?|life[- ]science|clinical|medical|"
    r"pharmacovigilance|regulatory|CMC|nonclinical)\b",
    re.IGNORECASE,
)
UNRESOLVED_PLACEHOLDER_RE = re.compile(r"\[[A-Z][A-Z0-9_ /-]{1,}\]")
TERMINOLOGY_TOKEN_RE = re.compile(
    r"\{[A-Z0-9_]*(?:GLOSSARY|TERMBASE|TERMINOLOGY|APPROVED_TERMS|TERMS)"
    r"[A-Z0-9_]*\}",
    re.IGNORECASE,
)
GENERIC_RUNTIME_TOKEN_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_-]*\}")
UNKNOWN_TERMINOLOGY_META_RE = re.compile(
    r"\b(?:no|without)\b.{0,100}\b(?:approved\s+)?"
    r"(?:glossar(?:y|ies)|term\s*base|termbase|term list)\b"
    r"|\b(?:glossar(?:y|ies)|term\s*base|termbase|term list)\b.{0,100}\b"
    r"(?:not\s+(?:provided|supplied|available|visible|accessible)|"
    r"absent|unknown|unconfirmed|external[- ]only|post[- ]check|"
    r"uploaded|upload|binding|runtime variable|model[- ]visible|"
    r"checked after translation)\b"
    r"|\b(?:model[- ]visible|model visibility|runtime variable|"
    r"platform binding|terminology check(?:ing)?)\b.{0,100}\b"
    r"(?:glossar(?:y|ies)|term\s*base|termbase|terminology|term list)\b"
    r"|术语表.{0,50}(?:未提供|不可见|绑定|上传|后检|检查)"
    r"|(?:绑定|上传|后检).{0,50}术语表",
    re.IGNORECASE | re.DOTALL,
)
UNKNOWN_TERMINOLOGY_ASSET_RE = re.compile(
    r"\b(?:glossar(?:y|ies)|term\s*base|termbase|term list|"
    r"terminology (?:file|asset|library))\b"
    r"|术语表|术语库"
    r"|\bterminology\b.{0,80}\b(?:uploaded|supplied by (?:the )?platform|"
    r"external file|post[- ]translation check)\b"
    r"|\b(?:uploaded|external)\b.{0,80}\bterminology\b",
    re.IGNORECASE | re.DOTALL,
)
WORKFLOW_META_RE = re.compile(
    r"\b(?:output|provide|return|submit)\b.{0,80}\b"
    r"(?:quer(?:y|ies)|issue[- ](?:list|report)s?|review[- ](?:report|"
    r"workflow)s?|error taxonomy|severity(?: level)?|pass/fail verdict|"
    r"revised translation|revision schema|QE result)\b"
    r"|\b(?:ask|request|contact)\b.{0,60}\b"
    r"(?:clarification|user|client|reviewer)\b"
    r"|^#{4,}\s+.*\b(?:qa|quality review|issue report|review report|"
    r"verdict|revision)\b",
    re.IGNORECASE | re.MULTILINE,
)
CLIENT_PROFILE_META_RE = re.compile(
    r"\b(?:client|customer)\s+(?:format|style)\s+profile\b"
    r"|\b(?:format|style)\s+profile\s+(?:id|file|path|selection|merge|"
    r"selected|loaded|unknown|unavailable)\b"
    r"|\b(?:load|read|merge)\b.{0,50}\b(?:format|style)\s+profile\b"
    r"|\bgeneric\s+(?:format|style)\s+profile\b"
    r"|(?:客户|格式)(?:配置|档案).{0,30}(?:未选择|路径|加载|合并|未知)",
    re.IGNORECASE | re.DOTALL,
)
FIXED_DATE_RE = re.compile(
    r"\b(?:MM/DD/YYYY|DD/MM/YYYY|YYYY/MM/DD|YYYY-MM-DD|MM-DD-YYYY|"
    r"DD-MM-YYYY|DD\.MM\.YYYY|MM\.DD\.YYYY|YYYY\.MM\.DD|"
    r"month/day/year|day/month/year|year/month/day|"
    r"month-day-year|day-month-year|year-month-day)\b"
    r"|YYYY年M月D日",
    re.IGNORECASE,
)
AUTHORITY_RE = re.compile(r"\b(?:FDA|EMA|NMPA|PMDA)\b", re.IGNORECASE)
BACKTICK_SPAN_RE = re.compile(r"`[^`\r\n]+`")
PROFILE_REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "references"
    / "client_format_profiles.json"
)

EXPECTED_H4_PATTERNS = (
    re.compile(r"\bevidence\b.*\bterminology\b.*\bauthority\b", re.I),
    re.compile(r"\bscientific\b.*\bclinical\b.*\bfidelity\b", re.I),
    re.compile(
        r"\bmedical entit(?:y|ies)\b.*\bdefinition\b.*\babbreviation\b.*"
        r"\bterminology\b.*\bintegrity\b",
        re.I,
    ),
    re.compile(
        r"\bclinical procedures?\b.*\bstatistics?\b.*\bformatting\b.*"
        r"\bdata\b.*\bstructure\b.*\bprotected content\b",
        re.I,
    ),
    re.compile(r"\bdocument[- ]type\b.*\bregister\b.*\bfluency\b", re.I),
    re.compile(r"\bverified project\b.*\bconstraints?\b", re.I),
    re.compile(r"\bsilent quality gate\b.*\bclosing contract\b", re.I),
)

NO_ADD_OMIT_RE = re.compile(
    r"\bdo not\b.{0,80}\b(?:add|omit|summarize|reinterpret|silently correct|"
    r"silently repair)\b"
    r"|\b(?:no|without)\b.{0,50}\b(?:addition|omission|silent correction)\b",
    re.IGNORECASE | re.DOTALL,
)
DATA_INTEGRITY_RE = re.compile(
    r"\b(?:number|numeric|dose|unit|range|comparator|threshold|precision|"
    r"p[- ]?value|confidence interval|statistic)\w*\b",
    re.IGNORECASE,
)
STRUCTURE_RE = re.compile(
    r"\b(?:tag|placeholder|table|list|flow[- ]?chart|heading|structure|"
    r"identifier|literal)\w*\b",
    re.IGNORECASE,
)

PROFILE_PATTERNS: dict[str, re.Pattern[str]] = {
    "general-pharma": re.compile(
        r"\b(?:pharma(?:ceutical)?|life[- ]science|clinical|medical)\b",
        re.IGNORECASE,
    ),
    "clinical-protocol": re.compile(
        r"\b(?:clinical protocol|protocol|eligibility|intervention|visit|"
        r"schedule of assessments)\b",
        re.IGNORECASE,
    ),
    "clinical-statistical": re.compile(
        r"\b(?:clinical[- ]statistical|statistical analysis|derivation|"
        r"endpoint|analysis dataset|event|censoring)\b",
        re.IGNORECASE,
    ),
    "regulatory-label": re.compile(
        r"\b(?:regulatory label(?:ing)?|package insert|prescribing information|"
        r"contraindication|warning|adverse reaction)\b",
        re.IGNORECASE,
    ),
    "pharmacovigilance": re.compile(
        r"\b(?:pharmacovigilance|case narrative|seriousness|expectedness|"
        r"causality|follow[- ]?up)\b",
        re.IGNORECASE,
    ),
    "patient-facing": re.compile(
        r"\b(?:patient[- ]facing|informed consent|patient leaflet|"
        r"patient instruction|comprehensib|readab)\w*\b",
        re.IGNORECASE,
    ),
    "cmc-quality": re.compile(
        r"\b(?:CMC|chemistry,? manufacturing|manufacturing|quality|"
        r"specification|analytical method)\b",
        re.IGNORECASE,
    ),
    "nonclinical": re.compile(
        r"\b(?:nonclinical|preclinical|toxicology|species|animal model|"
        r"pathology)\b",
        re.IGNORECASE,
    ),
    "medical-scientific": re.compile(
        r"\b(?:medical[- ]scientific|medical information|publication|"
        r"scientific summary|manuscript)\b",
        re.IGNORECASE,
    ),
}

FEATURE_OBJECTS: dict[str, tuple[tuple[str, re.Pattern[str]], ...]] = {
    "derivation-logic": (
        (
            "AND/OR grouping or shared condition scope",
            re.compile(
                r"\b(?:AND/OR|Boolean|logical grouping|shared condition|"
                r"condition scope|branch precedence)\b",
                re.I,
            ),
        ),
        (
            "candidate event/date/data-source set",
            re.compile(
                r"\b(?:candidate (?:event|date|data source|set)s?|"
                r"set of candidate|candidate-source)\b",
                re.I,
            ),
        ),
        (
            "earliest/latest aggregation",
            re.compile(
                r"\b(?:earliest|latest|whichever (?:is |comes )?"
                r"(?:first|last|earlier|later)|extrem\w*)\b",
                re.I,
            ),
        ),
        (
            "event/censoring branches",
            re.compile(
                r"\b(?:event|censor(?:ing|ed)?)\b.{0,120}\b"
                r"(?:branch|rule|distinction|logic|condition)\b"
                r"|\b(?:branch|rule|distinction|logic|condition)\b.{0,120}"
                r"\b(?:event|censor(?:ing|ed)?)\b",
                re.I | re.S,
            ),
        ),
    ),
    "partial-dates": (
        (
            "source date-operand granularity and explicit imputation",
            re.compile(
                r"\b(?:source (?:date )?operand granularity|"
                r"granularity of (?:each|every) (?:source )?(?:date )?operand|"
                r"date granularity|month[- ]year|partial date|incomplete date|"
                r"explicit imputation)\b",
                re.I,
            ),
        ),
        (
            "strict/inclusive temporal boundaries",
            re.compile(
                r"(?:\b(?:before|after|within|beyond|more than|at least|"
                r"on or before|on or after)\b.{0,180}\b"
                r"(?:strict|inclusive|boundary|direction|relation|distinction)"
                r"|\b(?:strict|inclusive|boundary|direction)\w*\b.{0,180}"
                r"\b(?:before|after|within|beyond|more than|at least)\b)",
                re.I | re.S,
            ),
        ),
    ),
    "assessor-provenance": (
        (
            "performer/assessor/evidence-source distinction",
            re.compile(
                r"\b(?:performer|performed by)\b.{0,180}\b"
                r"(?:assessor|assessment source|evidence source|adjudicator|"
                r"reviewer)\b"
                r"|\b(?:assessor|assessment source|evidence source|"
                r"adjudicator|reviewer)\b.{0,180}\b"
                r"(?:performer|performed by)\b",
                re.I | re.S,
            ),
        ),
    ),
    "tag-span": (
        (
            "tag identity/pairing/nesting",
            re.compile(
                r"\btag\b.{0,160}\b(?:identity|pairing|paired|nesting|nested)\b"
                r"|\b(?:identity|pairing|paired|nesting|nested)\b.{0,160}\btag\b",
                re.I | re.S,
            ),
        ),
        (
            "equivalent semantic span",
            re.compile(
                r"\b(?:semantic|meaning-equivalent|equivalent)\s+span\b"
                r"|\bspan\b.{0,80}\b(?:same|equivalent)\s+(?:meaning|concept)\b",
                re.I,
            ),
        ),
    ),
    "protected-syntax": (
        (
            "case and ASCII punctuation",
            re.compile(
                r"\b(?:case|casing)\b.{0,140}\bASCII\s+punctuation\b"
                r"|\bASCII\s+punctuation\b.{0,140}\b(?:case|casing)\b",
                re.I | re.S,
            ),
        ),
        (
            "functions/operators/quoted values",
            re.compile(
                r"\b(?:function|operator|quoted (?:coded )?(?:value|literal)|"
                r"dataset|variable)\w*\b",
                re.I,
            ),
        ),
    ),
}

POSITIVE_VERB_RE = re.compile(
    r"\b(?:preserve|retain|keep|maintain|protect|copy|ensure|distinguish|"
    r"separate|respect|match|reproduce)\w*\b",
    re.I,
)
NEGATED_POSITIVE_RE = re.compile(
    r"\b(?:do not|don't|never|need not|not required to|may not|must not)\b"
    r".{0,80}\b(?:preserve|retain|keep|maintain|protect|copy|ensure|"
    r"distinguish|separate|respect|match|reproduce)\w*\b",
    re.I | re.S,
)
PROTECTIVE_PROHIBITION_RE = re.compile(
    r"\b(?:do not|never|must not)\b.{0,80}\b"
    r"(?:change|alter|round|normalize|reformat|damage|omit|drop|remove|"
    r"conflate|confuse|merge|detach|restructure|invent|add)\w*\b",
    re.I | re.S,
)
EXTRA_OUTPUT_NOUN_RE = re.compile(
    r"\b(?:explanations?|commentary|notes?|alternatives?|quer(?:y|ies)|"
    r"issues?|review reports?|rationales?|change summary|changes?)\b",
    re.I,
)
EXTRA_OUTPUT_VERB_RE = re.compile(
    r"\b(?:output|provide|return|list|include|append|add|give|submit|"
    r"explain|report|revise)\w*\b",
    re.I,
)
NEGATED_EXTRA_OUTPUT_RE = re.compile(
    r"\b(?:do not|don't|never|no|without)\b.{0,80}"
    r"\b(?:explanations?|commentary|notes?|alternatives?|quer(?:y|ies)|"
    r"issues?|review reports?|rationales?|changes?)\b",
    re.I | re.S,
)

FORMAT_SETTING_PATTERNS = {
    "comparator-width": {
        "full": re.compile(r"\bfull[- ]width\b.{0,100}\b(?:compar|operator)", re.I),
        "half": re.compile(r"\bhalf[- ]width\b.{0,100}\b(?:compar|operator)", re.I),
    },
    "range-connector": {
        "fixed-hyphen": re.compile(
            r"\b(?:use|require)\b.{0,80}\bhyphen\b.{0,80}\b(?:all|range)",
            re.I,
        ),
        "source-preserved": re.compile(
            r"\bpreserve\b.{0,80}\bsource\b.{0,80}\brange connector",
            re.I,
        ),
    },
    "abbreviated-time-units": {
        "translated": re.compile(
            r"\btranslate\b.{0,80}\b(?:abbreviated )?time units?\b",
            re.I,
        ),
        "preserved": re.compile(
            r"\b(?:preserve|retain|keep)\b.{0,80}\babbreviated time units?\b",
            re.I,
        ),
    },
    "thousands-grouping": {
        "normalized": re.compile(
            r"\b(?:add|insert|normalize)\b.{0,80}\bthousands separator",
            re.I,
        ),
        "source-preserved": re.compile(
            r"\bpreserve\b.{0,80}\b(?:source )?thousands separator",
            re.I,
        ),
    },
}


def clauses(text: str) -> list[str]:
    paragraphs: list[str] = []
    buffer = ""

    def flush() -> None:
        nonlocal buffer
        if buffer.strip():
            paragraphs.append(buffer.strip())
        buffer = ""

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            flush()
            paragraphs.append(stripped.lstrip("#").strip())
            continue
        bullet = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", raw_line)
        if bullet:
            flush()
            buffer = bullet.group(1).strip()
            continue
        buffer = f"{buffer} {stripped}".strip() if buffer else stripped
    flush()

    result: list[str] = []
    for paragraph in paragraphs:
        result.extend(
            item.strip()
            for item in re.split(
                r"(?<=[.!?。！？])\s+|[;；]\s*",
                paragraph,
            )
            if item.strip()
        )
    return result


def has_positive_instruction(text: str, object_re: re.Pattern[str]) -> bool:
    for clause in clauses(text):
        if not object_re.search(clause):
            continue
        if NEGATED_POSITIVE_RE.search(clause):
            continue
        if POSITIVE_VERB_RE.search(clause):
            return True
        if PROTECTIVE_PROHIBITION_RE.search(clause):
            return True
    return False


def has_translation_only_contract(text: str) -> bool:
    for clause in clauses(text):
        if re.search(r"\bnot\s+translation[- ]only\b", clause, re.I):
            continue
        command = re.search(
            r"\b(?:output|respond|return|provide|give)\w*\b",
            clause,
            re.I,
        )
        translation = re.search(r"\btranslation\b", clause, re.I)
        exclusive = re.search(
            r"\bonly\b|\bnothing else\b|\bwithout\b.{0,50}"
            r"\b(?:commentary|explanation|notes?|additional output)\b",
            clause,
            re.I | re.S,
        )
        if command and translation and exclusive:
            return True
        if translation and re.search(r"\band nothing else\b", clause, re.I):
            return True
    return False


def has_positive_additional_output(text: str) -> bool:
    for clause in clauses(text):
        if NEGATED_EXTRA_OUTPUT_RE.search(clause):
            continue
        if EXTRA_OUTPUT_NOUN_RE.search(clause) and (
            EXTRA_OUTPUT_VERB_RE.search(clause)
            or re.search(r"\b(?:may|can|should|must)\s+follow\b", clause, re.I)
        ):
            return True
    return False


def normalize_locale(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def role_has_locale_pair(role: str, source: str, target: str) -> bool:
    compact = normalize_locale(role)
    source_key = normalize_locale(source)
    target_key = normalize_locale(target)
    source_pos = compact.find(source_key)
    target_pos = compact.find(target_key)
    return source_pos >= 0 and target_pos > source_pos


def load_profile_registry() -> tuple[dict[str, dict], list[dict]]:
    data = json.loads(PROFILE_REGISTRY_PATH.read_text(encoding="utf-8-sig"))
    profiles = data.get("profiles", [])
    aliases: dict[str, dict] = {}
    for profile in profiles:
        keys = [profile["id"], *profile.get("aliases", [])]
        for key in keys:
            aliases[key.casefold()] = profile
    return aliases, profiles


def format_scope(clause: str) -> str:
    if re.search(
        r"\b(?:code|formula|source[- ]fixed|protected|identifier|literal|"
        r"dataset|variable|executable)\b",
        clause,
        re.I,
    ):
        return "protected"
    if re.search(
        r"\b(?:ordinary|running|visible|narrative|body)\s+(?:prose|text)\b",
        clause,
        re.I,
    ):
        return "ordinary"
    return "unspecified"


def find_format_conflicts(text: str) -> list[str]:
    conflicts: list[str] = []
    prompt_clauses = clauses(text)
    for key, values in FORMAT_SETTING_PATTERNS.items():
        settings: list[tuple[str, str]] = []
        for clause in prompt_clauses:
            for value, pattern in values.items():
                if pattern.search(clause):
                    settings.append((value, format_scope(clause)))
        for index, (first_value, first_scope) in enumerate(settings):
            for second_value, second_scope in settings[index + 1 :]:
                if first_value == second_value:
                    continue
                if (
                    first_scope == second_scope
                    or first_scope == "unspecified"
                    or second_scope == "unspecified"
                ):
                    conflicts.append(key)
                    break
            if key in conflicts:
                break
    return conflicts


def find_prescriptive_fixed_date(
    text: str,
    allowed_source_literals: set[str],
) -> str | None:
    for clause in clauses(text):
        match = FIXED_DATE_RE.search(clause)
        if not match or match.group(0) in allowed_source_literals:
            continue
        if re.search(
            r"\b(?:preserve|copy|retain|keep)\b.{0,80}\b"
            r"(?:source[- ]fixed|literal|code|token|notation)\b"
            r"|\b(?:source[- ]fixed|literal|code|token|notation)\b.{0,80}"
            r"\b(?:preserve|copy|retain|keep)\b",
            clause,
            re.I | re.S,
        ):
            continue
        if re.search(
            r"\b(?:do not|don't|never)\b.{0,80}"
            r"\b(?:force|require|use|apply|normalize|convert|format)\b",
            clause,
            re.I | re.S,
        ):
            continue
        if re.search(
            r"\b(?:use|apply|format|render|convert|normalize|write|display|"
            r"require|must use|must follow|force)\b",
            clause,
            re.I,
        ):
            return match.group(0)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint a saved Pharma Role/Style translation prompt."
    )
    parser.add_argument("prompt", type=Path, help="Path to the Markdown prompt")
    parser.add_argument(
        "--source-locale",
        required=True,
        help="Expected source locale, such as en-US",
    )
    parser.add_argument(
        "--target-locale",
        required=True,
        help="Expected target locale, such as zh-CN",
    )
    parser.add_argument(
        "--document-profile",
        choices=DOCUMENT_PROFILES,
        default="general-pharma",
    )
    parser.add_argument(
        "--terminology-mode",
        choices=("unknown", "visible"),
        default="unknown",
    )
    parser.add_argument(
        "--format-profile",
        default="generic",
        help=(
            "Registered explicit client format profile ID, or 'generic'. "
            "Arbitrary unregistered IDs fail."
        ),
    )
    parser.add_argument("--allowed-runtime-token", action="append", default=[])
    parser.add_argument("--allowed-source-literal", action="append", default=[])
    parser.add_argument("--allowed-authority", action="append", default=[])
    parser.add_argument(
        "--require-feature",
        action="append",
        choices=FEATURES,
        default=[],
    )
    parser.add_argument("--require-format-fragment", action="append", default=[])
    parser.add_argument("--forbid-client-marker", action="append", default=[])
    parser.add_argument("--allow-fixed-date-format", action="store_true")
    parser.add_argument("--allow-large-literal-inventory", action="store_true")
    return parser.parse_args()


def lint(text: str, args: argparse.Namespace) -> list[str]:
    text = text.lstrip("\ufeff")
    errors: list[str] = []
    allowed_source_literals = set(args.allowed_source_literal)
    headings = [heading.strip() for heading in H3_RE.findall(text)]

    if headings != ["Role prompt", "Style prompt"]:
        errors.append(
            "C001 Structure: expected exactly '### Role prompt' followed by "
            "'### Style prompt', with no other H3 blocks."
        )

    role_match = re.search(r"^###\s+Role prompt\s*$", text, re.MULTILINE)
    style_match = re.search(r"^###\s+Style prompt\s*$", text, re.MULTILINE)
    role_body = ""
    style_body = ""
    if role_match and text[: role_match.start()].strip():
        errors.append("C002 Structure: content appears before the Role prompt block.")
    if role_match and style_match and role_match.end() <= style_match.start():
        role_body = text[role_match.end() : style_match.start()].strip()
        style_body = text[style_match.end() :].strip()
        if not role_body:
            errors.append("C002 Structure: the Role prompt block is empty.")
        if not style_body:
            errors.append("C002 Structure: the Style prompt block is empty.")
    else:
        errors.append("C002 Structure: Role/Style blocks are missing or reversed.")

    if role_body and not PHARMA_ROLE_RE.search(role_body):
        errors.append("C003 Role: no Pharma/life-science/medical role was identified.")
    if role_body and not role_has_locale_pair(
        role_body,
        args.source_locale,
        args.target_locale,
    ):
        errors.append(
            "C003 Role: expected source-to-target locale pair "
            f"{args.source_locale!r} -> {args.target_locale!r}."
        )
    if role_body and not has_translation_only_contract(role_body):
        errors.append("C004 Contract: Role must state translation-only output.")
    if style_body and not has_translation_only_contract(style_body[-1200:]):
        errors.append(
            "C004 Contract: restate translation-only output near the end of Style."
        )
    if has_positive_additional_output(text):
        errors.append(
            "C004 Contract: positive instruction requests commentary, issues, "
            "notes, alternatives, explanations, or another non-translation output."
        )

    if style_body:
        h4_headings = [heading.strip() for heading in H4_RE.findall(style_body)]
        if len(h4_headings) != len(EXPECTED_H4_PATTERNS):
            errors.append(
                "C011 Pharma structure: expected exactly seven H4 Style "
                "subsections from Evidence/Terminology through Silent Quality Gate."
            )
        else:
            for index, (heading, pattern) in enumerate(
                zip(h4_headings, EXPECTED_H4_PATTERNS),
                start=1,
            ):
                if not pattern.search(heading):
                    errors.append(
                        "C011 Pharma structure: Style subsection "
                        f"{index} has unexpected heading {heading!r}."
                    )

    unresolved = [
        match.group(0)
        for match in UNRESOLVED_PLACEHOLDER_RE.finditer(text)
        if match.group(0) not in allowed_source_literals
    ]
    if unresolved:
        errors.append(f"C005 Placeholder: unresolved token {unresolved[0]!r}.")

    runtime_tokens = {
        *GENERIC_RUNTIME_TOKEN_RE.findall(text),
        *TERMINOLOGY_TOKEN_RE.findall(text),
    }
    runtime_tokens -= allowed_source_literals
    if args.terminology_mode == "unknown":
        if runtime_tokens:
            errors.append(
                "C006 Terminology: external/unknown mode contains runtime token(s): "
                + ", ".join(sorted(runtime_tokens))
            )
        match = (
            UNKNOWN_TERMINOLOGY_ASSET_RE.search(text)
            or UNKNOWN_TERMINOLOGY_META_RE.search(text)
        )
        if match:
            errors.append(
                "C006 Terminology: remove asset/binding metadata "
                f"({match.group(0)!r})."
            )
    else:
        unexpected = sorted(runtime_tokens - set(args.allowed_runtime_token))
        if unexpected:
            errors.append(
                "C006 Terminology: visible mode contains unconfirmed token(s): "
                + ", ".join(unexpected)
            )

    workflow = WORKFLOW_META_RE.search(text)
    if workflow or has_positive_additional_output(text):
        errors.append(
            "C007 Production boundary: remove query/review output language "
            f"({workflow.group(0)!r})."
            if workflow
            else "C007 Production boundary: remove positive instructions for "
            "issues, explanations, commentary, revisions, or other review output."
        )

    client_meta = CLIENT_PROFILE_META_RE.search(text)
    if client_meta:
        errors.append(
            "C009 Client profile: remove profile-selection/merge metadata "
            f"({client_meta.group(0)!r})."
        )

    folded = text.casefold()
    try:
        profile_aliases, registered_profiles = load_profile_registry()
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        errors.append(f"C009 Client profile: cannot load profile registry: {exc}.")
        profile_aliases, registered_profiles = {}, []

    requested_profile = args.format_profile.casefold()
    if requested_profile == "generic":
        if args.require_format_fragment:
            errors.append(
                "C009 Client profile: generic mode cannot require client fragments."
            )
        for profile in registered_profiles:
            for marker in profile.get("client_markers", []):
                if marker.casefold() in folded:
                    errors.append(
                        "C009 Client profile: generic mode contains registered "
                        f"client marker {marker!r}."
                    )
            for pattern_text in profile.get("exclusive_patterns", []):
                if re.search(pattern_text, text, re.I | re.S):
                    errors.append(
                        "C009 Client profile: generic mode contains a registered "
                        f"client-only format fingerprint ({profile['id']})."
                    )
                    break
    else:
        selected_profile = profile_aliases.get(requested_profile)
        if not selected_profile:
            errors.append(
                "C009 Client profile: unregistered format profile ID "
                f"{args.format_profile!r}."
            )
        else:
            if normalize_locale(args.source_locale) != normalize_locale(
                selected_profile["source_locale"]
            ) or normalize_locale(args.target_locale) != normalize_locale(
                selected_profile["target_locale"]
            ):
                errors.append(
                    "C009 Client profile: selected profile locale pair "
                    f"{selected_profile['source_locale']} -> "
                    f"{selected_profile['target_locale']} does not match CLI."
                )
            required_patterns = selected_profile.get("required_any_patterns", [])
            if required_patterns and not any(
                re.search(pattern, text, re.I | re.S)
                for pattern in required_patterns
            ):
                errors.append(
                    "C009 Client profile: prompt contains none of the registered "
                    f"format fingerprints for {selected_profile['id']!r}."
                )
            for pattern_text in selected_profile.get("foreign_patterns", []):
                if re.search(pattern_text, text, re.I | re.S):
                    errors.append(
                        "C009 Client profile: selected profile contains a "
                        "foreign-client format fingerprint."
                    )
                    break

    for fragment in args.require_format_fragment:
        if fragment.casefold() not in folded:
            errors.append(
                f"C009 Client profile: required format fragment missing: {fragment!r}."
            )
    for marker in args.forbid_client_marker:
        if marker.casefold() in folded:
            errors.append(
                f"C009 Client profile: forbidden client marker found: {marker!r}."
            )

    allowed_authorities = {item.casefold() for item in args.allowed_authority}
    for authority in {m.group(0) for m in AUTHORITY_RE.finditer(text)}:
        if authority.casefold() not in allowed_authorities:
            errors.append(
                f"C010 Authority: {authority!r} requires explicit project authority."
            )

    if not has_positive_instruction(
        text,
        re.compile(
            r"\b(?:medical|scientific|clinical|evidence|causal|negation|"
            r"modality|limitation|safety)\b",
            re.I,
        ),
    ):
        errors.append(
            "P001 Pharma fidelity: explicitly preserve medical/scientific meaning, "
            "evidence, causal force, negation, modality, limitations, or safety."
        )
    if not NO_ADD_OMIT_RE.search(text):
        errors.append("P001 Pharma fidelity: no-addition/omission contract missing.")
    if not has_positive_instruction(text, DATA_INTEGRITY_RE):
        errors.append("P002 Data: numeric/dose/unit/statistical integrity missing.")
    if not has_positive_instruction(text, STRUCTURE_RE):
        errors.append("P003 Structure: tags/identifiers/structured content missing.")

    profile_pattern = PROFILE_PATTERNS[args.document_profile]
    if not profile_pattern.search(text):
        errors.append(
            "P004 Document profile: prompt does not demonstrate coverage for "
            f"{args.document_profile!r}."
        )

    for feature in dict.fromkeys(args.require_feature):
        for label, pattern in FEATURE_OBJECTS[feature]:
            if not has_positive_instruction(text, pattern):
                errors.append(
                    f"F001 Feature {feature!r}: missing {label} coverage."
                )

    if not args.allow_fixed_date_format:
        fixed_date = find_prescriptive_fixed_date(text, allowed_source_literals)
        if fixed_date:
            errors.append(
                "F002 Date format: fixed display pattern requires explicit authority "
                f"({fixed_date!r})."
            )

    for conflict in find_format_conflicts(text):
        errors.append(
            f"F003 Format conflict: conflicting {conflict} rules in the same "
            "or unspecified scope."
        )

    if not args.allow_large_literal_inventory:
        literal_count = len(BACKTICK_SPAN_RE.findall(text))
        if literal_count > 40:
            errors.append(
                "F004 Compaction: prompt contains "
                f"{literal_count} backtick spans; replace project inventories with "
                "category rules or explicitly allow a justified large inventory."
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
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Pharma prompt contract lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
