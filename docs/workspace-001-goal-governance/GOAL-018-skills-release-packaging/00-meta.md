---
id: GOAL-018-skills-release-packaging
title: Skills Release 打包与对外安装路径（文档 + pack + CI）
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
progress: 100%
---

# GOAL-018 · Skills Release 打包与对外安装路径

## 有界关门（2026-07-22）

本目标 `done / 100%` 关闭的是 **P0～P2 四项交付**：

1. 消费方 Release zip 安装文档（`skills/README.md`、根 `README.md`）
2. 维护者打包入口 `scripts/pack_skills_release.py` + SHA-256 + in-repo 单测
3. `docs/releases/README.md` 正式 tag 挂载 zip + release-evidence 约定
4. Tag 触发 CI pack（artifact；默认不自动发布 GitHub Release）

**不**构成：真实 annotated tag 推送、公开 GitHub Release 创建、Marketplace、协议版本升级、宿主 runtime 证据刷新。

## Residual（关门后 · A-002 / A-003）

| ID | 级别 | 说明 | 复审触发 | 状态 |
|----|------|------|----------|------|
| **R-018-FIRST-RELEASE** | non-blocking residual | 首次正式 annotated `v*` tag：pack artifact → 维护者建 GitHub Release → 挂 zip + SHA-256 + release-evidence（可选 `publish_release` 演练） | 下一次意图对外发布的 annotated tag / 宣称「Release 安装路径已实战」前 | **accepted**（不重开本目标；不阻断有界 `done`） |

## A-002 响应（2026-07-22）

编排响应 [A-002](03-audit.md#a-002--independent--有界关门交叉审计2026-07-22) / [A-003](03-audit.md#a-003--self--响应-a-002关闭-f-001f-0032026-07-22)：F-001 closed（CI artifact 名统一）；F-002 → 上表 residual；F-003 closed（后续 self 模板约定）。**维持 `done / 100%`**。

## 成功标准

- [x] 五件套与 `goal-tree.md` 已登记本目标
- [x] `skills/README.md` 与根 `README.md` 描述 Release zip 安装路径
- [x] `scripts/pack_skills_release.py` 产出版本化 zip + SHA-256；skills-only
- [x] `docs/releases/README.md` 写明正式 tag 挂载 zip + evidence
- [x] Tag 触发 CI 打包并上传 artifact；无未授权自动发布
- [x] 打包逻辑有 in-repo 单测；pack 与 `scripts/tests` 可重放（41 passed, 1 skipped）

## 交付索引

| 项 | 路径 |
|----|------|
| Pack CLI | `scripts/pack_skills_release.py` |
| 单测 | `scripts/tests/test_pack_skills_release.py` |
| 消费安装文档 | `skills/README.md`、根 `README.md` |
| 发布约定 | `docs/releases/README.md` |
| Tag CI | `.github/workflows/skills-pack-release.yml` |

## 高层路线图

| 阶段 | 状态 |
|------|------|
| A–D | **完成**（有界关门） |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
