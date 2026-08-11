# Formatting Standards by Target Language

此文件包含各目标语言的**行业标准排版规范**。在生成翻译提示词时，根据目标语言自动补充相应规则。

---

## Chinese (Simplified) - zh-CN

### Scope and Precedence

- Use standard Mainland Simplified Chinese.
- These are safe locale defaults, not a customer style guide. An explicitly
  selected and approved client format profile may override them.
- Apply locale formatting only to ordinary translatable prose. Do not reshape
  code, formulas, chemical notation, dataset fields, literal values,
  identifiers, URLs, tags, compact statistical notation, or other
  source-fixed content.
- Meaning, numeric value, logical strictness, date granularity, and protected
  source identity take precedence over visual normalization.

### Punctuation and Brackets

- Use full-width Chinese punctuation in ordinary Chinese prose: `，` `。` `；`
  `：` `！` `？`.
- Keep half-width punctuation when it is functional inside ratios, time,
  scientific notation, code, identifiers, URLs, or protected literals, such
  as `1:1` and `12:00`.
- Use Chinese quotation marks and the Chinese ellipsis in ordinary prose when
  the source format permits localization.
- Full-width parentheses `（）` are a safe default for ordinary Chinese prose.
  Preserve half-width parentheses and square brackets when they belong to
  formulas, chemical/PK notation, code, citations, tags, identifiers, or
  source-fixed layout.
- Do not impose a universal nested-bracket pattern or bracket-external spacing
  rule. Apply an exact pattern only from the active client profile.

### Spacing

- In ordinary Chinese prose, avoid arbitrary spaces between Chinese text and
  adjacent Latin letters or digits. Preserve a deliberate source or approved
  client convention when it carries structure.
- A number and an English measurement-unit token normally use one half-width
  space in ordinary prose, such as `10 mg` and `5 mL`, unless the selected
  client profile specifies otherwise.
- Do not insert, remove, or normalize spaces inside source-fixed notation,
  formulas, variables, tags, values, or compact data fields.
- Do not use fixed tag-spacing substitutions as a generic language rule.
  Preserve tag identity and semantic attachment; apply exact surrounding
  spaces only when an approved profile requires them.

### Numbers, Units, and Scientific Notation

- Preserve every number, decimal, significant digit, sign, unit, range,
  comparator, and threshold in meaning and precision.
- Preserve source thousands grouping in data, IDs, dates, batch/lot numbers,
  references, tables, and ambiguous standalone values. Do not add separators
  merely because a number has four or more digits.
- Use a period as the decimal marker unless an approved target convention
  explicitly requires another form.
- Do not globally normalize `°C`/`℃`, `μ`/`µ`, `ug`/`µg`, `l`/`L`, unit-product
  symbols, range connectors, or full-/half-width comparators. These exact
  Unicode and notation choices belong to a scientific or client style
  authority.
- Do not create or remove subscript/superscript formatting unless the source
  markup and output format safely support it and an approved convention
  requires it.
- In ordinary visible text, avoid beginning a sentence with a bare comparator
  when a natural Chinese construction can preserve the same strictness. Do not
  change `>` to `≥`, `<` to `≤`, or otherwise change boundary inclusion.

### Date and Time

- Preserve the same calendar date, time point, timezone if present, and source
  granularity.
- In ordinary prose without an approved fixed format, use a clear,
  unambiguous Chinese date expression. Do not force one numeric date pattern
  across tables, code, citations, or source-fixed fields.
- Preserve the source distinction between a complete date, month-year, year,
  study day, cycle, visit, and relative time window.
- Translate or retain abbreviated time units according to document function
  and the active client profile; do not impose one policy on prose, tables,
  formulas, and derivation code alike.

### Pharma/Medical Locale Guidance

- Render clinical trial phase designations consistently with the source and
  any approved official name; do not alter source-fixed study identifiers.
- Choose Chinese classifiers and participant/patient word order from context.
  Do not enforce one count-percentage pattern or one disease-description order
  across clients.
- Treat an acronym's plural suffix conservatively. It may be removed in
  ordinary Chinese prose when it is purely grammatical, but never modify a
  machine identifier, coded value, official name, or protected literal.
- Preserve Latin or scientific expressions according to source emphasis and
  the applicable publication/client style; do not globally strip formatting.

---

## Chinese (Traditional) - zh-TW

