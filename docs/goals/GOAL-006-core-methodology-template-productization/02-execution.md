---
id: GOAL-006-core-methodology-template-productization
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.2.0
---

# 执行记录 · GOAL-006

## 时间线

### 2026-07-19 · 目标立项

- 按用户明确指令创建本目标，设置 `parent: GOAL-001-main-vision`、`status: active` 与 `progress: 0%`。
- 将 [GOAL-001 D-008](../GOAL-001-main-vision/01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 的最小交付包、独立复制验证、版本/镜像同步与阶段审计门槛写入范围和成功标准。
- 已同步 [goal-tree.md](../goal-tree.md) 与 GOAL-001 的路线图/执行记录。
- 尚未修改或验证阶段 4 的实际交付物；独立复制、版本/镜像同步和阶段审计均未发生。

### 2026-07-19 · 核对核心入口与 canonical 模板

- **事实**：按 `skills/prompts/00-govern-orchestrator.md:65-72` 定位 `SKILLS_PKG` 为 `skills/`；`skills/prompts/README.md:16-25` 将 `/govern` 标为主入口、`/audit` 标为交叉入口，Copilot wrapper 与 Claude/Grok skill 均指向同一编排器。
- **事实**：`AGENTS.md:22-27,43-55,91-101`、`docs/README.md:45-53`、`docs/architecture/principles.md:45-58,86-101` 能相互定位目标存储、五件套、路线图和审计闭环；本次未发现需要补写的核心入口路径。
- **事实**：`docs/templates/goal-folder/` 含 `00-meta.md`、`01-decision.md`、`02-execution.md`、`03-audit.md` 与 `attachments/.gitkeep`；`docs/templates/README.md:12-29` 声明其为 canonical 上游，`skills/templates/README.md:12-16` 声明后者为分发镜像。
- **验证**：四个模板文件的 canonical/mirror SHA256 逐一相等；运行 `python -m unittest skills/tests/test_skills_orchestrator.py -v`，21 项测试全部通过（含 PowerShell `-All` 隔离安装烟测）。

| 模板 | canonical SHA256 | Skills mirror SHA256 |
|------|------------------|----------------------|
| `00-meta.md` | `876375F56EE57F15DAEA3A67C43EDFAAF651B4BB1CF16DB24376FAEC3424AB43` | `876375F56EE57F15DAEA3A67C43EDFAAF651B4BB1CF16DB24376FAEC3424AB43` |
| `01-decision.md` | `C4A35BA90099026154072D41D0385066F160B37C08D985E08058E45C617FED9B` | `C4A35BA90099026154072D41D0385066F160B37C08D985E08058E45C617FED9B` |
| `02-execution.md` | `B9BAB71636E3F3AF49192430DC4DE8A62859481B41D716D08F4997D320078D4F` | `B9BAB71636E3F3AF49192430DC4DE8A62859481B41D716D08F4997D320078D4F` |
| `03-audit.md` | `E5FB3681F0ED9C332E6EF3C2C486E150718C842352E7D2831823172C9E52F2BE` | `E5FB3681F0ED9C332E6EF3C2C486E150718C842352E7D2831823172C9E52F2BE` |

- **进度结论**：成功标准 1、2 已有路径与测试证据；尚未宣称独立启用说明、空 Git 复制、版本/变更范围记录或阶段审计完成。

## 下一步

1. 编写独立启用说明并执行空 Git 仓复制验证。
2. 记录版本/镜像同步与验证结果，再进行阶段审计。

## 进度评估

**40%**：五项成功标准中前两项已完成入口/模板核对并留有可复现证据；独立复制、版本/变更范围记录和阶段审计仍未完成。
