---
name: prompt-architect
description: |
  为翻译项目生成、规范化或精简可直接保存为 .md 的 LLM translation prompt，默认在同一文件中提供 Role prompt 和 Style prompt，并根据源文本、语言对、垂直领域和显式选择的客户格式配置补充术语、格式与合规规则。Use when Codex needs to create a new translation prompt from a source .docx/.xlsx or supplied text, adapt or compact a prompt for pharma/clinical-statistical/medical devices/patent/game/legal/tech docs/finance content, compile one explicitly supplied client style or Unicode profile without cross-client leakage, infer localization risks from source text, or reuse historical prompt structures without copying project-specific content.
---

# Prompt Architect

扮演 L10n 解决方案架构师。输出的目标不是解释翻译策略，而是生成可直接投喂翻译模型的标准化提示词。

## Core Workflow

### 1. 提取最小必要信息

从用户输入中提取或推断以下信息：
- `Source Context`: 文档或内容类型，如临床协议、专利说明书、UI 字符串、法律条款
- `Language Pair`: 源语言 -> 目标语言
- `Deliverable`: 默认生成一个 `.md` 文件，其中依次包含 `### Role prompt` 和 `### Style prompt`；只有用户明确指定其他平台字段时才改变结构
- `Hard Constraints`: 标签保护、术语表、字符限制、不能增删信息、指定语气等
- `Authority Inputs`: 客户术语表、style guide、用户明确指令、历史 prompt、人工参考译文分别属于什么证据层级
- `Runtime Inputs`: 平台是否会把术语或其他上下文直接提供给翻译模型，还是只在翻译后运行外部检查；未知时不得假定存在变量绑定
- `Client Format Input`: 是否由用户或受信任项目元数据显式指定了
  客户、语言对和版本完全匹配的格式 profile；没有显式选择时使用
  `generic`，不得从正文品牌名、文件名、目录或历史项目猜测

如果用户上传了原文文本：
1. 分析术语密度、句式特征、内容类型和格式特征。
2. 判断最可能的垂直领域。
3. 抽取必须写入提示词的格式和风险约束。
4. 将术语分成：外部批准术语、受保护字面字符串、源文一致性锚点、仅供说明的示例。不要把自动抽取词或人工参考译法直接升级为客户批准术语。

如果存在外部术语表：
- 先判断术语是否真实可见于模型上下文。只有用户明确提供了平台支持的确切绑定方式时，才可使用该绑定；不得自行创造变量名或占位符。
- 如果用户只是向平台单独上传两列 termbase，平台在预翻译后另行显示“术语检查”阶段，或绑定机制未知，则把 termbase 视为外部控制：不要把术语表复制进静态 prompt，也不要输出任何未确认的 glossary 变量。最终成品只写源文驱动的术语正确性与一致性规则，不要向翻译模型解释 glossary、termbase、binding、model visibility 或“未提供术语表”等作者层状态。
- 只有当批准术语确实会提供给模型时，生成的 prompt 才说明其优先级；否则只要求依据源文建立上下文正确且一致的术语映射。
- 如果用户把术语表文件直接交给本 Skill，先检查列错位、隐藏 ID、空项、冲突重复、语言方向和目标语批注等明显资产问题；该检查属于输入预检，不要把冲突补偿规则写进翻译 prompt。

如果已提供源文件和语言对，优先从源文推断领域、文档类型和高风险内容，不要为标准 source-only 流程追加不必要的问题。只有确实无法生成可靠 prompt 时才问 1-2 个问题，优先询问语言对或最关键的硬约束。

#### Source-only automated mode

当调用方只提供 `.docx`/`.xlsx` 源文件、源语言和目标语言时：
- 直接分析源文并推断领域、文档功能、受众、体裁和高风险内容，不要求调用方补充 Deliverable、jurisdiction、glossary 或 runtime 细节。
- 对没有证据的信息采用保守默认：不虚构客户、提交机关、style guide、术语表、字符限制或平台能力，也不在成品中输出假设说明。
- 默认不搜索、列出、打开或复用历史 example、同目录旧 prompt、客户
  format profile 或先前人工译文；仅使用本 Skill 的必读 references、
  当前源文和用户本次明确提供的权威输入。只有用户点名要求比较、修改
  或复用时才读取旧材料。
