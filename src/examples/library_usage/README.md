# Library API example

Run from the repository root:

```sh
moon run --target native src/examples/library_usage
moon run --target js src/examples/library_usage
moon run --target wasm src/examples/library_usage
```

The example parses a two-space nested task list with
`Doc::from_string(..., strict=false)` and renders it through the XHTML
renderer. The relaxed setting enables task-list syntax. With `strict=true`,
the same markers remain ordinary list text.
