---
id: D-002
goal_id: GOAL-004-r3-configurable-governance-root
title: R3 方案冻结 · canonical 权威面改写清单与例外说明（I-002 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-002 · canonical 权威面改写清单（2026-08-07）

## 决定

按「R3 协议面变更车辆（V-F-013 路径 A）」，将权威面「仓库根 `docs/`」硬编码叙述修订为**相对 `governance_root`（默认 `docs`）**。改写的**只限路径叙述**，治理内容语义不变。

### 改写清单（本目标范围内）

| 文件 | 改写内容 | 级别 |
|------|----------|------|
| `docs/vision/alignment.md` | 引入「治理根 `governance_root`（默认 `docs`）」定义节；§0.1 Charter 路径、§0.2 Minimal Complete Install 表路径列、vision 台账/plans/workspaces/checklist 路径叙述改为 `{governance_root}/…`；例外说明（生产仓固定 docs） | **必须** |
| `docs/architecture/workspace-protocol.md` | 顶部增加治理根定义与解析规则引用；工作区根/legacy 行叙述相对化 | 按影响面（必改） |
| 根 `AGENTS.md` | §1 文档真相来源表路径相对化 + 治理根定义句；§6d/快速链接关键路径相对化（操作摘要） | 按影响面（必改） |
| `docs/templates/workspace-context.md` | 复制说明与 `canonical_scope` 示例相对化 | 按影响面（必改） |
| `docs/templates/goal-folder/00-meta.md` | 与 `docs/README.md` 交叉链接句相对化 | 按影响面 |
| `docs/templates/vision/charter.md`、`vision-plan.md` | 「复制为 `docs/vision/...`」→「复制为 `{governance_root}/vision/...`（默认 docs）」 | 按影响面 |

**例外说明形态**：各文件写明「默认 `governance_root = docs`；本 monorepo 生产仓即固定 `docs`（生产实例自身）；消费仓可通过 `.goal-governance.json` 配置其他相对根，根下内部布局不可改」。

### 镜像

改完上述白名单路径（alignment、templates）后**同一任务**执行 `python scripts/stage_skills_mirrors.py` 并 `--check` 通过；`skills/core/docs/vision/alignment.md` 与 `skills/core/docs/templates/**` 变更一并提交（§8c）。根 `AGENTS.md` 与 `workspace-protocol.md` 不在 stage 白名单（protocol 在！——见下表更正）。

> 更正：`workspace-protocol.md` 属 `docs/architecture/` 白名单（`stage_skills_mirrors.py` ARCHITECTURE_FILES 含 workspace-protocol.md）→ 同样 stage 镜像 `skills/core/docs/architecture/workspace-protocol.md`。

## 未选方案

- 全仓机械替换所有 `docs/` 出现（含历史记录/legacy 语境）：排除——只改权威面当前叙述，历史与 legacy 保留事实语境。
- 不改 canonical 只改运行时：排除（VP-004 R3 禁止）。

## 依据

- VP-004「R3 协议面变更车辆」表：必须改 alignment（至少 MCI 路径叙述）；按影响面改 workspace-protocol、根 AGENTS、相关 templates。
- AGENTS §8c：改白名单 canonical 后同一任务 stage 镜像并 `--check`。

## 证据 / 结论

- I-002 以本决定关闭（required → closed）。验证动作：`docs/tests/test_governance_root_canonical.py`（C4 无裸硬编码断言）+ `stage_skills_mirrors.py --check`。