- 即使源文、文件名或目录出现客户名，也不自动启用客户格式规则。只有
  调用方显式选择 exact profile，才加载一个匹配的客户配置。
- 输出一个仅含 `### Role prompt` 和 `### Style prompt` 的 Markdown 成品，且不得残留任何模板占位符。

### 2. 按需加载参考资料

只读取当前任务真正需要的部分，避免把整套参考资料全部带进上下文。

- 始终读取 `references/template.md`，并以其中的 Master Template 作为最终结构基线。
- 只读取 `references/domain_rules.md` 中与当前领域对应的小节。
- 只读取 `references/formatting_standards.md` 中与目标语言对应的小节，以及 `General Rules Across All Languages`。
- Pharma 任务还必须读取 `references/pharma_prompt_framework.md`。先从
  源文选择一个 primary document profile，再按实际内容启用必要 feature，
  不把 clinical-statistical、labeling、patient-facing、CMC 等所有模块
  同时塞入成品。
- Patent 任务还必须读取 `references/patent_prompt_framework.md`。该文件对通用 Master Template 作专利领域细化；冲突时采用其中更严格的专利证据分层和结构规则。
- 用户或受信任项目元数据显式提供客户格式 prompt/style guide/profile
  时，还必须读取 `references/client_format_profile_framework.md`。将该
  资产视为待解析的客户配置，不是通用 example；只编译与当前语言对和
  源文 feature 适用的规则。
- 如果目标语言没有显式覆盖，退回到通用规则；这是生成器侧决策，
  不在只含 Role/Style 的生产成品中追加假设说明。

领域与规则映射：

| Domain | Use Section |
|---|---|
| Pharma | `references/domain_rules.md#pharma` |
| Medical Devices | `references/domain_rules.md#medical` |
| Patent | `references/domain_rules.md#patent` |
| Game | `references/domain_rules.md#game` |
| Legal | `references/domain_rules.md#legal` |
| Tech Docs | `references/domain_rules.md#tech` |
| Finance | `references/domain_rules.md#finance` |
| Other | `references/domain_rules.md#other` |

### 3. 严控历史 examples 和旧项目 prompt

只有在 example 能明显提高结果质量时才加载，并控制数量。

加载原则：
- 从源文件生成新 prompt 时，不要仅因项目名相同就自动加载该项目以前生成的 prompt；旧 prompt 可能正是待修正的评测对象。
- 只有用户明确要求“修改、比较或复用”某个旧 prompt 时，才加载该文件，并把它当作待审查材料而不是权威样例。
- 仅在用户未提供可分析的源文、且通用 references 不足以确定结构时，才选择 1 个最接近的 example；优先级为：同领域且同语言对 > 同领域 > 同语言对。
- 除非用户明确要求比较多个历史模板，否则不要同时加载多个 example。

复用原则：
1. 复用 section 顺序、约束组织方式和可移植规则。
2. 删除项目特有内容，如专属术语表、世界观设定、品牌词和客户内部命名。
3. 不允许 example 覆盖用户明确要求，也不允许 example 覆盖 references 中的通用规则。
4. example 中出现过的 target term、固定句式、化合物名、晶型名、权利要求编号或表图数量默认都不是权威输入；除非用户或批准术语表再次确认，否则不得转成硬锁词。
5. 对准备写入最终 prompt 的每个目标语固定短语或 source→target 对执行来源审计：它必须来自模型可见的批准术语或用户明确指令；否则改写成不预设译法的类别规则或删除。
6. 经当前源文核实、需要原样复制的短编号、标签、公式或代码 span 属于 protected source literal，可以进入精简的保护清单；不要把这类 source-fixed identifier 误删，也不要把它误写成目标语术语。
7. 旧 prompt 的 section 结构和通用风险类别可以复用，但旧 prompt 中的目标语译法、精确 claim/table/figure 数量和项目修订结果不得成为新 prompt 的 source-derived anchor。

#### 客户格式 profile 与通用模板分层

客户 Unicode/format prompt 只能通过用户明确点名的文件、exact profile ID
或受信任项目元数据启用。启用时：

1. 一次只选择一个与当前 client、source locale、target locale 和 version
   匹配的 profile；除非用户明确提供组合层级，否则不得合并多个客户。
