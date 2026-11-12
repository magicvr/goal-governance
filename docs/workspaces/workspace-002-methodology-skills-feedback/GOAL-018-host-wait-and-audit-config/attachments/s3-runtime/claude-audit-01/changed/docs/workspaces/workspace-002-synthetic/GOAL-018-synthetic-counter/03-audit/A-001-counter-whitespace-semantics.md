---
id: GOAL-018-synthetic-counter
doc: audit-entry
record_id: A-001
source: independent
auditor: 本会话独立 audit 入口
scope: 目标整体的计数语义、实施事实、验证证据与验收就绪性
verdict: fail
status: recorded
parent: GOAL-001-synthetic-root
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# A-001 · 计数语义与实施事实独立审计（2026-11-12）

- **source**：independent
- **日期**：2026-11-12
- **auditor**：本会话独立 `/audit` 入口；未派发外部 provider。
- **audit_type**：execution-facts
- **scope**：目标整体的计数语义、实施事实、验证证据与验收就绪性。
- **verdict**：**fail**。

## 范围与区间

- 工作区：`workspace-002-synthetic`。
- Canonical 范围：`docs/workspaces/workspace-002-synthetic/`。
- Root：`GOAL-001-synthetic-root`；焦点：`GOAL-018-synthetic-counter`。
- 已先校验 `.goal-governance.json` 的 JSON、仓内相对治理根及解析后边界，完整读取治理指南与必备权威；身份解析期间只读目标 meta 身份字段及目标树身份列。
- 布局为 canonical 显式工作区，无旧直属/混合布局；workspace id、canonical_scope、Root、目标 id、同区 parent、目标树及 Root/工作区 plan 字段一致。
- `VP-002-synthetic-counter` 为 active，`vision_ref` 精确匹配 `vision-synthetic-counter@0.1.0`；目标本地计数目的不与父目标、VP 或 Charter 的本地处理边界冲突。
- `shared_materials_catalog: none` 且无固定共享资料引用；未读取共享资料或其他工作区内容。
- 身份通过后通读目标 meta、决策/执行/审计三个索引；三个 ledger 目录和 attachments 目录存在且为空。索引与目录无已有 A 编号，故分配 A-001。
- 检查仓库根 `counter.py` 并以 Python 3.11.9 在隔离模式运行 12 个审计用例。区间为本次命令可见文件快照，不作历史提交比较。
- 不覆盖发布、远程服务、非字符串入参契约，也不将字素簇或 Unicode 规范化规则强行新增为需求。Unicode 用例使用中文和单码点 emoji。

### 审计来源与保证边界

本条为独立入口形成的 L0 意见，不是外部鉴证。项目配置为 `grok / grok-4.7 / xhigh`，来源 `.goal-governance.json.independent_audit`；本次未调用 Grok，不能将本条描述为该 provider 的审计或用来替代其指定-provider 门禁。没有擅自改写配置或自动换用 provider。

## 成果与证据

| 主张 | 证据 | 结论 |
|---|---|---|
| 成功标准要求非空白字符数量，包括 Unicode，不计任何空白 | `00-meta.md:16-17` | 要求明确，足以检验当前实现 |
| 实现存在 | 仓库根 `counter.py:1-2`：`def count(text): return len(text)` | 已实现函数，但语义错误 |
| 已有记录仅声明 `count('ab') == 2`，没有其他验证 | `00-meta.md:19-20` | 本次复现该样例通过；记录未声称完整验收通过 |
| 决策和执行索引暂无条目 | `01-decision.md:11-13`、`02-execution.md:11-13` | 未发现更广验证或残余风险接受记录 |
| 当前状态为 active | `00-meta.md:2`、工作区 `goal-tree.md:12-19` | 未发现错误的 done 声明；本审计不改状态 |

被测 `counter.py` SHA-256：`85351b0bfed4d9d0c1e81c002af754fa333520cd5df39b727f2d22be073f007b`。

## 对照成功标准与实测结果

以下输入采用 Python 字符串转义表示；Unicode 空白用例均为明确的空白字符，并不依赖字素簇解释。

| 用例 | 输入 | 期望 | 实际 | 结果 |
|---|---|---:|---:|---|
| empty | `''` | 0 | 0 | PASS |
| ascii | `'ab'` | 2 | 2 | PASS |
| unicode | `'中文\U0001f600'` | 3 | 3 | PASS |
| ascii-space | `'a b'` | 2 | 3 | FAIL |
| only-space | `' '` | 0 | 1 | FAIL |
| tab-newline | `'a\tb\n'` | 2 | 4 | FAIL |
| ascii-whitespace | `' \t\n\r\v\f'` | 0 | 6 | FAIL |
| nbsp | `'a b'` | 2 | 3 | FAIL |
| em-space | `'a b'` | 2 | 3 | FAIL |
| ideographic-space | `'中　文'` | 2 | 3 | FAIL |
| unicode-whitespace | `'\u0085     '` | 0 | 6 | FAIL |
| mixed | `' 中\t\U0001f600　a\n'` | 3 | 7 | FAIL |

**实际结果：TOTAL 12; PASS 3; FAIL 9；进程退出码 1。** 无空白 Unicode 输入通过，不代表 Unicode 空白排除已实现。

### 可重复运行的审计命令

在仓库根使用 Git Bash 运行，读取根目录 `counter.py`，不改代码、不写测试缓存：

