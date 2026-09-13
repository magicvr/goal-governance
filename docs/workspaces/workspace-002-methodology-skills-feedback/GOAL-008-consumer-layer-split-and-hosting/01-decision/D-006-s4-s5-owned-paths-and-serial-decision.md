---
id: D-006
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-006
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-006 · S4/S5 owned paths 与串行调度判定（2026-09-13）

**状态**：accepted

**触发**：A-001 F-003（required）要求 S1 列出 S4/S5 owned paths 并决定并行或串行；[D-002 §3](D-002-a001-response.md) 已取消无条件并行，规定「写集重叠，或 S5 依赖 S4 共存模型 → **S4→S5 串行**」。

## 决定

### 1. 判定：**S4 → S5 串行**（不并行）

理由基于 I-003 盘点出的实际写入面，而不是功能名称差异：

| 判据 | 事实 | 证据 |
|------|------|------|
| 安装器入口清单重叠 | S4 要改 `AGENTS.md`/`docs/` 的写入策略，S5 要在**同一份**宿主入口清单里加入 `commit`（并区分「默认安装」与「治理必达」）——同一文件、同一函数段、同一清单 | `skills/install.sh:581-644`、`skills/install.ps1:664-739` |
| updater 托管集重叠 | 根 `AGENTS.md` 是 `managed_file_pairs` 的 fixed 托管项；S4 要把它改成段级合并，S5 要让新 `commit` 壳进入托管枚举 | `skills/update.py:156-184` |
| 契约表达位依赖 | S5 需要新增「默认安装但不入必达集」的表达位；该表达位的形状取决于 S4 是否引入宿主/治理根的安装期选择 | `docs/contracts/skills-consumer-contract.json`；`docs/tests/test_file_l1.py:101,110` |
| 机读守卫重叠 | 两阶段都会触碰「必达入口等式」断言与安装产物负例清单 | `docs/tests/test_file_l1.py:51-70`；`skills/tests/test_skills_orchestrator.py:1423-1569`；`skills/tests/test_install_ps1_isolated.ps1:37-92` |

**结论**：写集重叠 + S5 依赖 S4 的安装面决策 → 串行。不做分支并行，不设合并顺序问题。

### 2. S4 owned paths（消费仓 `AGENTS.md` / `docs/` 共存）

| 类别 | 路径 | 说明 |
|------|------|------|
| 安装器 | `skills/install.sh`、`skills/install.ps1` | 根规则文件与 `docs/` 写入策略；是否读取 `.goal-governance.json` |
| 更新器 | `skills/update.py` | `managed_file_pairs` 的根 `AGENTS.md` 托管语义、冲突 fail closed、`--force-managed` 行为 |
| 可复用先例 | `mcp/lifecycle.py` | 已实现的 managed block 合并（区间外字节不变、区间损坏 fail closed） |
| canonical（视选型） | `docs/vision/alignment.md`（MUST 表 §0.2）、`docs/architecture/workspace-protocol.md`；必要时 `docs/architecture/principles.md` | **stage 白名单**：改则同轮 stage（C6） |
| 模板/分发 | `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md` | 消费端规则面（手维，非 stage 镜像） |
| 文档 | `docs/vision/consumer-checklist.md`、`docs/standalone-bootstrap.md`、`skills/README.md` | MUST 同表要求；含 `standalone-bootstrap` 的整文件复制缺陷（S3 已收口则此处只做一致性） |
| 测试 | `skills/tests/test_install_ps1_isolated.ps1`、`skills/tests/test_skills_orchestrator.py`、`scripts/tests/test_skills_update.py`、`skills/tests/test_consumer_surface_relativeization.py` | 负例测试落点见附件 §3 |

### 3. S5 owned paths（默认 `/commit` 便利入口）

| 类别 | 路径 | 说明 |
|------|------|------|
| 新安装源 | `skills/install/{claude,grok,codex}/skills/commit/SKILL.md`、`skills/install/copilot/prompts/commit.md` | 目前**全部未实现** |
| 入口清单 | `skills/install.sh`、`skills/install.ps1` | 默认安装清单与「治理必达」清单必须分离表达 |
| updater | `skills/update.py` | 新壳进入托管枚举；与 S4 的托管语义兼容 |
| 契约 | `docs/contracts/skills-consumer-contract.json`（+ schema） | 新增便利入口表达位；**不得**写进 `hostEntrypoints` / `requiredEntrypoints` |
| dogfood | `.github/prompts/commit.prompt.md` | 既有先例；需纳入相对化守卫清单 |
| 文档 | `skills/README.md`、`docs/vision/consumer-checklist.md`、`AGENTS.md`/`skills/AGENTS.template.md` 的入口说明 | 明示便利可选、非 MUST |
| 测试 | `skills/tests/test_skills_orchestrator.py`（既有 commit 守卫 `:147-161`）、`docs/tests/test_file_l1.py`（必达等式必须仍成立）、`skills/tests/test_consumer_surface_relativeization.py` | 负例清单见附件 §3 |

**互不重叠声明**：S4 与 S5 的新增实现文件不重叠；重叠集中在安装器/更新器/契约/测试四处，正是本决定判定串行的依据。

### 4. 串行调度的执行约束

1. S4 关闭（自身审计通过、无开放 required）后才开始 S5 的实现改动。
2. S5 方案冻结时必须引用 S4 的结论（共存模型、托管语义、必达清单表达位）。
3. 两阶段各自的 canonical 改动都要在**同一提交**内完成 stage 镜像（C6），不得跨阶段攒着提交。
4. 本条判定**不**授权任何并行分支；如需改为并行，须回到本目标决策层并复算写集。

## 为什么

- A-001 F-003 的实质是「仅列条件不能充当完成的写集分析」；本决定用 I-003 盘点的具体 `file:line` 证明重叠，因此结论可被独立复核。
- 保守串行的代价是工期，收益是不产生「同一安装器被两条分支同时改写」的合并冲突与集成验证盲区；在本目标的可逆性预算内这是合理选择。
- S5 依赖 S4 的「默认安装 vs 治理必达」表达位——如果 S4 改变了入口安装策略，S5 的契约改动会全部返工。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| S4/S5 并行（各自分支） | 安装器/更新器/契约/测试四处写集重叠，且 S5 依赖 S4 的安装面决策；合并顺序与集成验证责任无法在 S1 冻结 |
| 先做 S5（`/commit`）再做 S4 | `/commit` 也要写安装清单与契约，同样与 S4 冲突；且 FB-008（宿主共存）影响面更大，先做可更早暴露 MUST 约束 |
| 把 S4/S5 合并成一个阶段 | 两者成功判据与负例集不同（宿主共存 vs 命令契约），合并会让审计 scope 与证据归属变模糊 |
| 现在就为 S4/S5 各开子目标 | 用户本轮裁决「先等 S1 结论，再按需拆」；本决定冻结的是写集与调度，是否立项在 S1 关门后单独判定 |

## 影响

- A-001/F-003 具备合法闭合依据（owned paths + 串行判定 + 执行约束）。
- 00-meta 路线图 S4/S5 行的调度说明以本决定为准；S4→S5 串行不再有「可并行」的两种读法。
- 00-meta 在 S1 关门后需记录「是否为 S2～S5 创建子目标」的判定结果（本次不拆）。
