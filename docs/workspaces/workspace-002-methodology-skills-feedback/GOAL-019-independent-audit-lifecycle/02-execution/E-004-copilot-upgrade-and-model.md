---
id: GOAL-019-independent-audit-lifecycle
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.1.0
---

# E-004 · Copilot 版本归属修正与用户指定模型

本机 npm 包原为 `@github/copilot@1.0.71`；不带 `--no-auto-update` 的版本查询显示1.0.75，实际取证命令带该参数，启动日志却为1.0.71。VS Code shim仍转调npm旧二进制，attempt03的路径修正假设不成立，不能采用其表面pass。确认归属错误后停止在途实验，attempt02/03信封分别归档至 `attachments/copilot-path-attempt-02/`、`copilot-path-attempt-03/`；不改写其原始版本或摘要。

用户要求核对升级。官方npm查询当时latest为1.0.110，GitHub最新Release为v1.0.111；按官方npm安装路径运行 `npm install --global @github/copilot@1.0.110`。安装包、同一原生可执行文件带/不带禁用自动更新参数的版本输出均为1.0.110，实际新进程启动日志也为1.0.110。

原始稳定采集器 `s3-host-probes.py` 保持不变，以免使已完成的11份证据来源哈希失效。另建 `attachments/s3-copilot-probes.py`，执行及版本查询固定为同一npm原生二进制，版本查询同样禁用自动更新。attempt04仍使用原Gemini模型；用户随后明确要求改用 `gpt-6-luna`、不用Gemini，故按用户取消停止并归档至 `attachments/copilot-gemini-attempt-04/`。这次停止不基于探索子代理时长。

attempt05以 `gpt-6-luna` 重新建立全新夹具/会话；覆盖参数与Process级环境一致，不改用户级模型配置，不改正式审计provider Grok。govern项已完成且pass，其他项采集中。详情与诊断范围见 `attachments/s3-copilot-executable-selection.json`。端点健康检查不作为矩阵证据；升级已解决版本歧义，但不能把此前响应慢全部归因于CLI版本。

另11项已完成证据的结果、现行LF来源哈希与原始stdout/stderr摘要均匹配；主线程核对Claude/Grok四次正式审计的observation输入及SHA256，均严格匹配 `/audit workspace-002 goal-019` 或 `/vision-audit vp-002`。Claude vision-audit r2失败，r3新会话通过，只选r3。当前仍为active50%，I-003 collecting；尚未完成S3或发布。
