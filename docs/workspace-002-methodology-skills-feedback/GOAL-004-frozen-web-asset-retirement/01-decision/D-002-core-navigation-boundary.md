---
id: GOAL-004-frozen-web-asset-retirement
doc: decision-entry
record_id: D-002
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.3.0
---

# D-002 · 响应现行 core 导航引用并精化保护边界

## 新发现

S2 的全仓主动引用扫描确认：`docs/architecture/overview.md` 与 `directory-layout.md` 仍把本仓 `web/` 描述为现行路径；两者属于 stage 白名单并镜像到 `skills/core/docs/architecture/`。若只删除资产而保持这两份现行导航不变，会留下失效路径和错误仓库架构。

## 决定

1. 窄幅精化 D-001 与 workspace-001 D-029 的“core/Skills 不改”保护表述：**方法论语义和行为资产不改**，但允许修正两份现行导航的仓库事实，并由既有 stage 脚本生成对应 core 镜像。
2. 允许的 canonical、core/Skills 与生产者测试变化仅为：
   - `docs/contracts/skills-consumer-compatibility-matrix.json`
   - `skills/core/docs/architecture/overview.md`
   - `skills/core/docs/architecture/directory-layout.md`
   - `skills/contracts/skills-consumer-compatibility-matrix.json`
   - `skills/tests/test_skills_orchestrator.py`（只删除已退役 Web consumer 的生产者断言）
   - `docs/README.md` 与 `skills/README.md`（只修正现行 consumer / release 边界叙事）
3. 下列路径仍必须相对基线无变化：`docs/architecture/principles.md`、`docs/architecture/workspace-protocol.md`、`docs/templates/**`、`docs/vision/alignment.md`、`skills/prompts/**`、`skills/install/**`；除上述三份生成文件外的 `skills/core/**` / `skills/contracts/**` 也不得变化，Skills tests 除上述单文件的 Web consumer 断言外不得变化。
4. 此变更是删除后事实一致性的 **editorial stage**，不改变 P-001～P-006、模板、宿主行为或发布身份；不创建新版本、tag、pack 或 Release。

## 为什么不保留旧文案

核心资产“不损坏”包括不能继续指向已不存在的实现。由 canonical 修改并运行既有 stage，比手工改镜像或留下失效路径更符合 SSOT 与用户保护要求。

## 关门验证

最终以基线 path diff、stage `--check`、镜像逐字节一致、生产者测试 diff 和完整非 Web 回归证明该精化没有扩散到方法论或 Skills 行为面。
