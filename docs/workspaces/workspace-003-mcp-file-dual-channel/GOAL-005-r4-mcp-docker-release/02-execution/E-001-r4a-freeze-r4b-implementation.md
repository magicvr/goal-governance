---
id: E-001
goal_id: GOAL-005-r4-mcp-docker-release
title: R4a 冻结 + R4b 实施（搬迁 / Dockerfile / workflow / 薄装重定义 / 文档）
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# E-001 · R4a 冻结 + R4b 实施（2026-08-07）

## 事实

1. **R4a 方案冻结**：D-001 落盘（生产布局 = 根目录 `mcp/`；消费形态 = GHCR 镜像固定入口 `python server.py --repo-root /workspace`；`-Channel mcp` 薄装重定义；workflow 同 tag 同版本发布）。I-005/I-006 关闭（用户 2026-08-07 书面确认：`ghcr.io/magicvr/goal-governance-mcp-server` + 去 v 版本 tag + latest；固定入口）。
2. **搬迁**：`git mv skills/mcp → mcp/`（10 文件）。File zip 由 pack（只打 `skills/`）结构性排除 mcp；`scripts/tests/test_pack_skills_release.py` 加 `mcp/` 防御断言。
3. **Docker 资产**：`mcp/Dockerfile`（`ENTRYPOINT ["python"]` + `CMD ["server.py", "--repo-root", "/workspace"]`，零第三方依赖）+ `mcp/.dockerignore`。本地 `docker build` 验证通过（bootstrap 测试内构建）。
4. **发布 workflow**：`skills-pack-release.yml` publish job 增加 `packages: write`、`docker/login-action@v3`（GHCR）+ `docker/build-push-action@v6`（context `mcp/`，push `ghcr.io/magicvr/goal-governance-mcp-server:<版本>` + `latest`）；位于 release evidence gate 之后——同 tag 同时发布，fail closed 语义保持。
5. **薄装重定义**：`scripts/bootstrap/install-online.{sh,ps1}` 的 `-Channel mcp` 不再 materialize mcp 代码；改为写 `skills/contracts/` + `docker run` 镜像内 `lifecycle.py install`（写 AGENTS.md managed 段 + `.goal-governance/install.json`，`channel=mcp`）+ 输出 MCP client 配置指引（零参数 docker run 命令）；新增 `--mcp-image`/`-McpImage` 参数。对应 e2e 测试改造（ps1 + bash，本地构建镜像，`docker` 不可用时跳过）。
6. **文档**：根 `README.md` 新增「在其他项目中安装 MCP Server（Docker 通道）」节（pull/run + mcpServers 配置 + 同 tag 说明）；`mcp/README.md` 重写（Docker 主形态 + 本地 stdio 合法 + 「Dockerfile 可选」空头文案修正）；`scripts/bootstrap/README.md` 更新薄装描述；`docs/architecture/workspace-protocol.md` canonical 引用 `skills/mcp/config.py` → `mcp/config.py` + stage 镜像刷新（`--check` ok）。
7. **引用面更新**：`skills/tests/test_mcp_{l1,lifecycle,config}.py`、`docs/tests/test_dual_channel_l2.py`、`docs/tests/test_governance_root_canonical.py`、`mcp/server.py`（docstring）、`mcp/doctor.py`（fragment 路径）。历史记录（CHANGELOG、GOAL-004 台账、缺口描述）保留原路径不改写。

## 验证

- 全量回归：`python -m pytest docs/tests scripts/tests skills/tests -q` → **197 passed, 4 skipped, 4 subtests passed**（与 A-009 基线一致）。
- `python scripts/stage_skills_mirrors.py --check` → ok（36 对 0 漂移）。
- 薄装 e2e（ps1 + bash × docker 镜像内 lifecycle）：AGENTS.md managed 段 + `.goal-governance/install.json`（`channel=mcp`）真实写入消费仓；无 mcp 代码 materialize。

## 进度评估

- C1（R4a）/ C2（R4b）完成；C3（R4c）待跑：cross 审计（self + independent grok build）→ 通过后 Root 复关。