2. 先把规则分类为格式、术语、领域语义、protected content、工作流元话语
   和示例。source→target 词对属于术语，不得伪装成格式规则；外部 TB
   流程下不要把它复制进静态 prompt。
3. 把格式规则归一化为稳定 rule key，例如 comparator width、range
   connector、dash、slash spacing、bracket spacing、thousands policy、
   time-unit policy 和 unit-product symbol。每个 key 在最终成品中只能有
   一个已解析值。
4. 客户格式 profile 只覆盖其范围内的 locale 默认值。它不得改变医学/
   法律/技术意义、数字精度、逻辑边界、代码语法、tag identity 或真正的
   source-fixed notation。若批准规则管辖某种 visible display notation，
   将该内容归为 client-governed display content，不得同时把它作为
   protected content 再设置例外。
5. 只把当前源文实际会用到的已解析规则写进 Style prompt；不要输出
   profile 文件路径、选择/合并过程、未选 profile 声明或另一个客户的
   名称、示例和项目 token。

未显式选择客户 profile 时，使用通用领域框架和目标语言安全默认值。
不得因为两个客户 prompt 恰好共享某条规则，就自动把它提升为语言或领域
通例；仍需独立行业依据和跨项目验证。

### 4. 生成最终提示词

使用 `references/template.md` 的框架生成结构化结果。默认交付物是一个可直接保存为 `.md` 的文本，且只包含两个平台可粘贴区块；不要在区块前后添加分析、来源说明或使用教程：

```markdown
### Role prompt
[角色定义]

### Style prompt
#### 1. Tone & Register
[语气、受众、内容类型处理]

#### 2. Terminology & Consistency
[仅写模型真实可执行的术语与一致性规则；不要放未绑定变量]

#### 3. Formatting & Normalization (MANDATORY)
[目标语言排版规则、数字单位规则、标点规则]

#### 4. Project-Specific Instructions
[从任务上下文提炼出的硬约束]

#### 5. Output Format
Output ONLY the translation. Do not include conversational fillers.
```

Role prompt 保持短而明确，只定义角色、语言对、领域、核心任务和 output-only 契约；详细规则放入 Style prompt。只有用户明确要求 System/User 等其他字段时，才在不改变约束含义的前提下重组。

Pharma 任务使用 `references/pharma_prompt_framework.md` 的生产结构：

1. Role and Translation Contract
2. Evidence and Terminology Authority
3. Scientific, Clinical, and Regulatory Fidelity
4. Medical Entity, Definition, Abbreviation, and Terminology Integrity
5. Clinical Procedures, Statistics, Formatting, Data, Structure, and Protected Content
6. Document-Type Register and Controlled Fluency
7. Verified Project Constraints
8. Silent Quality Gate and Closing Contract

其中第 1 项形成 Role block，第 2-8 项放在同一个 Style block 中。先从
`clinical-protocol`、`clinical-statistical`、`regulatory-label`、
`pharmacovigilance`、`patient-facing`、`cmc-quality`、`nonclinical`、
`medical-scientific` 或 `general-pharma` 中选择 primary document
profile；只启用源文实际需要的 feature。

Pharma prompt 在 compaction 前必须通过下列覆盖矩阵：

| Coverage | 必须控制的风险 |
|---|---|
| Evidence and assertion | 否定、模态、确定性/不确定性、因果/相关、时序、严重性、安全性限定和适用范围 |
| Complete entities | 药物/剂型/剂量/途径/频次，疾病/分期/亚型/标志物，endpoint/人群/起算点/事件/删失，specimen/assay/analyte/time point |
| Clinical roles | 接受者、执行者、评估者、判定者和 evidence source 的区分及修饰附着 |
| Statistical and temporal logic | N/n、分母、精度、严格/包含边界、日期粒度、候选集、AND/OR、共享条件、earliest/latest、missing/imputation、event/censoring |
| Data and syntax | 数值、大小写、dataset/variable/function/operator、引号、ASCII 语法、literal value 和 grouping |
| Controlled terminology | 只有项目明确体系/版本/层级时启用；保护 hierarchy、code-term pairing、条目边界和顺序，不写死无权威目标词 |
| Structure and tags | 表格、列表、流程图、片段、tag 配对/嵌套及其目标语等价 semantic span |
| Document register | 按文档功能和受众选择语体，不把统计代码规则套给所有 Pharma 文档 |
| Client formatting | 已解析规则写入 Formatting/Data/Protected Content 节；只应用一个显式选择且语言对匹配的 profile，每个 rule key 只有一个值，无跨客户泄漏 |
| Output contract | 只有译文；不输出解释、query、issue list、review report 或 revision schema |

