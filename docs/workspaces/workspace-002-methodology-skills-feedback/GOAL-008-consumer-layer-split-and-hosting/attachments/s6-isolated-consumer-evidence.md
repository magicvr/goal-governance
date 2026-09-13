---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: S6 隔离消费仓冷启动与升级实测证据
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · S6 隔离消费仓实测（2026-09-13）

> 目的：闭合 [A-006](../03-audit/A-006-s3-stage-self.md) F-001（S3 骨架复制修正未端到端演练）与 [A-008](../03-audit/A-008-s4-stage-self.md) F-001（真实消费仓升级/冷启动未实测）。
> 环境：Windows + Windows PowerShell 5.1；源包 = 本仓工作树 `skills/`；隔离目录 `%TEMP%\s6-coldstart-6d78e3`（非本仓，`git init` 后为空仓）。

## 1. 冷启动骨架复制（按 `docs/standalone-bootstrap.md` §2.3 修正后的步骤）

| 步骤 | 命令 | 观察结果 |
|------|------|----------|
| 复制愿景树骨架 | 组合编排索引改为复制 `docs/templates/vision/roadmap.md`（**不再整文件复制生产仓 `roadmap.md`**） | `roadmap.md` 含**模板占位行** `VP-001-example-intent`；**不含**生产仓 `VP-004`；含投影标注 `派生投影` |
| 复制 reviews 索引 | `templates/vision/reviews-index.md` → `docs/vision/reviews.md` | 成功 |
| 手写最小 Charter | `vision-demo@0.1.0`，`status: active` | 成功 |
| 消费方自有根规则 | 预置 `AGENTS.md` = `# Consumer-owned rules …` | 安装前已存在 |

**结论**：S3 的骨架复制修正**在真实隔离仓生效**——生产仓 VP 行（VP-004 等）**不再泄漏**进消费仓组合编排索引；这正是 S1 盘点 §2.B「消费侧风险」所指缺陷的端到端反证。

## 2. 冷启动安装（`install.ps1 -Claude -NonInteractive`）

| 检查项 | 结果 |
|--------|------|
| 根 `AGENTS.md` 消费方自有内容保留 | **True**（文件仍以 `# Consumer-owned rules` 开头） |
| 受管标记块写入 | **True**（`goal-governance:begin managed` 与 `end managed` 均在） |
| 四治理入口落盘 | `.claude/skills/` = `audit, commit, govern, vision, vision-audit` |
| 便利入口 `/commit` 落盘（S5） | **True**（`.claude/skills/commit/SKILL.md`） |
| core 方法论落盘 | **True**（`docs/architecture/principles.md` 存在） |
| 既有 `docs/vision/roadmap.md` 未被生产仓行覆盖 | **True** |

### 2.1 观察到的一个 fail-closed 停止点（非缺陷，登记为行为边界）

安装进行到 `docs/vision/` 时**中止**：

```text
Error: Refusing directory overwrite in non-interactive mode (use -Force): …\docs\vision
```

原因与含义：

- 消费仓**预先存在** `docs/vision/`（本测试按 §2.3 先建了骨架），安装器在非交互模式下**拒绝覆盖目录**（`install.sh:196-197` / `install.ps1:229-231` 的既有策略）。
- 这是**有意保守**：框架不会静默覆盖消费方已有的愿景树；`AGENTS.md` 的标记块合并**已完成**（输出 `Merged managed block` 在错误之前）。
- 代价：消费方若已自建 `docs/vision/`，非交互安装会在该点停下，须显式 `-Force`/`--force` 或改治理根才能继续。
- **未**在本轮修正（不属 S4 用户裁定范围）；登记为后续项（与「可配置治理根」候选 C 同域）。

## 3. 升级路径实测（`update.py` 的重放语义）

`update.py` 的行为是「备份 → 换包 → 以 `--all --non-interactive --force` 重跑安装器」（`skills/update.py:248-283`），因此本测试直接重放该调用：消费仓保留，替换为**另一份包副本**（`%TEMP%\pkg-new-bfa135\skills`）并再次 `-Claude -NonInteractive -Force`。

