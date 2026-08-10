---
title: Skills 使用反馈与修正记录
status: active
created: 2026-07-18
updated: 2026-07-18
parent: GOAL-003-skills-practice
version: 0.1.0
---

# Skills 使用反馈与修正记录

> 关联目标：[GOAL-003-skills-practice](../00-meta.md)  
> 区间：2026-07-18 · 可复用产物落地后的首次强制使用（含 wrapper 创建 GOAL-004）

## 1. 已完成的核心交付

- **规则模板**：`skills/AGENTS.template.md` v0.2.0（表格化约束、P-001、检查清单）
- **核心提示词**：`skills/prompts/` 01～04（新目标 / 决策 / 执行 / 复盘）
- **目标模板**：`skills/templates/goal-folder/`（虚构 GOAL-042 示例）
- **安装脚本与文档**：`install.sh` / `install.ps1`（Claude + Copilot；`--skills-dir`；Copilot 自动复制 wrapper）+ `skills/README.md`
- **Copilot wrapper**：`new-goal` / `log-decision` / `update-execution` / `write-audit`

## 2. 使用 wrapper 创建 GOAL-004 的体验

用 `/new-goal` 等价流程创建 [GOAL-004-core-data-model](../../GOAL-004-core-data-model/00-meta.md) 时：能先读 `goal-tree.md` 推断下一编号与父目标；对跨模型/Web 的大范围目标按 P-001 只写阶段 A→D 路线图，未批量拆子目标；五件套与 goal-tree 可一次落齐。整体可用，交互优于空白表单式整表提问。

## 3. 优点

- Wrapper 要求**先分析上下文再补问**，避免一上来甩完整参数表。
- 编号、日期、默认 `status` 等可推断项有明确默认策略。
- 核心提示词与 wrapper 分离：改 `skills/prompts/` 即可全局生效。
- 安装脚本把规则与 slash 入口落到固定路径，降低手工遗漏。

## 4. 待改进点

- **wrapper 智能程度仍需提升**：当前偏「流程正确」；复杂 parent/范围边界时仍依赖用户多轮纠正，推断质量随模型读库深度波动。
- 决策 / 执行 / 复盘 wrapper 的真实使用样本仍少，01～04 尚未在多轮协作中充分压测。
- 外项目 install 实测不足；根 `AGENTS.md` 与 template 的字面同步仍靠人工判断。

## 5. 后续使用建议

1. **默认**使用编排主入口：`00-govern-orchestrator` / Copilot **`/govern`**（A-003/A-004 后产品模型）。
2. 仅在明确只要原子操作时使用 advanced：`/new-goal` 等 01～04 原语。
3. 规则有歧义时：先改 template 与核心 prompts，再评估同步根规则与 install 产物。
4. 有条件时在空仓库跑一遍 install，把结果并入本记录修订版。

## 6. A-003/A-004 修订摘要（2026-07-18）

- 偏差：四并列填表入口 ≠ 辅助达到目的；A-002 相对 GOAL-001 过早 done。
- 纠正：单一编排入口 + 01～04 原语；修订成功标准后 A-004 关门。
- 证据：`skills/prompts/00-govern-orchestrator.md`；`install/copilot/prompts/govern.md`；`python skills/tests/test_skills_orchestrator.py` OK。

## 7. Claude / Grok skill 入口（2026-07-18 补齐）

- Claude：`.claude/skills/govern/SKILL.md`（安装源 `install/claude/skills/govern/`）
- Grok：`.grok/skills/govern/SKILL.md`（安装源 `install/grok/skills/govern/`）
- 与 Copilot `govern.prompt.md` 同为 **primary `/govern`**；核心仍只读 `00-govern-orchestrator`。

## 结论

Skills 现以**编排主路径**对齐「设立 → 推进 → 审计」；原语与规则地基保留。继续用真实 `/govern` 会话压测推断质量即可，无需回到四入口并列主产品面。