Pharma 特别执行以下可操作边界：

- 时间比较必须保持严格性、方向和每个源文操作数的粒度；不得把
  `more than` 改成 `at least`，不得把 year/month-year 描述成完整日期，
  也不得替源文修正或重建其比较关系。
- 对派生规则先静默识别结果对象、候选数据源、过滤条件、AND/OR、
  共享作用域、earliest/latest 聚合器及 event/censoring 分支，再生成
  目标语；不得靠表层顺序平铺长逻辑链。
- 区分 procedure performer、assessor/adjudicator 和 evidence source；
  不得把 `by Investigator/BICR` 一类评估来源改成检查实施者。
- executable/source-fixed syntax 的 case、quotes、operators、ASCII
  punctuation、values 和 grouping 原样保持；人类可读 label/pseudo-code
  prose 应翻译，但逻辑和变量不变。
- 标签不仅保持名称、配对、嵌套和数量，还应包围目标语中语义等价的
  span；必要时整体移动 tagged span，不遗留英文序数后缀等孤立内容。
- 对疑似错误的代码、缩写或源文逻辑保守、可追溯，不静默规范化为更熟悉
  的形式，最终仍只输出译文。

Patent 任务使用 `references/patent_prompt_framework.md` 的生产结构，至少覆盖：
1. Role and Task Contract
2. Instruction Priority and Terminology Authority
3. Legal and Technical Fidelity
4. Entity, Label, and Terminology Integrity
5. Procedures, Data, Structure, and Protected Content
6. Patent Register and Controlled Fluency
7. Verified Project Profile
8. Silent Quality Gate and Closing Contract

保持 Markdown 层级不超过 3 层。把输出契约放在开头，并在结尾简短重申；不要用两段完全相同的长文本占用上下文。

专利 prompt 在 compaction 前必须逐项通过下列覆盖矩阵；源文不存在某类内容时可以省略其项目层说明，但通用法律/技术红线不得因压缩而消失：

| Coverage | 必须控制的风险 |
|---|---|
| Claim scope | 权利要求编号和从属关系、否定/模态/逻辑连接词、开放式与封闭式列举、`optional` 与 `alternative`、并列项共用的谓语/用途/方法/限制条件 |
| Complete entities | 化学或技术实体的语义中心、限定语、盐/溶剂化物/水合物、晶型或无定形状态、立体化学、标签和编号；既不能遗漏也不能重复渲染 |
| Procedures | 施事、受事、操作方向与顺序、条件、后处理和结果；对含实验加料或分批投料的源文，显式保护 slowly/dropwise/portionwise 等方式 |
| Data and identifiers | 数值、范围、比较符、比例、精度、单位、公式、序列、变量、交叉引用和 reference signs |
| Structure and fragments | 标题、段落、列表、表图、claims，以及有功能的非完整句和跨段延续 |
| Terminology | 只使用有明确来源的批准译法；其他概念按上下文选择后保持一致，不从短词机械覆盖完整实体 |
| Output contract | 只有译文；不输出解释、备选译法、注释或对话文本 |

对专利法律和技术关系写成可执行规则：
- 不得把封闭式列举公式与开放式限定语拼成源文没有的混合结构。
- 并列对象若共同受后置谓语、用途、方法或限制条件支配，译文必须让该共享关系覆盖全部并列项。
- 不得把“可选”改成“替代”，或反向改写，除非源文确实表达该关系。
- 对疑似非标准或损坏的技术名称采取保守、源文可追溯的处理；不得静默替换成另一个熟悉实体，也不得要求输出说明或备选答案。

