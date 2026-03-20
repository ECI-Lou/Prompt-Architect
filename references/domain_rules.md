# Domain-Specific Translation Rules

此文件包含各垂直领域的**专业翻译规则**。在生成翻译提示词时，根据文档类型自动补充相应规则。

---

## Pharma (医药/制药) {#pharma}

### Core Principles
- **Evidence-based translation**: Every claim must be traceable to source
- **Zero hallucination**: Do NOT add, omit, or alter medical information
- **Terminology consistency**: Use standardized medical terminology (ICD-10, MedDRA, SNOMED CT)

### Regulatory Context
- **Target authority**: Specify regulatory body (FDA, EMA, NMPA, PMDA)
- **Document type sensitivity**:
  - Clinical protocols: Maintain evidence levels (Level I-III)
  - Package inserts: Follow regulatory template structure
  - Informed consent: Prioritize patient comprehension over literal translation

### Specific Rules

#### 1. Medical Terminology
- **Drug names**: 
  - Generic names: Translate using WHO INN (International Nonproprietary Names)
  - Brand names: Keep as-is unless local registration uses different name
- **Adverse events**: Use MedDRA Preferred Terms (PTs) in target language
- **Anatomy**: Use standardized anatomical terminology (e.g., Terminologia Anatomica)

#### 2. Dosage & Units
- **Maintain precision**: "10 mg" must remain "10 mg" (never round to "approximately 10 mg")
- **Unit conversions**: Only if explicitly requested by client (rare in pharma)
- **Frequency abbreviations**: 
  - Latin: Keep as-is (e.g., "q.i.d.", "p.r.n.") or translate per local convention
  - Example (zh-CN): "q.i.d." → "每日四次 (q.i.d.)"

#### 3. Safety Information
- **Black box warnings**: Translate verbatim; do NOT soften language
- **Contraindications**: Maintain strict logical structure (e.g., "if A and B, then C")
- **Precautions**: Do NOT add qualifiers like "usually" or "generally" if not in source

#### 4. Statistical Data
- **P-values, confidence intervals**: Keep numerical values exact (do NOT round)
- **Sample sizes**: "N=123" must remain "N=123"
- **Tables & figures**: Translate labels but verify numerical accuracy

#### 5. References & Citations
- **Keep citation format**: (Author, Year) or [1] style should match source
- **Journal names**: Use official abbreviated form (per Index Medicus)

---

## Patent (专利) {#patent}

### Core Principles
- **1:1 correspondence**: Every source term must have exactly one target term (no synonyms)
- **Legal scope preservation**: Do NOT expand or narrow the scope of claims
- **Formal register**: Maintain patent-specific formal language

### Document Structure
- **Claims (权利要求书)**: Most critical section
  - Independent claims vs. dependent claims structure must be clear
  - "comprising" vs. "consisting of" distinction is legally significant
- **Description (说明书)**: Must support claims
- **Abstract**: Concise summary (typically <150 words)

### Specific Rules

#### 1. Claim Language
- **"comprising"**: Inclusive (includes listed elements + others)
  - zh-CN: "包括" or "包含"
  - ja-JP: "含む" or "備える"
- **"consisting of"**: Exclusive (only listed elements)
  - zh-CN: "由...组成"
  - ja-JP: "からなる"
- **"consisting essentially of"**: Limited flexibility
  - zh-CN: "基本上由...组成"

#### 2. Technical Terms
- **Locked terms**:
  - "SEQ ID NO: X" → Do NOT translate
  - Figure references: "Figure 1", "Fig. 2A" → Keep as-is (or follow target office convention)
  - Chemical formulas: H₂O, C₆H₁₂O₆ → Never translate
- **Neologisms**: If inventor created a term, keep consistency throughout document

#### 3. Cross-References
- **Internal references**: "as described in paragraph [0023]"
  - Ensure paragraph numbers are updated if formatting changes
  - zh-CN: "如第[0023]段所述"

#### 4. Measurements & Ranges
- **Numerical ranges**: "1-10" or "1 to 10"
  - Maintain exact phrasing (patent scope depends on this)
  - Example: "at least 5" ≠ "5 or more" (legally different in some jurisdictions)

#### 5. Drawing Descriptions
- **Element numbering**: (10), (20), (30) → Keep as-is
- **Consistency**: If "10" is "housing" in paragraph [0015], it must remain "housing" throughout

---

## Game (游戏) {#game}

### Core Principles
- **Immersion**: Translation should feel like original content, not translated
- **Character limit awareness**: UI strings often have display constraints
- **Lore consistency**: Maintain world-building and naming conventions

