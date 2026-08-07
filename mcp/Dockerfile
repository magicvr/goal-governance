# goal-governance MCP server（VP-004 R4 · Docker 发布形态）
#
# 固定入口：`python server.py --repo-root /workspace`（D-001 决策点③）。
# MCP client 以 stdio 直连容器（`docker run -i --rm -v <仓库根>:/workspace <镜像>`），
# 客户端零参数；`--repo-root` 指向挂载的消费仓根（/workspace）。
# 零第三方运行时依赖（Python 标准库），stdio 传输（JSON-RPC 2.0 over stdin/stdout）。
#
# 覆盖 CMD 可调用镜像内其他 CLI，如 lifecycle：
#   docker run --rm -v <仓库根>:/workspace <镜像> lifecycle.py install --root /workspace ...
FROM python:3.11-slim

# F-002 (A-012): pin the effective server version to the release at build
# time (workflow passes the pack/tag version); unset falls back to the
# internal layout version in mcp/__init__.py.
ARG GOAL_GOVERNANCE_MCP_VERSION=
ENV GOAL_GOVERNANCE_MCP_VERSION=${GOAL_GOVERNANCE_MCP_VERSION}

WORKDIR /app

COPY . /app

ENTRYPOINT ["python"]
CMD ["server.py", "--repo-root", "/workspace"]
