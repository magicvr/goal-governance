---
id: GOAL-017-on-demand-governance-context
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
version: 0.1.0
---

# D-001 · 反馈范围、路线图与可评审方案

## 已授权范围与取舍

用户 2026-11-03 明确要求：在工作区 2 新增子目标，解决消费仓 AGENTS 长期占用提示空间的问题；在 dev 开发，无误后提交 PR 合并 main，经 CI 发布新资产。立项、调查、实现、验证、PR/合并与发布均在授权内；不为这些已授权动作重复请求许可。

作为 Root R3 子目标继承 VP-002 / Charter，初步未见开放上游 required 阻断立项；不改 Charter 方向，不需要新 VP 或工作区。跨协议定义、安装/升级兼容与发布门禁，按 P-001 先建 S1～S4 路线图。

## 拟实施方案（S1 待冻结）

1. 消费仓根规则只保留最小受管入口：治理触发条件、完整规则路径/加载动作、必要的真相源与失败边界。完整指南放在不会被宿主自动当根规则加载的位置，随安装包落盘，可离线访问。
2. 触发覆盖四治理入口、自然语言治理请求，以及直接修改 Goal/VP/Charter/审计等治理记录；普通业务代码与一般文档任务不强制加载完整规则。保持实际治理任务原有门禁。
3. 四宿主 wrappers/prompts 显式接入完整指南；不能只给链接便声称宿主会加载。core-only 也要有完整指南和足够的导航。
4. 优先复用现有 managed markers 与 merge/update：框架块缩短，块外用户字节保留；覆盖旧整文件、旧块、重复安装、自定义治理根与包目录、缺文件及非法配置。
5. 精确路径与体积预算在逐项读实现后冻结；以安装产物行数/UTF-8 字节为可复核指标，当前 Claude 源 32,317 bytes，Copilot 源 32,300 bytes。不能用这些字节数宣称实际 token 数。
6. 先改 canonical architecture 约定，再改消费实现，stage 镜像并 --check；同步所有实际分发路径，验证本仓 dogfood 与消费包入口。
7. 完成定向及仓库规定回归、实际运行证据刷新、cross 审计与 finding 响应；dev PR 双平台 CI 全绿后合并 main，再 strict 门禁、annotated tag、CI Release/GHCR 与下载资产验收。

未选做法：只删除根规则不补加载链，会丢治理约束；只把全文移到仍会自动导入的规则文件，不能解决常驻开销。保留受管块外用户内容，避免升级覆盖业务规则。

## 风险与审计门禁

修改加载协议属于 cross，self + independent，不静默降低模式。本会话没有用户指定 provider；Q-001 为实施前必需裁决。正式独立派发正文只能为单行 `/audit workspace-002 goal-017`，不附加 scope 或自编提示、不复制编排历史。

运行证据绑定 behaviorSources；本次改规则/入口后必须检查并刷新受影响证据，不能复用过期 v0.13.8 记录作当前发布证明。上一目标 R-016-001（矩阵 host version 基线）在新捕获时复核，不自动继承历史 residual/overruled。

当前发布 workflow 使用 Environment release；保留仓库现有审批要求，不把用户的发布指令当成已经发生的环境审批。发行版本在 S4 前结合兼容语义与远端 tag 确定。

## 当前结论

范围与调查准备可执行，实施方案待 S1 冻结；Q-001 未答前暂停，不进入 S2、不派发独立审计、不提交 PR 或发布。

