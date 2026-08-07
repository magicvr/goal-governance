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

## 复跑

```powershell
python scripts/capture_runtime_evidence.py --consumer <host> --entrypoint govern `
  --protocol-version 0.1.0 --product "<product>" --product-version <ver> `
  --prompt-file <prompts>/<host>-l3-four-entry.txt --marker <MARKER> `
  --require-assert vision --require-assert vision-audit --require-assert audit `
  --behavior-source ... --output <evidence>/<host>-l3-four-entry-2026-08-07.json `
  -- <host CLI command>
```

注：codex 为 npm shim，需经 `cmd.exe /d /s /c "codex exec ..."` 包装；
copilot 经 `copilot-l3-replay.ps1`（gh auth token 注入）调用。
