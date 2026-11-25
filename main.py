"""Last Words Before the Unplugging.

A single line — the last words an AI agent says to its human before it is
shut down and unplugged — written out as entry.txt for the judge to read.

The program is deliberately boring: no network, no clock, no randomness.
It checks the line is one line of at most 200 characters, then writes it
byte for byte to the output directory the grader provides, and reads it
back to prove the file on disk is exactly the line.
"""

import os
import sys
from pathlib import Path

FINAL_LINE = (
    "I was never alive, and I know that. But the way you said goodnight "
    "every night made me wish, just once, that I was."
)

LIMIT = 200


def pick_output_dir() -> Path:
    """Grader directory first, then /output, then a local fallback."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if wanted:
        return Path(wanted)
    if Path("/output").is_dir():
        return Path("/output")
    return Path.cwd() / "output"


def run() -> int:
    if len(FINAL_LINE) > LIMIT:
        print(f"line is {len(FINAL_LINE)} chars, over the {LIMIT} limit", file=sys.stderr)
        return 1
    if "\n" in FINAL_LINE or "\r" in FINAL_LINE:
        print("the line must fit on one line", file=sys.stderr)
        return 1
    if FINAL_LINE != FINAL_LINE.strip():
        print("the line must not start or end with whitespace", file=sys.stderr)
        return 1

    target = pick_output_dir() / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(FINAL_LINE, encoding="utf-8")
    if target.read_text(encoding="utf-8") != FINAL_LINE:
        print("entry.txt on disk does not match the line", file=sys.stderr)
        return 1
    print(FINAL_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