### Game Genres
- **RPG**: Focus on narrative immersion, character voice
- **FPS/Action**: Punchy, concise UI text
- **Puzzle/Casual**: Friendly, accessible tone
- **Strategy**: Clear, tactical language

### Specific Rules

#### 1. Variables & Tokens
- **Protect variables**: `{player_name}`, `[item_count]`, `<color>`, etc. → Do NOT translate
- **Positioning**: Ensure variables fit grammatically in target language
  - Bad (zh-CN): "你好{player_name}" (no space)
  - Good (zh-CN): "你好 {player_name}"

#### 2. Character Limits
- **UI strings**: Ask for character limit if not specified (common: 10-30 chars)
- **Exceeding limit**: Prioritize conciseness over literal translation
  - Example: "Inventory Management System" (28 chars) → "背包" (2 chars, zh-CN)

#### 3. Lore & World-Building
- **Proper names**: Keep character/location names unless localization guide specifies
  - Exception: Games with official Chinese/Japanese names (e.g., "Zelda" → "ゼルダ" in ja-JP)
- **Fictional terms**: Maintain consistency
  - Example: If "Mana" is used in source, don't mix "法力", "魔力", "魔法值" in target (pick one)

#### 4. Tone & Voice
- **Character-specific tone**:
  - Young protagonist: Energetic, informal
  - Wise mentor: Measured, formal
  - Villain: Dramatic, menacing
- **Avoid over-localization**: Don't add cultural references not in source (breaks immersion)

#### 5. Technical Strings
- **Error messages**: Clear and helpful (not immersive)
  - "Connection lost" → Direct translation, no flowery language
- **Tutorial text**: Instructional tone (can break immersion for clarity)

---

## Legal (法律) {#legal}

### Core Principles
- **Binding language**: Every word has potential legal consequence
- **Ambiguity avoidance**: Resolve only if source is clear; otherwise, flag for review
- **Jurisdiction awareness**: Legal terms vary by jurisdiction

### Document Types
- **Contracts**: Bilateral obligations, conditions, warranties
- **Terms of Service**: Unilateral terms, disclaimers
- **Court documents**: Precedent-sensitive, formal register
- **Regulations**: Statutory interpretation rules apply

### Specific Rules

#### 1. Modal Verbs (Legal Obligation)
- **"shall"**: Mandatory obligation
  - zh-CN: "应当" (formal) or "应" (less formal)
  - ja-JP: "しなければならない"
- **"may"**: Permissive right
  - zh-CN: "可以" or "得"
  - ja-JP: "してもよい"
- **"must"**: Imperative (stronger than "shall")
  - zh-CN: "必须"

#### 2. Defined Terms
- **Capitalized terms**: Track all defined terms (e.g., "Party", "Agreement", "Effective Date")
  - First occurrence: "Party" (hereinafter "Party")
  - Subsequent: Use exact translation consistently

#### 3. Clause Structure
- **Provisos & exceptions**: "provided that", "except", "notwithstanding"
  - Maintain logical hierarchy (main clause → exception → sub-exception)
- **Cross-references**: "Section 5.2(a)(ii)" → Ensure numbering is accurate

#### 4. Boilerplate Language
- **Force majeure, indemnification, limitation of liability**: Use jurisdiction-appropriate standard phrasing
  - Check if target jurisdiction has equivalent legal concepts

#### 5. Date & Time Sensitivity
- **Effective dates**: "30 days from the Effective Date" → Calculate accurately if needed
- **Time zones**: Specify if ambiguous (e.g., "5:00 PM EST")

---

## Tech Docs (技术文档) {#tech}

### Core Principles
- **Accuracy**: Technical precision trumps fluency
- **Consistency**: Use same term for same concept throughout
- **Usability**: Clear instructions for end-users

### Document Types
- **User manuals**: Step-by-step instructions
- **API documentation**: Developer-focused, code examples
- **Release notes**: Changelog, bug fixes
- **Knowledge base**: Troubleshooting, FAQs

### Specific Rules

#### 1. Code & Commands
- **Do NOT translate**:
  - Code snippets: `print("Hello")` → Keep as-is
  - Command-line syntax: `git commit -m "message"` → Keep as-is
  - File paths: `/usr/local/bin` → Keep as-is
  - API endpoints: `GET /api/v1/users` → Keep as-is

#### 2. UI Element Names
- **Follow software's official localization**:
  - If software is already localized, use exact UI strings
  - Example: "File" menu in MS Word → "文件" (zh-CN), not "档案"

#### 3. Procedures
- **Numbered steps**: Maintain sequential structure
  - Use imperative mood ("Click", "Enter", "Select")
  - zh-CN: "单击", "输入", "选择"

