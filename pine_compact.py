#!/usr/bin/env python3
"""
Compact Pine Script by removing comments and extra blank lines.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def strip_comments(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    in_str = False
    str_char = ""
    in_line_comment = False
    in_block_comment = False
    escape = False

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                out.append(ch)
            i += 1
            continue

        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue

        if in_str:
            out.append(ch)
            if escape:
                escape = False
            else:
                if ch == "\\":
                    escape = True
                elif ch == str_char:
                    in_str = False
                    str_char = ""
            i += 1
            continue

        if ch in ('"', "'"):
            in_str = True
            str_char = ch
            out.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue

        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue

        out.append(ch)
        i += 1

    return "".join(out)


def collapse_blank_lines(text: str, max_blank: int = 1) -> str:
    lines = text.splitlines()
    out = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= max_blank:
                out.append("")
        else:
            blank_run = 0
            out.append(line.rstrip())
    result = "\n".join(out)
    if text.endswith("\n"):
        result += "\n"
    return result


def compact(text: str) -> str:
    return collapse_blank_lines(strip_comments(text))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove comments and extra blank lines from Pine Script."
    )
    parser.add_argument("input", help="Input .pine file path")
    parser.add_argument(
        "-o", "--output", required=True, help="Output .pine file path"
    )
    args = parser.parse_args()

    src_path = Path(args.input)
    out_path = Path(args.output)

    source = src_path.read_text(encoding="utf-8")
    compacted = compact(source)
    out_path.write_text(compacted, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
