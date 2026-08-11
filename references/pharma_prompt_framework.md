# Pharma Translation Prompt Framework

Use this framework only for pharmaceutical, clinical, regulatory,
medical-scientific, pharmacovigilance, CMC, and related life-science
translation prompts. It refines the repository-wide master template without
importing terminology or formatting preferences from one client or one
evaluated project.

## Contents

1. [Design Principles](#1-design-principles)
2. [Document-Type Dispatch](#2-document-type-dispatch)
3. [Recommended Production Prompt Structure](#3-recommended-production-prompt-structure)
4. [Pharma Coverage Matrix](#4-pharma-coverage-matrix)
5. [Hard Rules Versus External Controls](#5-hard-rules-versus-external-controls)
6. [Generalization and Evaluation](#6-generalization-and-evaluation)
7. [Compaction and Artifact Lint](#7-compaction-and-artifact-lint)

## 1. Design Principles

### 1.1 Preserve scientific and clinical meaning

Natural target-language prose is desirable only within the boundaries set by
the source. Preserve:

- medical facts, definitions, hypotheses, and limitations;
- certainty, uncertainty, modality, negation, causality, association, and
  temporal sequence;
- severity, seriousness, expectedness, and other safety distinctions;
- clinical endpoint definitions and analysis-population scope;
- dose, route, frequency, duration, time point, and treatment relationships;
- numeric precision, statistical logic, and source-visible structure.

Do not authorize summarization, unsupported inference, silent source
correction, or editorial improvement.

### 1.2 Separate terminology from semantic control

An external termbase can control approved word choices, but it cannot protect
the complete meaning of an endpoint, a date-selection rule, an assessor
relationship, or a Boolean condition. Keep these layers distinct:

1. **Model-visible approved terminology** — use only when the exact approved
   terms are actually supplied to the translation model.
2. **External terminology control** — a termbase used by a separate
   post-translation checker; do not invent a prompt variable for it.
3. **Protected source literals** — dataset names, variables, codes, quoted
   coded values, functions, operators, tags, identifiers, and other strings
   that must be copied exactly.
4. **Source-derived consistency anchors** — recurring complete concepts whose
   target wording is not externally approved; choose from context and reuse
   consistently.
5. **Illustrative examples** — explanations of risk, never hidden terminology
   locks.

Do not convert an automatically extracted term, a human reference
translation, or an evaluator preference into an approved source-to-target
mapping.

### 1.3 Use explicit authority and formatting boundaries

If approved terminology is model-visible, use this priority:

1. explicit current-project instructions and context-applicable approved
   terminology;
2. source scientific/clinical meaning, data identity, and source-fixed
   notation;
3. source definitions and established cross-segment consistency;
4. applicable document-type and regulatory conventions that are actually
   identified;
5. fluency and stylistic preference.

If terminology is external-only or its visibility is unknown, omit all
glossary-access claims and use source-grounded terminology consistency rules.
Do not mention the missing or external asset in the production prompt.

Formatting has a separate precedence:

1. source meaning, values, logic, and protected source content;
2. explicit current-project instructions;
3. one explicitly selected client format profile within its stated scope;
4. safe target-locale defaults for ordinary prose;
5. general style preferences.

A client format profile may override a locale default. It must not alter
medical meaning, numeric value, logical strictness, code syntax, tag identity,
or genuinely source-fixed/protected content. If an approved client rule
governs a visible display notation, classify that notation as client-governed
ordinary/display content rather than simultaneously calling it source-fixed;
do not create an exception that allows protected code or literals to drift.

### 1.4 Isolate source-only generation

When the caller supplies only a current source file and language pair:

- infer document function, audience, register, and high-risk content from that
  source;
- do not search for or activate nearby customer prompts, old translations,
  evaluation workbooks, or style profiles;
- do not infer a client profile from a company name in the source, filename,
  directory, or historical project name;
- use the generic domain framework and safe target-locale defaults only.

Activate a client format profile only when the user or trusted project
metadata explicitly identifies the exact profile.

## 2. Document-Type Dispatch

Select the narrowest applicable primary profile. Add a secondary module only
when the current source genuinely mixes functions.

| Document profile | Register and dominant risks |
|---|---|
| `clinical-protocol` | Prospective instructions, eligibility, interventions, visits, assessments, schedule and conditional obligations |
| `clinical-statistical` | SAP/CSR tables, endpoint definitions, derivation specifications, analysis datasets, event/censoring logic, partial dates, Boolean conditions |
| `regulatory-label` | Indications, dosage, contraindications, warnings, adverse reactions, mandated headings and safety force |
| `pharmacovigilance` | Case chronology, reporter attribution, seriousness/expectedness, causality, coded terms and follow-up status |
| `patient-facing` | ICF, patient instructions, questionnaires and leaflets; accurate but comprehensible language without technical oversimplification |
| `cmc-quality` | Materials, composition, manufacturing steps, specifications, analytical methods, acceptance criteria and batch identity |
| `nonclinical` | Species, model, exposure, toxicology, pathology, methods and evidence strength |
| `medical-scientific` | Publications, medical information and scientific summaries; preserve claims, citations and evidentiary qualification |
| `general-pharma` | Conservative fallback when no narrower profile is supported |

Do not load clinical-statistical censoring and code rules into every Pharma
prompt. Do not apply a regulatory-statistical register to patient-facing text.
Do not reorganize a document into an authority-specific template unless the
user or project metadata explicitly requires that adaptation.

## 3. Recommended Production Prompt Structure

The deliverable contains exactly one `### Role prompt` followed by one
`### Style prompt`. Section A supplies the Role block. Sections B-H are
subsections inside the single Style block.

### A. Role and Translation Contract

State:

- source and target language;
- verified Pharma document profile and audience;
- conservative scientific/clinical translation objective;
- translation-only output contract.

Recommended pattern:

```markdown
### Role prompt
You are a professional life-science translator translating from
{SOURCE_LANGUAGE} into {TARGET_LANGUAGE}. Translate the supplied
{VERIFIED_DOCUMENT_PROFILE} content accurately and naturally while preserving
its complete scientific and clinical meaning, evidence, data, logic, and
source-visible structure.

Do not add, omit, summarize, silently correct, or reinterpret source content.
Respond only with the translation.
```

Do not invent a client, regulatory authority, target-market registration
status, audience, or document subtype.

### B. Evidence and Terminology Authority

Place the executable priority rule near the top. In external-only or unknown
terminology mode, use:

```markdown
#### 1. Evidence and Terminology Authority
- Apply instructions in this order: explicit current-project instructions;
  source scientific/clinical meaning and data identity; source definitions
  and established consistency; applicable document convention; style
  preference.
- Choose terminology from the complete source concept and its context, then
  reuse the same rendering for that concept. Do not let a short recurring word
  mechanically override a longer medical or statistical entity.
```

Use model-visible terminology wording only when the exact binding is
confirmed. Do not put authoring explanations about terminology assets in the
production artifact.

### C. Scientific, Clinical, and Regulatory Fidelity

Require preservation of:

- every claim, definition, condition, exception, limitation, negation, modal
  force, causal statement, association, and uncertainty qualifier;
- treatment, disease, safety, endpoint, assessment, and outcome relationships;
- source evidence level or grading when it is actually present;
- warning and contraindication force, scope, hierarchy, and applicability;
- source ambiguity without inventing a missing relation.

Do not silently turn timing into causality, association into causation,
possibility into certainty, or a criterion for an endpoint into trial
eligibility.

### D. Medical Entity, Definition, Abbreviation, and Terminology Integrity

Protect complete entities rather than isolated words:

- drug plus active moiety, salt/form, strength, dose, route, frequency and
  duration;
- disease plus stage, grade, subtype, status and biomarker;
- endpoint plus definition, time origin, assessment time, population, event
  and censoring rule;
- specimen plus collection context, assay, analyte, method and time point;
- safety concept plus event, severity, seriousness, expectedness, causality
  and outcome where present.

Distinguish:

- machine identifiers and coded values, which are copied exactly;
- defined labels and source-fixed names;
- domain abbreviations in prose, whose handling depends on definition and
  context;
- translatable full medical concepts.

Do not globally preserve or expand every abbreviation. Preserve its function,
definition lifecycle, casing, and identifier status.

### E. Clinical Procedures, Statistics, Formatting, Data, Structure, and Protected Content

Require exact preservation of:

- who receives, performs, evaluates, confirms, reports, or reviews an action;
- intervention, route, sequence, timing, specimen collection and assessment
  relationships;
- N/n and denominator, p-values, confidence intervals, estimates, precision,
  ranges, comparators and inclusion/exclusion boundaries;
- candidate events or dates, filters, AND/OR grouping, branch precedence,
  earliest/latest selection, missingness, imputation, event and censoring
  branches;
- the granularity of every source operand, including year, month-year and
  complete date, plus any explicit imputation rule; do not silently invent a
  day, describe a year as a day, or normalize a source comparison into a
  different comparison. If the source deliberately compares mixed
  granularities, preserve that relation traceably rather than repairing it;
- tables, lists, flow-chart nodes, headings, fragments and cross-segment
  continuations;
- tag names, pairing, nesting and the semantic span enclosed by each tag.

For assessors such as an investigator, central laboratory, adjudication
committee, or independent image review, preserve whether the source names the
performer of a procedure, the assessor, or the evidence source. Do not turn an
assessment source into the person who performed a scan or test.

Use two content classes for mixed narrative and program logic:

1. **Executable or source-fixed syntax** — preserve dataset and variable names,
   case, functions, operators, ASCII punctuation, quotes, literal values and
   grouping exactly.
2. **Human-readable labels or pseudo-code prose** — translate explanatory
   wording while preserving variables, values, Boolean scope, item boundaries
   and operation meaning.

Compact appearance, uppercase, `#`, or `=` alone does not prove that a string
is code.

Place all resolved target-locale and selected client formatting rules in this
section. Apply them only to their compiled scope. Do not put profile names,
selection logic, competing values, or format merge instructions in the
production prompt.

### F. Document-Type Register and Controlled Fluency

Use the register selected in Section 2. Permit syntactic reordering or sentence
splitting only when it does not alter:

- scientific or clinical meaning;
- time and logical scope;
- complete entity identity;
- actor, assessor or evidence-source attachment;
- data, code, tag span or segment function.

For patient-facing content, prefer understandable target-language wording
without weakening warnings or changing informed-consent meaning. For
clinical-statistical and CMC content, preserve traceability even when the
source is dense or fragmentary.

### G. Verified Project Constraints

Include only verified facts that materially change translation strategy:

- primary document profile and audience;
- scientific or therapeutic subdomain;
- presence of controlled terminology, safety content, derivation logic,
  partial dates, code-like syntax, tables, flow charts, tags or formulas;
- a short list of current-source identifiers whose literal preservation is
  both high risk and operationally useful;
- source-verified display/content features that determine which already
  compiled locale or client formatting rules are relevant.

Do not include:

- a synopsis of the whole source;
- long inventories of medical terms, variables or values;
- exact section/table counts without an operational reason;
- fixed target terminology inferred from a human reference;
- rules from a different client or an unselected historical prompt;
- client/profile-selection, file-path or merge-process commentary.

The applicable formatting rules belong in Section E. This section records only
current-source constraints and protected literals, not a client-profile
concept or customer-rule inventory.

### H. Silent Quality Gate and Closing Contract

Use a compact checklist:

1. medical meaning, evidence, negation, modality, causal force and limitations
   are unchanged;
2. complete medical entities, definitions and abbreviations retain their
   identity;
3. source operand granularity, boundaries, candidate sets, AND/OR scope, extrema and
   event/censoring branches remain traceable where present;
4. actor, assessor and evidence-source attachments remain correct;
5. numbers, dose, units, statistics, code, literals and identifiers are intact;
6. structured labels remain translatable where appropriate, while tags retain
   identity, pairing, nesting and equivalent semantic span;
7. only the explicitly selected client formatting rules are applied, and only
   within their scope;
8. there is no addition, omission or silent source correction.

Close with:

```markdown
Translate the supplied source from {SOURCE_LANGUAGE} into {TARGET_LANGUAGE}.
Output only the translation.
```

## 4. Pharma Coverage Matrix

Run this matrix before compaction. A category may be omitted from the project
profile when the source does not contain it, but the relevant domain red line
must remain available to the selected document module.

| Coverage | Risks to control |
|---|---|
| Evidence and assertion | Negation, modality, certainty, causality, association, severity, seriousness, expectedness, temporality and limitations |
| Complete entities | Drug/form/dose/route/frequency; disease/stage/subtype/biomarker; endpoint definition/population/time origin/event/censoring; specimen/assay/analyte/time point |
| Clinical procedures | Recipient, performer, assessor, evidence source, intervention, sequence, timing and result |
| Statistical and temporal logic | N/n, denominator, estimates, precision, strict/inclusive boundaries, preservation of each source date operand and explicit imputation, candidate sets, AND/OR, extrema, missingness, event/censoring |
| Data and protected syntax | Values, units, case, variables, datasets, functions, operators, quotes, ASCII punctuation, literal codes and grouping |
| Controlled terminology | Coding-system/version/level only when identified; preserve hierarchy, item boundaries, order and code-term pairing |
| Structure and tags | Tables, lists, flow charts, headings, fragments, tag identity/pairing/nesting and equivalent semantic span |
| Register | Document-type and audience-specific delivery without changing meaning or safety force |
| Client formatting | Exactly one explicitly selected profile; scoped rules compiled without foreign-client leakage |
| Output contract | Translation only; no explanation, issue list, query, review report or revised-translation schema |

## 5. Hard Rules Versus External Controls

| Finding | Destination |
|---|---|
| Model-visible approved terminology violation | Terminology authority and terminology QA |
| External/post-check termbase choice | Termbase cleaning/checking, not a fabricated prompt variable |
| Evidence, negation, causal-force or safety-scope error | Pharma hard rule |
| Endpoint, temporal, statistical or derivation-logic error | Applicable Pharma document module |
| Actor/assessor/evidence-source error | Pharma hard rule |
| Number, code, literal, tag-span or structure corruption | Hard rule plus deterministic QA where possible |
| MedDRA or another controlled term choice | Version-matched approved resource/TB; prompt protects hierarchy and identity |
| Repeated objective locale defect | Target-locale reference only if it is genuinely cross-client |
| Exact Unicode, spacing, range, bracket or count convention | Explicit client format profile unless independently universal |
| Preferential wording | Do not hard-code |
| Source ambiguity or suspected typo | Conservative, traceable translation without silent correction |

## 6. Generalization and Evaluation

Before promoting a finding to the generic Pharma framework, ask:

1. Does it remain valid for another client and project?
2. Does it remain valid for the same document profile outside the current
   therapeutic area?
3. Is it objectively supported by source meaning or an approved authority?
4. Could it conflict with a future termbase or client format profile?
5. Is prompt text the right control layer, or should the issue be handled by
   terminology assets, deterministic validation, segmentation or upstream
   repair?

Test revised Pharma prompts on unseen examples from more than one document
profile. Include, as applicable:

- strict and inclusive temporal boundaries and partial dates;
- candidate-date sets, shared extrema, AND/OR scope and event/censoring logic;
- investigator or independent-review assessment provenance;
- code-like syntax, quoted values, human-readable labels and mixed tables;
- tag semantic span, fragments and flow-chart nodes;
- controlled terminology with external-only and model-visible modes;
- patient-facing or labeling content that must not inherit
  clinical-statistical code rules;
- suspected source typos or codes that must not be silently normalized;
- generic mode, one selected client profile, and foreign-client leakage checks.

Human LQA labels and reference translations are evidence, not automatic ground
truth. Verify the source relation and independent domain practice before
creating a hard rule.

## 7. Compaction and Artifact Lint

Compact only after the coverage matrix passes. Prefer category rules over long
lists of project tokens. Keep a short literal list only when source inspection
shows that exact copying is high risk and useful.

For a saved artifact, resolve the validator from the Prompt Architect Skill
root and run:

```powershell
python scripts/validate_pharma_prompt.py <prompt.md> `
  --source-locale en-US `
  --target-locale zh-CN `
  --document-profile general-pharma `
  --terminology-mode unknown `
  --format-profile generic
```

Choose the actual document profile. Use `--terminology-mode visible` only when
the exact model-visible terminology token is confirmed. Select a non-generic
format profile only when the user or trusted project metadata explicitly
authorizes it. Add feature flags required by the inspected source, such as
`derivation-logic`, `partial-dates`, `assessor-provenance`, or `tag-span`.

Generator-side lint verifies:

- exactly one Role block followed by one Style block;
- translation-only contracts in the Role and at the end of Style;
- no unresolved placeholder or unconfirmed runtime variable;
- no terminology-asset, profile-selection, query or review metadata;
- no invented authority or unapproved target lock;
- no unselected client fingerprint or conflicting format rule;
- the applicable document and feature coverage;
- no unnecessarily large project-token inventory.
