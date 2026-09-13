---
id: E-010
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S6 收官与发布：v0.13.3 发布、资产核对与目标关门
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-010 · S6 收官与发布（2026-09-13）

## 事实

- **范围**：GOAL-008 收官——`v0.13.3` 正式发布、资产核对、目标关门。前置：[D-011](../01-decision/D-011-s6-release-scope-freeze.md)（I-006 冻结）、[A-016](../03-audit/A-016-v0.13.3-release-acceptance.md)（发布验收）、[A-017](../03-audit/A-017-goal-close-out.md)（关门审计）。
- **用户裁决**：S6 含正式发布；本轮不开残余；发版中断后裁决「停发，先修再发」（后经自查更正，见下）。

## 1. 发布事实（可核对）

| 项 | 值 |
|----|-----|
| PR | #21（`dev` → `main`），CI 双 job pass |
| merge commit | `dfa8600ae638657d084098a48f6e8c4a7457a24a` |
| annotated tag | `v0.13.3` → `dfa8600…`（tag 对象类型已核对） |
| tag workflow | run `34748891084`：`pack` success + `Publish GitHub Release (gated)` success（Environment `release` 审批 + 5 分钟 wait timer） |
| Release | `releases/tag/v0.13.3`，`target_commitish: main`，published `2026-09-13T09:11:04Z` |
| 资产 | **9 项**：两 zip + 两 sidecar + `bootstrap-README.md` + `install-online.{ps1,sh}` + `compatibility-report.json` + `release-evidence.json` |
| 摘要核对 | 全部重下载；两 zip 的 sha256 **与 sidecar 逐项一致** |
| 包内容抽查 | skills zip 内含 `agents_merge.py`、`core/docs/templates/vision/roadmap.md`、四宿主 `commit` 壳、`install.sh`（**无 BOM**）；规则面含 §6e.1 与「总路线图」映射 |

## 2. 发版中断与更正（过程留痕）

1. 首轮末：tag 已推送，tag workflow 因 runner 排队处于 queued。
2. 第二轮初：编排器误判 legacy 迁移会丢消费方内容（探针把哨兵放在**受管区间内**），据此报告缺陷。
3. 用户裁决 **停发，先修再发** → 删除远端/本地 tag；经确认 `gh release view v0.13.3` = **release not found**（从未发布、无资产）。
4. 编排器自查：真正的不变量「**区间外字节保留**」在四种形态下均成立；`agents_merge.py` **未做任何代码改动**（已恢复原状）；误判根因与控制台编码干扰见 [附件](../attachments/v0.13.3-halt-and-misdiagnosis-correction.md)。
5. 在同一 commit `dfa8600` **重新打 tag** `v0.13.3` 并推送 → workflow 全绿 → 发布并核对资产。

**净效果**：无产品代码变更；tag 对象 hash 与首次不同但指向同一 commit；从未发布过中间产物。

## 3. 附带核实的运行 provenance

`main` 上出现的 4 次 `skills-pack-release.yml` 运行均为**仓库所有者手动 `workflow_dispatch`**（该 workflow 的触发只有 `push: tags: v*` 与 `workflow_dispatch`；dispatch 默认 `publish_release=false`，只跑 `pack`，全部 success，**未创建任何 Release**）。Release 仅由 tag push 的 run `34748891084` 的 gated publish 创建。

## 4. 收尾验证

| 项 | 结果 |
|----|------|
| docs / skills / scripts | 65 / 89 / **130** 全通过 |
| 镜像 stage `--check` | 37 对 0 漂移 |
| `git diff --check` | 洁净 |
| 12 格 runtime 证据 | `--check` 12/12 |
| `compatibility_report --require-ready` | 通过 |

## 5. 关门判定

[A-017](../03-audit/A-017-goal-close-out.md)：**verdict `pass`**——成功标准 5/5 满足、开放 required = 0、信息项全部 `verified`/`closed`、发布产出可核对、愿景对齐无冲突。

**GOAL-008 → `status: done` / `progress: 100%`（S1～S6 6/6）**；`goal-tree.md` 同步。

**不随之关门**：Root `GOAL-001-methodology-skills-feedback-evolution`（R3 长期持续治理）与 VP-002；A-017 登记的 5 项后续输入保留在本目标台账。

## 检查点

- owned paths = 本目标五件套与台账、`CHANGELOG.md`、`docs/README.md`、`scripts/tests/test_agents_merge.py`、三份 S6 附件、本区 `goal-tree.md`。
- 发布相关：`docs/contracts/**`、`skills/contracts/**`、`docs/releases/runtime/v0.13.3/**` 已在前面提交中入库。
