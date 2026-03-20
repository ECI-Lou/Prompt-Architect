# Formatting Standards by Target Language

此文件包含各目标语言的**行业标准排版规范**。在生成翻译提示词时，根据目标语言自动补充相应规则。

---

## Chinese (Simplified) - zh-CN

### General Principles
- Use **standard Mainland Chinese (Simplified)** conventions
- Prioritize clarity and regulatory compliance for pharma/medical/legal texts
- Follow industry-specific standards when applicable (e.g., NMPA for pharma)

---

### Punctuation (标点符号)

#### Basic Rules
- **Use full-width punctuation in main text**: "，" "。" "！" "？" "；"
- **Colon handling**:
  * Normal prose/labels: Use full-width "："
  * Compact token-like patterns (no surrounding spaces): Keep half-width ":"
    - Examples: `1:1` (ratio), `12:00` (time), `pH:7.4`, `Na+:K+` (ions)
- **Quotation marks**: Use Chinese-style "" or 「」; avoid English-style " "
- **Ellipsis**: Use "……" (6 dots), not "..." (3 dots)
- **Enumeration**: Use "、" for item separation (e.g., "苹果、香蕉、橙子")

#### Parentheses & Brackets (Pharma/Medical specific)
- **General text**: Use **full-width** "（）" with **no spaces** around them
- **Nested parentheses**: Outer "（）", inner "[  ]" (half-width square brackets)
- **Chemical expressions**: Keep half-width "()" where part of chemical/structural notation
- **J&J special bracket spacing rule** (OUTSIDE spacing):
  * Do NOT add spaces inside [ ]
  * If [ ] is adjacent to Arabic digits or English letters, insert **one half-width space OUTSIDE**:
    - `表1[附件ALR88KBS]` → `表1 [附件ALR88KBS]`
    - `Appendix[ALR88KBS]` → `Appendix [ALR88KBS]`
    - `]1` → `] 1`
  * Keep content inside brackets unchanged

---

### Spacing (空格规则 - "盘古之白")

#### General Spacing Rules
- **Rule 2 (GENERAL)**: Remove spaces between Chinese↔English and Chinese↔Arabic digits by default
- **Rule 4 (EXCEPTION - higher priority)**: Insert **one half-width space** between number and English unit:
  * Examples: `100 mg`, `5 mL`, `2.0 mmol/L`
  * Temperature: Convert `°C/°F` → `℃/℉` and **do not** add space: `37℃`, `98℉`
  * Liter: Convert lowercase `l` to uppercase `L`: `ml`→`mL`, `l`→`L`
  * Micro: Convert `u` or Greek `μ` to half-width `µ`: `ug`→`µg`

#### Special Tag-Spacing Cleanup (Medical/Pharma)
Remove spaces in these patterns:
- `章节 <tag>` → `章节<tag>`
- `附录 <tag>` → `附录<tag>`
- `附件 <tag>` → `附件<tag>`
- `图 <tag>` → `图<tag>`
- `表 <tag>` → `表<tag>`
- `<tag> 和 <tag>` → `<tag>和<tag>`

---

### Numbers & Units

#### Number Format
- **Thousands separator**: Use comma: `1,234,567`
  * Consistency rule: If some 4+ digit numbers use separators and others don't, normalize to **with commas**
  * Comma must remain half-width (never full-width "，")
- **Decimal point**: Use period: `3.14`

#### Unit Spacing (Critical for Pharma)
- **Number + English unit**: Insert **one half-width space**: `10 mg`, `5 mL`
- **Temperature symbols**: Convert `°C/°F` → `℃/℉` with **no space**: `37℃`
- **Percentage**: No space: `50%` (not `50 %`)
  * Percent range rule: `1%-99%` (put % on both ends)

#### Subscript/Superscript (NO underscore - Pharma)
Must use **real subscript/superscript formatting** (not `_`):
- **PK parameters**:
  * `AUC0-24h` → `AUC` with `0-24h` as subscript
  * `AUClast` → `AUC` with `last` as subscript
  * `Ctrough` → `C` with `trough` as subscript
  * `Cmax` → `C` with `max` as subscript
  * `tmax` → `t` with `max` as subscript
  * `t1/2` → `t` with `1/2` as subscript
