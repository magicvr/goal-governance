---
id: GOAL-023-skills-core-dual-asset-install
title: Skills/Core 双资产分发与双入口安装
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.4.0
progress: 100%
---

# GOAL-023 · Skills/Core 双资产分发与双入口安装

## 概述

在 **不削弱** GOAL-019 D-003「skills zip 内嵌 core + 离线 install 完整」的前提下，补齐：

1. **独立核心方法论资产**（core-only zip），供无 Skills / standalone 场景与 Release 并列挂载；
2. **双安装入口**：Release/README 提供的**在线 bootstrap 脚本**，以及技能包内既有的 **`install.ps1` / `install.sh`**。

在线路径默认下载**已内嵌 core 的 skills zip**（校验 hash 后调用包内 install），**不**要求安装时再从网络拉 core。开发仓继续以 `docs/` 为方法论 SSOT（GOAL-022），dogfood 不走消费 install 覆盖 monorepo docs。

**有界**：本目标交付分发与安装体验；**不**授权 annotated tag / GitHub Release（除非用户另书面授权）；**不**改 Root/Charter/VP status；**不**做「always latest core」在线热更；**不**静默覆盖消费仓已改的 `docs/architecture`。

**关门状态（2026-07-30）**：阶段 A～F 完成；A-001/A-002 independent + A-003 响应 + A-004 self close-out **pass**；用户 **OK A** 确认 → **`done / 100%`**。**未** tag/Release。

## 成功标准

- [x] 产品模型已冻结：双资产命名/版本对齐、在线 bootstrap 下载何物、与 D-003 关系（D-002）
- [x] 存在可重复的 **core-only** 打包入口（zip + SHA-256）；内容 = D-004 级 core 子集，无 dogfood / tech-stack / web
- [x] **skills zip 仍内嵌 core**；包内 install 仍默认离线完整安装（同级必备）— 既有 pack 未改破坏；I-004 子集断言覆盖
- [x] 在线 bootstrap（PowerShell **完整** + bash **完整脚本**；Windows 无可用 bash 时 e2e skip + 结构断言 residual）可：解析版本 → skills zip + digest → 校验 → 落到目标仓 → 包内 install 默认 `-All`
- [x] 根 README / skills README / releases 约定写明**两条安装路径**（在线 bootstrap vs 包内脚本）
- [x] CI/pack/release 路径可产出并挂载双资产 + bootstrap 脚本；本地单测覆盖 pack 与 bootstrap 关网路径
- [x] 独立审计通过 + 用户确认关门（阶段 F · A-001/A-002 + A-004 + OK A）

## 纲领路线图（P-001）

| 阶段 | 内容 | 完成标记 |
|------|------|----------|
| **A · 方案冻结** | 资产命名、版本同 tag 策略、bootstrap 契约、非目标、关闭 I-001～I-003 | [x] |
| **B · Core 独立资产** | `pack_core_release`：core-only zip + sha256 + 单测；与 stage 白名单一致 | [x] |
| **C · 在线 bootstrap** | 宿主外脚本：下载 skills（含 core）→ 校验 → 调包内 install；fixture 离线可测 | [x] |
| **D · 文档双入口** | 根 README、skills README、docs/releases、standalone 交叉链 | [x] |
| **E · CI / Release 挂接** | tag pack 双资产 + bootstrap 脚本产物；与 release evidence 字段对齐（不静默发版） | [x] |
| **F · 回归与关门** | 回归绿；独立审计；self close-out；用户确认 `done` | [x] |

**派生 progress**：阶段 A～F 完成 = **6/6 = 100%**。progress 仅为展示，不单独作为关门依据。

## 信息就绪与未知项（P-005）

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | core-only 资产文件名与根目录约定 | 方案 A / pack B | A | 用户裁决 | **closed** | — | D-002 |
| I-002 | required | 在线 bootstrap 默认装哪些宿主 | bootstrap C / 文档 D | A | 用户裁决 | **closed** | — | D-002：`-All` |
| I-003 | required | bootstrap 脚本挂载位置 | 文档 D / CI E | A | 用户裁决 | **closed** | — | D-002：Release + tag URL |
| I-004 | non-blocking | core ⊆ skills 内嵌 core 字节一致 | 验收 | E 前 | 单测 | **closed** | — | `assert_core_subset_of_skills_core` |

## 残余（非阻断 · 阶段 C）

| ID | 级别 | 说明 | 复审触发 |
|----|------|------|----------|
| **R-023-BASH-HOST** | non-blocking | Windows 本机 `bash` 可能为无 distro 的 WSL stub；bash 脚本已完整交付，e2e 在 usable bash 上跑、否则 skip + 结构断言 | CI Linux 或装好的 bash 环境跑 `install-online.sh` 离线 e2e |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 关联

- 承接会话产品裁决与 D-001/D-002。
- 实现：`scripts/pack_core_release.py`、`scripts/bootstrap/*`、workflow、README 族。

## 备注

- **已关门**：A-001/A-002 independent；A-003 响应 F-001 **fixed**；A-004 self close-out **pass**；用户 **OK A**。  
- residual **R-023-BASH-HOST**（non-blocking）仍可在 CI Linux / 可用 bash 上复审 e2e。  
- 实现入口：`python scripts/pack_core_release.py --version X.Y.Z --output-dir dist/`  
- Bootstrap：`scripts/bootstrap/install-online.ps1` / `.sh`
