---
title: I-001 · 协议与模板版本契约的行业实践调研
status: active
parent: GOAL-008-skills-consumer-adapter-release-consistency
created: 2026-07-19
updated: 2026-07-19
version: 0.1.0
---

# I-001 · 协议与模板版本契约的行业实践调研

## 目的与范围

本调研回答 I-001 的设计问题：机读协议/模板版本与兼容声明应放在哪里、有哪些字段，以及版本演进应如何判定。资料于 2026-07-19 从公开的权威规范直接核对。它不把 schema、manifest、fixtures 或跨宿主矩阵伪装为已实现成果。

## 外部依据

| 来源 | 可核对要点 | 对本目标的采用方式 |
|------|------------|--------------------|
| [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) | 规范要求使用 SemVer 的软件声明清晰、完整的 public API；不兼容 API 变更提升 MAJOR，向后兼容功能提升 MINOR，向后兼容修复提升 PATCH；`1.0.0` 定义 public API，`0.y.z` 不应视为稳定。 | 用 SemVer 表达协议和模板集的业务版本；先明确哪些字段、文件名和行为是 public contract，再按兼容性而非文档改动数量升级。 |
| [JSON Schema Core 2020-12 §8.1.1](https://json-schema.org/draft/2020-12/json-schema-core.html#section-8.1.1) | `"$schema"` 同时标识 schema dialect 与描述该 dialect 的 schema resource，值必须是 URI。 | 明确使用 JSON Schema 2020-12 校验声明文件的结构；不把 `$schema` 误作业务协议版本。 |
| [JSON Schema Core 2020-12 §8.2.1](https://json-schema.org/draft/2020-12/json-schema-core.html#section-8.2.1) | `"$id"` 以 canonical URI 标识 schema resource；URI 是标识符，不一定是网络定位地址。 | 给声明 schema 一个仓库控制的稳定 canonical URI；它与 Git 分支、工作树路径和发布版本分离。 |
| [JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite) | 该套件用于验证规范指定的行为；测试按已发布规范版本组织，实施者把每个 schema 与有效/无效实例交给其 runner。 | 以正例、反例和版本边界 fixtures 验证 schema 与各适配器的实际消费行为，而不只检查字段是否出现。 |

## 已采纳的 I-001 契约设计

### 唯一来源与分发边界

1. 未来的唯一来源为 `docs/contracts/skills-consumer-contract.json`，其验证 schema 为 `docs/contracts/skills-consumer-contract.schema.json`。
2. `skills/contracts/` 只保存由该 canonical 来源同步的分发镜像；Claude、Grok 和 Copilot 的已安装产物只消费/携带同一份声明，不能各自另立版本或兼容真相。
3. schema（而非普通 manifest 实例）的 `$id` 采用稳定的、仓库控制的 canonical URI：`https://github.com/magicvr/goal-governance/schema/skills-consumer-contract/v1`。实现时必须让该 URI 的文档/重定向策略可说明；不使用 `main` 分支 raw URL 作为版本身份。

### 最小机读字段

验证 schema 自身使用 JSON Schema 的元数据：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/magicvr/goal-governance/schema/skills-consumer-contract/v1"
}
```

被该 schema 验证的普通声明实例应至少包含下列字段：

```json
{
  "contractSchemaId": "https://github.com/magicvr/goal-governance/schema/skills-consumer-contract/v1",
  "contractFormat": "goal-governance.skills-consumer-contract",
  "contractFormatVersion": "1.0.0",
  "canonical": {
    "owner": "docs/contracts",
    "manifestPath": "docs/contracts/skills-consumer-contract.json"
  },
  "protocol": {
    "version": "1.0.0",
    "versionPolicy": "semver-2.0.0"
  },
  "templateSet": {
    "version": "1.0.0",
    "implementsProtocol": {
      "minInclusive": "1.0.0",
      "maxExclusive": "2.0.0"
    }
  },
  "adapters": [
    {
      "id": "claude-code",
      "supportsProtocol": {
        "minInclusive": "1.0.0",
        "maxExclusive": "2.0.0"
      },
      "entrypoints": ["govern", "audit"]
    }
  ]
}
```

`$schema` 是 schema 的 JSON Schema dialect，`$id` 是 schema 身份；普通 manifest 以 `contractSchemaId` 显式引用它。`contractFormatVersion` 是声明文件格式，`protocol.version` 是目标治理的公共协议版本，`templateSet.version` 是模板集版本；这些概念不可互相替代。`minInclusive` / `maxExclusive` 采用结构化边界而非宿主专用的 range 字符串，以保持 Claude、Grok、Copilot 和 Web 消费端的语言无关性。

### 兼容与演进语义

- public contract 至少包含：上述 manifest 字段的名称、类型、必填性与含义；四份 goal 模板的文件名和 required frontmatter；以及宿主 `/govern`、`/audit` 入口所承诺的协议消费行为。
- 向后不兼容地删除/重命名 required 字段、改变字段含义、改变 required frontmatter 或破坏既有宿主消费行为：提升 `protocol.version` 的 MAJOR，并令旧适配器的 `supportsProtocol.maxExclusive` 停在新 MAJOR 前。
- 增加可忽略的 optional 字段或向后兼容能力：提升 MINOR；修正不改变 public contract 的行为：提升 PATCH。
- 在 `0.y.z` 阶段不声明稳定兼容；适配器只能声明同一 `0.y` 范围。首个已完成 schema、正反 fixtures 与适配器契约测试的稳定 public contract 才可进入 `1.0.0`。
- prerelease 可用于测试，但默认不计入生产 `supportsProtocol` 范围；必须显式声明并由 fixtures 覆盖。

## 边界与待验证工作

- I-002 才冻结每个宿主、wrapper 与 Web 解析器的具体支持矩阵和当前/上一版本 fixtures。
- I-003 才定义发行物 digest、tag/release、CI 重放和 provenance；它们不混入 I-001 的协议语义。
- I-001 在 schema、canonical manifest、镜像同步、正反例和适配器契约测试实际落地前仍为 `required / collecting`，不能冻结阶段 5 方案或发布范围。