- **Chemical formulas**: `H2O` → `H₂O`, `CO2` → `CO₂`
- **Ions**: `Ca2+` → `Ca²⁺`, `SO42-` → `SO₄²⁻`

---

### Math & Relational Symbols (Pharma/Medical)

**Use specified full-width forms; no spaces around them**:
- `≥`、`≤`、`＞`、`＜`、`±`、`－`

**Sentence start constraint**: Do not begin a normal narrative sentence with an operator; rewrite:
- Bad: `≥10 mg 的剂量`
- Good: `剂量≥10 mg`

**Ranges**: Use hyphen-minus `-` only (not `～`):
- Example: `10-20 mg`

---

### Date & Time

- **Date format**: `YYYY年M月D日` without leading zeros (e.g., `2018年6月8日`)
  * Technical docs may use: `YYYY-MM-DD`
- **Time format**: 24-hour (e.g., `14:30`) or with 上午/下午 for general audience
- **Time units in body text**: Translate into Chinese words if not in parentheses:
  * `涂旋5分钟` (not `涂旋5 min`)
  * If inside parentheses, follow source

---

### Domain-Specific Rules (Pharma/Medical)

#### Latin Phrases
Remove italic formatting for Latin terms (output in plain text):
- `in vitro`, `in vivo`, `ex vivo`, `in situ`, `in utero`, `in silico`
- `a priori`, `a posteriori`, `post hoc`, `per se`, `de novo`, `ad hoc`

#### Clinical Trial Phases
Use Roman numerals: `I期`、`II期`、`IIb期` (not Arabic "1期")

#### Count-Unit Normalization
Use correct Chinese measure words:
- Subjects: `例`
- Adverse events: `起`
- Studies: `项`
- Study sites/labs: `家`
- Samples: `份`
- Animals: `只`

#### Subject Count + Percentage Format
Fixed pattern: `x例(xx%)受试者` (not `x例受试者(xx%)`)

#### Subject Descriptor Order
Use: `疾病程度 + 疾病名称 + 年龄段 + 受试者/患者`
- Example: `中重度活动性克罗恩病成人患者`

#### Acronym Plural Normalization
Remove plural "s" from abbreviations:
- `AEs` → `AE`
- `SAEs` → `SAE`
- Express plurality in Chinese wording: `多起AE`

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
- **Date format**: MM/DD/YYYY (e.g., "03/15/2024")
- **Time format**: 12-hour with AM/PM (e.g., "2:30 PM")

---

## English (UK) - en-GB

### Punctuation
- **Oxford comma**: Generally avoided in British English
- **Quotation marks**: Use single quotes ' ' (double quotes " " for nested)

### Spelling
- **Use British spelling**: "colour", "centre", "organisation"

### Date & Time
- **Date format**: DD/MM/YYYY (e.g., "15/03/2024")
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
- **Date format**: DD.MM.YYYY (e.g., "15.03.2024")
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
- **Date format**: DD/MM/YYYY (e.g., "15/03/2024")
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

- **Date format**: DD/MM/YYYY (e.g., `15/03/2024`)
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
- **Do NOT translate**: Tag names, attribute names, variable names, HTML entities
- **Maintain positions**: Keep tags in the same relative position to surrounding text

### URL & Email Handling
- **Do NOT translate**: URLs, email addresses, file paths (keep as-is)

### Measurement Units
- **Keep source units** unless conversion is explicitly requested
- **Always insert space** between number and unit (e.g., "10 mg", "25 °C")

---

## Usage Instructions

When generating a translation system prompt:
1. Identify the target language from user input
2. Load the corresponding section from this file
3. Insert relevant rules into the "Formatting & Normalization" section of the prompt
4. Customize rules based on project-specific requirements (e.g., if client prefers non-standard conventions)