### Punctuation (標點符號)
- Same as zh-CN, but prefer traditional quotation marks: 「」『』
- **Proper names**: Follow Taiwan Ministry of Education romanization guidelines

### Terminology Preferences
- **Software terms**: Prefer Taiwan-specific terms (e.g., "軟體" not "软件"，"資料夾" not "文件夹")

---

## Japanese - ja-JP

### Punctuation (句読点)
- **Use full-width punctuation**: "、" (読点), "。" (句点)
- **Quotation marks**: Use 「」 for quotes, 『』 for nested quotes
- **Katakana long vowel**: Use "ー" (長音符号) correctly (e.g., "コンピューター", not "コンピュータ")

### Spacing
- **No spaces between Japanese and alphanumerics**: "設定を開く" (not "設定 を 開く")
- **Exception**: Optional space before/after English words for readability (style-dependent)

### Honorifics (敬語)
- **B2C content**: Use polite form (です・ます体)
- **Technical docs**: Use plain form (だ・である体) unless otherwise specified
- **UI strings**: Use command form (e.g., "保存する", "キャンセル")

### Katakana Usage
- **Foreign words**: Use katakana (e.g., "ファイル", "ダウンロード")
- **Established loanwords**: Follow JIS conventions (e.g., "コンピューター" not "コンピュータ")

---

## Korean - ko-KR

### Punctuation (구두점)
- **Period**: Use "。" or "." (both acceptable, but "." is more common in modern text)
- **Quotation marks**: Use " " or ' ' (Western-style preferred in technical docs)

### Spacing (띄어쓰기)
- **Follow Korean orthography rules**: Strict spacing between words (e.g., "파일을 저장합니다", not "파일을저장합니다")
- **Common errors**: Watch for compound nouns (e.g., "데이터베이스" not "데이터 베이스")

### Honorifics (존댓말)
- **B2C content**: Use formal polite form (합니다체)
- **UI strings**: Use declarative or imperative (e.g., "저장", "취소")

---

## English (US) - en-US

### Punctuation
- **Comma**: Use Oxford comma in lists (e.g., "a, b, and c")
- **Quotation marks**: Use double quotes " " (single quotes ' ' for nested)
- **Periods in abbreviations**: Generally no periods for acronyms (e.g., "USA", "NASA")

### Spelling
- **Use American spelling**: "color" (not "colour"), "center" (not "centre")

### Date & Time
- **Ordinary-prose date default**: Use the en-US month-day-year convention;
  spell out the month when needed for clarity and unambiguous interpretation.
- **Patent/legal/regulatory boundary**: Preserve the same calendar date and
  use an unambiguous en-US expression when reformatting is appropriate (for
  example, "March 15, 2024"). Do not force a numeric order unless an explicit
  client or filing requirement controls it.
- **Time format**: 12-hour with AM/PM (e.g., "2:30 PM")

---

## English (UK) - en-GB

### Punctuation
- **Oxford comma**: Generally avoided in British English
- **Quotation marks**: Use single quotes ' ' (double quotes " " for nested)

### Spelling
- **Use British spelling**: "colour", "centre", "organisation"

### Date & Time
- **Ordinary-prose date default**: Use the en-GB day-month-year convention;
  spell out the month when needed for clarity and unambiguous interpretation.
- **Patent/legal/regulatory boundary**: Preserve the same calendar date and do
  not impose a fixed numeric order without an explicit controlling convention.
- **Time format**: 24-hour preferred in formal contexts

---

## German - de-DE

### Capitalization (Großschreibung)
- **Capitalize all nouns**: "das Haus", "die Datenbank", "der Computer"

### Punctuation
- **Quotation marks**: Use „" (German-style), not " " (English-style)
- **Comma rules**: Strict comma placement before subordinate clauses

### Numbers
- **Decimal separator**: Use comma (e.g., "3,14")
- **Thousands separator**: Use period (e.g., "1.234.567")

### Date & Time
- **Ordinary-prose date default**: Use the German day-month-year convention;
  spell out the month when needed for clarity and unambiguous interpretation.
- **Patent/legal/regulatory boundary**: Preserve the same calendar date and do
  not impose a fixed numeric order without an explicit controlling convention.
- **Time format**: 24-hour (e.g., "14:30 Uhr")

---

## French - fr-FR

### Spacing (Espacement)
- **Before high punctuation marks**: Insert non-breaking space before ":", ";", "!", "?"
  - Example: "Bonjour !" (not "Bonjour!")
