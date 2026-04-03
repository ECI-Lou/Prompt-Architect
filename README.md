# Prompt Architect

Prompt Architect is a domain-aware skill for turning raw translation requirements into standardized, production-ready LLM prompts with built-in terminology, formatting, and localization rules.

## What It Does

This skill helps Codex generate translation prompts that are:

- Structured for real translation workflows, not one-off demos
- Adapted to domain-specific requirements such as pharma, patent, legal, and game localization
- Aware of target-language formatting conventions
- Reusable across portals, vendors, and project types

Instead of producing a vague "translate this well" instruction, Prompt Architect assembles a prompt package that can include role definition, style rules, terminology controls, formatting normalization, and project-specific constraints.

## Core Capabilities

- Generate new translation System Prompt / Style Prompt / User Prompt sets
- Infer likely domain rules from source content
- Apply language-pair formatting standards such as `zh-CN`, `ja-JP`, `ru-RU`, `pt-BR`, and more
- Reuse historical prompt patterns without leaking project-specific content
- Normalize prompt structure across different translation portals or LLM workflows

## Supported Domains

- Pharma
- Medical Devices
- Patent
- Game
- Legal
- Tech Docs
- Finance
- General Business / Other

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
│   └── formatting_standards.md
└── examples/
    └── *.md
```

## How It Works

Prompt Architect follows a four-step workflow:

1. Extract the minimum required information from the request or source text.
2. Load only the relevant domain rules and target-language formatting standards.
3. Optionally inspect one closely matched historical example.
4. Generate a structured prompt that can be used directly in translation workflows.

The skill is intentionally conservative about context loading. It favors one matching example over many, and it does not copy project-specific glossaries, world-building, or client terminology into new prompts unless the user explicitly provides them.

## Example Trigger Requests

```text
Use $prompt-architect to create a translation system prompt for an en-US to zh-CN clinical study document.
```

```text
Use $prompt-architect to turn this patent translation brief into a reusable style prompt for ar-SA to en-US work.
```

```text
Use $prompt-architect to standardize our game localization prompt across multiple vendors.
```

## Why This Skill Exists

Most translation prompts fail in one of two ways:

- They are too generic to enforce terminology, formatting, and compliance rules
- They are too project-specific to reuse safely

Prompt Architect sits in the middle. It keeps the prompt reusable, while still injecting the domain and language-pair rules that matter in production.

## Installation

Place this folder under your Codex skills directory so it can be discovered as `prompt-architect`.

Typical location:

```text
$CODEX_HOME/skills/prompt-architect
```

## Notes

- `SKILL.md` is optimized for model use.
- `README.md` is user-facing repository documentation.
- `references/` contains reusable rule libraries.
- `examples/` provides structural inspiration, not copy-paste templates.
- JUNCTION TEST 2026-03-27