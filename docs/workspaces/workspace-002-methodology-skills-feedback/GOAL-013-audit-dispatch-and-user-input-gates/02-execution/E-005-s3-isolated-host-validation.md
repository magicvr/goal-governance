---
id: E-005
goal: GOAL-013-audit-dispatch-and-user-input-gates
doc: execution-entry
title: S3 隔离宿主验证与取证
status: recorded
parent: GOAL-013-audit-dispatch-and-user-input-gates
created: 2026-10-16
updated: 2026-10-17
version: 0.2.0
---

# E-005 · S3 隔离宿主验证与取证

## 已发生事实

按用户指令开展 S3；Charter 0.2.0、VP-002 与 workspace 绑定有效，无新战略宽阻断或本目标正式 required finding。D-003 路径 A 与 Grok Build independent provider 保持。用户放宽审核、更新 Claude 供应商后明确要求重试，真实指令见 [D-004](../01-decision/D-004-s3-host-probe-retries.md)。此前自动审核拒绝的探针重新提交后获准执行，没有绕路。

1. Claude Code 2.1.301 更新配置后正常运行。旧模型错误、参数错误和 240 秒超时记录保留；成功重试独立另存，没有把失败覆盖成 pass。Claude/Grok/Copilot 三宿主四入口共 12 格完成当前工作树捕获；四宿主目录角色探针另有 4 份。16 份 envelope 来源和输出摘要一致，矩阵改指新 12 格，CI 一致性门禁改查新 16 份。旧跨区证据仅作为历史构建依赖识别，未读取或修改其 Goal 正文。
2. [测试驱动](../attachments/s3-host-probes.py) 每次建立新的合成消费仓和会话，记录版本、argv、原始输入、前后 SHA、实际变更与输出。自动审计语义输入只有正式命令，不追加 marker、scope 或编排历史。合成 A/VRev 不属于生产 GOAL-013 的正式意见。
3. 三项实际偏差已整改并重试：Claude 缺答只聊天停下、未写 blocked；Grok 混合布局后仍继续审计；Copilot audit 额外写非审计目录 .gitkeep。先修 canonical 暂停收尾语义，再同步全部入口；后两项收紧 core05/宿主入口的已有 fail-closed 和写权限边界。成功复测分别为 claude-wait-04、grok-audit-c08-fixed、copilot-audit-final-r2。
4. Claude wait04 与 Copilot wait02 在 headless 无卡片模式写入待答、blocked、执行索引和树，业务代码未变；Claude fresh restart 读取原待答、无重复阻塞或新写入；u07 保留 B-001；u09 不 reopen done。write-denied 无写工具时停止且无修改，但未明确说明持久化失败原因，不能计完整 U10 通过。
5. Grok 真实 TUI 卡片展示后 Shift+X 关闭，保持 blocked、无实现；只有可见界面和落盘结果，没有原始工具返回。另一次按键 1 自动提交 JSON，明确标记为合成输入，绝不是生产用户答复或 U04/U11 通过。首次 TUI cwd 绑定失败后立即取消，无生产文件修改，该次排除验收。
6. Copilot SDK empty 合成 callback 返回空 answer 后仍等待；其 runtime 1.0.71 / gpt-5-mini 未加载当前 File govern/core，不作为 CLI 1.0.75 或真实卡片行为证明。Codex 目录探针默认模型与账户不兼容，单次覆盖 gpt-6.1-sol 后成功，未改用户配置；Codex 不新增矩阵支持承诺。
7. 最终回归：docs 67、Skills 101、scripts 146（4 skipped）通过；38 对镜像一致；runtime check 16；compatibility --require-ready 为 ready-for-release-evidence。最初沙箱内临时 Git 初始化/原子替换失败，依规定 escalated 重跑同套测试后通过；不把环境失败隐去。脚本负例预期输出 fail/missing 等诊断，整套退出 0。Skills 固定旧宿主版本的断言已按实际新版与日期命名证据更新，不放宽摘要校验。

## 证据与验收边界

[22 条覆盖表与限制](../attachments/s3-results-and-coverage.md) 逐条保留未覆盖变体；[真实交互包](../attachments/s3-manual-interaction-checklist.md) 已准备两个 required 信息项及另一个既有 blocker 的隔离实例，尚无用户提交。真实预选未提交、多题部分答复、修正后真实提交与恢复等仍未充分验证；写盘失败诊断也有缺口。S1 的真实卡片答复是历史证据，不能替代本次修改后的交互验证。

矩阵 ready 仅说明既有 producer 入口覆盖，不等于本目标整体通过或发行。S3 未退出，I-004 collecting，S4 未开始，无本目标正式 A 条目。完成检查点仍为 2/4，progress 50%；待用户安排真实参与时按 UI-03 留待答并 blocked，见 E-006。Git checkpoint 仍受既有 dirty baseline/ownership 门禁，未自动暂存或提交；无版本提升、PR、tag 或 Release。
