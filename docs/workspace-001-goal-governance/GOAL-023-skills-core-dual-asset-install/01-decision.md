---
id: GOAL-023-skills-core-dual-asset-install
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.2.0
---

# 决策记录 · GOAL-023

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同一套 I-00N。I-001～I-004 已由 **D-002** 关闭。

## D-001 · 立项与产品裁决固化（2026-07-30）

**状态**：accepted  
**确认来源**：用户书面裁决 + 要求「构建新目标、必要时拆阶段子目标、准备开始实现」

### 决定

1. **新建** `GOAL-023-skills-core-dual-asset-install`，`parent: GOAL-001-main-vision`，`status: active`。
2. **双资产（扩展分发，不削弱一体安装）**  
   - **提供**独立 **核心方法论资产**（core-only zip + digest）。  
   - **同时** **skills 资产仍内嵌** core 镜像（GOAL-019 D-003 / D-004 不变）。  
   - 消费方使用 **包内 install** 时：**不需要**再从网络拉取 core；离线完整安装仍为一等公民。  
3. **双安装入口**  
   - **入口 1 · 在线 bootstrap**：README / Release 提供的安装脚本（下载 skills 包 → 校验 → 调用包内 install）。  
   - **入口 2 · 包内脚本**：既有 `skills/install.ps1` / `skills/install.sh`（解压后本地执行）。  
4. **在线路径下载对象**：默认下载 **已内嵌 core 的 skills zip**（及 `.sha256`），**不是**「只下 skills 再另拉 latest core」。  
5. **core-only 资产用途**：standalone / 无 Skills 场景、与 monorepo `docs/` 可核对的方法论快照、Release 并列挂载；**不**替代 skills 默认安装路径上的内嵌 core。  
6. **明确非目标（本目标）**  
   - 默认 `always latest` 无版本锁的在线热更；  
   - 拆掉 skills zip 内 core、迫使 install 必须联网；  
   - 静默覆盖消费仓已修改的 `docs/architecture` / templates（升级策略若出现须另决策 + 用户确认）；  
   - Marketplace、自动推 tag、未授权 GitHub Release；  
   - 改 Root / Charter / VP status。  
7. **纲领阶段 A→F**；子目标默认不预建，A 后按需拆。  
8. **与历史决策关系**  
   - GOAL-019 D-003 **方案 A（内嵌）维持为主安装形态**。  
   - 会话中讨论的「强化 B（双包 + 强制组装）」**不**采用为默认消费路径；本目标是 **A + 附加 core-only 资产 + bootstrap UX**。  
   - GOAL-022 stage 仍为镜像生成机制。

### 为什么

- 内嵌 core 已验证可避免「只装适配器、缺方法论」。  
- 独立 core 资产补齐 standalone 与「只要方法论」的分发，无需强迫 clone monorepo。  
- 在线 bootstrap 消除手工「下 zip → 解压 → 改名 → 再 install」摩擦，且仍落到同一包内 install 逻辑。  
- 避免 online latest core 带来的版本错配与气隙失败。

### 未选方案

| 方案 | 未选原因 |
|------|----------|
| skills 不含 core，install 时拉 latest core | 用户明确否决；与离线完整安装冲突 |
| 仅文档说明、不提供 bootstrap | 体验缺口仍在 |
| 仅 core-only、取消 skills 内嵌 | 回退 D-003，漏装风险上升 |
| 开发仓 git 去镜像 + 本目标一并做 | 可 follow-up；非本目标必需，GOAL-022 仍提交镜像 |

### 对后续实现的约束

- pack skills 路径：**不得**因本目标删除 zip 内 `core/`。  
- bootstrap：**必须**校验 digest（至少 sha256）；失败 fail closed。  
- 测试：bootstrap 须有**不依赖公网**的 fixture 路径（本地 zip）。  
- 版本：同一次 release 的 skills zip 与 core-only zip 应对齐同一 `version` 字符串（I-001/I-004）。

## D-002 · 阶段 A 方案冻结（接受推荐默认 · 2026-07-30）

**状态**：accepted  
**确认来源**：用户书面「接受推荐默」（接受推荐默认）

### 决定

| ID | 决议 | 关闭 |
|----|------|------|
| **I-001** | core-only 文件名：`goal-governance-core-v{version}.zip`；归档根目录同名；sidecar `….zip.sha256`（GNU 风格一行 digest） | **closed** |
| **I-002** | 在线 bootstrap **默认**等价包内 `-All` / `--all`（四入口 + core→docs）；可用 flag 收窄宿主 | **closed**（阶段 C 实现约束） |
| **I-003** | bootstrap 脚本 **Release 附件为主**；README 使用 **annotated tag 固定 URL**（非漂浮 branch raw） | **closed**（阶段 D/E） |
| **I-004** | 同 `version` 下 core-only 每个成员须与 skills zip 内 `core/` **字节一致**（同源 stage）；单测 `assert_core_subset_of_skills_core` | **closed**（策略）；实现断言在阶段 B |

### 实现顺序（冻结后）

1. **B**：`scripts/pack_core_release.py` + 单测（含 I-004 子集一致性）  
2. **C**：在线 bootstrap（默认下 **skills** zip，内嵌 core；不另拉 core）  
3. **D**：双入口文档  
4. **E**：CI/Release 挂 core zip + bootstrap + 既有 skills zip  
5. **F**：回归关门  

### 未选方案

- core zip 与 skills 使用不同 version 字符串（增加错配面）  
- bootstrap 默认只装单宿主（与包内默认四入口不一致）  
- 仅 raw main 分支 URL 作权威安装入口（不可复现）
