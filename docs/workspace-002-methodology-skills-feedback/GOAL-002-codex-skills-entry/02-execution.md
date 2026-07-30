---
id: GOAL-002-codex-skills-entry
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-07-31
version: 0.3.0
---

# 执行记录 · GOAL-002

## 时间线

### 2026-07-31 · 目标立项

- `/govern` 在 workspace-002 开区同轮创建本目标五件套。
- 登记成功标准 4 检查点、阶段 A～D、信息项 I-001～I-004。
- **尚未**开始 Codex 加载机制调研或 `install/codex` 实现。

### 2026-07-31 · 阶段 A 澄清 + 方案冻结（I-001/I-002 / D-002）

- `/govern` 焦点本目标：用户意图「先澄清 Codex skills 加载（I-001/I-002），再定 install/codex 方案」；确认 **OK 全套写入**。
- **调研（文档）**：OpenAI Codex Build skills / customization / AGENTS.md 官方说明 + 对照 `skills/install/claude|grok`。
- **产物**：
  - [attachments/i-001-i-002-codex-skills-loading-2026-07-31.md](attachments/i-001-i-002-codex-skills-loading-2026-07-31.md)
  - **I-001 → verified**：REPO skills = `.agents/skills`；AGENTS 为独立 instruction 链（`~/.codex` + 仓库 `AGENTS.md`）。
  - **I-002 → verified**：四独立 skill（govern/audit/vision/vision-audit）+ `$name` 显式调用。
  - **D-002 accepted**：包源 `skills/install/codex/skills/…`；落点 `.agents/skills/…`；开关 `--codex`；`-All` 纳入；AGENTS 复用 claude 源；I-003 不阻塞 C。
- **检查点**：成功标准 #1 勾选；`progress` **25%**（1/4）。
- **未做**：`install/codex` 文件与脚本改动（阶段 C）；Codex runtime 探针（阶段 D）。

### 2026-07-31 · 阶段 C 实现 install/codex + 脚本开关

- `/govern` 用户明确实现阶段 C（D-002 冻结方案）。
- **包源**：
  - `skills/install/codex/skills/govern/SKILL.md`
  - `skills/install/codex/skills/audit/SKILL.md`
  - `skills/install/codex/skills/vision/SKILL.md`
  - `skills/install/codex/skills/vision-audit/SKILL.md`
  - `metadata.host: codex`；正文指向 prompts `00` / `05` / `06` / `07`。
- **脚本**：
  - `skills/install.ps1`：`-Codex` / `--codex`；`-All` 纳入 Codex；安装 `AGENTS.md` + `.agents\skills\{govern,audit,vision,vision-audit}\SKILL.md`。
  - `skills/install.sh`：对称 `--codex` / `--all`。
  - 同源文件二次安装：若 dest 与 source **SHA-256 相同**则 `Already present` 跳过确认（避免 Claude+Codex 同写 `AGENTS.md` 在 non-interactive 失败）。
- **文档 / 测试**：
  - `skills/README.md` 增加 Codex 安装面与参数说明（**未**将 Codex 标为 matrix committed / runtime-verified）。
  - `skills/tests/test_install_ps1_isolated.ps1`、`test_skills_orchestrator.py` 断言 `.agents/skills` 与 codex 源。
  - `python skills/tests/test_skills_orchestrator.py`：**41 tests OK**（本机）。
- **检查点**：成功标准 #2、#3 勾选；I-004 **verified**；`progress` **75%**（3/4）。
- **未做**：Codex 宿主 runtime 探针（阶段 D / 成功标准 #4）；consumer 矩阵 committed（I-003）。

## 待办

1. ~~**阶段 A**：收集 Codex skills / 项目指令加载证据（关闭或推进 I-001/I-002）。~~ **完成**
2. ~~**阶段 B**：方案决策（目录、install 开关、入口覆盖）。~~ **D-002 冻结**
3. ~~**阶段 C**：实现 `install/codex` + `install.ps1`/`install.sh` + 文档/help。~~ **完成**
4. **阶段 D**：Codex runtime 探针 + 审计关门。

## 进度评估

3/4 成功检查点；阶段 A–C 完成；待 D 验证与关门。
