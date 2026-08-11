from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate_patent_prompt.py"
)
SPEC = importlib.util.spec_from_file_location("validate_patent_prompt", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def args(**overrides):
    values = {
        "terminology_mode": "unknown",
        "allowed_runtime_token": [],
        "allowed_source_literal": [],
        "require_procedure_manner": False,
        "allow_fixed_date_format": False,
        "allow_project_counts": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


VALID_PROMPT = """### Role prompt
You are a professional patent translator from zh-CN into en-US.
Respond only with the translation.

### Style prompt
Use contextually correct terminology consistently.
Preserve claim scope, complete entity identity, identifiers such as ABC-12,
and the same calendar date without imposing an ambiguous numeric order.
Preserve actor, object, addition direction, order, and manner qualifiers such
as slowly, dropwise, and portionwise.
Output only the translation.
"""


class PatentPromptValidatorTests(unittest.TestCase):
    def test_valid_unknown_mode_prompt_passes(self):
        self.assertEqual(
            VALIDATOR.lint(
                VALID_PROMPT,
                args(require_procedure_manner=True),
            ),
            [],
        )

    def test_authoring_metadata_and_workflow_leaks_fail(self):
        prompt = VALID_PROMPT.replace(
            "Use contextually correct terminology consistently.",
            "No glossary binding is model-visible; output a query if uncertain.",
        )
        errors = VALIDATOR.lint(prompt, args())
        joined = "\n".join(errors)
        self.assertIn("Terminology boundary", joined)
        self.assertIn("Production boundary", joined)

    def test_fixed_date_and_project_counts_fail_without_authority(self):
        prompt = VALID_PROMPT + "\nUse MM/DD/YYYY for Figures 1-13 and claims 1-21.\n"
        errors = VALIDATOR.lint(prompt, args())
        joined = "\n".join(errors)
        self.assertIn("Date boundary", joined)
        self.assertIn("Project-profile boundary", joined)

    def test_visible_mode_can_reference_confirmed_glossary(self):
        prompt = VALID_PROMPT.replace(
            "Use contextually correct terminology consistently.",
            "Use the approved glossary terms supplied in the current context.",
        )
        self.assertEqual(
            VALIDATOR.lint(prompt, args(terminology_mode="visible")),
            [],
        )

    def test_unknown_mode_rejects_glossary_runtime_token(self):
        prompt = VALID_PROMPT + "\nUse {GLOSSARY_TERMS}.\n"
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("runtime tokens" in error for error in errors))

    def test_terminology_runtime_tokens_are_case_insensitive(self):
        unknown_prompt = VALID_PROMPT + "\nUse {glossary_terms}.\n"
        self.assertTrue(
            any("runtime tokens" in error for error in VALIDATOR.lint(unknown_prompt, args()))
        )
        visible_prompt = VALID_PROMPT + "\nUse {approved_terms}.\n"
        self.assertTrue(
            any(
                "unconfirmed" in error
                for error in VALIDATOR.lint(
                    visible_prompt,
                    args(terminology_mode="visible"),
                )
            )
        )

    def test_verified_source_literals_can_be_allowlisted(self):
        prompt = VALID_PROMPT + "\nCopy [TARGET] and {TERMS} literally.\n"
        self.assertEqual(
            VALIDATOR.lint(
                prompt,
                args(allowed_source_literal=["[TARGET]", "{TERMS}"]),
            ),
            [],
        )

    def test_generic_template_placeholders_are_rejected(self):
        prompt = VALID_PROMPT + "\nUse [TONE_DESCRIPTION].\n"
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("Placeholder" in error for error in errors))

    def test_generic_brace_tokens_require_an_allowlist(self):
        prompt = VALID_PROMPT + "\nUse {TB} and {runtime}.\n"
        self.assertTrue(
            any("runtime tokens" in error for error in VALIDATOR.lint(prompt, args()))
        )
        self.assertTrue(
            any(
                "unconfirmed" in error
                for error in VALIDATOR.lint(
                    prompt,
                    args(terminology_mode="visible"),
                )
            )
        )
        self.assertEqual(
            VALIDATOR.lint(
                prompt,
                args(
                    terminology_mode="visible",
                    allowed_runtime_token=["{TB}", "{runtime}"],
                ),
            ),
            [],
        )

    def test_visible_mode_rejects_unconfirmed_terminology_token(self):
        prompt = VALID_PROMPT + "\nUse {INVENTED_TERMS}.\n"
        errors = VALIDATOR.lint(prompt, args(terminology_mode="visible"))
        self.assertTrue(any("unconfirmed" in error for error in errors))
        self.assertEqual(
            VALIDATOR.lint(
                prompt,
                args(
                    terminology_mode="visible",
                    allowed_runtime_token=["{INVENTED_TERMS}"],
                ),
            ),
            [],
        )

    def test_scientific_binding_is_not_runtime_metadata(self):
        prompt = (
            VALID_PROMPT
            + "\nPreserve receptor binding assays, binding affinity data, "
            "and receptor-binding terminology.\n"
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_terminology_technology_is_not_asset_metadata(self):
        prompt = (
            VALID_PROMPT
            + "\nPreserve the glossary database, termbase synchronization, "
            "and terminology-search relationships described by the invention.\n"
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_software_patent_query_is_not_workflow_metadata(self):
        prompt = (
            VALID_PROMPT
            + "\nPreserve database queries, query-plan relationships, a system "
            "that generates a database query, and output query results.\n"
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_source_fixed_date_token_is_not_a_locale_rule(self):
        prompt = VALID_PROMPT + "\nCopy the source-fixed YYYY-MM-DD token literally.\n"
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_literal_marker_may_follow_source_fixed_date_token(self):
        prompt = VALID_PROMPT + "\nCopy YYYY-MM-DD verbatim.\n"
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_use_source_fixed_date_token_is_not_a_format_instruction(self):
        prompt = VALID_PROMPT + "\nUse the source-fixed YYYY-MM-DD token literally.\n"
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_explicit_source_literal_allowlist_has_priority(self):
        prompt = VALID_PROMPT + "\nRender all dates as YYYY-MM-DD.\n"
        self.assertEqual(
            VALIDATOR.lint(
                prompt,
                args(allowed_source_literal=["YYYY-MM-DD"]),
            ),
            [],
        )

    def test_multiline_source_fixed_date_token_is_allowed(self):
        prompt = (
            VALID_PROMPT
            + "\nPreserve the source-fixed token\nYYYY-MM-DD literally.\n"
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_prescriptive_date_rule_cannot_hide_behind_literal_language(self):
        prompt = (
            VALID_PROMPT
            + "\nPreserve source-fixed notation, but render all dates as MM/DD/YYYY.\n"
        )
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("Date boundary" in error for error in errors))

    def test_written_out_numeric_date_order_fails(self):
        prompt = VALID_PROMPT + "\nUse month/day/year for all dates.\n"
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("Date boundary" in error for error in errors))

    def test_role_and_closing_contracts_are_both_required(self):
        no_role_contract = VALID_PROMPT.replace(
            "Respond only with the translation.",
            "Translate accurately.",
        )
        errors = VALIDATOR.lint(no_role_contract, args())
        self.assertTrue(any("Role prompt" in error for error in errors))

    def test_empty_style_block_fails(self):
        prompt = """### Role prompt
Respond only with the translation.

### Style prompt
"""
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("Style prompt block is empty" in error for error in errors))

    def test_platform_heading_case_is_exact(self):
        prompt = VALID_PROMPT.replace("### Role prompt", "### Role Prompt")
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("expected exactly" in error for error in errors))

    def test_mechanical_procedure_does_not_require_chemical_manner_flag(self):
        prompt = VALID_PROMPT.replace(
            "Preserve actor, object, addition direction, order, and manner qualifiers such\n"
            "as slowly, dropwise, and portionwise.",
            "Preserve the actor, object, sequence, conditions, and result of each mechanical test.",
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_project_profile_manner_words_do_not_satisfy_protection(self):
        prompt = VALID_PROMPT.replace(
            "Preserve actor, object, addition direction, order, and manner qualifiers such\n"
            "as slowly, dropwise, and portionwise.",
            "The project profile contains slowly, dropwise, and portionwise additions.",
        )
        errors = VALIDATOR.lint(prompt, args(require_procedure_manner=True))
        self.assertTrue(any("Procedure coverage" in error for error in errors))

    def test_unresolved_template_token_fails(self):
        prompt = VALID_PROMPT.replace("zh-CN", "[SOURCE_LANG]")
        errors = VALIDATOR.lint(prompt, args())
        self.assertTrue(any("Placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
