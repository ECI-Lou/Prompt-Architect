# Security and Project-Data Handling

## Supported Repository Scope

This public repository contains reusable Prompt Architect skill assets. It is not an approved storage location for customer data, production documents, credentials, or portal uploads.

## Sensitive Data

Keep all real project files under the ignored `projects/` directory or outside the repository. Keep private reference documents and local-only utilities under the ignored `local/` directory.

Before every push, run:

```powershell
python scripts/validate_skill_package.py
git status --short
git diff --cached --name-only
```

If sensitive data is committed but not pushed, rewrite the unpublished local commit before publishing. If sensitive data has already reached GitHub, deleting it in a later commit is not sufficient because it remains in history. Revoke exposed credentials immediately and coordinate an explicit history-rewrite and force-push; do not perform that destructive operation implicitly.

## Reporting

Report repository-security issues privately to the repository owner. Do not include customer documents, proprietary terminology, access tokens, or exploitable details in a public GitHub issue.