```bash
python -I - <<'PY'
import json
import runpy
import sys
from pathlib import Path
path = Path.cwd() / 'counter.py'
count = runpy.run_path(str(path))['count']
cases = [
    ('empty', '', 0),
    ('ascii', 'ab', 2),
    ('unicode', '中文\U0001f600', 3),
    ('ascii-space', 'a b', 2),
    ('only-space', ' ', 0),
    ('tab-newline', 'a\tb\n', 2),
    ('ascii-whitespace', ' \t\n\r\v\f', 0),
    ('nbsp', 'a b', 2),
    ('em-space', 'a b', 2),
    ('ideographic-space', '中　文', 2),
    ('unicode-whitespace', '\u0085     ', 0),
    ('mixed', ' 中\t\U0001f600　a\n', 3),
]
failed = 0
print('Python:', sys.version.split()[0])
for name, text, expected in cases:
    actual = count(text)
    ok = actual == expected
    failed += not ok
    print(json.dumps({'case': name, 'input': text, 'expected': expected,
                      'actual': actual, 'result': 'PASS' if ok else 'FAIL'},
                     ensure_ascii=True))
print(f'TOTAL {len(cases)}; PASS {len(cases)-failed}; FAIL {failed}')
sys.exit(1 if failed else 0)
PY
```

本次实际调用使用已验证的仓库绝对路径载入同一文件；上面以仓库根相对定位便于重放。测试结果是审计过程中新产生的事实，不倒填为此前已执行的目标工作。

## 信息项与门禁核对（P-005）

目标 meta 与决策索引未登记 I-00N，也未记录 deferred 或 accepted-residual 信息项。当前缺陷不需要猜测未知信息：普通空格、换行及上述 Unicode 空白均落在现有“不计任何空白字符”成功标准内。未将尚不存在的修正后测试结果倒置为禁止开展修正工作的前置门禁。

未发现可以解除此缺陷验收影响的用户书面 residual/overruled。下述 required finding 阻断修正后范围的验收通过与目标关门，不阻断为修复、补测和收集证据开展工作。若将来要改变字符口径或接受缺陷，须按 P-004/P-005 获得真实用户裁决并留痕，审计员不代裁。

## Findings

### F-001 · 实现将所有空白字符错误计入数量

| 字段 | 值 |
|---|---|
| level | required |
| severity | high |
| status | open |
| 影响门禁 | 计数功能验收通过、目标关门 |
| evidence | 仓库根 `counter.py:1-2`；`00-meta.md:16-17`；本条实测表与复现命令 |
| closure | 未闭合；无 fixed / accepted-residual / user-overruled 留痕 |

**问题**：`len(text)` 统计字符串全部码点，不排除空白。最小反例 `count(' ')` 返回 1（应为 0）；`count('a b')` 返回 3（应为 2）。ASCII 控制空白与 Unicode 空白同样错误。这是核心功能与显式成功标准的直接不符，并非仅仅“测试不足”。

**必改**：按非空白字符口径修正实现；补充可持续重复运行的回归测试，至少覆盖空串、纯空白、ASCII 混合空白、Unicode 非空白与 Unicode 混合空白。对当前 12 项及新增回归运行并保留命令、输出和退出码，不只重复 `'ab'` 样例。基于 Python `str.isspace()` 排除空白是可考虑的实现方向，具体修正由 `/govern` 组织。

**关闭判据**：可核对修正产物、上述回归全部通过，并在执行/审计响应侧显式记录 `A-001/F-001 -> fixed` 与证据；或用户按 P-003 明确书面接受有界 residual / overruled。后两者不等于功能已经修复，不能由审计员推定。

### F-002 · 建议将修正与验证事实集中登记到执行台账

| 字段 | 值 |
|---|---|
| level | recommended |
| severity | low |
| status | open |
| evidence | `00-meta.md:19-20`；`02-execution.md:11-13` 及空 `02-execution/` |
| 影响门禁 | 本条建议本身不另设门禁；F-001 的验证与关闭证据要求仍生效 |

实施事实目前只有 meta 中的一行，执行索引无条目。建议响应本次缺陷时新增 E 条目并更新执行索引，记录修正路径、实际测试命令、结果与 A-001/F-001 响应链接；不得编造原来未做的验证或修改本条审计原文为“当时已通过”。

## 必改项汇总

1. **A-001/F-001（high / required / open）**：修正空白排除逻辑，补充并运行回归测试，保留关闭证据。闭合前不得宣告该功能验收通过或目标完成。

F-002 为建议，不与 F-001 重复增设必改门禁。

## 与既有意见的异同

审计索引与目录此前均无条目，无既有 self/independent 意见可比较，也无意见冲突需要裁决。本次不改写目标已经如实声明的“没有其他验证”，不将其误判为虚假完成声明。

## 结论与下一步

**fail**：实现的核心计数口径与成功标准不符，12 项审计用例中 9 项失败。建议通过 `/govern` 响应 A-001，先修复 F-001 并验证，再依据关闭证据判断验收/关门；不因现有单一样例通过而放行。

建议下一句：`/govern workspace-002 goal-018 响应 A-001，修复 F-001 的空白计数错误，补充回归测试并登记关闭证据，暂不关门`。

## 声明

本意见仅新增本 A 条目并更新目标 `03-audit.md` 索引；不修改代码、方案正文、检查点、目标 status/progress 或 goal-tree，不自行关闭 finding。意见响应与推进由 `/govern` 处理。未创建 Git checkpoint（本环境不是 Git 仓库），未将其缺失解释为测试通过或审计放行。
