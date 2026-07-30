---
id: GOAL-021-skills-release-chain-hardening
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
---

# 决策记录 · GOAL-021

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同一套 I-00N。I-001 / I-002 已由 D-002 关闭；I-003 发版不在本目标默认交付。

## D-001 · 立项：执行链对抗审主台账 + 同轮落盘 A-001（2026-07-30）

**决定**：

1. 新建 `GOAL-021-skills-release-chain-hardening`，`parent: GOAL-001-main-vision`，status `active`。
2. **正式审计意见主落点**为本目标 `03-audit.md`；**不**向已 `done` 的 GOAL-008 / 018 / 019 / 020 追加本轮 required。
3. 立项当轮将用户提供的执行链对抗审以 **A-001 / `source: independent`** 写入本目标（阶段 A 完成）；**不**因 A-001 自动改 status 为 done，也**不**在本轮自动执行 B～F 代码/文档修复（除非用户下一条明确「直接修」）。
4. 纲领阶段按建议修复顺序：**B core mirror → C 运行证据 → D 打包 symlink → E P-006 验证器 → F 安装/工作区可复现 → G 回归关门**。
5. 本目标定位为路径 D 下 **Skills 分发/证据/门禁质量** 单点工作；**不**重开阶段 7；**不**宣称 Root 终态；**不**授权 tag/Release。

**为什么**：

- 4×P1 直接影响「可否发布新 Skills 包 / 运行证据是否充分」；需要独立生命周期与可追踪 findings，而非散落在 Root 维护笔记。
- 已关门目标不宜死后追加 required（P-003 / 历史关门语义）。
- 用户本轮意图明确：在工作区 001 **开启新目标处理该审计意见**。

**未选方案**：

- **挂 GOAL-018/008 追加 A-00N**：污染已关门目标。
- **只修不立项**：缺少台账与门禁，易与路径 D 发版叙事缠在一起。
- **立即拆 5 个子目标**：违反 P-001——先本目标纲领，阶段内并行改文件即可。
- **本轮直接全量修完**：用户要求先「开启目标处理意见」；写入指令覆盖到立项 + 落盘，修复等待确认或下一条 `/govern`。

**确认来源**：用户 `/govern` 指令「在工作区001开启一个新的目标，处理下述审计意见」+ 完整审计正文。

## D-002 · 按 A-001 建议顺序 fixed F-001～F-005（2026-07-30）

- **状态**：accepted

**决定**：

1. 用户明确指令「按 GOAL-021 A-001 建议顺序修 F-001～F-005」→ 同轮实施 B～F，全部走 **`fixed`**（不 residual / 不 overruled）。
2. **F-001**：同步 `skills/core/docs/templates/README.md` 至 canonical `0.6.0`；在 skills 测试中增加 core mirror **全文件 hash** 一致性（templates + architecture，排除 tech-stack）。
3. **F-002**：运行证据采用断言策略 **`marker+entrypoint+nontrivial-stdout@1`**（exit 0 + marker + entrypoint 出现在 stdout + 非 marker 的 nontrivial 内容）；payload 写入 `assertions`/`assertionPolicy`；兼容性报告 **重算** stdout，不信任仅摘要/`verdict: pass`；**marker-only 必须 fail**。历史无 `assertions` 的 evidence 走 legacy 等价门禁（entrypoint + nontrivial），避免立即作废全部既有 capture。
4. **F-003**：`pack_skills_release.inventoriable_files` 拒绝 symlink，并对 `resolve()` 做 skills 根 containment；单测在可创建 symlink 的环境断言，Windows 无权限时 skip。
5. **F-004**：`validate_charter(..., require_active=True)` 用于当前栈；工作区对齐 **删除** `require_plans=False`；每个 `plan_ref` 调用 `validate_vision_plan` 校验 `vision_ref`；工作区结构校验拒绝空 `id`，并支持 `require_root_on_disk` 验证真实 Root。
6. **F-005**：`install.sh` / `install.ps1` 增加 `--force` / `--non-interactive` / `--dry-run`（及 PS 等价开关）：非交互遇到覆盖 **fail**（除非 force）；dry-run 只打印不写盘。
7. **不**授权 tag/Release；阶段 G 自审/关门另拍。
8. I-001 / I-002 以本决策关闭。

**为什么**：审计顺序已写清；用户一次授权全量 fixed，避免逐 finding 往返。Legacy 兼容路径保留历史 matrix 可验证性，同时堵住「仅 marker」与「信任 stored observed」两条洞。

**未选方案**：只修 P1 留下 F-005；用 GG_RUNTIME_ASSERT 强制所有宿主立刻改探针文案（会立即作废 12 格历史 evidence）；schema 强制 pass 必须含 assertions（同上）。

**确认来源**：用户 `/govern 按 GOAL-021 A-001 建议顺序修 F-001～F-005`。

## D-003 · 接受 A-003 并确认 GOAL-021 关门（2026-07-30）

- **状态**：accepted

**决定**：

1. 接受 A-003 `self / close-out / pass`，将 GOAL-021 从 `active` 改为 **`done`**；派生 progress **100%**（A～G 7/7）。
2. F-001～F-005 保持 `fixed`；开放 required = 0。
3. I-003 关闭为 **out of scope**（本目标不授权 tag/Release）；发版 follow-up 记为 residual **R-021-RUNTIME-RECAPTURE**（非阻断）。
4. **R-021-SYMLINK-CI**：Windows 本机 symlink 动态负例 skip 接受为 non-blocking residual（实现已落地；Ubuntu pack 路径仍是真实风险面且逻辑已拒 symlink）。
5. 本次**不**强制独立 `/audit` 复审（用户选择 self 自审并确认关门）；未来仍可只读复审。
6. **不**改 Root/Charter/VP status；**不**开启阶段 7；**不**自动 tag/Release。

**为什么**：成功标准已全部可核对；A-003 核对 required=0、到期 required I=0、回归绿、产物路径可指回。用户指令「阶段 G 自审并确认关门」为书面确认。

**未选方案**：先独立复审再关门；保持 `active / 100%`；借关门宣称可发版或 Root done。

**确认来源**：用户 `/govern GOAL-021 阶段 G 自审并确认关门`。