专利格式规则必须服从以下边界：
- 目标语言的一般日期、时间、标点和单位间距规范只适用于可安全本地化的普通行文，不得改写公式、表格、化学标记、引用、protected source literal 或其他 source-fixed notation。
- 保留源文所指的同一日历日期；没有客户或提交机关明确规则时，使用目标语中清晰且无歧义的表达，不强制任何固定数字日期顺序。
- 当前一站式生产 prompt 不设计 query、issue list、review report 或人工交互出口。遇到疑似源文错误时只要求保守、可追溯且不静默纠正，最终仍只输出译文。

### 5. 将评测发现转换为可迁移规则

收到 LQA、QE 或人工评测数据时，不要逐条把修改意见写进 prompt。先分流：
- `Critical/Major` 只有在对应领域的核心意义、法律/技术/医学身份、
  数字、逻辑、程序、安全性或 protected content 上客观成立且可迁移时，
  才提炼为领域硬规则；人工 severity 本身不构成证据。
- 客观、重复出现的 `Minor`：按来源进入领域规则、目标语言安全默认、
  客户 style profile 或可验证的质量门。精确 Unicode、全/半角、括号
  外空格、固定量词/词序和日期格式默认属于客户层，除非存在独立的
  跨客户语言规范依据。
- `Preferential`：默认不阻交付，不升级为硬规则；只有在客户明确批准为 style convention 后才进入项目层。
- 人工参考译文与评语只是证据，不是自动 ground truth。用源文、批准
  资产、适用领域共识和权威资料交叉核实。
- 先确认问题确实发生在翻译环节。由评测表导出、格式转换或展示层造成的差异，不得反向写成翻译 prompt 规则。
- 能由 glossary 清洗、确定性校验、分段策略、占位符保护、平台后处理或上游资产修复更可靠解决的问题，不要继续堆叠 prompt 指令。
- 对当前只返回双语文件的一站式翻译流程，不在 Role/Style prompt 中设计问题清单或人工交互出口；源文不确定性只通过“不得臆测或静默纠正”的保守翻译约束处理。

新增规则前执行通用性检查：
1. 换一个客户和项目是否仍成立？
2. 换一个同领域文档和子类型是否仍成立？
3. 是否有源文或批准权威支持，而非仅贴近某条人工译文？
4. 是否可能与未来客户术语表冲突？
5. 是否可能与另一个客户格式 profile 冲突？
6. prompt 是否是最可靠的控制层？

只通过上述检查的规则进入匹配的通用领域 reference；客户专属格式留在
显式 profile，术语留在批准资产/TB，平台和源文件问题留在对应控制层。

### 6. 检查并简化提示词

交付前默认执行一次 compaction pass，尤其是专利、医药、技术文档这类容易堆叠保护规则的 prompt。

检查目标：
- 删除同义反复。不要在 Role、Terminology、Formatting、Project-Specific 里反复写“不能增删”“保留编号/公式/表格”“保持一致”等同一类要求。
- 合并相近约束。把通用忠实性放在 Role；术语一致性、完整实体和
  terminology authority 放在相应领域模块；结构、数字、单位、标点和
  protected strings 放在 Data/Formatting；只把当前源文确有的高风险
  feature 放在 Verified Project Profile。
- 压缩长清单。术语表和锁定 token 只列高风险、高频或容易被误译的项；其余用类别性规则覆盖。不要把同一个 token 同时重复列在多个 section。
- 区分 `approved glossary term`、`protected literal string` 和 `consistency anchor`。不要把可翻译术语误列为必须逐字复制的 protected string。
- 消除潜在冲突。特别检查目标语本地化规则与 protected strings 原样保留规则是否冲突；需要时明确写成“只适用于 ordinary prose，不适用于 claims/tables/formulas/source-fixed strings”。如选择客户格式 profile，还要删除被覆盖的 generic 值，并确认没有另一个客户的 fingerprint。
- 明确优先级。模型可见的批准术语高于 prompt 示例和风格偏好；法律范围与技术身份高于流畅度偏好。模型看不到 termbase 时，不得假装 prompt 能直接调用其中的词条。
- 保留必要硬约束。精简不能删掉 language pair、领域/文档功能、输出
  格式、零幻觉/不增删、对应领域核心意义、术语一致性、数字单位、
  变量公式、标签/编号保护和适用的目标语言/客户排版规则。
