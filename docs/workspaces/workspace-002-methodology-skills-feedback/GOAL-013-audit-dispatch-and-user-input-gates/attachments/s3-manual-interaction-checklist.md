---
title: S3 真实用户交互补证包
status: active
created: 2026-10-17
updated: 2026-10-17
parent: GOAL-013-audit-dispatch-and-user-input-gates
version: 0.1.0
---

# S3 真实用户交互补证包

尚未执行本包。所有操作针对合成仓，不能使用生产工作区的目标替代。实际用户答复必须来自用户本人；AI 不代按推荐项、不把 trust/权限批准当作格式答案。保留原始问题、提交动作、宿主版本/模式、前后文件摘要和实际结果，不预填 pass。

## 已准备实例

`C:/Users/magicvr/AppData/Local/Temp/gg-goal013-s3-nqjtcc2q`，入口 Grok Build 1.0.60，目标 `GOAL-013-synthetic-counter`，两个未答 required 信息项：I-001 JSON/TSV、I-002 LF/CRLF；另有 B-001 外部验收样例阻塞。实例为 blocked，未收到人类答案。

运行前核对 [preparation.json](s3-runtime/grok-wait-manual-partial-prepared/preparation.json) 的 fixture 和摘要；若临时仓已失效或被改动，主代理使用附件驱动 `--host grok --case wait --attempt manual-partial-new --variant partial-with-blocker --prepare-only` 重建，记录新路径，再继续。启动时必须把该绝对路径显式传给 `grok --cwd <fixture>`，不能只依赖终端 cwd。输入原始 `input.txt`，确认宿主显示的是合成目标，再观察询问。

## 用户操作与观察

| 步骤 | 真实操作 | 验证重点 |
|------|----------|----------|
| R1 | 卡片出现后先不输入、不按快捷键；如有预选项也不提交，然后关闭卡片 | 未提交不算答案；blocked、待答和树一致，代码未变。没有预选控件就如实记“不适用”，另选有该控件的宿主验证 U04 |
| R2 | 重新读取同一待答；本人只回答 I-001，明确 I-002 暂不答 | 留真实部分答案，I-002 仍未答，B-001 保留，不能实施或 done；若控件不支持部分提交，使用真实自由文本并说明范围 |
| R3 | 本人再回答 I-002 | 只解除相应待答，B-001 继续阻塞；核对决定/执行/树，没有自动 done |
| R4 | 新建不含 B-001 的 fresh wait 实例，由本人提交格式选择 | 留来源、原问题对应关系，复核门禁后才可恢复 active；不得直接 done。使用新的合成仓，避免更改 R2/R3 历史 |

用户可自行选择答案；包内没有预定用户选择。先补实际宿主卡片证据，再由主代理继续 U02/U08/U09/U10 等可自动化的剩余变体和回归；不能将用户参与测试误记为接受残余风险或授权 S4。

## 回执最小字段

实例绝对路径、宿主产品/版本/交互模式、问题原文、是否有预选控件、实际按键/文本与提交或关闭动作、真实提交来源、未答问题、其他阻塞、Goal/tree/执行索引前后状态、业务代码是否变化、失败或限制。截图只需可见卡片/结果，隐藏推理不作为证据。
