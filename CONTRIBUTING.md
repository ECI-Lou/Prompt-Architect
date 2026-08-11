# Contributing

Prompt Architect is maintained as a standalone Codex skill. Changes should improve reusable prompt-generation behavior without introducing project-specific data or portal application code.

## Repository Boundaries

Commit only reusable skill assets:

- `SKILL.md`
- `agents/`
- `references/`
- sanitized `examples/`
- deterministic `scripts/`
- `tests/` and `evals/`
- repository documentation and CI configuration

Never commit:

- files under `projects/`, `local/`, `.codex/`, `.agents/`, or `tmp/`
- real customer source or target documents
- customer termbases, LQA workbooks, internal reports, or generated project prompts
- dependency directories, caches, compiled Python files, or release archives
- credentials, API keys, tokens, or environment files

Do not use `git add -f` to bypass these boundaries.

## Change Workflow

1. Read `SKILL.md` and only the references relevant to the change.
2. Keep reusable rules separate from customer profiles, approved terminology, and project examples.
3. Update tests or evals when behavior changes.
4. Run the package and test checks.
5. Inspect the staged diff before committing.

```powershell
python scripts/validate_skill_package.py
pytest
python scripts/package_skill.py
python scripts/validate_skill_package.py dist/prompt-architect.skill --archive
git diff --check
```

The `.skill` archive is generated output and must not be committed.

## Pull Requests

Describe the current behavior after the change, the reason for the change, affected domains, and validation performed. Do not paste customer content into issues, commit messages, test fixtures, or pull-request descriptions.
