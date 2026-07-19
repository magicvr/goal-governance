# 发布证据

本目录定义阶段 5 的发行证据格式，而不是新的目标状态源。

- canonical 兼容性声明仍位于 `docs/contracts/skills-consumer-contract.json`；兼容矩阵位于 `docs/contracts/skills-consumer-compatibility-matrix.json`。
- CI 使用 `scripts/compatibility_report.py` 与 `scripts/release_evidence.py` 生成 JSON 报告、测试结果和 SHA-256 清单，并将其作为 workflow artifact 或 release attachment 保存。运行了检查时，任一检查失败会让命令和 CI 失败；报告文件仍会保留失败事实。
- `release-evidence.schema.json` 描述并约束证据格式。`rehearsal` 证明一条可重放路径被执行，不等同于 GitHub Release；`release-candidate` 仅在 annotated `vMAJOR.MINOR.PATCH` tag 指向 HEAD、矩阵 `candidateRevision` 与该 tag 一致、工作树干净、CHANGELOG 有同版本节、兼容矩阵无未覆盖 required 单元且全部检查通过时生成。
- 检查结果只能由 `release_evidence.py` 内部执行并记录，API/CLI 都不接受调用方注入的“已通过”结果；传入的 compatibility report 必须与当前 HEAD 重新生成的 source、contract、matrix、mirror 与 coverage 全部一致。
- rehearsal 命令：`python scripts/release_evidence.py --mode rehearsal --run-checks --include-web --output artifacts/release-evidence.json`。发布候选命令在维护者创建 annotated tag 后改用 `--mode release --tag vX.Y.Z`；该命令只生成证据，不推送 tag、不创建 GitHub Release。
- 创建或推送 tag、发布 GitHub Release、以及确认真实宿主 runtime 证据均须维护者授权。自动化不得把缺少这些动作的工作树写成已发布。
