---
id: GOAL-018-host-wait-and-audit-config
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# E-004 · 严格发布演练通过

运行 `release_evidence.py --mode rehearsal --run-checks`，最终 checksPassed=true，四组必需checks全部通过，证据见 attachments/s3-rehearsal-evidence.json；compatibility-report为ready-for-release-evidence。此为rehearsal，不是正式Release，也不把工作树状态当作clean发布事实。

失败排查与修正：首次提供的compatibility report仍绑定旧checkpoint，按当前HEAD重新生成；完整检查又发现旧candidate/host/path测试pin，以及检查器选择现存.venv Python3.14导致Windows临时文件权限不匹配。版本断言更新到本次实际证据；检查器改为优先启动它的解释器，保留缺依赖时的venv候选，并增加回归。当前Python3.11下完整Skills108、scripts156及必需bootstrap检查通过。未移动或修改用户现有.venv，也未放宽实际安装检查。

为本目标JSONL增加eol=lf Git属性，新增checkout round-trip覆盖；实际Windows换行转换后摘要保持一致。安装日志去除记录拼接造成的空白尾行，未改安装事实；运行18信封的来源一致性再次通过。

checkpoint `8b5e187` 保存S3运行/回归基线与v0.15.0清单；上列修正将在下一checkpoint纳入。正式独立审计第02次仍从项目配置读取Grok/grok-4.7/xhigh，干净会话、唯一正式命令，当前尚未返回。S3仍进行中，active50%，不据演练通过跳过cross审计或正式发布门禁。
