---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: S6 发布前 CI 缺陷与修复（PR #21）
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · PR #21 上由 CI 抓获的两个跨平台缺陷（2026-09-13）

> 背景：S6 本地回归全绿后开 PR #21（`dev` → `main`）。**Windows CI job 连续两次失败**，抓出本地测不出（Windows 上无 bash）的两个真实缺陷。两处均已修复、CI 转绿。

## 缺陷 1 · `install.sh` 带 UTF-8 BOM，下载后 shebang 失效

| 项 | 内容 |
|----|------|
| 现象 | Windows CI：`/tmp/.../skills/install.sh: line 1: \ufeff#!/usr/bin/env: No such file or directory`，随后 AGENTS.md 合并 fail closed |
| 根因 | S4 期间用 PowerShell `Set-Content -Encoding utf8` 改写 `install.sh` / `install.ps1`，Windows PowerShell 会写入 **UTF-8 BOM**；包内 `install.sh` 因此以 `\ufeff#!` 开头，bash 无法解析 shebang |
| 为何本地没抓到 | 本机无 bash（WSL 无发行版），本地无法执行 `install.sh`；Ubuntu CI 用的是 `skills/tests` 路径，Windows CI 才走「下载包 → bash 离线自举」路径 |
| 修复 | 去除两个安装器的 BOM（`skills/install.sh`、`skills/install.ps1`） |
| 防再犯 | 新增 `test_installers_ship_without_utf8_bom`：断言两文件字节 0 不是 BOM，且分别以 `#!/usr/bin/env bash` / `# Goal Governance Skills installer` 开头 |
| 提交 | `af9f079` |

## 缺陷 2 · Git Bash 下把 POSIX 路径交给原生 Python

| 项 | 内容 |
|----|------|
| 现象 | Windows CI：`python3.exe: can't open file 'C:\\tmp\\...\\consumer\\skills\\agents_merge.py': [Errno 2] No such file or directory` |
| 根因 | Git Bash / MSYS 传的是 POSIX 路径（`/tmp/...`、`/c/...`），原生 Windows Python 无法打开；`merge_agents_file` 把 `$SCRIPT_DIR/agents_merge.py` 直接交给解释器 |
| 修复 | `install.sh` 新增 `native_path()`：`uname` 报告 `MINGW*/MSYS*/CYGWIN*` 且存在 `cygpath` 时转成 Windows 路径；POSIX 主机原样透传。合并调用对 helper / source / target 三个路径都做转换 |
| 提交 | `de7fd31` |

## 结果

| 项 | 状态 |
|----|------|
| PR #21 CI（run `34748262249`） | `contract-and-report` **pass**（1m3s）· `windows-install-surface` **pass**（2m3s） |
| 本地复验 | scripts 128 OK（skipped=4）· skills 44 OK · 镜像 0 漂移 · `git diff --check` 洁净 |
| 教训（登记待后续治理目标） | **本地无 bash 的环境**无法验证 shell 安装器；跨平台安装面必须有 CI 兜底（本仓已有 Windows/Ubuntu 双 job，本次正是它拦下的）。此类缺陷**不**应等发布前才发现——`install.sh` 的任何改动都应以 CI 为准，而非本地套件 |

## 未覆盖

- 修复后**未**在 POSIX 主机上本地复跑 `install.sh`（本机无 bash）；依据是 Windows CI 的 bash 路径已通过 + Ubuntu CI 的 `contract-and-report` 通过。
- `test_bootstrap_install_online.py` 的 bash 用例在 Windows 上 `skipped=2`（无 bash 时跳过），本地无法替代 CI。
