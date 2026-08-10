---
id: A-001
goal: GOAL-003-r2-dual-channel-productization
title: R2 方案冻结与双通道产品化实现自审
status: recorded
source: self
date: 2026-08-07
scope: R2 方案冻结（D-001/D-002）、薄壳 lifecycle、bootstrap 双入口、gitignore+doctor、AGENTS managed、File-classic 与生产仓自举证据
verdict: pass
version: 0.1.0
---

# A-001 · R2 方案冻结与双通道产品化实现自审

## 结论

`pass`。本审覆盖 R2 方案冻结、实现与验证事实；不替代 independent cross audit（A-002 待写），也不宣称 R3 或目标关门。

## 证据（可指回）

| 主张 | 证据 |
|------|------|
| I-001/I-002 关闭 | `01-decision/D-001/D-002` accepted；`00-meta` 信息表 closed |
| 薄壳 lifecycle | `skills/mcp/lifecycle.py`（marker 纯函数 + allowlist + confirm 门禁 + CLI）；`skills/tests/test_mcp_lifecycle.py` 全绿 |
| allowlist / 越界 fail closed | 测试覆盖（`_validate_allowlist`、`_ensure_inside_repo`、非目录 root） |
| 标记外字节不变 | 测试：install 前后用户 preamble 逐字节保留；uninstall 后仅用户内容 |
| doctor | `skills/mcp/doctor.py`；测试覆盖 install 前/后/卸载后状态 |
| gitignore 片段 | `skills/mcp/gitignore-fragment.txt`；doctor 报告薄壳被忽略 |
| bootstrap 双入口 | `install-online.ps1/.sh` `-Channel files\|mcp`；mcp 薄通道测试（无 File 大包、managed 段、install.json、File 一等声明）；files 显式完整安装测试；非法 channel 拒绝；ps1 加 UTF-8 BOM 解决 GBK 控制台解析 |
| 生产仓 File 自举 | `{SCRATCH}/file-bootstrap.log`（pack → files 完整安装到临时消费目录 → stage --check ok → L1 File 测试通过）；R1 四宿主 L3 探针（生产仓 File skill 面） |
| 全量回归 | `python -m pytest docs/tests scripts/tests skills/tests` = 178 passed / 3 skipped / 4 subtests |

## Findings

- **required findings：无。**
- **recommended（非阻断）：**
  - R-001：`install-online.ps1` 与 `install-online.sh` 的 mcp 通道逻辑存在少量重复（thin materialize 步骤）；marker/状态写盘已收敛到 `lifecycle.py` CLI（单一真相源），重复仅限文件复制，可接受。
  - R-002：ps1 因 Windows PowerShell 5.1 按 ANSI 读无 BOM 脚本而需 UTF-8 BOM；bash 脚本保留中文输出。已记录，后续维护者勿移除 BOM。
  - R-003：doctor 的 gitignore 检测是启发式（读 `.gitignore` 文本匹配），非 git check-ignore 全语义；对本用例足够，文档注明。

## 边界与后续

- 未覆盖：R3（governance_root）、正式 Release 身份、Docker 镜像构建（VP-004 不强制）。
- 后续：independent cross audit（A-002，provider=grok build / grok-4.5 / thinking-high）→ 响应 findings → C6 闭合 → R2 检查点 git commit。