| 检查项 | 结果 |
|--------|------|
| 第二次安装对根 `AGENTS.md` 的输出 | `Already present (managed block unchanged)`（**幂等**，未重写） |
| 消费方自有规则仍在文件开头 | **True** |
| 受管标记块数量 | **1**（未重复追加、未嵌套失控） |
| 四个治理入口 + `/commit` | 全部 `Already present`（字节一致时不重写） |
| core 方法论重放 | `docs/architecture/`、`docs/templates/`、`docs/vision/` 重新落地（带 `-Force` 时按更新语义覆盖框架文件） |

**结论**：S4 的「区间外字节永不被改写 + 区间幂等」在**真实升级重放**下成立；消费仓自有规则在两次安装后均保留。

## 4. 与验收阈值的对应

| 阈值（[验收矩阵](../attachments/s1-acceptance-matrix.md)） | 本轮证据 |
|-----------------------------------------------------------|----------|
| S3 ④ 两处漂移修正 | 已在 S3 静态核对；本附件补充消费侧「不再泄漏生产仓 VP 行」的端到端证据 |
| S3 ⑤ 骨架复制不再带入生产仓 VP 行 | **满足**（§1） |
| S4 负例 1「消费仓已有自有 `AGENTS.md`」 | **满足**（§2） |
| S4 负例 5「受管文件被改动后的行为」 | **满足**：升级重放下根 `AGENTS.md` 幂等且消费方内容保留（§3）；区间被人工改写的 fail-closed 分支由 `scripts/tests/test_agents_merge.py` 覆盖 |
| S4 负例 9「同包重复安装幂等」 | **满足**（§3：`Already present (managed block unchanged)` 与逐文件 `Already present`） |
| S5 阈值 ① 已支持宿主可调用 | 落盘层面满足（§2、§3）；**真实宿主调用**仍待 A-009 F-001 闭合 |

## 5. 未完成部分（诚实登记）

- **宿主 CLI 真实调用未跑**：`/commit` 与四入口的宿主行为证据属 A-005 F-001 / A-009 F-001，需在 S6 cross 回归中单列捕获（`scripts/capture_runtime_evidence.py` 的 `--entrypoint` 目前只接受四入口，便利入口需以独立标记处理以免污染必达矩阵）。
- **runtime 证据重捕获未跑**：`docs/releases/runtime/` 的 12 份矩阵证据在 S2/S4 规则面变更后过期（A-005 F-002），必须在 I-006 冻结的 revision 上重捕获。
- **I-006 未冻结**（A-001 F-005）：版本、tag/revision、资产清单、回归矩阵、cross 覆盖面与证据归属仍待冻结。

## 6. 复现命令

```powershell
$t = Join-Path $env:TEMP ("s6-coldstart-" + [guid]::NewGuid().ToString("N").Substring(0,6))
New-Item -ItemType Directory -Path $t | Out-Null
Push-Location $t; git init -q; Pop-Location
New-Item -ItemType Directory -Path (Join-Path $t 'docs/vision') -Force | Out-Null
Copy-Item '<repo>\docs\templates\vision\roadmap.md' (Join-Path $t 'docs/vision/roadmap.md')
Copy-Item '<repo>\docs\templates\vision\reviews-index.md' (Join-Path $t 'docs/vision/reviews.md')
Set-Content (Join-Path $t 'AGENTS.md') "# Consumer-owned rules`n" -Encoding UTF8
Copy-Item -Recurse '<repo>\skills' (Join-Path $t 'skills')
# 冷启动（首次会在 docs\vision 处 fail closed；加 -Force 表示消费方同意覆盖框架文件）
Push-Location $t; & (Join-Path $t 'skills/install.ps1') -Claude -NonInteractive -Force -SkillsDir (Join-Path $t 'skills'); Pop-Location
Get-Content (Join-Path $t 'AGENTS.md') -Raw   # 期望：消费方规则在前 + 唯一受管标记块
# 升级重放（等价于 update.py 的 --all --non-interactive --force）
Copy-Item -Recurse '<repo>\skills' (Join-Path $env:TEMP 'pkg-new\skills')
Push-Location $t; & (Join-Path $env:TEMP 'pkg-new\skills\install.ps1') -Claude -NonInteractive -Force -SkillsDir (Join-Path $t 'skills'); Pop-Location
# 期望输出：Already present (managed block unchanged): ...\AGENTS.md
```
