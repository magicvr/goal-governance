---
id: GOAL-019-skills-consumer-workspace-bootstrap
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 0.5.0
---

# 决策记录 · GOAL-019

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同一套 I-00N。

| ID | 级别 | 状态 | 备注 |
|----|------|------|------|
| I-001 | non-blocking | open | 消费安装形态 |
| I-002 | non-blocking | open | 是否做 install scaffold 开关 |
| I-003 | required | **closed** | D-005：slug 必须用户确认，禁止静默默认 |
| I-004 | required | **closed** | D-004 清单；实现时按表 pack/install |
| I-005 | non-blocking | deferred | standalone 全文；skills README 已标主路径 |

## D-001 · 立项：关闭「装 Skills ≠ 有治理存储」缝隙

**决定**：

设立 `GOAL-019-skills-consumer-workspace-bootstrap`，`parent: GOAL-001-main-vision`，`status: active`。范围按路线图 A→D：安装引导对齐、README 最小可运行集、S0/`01` 空仓 scaffold 语义、可选 install 脚手架与可复现证据。

**为什么**：

- GOAL-018 已交付 skills-only zip 与安装入口，但消费方仍缺「工作区真相源」落地路径。
- 另见 **D-003**：用户纠正后，核心方法论缺失同属本目标范围，不再仅收「存储 scaffold」。

**未选方案**：

- **仅改文档、不改 prompts/S0**：Windows legacy 路径与 AI 空仓行为仍会复发。

## D-002 · 产品边界（立项时草案 · **已被 D-003 修订**）

**日期**：2026-07-24  
**状态**：**superseded by D-003**

**原决定摘要**（保留供审计追溯）：曾将 `docs/architecture/*`、standalone-bootstrap 标为消费方「可选」，仅把 AGENTS + prompts + 工作区骨架标为必须。

**为何作废**：用户明确反对——核心方法论若可选，单独 Skills 适配器没有意义。见 D-003。

## D-003 · 核心方法论与 Skills 同级必备；内嵌 core 镜像 + 默认安装

**日期**：2026-07-24  
**状态**：accepted  
**用户确认**：是（会话明确指令）

### 决定

1. **产品定位**  
   - **核心方法论**（以 `docs/architecture` 中的治理元规则与工作区协议为主）与 **Skills**（prompts / 宿主入口 / install）为**同级必备**交付。  
   - 缺其一 = **不完整安装**。  
   - AGENTS 是 AI **操作细则摘要**，**不能**替代 principles / workspace-protocol 的 canonical 长文。  
   - 「无 architecture 时仍遵守 AGENTS §6b」仅作**降级兜底**，**不是**正式产品定位。

2. **交付形态（方案 A，用户选定）**  
   - **skills zip 内嵌 core 镜像**（非 dogfood、非完整 monorepo）。  
   - **`install` 默认安装** core 到目标仓库约定路径（默认：`docs/architecture/`，以及与五件套相关的 `docs/templates/` 等；精确映射见 I-004 阶段 A 清单）。  
   - 打包脚本须包含该镜像，并尽量保持与 monorepo canonical `docs/` 可核对一致。

3. **Core 必备 vs 可裁剪（原则）**  

   | 内容 | 消费方 |
   |------|--------|
   | `principles.md`（P-001～P-005） | **必备** |
   | `workspace-protocol.md` | **必备** |
   | `overview.md` / `directory-layout.md`（可去 monorepo 专有段） | **建议必备** |
   | canonical 五件套 + workspace-context 模板 | **必备**（可与现有 `skills/templates` 统一为「装到 `docs/templates`」） |
   | 精简 `docs/README` 入口 | **建议必备** |
   | `tech-stack.md` | **可裁剪**（本仓实现向） |
   | dogfood `GOAL-*` / 本仓过程树 | **禁止**进包 |

4. **仍排除**  
   - monorepo 过程数据、Web 发布物、未授权的「第二套目标状态」。

5. **与 GOAL-006 / GOAL-018 的关系**  
   - GOAL-006：**无 Skills 时**核心仍可独立复制启用（standalone）——保留为次路径。  
   - **有 Skills 的主消费路径**以本条为准：装 Skills = 同时装 core 镜像。  
   - GOAL-018 skills-only 边界**扩展**为「adapter + core 镜像、仍无 dogfood」，不重开 GOAL-018；变更在本目标交付与后续发版说明中体现。

### 为什么

- 适配器没有方法论 = 只会填表，没有可核对的治理权威。  
- 方法论没有适配器 = 人类仍可用，但 AI 闭环弱。  
- 用户现场已验证：只装 Skills、无 architecture，体验上「缺了很重要的东西」。  
- 内嵌 + 默认安装（A）比「双包靠自觉」更不易漏装。

### 未选方案

- **B：Release 双包 + 安装强校验、core 不进 skills zip**：用户未选；校验可作补充，主形态为 A。  
- **维持 D-002「architecture 可选」**：否决。  
- **把完整 monorepo docs（含 dogfood）打进 zip**：否决。  
- **只靠 AGENTS 摘要冒充核心方法论**：否决。

### 对后续实现的约束

- 精确文件清单与路径映射以 **D-004** 为准（I-004 已关闭）。  
- 改 AGENTS / skills README / prompts 时，删除或改写「architecture 整体可选」类表述，改为「必备；install 默认提供」。  
- 包内镜像根目录名在实现时固定（建议 `skills/core/`），install 按 D-004 映射到消费仓 `docs/`。

