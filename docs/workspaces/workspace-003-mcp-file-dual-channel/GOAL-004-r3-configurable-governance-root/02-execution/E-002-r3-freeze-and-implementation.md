---
id: E-002
goal_id: GOAL-004-r3-configurable-governance-root
title: R3 方案冻结与 governance_root 实现落盘
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# E-002 · R3 方案冻结与实现（2026-08-07）

## 事实

1. **方案冻结**：D-001（配置 schema 与解析规则）与 D-002（canonical 改写清单 + 例外说明）落盘并 accepted；I-001 / I-002 关闭。
2. **解析实现**（`skills/mcp/config.py`）：
   - `resolve_governance_root`：默认 `docs`；`.goal-governance.json`（可提交项目配置）可覆盖为其他仓库内相对根；绝对路径、`..` 越界、非法 JSON、非对象配置全部 fail closed 明确报错。
   - `governance-root.schema.json` 随包分发（`skills/mcp/`）。
   - doctor 接线：解析失败时报告 `governanceRootError`。
3. **canonical 权威面修订**（V-F-013 路径 A）：
   - `docs/vision/alignment.md`：治理根定义节 + Minimal Complete Install 表路径列与全部路径叙述相对化（`{governance_root}/…`）+ 例外说明（monorepo 固定 docs）。
   - `docs/architecture/workspace-protocol.md`：治理根定义 + 术语表/§2/§2.6/Q2/legacy 路径相对化。
   - 根 `AGENTS.md`（0.12.0 → 0.13.0）：§1 真相来源表相对化 + 治理根定义 + §6d/快速链接相对化。
   - `docs/templates/`：workspace-context（frontmatter + 复制说明）、goal-folder/00-meta、vision/charter、vision-plan 相对化。
   - 镜像已 stage（`stage_skills_mirrors.py` 6 个文件复制，`--check` 通过）。
4. **测试**（新增 15 条）：

   | 文件 | 覆盖 |
   |------|------|
   | `skills/tests/test_mcp_config.py` | 默认/配置覆盖/内部布局冻结/绝对路径 fail/越界 fail/非法 JSON fail/schema 校验（9 条） |
   | `docs/tests/test_governance_root_canonical.py` | C4：alignment/protocol/AGENTS/templates 无裸硬编码（相对化断言 + 例外说明；6 条） |

5. **行为源变更连锁**：AGENTS.md 变更使 v0.13.0 runtime evidence（12 条，行为源含 AGENTS.md）哈希失效 → 按 producer 门禁惯例整批刷新（`{SCRATCH}/runtime-refresh-v0130.log`，复用既有探针参数真重新捕获）。矩阵/镜像随之保持一致。
6. **全量回归**：待 evidence 刷新完成后最终数字（预期 197+ passed）。

## 进度评估

- C1（解析 + fail closed + 布局冻结）✅、C2（pin 落盘）✅、C3（canonical 修订 + 镜像）✅、C4（无裸硬编码测试）✅、C5（审计闭合）⏳。
- 待办：self 审视落盘；grok build（grok-4.5 / high）independent 意见落盘；required findings 闭合；R3 检查点 git commit。
