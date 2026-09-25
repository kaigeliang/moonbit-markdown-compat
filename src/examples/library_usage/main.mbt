///|
fn main raise {
  let source = "- [x] parent\n  - [ ] child\n"
  let doc = @cmark.Doc::from_string(source, strict=false)
  let html = @cmark_html.xhtml_renderer(safe=false).doc_to_string(doc)
  println(html)
}
