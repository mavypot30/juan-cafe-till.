#!/usr/bin/env python3
"""Copy the POS page into the app's assets.

The till is one HTML file that runs both as a web page and inside this app.
Point this at the page and it wraps it in a full HTML document and drops the
web-font request, which would otherwise stall the first paint when the tablet
is offline.

    python3 sync-assets.py path/to/index.html
"""
import re, sys, pathlib

src_path = sys.argv[1] if len(sys.argv) > 1 else 'pos-page/index.html'
src = pathlib.Path(src_path).read_text()

body, n = re.subn(
    r'<link rel="preconnect"[^>]*>\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">\s*',
    '', src, count=1)
if n == 0:
    print('note: no web-font link found (already stripped?)')

doc = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<style>
  html, body { height: 100%; }
  body { margin: 0; font: 14px system-ui, -apple-system, "Roboto", sans-serif; background: #EDEFEC; }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
  * { -webkit-tap-highlight-color: transparent; }
  input, select, textarea, button { font-family: inherit; }
</style>
</head>
<body>
''' + body + '''
</body>
</html>
'''
out = pathlib.Path(__file__).parent / 'app/src/main/assets/index.html'
out.write_text(doc)
print(f'wrote {out} ({len(doc):,} bytes)')
