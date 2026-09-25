# MoonBit Markdown Compat

MoonBit Markdown 兼容性与可靠性增强：基于社区 `cmark.mbt` 的贡献型项目。

这是 [moonbit-community/cmark.mbt](https://github.com/moonbit-community/cmark.mbt) 的开发 fork，保留上游提交历史和许可证。原有解析器、渲染器及测试属于上游成果。本项目的新增贡献从基线 `452c95f8369357785c5b78b03f4d990200e9ac3c` 之后计算。

首个目标是复现并修复 [嵌套任务列表缩进问题 #149](https://github.com/moonbit-community/cmark.mbt/issues/149)，随后增加针对真实 README 的回归用例和跨后端验证。当前仅完成仓库初始化，修复及验证尚未完成。

下方保留原项目说明。

---

# cmark

Cmark is a [CommonMark][CommonMark specification] toolkit for the MoonBit programming language,
started as a MoonBit rewrite of the [`cmarkit`] library from the OCaml ecosystem.

So far, it supports the following use cases:

- Parsing CommonMark documents with best-effort source-aware layout preservation:
- Rendering CommonMark documents via the `Renderer` API, along with a ready-to-use HTML renderer.

Supported CommonMark features include:

- Vanilla CommonMark syntax;
- Common syntax extensions, including:
  - Strikethroughs
  - Task lists
  - Footnotes
  - Tables
  - Inline math
  - Math blocks

## Building

To begin, you will need to install a recent MoonBit toolchain.
To do so, please refer to instructions at MoonBit's [official website](https://www.moonbitlang.com/download).

Also, a Python installation is required to run the pre-build scripts.
You can find relevant instructions from Python's [official website](https://www.python.org/downloads/).

Once you have the toolchain installed, you can build this project by running the following command:

```sh
moon build
```

## CLI

The repository includes a native command-line renderer that follows the basic
`cmark` input model: read Markdown from stdin, `-`, or one or more file paths and
write rendered HTML to stdout.

```sh
printf '# Hello\n' | moon run src/cmark_cli -- -
moon run src/cmark_cli -- README.md
moon run src/cmark_cli -- --safe --to xhtml README.md
```

For reference comparisons, install the upstream CommonMark CLI and compare
against the MoonBit executable:

```sh
brew install cmark
printf '# Hello\n' | cmark --unsafe
printf '# Hello\n' | moon run src/cmark_cli -- -
```

## Testing

With the MoonBit toolchain installed, you can run the tests by executing the following command:

```sh
moon test
```

## Acknowledgements

`cmark` is built on top several pre-existing projects. Thanks go to:

- Daniel Bünzli for the [`cmarkit`] project;
- John MacFarlane for the [CommonMark specification] and the [`cmark`] project;
- Martin Mitáš for the [`md4c`] project.

[CommonMark specification]: https://spec.commonmark.org/
[`cmark`]: https://github.com/commonmark/cmark
[`cmarkit`]: https://github.com/dbuenzli/cmarkit
[`md4c`]: https://github.com/mity/md4c
