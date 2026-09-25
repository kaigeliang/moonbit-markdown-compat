# MoonBit Markdown Compat

MoonBit Markdown 兼容性与可靠性增强：基于社区 `cmark.mbt` 的贡献型项目。

这是 [moonbit-community/cmark.mbt](https://github.com/moonbit-community/cmark.mbt) 的开发 fork，保留上游提交历史和许可证。原有解析器、渲染器及测试属于上游成果。本项目的新增贡献从基线 `452c95f8369357785c5b78b03f4d990200e9ac3c` 之后计算。

首个目标 [嵌套任务列表缩进问题 #149](https://github.com/moonbit-community/cmark.mbt/issues/149) 已在固定基线上独立复现并修复。`- [x] parent` 下的两空格和四空格子任务现在都保持正确层级。原始报告中的 [async@0.22.2 README](https://assets.mooncakes.io/assets/moonbitlang/async@0.22.2/README.md) 已从 20 个 checkbox 恢复为 26 个。

## 直接运行

```sh
# CLI 默认 strict 模式；--relaxed 开启任务列表等扩展。
moon run --target native src/cmark_cli -- --relaxed examples/task-list.md

# 显示 Markdown 原文、基线 HTML 与当前 HTML 的实际差异。
python3 scripts/demo_task_fix.py

# 四后端测试、渲染输出对比和真实 README 验证。
python3 scripts/verify_targets.py --async-readme

# MoonBit 库 API 示例。
moon run --target native src/examples/library_usage
```

需要已安装的 [MoonBit 工具链](https://www.moonbitlang.com/download) 与 Python 3。`--async-readme` 会下载固定版本的公开 README 并核验 SHA-256；离线时可用 `--source /path/to/README.md`。不需要上传 JSON 或视频。

## 来源与新增贡献

| 能力 | 来源 | 当前状态 |
| --- | --- | --- |
| CommonMark 解析器、HTML 渲染器、CLI、原有测试 | 上游 `moonbit-community/cmark.mbt` | 保留历史、署名和 Apache-2.0 许可证 |
| Task list 语法支持 | 上游已有扩展 | `strict=false` 或 CLI `--relaxed` 启用 |
| 嵌套任务列表缩进修复 | 本 fork | 两/四空格子项保持嵌套；含最小失败回归 |
| 混排、续行、代码块、引用、strict 回归 | 本 fork | 精确 HTML 快照与测试 |
| async README 集成验证 | 本 fork | 校验源文件哈希、26/23 checkbox 数量及六个子项层级 |
| 跨后端与演示工具 | 本 fork | native、JS、Wasm、Wasm-GC 测试和输出对比 |

上游补丁尚未提交社区审阅。

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