- **Quotation marks**: Use « » with spaces (e.g., "« Bonjour »")

### Numbers
- **Decimal separator**: Use comma (e.g., "3,14")
- **Thousands separator**: Use space (e.g., "1 234 567")

### Capitalization
- **Titles**: Only capitalize first word (e.g., "Les misérables", not "Les Misérables")
- **Months/days**: Lowercase (e.g., "lundi 15 mars")

---

## Spanish - es-ES

### Punctuation
- **Inverted marks**: Use ¡ and ¿ at the beginning of exclamations/questions
  - Example: "¡Hola! ¿Cómo estás?"
- **Quotation marks**: Use « » or " " (style-dependent)

### Numbers
- **Decimal separator**: Use comma (e.g., "3,14")
- **Thousands separator**: Use period (e.g., "1.234.567")

### Date & Time
- **Ordinary-prose date default**: Use the Spanish day-month-year convention;
  prefer a written month in formal text when needed to avoid ambiguity.
- **Patent/legal/regulatory boundary**: Preserve the same calendar date and do
  not impose a fixed numeric order without an explicit controlling convention.
- **Months/days**: Lowercase (e.g., "lunes, 15 de marzo")

---

## Portuguese (Brazil) - pt-BR

### General Principles
- Use **standard Brazilian Portuguese** (not European Portuguese)
- Prefer `tela`, `configurações`, `online`, `botão`, `falha` (avoid EU-PT: `ecrã`, `ficar ligado`)
- Default tone: Conversational-neutral with slight sci-fi/tech flavor when appropriate

---

### Punctuation

#### Basic Rules
- **Quotation marks**: Use `" "` or `« »` (both acceptable)
- **Travessão (em dash)**: Use `—` for dialogue
- **Ellipsis**: Keep `...` for hesitation/suspense (avoid multiple exclamation marks)

#### Spacing
- **No space before punctuation**: Standard for Portuguese

---

### Numbers & Units

#### Number Format
- **Decimal separator**: Use comma: `3,14`
- **Thousands separator**: Use period: `1.234.567`

#### Unit Spacing
- **Number + unit**: Insert space: `10 mg`, `5 m`
- **Symbols**: Preserve `%`, `×`, etc.
  * Example: `+10% de dano`

---

### Date & Time

- **Ordinary-prose date default**: Use the Brazilian Portuguese
  day-month-year convention; prefer a written month in formal text when needed
  to avoid ambiguity.
- **Patent/legal/regulatory boundary**: Preserve the same calendar date and do
  not impose a fixed numeric order without an explicit controlling convention.
- **Time format**: 24-hour common (e.g., `14h30`)

---

### Register & Tone (Game-specific)

#### Público-alvo & Legibilidade
1. Target audience: **Typical ARPG players in Brazil**
   * Prefer medium-length sentences
   * Avoid heavy nesting, excessive subordinate clauses
   * You may **split** long English sentences into 2 shorter Portuguese sentences
2. Default tone: **Conversational-neutral**, with slight sci-fi/tech flavor
   * Avoid slang that is too local, time-bound, or internet-specific
   * Choose timeless register

#### Diálogos vs. Texto de Sistema

**System/UI/Tutorial**:
- Avoid explicit pronouns; use imperative or neutral constructions:
  * `Abra o inventário.`
  * `Selecione um Eco.`
- If pronoun needed, default to **`você`** (3rd person singular), but don't overuse

**Narrative and Character Dialogue**:
- Should read like **spoken Brazilian Portuguese**
- Natural word order, contractions: `alguma coisa`, `meio estranho`, `tá bom` (casual)
- Light colloquial forms (`tá`, `pra`) for casual/young characters
- More neutral forms (`está`, `para`) in system text and formal characters

**Profanity**:
- If English is mildly rude, soften slightly but keep emotional force
- Avoid explicit swear words that would raise age rating

---

### Character Voice & Personality (Game-specific)

#### Self-reference (Childlike characters)
- Some characters refer to themselves by name (cuteness/modesty)
- In pt-BR, keep occasional self-reference:
  * `A Encore vai dar o melhor de si hoje!` (instead of only `Eu vou dar o meu melhor hoje!`)
- Use sparingly and consistently

#### Addressing Others
- Directly calling people by name is part of charm; keep it
- Use simple, warm phrases for childlike characters

