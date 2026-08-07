---
id: D-001
goal: GOAL-006-consumer-surface-convergence
doc: decision
title: 消费面路径相对化方案冻结（A+C 混合）
status: accepted
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# D-001 · 消费面路径相对化方案冻结（2026-08-08）

## 决定

采用 **A+C 混合**：

1. **prompts / 薄壳 / canonical 扫尾**（00/05/06/07 与 01～04 原语、`mcp/lifecycle.py` managed 段、`docs/architecture/overview.md`、`docs/architecture/directory-layout.md`、`docs/README.md`）：全部 `docs/…` 路径引用相对化为 **`{governance_root}/…`** 字面，语义定义句与 `docs/vision/alignment.md` / AGENTS §1 同构——「`{governance_root}` 默认 `docs`，可经 `.goal-governance.json` 配置为仓库内相对根；仓外 fail closed；根下内部相对布局不可改」。
2. **`skills/AGENTS.template.md`**：路径类引用并入 **`{{GOVERNANCE_ROOT}}`** 占位（与既有 `{{CORE_TEMPLATES_DIR}}`、`{{WORKSPACE_ROOT}}` 等 `{{...}}` 机制一致，消费方安装时替换为项目真实值）；非路径类引用维持现状。使用说明补 `{{GOVERNANCE_ROOT}}` 条目。
3. **install 链路**（`install.sh` / `install.ps1` / `update.py`）：不改机器展开逻辑（方案 A 语义）；其中面向消费方的说明文本与示例路径同步相对化表述。

## 为什么

- **先例**：R3 车辆（workspace-003 GOAL-004 D-002 必改清单）已把 `docs/vision/alignment.md` 相对化（26 处 `{governance_root}`）；AGENTS §1 与 `principles.md` 顶部已有治理根定义句——本方案是同一语义向消费面（模板/prompts）的延伸，非新协议。
- **零运行时改动**：`{governance_root}` 为文档语义（AI/读者按仓库内实际布局解释），不要求 install/update 机器替换；已发布 zip 与已安装消费仓**不回滚、不破坏**（成功标准 4）。
- **模板一致性**：`AGENTS.template.md` 使用说明本就要求「将 `{{...}}` 替换为项目真实信息后生效」——路径类并入 `{{GOVERNANCE_ROOT}}` 与该机制天然一致，避免模板内出现两层语义（`{{...}}` 与 `{governance_root}` 混用）。
- **测试面小**：文本相对化 + 少量断言（`governance_root≠docs` 场景）+ stage 0 漂移，无需新运行时契约。

## 未选方案

| 方案 | 理由（未选） |
|------|--------------|
| B · 安装时 pin 展开（install 脚本机器替换 `{governance_root}` 为实际 pin） | 需改 install.sh/ps1/update.py + 消费契约 + 已安装内容不回滚策略；AI 消费时读仓库实际布局，占位符语义已足够；成本高、收益有限 |
| 纯 A · 模板也全用 `{governance_root}` 字面（不并入 `{{...}}`） | 模板已有 `{{...}}` 安装时替换机制；路径类并入占位与机制一致，消费方填写明确；纯 A 会在模板中制造两套占位语义 |

## 影响范围

- E-002 影响面清单：14 文件约 240 处 `docs/` 引用（prompts 5+4 文件、AGENTS.template、install 3 文件、lifecycle、canonical 3 文件）。
- 镜像面：`skills/core/docs/**` 由 stage 生成——改 canonical 白名单（`directory-layout.md` 等）后必须 `python scripts/stage_skills_mirrors.py` + `--check` + 同一提交（AGENTS §8c）。`skills/core/docs/README.md`、`skills/core/docs/vision/README.md`、`skills/core/README.md` 为手维文件，不在 stage 覆盖范围，按需同步。
- `docs/vision/alignment.md` 已相对化（基准），不改。

## 后续

- **S2 实施**：按上述三条逐一改写 14 个文件；模板补 `{{GOVERNANCE_ROOT}}` 使用说明；测试补 `governance_root≠docs` 场景断言（如 install 输出/模板渲染断言或 prompts 相对化一致性检查）；stage + `--check`。
- **I-001 closed**：证据 = E-002（盘点）+ 本决策（方案取舍）。
- I-002（non-blocking）保持 open，S3 验收时核对已发布资产兼容面。
