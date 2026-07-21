---
id: GOAL-018-skills-release-packaging
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.2
---

# 审计 · GOAL-018

## A-001 · self · 交付关门审视（2026-07-22）

| 字段 | 值 |
|------|-----|
| source | `self` |
| date | 2026-07-22 |
| scope | 目标整体 · P0～P2 四项 |
| verdict | **pass** |

### 成果

- 消费路径：Release zip → 解压 → `install.ps1`/`install.sh` 已写进 `skills/README.md` 与根 `README.md`。
- 打包：`scripts/pack_skills_release.py` 产出版本命名 zip + SHA-256；单测覆盖 temp tree 与真实 `skills/` CLI。
- 发布约定：`docs/releases/README.md` 明确正式 tag 挂载 zip + evidence。
- CI：`skills-pack-release.yml` tag 触发 pack + artifact；默认不 `gh release create`；可选 attach 需显式 gate。

### 证据

- `scripts/tests/test_pack_skills_release.py`；`scripts/tests` 全量 **41 passed, 1 skipped**。
- 可重放 CLI：`python scripts/pack_skills_release.py --version 0.0.0-testpack --output-dir <dir>`。

### Findings

无 required 未关闭项。

### 结论

有界交付完成，允许 `status: done`。真实 GitHub Release 仍属维护者授权后续动作，不阻塞本目标。

---

## A-002 · independent · 有界关门交叉审计（2026-07-22）

- **source**：`independent`
- **auditor**：GitHub Copilot（Grok 4.5）· `/audit`
- **类型**：`close-out`
- **scope**：目标整体 · P0～P2 四项交付与有界 `done / 100%` 主张；工作区 `workspace-001-goal-governance` / Root `GOAL-001-main-vision`
- **verdict**：**pass**
- **完整意见**：本节即全文（未另附 attachments）

### 范围与区间

| 项 | 核对 |
|----|------|
| 工作区 | `docs/workspace-001-goal-governance/workspace.md`：`root_goal=GOAL-001-main-vision`，`canonical_scope` 匹配；本目标在 canonical 内 |
| 共享资料 | workspace 固定引用表为空；本目标未依赖 `material_id`/sha256 关闭证据 |
| 信息项 I-00N | 五件套未登记正式 I-00N；有界范围由 D-001～D-003 与成功标准勾选表达（见 F-002 recommended） |
| 既有意见 | A-001 `self` / `pass`，无 open required |
| 边界 | 不审其他工作区；不把「未创建公开 Release」当作本有界目标必改缺口（与 D-003 / Non-goals 一致） |

### 成果（有证据 · 本轮独立重放）

| 主张 | 证据 |
|------|------|
| 消费文档 | [skills/README.md](../../../skills/README.md)「从 GitHub Release 安装」；根 [README.md](../../../README.md)「在其他项目中安装 Skills（Release zip）」；远程 `magicvr/goal-governance` 与文档 Releases 链接一致 |
| pack CLI | [scripts/pack_skills_release.py](../../../scripts/pack_skills_release.py)：版本化 zip + `.sha256` sidecar；`inventoriable_files` 强制 install 脚本 / orchestrator / contracts；排除 cache 与防御性 monorepo 路径 |
| 单测 | [scripts/tests/test_pack_skills_release.py](../../../scripts/tests/test_pack_skills_release.py)：本轮 `python -m unittest scripts.tests.test_pack_skills_release -v` → **5 passed** |
| scripts 全量 | 本轮 `python -m unittest discover -s scripts/tests -p "test_*.py" -v` → **41 passed, 1 skipped**（与 A-001 / 02-execution 一致） |
| CLI pack | `python scripts/pack_skills_release.py --version 0.0.0-testpack --output-dir <temp>` → **46 members**；SHA-256 与 zip 字节一致；成员无 `__pycache__` / `docs/workspace-` / `web/` / `artifacts/` |
| 发布约定 | [docs/releases/README.md](../../releases/README.md)：本地 pack、正式 tag 挂载 zip+evidence、CI 默认 pack-only |
| Tag CI | [.github/workflows/skills-pack-release.yml](../../../.github/workflows/skills-pack-release.yml)：`v*` + `workflow_dispatch`；pack job `contents: read`；`attach-to-release` 仅 `publish_release=true` 且 tag 且已有 Release 才 `gh release upload`（fail closed，不 create） |
| 决策边界 | D-001 skills-only；D-002 不改 release identity；D-003 有界关门不以公开 Release 为 open required |

### 对照成功标准

| 成功标准（00-meta） | 独立判定 |
|--------------------|----------|
| 五件套与 goal-tree 登记 | **满足**（文件夹 + 树/表存在且 status done） |
| README 描述 Release zip 安装 | **满足** |
| pack 产出版本化 zip + SHA-256；skills-only | **满足**（CLI 重放 + 成员检查） |
| releases README 正式 tag 挂载约定 | **满足** |
| Tag CI pack + artifact；无未授权自动发布 | **满足**（工作流文件；默认无 `gh release create`） |
| in-repo 单测；pack 与 scripts/tests 可重放 | **满足**（本轮 5 / 41+1sk） |

有界 `done / 100%` 与「未做真实公开 Release」并存，与 D-003 / Non-goals **一致**，不构成名不副实关门。

### Findings

#### F-001 · recommended · 低 · CI attach 产物名与 tag 引用不一致