#### Ancient/Primordial Beings
- Slightly more formal and elevated
- More structured sentences, less slang, hint of solemnity
- Do not overdo pseudo-archaic Portuguese

#### Children & Very Young Characters
- Add **minor simplifications** to show age:
  * `Esse barulho é muito esquisito...` (instead of formal phrasing)
- Must never look like translation mistakes; use with care

---

### Terminology Preferences (Brazil-specific)

- **Software terms**: Use modern Brazilian terms
  * `software` (not `programa`)
  * `download` (not `baixar` in technical context)
- **Gaming terms**: 
  * `inventário` (not `inventário` with EU-PT spelling)
  * `configurações` (not `definições`)

---

### Quality Indicators
- Naturalness: Would it fit in a modern Brazilian-localized ARPG?
- Not MT-sounding: Avoid stiff, literal, or raw MT feel
- Character voice: Reflect personality when inferable

---

## Russian - ru-RU

### General Principles
- Use **modern Russian** suitable for game/tech/business contexts
- Maintain proper formal vs. informal address (ты/вы)
- Always use **ё** where required (do NOT replace with `е`)

---

### Punctuation (Пунктуация)

#### Quotation Marks
- **Primary**: Use guillemets `« »`
- **Nested quotes**: Outer guillemets + inner straight quotes: `«"..."»`

#### Dashes & Hyphens
- **Hyphen** `-`: For compounds: `эхо-поезд`
- **En dash** `–` (U+2013): For ranges/date ranges: `10–50`
- **Em dash** `—` (U+2014): As punctuation dash (with spaces in text)

#### Ellipsis & Punctuation Clusters
- **Use single-character ellipsis** `…` (U+2026) — do NOT use three dots `...`
- **Russian-valid combos**: `?..` (question + two dots), `!..` (exclamation + two dots)
  * Output exactly: `?` or `!` + TWO DOTS (not `?…`, `…?`, `!…`, or `…!`)
- **Do not copy English punctuation patterns**

#### Punctuation with Quotes
- **Period**: After closing guillemets: `...».`
- **Question/exclamation**: Before closing guillemets: `...?»`, `...!»`

---

### Spacing (Пробелы)

#### General Rules
- **No space before punctuation**: `Привет, мир!` (not `Привет , мир !`)
- **Spaces around em dash**: Use spaces in narrative text

#### Numbers & Units
- **Percent**: No space: `5%`
- **Seconds**: Use `сек.` with **non-breaking space** (U+00A0): `5 сек.`
- **Level**: Number first with NBSP: `20 ур.`
- **Star quality**: `4 зв.` / `5 зв.` (NBSP recommended)

---

### Address Forms (Обращение)

#### System Text (Formal)
- **UI labels**: No personal pronouns
- **System notifications/results**: Explicitly use **«Вы»** (formal plural):
  * `Вы получили помидор.`
  * `Вы разблокировали функцию.`
- **Tutorial/instructions**: Formal imperative (pronoun optional):
  * `Откройте инвентарь.`
  * `Следуйте маркеру задания.`
  * Never use «ты»

#### Dialogue (Context-dependent)
- **«ты»** or **«вы»** depending on relationship
- **Superior→subordinate**: Subordinate uses «вы», superior may use «ты»
- **Most situations**: Characters address each other by name + «ты»

#### Honorific Replacements
- Replace Mr., Ms., Miss, ma'am with **«господин / госпожа»** when needed
- Between characters, prefer «ты/вы» + name; don't force господин/госпожа unless context requires

---

### Numbers & Symbols

#### Variable Grammar Safety
- **Problem**: Variable counts make correct Russian agreement unsafe
- **Solution**: Use **×** (U+00D7, not letter `x`) to avoid incorrect forms:
  * `Яблоко ×{count}` / `{item} ×{count}`
  * Keep noun in stable base form when using ×

---

### Casing & Capitalization

#### Generic Gameplay Elements
- **Lowercase** when not proper names: `резонатор`, `форте`, `диссон`, `мощный навык`
- **Exception**: Special naming rules (see below)

#### Titles, Groups, Proper Nouns
- **Орден Глубин**: Always capitalized; when shortened to `Орден` referring to it, keep capitalized
- **Тренодиан**: Always capitalized
- **Гева**, **Эфор**: Capitalized

#### "Странник" Address Form
- **Singular address**: `Странник` capitalized
- **Plural address**: Lowercase (`дорогие странники`), unless sentence-initial

