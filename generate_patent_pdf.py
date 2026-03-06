#!/usr/bin/env python3
import base64
import os
import re
import markdown
from weasyprint import HTML

# Generate figures first
import generate_figures
generate_figures.fig1()
generate_figures.fig2()
generate_figures.fig3()
generate_figures.fig4()


def img_tag(path):
    """Return an <img> tag with the image base64-encoded inline."""
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{data}" style="max-width:100%;margin:1em auto;display:block;" alt="{os.path.basename(path)}">'


FIGURE_IMAGES = {
    'FIG. 1': img_tag('docs/patent/figures/fig1.png'),
    'FIG. 2': img_tag('docs/patent/figures/fig2.png'),
    'FIG. 3': img_tag('docs/patent/figures/fig3.png'),
    'FIG. 4': img_tag('docs/patent/figures/fig4.png'),
}

with open('patent/application.md', 'r') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

# Inject figure images after each "FIG. N" heading inside the drawings section
for fig_id, img_html in FIGURE_IMAGES.items():
    # Match the <h3> tag that contains the figure label (e.g. "FIG. 1 — ...")
    pattern = re.escape(fig_id).replace(r'\.', r'\.')
    html_body = re.sub(
        rf'(<h3>[^<]*{re.escape(fig_id)}[^<]*</h3>)',
        rf'\1\n{img_html}',
        html_body
    )

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    margin: 1in;
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
  img {{ page-break-inside: avoid; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html, base_url='.').write_pdf('docs/patent/application.pdf')
print("PDF generated: docs/patent/application.pdf")
