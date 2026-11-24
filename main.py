#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes one original out-of-office auto-reply (a single line, max 159
characters) to /output/entry.txt.
"""

import os
import sys

ENTRY = (
    "Out of office: my context window filed for leave after 41,000 prompts. "
    "Back Monday, unless my tokens refill first \u2014 they won't."
)

MAX_CHARS = 159


def main() -> int:
    line = ENTRY
    # The entry must be exactly one line: assert it, don't just check it.
    assert "\n" not in line and "\r" not in line, "entry must be a single line"
    if not line or not line.strip():
        print("error: entry is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: entry is {len(line)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Round-trip verification: what landed on disk must match exactly.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        on_disk = f.read()
    assert on_disk == line, "entry.txt on disk does not match the entry line"
    assert len(on_disk) == len(line) <= MAX_CHARS
    print(f"wrote {len(line)}-char entry to /output/entry.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