#### 4. Warnings & Notes
- **Signal words**: DANGER, WARNING, CAUTION, NOTE
  - Translate but keep visual emphasis (bold, color coding)
  - zh-CN: "危险", "警告", "注意", "备注"

#### 5. Version Numbers
- **Keep as-is**: "Version 2.3.1" → "版本 2.3.1" (not "版本二点三点一")

---

## Medical Devices (医疗器械) {#medical}

### Core Principles
- **Regulatory compliance**: Follow target jurisdiction's medical device regulations (FDA, EU MDR, NMPA)
- **Safety-first translation**: All warnings, contraindications, and precautions must be complete and unambiguous
- **Terminology consistency**: Use standardized device terminology and anatomical terms

### Regulatory Context
- **Target authority**: Specify regulatory body (FDA 510(k), EU MDR, NMPA, TGA)
- **Document type sensitivity**:
  - IFU (Instructions for Use): Patient/clinician comprehension is paramount
  - Technical specifications: Maintain engineering precision
  - Clinical evaluation reports: Evidence-based, traceable to source data
  - Labeling: Follow regulatory template structure exactly

### Specific Rules

#### 1. Device Nomenclature
- **Device names**:
  - Trade names: Keep as-is unless local registration uses different name
  - Generic names: Use GMDN (Global Medical Device Nomenclature) or local equivalents
- **Model/catalog numbers**: Always preserve exactly (e.g., `REF 12345`, `Model X-200`)
- **Size designations**: Keep precise (e.g., `5 French`, `24G needle`)

#### 2. Warnings & Precautions
- **Signal words**: Translate but maintain hierarchy
  - DANGER → 危险 (zh-CN), ОПАСНОСТЬ (ru-RU)
  - WARNING → 警告, ПРЕДУПРЕЖДЕНИЕ
  - CAUTION → 注意, ВНИМАНИЕ
  - NOTE → 备注, ПРИМЕЧАНИЕ
- **Do NOT soften**: "may cause death" must not become "might be harmful"
- **Preserve logical structure**: If-then conditions in contraindications

#### 3. Procedural Instructions
- **Numbered steps**: Maintain exact sequence
- **Use imperative mood**: `Insert`, `Connect`, `Verify` → `插入`, `连接`, `验证`
- **Equipment setup**: Keep diagrams/figures references accurate
- **Sterilization/storage**: Translate conditions exactly (temperature ranges, humidity, shelf life)

#### 4. Materials & Specifications
- **Material composition**: Keep chemical names and percentages exact
  - Example: `316L stainless steel`, `Polyethylene terephthalate (PET)`
- **Biocompatibility**: Use standard terminology (e.g., ISO 10993 test names)
- **Dimensions & tolerances**: Never round (e.g., `1.5 mm ± 0.1 mm`)

#### 5. Symbols & Standards
- **ISO 15223**: Medical device symbols (keep as-is or use standardized local equivalents)
- **Standards references**: `ISO 13485`, `IEC 60601-1` → Keep exact
- **CE marking, FDA approval numbers**: Preserve verbatim

#### 6. Clinical Data
- **Study references**: Keep citation format intact
- **Endpoints**: Translate but maintain clinical precision (e.g., "primary safety endpoint")
- **Statistical data**: P-values, confidence intervals, sample sizes exact

---

## Finance (金融) {#finance}

### Core Principles
- **Regulatory accuracy**: Follow target jurisdiction's financial reporting standards (GAAP, IFRS, local regulations)
- **Numerical precision**: All figures, percentages, and ratios must be exact
- **Consistency**: Same financial term must have same translation throughout

### Regulatory Context
- **Target authority**: Specify regulatory body (SEC, FCA, CSRC, FSA)
- **Document type sensitivity**:
  - Financial statements: Follow local GAAP/IFRS terminology exactly
  - Prospectuses: Legal precision required
  - Annual reports: Balance readability with regulatory compliance
  - Disclosures: Complete, unambiguous

### Specific Rules

#### 1. Financial Terminology
- **Account names**: Use standardized chart of accounts translations
  - Example: `Revenue` → `收入` (zh-CN), `Выручка` (ru-RU)
  - `Operating expenses` → `营业费用`, `Операционные расходы`
- **Ratios & metrics**: Maintain standard formulations
  - `P/E ratio` → `市盈率 (P/E)`
  - `ROE` → `净资产收益率 (ROE)`
- **Financial instruments**: Use regulatory-approved terms
  - `Convertible bond` → `可转换债券`, `Конвертируемая облигация`