- **证据**：[.github/workflows/skills-pack-release.yml](../../../.github/workflows/skills-pack-release.yml)：upload 名为 `skills-pack-${{ steps.ver.outputs.version }}`（去 `v` 的 NORM）；`attach-to-release` 首步 `download-artifact` 使用 `skills-pack-${{ github.ref_name }}`（tag 含 `v`），依赖 `continue-on-error` + 后续 `pattern: skills-pack-*`。
- **影响**：显式 `publish_release` 路径依赖回退下载；首步名对不上，运维可读性差，未来改 pattern 时易回归。
- **建议**：统一 artifact 名（全程用 NORM 或全程用 `github.ref_name`），去掉无用的失败首步。
- **门禁**：不阻断有界关门（默认 tag 路径只 pack + artifact，不走 attach）。

#### F-002 · recommended · 低 · 未单列 residual / I 表

- **证据**：`00-meta` / `01-decision` 无 I-00N 表；无 `R-018-*` residual 行；D-003 以 Non-goals 排除「未公开 Release」。
- **影响**：与仓库近期目标（如 R-009-X、R-017-HUMAN-UX）的 residual 写法不完全一致；后续维护者扫 residual 时可能漏「首次真实 tag+Release 挂载」待办。
- **建议**：可选在 GOAL-001 或后续 release 目标登记轻量 residual（例：首次 annotated tag 挂 zip+evidence+可选 attach 演练）；**非**本目标重开条件。
- **门禁**：不构成到期 required 信息项。

#### F-003 · recommended · 低 · A-001 自审结构偏薄

- **证据**：A-001 无分条 SC 对照表、无 findings 编号体系、无「与原则/工作区」核对段。
- **影响**：交叉审计成本上升；不削弱本轮独立重放结论。
- **建议**：后续关门 self 至少保留：SC 勾选证据路径 + 明确 Non-goals/residual + open required=无。

### 必改项汇总

**无 required / 必改未关闭项。**  
推荐项：F-001、F-002、F-003（均可在后续维护提交中处理，**不**要求将本目标重开为 `active`）。

### 与既有意见的异同

| | A-001 self | A-002 independent |
|--|------------|-------------------|
| verdict | pass | **pass** |
| 四项交付可验证 | 是 | 是（本轮重放确认） |
| 公开 Release 非阻塞 | 是 | 是 |
| 额外发现 | 无 | F-001～F-003 recommended only |

**无** verdict 冲突；**无**对同一必改项的一要一否（P-004 冲突门不适用）。

### 结论 + 建议给编排器/用户的下一步

1. **结论**：在声明的有界 scope（文档 + pack + releases 约定 + tag CI pack-only）内，关闭主张**成立**；`status: done` / `progress: 100%` **可维持**。
2. **编排器**（`/govern`）：汇总 A-001+A-002；可将 F-001～F-003 标为 recommended 待办或明确 defer；**禁止**因本意见改写本目标 status（除非用户另授权）。
3. **可选后续**（非本目标开门）：修 CI artifact 名；首次真实 `v*` tag 时演练 pack artifact → 维护者建 Release → 可选 `publish_release` 挂载。

### 声明

本意见 **source: independent**，**不**修改 `00-meta` 的 `status` / `progress`，**不**改 `goal-tree` 状态列，**不**改方案正文。响应、关闭 finding、推进其他目标由 **`/govern`** 处理。

---

## A-003 · self · 响应 A-002（关闭 F-001～F-003）（2026-07-22）

- **source**：`self`
- **auditor**：Grok Build · `/govern`
- **类型**：`response`
- **scope**：GOAL-018 A-002 findings F-001～F-003；维持有界 `done / 100%`
- **verdict**：**pass**
- **用户意图**：响应 A-002（F-001～F-003 recommended；维持 done；可选修 CI artifact 名）

### 意见台账摘要

| A-00N | source | verdict | 开放 required |
|-------|--------|---------|---------------|
| A-001 | self | pass | 0 |
| A-002 | independent | pass | 0（F-001～F-003 均为 recommended） |
| A-003 | self | pass | 0（本条关闭/接纳 recommended） |

**冲突**：无（双 pass，无必改对峙）。**P-004**：不适用冲突门；用户已明确指示响应方式，无需再问是否自审（本条即为 self 响应记录）。

### 成果（有证据）

| Finding | 处置 | 证据 |
|---------|------|------|
| **F-001** | **closed** | [`.github/workflows/skills-pack-release.yml`](../../../.github/workflows/skills-pack-release.yml)：`pack` job 输出 `artifact_name=skills-pack-${NORM}`；upload 与 `attach-to-release` 的 `download-artifact` 均用 `needs.pack.outputs.artifact_name`；删除错误的 `skills-pack-${{ github.ref_name }}` 首步与 pattern 回退。 |
| **F-002** | **closed（accepted residual）** | [00-meta.md](00-meta.md) 登记 **R-018-FIRST-RELEASE**（首次真实 tag+Release 挂载演练）；non-blocking；**不**重开本目标。 |
| **F-003** | **closed（process）** | 本条起确认后续关门 self 最小结构：SC 对照 + Non-goals/residual + open required=无；A-001 历史结构不回溯改写。 |

### 对照成功标准 / 门禁

| 项 | 状态 |
|----|------|
| 有界 `done / 100%` | **维持**（用户授权；A-002 亦允许） |
| 开放 required findings | **无** |
| goal-tree status 列 | **保持 done / 100%**（仅进度说明可增日志，不降级） |

### Findings

本条无新的 required finding。F-001～F-003 关闭状态见上表。

### 结论

A-002 已响应；recommended 三项均有关闭证据或 accepted residual。GOAL-018 **保持** `status: done` / `progress: 100%`。
