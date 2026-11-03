---
id: GOAL-017-on-demand-governance-context
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
version: 0.1.0
---

# D-003 · 按需加载契约与实施计划冻结

## 已核对事实

Claude/Codex 根规则源共用 Claude AGENTS，Copilot 有同等长规则；Grok 使用 Skills 入口。agents_merge 的受管块支持保留块外字节；update 比较当前/新包的渲染变体。core architecture 树递归安装、映射与备份，新文档需进 stage 白名单和 pack/install 必需清单。

## 冻结方案

- canonical 完整操作指南：`docs/architecture/governance-guide.md`，承接原消费 AGENTS 操作规则；principles/workspace-protocol/alignment 仍为对应规则权威。
- canonical 最小入口：`docs/templates/governance-entry.md`，stage 生成 core 模板、skills/AGENTS.template.md、Claude AGENTS 与 Copilot instructions，避免三处漂移。常驻受管块（含 frontmatter）预算 ≤ 40 行、≤ 4096 UTF-8 bytes；明确非治理任务不读取全文，治理命令/自然语言治理/治理记录修改触发全文读取。自定义路径以配置预检为先，非法不回退；缺指南停止治理并补装。
- 完整指南不是 AGENTS/CLAUDE 自动规则文件，不使用自动 import。所有四入口、advanced 原语及宿主 wrappers 在根预检后、扫描治理正文前显式完整读取指南与适用权威；不靠仅存在链接声称已加载。
- core-only 包带最小入口模板和全文指南；独立启用按模板合并/复制入口，不复制 monorepo 维护者长 AGENTS。生产仓根保留维护者规则并增加新 stage 约定与指南导航。
- 复用 managed-block 更新；验证旧长受管块→短块、旧整文件→短块、用户前后缀字节保留、自定义治理根/包目录、重复安装及错误配置/缺文件停止边界。发现迁移缺陷在该目标内修正。
- canonical 先行，再实现与镜像，定向/完整回归、代表真实宿主按需加载验证、16 格兼容证据刷新、cross 审计与 finding 闭环。
- 发行候选采用 minor `v0.14.0`（新增按需加载默认消费能力，协议数据结构保持 0.1.0）；打 tag 前复查未占用。同步所有版本 pin/矩阵/CI 证据路径，dev PR 双平台全绿合入 main 后，严格预检、annotated tag、CI Release 与实际资产验收。保留 Environment release 现有人工门禁。

## 风险与保证

仅承诺 L0 提示词加载契约与代表运行证据，不宣称硬拦截所有非治理读取/所有宿主。用户自有块外规则仍可能自行要求加载全文，本次不能删除用户内容。规则加载行为改变使旧 behaviorSources 过期，S3/S4 必须刷新后再发布。

I-001 已核对；I-002 由 D-002 关闭，当前无其他实施前待答。S1 完成，进入 S2；I-003/I-004 留至原最晚阶段，不用进度放行发布。
