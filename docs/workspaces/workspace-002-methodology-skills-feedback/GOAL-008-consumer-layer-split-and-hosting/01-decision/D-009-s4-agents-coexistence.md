---
id: D-009
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-009
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-009 · S4 共存模型裁决：AGENTS.md 受管标记块（2026-09-13）

**状态**：accepted

**触发**：S1 盘点（I-003）列出消费仓 `AGENTS.md` / `docs/` 的硬碰撞与候选共存模型 A～E；[A-004](D-004-s1-inventory-acceptance.md) F-001 把「选型」登记为 required，阻断 S4 方案冻结。用户于本轮书面裁决两项。

## 决定

1. **共存模型 = A（标记块合并）**（用户裁定）：
   - 消费仓**拥有**根 `AGENTS.md`；框架规则位于受管区间 `<!-- goal-governance:begin managed -->` … `<!-- goal-governance:end managed -->` 之内。
   - **区间外字节永不被安装/更新改写**：消费方可把自有 agent 规则与框架规则放在同一文件。
   - 标记块语义与既有 **MCP 薄壳**（`mcp/lifecycle.py`）**收敛为同一契约**（同名标记、区间外不变、区间损坏 fail closed），消除「File 通道与 MCP 通道两套合并逻辑」的既存分裂。
   - 迁移兼容：安装前已是「本包规则整份副本」的仓，迁移后**内容等价**（规则进入受管区间），不丢消费方内容；消费方已自建 `AGENTS.md` 时**追加**受管区间，不覆盖。
2. **本轮 docs/ 维度只做现状 + 共存说明**（用户裁定）：治理根默认仍为 `docs`，安装面不再改动其归属；「安装器读取 `.goal-governance.json` 实现可配置治理根」（候选 C）**不在本轮范围**，登记为后续项。
3. **实现面**：安装器（bash/PowerShell）与 updater 不再把根 `AGENTS.md` 当作「完全托管文件」；统一走共享合并实现 `skills/agents_merge.py`（Python，安装器与 updater 共用）。
4. **fail closed 边界**：
   - 标记块半写（只有 begin 或只有 end、或 end 在前）→ 拒绝合并并报错；
   - Shell 安装器在**无 Python** 且目标 `AGENTS.md` 已存在且内容不同时 → **拒绝覆盖**并报错（不静默覆盖消费方规则）；目标不存在时写整份文件并标注「无 Python，未做标记块拆分」；
   - updater：受管区间被人工改写 → 仍走既有 `managed files have local changes` / `--force-managed` 路径（只替换区间）。
5. **不在本轮**：`docs/` 归属可配置化、大小写碰撞（`agents.md`）、只读目标回滚、updater 点文件、卸载路径——均保持 [A-004](../03-audit/A-004-s1-stage-self.md) 与盘点清单中的 open 状态。

## 为什么

- 候选 A 复用仓库**已有**的区间合并实现与测试先例（MCP 通道），风险最低、改动面最小，且直接满足 FB-008「消费仓可在兼容治理框架的前提下维护自有规则」。
- 候选 C（可配置治理根）会同时改动安装器、updater、scaffold 路径与一致性检查，属独立交付面；用户选择先只解决 `AGENTS.md` 这一最硬的碰撞。
- 把合并实现放进一个 Python 模块，避免 bash / PowerShell / updater 三处各写一套（A-003 F-003 已警告写集重叠导致的集成盲区）。
- 「无 Python 时不覆盖」比「无 Python 时照旧整份覆盖」更符合 C7（消费仓兼容优先于形式洁癖）。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| B 命名空间子目录 + 根薄指针 | 宿主自动加载只认根 `AGENTS.md`，指针丢失即断链；且需一次性拆分已装仓 |
| C 可配置治理根 | 写集与测试面显著更大（安装器 + updater + scaffold + 一致性检查）；用户本轮明确只做 AGENTS.md |
| D 安装时显式选择 | 需持久化并重放选择，分支 × 双通道矩阵膨胀 |
| E 不写根 `AGENTS.md` | 触碰完整安装 MUST「规则入口」行，治理摘要失去默认载体 |
| 保持「整份覆盖 + --force」 | 正是 FB-008 的痛点；消费方规则无合法存放位置 |

## 影响

- 新增 `skills/agents_merge.py`（共享合并实现 + CLI）。
- `skills/install.sh`：新增 `merge_agents_file` / `same_content`、Python 探测、`copy_file` 复用 `same_content`；两处 `AGENTS.md` 安装点改为合并。
- `skills/install.ps1`：新增 `$script:PythonBin` 探测与 `Merge-RuleAgentsFile`；两处安装点改为合并。
- `skills/update.py`：`managed_file_pairs` **移除**根 `AGENTS.md`；新增 `agents_managed_conflict` / `merge_root_agents`；换包前尝试把 legacy 整份安装迁入标记形态。
- 规则源面 `skills/{AGENTS.template.md,install/claude/AGENTS.md,install/copilot/copilot-instructions.md}` 增加**外层标记**（包裹整份规则；文件内部原有的规则级标记对作为嵌套保留），使合并能区分「框架规则」与「消费方内容」。
- 新增 `scripts/tests/test_agents_merge.py`（12 例）。
- 未新增 MUST；未改 `docs/` 归属；`.goal-governance.json` 仍未接入安装器（登记为后续项）。
