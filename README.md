# MoonBit Markdown Compat

[![Markdown compatibility](https://github.com/kaigeliang/moonbit-markdown-compat/actions/workflows/compat.yml/badge.svg)](https://github.com/kaigeliang/moonbit-markdown-compat/actions/workflows/compat.yml)

基于 [moonbit-community/cmark.mbt](https://github.com/moonbit-community/cmark.mbt) 的 MoonBit Markdown 工具包，提供 CommonMark 解析与 HTML 渲染，并修复嵌套任务列表的缩进解析问题。

适用于 README 渲染、文档预览及需要 Markdown 解析的 MoonBit 应用。支持原有的任务列表、表格、删除线、脚注和数学公式扩展。

## 安装与运行

需要 [MoonBit 工具链](https://www.moonbitlang.com/download)、Python 3，以及运行 JS 示例时所需的 Node.js。

```sh
git clone https://github.com/kaigeliang/moonbit-markdown-compat.git
cd moonbit-markdown-compat
moon update
moon build --target native

# 渲染包含任务列表的 Markdown 文件。
moon run --target native src/cmark_cli -- --relaxed examples/task-list.md

# 从标准输入读取 Markdown。
printf '# Hello\n' | moon run --target native src/cmark_cli -- -

# 安全渲染模式与 XHTML 输出。
moon run --target native src/cmark_cli -- --safe --to xhtml README.md
```

CLI 默认使用严格 CommonMark 模式；添加 `--relaxed` 开启任务列表等扩展。CLI 使用 native 后端，解析和渲染库支持 native、JS、Wasm 和 Wasm-GC。

**当前修复通过本仓库源码提供，尚未发布为 Mooncakes 新版本。** 安装已发布的 `moonbit-community/cmark@0.4.8` 不会包含此修复；本仓库保留上游模块名，便于审阅和集成补丁。

## MoonBit 库用法

使用 `@cmark.Doc::from_string(source, strict=false)` 解析扩展语法，再用 `@cmark_html.xhtml_renderer(safe=true).doc_to_string(doc)` 生成 HTML。完整的导入配置和可运行代码见 [库 API 示例](src/examples/library_usage)。

```sh
moon run --target native src/examples/library_usage
moon run --target js src/examples/library_usage
moon run --target wasm src/examples/library_usage
moon run --target wasm-gc src/examples/library_usage
```

## 嵌套任务列表修复

以下输入的子任务应属于 `parent`：

```markdown
- [x] parent
  - [ ] child
```

上游问题 [#149](https://github.com/moonbit-community/cmark.mbt/issues/149) 中，任务标记被额外计入续行缩进，导致两空格和四空格子任务无法正确嵌套。本仓库按列表标记计算续行缩进，并增加混合列表、续行段落、引用、代码块和严格模式回归测试。

在固定版本 [async@0.22.2 README](https://assets.mooncakes.io/assets/moonbitlang/async@0.22.2/README.md) 上，修复后渲染出 26 个复选框，其中 23 个已勾选；检查同时验证六个受影响子任务的层级和勾选状态。

查看示例原文及修复前后的 HTML 差异：

```sh
python3 scripts/demo_task_fix.py
```

基线输出来自上游提交 `452c95f8369357785c5b78b03f4d990200e9ac3c`。

## 测试

```sh
# 当前工具链默认后端的测试。
moon test

# 四后端测试与库示例输出一致性检查。
python3 scripts/verify_targets.py

# 加上真实 README 回归检查（下载固定版本并验证 SHA-256）。
python3 scripts/verify_targets.py --async-readme

# 已有 README 副本时，无需重新下载。
python3 scripts/verify_targets.py --source /path/to/README.md
```

这里的输出一致性检查针对随仓库提供的示例；回归测试覆盖明确列出的场景，不代表所有 Markdown 输入均已验证。

## 项目来源与许可证

本仓库是 `moonbit-community/cmark.mbt` 的 fork。原有解析器、渲染器、CLI、语法扩展和测试来自上游；新增内容包括任务列表缩进修复、相关回归用例、真实 README 验证和跨后端示例对比。上游修复已提交为 [PR #150](https://github.com/moonbit-community/cmark.mbt/pull/150)，等待审阅，尚未合并。

保留原有作者署名与 [LICENSE](LICENSE) 中的 Apache-2.0 及 cmarkit ISC 许可声明。cmark 最初是 OCaml `cmarkit` 库的 MoonBit 重写。

## Acknowledgements

`cmark` is built on top several pre-existing projects. Thanks go to:

- Daniel Bünzli for the [`cmarkit`] project;
- John MacFarlane for the [CommonMark specification] and the [`cmark`] project;
- Martin Mitáš for the [`md4c`] project.

[CommonMark specification]: https://spec.commonmark.org/
[`cmark`]: https://github.com/commonmark/cmark
[`cmarkit`]: https://github.com/dbuenzli/cmarkit
[`md4c`]: https://github.com/mity/md4c
