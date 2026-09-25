#!/usr/bin/env python3
"""Run the same snapshot-backed suite on every supported parser target."""

import argparse
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("native", "js", "wasm", "wasm-gc")
SUMMARY = re.compile(r"Total tests: (\d+), passed: (\d+), failed: (\d+)\.")


def run_suite(target, package=None):
    command = ["moon", "test", "--target", target, "--no-render"]
    if package:
        command.extend(("-p", package))
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    match = SUMMARY.search(completed.stdout + completed.stderr)
    if completed.returncode or not match:
        tail = "\n".join((completed.stdout + completed.stderr).splitlines()[-30:])
        raise RuntimeError(f"{target} suite failed (exit {completed.returncode}):\n{tail}")
    total, passed, failed = map(int, match.groups())
    if total != passed or failed:
        raise RuntimeError(f"{target} suite incomplete: {match.group()}")
    return total


def run_example(target):
    command = [
        "moon", "run", "-q", "--target", target,
        "src/examples/library_usage",
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"{target} library example failed:\n{completed.stderr[-2000:]}"
        )
    return completed.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--async-readme", action="store_true",
        help="also download and verify the pinned async@0.22.2 README",
    )
    parser.add_argument(
        "--source", type=Path,
        help="verify a locally saved async README instead of downloading it",
    )
    args = parser.parse_args()
    totals = {target: run_suite(target) for target in TARGETS}
    renderer = {
        target: run_suite(target, "moonbit-community/cmark/cmark_html")
        for target in TARGETS
    }
    if len(set(renderer.values())) != 1:
        raise RuntimeError(f"renderer test totals differ: {renderer}")
    # src/cmark_cli is native-only and currently contributes three tests.
    if totals["native"] != totals["js"] + 3 or len(
        {totals[target] for target in TARGETS[1:]}
    ) != 1:
        raise RuntimeError(f"unexpected target coverage difference: {totals}")
    for target, total in totals.items():
        print(f"{target:7} {total}/{total} passed; renderer {renderer[target]}/{renderer[target]}")
    outputs = {target: run_example(target) for target in TARGETS}
    if len(set(outputs.values())) != 1:
        raise RuntimeError("library example HTML differs across backends")
    if outputs["native"].count('type="checkbox"') != 2 or outputs["native"].count("<ul>") != 2:
        raise RuntimeError("library example lost nested task structure")
    print("library example: identical nested-task XHTML on all four targets")
    if args.async_readme or args.source:
        command = [sys.executable, str(ROOT / "scripts/check_async_readme.py")]
        if args.source:
            command.extend(("--source", str(args.source.resolve())))
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
