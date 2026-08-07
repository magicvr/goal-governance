---
id: E-002
goal_id: GOAL-003-r2-dual-channel-productization
title: R2 方案冻结与双通道产品化实现落盘
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# E-002 · R2 方案冻结与实现（2026-08-07）

## 事实

1. **方案冻结**：D-001（薄壳落点 + managed paths allowlist + 默认确认写盘）与 D-002（bootstrap 双入口形态）落盘并 accepted；I-001 / I-002 关闭。
2. **MCP 薄壳 lifecycle**（`skills/mcp/lifecycle.py`）：
   - managed 标记 `<!-- goal-governance:begin managed -->` … `end managed`；`replace_managed_section` / `remove_managed_section` / `parse_managed_version` 纯函数。
   - allowlist = `{AGENTS.md, .goal-governance}`；仓外/越界 fail closed；install/upgrade/uninstall 默认 `confirm=false` 拒绝写盘。
   - CLI（`lifecycle.py install|upgrade|uninstall|state`）供 bootstrap mcp 通道调用（单一真相源）。
3. **doctor**（`skills/mcp/doctor.py`）：只读状态报告（managed 段、薄壳状态一致性、gitignore 覆盖、governance_root、合同信息项）。
4. **官方 gitignore 片段**：`skills/mcp/gitignore-fragment.txt`（忽略 `.goal-governance/`）。
5. **MCP server 扩展**：新增 `install` / `upgrade` / `uninstall` / `doctor` 工具（`tools/list` 可见；四治理工具集不变；`commit` 仍不入集）。
6. **bootstrap 双入口**：`install-online.ps1`（新增 UTF-8 BOM 解决 GBK 控制台解析）+ `install-online.sh` 新增 `-Channel files|mcp`；mcp 通道只装 `skills/mcp` + consumer contract + AGENTS managed 段 + `.goal-governance/` 状态；files 默认行为不变；Usage/README 推荐 MCP 同屏声明 File 仍一等、非日落。
7. **测试**（新增 18 条，全绿）：

   | 文件 | 覆盖 |
   |------|------|
   | `skills/tests/test_mcp_lifecycle.py` | 确认门禁、allowlist、标记外字节不变、upgrade 只改标记内、uninstall、doctor、gitignore 片段 |
   | `scripts/tests/test_bootstrap_install_online.py` | mcp 薄通道安装（无 File 大包、managed 段、install.json）、files 显式完整安装、非法 channel 拒绝、README/ps1 双入口声明、File-classic 无 docker 依赖 |

8. **生产仓 File 自举证据**：`{SCRATCH}/file-bootstrap.log` —— 本仓 pack → File 通道完整安装到临时消费目录（docs/architecture、prompts、宿主 skill、AGENTS.md 全 True）→ `stage --check` ok → L1 File 测试通过。R1 已捕获四宿主 L3 探针（本仓即生产仓，File skill 面 dispatch）。
9. **全量回归**：`python -m pytest docs/tests scripts/tests skills/tests` = 178 passed / 3 skipped / 4 subtests。

## 进度评估

- C1（双入口 + 推荐声明）✅、C2（lifecycle）✅、C3（gitignore + doctor）✅、C4（managed 标记）✅、C5（File-classic + 生产仓自举）✅、C6（审计闭合）⏳。
- 待办：self 审视落盘；grok build（grok-4.5 / high）independent 意见落盘；required findings 闭合；R2 检查点 git commit。
