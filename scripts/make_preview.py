"""Create preview.html from draft.md for pasting into Medium and Substack.

Usage: python scripts/make_preview.py output/<slug>
"""
import html
import sys
from pathlib import Path

import markdown

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ max-width: 720px; margin: 40px auto; padding: 0 20px;
         font-family: Georgia, serif; font-size: 19px; line-height: 1.6; color: #222; }}
  pre {{ background: #f5f5f5; padding: 16px; overflow-x: auto; font-size: 15px; }}
  code {{ font-family: Menlo, monospace; }}
</style>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/make_preview.py output/<slug>")
        sys.exit(2)
    folder = Path(sys.argv[1])
    lines = (folder / "draft.md").read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        print("draft.md must start with the title as '# Title'")
        sys.exit(1)
    title = lines[0][2:].strip()
    body = markdown.markdown("\n".join(lines[1:]), extensions=["fenced_code"])
    output = folder / "preview.html"
    output.write_text(TEMPLATE.format(title=html.escape(title), body=body), encoding="utf-8")
    print(f"Created {output}")


if __name__ == "__main__":
    main()