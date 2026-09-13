"""Root ``AGENTS.md`` managed-block merge (GOAL-008 S4, model A).

User ruling D-009 / model A: the consumer repo owns its root ``AGENTS.md``; the
framework's rules live inside a delimited block (``goal-governance:begin
managed`` … ``end managed``).  Everything outside the markers is never touched,
so a consumer can keep its own agent rules in the same file.

The same markers are used by the MCP thin shell (``mcp/lifecycle.py``), so both
delivery channels converge on one block contract.

Compatible migration for already-installed repos: when the existing file is
byte-identical to the package copy (the whole-file install this replaces), the
content is wrapped in the managed block — the resulting bytes are equivalent and
no consumer content is lost.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MANAGED_BEGIN = "<!-- goal-governance:begin managed -->"
MANAGED_END = "<!-- goal-governance:end managed -->"

# Current markers are appended to the end of the file when no block exists yet.
DEFAULT_APPEND_NOTE = (
    "> 本文件由消费仓维护：`managed` 标记区间内的内容由目标治理框架更新，"
    "区间外内容不会被安装/更新改写。"
)


class MergeError(ValueError):
    """Raised when the managed block cannot be merged safely (fail closed)."""


def _norm_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def has_managed_block(text: str) -> bool:
    """True when the file already carries a complete balanced managed block."""
    if MANAGED_BEGIN not in text:
        return False
    try:
        validate_markers(text)
    except MergeError:
        return False
    return True


def validate_markers(text: str) -> None:
    """Fail closed on half-written or unbalanced blocks.

    Markers nest: shipped rule sources wrap their *whole* content in one pair
    while the rule text itself may contain another pair. Nesting lets the merge
    answer a question that a single pair cannot: is the file legacy (framework
    rules only) or already merged (consumer content + managed block)?
    """
    depth = 0
    position = 0
    while position < len(text):
        begin = text.find(MANAGED_BEGIN, position)
        end = text.find(MANAGED_END, position)
        if begin == -1 and end == -1:
            break
        if begin != -1 and (end == -1 or begin < end):
            depth += 1
            position = begin + len(MANAGED_BEGIN)
        else:
            depth -= 1
            if depth < 0:
                raise MergeError("managed block is malformed: end marker without begin")
            position = end + len(MANAGED_END)
    if depth != 0:
        raise MergeError("managed block is malformed: begin/end markers mismatch")


def extract_managed_block(source_text: str) -> str:
    """Return the outermost managed block (markers inclusive) from the source.

    A source without markers is entirely managed (legacy whole-file layout).
    """
    text = _norm_newlines(source_text)
    begin = text.find(MANAGED_BEGIN)
    if begin == -1:
        return text.strip("\n")
    validate_markers(text)
    depth = 0
    position = begin
    while position < len(text):
        next_begin = text.find(MANAGED_BEGIN, position)
        next_end = text.find(MANAGED_END, position)
        if next_begin == -1 and next_end == -1:
            break
        if next_begin != -1 and (next_end == -1 or next_begin < next_end):
            depth += 1
            position = next_begin + len(MANAGED_BEGIN)
            continue
        depth -= 1
        position = next_end + len(MANAGED_END)
        if depth == 0:
            return text[begin:position]
    raise MergeError("source managed block is not closed")


def _append_block(existing: str, block: str) -> str:
    text = existing
    if text and not text.endswith("\n"):
        text += "\n"
    if text and not text.endswith("\n\n"):
        text += "\n"
    return f"{text}{block}\n"


def block_payload(block: str) -> str:
    """The managed block without its outer marker lines."""
    lines = block.split("\n")
    if lines and lines[0].strip() == MANAGED_BEGIN:
        lines = lines[1:]
    if lines and lines[-1].strip() == MANAGED_END:
        lines = lines[:-1]
    return "\n".join(lines).strip("\n")


def _outer_frame(text: str) -> tuple[int, int] | None:
    """Bounds of the outermost managed block, or ``None`` when there is none.

    The frame is the widest balanced BEGIN…END span: rule-level pairs nested
    inside a wrapper are therefore not mistaken for the wrapper itself.
    """
    best: tuple[int, int] | None = None
    for index in range(len(text)):
        if not text.startswith(MANAGED_BEGIN, index):
            continue
        depth = 0
        position = index
        while position < len(text):
            next_begin = text.find(MANAGED_BEGIN, position)
            next_end = text.find(MANAGED_END, position)
            if next_begin == -1 and next_end == -1:
                break
            if next_begin != -1 and (next_end == -1 or next_begin < next_end):
                depth += 1
                position = next_begin + len(MANAGED_BEGIN)
                continue
            depth -= 1
            position = next_end + len(MANAGED_END)
            if depth == 0:
                if best is None or (position - index) > (best[1] - best[0]):
                    best = (index, position)
                break
    return best


def merge_agents_text(target_text: str, source_text: str) -> tuple[str, bool]:
    """Return ``(merged_text, changed)``. Never rewrites bytes outside markers.

    Nesting contract:
      * ``source_text`` is the shipped rule face. When it wraps its whole content
        in one marker pair, that outer pair is the managed block; a nested inner
        pair (the rule-level markers) is preserved verbatim inside it.
      * When the target already carries an *outer* frame, only that frame is
        rewritten; every other byte is kept (consumer rules coexist).
      * A target that is a pre-S4 whole-file install of these same rules is
        migrated to the marked form instead of having the block appended twice.
    """
    target = _norm_newlines(target_text)
    source = _norm_newlines(source_text)
    validate_markers(target)
    block = extract_managed_block(source)
    payload = block_payload(block)

    if target.strip() == "":
        # Fresh install: the package copy becomes the managed block.
        return f"{block}\n", True

    # Pre-S4 installs: the file *is* the rule face (with or without the old
    # rule-level pair). Migrate them to the marked form.
    if target.strip() == source.strip() or target.strip() == payload:
        marked = f"{block}\n"
        if target == marked:
            return target, False
        return marked, True

    frame = _outer_frame(target)
    if frame is not None:
        begin, end = frame
        if target[begin:end] == block:
            # Already converged: nothing to do.
            return target, False
        # A pre-S4 install of these same rules became "this frame, plus whatever
        # the consumer owned". When the frame's payload is still what the
        # package used to ship, migrating is loss-free: marked form plus the
        # surrounding bytes unchanged.
        if block_payload(target[begin:end]) == payload:
            merged = f"{target[:begin]}{block}{target[end:]}"
            if not merged.endswith("\n"):
                merged += "\n"
            return merged, True
        # The frame was hand-edited or holds an older payload: replace only the
        # block and keep every byte outside it.
        merged = target[:begin] + block + target[end:]
        if not merged.endswith("\n"):
            merged += "\n"
        return merged, True

    # Consumer owns this file: append the block, keep every existing byte.
    return _append_block(target, block), True


def merge_agents_file(
    source: Path,
    target: Path,
    *,
    dry_run: bool = False,
) -> dict[str, object]:
    """Merge ``source``'s managed block into ``target`` (creating it if absent)."""
    if not source.is_file():
        raise MergeError(f"framework AGENTS source not found: {source}")
    source_text = source.read_text(encoding="utf-8")
    existed = target.is_file()
    target_text = target.read_text(encoding="utf-8") if existed else ""
    merged, changed = merge_agents_text(target_text, source_text)
    if not changed:
        return {"status": "unchanged", "path": str(target), "existed": existed}
    if dry_run:
        return {"status": "would-merge", "path": str(target), "existed": existed}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(merged, encoding="utf-8", newline="\n")
    return {"status": "merged", "path": str(target), "existed": existed}


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge the goal-governance managed block into a consumer AGENTS.md"
    )
    parser.add_argument("--source", required=True, help="framework AGENTS.md template")
    parser.add_argument("--target", required=True, help="consumer repo AGENTS.md")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only report the status token",
    )
    args = parser.parse_args(argv)
    try:
        result = merge_agents_file(
            Path(args.source), Path(args.target), dry_run=args.dry_run
        )
    except MergeError as error:
        print(f"AGENTS.md merge failed (fail closed): {error}", file=sys.stderr)
        return 1
    status = str(result["status"])
    if args.quiet:
        print(status)
    else:
        label = {
            "unchanged": "Already present (managed block unchanged)",
            "would-merge": "Dry-run: would merge managed block",
            "merged": "Merged managed block",
        }[status]
        print(f"{label}: {result['path']}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(_main())