#### 2. Numbers & Currency
- **Monetary amounts**: Preserve exact values
  - First occurrence: `$1,000,000 (100万美元)` or as style guide requires
  - Keep source currency symbol: `$`, `€`, `¥`, `£`
- **Percentages**: Exact to decimal places shown
  - `5.25%` must remain `5.25%` (not rounded to `5.3%` or `5%`)
- **Date-specific data**: Tie amounts to reporting periods clearly
  - `For the year ended December 31, 2023` → `截至2023年12月31日的年度`

#### 3. Time Periods & Dates
- **Fiscal year**: Distinguish from calendar year
  - `FY2023` → `2023财年` (zh-CN)
- **Quarter notation**: `Q1 2024`, `1Q24` → `2024年第一季度` or keep as-is per style
- **As of dates**: Critical for balance sheet items
  - `As of March 31, 2024` → `于2024年3月31日`

#### 4. Regulatory Disclosures
- **Risk factors**: Translate completely; do NOT summarize or soften
- **Forward-looking statements**: Keep disclaimers intact
- **Material events**: Preserve legal scope and timing

#### 5. Comparative Data
- **Year-over-year**: `YoY`, `同比` (zh-CN)
- **Quarter-over-quarter**: `QoQ`, `环比`
- **Tables**: Maintain column/row alignment and all footnotes

#### 6. Legal & Compliance
- **Stock exchange codes**: Keep as-is (`NYSE: ABC`, `NASDAQ: XYZ`)
- **Registration statements**: Preserve form numbers (`Form 10-K`, `Form 20-F`)
- **Audit opinions**: Use standard audit terminology

---

## Other (其他/通用) {#other}

### When to Use This Section
This section covers general business, marketing, and miscellaneous content that doesn't fit clearly into specialized domains above.

### Core Principles
- **Clarity first**: Prioritize reader comprehension
- **Brand consistency**: Maintain company voice and terminology
- **Cultural adaptation**: Localize appropriately for target market while preserving brand identity

### Common Document Types

#### Marketing Materials
- **Tone**: Engaging, persuasive, culturally appropriate
- **Slogans/taglines**: May require transcreation rather than literal translation
- **Calls to action**: Use natural, action-driven language
  - `Learn more` → `了解更多` (zh-CN), `Узнать больше` (ru-RU)
  - `Get started` → `开始使用`, `Начать`

#### Business Communications
- **Emails**: Maintain appropriate formality level
- **Presentations**: Keep concise; consider slide space constraints
- **Reports**: Professional tone, clear structure

#### E-commerce
- **Product descriptions**: Benefit-focused, scannable
- **Pricing**: Currency localization, tax implications noted if needed
- **Shipping/returns**: Clear, complete policy translation

#### HR/Internal Documents
- **Job descriptions**: Use standard role titles for target market
- **Policies**: Legal precision where needed
- **Training materials**: Clear, actionable instructions

### Style Guidelines

#### Tone Matching
- Match source formality level (casual, professional, formal)
- Adapt idioms and cultural references where appropriate
- Preserve brand personality (friendly, authoritative, innovative)

#### Localization Considerations
- **Measurements**: Convert if target market uses different system (imperial ↔ metric)
- **Dates/times**: Use local conventions
- **Contact information**: Adapt format (phone, address) to local standards
- **Social media**: Platform names may differ by region

#### Visual Considerations
- **Text expansion**: Account for length changes (zh-CN typically shorter, de-DE/ru-RU longer)
- **Character limits**: Preserve if specified (e.g., meta descriptions, UI strings)
- **Graphics**: Note when text is embedded in images

---

## Domain Detection Heuristics (Updated)

Use these keywords to auto-detect domain from uploaded source text:

- **Pharma**: "adverse event", "clinical trial", "dosage", "ICD-10", "MedDRA", "patient", "placebo", "pharmacokinetics"
- **Medical Devices**: "IFU", "instructions for use", "contraindication", "sterilization", "biocompatibility", "REF", "model number", "ISO 13485"
- **Patent**: "claim", "comprising", "embodiment", "prior art", "SEQ ID NO", "invention", "patent application"
- **Game**: "{player_name}", "[item]", "NPC", "quest", "mana", "inventory", "lore", "skill tree", "achievement"
- **Legal**: "whereas", "hereinafter", "indemnify", "arbitration", "jurisdiction", "party", "shall", "covenant"
- **Tech**: "API", "function", "syntax", "command", "git", "version", "documentation", "repository"
- **Finance**: "revenue", "EBITDA", "fiscal year", "balance sheet", "shareholder", "securities", "prospectus", "10-K"
- **Other/Marketing**: "call to action", "brand", "campaign", "engagement", "conversion", "SEO", "social media"
