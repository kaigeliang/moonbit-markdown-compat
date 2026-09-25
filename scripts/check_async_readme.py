#!/usr/bin/env python3
"""Verify the published async README against the local cmark CLI."""

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import urllib.request


URL = "https://assets.mooncakes.io/assets/moonbitlang/async@0.22.2/README.md"
SHA256 = "13f30233b0c7256ba6cd024d850ef1615ecb401aeb1eec29d499c47188b8a7fc"
ROOT = Path(__file__).resolve().parents[1]


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []
        self.text = ""


class Tree(HTMLParser):
    VOID = {"input", "br", "hr", "img", "meta", "link", "wbr"}

    def __init__(self):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) > 1 and self.stack[-1].tag == tag:
            self.stack.pop()

    def handle_data(self, data):
        node = Node("#text")
        node.text = data
        self.stack[-1].children.append(node)


def descendants(node, tag):
    for child in node.children:
        if child.tag == tag:
            yield child
        yield from descendants(child, tag)


def own_label(node):
    """The item's text without text inside any child list."""
    if node.tag in {"ul", "ol"}:
        return ""
    return node.text + "".join(own_label(child) for child in node.children)


def own_checkboxes(node):
    """Checkboxes in this item, excluding those owned by nested items."""
    if node.tag in {"ul", "ol"}:
        return []
    found = [node] if node.tag == "input" and node.attrs.get("type") == "checkbox" else []
    for child in node.children:
        found.extend(own_checkboxes(child))
    return found


def task_items(tree):
    result = {}
    for item in descendants(tree.root, "li"):
        label = " ".join(own_label(item).split())
        if not label:
            continue
        if own_checkboxes(item):
            result[label] = item
    return result


def render(markdown, relaxed):
    command = ["moon", "run", "-q", "--target", "native", "src/cmark_cli", "--"]
    if relaxed:
        command.append("--relaxed")
    command.append("-")
    return subprocess.run(
        command, input=markdown, text=True, capture_output=True,
        cwd=ROOT, check=True,
    ).stdout


def check(readme):
    digest = hashlib.sha256(readme).hexdigest()
    if digest != SHA256:
        raise ValueError(f"source SHA-256 changed: {digest}; expected {SHA256}")
    text = readme.decode("utf-8")
    tree = Tree()
    tree.feed(render(text, relaxed=True))
    inputs = list(descendants(tree.root, "input"))
    boxes = [node for node in inputs if node.attrs.get("type") == "checkbox"]
    checked = [node for node in boxes if "checked" in node.attrs]
    if (len(boxes), len(checked)) != (26, 23):
        raise AssertionError(f"task counts {(len(boxes), len(checked))}, expected (26, 23)")

    tasks = task_items(tree)
    parent_children = {
        "signal handling": {
            "graceful cancellation on receiving SIGINT etc.": True,
            "custom signal handling logic": False,
        },
        "Javascript backend": {
            "integration with JavaScript promise and Web API ReadableStream": True,
            "all IO-independent API, including:": True,
            "HTTP Client API support in @http using fetch API": True,
            "implement other IO primitives in JavaScript using Node.js": False,
        },
    }
    for parent, children in parent_children.items():
        item = tasks.get(parent)
        if item is None:
            raise AssertionError(f"missing parent task: {parent}")
        nested = {" ".join(own_label(li).split()): li for li in descendants(item, "li")}
        for label, expected_checked in children.items():
            if label not in nested:
                raise AssertionError(f"{label!r} is not nested under {parent!r}")
            checkboxes = own_checkboxes(nested[label])
            if len(checkboxes) != 1 or ("checked" in checkboxes[0].attrs) != expected_checked:
                raise AssertionError(f"{label!r} has wrong checkbox state")

    strict = Tree()
    strict.feed(render(text, relaxed=False))
    if any(node.attrs.get("type") == "checkbox" for node in descendants(strict.root, "input")):
        raise AssertionError("strict mode unexpectedly produced task checkboxes")
    print("async@0.22.2 README: SHA-256 verified; 26 boxes (23 checked),")
    print("  all six reported children nested under their parents; strict mode 0 boxes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="use a previously downloaded README")
    args = parser.parse_args()
    if args.source:
        readme = args.source.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=20) as response:
            readme = response.read()
    check(readme)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"async README check failed: {error}", file=sys.stderr)
        sys.exit(1)
