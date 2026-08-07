# goal-governance MCP channel（VP-004 R1）

MCP 通道是目标治理的**一等交付通道**（与 File 通道并列；File 不被废除）。本目录为 MCP
通道实现：最小 stdio MCP server + 四治理入口映射 + L2 共享等价内核。

## 运行形态

- **最小运行形态**：Python 3 stdio 进程（换行分隔 JSON-RPC 2.0），零第三方运行时依赖。
- **不强制 Docker**：`Dockerfile` 仅作便捷（可选）；本地 stdio 进程形态合法（VP-004）。
- 启动：`python skills/mcp/server.py [--repo-root PATH]`。

## 四治理入口（工具）

| 工具 | 关键参数 | 层级 | 角色边界 |
|------|----------|------|----------|
| `vision` | `task`(必填)、`workspace`(可选) | 决策层 | 建修 Charter / VP / Vision Review / re-align；冷启动优先 |
| `vision-audit` | `task`(必填)、`scope`(可选) | 决策层 | 独立 Vision Review：只出意见，不改 Charter/VP/Goal 状态 |
| `govern` | `task`(必填)、`workspace`(可选)、`goal_id`(可选) | 实现层 | 实现编排：扫描→台账→P-004→提议→确认→原语写入 |
| `audit` | `task`(必填)、`goal_id`(必填)、`scope`(可选) | 实现层 | Goal 交叉审计：只出意见到 `03-audit`，不改 status |

`commit` 不进工具集（便利可选、与治理正交，VP-004 入口面）。

## 消费方式（宿主示例）

MCP 客户端配置指向 `python <skills>/mcp/server.py`（stdio）。`tools/list` 发现四工具；
`tools/call` 返回结构化元数据（entrypoint/layer/role/readonly/prompt_path/guidance），
宿主据此 dispatch 到对应方法论正文（仓内 `skills/prompts/` 存在时可按 sha256 核对）。

## 实例真相

实例状态**永远在仓库内治理记录树**（`{governance_root}`，默认 `docs`）；本 server
不写任何治理状态，**不是**权威状态库。

## 测试与证据分级

- L1 MCP：`skills/tests/test_mcp_l1.py`（真启动 server 进程）。
- L1 File：`docs/tests/test_file_l1.py`（直接驱动 File 资产，不用 MCP mock）。
- L2 共享：`docs/tests/test_dual_channel_l2.py`（`kernel.check_equivalence` 两通道同断言）。
- 合同：`scripts/tests/test_contract_delivery_channels.py`（`deliveryChannel: files | mcp` 分列）。
- L3：承诺宿主抽稀真探针（`docs/releases/runtime/` 既有模式）。

## 目录

| 文件 | 内容 |
|------|------|
| `server.py` | MCP stdio server（JSON-RPC 2.0 over stdio；四治理工具 + install/upgrade/uninstall/doctor） |
| `entries.py` | 四入口映射纯数据（名称/参数边界/层级/角色边界单一真相源） |
| `kernel.py` | L2 共享等价内核（10 条检查点 + 两通道描述 + 同断言校验） |
| `lifecycle.py` | 薄壳 lifecycle：managed 标记、allowlist、默认确认写盘、CLI（R2 交付） |
| `doctor.py` | 只读安装状态报告（含 `governance_root` 解析与错误面）（R2/R3 交付） |
| `config.py` | `governance_root` 解析：默认 `docs`、`.goal-governance.json` pin、仓外 fail closed（R3 交付） |
| `governance-root.schema.json` | 项目配置 schema（随包分发） |
| `gitignore-fragment.txt` | 官方 ignore 片段（薄壳默认 gitignore） |

## 证据分级与 L3 边界

- L1 MCP = 真启动 server 进程的直接测试；L1 File = 直接驱动 File 资产（无 MCP mock）。
- L2 = `kernel.check_equivalence` 同一组断言驱动两通道；角色事实从两通道**真实资产独立提取**（File 侧读 prompt 正文短语，MCP 侧读 `tools/list` description 并解析层级前缀），其余检查点（台账边界、fail closed 声明、单愿景等）为协议 SSOT 防漂移断言。
- L3 = 承诺宿主抽稀真探针：覆盖四治理入口在宿主侧的 dispatch 与角色边界（File skill 面）；MCP stdio 客户端路径由 L1/L2 确定性覆盖。宿主 × MCP 通道的全链路长剧不在 R1 范围（VP-004 明确「不要求完整治理长剧 + 真模型全链路」）。
