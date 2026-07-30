---
id: GOAL-023-skills-core-dual-asset-install
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.2.0
---

# 审计 · GOAL-023

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001～I-004 **closed**（D-002） | 阶段 C～E 无新增 required 信息门禁 |
| 到期 required 是否已 verified / residual | 是（策略已决） | 实现证据见阶段 B 单测 |
| 资料引用（若有）是否固定且用户确认 | 无 | — |

## 意见台账索引

| ID | 日期 | source | scope | verdict | 开放必改 |
|----|------|--------|-------|---------|----------|
| A-001 | 2026-07-30 | independent | GOAL-023 C～E 交付、回归与关门前检查 | conditional | **F-001 required（medium）开放** |

---

## A-001 · 双资产与双入口关门前独立交叉审计（2026-07-30）

- **source**：independent
- **auditor**：GitHub Copilot
- **类型** / **scope**：execution-facts / close-out precheck；GOAL-023 阶段 C～E、双资产打包、bootstrap 离线安装、文档与 CI 发布挂接。
- **verdict**：conditional

### 范围与区间

- 工作区：`workspace-001-goal-governance`；Root 为 `GOAL-001-main-vision`，canonical 范围为 `docs/workspace-001-goal-governance/`，与本目标的 parent 一致。
- 本 scope 无共享资料固定引用。I-001～I-004 均为 `closed`；其中 I-004 的同版本 core-only 与 skills 内嵌 core 字节一致性由下列单测覆盖。
- 审计不改 `00-meta` status/progress、决策、执行记录或 `goal-tree.md`。

### 成果（有证据）

- `scripts/tests/test_pack_core_release.py`：6 passed。覆盖 core-only zip + digest、`tech-stack.md` 排除、完整性拒绝，以及 core-only 成员与 skills zip `core/` 成员逐字节一致（I-004）。
- `scripts/tests/test_bootstrap_install_online.py`：5 passed，1 skipped。PowerShell 离线 bootstrap 成功安装 core 与至少一个宿主入口；摘要不匹配时在安装前失败关闭。bash 完整脚本有结构断言；本机 WSL 无可用 bash 发行版，离线 e2e 按 `R-023-BASH-HOST` skip。
- `scripts/tests/test_pack_skills_release.py`：6 passed，1 skipped。既有 skills pack 仍含内嵌 core；Windows 无创建 symlink 权限，symlink 拒绝用例 skip。
- `.github/workflows/skills-pack-release.yml` 明确打包并上传 skills/core zip 与各自 digest、两个 bootstrap 脚本；发布上传步骤还 fail-closed 要求双 zip 和双 digest。

### 对照成功标准

- 双资产命名、core-only 内容边界、skills 内嵌 core 与 digest 校验均有实现和自动化证据。
- PowerShell bootstrap 的绝对本地路径流程及摘要失败关闭有可重复测试证据。
- CI 资产集合和发布上传门禁与 D-002 的双入口、同版本双资产模型一致。

### Findings

#### F-001 · 文档示例的相对 `-ZipPath` 与 `-TargetDir` 组合不可执行

- **级别**：required；**严重度**：medium
- **影响范围**：阶段 C 的离线 bootstrap 用户路径；阶段 D 文档准确性；阶段 F 关门。
- **证据**：`scripts/bootstrap/README.md` 的离线 PowerShell 示例同时使用 `-TargetDir C:\path\to\empty-project` 和相对 `-ZipPath dist\goal-governance-skills-v0.0.0-testpack.zip`。但 `scripts/bootstrap/install-online.ps1` 的 `Resolve-FullPath $ZipPath $TargetDir` 将相对 zip 路径解析为 `<TargetDir>\dist\...`。独立隔离复现把 zip 放在调用目录的 `pack/`、目标仓设为其 sibling `consumer/` 后，报错 `ZipPath not found: ...\consumer\pack\goal-governance-skills-v0.0.0-audit.zip`。
- **风险**：按发布文档从维护仓或下载目录运行 bootstrap、同时指定另一个消费目标仓时会在摘要校验前失败；现有成功测试传绝对 `ZipPath`，未覆盖该文档组合。
- **要求的闭合证据**：由 `/govern` 选择并记录一种明确契约，再提供回归测试：
	- 将文档中的 `ZipPath` / `Sha256Path` 改为绝对路径或位于 `TargetDir` 下的路径；或
	- 调整脚本使相对 zip / digest 路径相对调用目录解析，并覆盖该行为。

### 必改项汇总

- **F-001**：在阶段 F 关门前闭合。当前没有用户书面 residual 或 overruled 决定，故不得以本意见无条件关门。

### 与既有意见的异同

- 本目标此前无 self 或 independent 正式意见。本意见认可 A～E 已有的自动化成果，但独立发现文档所示离线参数组合与 PowerShell 实现的路径基准不一致。

### 结论 + 建议给编排器/用户的下一步

结论为 **conditional**：核心双资产、摘要 fail-closed、PowerShell 离线主路径与 CI 挂接具有可核验证据；但 F-001 是影响实际离线安装说明的 required 缺口。建议 `/govern` 先选择路径语义并修正文档或实现，加入相应回归；随后复审 F-001，再进行 self close-out 和用户关门确认。

### 声明

本意见不修改 status/progress；响应、finding 闭合与阶段推进由 `/govern` 处理。
