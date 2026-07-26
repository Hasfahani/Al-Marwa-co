"""Fast, dependency-free checks for the static production website."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = sorted(path for path in ROOT.glob("*.html") if path.name != "404.html")
errors: list[str] = []
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
NOSCRIPT_CSS = (ROOT / "assets" / "css" / "noscript.css").read_text(encoding="utf-8")


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))


def fail(page: Path, message: str) -> None:
    errors.append(f"{page.name}: {message}")


for page in PUBLIC_PAGES:
    source = page.read_text(encoding="utf-8")
    document = Document()
    document.feed(source)

    if len(re.findall(r"<h1\b", source, re.I)) != 1:
        fail(page, "must contain exactly one h1")
    language = re.search(r'<html\s+lang="([a-z-]+)"', source, re.I)
    if not language:
        fail(page, "missing document language declaration")
    elif language.group(1).lower().startswith("ar") and not re.search(r'<html[^>]+dir="rtl"', source, re.I):
        fail(page, "Arabic pages must declare right-to-left direction")
    if not re.search(r'<meta\s+name="description"\s+content=".{70,170}"', source, re.I):
        fail(page, "description should be 70-170 characters")
    if len(re.findall(r'<link\s+rel="canonical"', source, re.I)) != 1:
        fail(page, "must contain exactly one canonical URL")
    canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', source, re.I)
    if canonical and canonical.group(1) not in SITEMAP:
        fail(page, "canonical URL is missing from sitemap.xml")

    for match in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S):
        try:
            json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            fail(page, f"invalid JSON-LD ({exc.msg})")

    for tag, attrs in document.tags:
        if tag == "img" and "alt" not in attrs:
            fail(page, f"image missing alt text: {attrs.get('src', 'unknown')}")
        if tag not in {"a", "link", "script", "img"}:
            continue
        attribute = "href" if tag in {"a", "link"} else "src"
        target = attrs.get(attribute)
        if not target or target.startswith(("http:", "https:", "mailto:", "tel:", "#", "data:")):
            continue
        local_path = urlsplit(target).path
        if local_path and not (ROOT / local_path).exists():
            fail(page, f"broken local reference: {target}")

if ".reveal" not in NOSCRIPT_CSS or "opacity: 1" not in NOSCRIPT_CSS:
    errors.append("noscript.css: reveal content must remain visible without JavaScript")

if errors:
    print("SITE CHECK FAILED")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"SITE CHECK PASSED: {len(PUBLIC_PAGES)} public pages validated")
