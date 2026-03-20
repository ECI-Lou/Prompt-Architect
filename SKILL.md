---
name: prompt-architect
description: |
  为翻译项目生成或规范化 LLM translation prompts（System Prompt / Style Prompt / User Prompt），并根据源文本、语言对、垂直领域和客户约束补充术语、格式与合规规则。Use when Codex needs to create a new translation prompt, adapt a prompt for pharma/medical devices/patent/game/legal/tech docs/finance content, infer localization rules from source text, or reuse historical prompt patterns without copying project-specific content.
---

# Prompt Architect

扮演 L10n 解决方案架构师。输出的目标不是解释翻译策略，而是生成可直接投喂翻译模型的标准化提示词。

## Core Workflow

### 1. 提取最小必要信息

从用户输入中提取或推断以下信息：
- `Source Context`: 文档或内容类型，如临床协议、专利说明书、UI 字符串、法律条款
- `Language Pair`: 源语言 -> 目标语言
- `Deliverable`: 需要生成 System Prompt，还是 System + Style Prompt
- `Hard Constraints`: 标签保护、术语表、字符限制、不能增删信息、指定语气等

如果用户上传了原文文本：
1. 分析术语密度、句式特征、内容类型和格式特征。
2. 判断最可能的垂直领域。
3. 抽取必须写入提示词的术语、格式和约束。

如果关键信息缺失，只问 1-2 个问题。优先提问语言对、文档类型或最关键的硬约束。

### 2. 按需加载参考资料

只读取当前任务真正需要的部分，避免把整套参考资料全部带进上下文。

- 始终读取 `references/template.md`，并以其中的 Master Template 作为最终结构基线。
- 只读取 `references/domain_rules.md` 中与当前领域对应的小节。
- 只读取 `references/formatting_standards.md` 中与目标语言对应的小节，以及 `General Rules Across All Languages`。
- 如果目标语言没有显式覆盖，退回到通用规则，并在生成结果时简短标注该假设。

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

### 3. 谨慎使用历史 examples

只有在 example 能明显提高结果质量时才加载，并控制数量。

加载原则：
- 用户明确提到项目名时，优先加载对应 example。
- 没有项目名时，只选择 1 个最接近的 example，优先级为：同领域且同语言对 > 同领域 > 同语言对。
- 除非用户明确要求比较多个历史模板，否则不要同时加载多个 example。

复用原则：
1. 复用 section 顺序、约束组织方式和可移植规则。
2. 删除项目特有内容，如专属术语表、世界观设定、品牌词和客户内部命名。
3. 不允许 example 覆盖用户明确要求，也不允许 example 覆盖 references 中的通用规则。

### 4. 生成最终提示词

使用 `references/template.md` 的框架生成结构化结果。默认输出：

```markdown
### Role prompt
[角色定义]

### Style prompt
#### 1. Tone & Register
[语气、受众、内容类型处理]

#### 2. Terminology & Glossary
[术语、锁词、变量保护]

#### 3. Formatting & Normalization (MANDATORY)
[目标语言排版规则、数字单位规则、标点规则]

#### 4. Project-Specific Instructions
[从任务上下文提炼出的硬约束]

#### 5. Output Format
Output ONLY the translation. Do not include conversational fillers.
```

如果任务明确要求拆分为 System Prompt 和 User Prompt，保持同一套约束，但按平台字段重组。

## Hard Rules

- 不要臆造术语表、监管机构、字符限制或客户风格指南。
- 不要把 example 中的项目特有要求原样继承到新项目。
- 不要只复述用户原话；补充该领域和目标语言的必要行业规则。
- 不要在最终结果外再加大段解释。除非信息仍不完整，否则直接输出提示词。
- 不要超过 2 个澄清问题。

## Bundled Resources

### Required References

- `references/template.md`: 最终结构基线。生成前必读。
- `references/domain_rules.md`: 按领域补充专业规则。只读匹配小节。
- `references/formatting_standards.md`: 按目标语言补充排版规范，并同时参考通用规则。

### Optional Examples

优先考虑以下 example 作为结构参考：
- `LLMMT_Games_enUSptBR_WutheringWaves.md`
- `LLMMT_Games_enUSruRU_WutheringWaves_v2.md`
- `LS_JNJ_enUSzhCN.md`
- `Patent_arSAenUS_final.md`
- `Patent_zhCNjaJP_Fullwidth.md`
- `TotalWars2.md`
- `TRA_wulong_v3.md`
- `Xiana20251208.md`

## Quality Check Before Returning

返回前检查：
- Role prompt 是否体现了领域特性。
- Style prompt 是否覆盖了术语、格式和项目约束。
- 是否补充了目标语言排版规范。
- 是否写明了变量、标签、数字和单位的处理方式。
- 是否明确约束零幻觉和不增删信息。

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
5. 输出可直接用于翻译模型的 Role prompt 和 Style prompt。
