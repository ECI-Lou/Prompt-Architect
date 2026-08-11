# Client Format Profile Framework

Use this framework whenever a user supplies, names, or selects a customer
style guide, Unicode prompt, formatting prompt, or other client-specific
format asset. It controls how Prompt Architect reads and compiles that asset;
it is not itself content for the production translation prompt.

Known approved profiles and their deterministic lint fingerprints are
registered in `references/client_format_profiles.json`. Adding a new customer
requires an explicit registry entry; do not pass an arbitrary profile ID and
treat it as approved.

## 1. Activation

Activate a client format profile only through one of these trusted inputs:

- the user explicitly identifies the profile or style-guide file;
- the caller supplies an exact profile ID;
- trusted project metadata supplies an exact, versioned profile ID.

Do not activate a profile because:

- a company name appears in the source;
- the filename or directory resembles an earlier project;
- a nearby prompt belongs to that client;
- one client profile looks similar to another;
- a historical translation used the same language pair.

Source-only mode with only a source file and language pair uses `generic`.

## 2. One Profile, One Language Pair, One Version

Resolve exactly one active profile for a language pair unless the user
explicitly supplies a documented composite hierarchy.

Validate:

- client/profile ID;
- source and target locale;
- profile version and approval status;
- the content classes to which each rule applies;
- whether the asset is a format profile, terminology asset, or mixed legacy
  prompt.

Do not merge rules from two customers. Do not silently choose the newest
filename or infer that a similarly named profile supersedes another.

## 3. Separate Rule Classes

Classify each rule before compiling it:

1. **Formatting rule** — punctuation, Unicode form, spaces, brackets, ranges,
   dates, number grouping, units, dash/slash behavior, references or layout.
2. **Terminology rule** — source-to-target wording such as a preferred term.
   Route this to approved terminology handling; do not disguise it as format.
3. **Semantic/domain rule** — scientific, legal, clinical or technical
   fidelity. Keep the generic domain framework unless the explicit client rule
   is stricter and compatible with source meaning.
4. **Protected-content rule** — identifiers, code, literals, tags or notation
   that must be preserved.
5. **Workflow metadata** — profile name, file path, merge instructions,
   comments about platform binding or post-processing. Never copy these into
   the production prompt.
6. **Example** — neutralize or remove any real project ID, drug, attachment
   code, section number or target term that is not independently authorized.

A legacy client prompt may contain all six classes. Reuse only the applicable,
authorized rule content.

## 4. Rule-Key Compilation

Normalize formatting rules to stable keys before merging. Useful keys include:

- `spacing.cjk_latin_digit`
- `spacing.number_unit`
- `operator.lt_gt_eq`
- `range.connector`
- `range.percent_repetition`
- `punctuation.dash`
- `punctuation.slash_spacing`
- `punctuation.colon`
- `bracket.parentheses`
- `bracket.square_external_spacing`
- `number.thousands`
- `date.display`
- `time_unit.policy`
- `unit.micro_sign`
- `unit.product_symbol`
- `reference.section_style`
- `address.nonlocal`
- `abbreviation.plural_suffix`
- `count.classifier`
- `count.percentage_pattern`

For each key, retain:

- the resolved value;
- scope such as `ordinary_prose`, `table_display`, `formula`, or `code`;
- exclusions;
- authority/provenance;
- profile version.

If two rules set different values for the same key, resolve the conflict before
prompt generation. Do not put both rules into the translation prompt and ask
the model to choose.

## 5. Precedence and Scope

Use this order:

1. source meaning, values, logic, and protected source content;
2. explicit current-project instructions;
3. the selected approved client format profile;
4. generic target-locale defaults;
5. ordinary style preference.

Client formatting normally applies to translatable visible text. It never
reshapes genuinely source-fixed/protected content, including:

- code, variables, dataset names or quoted coded values;
- formulas, chemical notation or source-fixed scientific notation;
- URLs, file paths, identifiers or tags;
- numeric value, precision, comparison strictness or date granularity.

If an approved client rule governs a visible display notation, classify that
notation as client-governed display content instead of protected content.
Do not keep both classifications or use the client rule as permission to
modify protected code, identifiers, tags, formulas, or literal values.

## 6. Production-Prompt Integration

Compile the applicable rules into the formatting/data/protected-content
subsection of the single `### Style prompt` block. The Verified Project
Constraints subsection remains source-focused. The production prompt should
contain the resolved instruction, not:

- a profile placeholder;
- a path to another file;
- instructions to load or merge a profile;
- statements that no profile is available;
- competing generic and client values;
- another customer's name, examples or project tokens.

Include only rules relevant to content features found in the current source.
For example, a unit-product rule need not be emitted when the document has no
unit products, and a section-reference rule need not be emitted when no such
references exist.

Naming the current client in the Role is optional and requires explicit
authority. Naming it does not replace compiling the actual applicable rules.

## 7. Validation

Before delivery, check:

- the active profile was explicitly selected;
- its locale pair matches the request;
- exactly one value exists for every emitted rule key;
- generic defaults that conflict with the active profile were removed;
- terminology mappings were routed separately;
- real project examples were removed unless verified in the current source;
- no foreign-client fingerprint remains;
- every rule is scoped away from protected syntax unless explicitly approved;
- the production artifact contains no profile-selection or merge metadata.

For a future portal, provide an optional explicit client/style-profile selector
or trusted backend project-profile field. Keep its default as `Generic / no
client profile`. A portal that accepts only source file and language pair
cannot safely activate customer-specific formatting.
