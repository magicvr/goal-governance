# L3 探针证据说明（R1 · 2026-08-07）

## 语义边界

四条 `*-l3-four-entry-2026-08-07.json` 探针覆盖**承诺宿主侧**的四治理入口
dispatch 与角色边界（`vision` / `vision-audit` / `govern` / `audit`），经
`scripts/capture_runtime_evidence.py` 捕获并经 `runtime-evidence.schema.json`
校验（verdict 全部 `pass`，marker observed）。

- 宿主：claude-code-cli（2.1.223）、grok-build-cli（1.0.0 / grok-4.5）、
  codex-cli（0.146.1）、github-copilot-cli（1.0.75）。
- 断言策略：`marker+entrypoint+nontrivial-stdout@1` + 四入口名 require-assert。
- **MCP stdio 客户端路径**不在本组探针内：该路径由 L1（`skills/tests/test_mcp_l1.py`
  真启动 server 进程）与 L2（`docs/tests/test_dual_channel_l2.py` 共享内核）确定性
  覆盖。宿主 × MCP 通道的全链路长剧不在 R1 范围（VP-004：「不要求完整治理长剧 +
  真模型全链路」）。

## 捕获点与重捕获（A-012 F-001 选项 A）

- **R1 捕获（2026-08-07 13:40–13:42 UTC）**：behaviorSources 绑定 R1 时点路径
  `skills/mcp/{entries,kernel,server}.py`（当时存在）。
- **R4 迁路径（2026-08-07）**：MCP 实现迁至仓库根 `mcp/`（通道资产分离，
  GOAL-005）；`skills/mcp/` 路径不复存在。R4 后 `entries.py`/`kernel.py` 内容
  未变（remap 后哈希一致），`server.py` 经 R2/R4 合法演进（哈希变化）。
- **重捕获（2026-08-07，同日，F-001 选项 A）**：四宿主以**同一探针 prompt**（prompt
  哈希未变）与同一宿主 CLI 版本重跑，behaviorSources 更新为当前树
  `mcp/{entries,kernel,server}.py` 当前哈希；四条证据 `capturedAt` 为重捕获时点，
  verdict 全部 `pass`。R1 时点 verdict 仍有效（重捕获不使其作废）。
- **F-004/F-005 修复后（2026-08-07，A-015）**：`mcp/server.py` 增 initialize
  握手门禁与 lifecycle root 边界（-32002 / -32602），server 哈希演进
  `c0af461e… → cd31cbde…`；A-016（independent）复核发现 L3 证据 server 哈希
  过期。
- **重捕获 #2（2026-08-07，同日，A-016 F-001r 响应）**：四宿主以**同一探针
  prompt**（prompt 哈希未变）与同一宿主 CLI 版本重跑，behaviorSources 重新绑定
  当前树（server `cd31cbde…`）；四条证据 `capturedAt` 2026-08-07T15:59–16:01Z，
  verdict 全部 `pass`（E-009）。此后修改 `mcp/` 实现（尤其 `server.py`）须同步
  刷新本组证据或按本节约记哈希演进。

## 复跑

```powershell
python scripts/capture_runtime_evidence.py --consumer <host> --entrypoint govern `
  --protocol-version 0.1.0 --product "<product>" --product-version <ver> `
  --prompt-file <prompts>/<host>-l3-four-entry.txt --marker <MARKER> `
  --require-assert vision --require-assert vision-audit --require-assert audit `
  --behavior-source <prompts>/claude-l3-four-entry.txt --behavior-source <prompts>/grok-l3-four-entry.txt `
  --behavior-source <prompts>/codex-l3-four-entry.txt --behavior-source <prompts>/copilot-l3-four-entry.txt `
  --behavior-source mcp/entries.py --behavior-source mcp/kernel.py --behavior-source mcp/server.py `
  --output <evidence>/<host>-l3-four-entry-2026-08-07.json `
  -- <host CLI command>
```

注：codex 为 npm shim，需经 `cmd.exe /d /s /c "codex exec ..."` 包装；
copilot 经 `copilot-l3-replay.ps1`（gh auth token 注入）调用。