## D-004 · Core 镜像文件清单与安装映射（关闭 I-004）

**日期**：2026-07-24  
**状态**：accepted  
**用户确认**：是（会话明确清单）  
**关闭**：I-004

### 决定

消费方 skills 包内嵌、且 **`install` 默认安装** 的 core 子集如下。

#### 1. 安装到 `docs/architecture/`（必备）

| 源（monorepo canonical） | 消费仓目标 | 处理 |
|--------------------------|------------|------|
| `docs/architecture/principles.md` | `docs/architecture/principles.md` | 全文镜像（可仅修 monorepo 内链） |
| `docs/architecture/workspace-protocol.md` | `docs/architecture/workspace-protocol.md` | 全文镜像（可仅修 monorepo 内链） |
| `docs/architecture/overview.md` | `docs/architecture/overview.md` | 镜像；**去掉 / 改写 monorepo 专有段**（如本仓 `web/` 实现细节、dogfood 路径、仅维护者说明），保留「核心协议 + Skills 适配器 + 工作区真相源」逻辑架构 |
| `docs/architecture/directory-layout.md` | `docs/architecture/directory-layout.md` | 镜像；**去掉 monorepo 专有段**：不把本仓 `web/`、dogfood `workspace-001-goal-governance` 过程树、维护者-only 树当作消费方必有；改为**消费方最小树**（`AGENTS.md`、`docs/architecture/`、`docs/templates/`、`docs/workspace-<NNN>-<slug>/`、`skills/`） |

#### 2. 明确不装

| 路径 | 原因 |
|------|------|
| `docs/architecture/tech-stack.md` | 本仓实现栈，非治理元规则 |
| monorepo dogfood 目标树 / `artifacts/` / `web/` 运行时 | 过程数据或可选产品面 |
| 完整 `docs/contracts/` 作为「方法论」 | 已由 `skills/contracts/` 分发；本清单不重复进 architecture（contracts 仍随 skills 现有路径，不在本条 core 方法论集内另立） |

#### 3. 安装到 `docs/templates/`（必备）

| 源 | 消费仓目标 |
|----|------------|
| `docs/templates/goal-folder/**`（五件套 + `attachments/`） | `docs/templates/goal-folder/**` |
| `docs/templates/workspace-context.md` | `docs/templates/workspace-context.md` |
| `docs/templates/README.md` | `docs/templates/README.md`（可小幅改写，去掉「仅 monorepo 同步」口吻，说明消费仓以本目录为模板源） |

> 包内可继续保留 `skills/templates/` 作离线副本；**install 默认还要把 canonical 等价物落到消费仓 `docs/templates/`**，使无 Skills 手改时仍有核心层路径。

#### 4. 安装到 `docs/README.md`（精简 · 必备）

| 源 | 消费仓目标 | 处理 |
|----|------------|------|
| 以 `docs/README.md` 为起点的 **consumer 精简版** | `docs/README.md` | **不**整份复制 monorepo 长文。精简版须含：文档体系职责、工作区扁平规则摘要、五件套、链到 `architecture/principles` / `workspace-protocol` / `templates`、与 Skills 同级必备说明、**不含** standalone 测试/本仓 releases/dogfood 索引等维护者专节（或改为可选链接说明「维护者 monorepo」） |

包内建议路径：`skills/core/docs/README.md`（精简稿）+ `skills/core/docs/architecture/*` + `skills/core/docs/templates/*`；实现阶段可微调目录名，但 **install 落点固定为上表消费仓路径**。

#### 5. 与 D-003 的关系

- 落实 D-003「至少 principles + workspace-protocol；overview/directory-layout/templates/精简 README」的用户细化。  
- 阶段 A 实现以本表为验收清单；缺任一必备落点 = 阶段 A 未完成。

### 为什么

- 用户明确给出 core 边界，关闭 I-004，避免 pack/install 范围漂移。  
- overview / directory-layout 去 monorepo 段，避免消费仓被本仓 `web/`、dogfood 树误导。  
- 不装 tech-stack，保持方法论包干净。

### 未选方案

- **整份复制 monorepo `docs/README.md` + 全量 architecture（含 tech-stack）**：否决。  
- **只装 principles + workspace-protocol、不装 overview/layout/README**：否决（用户清单含后三项）。  
- **templates 仅留在 `skills/templates/`、不装到 `docs/templates/`**：否决（用户要求 templates 作为 core 落地）。

## D-005 · 工作区/Root slug 必须用户确认（关闭 I-003 · 阶段 B）

**日期**：2026-07-24  
**状态**：accepted  
**关闭**：I-003

### 决定

1. 空仓 S0 scaffold 时，**工作区路径 slug**（`docs/workspace-001-<workspace-slug>/`）与 **Root 英文 slug**（`GOAL-001-<root-slug>`）均须**用户明确确认**后写入。  
2. **禁止**静默使用占位名（如 `main-vision`、`example`、`default`）。  
3. 首工作区编号默认 `001`，除非用户指定其他 NNN。  
4. 已写入编排器 S0、`01` 原语、AGENTS 模板与宿主 govern wrapper。

### 为什么

- I-003 阻断阶段 B 实施；用户此前清单与 D-003/D-004 均要求消费方自定 slug。  
- 静默默认会导致跨项目同质化与错误绑定。

### 未选方案

- **包内固定默认 slug 可事后改**：否决。  
- **从仓库目录名自动推断 slug 不经确认**：否决（可作为建议展示，仍须确认）。
