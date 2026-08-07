# goal-governance MCP channel（VP-004 R1/R4）

MCP 通道是目标治理的**一等交付通道**（与 File 通道并列；File 不被废除）。本目录为 MCP
通道实现：最小 stdio MCP server + 四治理入口映射 + L2 共享等价内核。
R4（2026-08-07）起本目录位于仓库根 `mcp/`（与 `skills/` 并列，通道资产分离）：
File 发布资产（skills zip）**不**包含本目录代码；MCP 通道的发布资产为 **GHCR Docker 镜像**
（与 File 资产同 tag 同版本发布）。

## 运行形态

- **主消费形态（R4）**：**Docker 镜像** `ghcr.io/magicvr/goal-governance-mcp-server:<版本>`
  （与 GitHub Release 同 tag 同版本，如 tag `v0.13.0` → 镜像 `:0.13.0`；另有 `latest`）。
  固定入口：`python server.py --repo-root /workspace`（MCP client 零参数，见下）。
- **本地 stdio 进程形态仍合法**（VP-004：不强制 Docker-only）：
  `python mcp/server.py [--repo-root PATH]`。
- 零第三方运行时依赖（Python 标准库），stdio 传输（换行分隔 JSON-RPC 2.0）。

## Docker 使用（推荐）

```bash
# 拉取（版本与 GitHub Release tag vX.Y.Z 对应；latest 指向最新发布）
docker pull ghcr.io/magicvr/goal-governance-mcp-server:0.13.0

# 手动验证（stdio 直连；将 <仓库根> 换为消费仓路径）
docker run -i --rm -v "<仓库根>:/workspace" ghcr.io/magicvr/goal-governance-mcp-server:0.13.0
```

**MCP client 配置**（mcpServers，stdio 直连容器，零参数；固定入口自动使用
`--repo-root /workspace`）：

```json
{
  "goal-governance": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-v", "<仓库根>:/workspace", "ghcr.io/magicvr/goal-governance-mcp-server:0.13.0"]
  }
}
```

镜像内亦可调用其他 CLI（覆盖 CMD），如 lifecycle：

```bash
docker run --rm -v "<仓库根>:/workspace" ghcr.io/magicvr/goal-governance-mcp-server:0.13.0 \
  lifecycle.py install --root /workspace --version 0.13.0 --channel mcp --confirm
```

镜像构建（发布由 `skills-pack-release.yml` tag 流程自动完成）：`docker build -t <tag> mcp/`。

## 版本语义（F-002 · A-012）

- **有效 server 版本**（`initialize.serverInfo.version`、lifecycle `install`/`upgrade` 写入的版本、
  `version` 命令）＝发布钉：发布流水线经 Docker build arg
  `GOAL_GOVERNANCE_MCP_VERSION=<pack/tag 版本>` 写入镜像，镜像内自报版本与
  GHCR tag / GitHub Release **同源**，不会漂移。
- **内部布局版本**（`MCP_LAYOUT_VERSION = "0.1.0"`）＝通道协议/布局代际，**不等于**产品
  release 版本；本地源码 checkout（stdio 进程）未设 `GOAL_GOVERNANCE_MCP_VERSION` 时
  有效版本回退为该值。`doctor` 报告分列 `server.version`（有效）与
  `server.layoutVersion`（布局），两者语义不可混用。

## 四治理入口（工具）

| 工具 | 关键参数 | 层级 | 角色边界 |
|------|----------|------|----------|
| `vision` | `task`(必填)、`workspace`(可选) | 决策层 | 建修 Charter / VP / Vision Review / re-align；冷启动优先 |
| `vision-audit` | `task`(必填)、`scope`(可选) | 决策层 | 独立 Vision Review：只出意见，不改 Charter/VP/Goal 状态 |
| `govern` | `task`(必填)、`workspace`(可选)、`goal_id`(可选) | 实现层 | 实现编排：扫描→台账→P-004→提议→确认→原语写入 |
| `audit` | `task`(必填)、`goal_id`(必填)、`scope`(可选) | 实现层 | Goal 交叉审计：只出意见到 `03-audit`，不改 status |

`commit` 不进工具集（便利可选、与治理正交，VP-004 入口面）。

## 消费方式（宿主示例）

MCP 客户端配置指向容器（stdio 直连，见上）或本地 `python mcp/server.py`（stdio）。
`tools/list` 发现四工具；`tools/call` 返回结构化元数据
（entrypoint/layer/role/readonly/prompt_path/guidance），宿主据此 dispatch 到对应
方法论正文（仓内 `skills/prompts/` 存在时可按 sha256 核对）。

## 实例真相

实例状态**永远在仓库内治理记录树**（`{governance_root}`，默认 `docs`）；本 server
不写任何治理状态，**不是**权威状态库。

## 测试与证据分级

- L1 MCP：`skills/tests/test_mcp_l1.py`（真启动 server 进程）。
- L1 File：`docs/tests/test_file_l1.py`（直接驱动 File 资产，不用 MCP mock）。
- L2 共享：`docs/tests/test_dual_channel_l2.py`（`kernel.check_equivalence` 两通道同断言）。
- 合同：`scripts/tests/test_contract_delivery_channels.py`（`deliveryChannel: files | mcp` 分列）。
- L3：承诺宿主抽稀真探针（`docs/releases/runtime/` 既有模式）。
- 发布面（R4）：`scripts/tests/test_bootstrap_install_online.py`（薄装经镜像内 lifecycle）、
  `scripts/tests/test_pack_skills_release.py`（File zip 不含 `mcp/` 防御断言）、
  `skills-pack-release.yml` 契约测试（同 tag GHCR 发布）。

## 目录

| 文件 | 内容 |
|------|------|
| `server.py` | MCP stdio server（JSON-RPC 2.0 over stdio；四治理工具 + install/upgrade/uninstall/doctor） |
| `entries.py` | 四入口映射纯数据（名称/参数边界/层级/角色边界单一真相源） |
| `kernel.py` | L2 共享等价内核（10 条检查点 + 两通道描述 + 同断言校验） |
| `lifecycle.py` | 薄壳 lifecycle：managed 标记、allowlist、默认确认写盘、CLI（R2 交付） |
| `doctor.py` | 只读安装状态报告（含 `governance_root` 解析与错误面）（R2/R3 交付） |
| `config.py` | `governance_root` 解析：默认 `docs`、`.goal-governance.json` pin、仓外 fail closed（R3 交付） |
| `governance-root.schema.json` | 项目配置 schema |
| `gitignore-fragment.txt` | 官方 ignore 片段（薄壳默认 gitignore） |
| `Dockerfile` / `.dockerignore` | R4 发布形态：GHCR 镜像构建（固定入口 `python server.py --repo-root /workspace`） |

## 证据分级与 L3 边界

- L1 MCP = 真启动 server 进程的直接测试；L1 File = 直接驱动 File 资产（无 MCP mock）。
- L2 = `kernel.check_equivalence` 同一组断言驱动两通道；角色事实从两通道**真实资产独立提取**（File 侧读 prompt 正文短语，MCP 侧读 `tools/list` description 并解析层级前缀），其余检查点（台账边界、fail closed 声明、单愿景等）为协议 SSOT 防漂移断言。
- L3 = 承诺宿主抽稀真探针：覆盖四治理入口在宿主侧的 dispatch 与角色边界（File skill 面）；MCP stdio 客户端路径由 L1/L2 确定性覆盖。宿主 × MCP 通道的全链路长剧不在 R1 范围（VP-004 明确「不要求完整治理长剧 + 真模型全链路」）。
