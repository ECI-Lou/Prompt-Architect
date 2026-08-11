# Prompt Architect

Prompt Architect is a standalone Codex skill that turns source documents or localization requirements into production-ready LLM translation prompts. Its default deliverable is one Markdown artifact containing exactly one `### Role prompt` followed by one `### Style prompt`.

Repository: <https://github.com/ECI-Lou/Prompt-Architect>

## Scope

Prompt Architect supports:

- Pharma and clinical-statistical content
- Medical devices
- Patents
- Games and dialogue localization
- Legal content
- Technical documentation
- Finance
- General business and other content

The skill infers the domain and source risks, applies only the relevant domain and target-language rules, separates approved terminology from protected source literals and consistency anchors, and avoids inventing client or runtime capabilities.

This repository contains the standalone skill only. A document-upload portal, API, browser editor, storage layer, and download workflow are explicitly out of scope and belong to a future application repository.

## Repository Structure

```text
prompt-architect/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── template.md
│   ├── domain_rules.md
│   ├── formatting_standards.md
│   ├── patent_prompt_framework.md
│   ├── pharma_prompt_framework.md
│   ├── client_format_profile_framework.md
│   └── client_format_profiles.json
├── examples/
│   └── *.md
├── scripts/
│   ├── validate_patent_prompt.py
│   ├── validate_pharma_prompt.py
│   ├── validate_skill_package.py
│   └── package_skill.py
├── tests/
│   └── test_*.py
├── evals/
│   └── evals.json
└── .github/workflows/
    └── ci.yml
```

Local working material is intentionally outside the published skill:

- `projects/` contains real project files and local test runs.
- `local/` contains private reference documents and legacy utilities.
- `.codex/`, `.agents/`, `tmp/`, caches, dependencies, and generated packages are also ignored.

Do not force-add files from these locations.

## Resource Loading

Every generation task uses:

1. `SKILL.md`
2. `references/template.md`
3. The matching section of `references/domain_rules.md`
4. The general and target-locale sections of `references/formatting_standards.md`

Patent tasks additionally use `references/patent_prompt_framework.md` and the patent validator. Pharma tasks additionally use `references/pharma_prompt_framework.md` and the Pharma validator. Client format profiles are loaded only when the caller explicitly selects an exact registered profile that matches the language pair.

Historical examples are optional structural references. Source-only generation does not load them by default, and examples never establish approved terminology for a new project.

## Installation

Clone or copy the repository into a Codex skill directory:

```text
$CODEX_HOME/skills/prompt-architect
```

Alternatively, build the deterministic installable archive:

```powershell
python scripts/package_skill.py
```

The archive is written to `dist/prompt-architect.skill`. It contains only runtime skill resources; tests, evals, CI files, local projects, and private material are excluded.

## Usage

Example requests:

```text
Use $prompt-architect to generate an en-US to zh-CN translation prompt from this clinical-statistical DOCX.
```

```text
Use $prompt-architect to create a compact zh-CN to en-US patent translation prompt from these source files.
```

```text
Use $prompt-architect to standardize this game localization prompt while preserving placeholders and inline tags.
```

## Validation

The validator scripts use only the Python standard library. Development tests require `pytest`.

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_skill_package.py
pytest
python scripts/package_skill.py
python scripts/validate_skill_package.py dist/prompt-architect.skill --archive
```

Patent artifact lint:

```powershell
python scripts/validate_patent_prompt.py <prompt.md> --terminology-mode unknown
```

Pharma artifact lint:

```powershell
python scripts/validate_pharma_prompt.py <prompt.md> `
  --source-locale <SOURCE_LOCALE> `
  --target-locale <TARGET_LOCALE> `
  --document-profile <PROFILE> `
  --terminology-mode unknown `
  --format-profile generic
```

Use model-visible terminology or a client profile only when the platform explicitly confirms that binding and supplies the exact token or profile ID.

## Development and Data Safety

See [CONTRIBUTING.md](CONTRIBUTING.md) for the repository workflow and [SECURITY.md](SECURITY.md) for project-data handling rules.

Before committing, verify that Git is not tracking local material:

```powershell
python scripts/validate_skill_package.py
git status --short
```

The public package must contain reusable skill instructions, sanitized examples, deterministic validators, tests, and metadata only. Real source documents, customer deliverables, termbases, LQA workbooks, credentials, and generated analysis artifacts do not belong in this repository.
