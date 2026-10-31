"""Build the website from game.html.

game.html is the game as published on Claude (no <head>). This wraps it into a full
index.html for GitHub Pages, and optionally zips that for itch.io:

    python3 build.py                       # writes index.html and preview/index.html
    python3 build.py ~/Desktop/crossover-itch.zip   # also writes the zip

preview/ is the game played with the finished printed cards (preview/game.html plus the card
images in preview/cards/). It is built next to the live game but never goes into the itch zip.
"""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESC = "A quick family basketball card game. Play a shot, the defense answers it or it scores, first to 21 wins."
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='9' fill='%230d1220'/%3E"
        "%3Ccircle cx='20' cy='20' r='13' fill='%23e0702a'/%3E%3Cpath d='M7 20h26M20 7v26M11 11c4.5 4.3 4.5 13.7 0 18M29 11c-4.5 4.3-4.5 13.7 0 18' "
        "stroke='%232a1405' stroke-width='1.6' fill='none'/%3E%3C/svg%3E")


def build(folder, title):
    src = (folder / "game.html").read_text(encoding="utf-8")
    start = src.index('<link rel="preconnect"')
    split = src.index('<svg width="0"')
    head_assets, body = src[start:split].rstrip(), src[split:].rstrip()

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0d1220">
<link rel="icon" href="{ICON}">
{head_assets}
</head>
<body>
{body}
</body>
</html>
"""
    (folder / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {(folder / 'index.html').relative_to(HERE)}")


build(HERE, "Crossover")
build(HERE / "preview", "Crossover")

if len(sys.argv) > 1:
    out = Path(sys.argv[1]).expanduser()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(HERE / "index.html", "index.html")
    print(f"wrote {out}")
