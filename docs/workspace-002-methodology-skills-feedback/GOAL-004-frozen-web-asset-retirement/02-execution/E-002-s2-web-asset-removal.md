---
id: GOAL-004-frozen-web-asset-retirement
doc: execution-entry
record_id: E-002
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-002 · S2 Web 资产与主动依赖移除

- 删除前将精确目标解析为仓库内 `web/`，确认 **63** 个 tracked 文件与 **64** 个 ignored 本地遗留；未使用宽目录或未解析变量作为删除目标。
- `git rm -r -- web` 删除全部受跟踪源码、模板、fixtures 与 tests；随后仅对已核对的 `web/` 清除 ignored `.env`、cache 等本地遗留。删除后 `Test-Path web = False`、tracked `0`、ignored `0`。
- `.github/workflows/ci.yml` 与 `skills-pack-release.yml` 不再安装 `web/requirements.txt`、运行 Web tests 或传递 `--include-web`。
- `scripts/release_evidence.py` 删除 Web Python/import/test check、`include_web` API/CLI 参数与 release-mode Web 强制；release 与 rehearsal 仍使用同一组非 Web 固定检查。
- `scripts/compatibility_report.py`、canonical matrix 与对应测试删除 `web-readonly-parser` 专属 consumer/校验；其余三宿主、coverage、freshness、mirror 与 release identity 门禁保留。
- 未删除或改写历史 workspace ledgers、旧 CHANGELOG release sections 与 SHA 固定 runtime captures；D-003 将其中 Web 文字明确限定为退役前历史观察。

S2 完成；此条不宣称验证或 independent 关门完成。
