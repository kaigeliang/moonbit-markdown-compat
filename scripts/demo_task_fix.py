#!/usr/bin/env python3
"""Show the original Markdown and a real baseline-to-current HTML diff."""

import difflib
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/task-list.md"
BASELINE = ROOT / "examples/task-list.baseline.html"


def main():
    source = SOURCE.read_text()
    before = BASELINE.read_text()
    command = [
        "moon", "run", "-q", "--target", "native", "src/cmark_cli", "--",
        "--relaxed", str(SOURCE),
    ]
    after = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, check=True,
    ).stdout
    if before == after:
        raise AssertionError("baseline and current render are identical")
    if after.count('type="checkbox"') != 4 or after.count("<ul>") != 3:
        raise AssertionError("current render lost the expected child lists")
    print("Markdown source:\n" + source)
    print("Baseline: 452c95f; current: local checkout")
    print("".join(difflib.unified_diff(
        before.splitlines(keepends=True), after.splitlines(keepends=True),
        fromfile="452c95f HTML", tofile="current HTML",
    )))
    print("Verification: four task nodes; two nested child lists")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(f"demo failed: {error}", file=sys.stderr)
        sys.exit(1)
