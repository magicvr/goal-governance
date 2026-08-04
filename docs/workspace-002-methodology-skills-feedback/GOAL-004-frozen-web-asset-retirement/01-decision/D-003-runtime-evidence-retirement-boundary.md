---
id: GOAL-004-frozen-web-asset-retirement
doc: decision-entry
record_id: D-003
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-003 · 已发布 runtime evidence 的退役解释边界

## 新发现

主动引用扫描在 `docs/releases/runtime/v0.12.1/**/stdout.txt` 中发现退役前的 Web parser / Web CI 文字和 `web/tests` 文件名。这些 stdout 由同目录 runtime evidence JSON 的 `stdoutSha256` 固定，属于发布时点的原始捕获，不是当前运行依赖。

## 决定

1. 不删除、不改写、不重采这些已发布 runtime captures；否则会破坏 SHA 绑定的历史证据，或无必要地产生新的 Skills runtime evidence。
2. 在现行 `docs/releases/README.md` 明确解释：其中 Web 文字仅是 capture 当时的历史观察，不再构成当前 Web consumer、支持声明或回归门禁。
3. 当前状态只由现行 compatibility matrix、CI/workflow、release-evidence 检查清单和当前入口文档判定；这些表面必须不再包含 Web consumer 或可执行 Web 依赖。
4. 本解释不改变 `v0.12.1` 发布身份，不创建新版本、tag、pack、runtime capture 或 Release。

## 关门验证

- 原始 runtime JSON/stdout 相对基线无 diff，SHA 绑定保持完整。
- 当前 active scan 将 versioned runtime captures 分类为历史证据，并单独验证 CI、scripts、matrix 与现行入口无 Web 执行依赖。
- compatibility/release rehearsal 继续验证三宿主 evidence 的既有 freshness 与非 Web producer 门禁。
