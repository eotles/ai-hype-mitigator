#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS

with open('patent/application.md', 'r') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    margin: 1in 1in 1in 1.5in;
    color: #000;
  }}
  h1 {{ font-size: 16pt; text-align: center; margin-bottom: 0.5em; }}
  h2 {{ font-size: 13pt; margin-top: 1.5em; }}
  h3 {{ font-size: 12pt; margin-top: 1em; }}
  pre {{
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background: #f5f5f5;
    padding: 0.5em;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  code {{
    font-family: 'Courier New', monospace;
    font-size: 10pt;
  }}
  p {{ margin: 0.5em 0; text-align: justify; }}
  ul, ol {{ margin: 0.5em 0; padding-left: 1.5em; }}
  li {{ margin: 0.25em 0; }}
  hr {{ border: none; border-top: 1px solid #000; margin: 1em 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html, base_url='.').write_pdf('docs/patent/application.pdf')
print("PDF generated: docs/patent/application.pdf")