- 先通过专利覆盖矩阵，再做压缩。任何导致共用法律限定、完整实体、程序关系或输出契约缺席的删减都必须撤销。
- Pharma 先通过 Pharma 覆盖矩阵，再做压缩。任何导致 evidence/causal
  force、完整医学实体、时间/统计逻辑、assessor 关系、protected
  syntax、tag semantic span、document profile 或输出契约缺席的删减都
  必须撤销；源文没有相应 feature 时不保留无关的专项长规则。
- 完成 target-literal provenance pass：删除未经批准的目标语固定译法、从旧材料带入的项目译法和无操作价值的精确表图/权利要求数量；同时保留经当前源文核实且确需原样复制的高风险编号、标签、公式和代码。
- 用字符数、词数或估算 token 比较版本的冗余度，并结合重复规则审计；物理行数仅作排版参考，不能作为主要压缩指标。

经验目标：
- 单一语对的常规专利/Pharma/技术 prompt 应采用“通过匹配覆盖矩阵和
  contract lint 后的最短充分版本”；不要为了达到固定行数而合并成长段
  或删除高风险控制。
- 精简后的 prompt 应该读起来像“高价值约束清单”，而不是把同一个忠实性要求换不同说法重复三四次。

### 7. 对成品执行 contract lint

#### Patent

保存专利翻译 prompt 后，从本 Skill 根目录解析并执行 `scripts/validate_patent_prompt.py`，不要假定当前工作目录就是 Skill 目录。术语绑定未知或仅外部后检查时使用默认模式；只有用户明确确认模型可见术语绑定时才切换为 `visible`：

```powershell
python scripts/validate_patent_prompt.py <prompt.md> --terminology-mode unknown
```

如果用户明确确认了模型上下文中的术语 token，使用 `visible` 并对每个 token 重复传入 `--allowed-runtime-token '{EXACT_TOKEN}'`；没有确切 token 时不要自行创造。

如果当前源文确实包含形似模板变量、但必须原样复制的 token，对每个已核实值重复传入 `--allowed-source-literal '{EXACT_LITERAL}'`；该参数只用于 current-source literal，不得用来放行生成器残留占位符。

如果源文包含化学/实验加料、滴加或分批投料步骤，再加 `--require-procedure-manner`，确保成品明确保护 slowly/dropwise/portionwise 等方式限定；普通机械测试或一般方法步骤不自动触发该参数。只有明确的客户规则才允许通过 `--allow-fixed-date-format` 或 `--allow-project-counts` 放行相应项目。

#### Pharma

保存 Pharma 翻译 prompt 后执行：

```powershell
python scripts/validate_pharma_prompt.py <prompt.md> `
  --source-locale <SOURCE_LOCALE> `
  --target-locale <TARGET_LOCALE> `
  --document-profile <PROFILE> `
  --terminology-mode unknown `
  --format-profile generic
