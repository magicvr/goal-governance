---
id: GOAL-016-shared-materials-product
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
---

# 决策记录 · GOAL-016

## D-001 · 立项：X-SM（2026-07-22）

**状态**：accepted · 用户 S1（GOAL-009 D-036）。

## D-002 · 阶段 A：R-016-A 冻结（2026-07-22）

**状态**：accepted · 存储/安全/AI 读裁决。

## D-003 · 阶段 B：materials_store（2026-07-22）

**状态**：accepted · put/list/ref/delete service；refs 权威 = `shared-materials/refs/`。

## D-004 · 阶段 C：Web `/materials`（2026-07-22）

**状态**：accepted · 上传/附加/软删/下载；Web 上传不传 material_id（新建）。

## D-005 · 阶段 D：负向矩阵 + R-016-AI-READ（2026-07-22）

**状态**：accepted · 隔离扩展测；AI 读 residual。

## D-006 · 有界关门 GOAL-016（X-SM）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-016 阶段 E：阶段审与有界关门`。

**决定**：

1. 有界 close-out（A-006 阶段审 + A-007 关门）：关闭范围 = **用户 CRUD + 固定引用 + 隔离负向 + Web 入口 + 回归绿**。  
2. GOAL-016 → `done / 100%`。  
3. **接受 residual**（含既有 R-016-AI-READ）：

| ID | 残余 | 复审触发 |
|----|------|----------|
| **R-016-AI-READ** | AI 读资料运行时 | 宣称 AI 读资料产品前 |
| **R-016-E2E** | 浏览器全矩阵 / 人类多会话资料 UX | 宣称全矩阵或试点放行前 |
| **R-016-UX** | 分页/搜索/预览深度 | 扩大体验验收前 |

4. **不**因本条：I-010 全文 verified；关 R-009-X；Root done；阶段 6 终态。  
5. 复跑证据：**142 passed, 1 skipped**。

**为什么**：A–D 证据齐；剩余为 AI 读与体验全矩阵，不阻断有界资料产品表面。

**未选**：无 residual 全文关；本拍实现 AI 读。

**影响**：goal-tree；A-006/A-007；Root 子目标指向。

## D-007 · 响应 A-008：关闭 F-001～F-003（文档对齐，不重开）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 响应 GOAL-016 A-008：关闭推荐项 F-001～F-003（文档对齐，不重开）`。

**决定**：

1. **关闭 F-001**：勘误 [R-016-A §3 / §3.1 / §4](attachments/r-016-a-shared-materials-boundary.md) v1.0.1 —  
   - 产品 ref 权威 = `{DATA_ROOT}/shared-materials/refs/{workspace_id}.json`（非默认 `workspace.md` 表）  
   - protocol `source` 非本有界必交  
   - Web 追加版本 → **R-016-UX**（service 已支持 `material_id=`）  
   - `00-meta` 有界关门「不构成」与 residual 表同步  
2. **关闭 F-002**：`00-meta` 信息就绪完整 P-005 字段 + 证据指针。  
3. **关闭 F-003**：`03-audit` A-001～A-005 回填一行 verdict/证据表（A-009 节内索引）。  
4. GOAL-016 **保持** `done / 100%`；**不**重开；residual 集合不变（AI-READ / E2E / UX）。

**为什么**：A-008 independent **pass（有界）**；三项均为 recommended 文档卫生。

**影响**：A-009；R-016-A v1.0.1；goal-tree 日志。