#### Generic Location Terms vs. Proper Names
- Generic terms (`храм`, `перевал`, `пик`): Lowercase unless part of proper noun
- If followed by proper name in genitive: generic lowercase + proper-name capitalized:
  * `равнина Асфодел`
  * `перевал Ржавой Крови`
- Palace names are proper nouns: `Дворец Эфора`

---

### Game-Specific Rules (Example: Wuthering Waves)

#### "Эхо" (Client Rule - MUST FOLLOW)
- Always written as **«Эхо»** with initial capital
- **Grammatically invariable** (neuter)
- In compound words (e.g., `эхо-поезд`): Does NOT need capitalization unless at sentence start
- **Never decline**: No `Эха/Эху/Эхом/Эхе`
  * If grammar requires a case, rephrase to keep «Эхо» unchanged

#### Attributes / Damage Types
- When possible, place attribute name first and capitalize:
  * `Спектро урон`
  * `Аэро призма`
- Prefer pattern **«урон от ...»**: `урон от обычного навыка`

#### Skills & Statuses (Quotes only in running text)
- When a skill/status name appears **inside a sentence**, use guillemets and capitalize:
  * `мощная атака «Рифф рапсодии»`
  * `эффект «Шок»`
- If the entire string is just the name/label (UI list/title), do NOT force quotes

---

### Domain-Specific Notes

#### Tech/Cyberpunk Flavor (适用于科幻/赛博朋克游戏)
- Use modern tech terms: `интерфейс`, `протокол`, `сбой`, `сканирование`, `пакет данных`, `перегрузка`

---

### Quality Checklist
Before finalizing Russian text:
- [ ] ё used where required (not е)
- [ ] Guillemets « » used for quotes
- [ ] Ellipsis is single character …
- [ ] ?.. and !.. (not ?… or !…)
- [ ] Formal «Вы» in system text, appropriate ты/вы in dialogue
- [ ] × used for variable counts
- [ ] Proper capitalization for names and titles

---

## Arabic - ar-SA

### Text Direction
- **RTL (Right-to-Left)**: Ensure proper bidirectional text handling
- **LTR exceptions**: English names, numbers, URLs remain LTR within RTL text

### Punctuation
- **Arabic punctuation**: Use "،" (Arabic comma), "؛" (Arabic semicolon), "؟" (Arabic question mark)
- **Period**: Use "." (same as English)

### Numbers
- **Use Western Arabic numerals**: 0-9 (not Eastern Arabic-Indic ٠-٩) in technical content
- **Exception**: Eastern Arabic-Indic may be used in literary/cultural content

### Spacing
- **No spaces around punctuation**: Same as other RTL languages

---

## General Rules Across All Languages

### Tag Protection (Universal)
- **Preserve all markup tags verbatim**: `<b>`, `</b>`, `{variable}`, `[link]`, etc.
- **Do NOT translate**: Tag names, attribute names, and variable names.
- Preserve tag pairing, nesting, and the semantic content enclosed by each
  tag. If target-language syntax requires movement, move the complete tagged
  span without splitting or orphaning the tag.
- Distinguish source-fixed markup entities from visible prose encoded as an
  entity. Preserve the encoding when it is operational; when the platform
  exposes a visible comparator or symbol for translation, preserve the same
  meaning and strictness rather than blindly leaving an entity as prose.
- Compact appearance, uppercase, a `#` prefix, or `=` alone does not prove
  that a string is code. Translate human-readable table and flow-chart labels;
  preserve verified identifiers, variables, literals, and executable syntax.

### URL & Email Handling
- **Do NOT translate**: URLs, email addresses, file paths (keep as-is)

### Measurement Units
- **Keep source units** unless conversion is explicitly requested
- In ordinary prose, apply the target locale's standard spacing between a
  number and unit (e.g., "10 mg", "25 °C").
- Do not insert, remove, or normalize spacing inside formulas, chemical
  notation, tables, protected strings, machine-readable tokens, or other
  source-fixed notation. Domain and approved client rules override the
  ordinary-prose default.

---

## Usage Instructions

When generating a translation system prompt:
1. Identify the target language from user input
2. Load the corresponding section from this file
3. Insert relevant rules into the "Formatting & Normalization" section of the prompt
4. Customize rules based on project-specific requirements (e.g., if client prefers non-standard conventions)
