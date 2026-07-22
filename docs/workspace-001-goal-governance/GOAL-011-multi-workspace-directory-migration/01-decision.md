---
id: GOAL-011-multi-workspace-directory-migration
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.2.0
---

# 决策记录 · GOAL-011

## 信息需求与阶段门禁

本目标唯一的信息台账位于 [00-meta.md](00-meta.md#信息就绪与未知项)。I-001～I-003 为 required，分别阻断目录迁移、共享资料索引和消费适配器验证；I-004 是 GOAL-009 的后续产品能力，不阻断本目标。

## D-001 · 以工作区根取代全局 goals 根，并建立候选资料索引（2026-07-20）

**状态**：accepted

**确认来源**：用户明确要求取消全局 `docs/goals/`，改为 `docs/workspace-序号-名称/` 形式的多个工作区目录和同级 `docs/shared-materials/`；并要求当前项目迁入 `workspace-001-xxx`，以及在用户手动复制文件后提供重建资料索引的脚本。

**决定**：

1. 当前唯一工作区命名为 `workspace-001-goal-governance`，取自 Root Goal 的稳定目的和仓库名称。它的 canonical scope 是工作区根本身，而不是一个内部 `goals/` 子目录。
2. 每个工作区根直接包含 `workspace.md`、`goal-tree.md` 和平铺的 `GOAL-*` 文件夹；每个工作区各自拥有一个 `GOAL-001-*` Root Goal。跨工作区引用必须以稳定 `workspace_id` 和工作区内目标 ID 一起限定。
3. `docs/shared-materials/` 是所有工作区之外的共同资料根。重建脚本只生成路径、字节数和 SHA-256 的候选清单；它不自动分配业务 `material_id`、版本、用途、工作区引用或事实确认状态。
4. 当前 Web 继续只读取这个唯一的显式工作区根；多工作区动态发现、导航和 Web 操作留在 GOAL-009 的产品门禁中。
5. 旧外部仓库可被明确识别为无 workspace manifest 的 legacy `docs/goals/` 单工作区，但本仓库不保留并行旧目录或重定向副本。

**为什么**：

- 工作区成为真实的文件系统边界，可避免多个独立 Root Goal 共用一个可写目标目录。
- 将共享资料放在工作区外保留其版本固定引用边界，避免资料与任一工作区的目标状态混淆。
- 候选索引提供可核对的文件盘点，却不会把人工复制的内容伪装成已确认治理事实。

**未选方案**：

- 保留 `docs/goals/` 并在其中嵌套工作区：用户已明确否决，且会混淆全局目标根与工作区边界。
- 在 `docs/` 维护一个保存目标状态的全局工作区索引：会形成第二套生命周期真相。
- 由索引脚本自动把文件登记成固定共享资料引用：缺少用户确认的 `material_id`、版本、用途和适用工作区，违反事实准入与 fail-closed 规则。

**影响与后续**：完成迁移后，核心协议、模板、Skills、Web 默认读取路径、测试与历史证据路径必须同步；GOAL-009 的 I-009/I-010、F-003/F-004 仍保持开放，不能因目录迁移自动关闭。
