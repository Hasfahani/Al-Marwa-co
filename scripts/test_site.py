"""Fast, dependency-free checks for the static production website."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = sorted(path for path in ROOT.glob("*.html") if path.name != "404.html")
errors: list[str] = []
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
NOSCRIPT_CSS = (ROOT / "assets" / "css" / "noscript.css").read_text(encoding="utf-8")
MAIN_CSS = (ROOT / "assets" / "css" / "main.css").read_text(encoding="utf-8")
CSS_FILES = [
    ROOT / "assets" / "css" / "main.css",
    ROOT / "assets" / "css" / "fonts.css",
    ROOT / "assets" / "css" / "fontawesome-all.min.css",
]
seen_titles: dict[str, str] = {}
seen_descriptions: dict[str, str] = {}

try:
    sitemap_root = ET.fromstring(SITEMAP)
except ET.ParseError as exc:
    errors.append(f"sitemap.xml: invalid XML ({exc})")
    sitemap_root = None

if sitemap_root is not None:
    sitemap_namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_locations = [
        element.text
        for element in sitemap_root.findall("s:url/s:loc", sitemap_namespace)
        if element.text
    ]
    if len(sitemap_locations) != len(set(sitemap_locations)):
        errors.append("sitemap.xml: contains duplicate URLs")


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
    if "fonts.googleapis.com" in source or "fonts.gstatic.com" in source:
        fail(page, "must use the self-hosted font files")
    if "\ufffd" in source:
        fail(page, "contains an invalid Unicode replacement character")
    title = re.search(r"<title>(.*?)</title>", source, re.I | re.S)
    if not title:
        fail(page, "missing title")
    else:
        normalized_title = " ".join(title.group(1).split()).lower()
        if normalized_title in seen_titles:
            fail(page, f"duplicate title also used by {seen_titles[normalized_title]}")
        seen_titles[normalized_title] = page.name
    language = re.search(r'<html\s+lang="([a-z-]+)"', source, re.I)
    if not language:
        fail(page, "missing document language declaration")
    elif language.group(1).lower().startswith("ar") and not re.search(r'<html[^>]+dir="rtl"', source, re.I):
        fail(page, "Arabic pages must declare right-to-left direction")
    description = re.search(r'<meta\s+name="description"\s+content="(.{70,170})"', source, re.I)
    if not description:
        fail(page, "description should be 70-170 characters")
    else:
        normalized_description = " ".join(description.group(1).split()).lower()
        if normalized_description in seen_descriptions:
            fail(page, f"duplicate description also used by {seen_descriptions[normalized_description]}")
        seen_descriptions[normalized_description] = page.name
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
        if tag == "img" and ("width" not in attrs or "height" not in attrs):
            fail(page, f"image missing width or height: {attrs.get('src', 'unknown')}")
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
if re.search(r"^\s*@import", MAIN_CSS, re.M):
    errors.append("main.css: avoid render-blocking nested stylesheet imports")

for css_file in CSS_FILES:
    css_source = css_file.read_text(encoding="utf-8")
    for target in re.findall(r"url\([\"']?([^\"')]+)", css_source):
        if target.startswith(("data:", "http:", "https:")):
            continue
        resolved_target = (css_file.parent / urlsplit(target).path).resolve()
        if not resolved_target.exists():
            errors.append(f"{css_file.name}: broken local reference: {target}")

if errors:
    print("SITE CHECK FAILED")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"SITE CHECK PASSED: {len(PUBLIC_PAGES)} public pages validated")
