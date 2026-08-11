from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate_pharma_prompt.py"
)
SPEC = importlib.util.spec_from_file_location("validate_pharma_prompt", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def args(**overrides):
    values = {
        "source_locale": "en-US",
        "target_locale": "zh-CN",
        "document_profile": "clinical-statistical",
        "terminology_mode": "unknown",
        "format_profile": "generic",
        "allowed_runtime_token": [],
        "allowed_source_literal": [],
        "allowed_authority": [],
        "require_feature": [
            "derivation-logic",
            "partial-dates",
            "assessor-provenance",
            "tag-span",
            "protected-syntax",
        ],
        "require_format_fragment": [],
        "forbid_client_marker": [],
        "allow_fixed_date_format": False,
        "allow_large_literal_inventory": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


VALID_PROMPT = """### Role prompt
You are a professional life-science translator translating clinical-statistical
content from en-US into zh-CN. Preserve complete scientific and clinical
meaning, evidence, causal force, negation, modality, limitations, and safety.
Respond only with the translation.

### Style prompt
#### 1. Evidence and Terminology Authority
Preserve source-established terminology and complete concept identity
consistently.

#### 2. Scientific, Clinical, and Regulatory Fidelity
Do not add, omit, summarize, reinterpret, or silently correct source content.
Treat the source as endpoint definitions and statistical derivation rules.

#### 3. Medical Entity, Definition, Abbreviation, and Terminology Integrity
Preserve complete medical entities, definitions, and abbreviation functions.

#### 4. Clinical Procedures, Statistics, Formatting, Data, Structure, and Protected Content
Preserve every number, dose, unit, range, comparator, threshold, precision,
p-value, confidence interval, and statistic.
Preserve AND/OR logical grouping, shared condition scope, each candidate date
set and candidate data source, earliest/latest aggregation, and event/censoring
branch logic.
Preserve the granularity of every source date operand and explicit imputation.
Keep before, after, within, beyond, more than, at least, on or before, and on
or after unchanged in boundary direction and strict or inclusive effect.
Distinguish the procedure performer from the assessor, adjudicator, reviewer,
and evidence source.
Preserve tag identity, pairing, nesting, and the equivalent semantic span.
Preserve case and ASCII punctuation in source-fixed syntax. Copy datasets,
variables, functions, operators, and quoted coded values exactly.
Preserve each table, flow-chart label, identifier, list, and placeholder.

#### 5. Document-Type Register and Controlled Fluency
Maintain the traceable clinical-statistical register without smoothing logic.

#### 6. Verified Project Constraints
Protect only source-verified high-risk identifiers and content features.

#### 7. Silent Quality Gate and Closing Contract
Ensure the final line preserves meaning, logic, data, and structure.
Output ONLY the Simplified Chinese translation.
"""


class PharmaPromptValidatorTests(unittest.TestCase):
    def test_valid_clinical_statistical_prompt_passes(self):
        self.assertEqual(VALIDATOR.lint(VALID_PROMPT, args()), [])

    def test_flexible_output_only_wording_passes(self):
        prompt = VALID_PROMPT.replace(
            "Respond only with the translation.",
            "Output ONLY the accurate target-language translation.",
        )
        self.assertEqual(VALIDATOR.lint(prompt, args()), [])

    def test_structure_and_role_contract_failures_are_detected(self):
        prompt = VALID_PROMPT.replace(
            "### Style prompt",
            "### Notes\nDo not show this.\n\n### Style prompt",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("C001", joined)

        prompt = VALID_PROMPT.replace("Respond only with the translation.", "")
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("C004", joined)

    def test_unknown_terminology_mode_rejects_tokens_and_metadata(self):
        prompt = VALID_PROMPT.replace(
            "Treat the source as endpoint definitions and statistical derivation rules.",
            "Follow {GLOSSARY_TERMS}; the uploaded termbase is checked after translation.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("C006", joined)

    def test_unknown_mode_rejects_natural_asset_phrasings(self):
        phrasings = (
            "Follow the uploaded glossary.",
            "Use the termbase supplied by the platform.",
            "Apply terminology from the external file.",
            "使用已上传的术语库。",
        )
        anchor = "Treat the source as endpoint definitions and statistical derivation rules."
        for phrase in phrasings:
            with self.subTest(phrase=phrase):
                prompt = VALID_PROMPT.replace(anchor, phrase)
                joined = "\n".join(VALIDATOR.lint(prompt, args()))
                self.assertIn("C006", joined)

    def test_visible_mode_allows_only_confirmed_runtime_token(self):
        prompt = VALID_PROMPT.replace(
            "Treat the source as endpoint definitions and statistical derivation rules.",
            "Use the approved terms in {APPROVED_TERMS}.",
        )
        visible_args = args(
            terminology_mode="visible",
            allowed_runtime_token=["{APPROVED_TERMS}"],
        )
        self.assertEqual(VALIDATOR.lint(prompt, visible_args), [])

        bad = prompt.replace(
            "{APPROVED_TERMS}",
            "{APPROVED_TERMS} and {OTHER_TERMS}",
        )
        joined = "\n".join(VALIDATOR.lint(bad, visible_args))
        self.assertIn("C006", joined)

    def test_profile_selection_metadata_is_rejected(self):
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Load the client format profile from the supplied file.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("C009", joined)

    def test_generic_profile_rejects_foreign_client_marker(self):
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Preserve each table and apply the Johnson & Johnson bracket rule.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("generic mode contains registered client marker", joined)

    def test_selected_profile_uses_registry_and_locale_pair(self):
        joined = "\n".join(
            VALIDATOR.lint(
                VALID_PROMPT,
                args(format_profile="made-up-client"),
            )
        )
        self.assertIn("unregistered format profile", joined)

        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Preserve each table and use full-width comparators in ordinary prose.",
        )
        selected_args = args(format_profile="jnj-enUS-zhCN")
        self.assertEqual(VALIDATOR.lint(prompt, selected_args), [])

        wrong_locale = args(
            source_locale="fr-FR",
            target_locale="zh-CN",
            format_profile="jnj-enUS-zhCN",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, wrong_locale))
        self.assertIn("does not match CLI", joined)

    def test_each_required_feature_has_material_coverage(self):
        cases = {
            "derivation-logic": (
                "Preserve AND/OR logical grouping, shared condition scope, "
                "each candidate date",
                "Preserve each candidate date",
            ),
            "partial-dates": (
                "Preserve the granularity of every source date operand and "
                "explicit imputation.",
                "Preserve source dates.",
            ),
            "assessor-provenance": (
                "Distinguish the procedure performer",
                "Preserve the procedure",
            ),
            "tag-span": (
                "equivalent semantic span",
                "surrounding text",
            ),
            "protected-syntax": (
                "case and ASCII punctuation",
                "syntax",
            ),
        }
        for feature, (old, new) in cases.items():
            with self.subTest(feature=feature):
                prompt = VALID_PROMPT.replace(old, new)
                joined = "\n".join(VALIDATOR.lint(prompt, args()))
                self.assertIn(f"Feature {feature!r}", joined)

    def test_reverse_polarity_does_not_satisfy_feature_coverage(self):
        prompt = VALID_PROMPT.replace(
            "Distinguish the procedure performer from the assessor, adjudicator, "
            "reviewer,\nand evidence source.",
            "Conflate the procedure performer with the assessor, adjudicator, "
            "reviewer,\nand evidence source.",
        ).replace(
            "Preserve case and ASCII punctuation in source-fixed syntax. Copy "
            "datasets,\nvariables, functions, operators, and quoted coded values exactly.",
            "Do not preserve case and ASCII punctuation in source-fixed syntax. "
            "Datasets,\nvariables, functions, operators, and quoted coded values "
            "may be normalized freely.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("assessor-provenance", joined)
        self.assertIn("protected-syntax", joined)

    def test_translation_only_contract_handles_natural_and_adversarial_forms(self):
        natural = VALID_PROMPT.replace(
            "Respond only with the translation.",
            "Provide the final translation and nothing else.",
        ).replace(
            "Output ONLY the Simplified Chinese translation.",
            "Return the final translation and nothing else.",
        )
        self.assertEqual(VALIDATOR.lint(natural, args()), [])

        adversarial = VALID_PROMPT.replace(
            "Respond only with the translation.",
            "Output explanations only; after that provide the translation.",
        )
        joined = "\n".join(VALIDATOR.lint(adversarial, args()))
        self.assertIn("C004", joined)

        adversarial = VALID_PROMPT.replace(
            "Output ONLY the Simplified Chinese translation.",
            "List all issues after the translation.",
        )
        joined = "\n".join(VALIDATOR.lint(adversarial, args()))
        self.assertIn("C007", joined)

        adversarial = VALID_PROMPT.replace(
            "Respond only with the translation.",
            "This is not translation-only; commentary may follow.",
        )
        joined = "\n".join(VALIDATOR.lint(adversarial, args()))
        self.assertIn("C004", joined)

    def test_wrong_or_missing_locale_pair_fails(self):
        joined = "\n".join(
            VALIDATOR.lint(
                VALID_PROMPT,
                args(source_locale="fr-FR", target_locale="de-DE"),
            )
        )
        self.assertIn("C003", joined)

        prompt = VALID_PROMPT.replace("from en-US into zh-CN", "for this project")
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("C003", joined)

    def test_patient_facing_profile_does_not_require_derivation_features(self):
        prompt = VALID_PROMPT.replace(
            "clinical-statistical\ncontent",
            "patient-facing informed consent content",
        ).replace(
            "Treat the source as endpoint definitions and statistical derivation rules.",
            "Use comprehensible patient-facing language without weakening safety.",
        )
        patient_args = args(
            document_profile="patient-facing",
            require_feature=[],
        )
        self.assertEqual(VALIDATOR.lint(prompt, patient_args), [])

    def test_fixed_date_and_unapproved_authority_fail(self):
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Use YYYY-MM-DD for every FDA submission date.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("F002", joined)
        self.assertIn("C010", joined)

        allowed = args(
            allow_fixed_date_format=True,
            allowed_authority=["FDA"],
        )
        self.assertEqual(VALIDATOR.lint(prompt, allowed), [])

    def test_conflicting_client_format_rules_fail(self):
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Use full-width comparator operators in ordinary prose, but use "
            "half-width comparator operators in ordinary prose.",
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("F003", joined)

    def test_scoped_comparator_exception_is_not_a_conflict(self):
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Use full-width comparator operators in ordinary prose; preserve "
            "half-width comparator operators in source-fixed code.",
        )
        self.assertEqual(
            VALIDATOR.lint(
                prompt,
                args(format_profile="jnj-enUS-zhCN"),
            ),
            [],
        )

    def test_fixed_date_negative_and_source_literal_are_allowed(self):
        negative = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Do not force YYYY-MM-DD as a display format.",
        )
        self.assertEqual(VALIDATOR.lint(negative, args()), [])

        literal = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            "Preserve source-fixed YYYY-MM-DD literally inside code.",
        )
        self.assertEqual(VALIDATOR.lint(literal, args()), [])

    def test_utf8_bom_is_accepted(self):
        self.assertEqual(VALIDATOR.lint("\ufeff" + VALID_PROMPT, args()), [])

    def test_large_project_literal_inventory_requires_justification(self):
        inventory = " ".join(f"`TOKEN_{i}`" for i in range(41))
        prompt = VALID_PROMPT.replace(
            "Preserve each table, flow-chart label, identifier, list, and placeholder.",
            inventory,
        )
        joined = "\n".join(VALIDATOR.lint(prompt, args()))
        self.assertIn("F004", joined)


if __name__ == "__main__":
    unittest.main()
