# Patent Translation Prompt Framework

Use this framework only for patent translation prompts. It refines the
repository-wide master template for patent work without importing terminology
or drafting preferences from a single project.

## Contents

1. [Design Principles](#1-design-principles)
2. [Recommended Production Prompt Structure](#2-recommended-production-prompt-structure)
3. [Hard Rules Versus Preferences](#3-hard-rules-versus-preferences)
4. [Generalization Check](#4-generalization-check)
5. [Translation and QA Are Different Prompt Types](#5-translation-and-qa-are-different-prompt-types)
6. [Evaluation Coverage](#6-evaluation-coverage)
7. [Compaction and Artifact Lint](#7-compaction-and-artifact-lint)

## 1. Design Principles

### 1.1 Preserve legal and technical identity

A patent translation must remain traceable to the source. Natural target
language is desirable only within the boundary set by:

- legal scope;
- technical identity;
- defined terms and labels;
- claim dependencies and logical connectors;
- numerical and experimental data;
- source-visible structure.

Do not authorize creative localization, summarization, silent correction, or
editorial improvement.

### 1.2 Separate authorities from references

Classify every terminology input before placing it in the prompt:

1. **Approved external terminology** — authoritative target terms supplied by
   the client or translation platform. Distinguish terms visible to the
   translation model from a termbase used only by an external post-translation
   checker.
2. **Approved project terminology** — verified project terms supplied or
   confirmed by the user.
3. **Protected literal strings** — identifiers, formulas, labels, codes,
   sequences, tags, variables, and other strings that must be copied rather
   than translated.
4. **Source-derived consistency anchors** — recurring concepts whose exact
   target rendering is not externally approved; the model must choose a
   contextually correct rendering and then reuse it consistently.
5. **Illustrative examples** — explanations of a rule. They are not glossary
   entries and must never become hidden target-term locks.

Do not convert automatically extracted or historically observed terms into
approved terminology. A term list inside the prompt must state which class it
belongs to.

### 1.3 Use an explicit priority order only for model-visible authorities

First determine whether approved terminology is actually available to the
translation model. Do not infer variable binding merely because the platform
accepts a two-column termbase or shows a separate terminology-checking stage.

When reviewed terminology is model-visible, use this precedence:

1. explicit client instructions and the approved external glossary;
2. source meaning, legal scope, and technical identity;
3. source-document definitions and established cross-segment terminology;
4. target-jurisdiction patent drafting conventions;
5. fluency and stylistic preferences.

In that mode, add this boundary explicitly:

> Approved glossary terms override inferred terminology, examples, historical
> prompts, and stylistic preferences. Examples and source-derived reference
> terms never override the approved glossary.

If the termbase is uploaded separately, checked only after translation, or its
binding is unknown:

- do not copy it into the static prompt;
- do not invent a runtime variable or placeholder for it;
- do not tell the model that it can access terms it may not see;
- use source-grounded, contextually correct, internally consistent terminology
  rules in the prompt, while leaving termbase enforcement to the platform.

Treat this visibility decision as authoring logic, not production-prompt
content. In the final Role/Style artifact, do not state that a glossary,
termbase, binding, runtime variable, or model-visible terminology is absent,
unknown, or handled elsewhere. The model only needs the executable
source-grounded terminology rule.

If the workflow can receive unreviewed glossaries, do not promise blind
precedence. Glossary cleaning and conflict resolution remain outside the
translation prompt.

### 1.4 Isolate source-only generation from project history

When the task supplies a current source file and language pair but does not
request historical reuse, do not search, enumerate, open, or reuse nearby
prompts, examples, human translations, evaluation exports, or project
artifacts. A matching project name, directory, filename, or language pair is
not authorization. Only load old material that the user explicitly identifies
for comparison, revision, or reuse, and still subject every target wording to
the authority and provenance rules above.

## 2. Recommended Production Prompt Structure

Keep the hierarchy to no more than three Markdown levels. The prompt should
normally contain the following sections in this order.

### A. Role and Task Contract

The default deliverable is one Markdown file containing, in order,
`### Role prompt` and `### Style prompt`. The Role block is concise and
platform-ready; all detailed constraints belong in the Style block. Do not
surround the two blocks with analysis or usage commentary.
Section A supplies the Role block; sections B-H are organized as subsections
inside the single Style block, not as additional top-level prompt fields.

State:

- source and target language;
- patent document type and technical field, if verified;
- target jurisdiction or office only if supplied;
- conservative translation objective;
- output-only contract.

Recommended pattern:

```markdown
### Role prompt
You are a professional patent translator translating from {SOURCE_LANGUAGE}
into {TARGET_LANGUAGE}. Translate the supplied patent text into formal,
jurisdiction-appropriate patent language while preserving its exact legal
scope, technical identity, data, and source-visible structure.

Do not add, omit, summarize, silently correct, or reinterpret source content.
Respond only with the translation.
```

Do not invent a filing office, regulatory framework, client, audience, or
document subtype.

### B. Instruction Priority and Terminology Authority

Place the priority order near the top, before long style or formatting rules.
Choose the applicable terminology mode before writing this section.

If approved terminology is model-visible, use:

```markdown
#### 1. Instruction Priority and Terminology
- Apply instructions in this order: approved client glossary and explicit
  project instructions; source meaning/legal scope/technical identity;
  source-established consistency; target patent convention; style preference.
- Use each context-applicable approved target term provided in the current
  model context exactly. Do not replace it with a synonym or a prompt example.
- Terms shown only as examples or consistency anchors are references, not
  approved glossary entries.
- When no approved term exists, choose the technically and legally correct
  target rendering from context and reuse it for the same concept.
```

If approved terminology is not model-visible or visibility is unknown, omit
all glossary-access claims and use:

```markdown
#### 1. Instruction Priority and Terminology
- Apply instructions in this order: explicit project instructions; source
  meaning/legal scope/technical identity; source-established consistency;
  target patent convention; style preference.
- Choose technically and legally correct terminology from context and reuse
  the same rendering for the same concept. Do not let a short recurring word
  mechanically override the identity of a longer technical entity.
```

Use the block directly. Do not preface or follow it with statements such as
"no glossary was provided," "the termbase is not model-visible," or "binding
is unknown." Those are generator-side facts and do not help the translation
model.

Never emit a placeholder for a glossary unless the user explicitly supplies
the exact platform binding syntax. Do not copy an entire customer glossary
into the static prompt.

### C. Legal and Technical Fidelity

Cover the patent-wide hard rules:

- no addition, omission, unsupported inference, or silent source correction;
- no broadening or narrowing of claims;
- exact preservation of claim numbering, dependencies, alternatives,
  limitations, negation, modality, and logical connectors;
- preservation of any predicate, use, method step, condition, or limitation
  shared by coordinated alternatives; do not leave earlier alternatives
  outside the common legal relationship;
- preservation of the distinction between optional matter and alternative
  matter;
- correct antecedent basis according to the target language and jurisdiction;
- stable mapping between the same technical entity, term, label, and reference
  sign throughout the description and claims;
- preservation of incomplete source fragments as fragments when segment
  boundaries are meaningful.

Do not prescribe one English word globally for a source marker whose legal
effect depends on context. For example, selection language must be rendered
from the actual open or closed scope expressed by the source and any
explicitly applicable approved target wording, not from a universal phrase
pair invented by the prompt.
Do not create a hybrid that combines a closed-list formula with an open-ended
qualifier unless both effects are explicitly present in the source.

When a technical name appears unfamiliar, nonstandard, or visibly corrupted,
preserve the source-supported identity conservatively. Do not silently
normalize it into a different familiar entity or invent missing content. Keep
the same translation-only output contract; source uncertainty does not create
a separate interaction or reporting channel.

### D. Entity, Label, and Terminology Integrity

Require the model to preserve complete technical identity, not just isolated
words. In particular:

- retain the semantic head of a defined entity;
- retain all qualifiers, salt/solvate/hydrate states, stereochemical
  descriptors, polymorph or crystal-form status, and form labels;
- distinguish an entity name from an arbitrary descriptive phrase;
- keep the same label attached to the same entity across the description,
  drawings, examples, tables, and claims;
- avoid both omission and redundant double rendering when composing terms.

Generic diagnostic example:

> If the source identifies “salt X + crystal-form status + label II,” the
> target must preserve all three components. A shortened phrase that keeps only
> “salt X + form II” may lose technical identity; adding “crystal form” twice
> is also wrong.

This example explains a composition check. It is not an approved target term.

### E. Procedures, Data, Structure, and Protected Content

Require exact preservation of:

- experimental actions, actor/object relationships, order, direction of
  addition, qualifiers such as slowly/dropwise/portionwise, conditions, and
  results;
- chemical names, formulas, stereochemistry, sequences, variables, ranges,
  comparators, ratios, values, precision, units, and statistical data;
- headings, paragraphs, claims, lists, tables, figures, captions,
  cross-references, citations, and reference signs;
- tags, placeholders, inline markup, encoded entities, URLs, and file-like
  tokens.

Include a literal protected-string list only when the source inspection or
user input supplies short, verified, high-risk literals. Otherwise express
the protection by category and omit the list. Never leave a protected-string
placeholder in the delivered prompt. Protected strings must be copied
literally; translatable terminology belongs in the approved-terminology or
consistency-anchor class instead.

Distinguish verified source-fixed literals from project-specific target
wording. A short identifier, label, formula, sequence marker, or code span
confirmed in the current source may be listed for literal preservation. A
target-language phrase, source-to-target pair, human-reference wording, or
exact claim/table/figure count needs separate authority or clear operational
value; frequency in the sample does not make it a lock.

Do not globally demand that all source punctuation be copied. Apply target
language punctuation in ordinary prose while preserving punctuation that
controls formulas, chemical notation, legal scope, tags, tables, or protected
strings.

Apply general target-locale rules for punctuation, unit spacing, dates, and
time only to ordinary prose that can be localized without changing identity or
traceability. Do not mechanically normalize formulas, tables, chemical
notation, bibliographic data, or source-fixed strings. Preserve the same
calendar date; absent an explicit client or filing-office convention, use a
clear and unambiguous target-language date expression rather than forcing a
fixed numeric date order.

### F. Patent Register and Controlled Fluency

Use a formal, objective, precise, and impersonal patent register appropriate
to the target locale.

Permit syntactic reordering only when needed for grammatical target-language
patent prose and only when it does not alter:

- legal scope;
- technical relationships;
- entity identity;
- procedure order;
- segment function.

Do not make universal hard rules out of preferences such as:

- one acceptable patent verb instead of another;
- sentence splitting versus joining;
- optional articles outside a claim-scope or antecedent-basis issue;
- preferred caption wording;
- title capitalization, unless a client style guide requires it.

### G. Verified Project Profile

Include only source-verified information that materially helps translation,
such as:

- document subtype;
- technical subdomain;
- unusually high-risk content classes;
- presence of claims, sequences, chemical formulas, tables, tagged text, or
  experimental procedures;
- client-approved drafting conventions.
- a short set of current-source identifiers or labels whose literal
  preservation is both high risk and operationally useful.

Do not hard-code:

- full project-specific compound names merely because they are frequent;
- exact claim, table, or figure counts unless the user explicitly requests
  them or a downstream deterministic control genuinely consumes them; merely
  observing the counts in the source is not sufficient;
- a project term translation inferred from a human reference;
- sample-specific error corrections as universal rules.

Express source-derived consistency anchors as source concepts, entity classes,
or risk categories. Do not turn them into fixed target-language wordings
unless an approved authority supplies those wordings.

### H. Silent Quality Gate and Closing Contract

The Style block may contain a compact translation-time checklist:

1. terminology follows the authority rule stated above and recurring concepts
   remain contextually consistent;
2. each entity retains its full identity and label;
3. claim scope, dependencies, optional/alternative status, open/closed list
   effect, shared predicates or limitations, and connectors unchanged;
4. no addition, omission, or silent correction;
5. procedures preserve actor, object, addition direction, order, manner
   qualifiers such as slowly/dropwise/portionwise, conditions, work-up, and
   results;
6. numbers, units, formulas, tags, and cross-references intact;
7. repeated source concepts rendered consistently;
8. source fragments remain functionally traceable.

The following are generator-side checks, not translation-prompt content. Do
not copy or paraphrase this audit list into the Role/Style artifact. Before
delivery, Prompt Architect verifies that the artifact contains:

- exactly one Role block followed by one Style block;
- no unresolved template placeholder or unconfirmed runtime variable;
- no unapproved target-language fixed wording imported from a historical
  prompt;
- no review, issue-report, interaction, or explanatory output request;
- when terminology binding is unknown or external-only, no glossary,
  termbase, binding, model-visibility, or availability commentary;
- no fixed numeric date pattern unless an approved instruction requires it;
- no exact project counts without operational justification;
- explicit protection of slowly/dropwise/portionwise and equivalent manner
  qualifiers when the source contains chemical or experimental addition,
  dropwise addition, or portionwise charging.

Close by repeating the main production contract:

```markdown
Translate the supplied source from {SOURCE_LANGUAGE} into {TARGET_LANGUAGE}.
Output only the translation.
```

## 3. Hard Rules Versus Preferences

Convert a finding into a prompt-level hard rule only when it is:

- legally or technically material;
- objectively verifiable;
- recurrent or high risk;
- portable to other patent projects of the same class.

Use this routing:

| Finding | Destination |
|---|---|
| Model-visible approved terminology violation | Prompt terminology authority and terminology QA |
| External/post-check termbase violation | Platform terminology check or termbase cleaning, not a fabricated prompt variable |
| Claim-scope or dependency error | Patent hard rule |
| Technical-entity or label loss | Patent hard rule |
| Number, formula, tag, or procedure corruption | Hard rule plus deterministic QA where possible |
| Repeated objective formatting defect | Target-language formatting reference |
| Client drafting convention | Client style guide or approved project instructions |
| Preferential wording | Do not hard-code; retain as optional style guidance if needed |
| Source ambiguity or defect | Conservative, traceable translation without silent correction or an invented replacement |

## 4. Generalization Check

Before adding a rule, ask:

1. Does it remain valid for a different patent family?
2. Does it remain valid outside the current technical example?
3. Is it tied to the source meaning or an approved authority, rather than a
   preferred human reference?
4. Could it conflict with a future client glossary?
5. Is prompt text the correct control layer, or should this be handled by
   glossary cleaning, deterministic validation, segmentation, or human review?

If a rule fails questions 1-3, move it to the project-specific layer or omit
it. If question 5 points elsewhere, document the operational control instead
of overloading the prompt.

## 5. Translation and QA Are Different Prompt Types

Do not create a QA prompt by changing only the role words in a translation
prompt.

A translation prompt must:

- produce only the target translation;
- resolve terminology under the stated authority order;
- silently self-check before output.

A QA prompt must separately define:

- source-versus-target comparison;
- error taxonomy and severity;
- pass/fail meaning;
- whether preferences block delivery;
- whether severity describes the original translation or the reviewed result;
- evidence requirements and output schema;
- a conservative editing rule that prevents unnecessary revisions.

The translation and QA prompts may share the same glossary, protected strings,
and patent-domain risk model, but they must not share an ambiguous output
contract.

## 6. Evaluation Coverage

When testing a revised patent prompt, include unseen examples covering:

- independent and dependent claims;
- open/closed selection language and logical connectors;
- defined terms and antecedent basis;
- entity labels and repeated terminology;
- chemical, biological, mechanical, and electrical patent content as
  applicable;
- procedures with actor/object/order relationships;
- chemical or experimental addition steps with direction, order, and
  slowly/dropwise/portionwise manner qualifiers;
- numbers, ranges, units, formulas, sequences, tables, and tags;
- headings, captions, fragments, and cross-segment continuations;
- glossary-present, glossary-absent, and overlapping-term cases;
- source-side ambiguity that must not be silently corrected;
- dates, unit spacing, and source-fixed technical notation whose identity must
  not be changed by a generic locale rule;
- source-only generation where old project prompts exist nearby but were not
  requested;
- production-only output with no authoring metadata or review workflow.

Do not evaluate only on the project that produced the latest feedback.

## 7. Compaction and Artifact Lint

Compact only after the coverage matrix passes. Compare candidate prompts by
characters, words, or estimated tokens together with a repetition audit;
physical line count is a layout signal, not a quality target. Prefer the
shortest version that still preserves every material legal, technical,
procedural, data, structure, and output control.

For a saved artifact, resolve the validator from the Prompt Architect Skill
root rather than assuming the caller's current directory, then run:

```powershell
python scripts/validate_patent_prompt.py <prompt.md> --terminology-mode unknown
```

Use `--terminology-mode visible` only when the model-visible terminology
binding is explicitly confirmed, and pass each exact confirmed terminology
token with `--allowed-runtime-token`. Pass a placeholder-like token through
`--allowed-source-literal` only when it is verified in the current source and
must be copied literally; never use this option to excuse a generator
placeholder. Add `--require-procedure-manner` only when source inspection finds
chemical or experimental addition, dropwise addition, or portionwise charging;
ordinary mechanical procedures do not trigger it. Fixed date patterns and
exact project counts remain lint failures unless an explicit authority or
operational need justifies the corresponding allow flag.
