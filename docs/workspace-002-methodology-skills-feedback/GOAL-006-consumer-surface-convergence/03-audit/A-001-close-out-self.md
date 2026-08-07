---
id: A-001
goal: GOAL-006-consumer-surface-convergence
doc: audit
title: S3 关门审计（self · 协议正文相对化 + I-002 兼容面 + F-006/R-001 关闭）
status: recorded
source: self
date: 2026-08-08
scope: GOAL-006 全目标关门：S1 方案冻结（D-001）→ S2 实施（相对化/测试/矩阵证据刷新）→ S3 验收；成功标准 1–5；I-001 closed 复核、I-002 兼容面验收；F-006/R-001 关闭留痕
audit_type: close-out
verdict: pass
version: 0.1.0
---

# A-001 · GOAL-006 S3 关门审计（2026-08-08）

## 结论

**verdict: `pass`**（self）。消费面路径收敛按 D-001（A+C 混合）完整实施并经独立核验：

- **相对化正确性**：prompts（8）/ AGENTS.template（占位 `{{GOVERNANCE_ROOT}}` + 使用说明）/ lifecycle / 安装形态（install 19 + dogfood 17）/ canonical 扫尾（3）——无裸 `docs/` 残留（防再犯测试 `test_consumer_surface_relativeization.py` 固化；canonical 仅保留目录树/标题/物理路径，经协议前缀断言放行）。`install.sh/ps1`、`update.py` 的物理安装路径与 `core/docs` 包内路径按执行判断保留（相对化失真）。
- **门禁**：全量 **239 passed**（+5 防再犯，既有断言按相对化语义更新）；stage `--check` 36 对 0 漂移；矩阵引用 08-08 证据经 `generate_report` 校验一致（12/12 重捕获 pass，prompt 字节级同源）。08-06 历史发布快照 stale 为**预期**（绑定发布时点树；M-001 `--check` 显式检出，不改写历史）。
- **I-002（兼容面）closed**：无运行时/契约变更；v0.13.0 发布 zip 未重打包；`{governance_root}` 默认 `docs` 与旧 `docs/` 语义等价；物理安装路径（`$TARGET_DIR/docs`）未动 → 已安装消费仓不回滚、不破坏（成功标准 4 成立）。
- **成功标准 1–5 全部满足**（5：F-006/R-001 关闭留痕，见「结论状态」）。
- 无 required finding；无冲突。

## 范围与区间

| 项 | 内容 |
|----|------|
| 目标 | GOAL-006-consumer-surface-convergence（active → 建议 done） |
| 工作区 | workspace-002-methodology-skills-feedback（显式 · active） |
| S1 | E-002 盘点（14 文件约 240 处 + S2 补入安装形态 150 处 ≈ 390 处）→ D-001 方案冻结（A+C 混合，用户确认）→ I-001 closed |
| S2 | E-004 实施（相对化 + 防再犯测试 + 12 宿主证据重捕获 + matrix cells 刷新 + stage ×3） |
| S3 | 本审：验收 + I-002 + 关闭留痕 |

## 成果（有证据）

| 项 | 证据 |
|----|------|
| 相对化实施 | E-004 事实表 + 防再犯测试（5 条，239 绿） |
| 模板占位语义 | `skills/AGENTS.template.md` 使用说明（`{{GOVERNANCE_ROOT}}`：默认 docs、可配置、仓外 fail closed） |
| 矩阵证据刷新 | `docs/releases/runtime/v0.13.0/*-2026-08-08.json` ×12（capturedAt 2026-08-08；pass）；matrix cells 引用更新 |
| stage 同步 | `skills/core/docs/architecture/{overview,directory-layout}.md`、`skills/contracts/*` 镜像随提交；`--check` 0 漂移 |
| I-002 验收 | E-004 执行判断 1 + 无 zip 重打包 + 物理路径未动 |

## 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 1. 模板/prompts 无裸 `docs/` | ✅ | 防再犯测试 + 残留扫描 |
| 2. 展开链路一致 + `governance_root≠docs` 测试覆盖 | ✅ | 字面断言固化；install 物理路径保留判断留痕（E-004） |
| 3. 全量测试绿 + stage 0 漂移 | ✅ | 239 passed / 36 pairs |
| 4. 已安装消费仓不回滚 | ✅ | I-002 closed（见上） |
| 5. F-006/R-001 关闭留痕 | ✅ | 本审结论状态 + workspace-003 台账 / VP-002 路线图更新（合并响应轮执行） |

## Findings

无 required。建议（recommended，非阻断）：

- **R-001**（low）：`docs/releases/runtime/v0.13.0/*-2026-08-06.json` 历史快照与当前树 stale 属预期，但建议下一次 release 轮把 matrix `candidateRevision` 与 evidenceScope 一并刷新（本 S2 已刷新引用，candidateRevision 仍为 v0.13.0）。
- **R-002**（low）：防再犯测试目前覆盖字面层；`governance_root≠docs` 的**消费场景端到端**（如模拟 install 到非 docs 根）可随 VP-002 后续波次补强（I-002 已验收语义等价，非阻断）。

## 必改项汇总

无。

## 结论 + 建议

- 建议 **GOAL-006 → `done`**（progress 67% → 100%，S1/S2/S3 3/3；等权），goal-tree 同步；Root R3 不自动关门。
- 建议合并响应轮（A-003）执行：F-006/R-001 关闭留痕（[workspace-003] Root 03-audit 结论段 + VP-002 消费面承接路线图登记更新）。
- 本审为 self；按用户指令，独立审计由 grok build（grok-4.5 / thinking high）执行后由编排器合并响应。

## 声明

本意见不修改 status/progress；响应由 `/govern` 合并处理。独立审计将追加 A-002（source: independent）。