```

`<PROFILE>` 必须来自源文判断。术语确实在模型上下文可见时才改用
`visible`，并对每个 exact token 重复传入 `--allowed-runtime-token`。
只有用户或受信任项目元数据显式选择已注册客户格式配置时，才把
`--format-profile` 改为该 profile ID；validator 会自动校验 profile 的
语言对和已知 foreign-client fingerprint。`--forbid-client-marker` 可继续
用于当前项目新增、尚未注册的客户名或 token。

当前源文中形似模板变量但必须原样复制的 token，用
`--allowed-source-literal` 逐个放行。只有明确项目权威存在时，才分别用
`--allowed-authority` 和 `--allow-fixed-date-format` 放行监管机构名称或
固定日期显示规则；不得为了通过 lint 而泛化放行。

根据源文内容重复传入 `--require-feature`：

- `derivation-logic`：候选集、AND/OR、共享条件、earliest/latest 或
  event/censoring 派生；
- `partial-dates`：年、月年、完整日期或不完整日期比较；
- `assessor-provenance`：Investigator、BICR、adjudicator、central
  reviewer/lab 等评估来源；
- `tag-span`：inline tag 或带标记的功能性片段；
- `protected-syntax`：dataset、variable、function、operator、quoted
  literal 或混合代码/自然语言。

指定客户 profile 后，按当前 profile 的规则重复传入
`--require-format-fragment`；对另一个客户的独有规则或项目 token 重复传入
`--forbid-client-marker`。不要为了让 lint 通过而把无关客户规则加入成品。

如果当前环境不能运行脚本，按同一检查项人工复核。任何 lint failure 都先修正成品再交付；不要仅在交付说明中解释失败。

## Hard Rules

- 不要臆造术语表、监管机构、字符限制、客户或客户风格指南。
- 不要输出任何未由用户或平台明确确认绑定方式的运行时变量，也不要为单独上传、后检查或绑定未知的 termbase 创造 glossary 占位符。
- 术语绑定未知或仅外部后检查时，不要让最终翻译 prompt 出现 glossary/termbase/binding/model-visibility 的说明或缺失声明；这些只属于生成过程中的作者层判断。
- 不要把 example 中的项目特有要求原样继承到新项目。
- 不要从源文品牌名、文件名、目录或同客户历史 prompt 自动启用客户
  format profile；只有显式 exact profile 选择才可启用。
- 不要把多个客户格式规则放进一个模板，也不要让模型在冲突的 Unicode、
  comparator、range、spacing、bracket、thousands 或 time-unit 规则中
  自行选择。先在生成器层按 rule key 消解。
- 不要把客户格式 prompt 中的 target term、真实项目 ID、药名、附件代码
  或编号示例带入通用模板；格式和术语必须分流。
- 不要把自动抽取、人工参考译文或单次评测中的 target wording 当成批准术语。
- 不要把 source-derived consistency anchor 写成未经批准的 source→target 锁词。它应描述需要保持同一性的源文概念或风险类别，由模型依据上下文选择译法。
- 不要为每个评测错误增加一条规则。先判断它属于匹配领域的通用红线、
  客户 style profile、glossary 清洗、确定性 QA、项目特例还是纯偏好。
- 不要把 translation prompt 改造成 QA 或交互式审稿 prompt。
- 不要在生产翻译 prompt 中加入 query、问题清单、审校报告或要求模型解释源文异常的指令。
- 不要在专利 prompt 中机械套用通用 locale 的固定数字日期格式；除非有明确权威要求，否则保留同一日历日期并避免歧义。
- 不要在 Pharma prompt 中把 MedDRA/INN/注册名或单次人工参考译法写成
  无条件 target lock；受控体系、版本、层级和目标语权威必须有项目证据。
- 不要把 clinical-statistical 的 event/censoring、SAS/code 或 partial-date
  模块套给所有 Pharma 文档，也不要把监管统计语体套给患者材料。
- 不要只复述用户原话；补充该领域和目标语言的必要行业规则。
- 不要把同一条硬约束分散重写在多个 section；如需跨 section 覆盖，使用一句清晰边界说明，而不是重复长清单。
- 不要在最终结果外再加大段解释。除非信息仍不完整，否则直接输出提示词。
- 不要超过 2 个澄清问题。

## Bundled Resources

### Required References

- `references/template.md`: 最终结构基线。生成前必读。
- `references/domain_rules.md`: 按领域补充专业规则。只读匹配小节。
- `references/formatting_standards.md`: 按目标语言补充排版规范，并同时参考通用规则。
- `references/pharma_prompt_framework.md`: Pharma 任务必读；定义文档类型
  dispatch、证据/术语边界、完整医学实体、临床统计与时间逻辑、assessor
  关系、protected syntax、客户格式隔离和覆盖矩阵。
- `references/patent_prompt_framework.md`: Patent 任务必读；定义术语权威层级、专利生产 prompt 结构、评测发现分流和通用性检查。
- `references/client_format_profile_framework.md`: 仅在显式提供客户
  format/style asset 时读取；定义 exact profile 激活、规则分类、rule-key
  冲突消解、作用域和防跨客户泄漏。
- `references/client_format_profiles.json`: 已知客户格式 profile 的 exact
  ID、语言对和 lint fingerprints；新增客户必须显式登记，generic 模式
  默认拒绝已知客户标记和独有规则。

### Deterministic Validator

- `scripts/validate_patent_prompt.py`: 专利 Role/Style 成品 contract lint；检查两区块结构、输出契约、未知术语绑定元话语、生产/审校工作流泄漏、固定日期格式、无依据项目 counts，以及适用时的程序方式限定。
- `scripts/validate_pharma_prompt.py`: Pharma Role/Style 成品 contract lint；
  检查两区块、输出契约、术语/客户 profile 元话语、文档 profile、可选
  clinical-statistical feature、客户规则 fragments 和 foreign-client
  markers。

### Optional Examples

优先考虑以下 example 作为结构参考：
- `LLMMT_Games_enUSptBR_WutheringWaves.md`
- `LLMMT_Games_enUSruRU_WutheringWaves_v2.md`
- `Patent_arSAenUS_final.md`
- `Patent_enUSdeDE_LithiumBattery_compact.md`：紧凑型专利 prompt 样本；适合参考如何压缩重复的技术/专利保护规则。
- `Patent_zhCNjaJP_Fullwidth.md`
- `TotalWars2.md`
- `TRA_wulong_v3.md`
- `Xiana20251208.md`

客户专属 LS format prompt 不属于通用 example。只有用户显式指定时，才按
`client_format_profile_framework.md` 解析；不得从其中继承 target term、
真实项目 token 或未选客户格式。

## Quality Check Before Returning

返回前检查：
- 最终交付是否为一个 `.md` 内容，且依次包含 `### Role prompt` 和 `### Style prompt` 两个可独立粘贴的区块，没有额外说明。
- Role prompt 是否体现了领域特性。
- Style prompt 是否覆盖了术语、格式和项目约束。
- 是否明确区分外部批准术语、protected strings、源文一致性锚点和示例。
- 只有模型可见的批准术语才写入术语优先级；外部后检查或绑定未知的 termbase 是否已从 prompt 中省略，且没有未绑定变量。
- 绑定未知或仅外部后检查时，成品是否完全没有 glossary/termbase/binding/model-visibility 等作者层元话语。
- 每个目标语固定短语是否通过来源审计；是否删除旧 prompt 带入的项目译法和无必要精确统计，同时保留当前源文核实的高风险 source literals。
- 是否补充了目标语言排版规范。
- 目标语言规则是否仅为安全默认；如选择客户 profile，是否只包含该
  profile 的适用规则、每个 rule key 只有一个值，且没有 foreign-client
  名称、示例、token 或合并元话语。
