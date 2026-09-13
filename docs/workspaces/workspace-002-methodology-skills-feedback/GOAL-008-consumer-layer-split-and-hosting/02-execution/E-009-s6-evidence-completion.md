---
id: E-009
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S6 补做证据、PR #21 与 CI 缺陷修复
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-009 · S6 补做证据与 PR 阶段（2026-09-13）

## 事实

- **触发**：用户选择「先完成三项证据」（A-013 指出的缺口），随后选择「推进：推送 + 开 PR」。
- **关联**：[D-011](../01-decision/D-011-s6-release-scope-freeze.md)（I-006 冻结）、[A-013](../03-audit/A-013-independent-s6-close-review.md)（独立关门复审）、[A-014](../03-audit/A-014-response-a013.md)（响应）、[A-015](../03-audit/A-015-s6-stage-self.md)（S6 自审）。

## 1. 三项证据补做

| # | 交付 | 产物 |
|---|------|------|
| 1 | **层语义 CE1–CE10 双宿主探针**（Claude `2.1.270` + Grok `1.0.30`） | [attachments/layer-semantics-host-probe.md](../attachments/layer-semantics-host-probe.md)；原始输出 `attachments/probes/layer-semantics-{claude,grok}.txt` |
| 2 | **`/commit` 宿主实测**（Claude 正例 + fail-closed 负例 + 权限不足负例） | [attachments/commit-entry-host-evidence.md](../attachments/commit-entry-host-evidence.md) §1；原始输出 `attachments/probes/commit-{positive,failclosed}-claude.txt` |
| 3 | **隔离仓 legacy 核对**（缺列 / 他仓遗留行不改写、不阻断、不构成「不完整安装」） | 同上 §2 |

判定：A-005 F-001/F-002、A-006/A-008 F-001、A-009 F-001 全部 **`fixed`**（残余已具名：探针标签噪声、`/commit` 仅单宿主实测）。开放 required 由 4 降为 **1**（A-001 F-005 发布产出）。

## 2. 推送与 PR

- `git push -u origin dev`（此前 `dev` 无上游）；`gh pr create --base main --head dev` → **PR #21**。
- PR 描述含变更概要、验证结果、审计状态与 merge 后发布步骤。

## 3. CI 抓出的两个跨平台缺陷（本地不可见）

| # | 缺陷 | 根因 | 修复 |
|---|------|------|------|
| 1 | `install.sh` 以 `\ufeff#!` 开头，下载后 shebang 失效 → 自举安装失败 | S4 期间用 Windows PowerShell `Set-Content -Encoding utf8` 改写安装器，写入 UTF-8 BOM | 去除两个安装器的 BOM；新增 `test_installers_ship_without_utf8_bom` 防再犯（`af9f079`） |
| 2 | Git Bash 下 `python3.exe: can't open file 'C:\tmp\...\agents_merge.py'` | Git Bash 传 POSIX 路径（`/tmp/...`），原生 Windows Python 打不开 | `install.sh` 新增 `native_path()`，在 MINGW/MSYS/CYGWIN 下用 `cygpath -w` 转换 helper/source/target 三处路径（`de7fd31`） |

细节与教训见 [attachments/pr21-ci-defects.md](../attachments/pr21-ci-defects.md)。

## 4. 验证结果

| 项 | 结果 |
|----|------|
| CI（run `34748262249`） | `contract-and-report` **pass**（1m3s）· `windows-install-surface` **pass**（2m3s） |
| 本地 | docs 65 OK · skills 44 OK · scripts 128 OK（skipped=4）· 镜像 37 对 0 漂移 · `git diff --check` 洁净 |
| 发布门禁（本地） | `compatibility_report.py --require-ready` 通过 · release rehearsal 通过 |
| PowerShell 隔离安装 | PASS |

## 5. 仍待完成（不得以残余关门）

- **merge PR #21 到 `main`**（需用户确认；merge 后 `main` = 发布 revision）；
- **annotated tag `v0.13.3` 指向 merge commit**；
- **tag workflow**（`skills-pack-release`，Environment `release` 审批 + wait timer）；
- **Release 资产逐项核对**（重下载比对 sha256）；
- 之后 A-001 F-005 方可判闭合、GOAL-008 方可评估关门。

## 检查点

- owned paths = 四份探针原始输出、三份 S6 附件、`00-meta.md`、`02-execution.md`、`03-audit.md`、`skills/install.sh`、`skills/install.ps1`、`skills/tests/test_skills_orchestrator.py`。
- 未使用 `git add -A`（`git add` 均为显式路径；一次 `git add docs/... goal-tree.md` 为目录级显式路径）。