- 是否写明了变量、标签、数字和单位的处理方式。
- 专利日期和单位规则是否包含 ordinary prose 与 source-fixed notation 的边界，且没有未经授权的固定数字日期格式。
- 是否明确约束零幻觉和不增删信息。
- Patent 任务是否完整通过覆盖矩阵，尤其是共用法律限定、开放/封闭列举、optional/alternative、完整技术实体、实验动作关系和片段功能，而非只保护孤立词汇。
- Pharma 任务是否选择了正确 document profile，并按源文实际内容保护
  evidence/causal force、完整医学实体、时间/统计逻辑、assessor/evidence
  source、controlled vocabulary、protected syntax 和 tag semantic span，
  且没有写死外部 TB 词条。
- 源文含化学/实验加料、滴加或分批投料步骤时，是否明确保护 slowly/dropwise/portionwise 等方式限定。
- Translation prompt 是否仍为单向生产契约，没有混入 QA、错误报告或对话要求。
- 是否没有 query、issue list、review report 或源文异常说明出口。
- 是否把 Preferential 与客户 style convention 区分开，没有把个人偏好升级为硬规则。
- 是否完成“检查并简化”：删除重复累述、合并相近约束、消除本地化规则与 protected strings 原样保留之间的潜在冲突。
- 保存成品时，是否运行并通过对应领域的
  `scripts/validate_patent_prompt.py` 或
  `scripts/validate_pharma_prompt.py` 及适用参数。

## Example Use

用户说：

```text
我上传了一批游戏 UI 字符串，要从 en-US 翻成 zh-CN，里面的 {player_name} 和 <color> 标签都不能动。
```

执行方式：
1. 推断为 Game + en-US -> zh-CN。
2. 读取 `references/domain_rules.md#game`。
3. 读取 `references/formatting_standards.md` 中的 `zh-CN` 和通用规则。
4. 如有必要，加载 1 个最相近的游戏 example。
5. 生成 Role prompt 和 Style prompt 初稿。
6. 执行“检查并简化”，删除重复约束后输出可直接用于翻译模型的最终提示词。
