"""Fast, dependency-free checks for the static production website."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.robotparser import RobotFileParser
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
    ROOT / "assets" / "css" / "freight-pages.css",
]
seen_titles: dict[str, str] = {}
seen_descriptions: dict[str, str] = {}
MULTILINGUAL_ALTERNATES = {
    "freight-forwarding-lebanon.html": {
        "en-LB": "https://al-marwaco.com/freight-forwarding-lebanon.html",
        "de-DE": "https://al-marwaco.com/spedition-libanon-deutschland.html",
        "x-default": "https://al-marwaco.com/freight-forwarding-lebanon.html",
    },
    "spedition-libanon-deutschland.html": {
        "de-DE": "https://al-marwaco.com/spedition-libanon-deutschland.html",
        "en-LB": "https://al-marwaco.com/freight-forwarding-lebanon.html",
        "x-default": "https://al-marwaco.com/freight-forwarding-lebanon.html",
    },
    "sea-freight-lebanon.html": {
        "en-LB": "https://al-marwaco.com/sea-freight-lebanon.html",
        "de-DE": "https://al-marwaco.com/seefracht-deutschland-libanon.html",
        "ar-LB": "https://al-marwaco.com/fcl-shipping-lebanon-ar.html",
        "x-default": "https://al-marwaco.com/sea-freight-lebanon.html",
    },
    "seefracht-deutschland-libanon.html": {
        "de-DE": "https://al-marwaco.com/seefracht-deutschland-libanon.html",
        "en-LB": "https://al-marwaco.com/sea-freight-lebanon.html",
        "ar-LB": "https://al-marwaco.com/fcl-shipping-lebanon-ar.html",
        "x-default": "https://al-marwaco.com/sea-freight-lebanon.html",
    },
    "air-cargo-lebanon.html": {
        "en-LB": "https://al-marwaco.com/air-cargo-lebanon.html",
        "de-DE": "https://al-marwaco.com/luftfracht-deutschland-libanon.html",
        "x-default": "https://al-marwaco.com/air-cargo-lebanon.html",
    },
    "luftfracht-deutschland-libanon.html": {
        "de-DE": "https://al-marwaco.com/luftfracht-deutschland-libanon.html",
        "en-LB": "https://al-marwaco.com/air-cargo-lebanon.html",
        "x-default": "https://al-marwaco.com/air-cargo-lebanon.html",
    },
}
MULTILINGUAL_ALTERNATES["fcl-shipping-lebanon-ar.html"] = dict(MULTILINGUAL_ALTERNATES["sea-freight-lebanon.html"])
sys.path.insert(0, str(ROOT / "scripts"))
from routes_ar import ROUTES_AR
for _ar in ROUTES_AR:
    for _name in (_ar["en_slug"], _ar["slug"]):
        MULTILINGUAL_ALTERNATES[_name] = {
            "en-LB": "https://al-marwaco.com/" + _ar["en_slug"],
            "ar-LB": "https://al-marwaco.com/" + _ar["slug"],
            "x-default": "https://al-marwaco.com/" + _ar["en_slug"],
        }
for beirut_page in ("freight-forwarding-beirut.html", "freight-forwarding-beirut-ar.html"):
    MULTILINGUAL_ALTERNATES[beirut_page] = {
        "en-LB": "https://al-marwaco.com/freight-forwarding-beirut.html",
        "ar-LB": "https://al-marwaco.com/freight-forwarding-beirut-ar.html",
        "x-default": "https://al-marwaco.com/freight-forwarding-beirut.html",
    }
GERMAN_B2B_CLUSTER = {
    "spedition-libanon-deutschland.html": {
        "seefracht-deutschland-libanon.html",
        "luftfracht-deutschland-libanon.html",
    },
    "seefracht-deutschland-libanon.html": {
        "spedition-libanon-deutschland.html",
        "luftfracht-deutschland-libanon.html",
    },
    "luftfracht-deutschland-libanon.html": {
        "spedition-libanon-deutschland.html",
        "seefracht-deutschland-libanon.html",
    },
}

sitemap_locations: list[str] = []
try:
    sitemap_root = ET.fromstring(SITEMAP)
except ET.ParseError as exc:
    errors.append(f"sitemap.xml: invalid XML ({exc})")
    sitemap_root = None

if sitemap_root is not None:
    sitemap_namespace = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }
    sitemap_locations = [
        element.text
        for element in sitemap_root.findall("s:url/s:loc", sitemap_namespace)
        if element.text
    ]
    if len(sitemap_locations) != len(set(sitemap_locations)):
        errors.append("sitemap.xml: contains duplicate URLs")
    sitemap_urls = {
        url.findtext("s:loc", namespaces=sitemap_namespace): url
        for url in sitemap_root.findall("s:url", sitemap_namespace)
    }
    for page_name, alternates in MULTILINGUAL_ALTERNATES.items():
        page_url = f"https://al-marwaco.com/{page_name}"
        url_element = sitemap_urls.get(page_url)
        if url_element is None:
            continue
        sitemap_alternates = {
            link.get("hreflang"): link.get("href")
            for link in url_element.findall("xhtml:link", sitemap_namespace)
        }
        if sitemap_alternates != alternates:
            errors.append(f"sitemap.xml: incorrect hreflang cluster for {page_name}")


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.stack: list[tuple[str, bool]] = []
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        self.tags.append((tag, attributes))
        suppressed = (
            bool(self.stack and self.stack[-1][1])
            or tag in {"head", "script", "style", "template"}
            or "hidden" in attributes
            or bool(re.search(r"display\s*:\s*none", attributes.get("style") or "", re.I))
        )
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, suppressed))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.stack or not self.stack[-1][1]:
            self.visible_text.append(data)


def fail(page: Path, message: str) -> None:
    errors.append(f"{page.name}: {message}")


parsed_documents: dict[str, Document] = {}
for page in PUBLIC_PAGES:
    source = page.read_text(encoding="utf-8")
    document = Document()
    document.feed(source)
    parsed_documents[page.name] = document

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
    if canonical and canonical.group(1) not in sitemap_locations:
        fail(page, "canonical URL is missing from sitemap.xml")
    expected_url = "https://al-marwaco.com/" + ("" if page.name == "index.html" else page.name)
    if canonical and canonical.group(1) != expected_url:
        fail(page, "canonical must point to this page's production URL")

    # Every indexable page should produce a complete, intentional search/social
    # preview instead of relying on crawler-generated fallback text or images.
    required_preview_tags = {
        "Open Graph title": r'<meta\s+property="og:title"\s+content="[^"]+"',
        "Open Graph description": r'<meta\s+property="og:description"\s+content="[^"]+"',
        "Open Graph URL": r'<meta\s+property="og:url"\s+content="https://al-marwaco\.com/[^"]*"',
        "Open Graph image": r'<meta\s+property="og:image"\s+content="https://al-marwaco\.com/[^"]+"',
        "Twitter card": r'<meta\s+name="twitter:card"\s+content="summary_large_image"',
    }
    for label, pattern in required_preview_tags.items():
        if not re.search(pattern, source, re.I):
            fail(page, f"missing {label}")

    for locale, alternate_url in MULTILINGUAL_ALTERNATES.get(page.name, {}).items():
        expected = f'<link rel="alternate" hreflang="{locale}" href="{alternate_url}"'
        if expected not in source:
            fail(page, f"missing reciprocal {locale} hreflang URL")

    if page.name in GERMAN_B2B_CLUSTER:
        if not re.search(r'<html\s+lang="de"', source, re.I):
            fail(page, "German B2B cluster pages must declare German as the page language")
        if '"@type": "Service"' not in source:
            fail(page, "German B2B cluster pages must include Service structured data")
        for cluster_target in GERMAN_B2B_CLUSTER[page.name]:
            if f'href="{cluster_target}"' not in source:
                fail(page, f"missing German B2B cluster link: {cluster_target}")

    structured_nodes = []
    for match in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S):
        try:
            data = json.loads(match.group(1))
            structured_nodes.extend(data.get("@graph", [data]))
        except json.JSONDecodeError as exc:
            fail(page, f"invalid JSON-LD ({exc.msg})")

    # Business facts and service providers must identify the same real company.
    organization_id = "https://al-marwaco.com/#organization"
    nodes_by_id = {node.get("@id"): node for node in structured_nodes}
    ids = [node["@id"] for node in structured_nodes if "@id" in node]
    if len(ids) != len(set(ids)):
        fail(page, "structured data contains duplicate entity IDs")
    organization = nodes_by_id.get(organization_id, {})
    if (
        organization.get("@type") != "LocalBusiness"
        or organization.get("name") != "AL MARWA CO"
        or organization.get("telephone") != "+96170099978"
        or organization.get("email") != "info@al-marwaco.com"
        or organization.get("foundingDate") != "1997"
        or organization.get("address", {}).get("streetAddress") != "Khalde Highway"
        or organization.get("address", {}).get("addressLocality") != "Khalde"
        or organization.get("address", {}).get("addressCountry") != "LB"
    ):
        fail(page, "missing or inconsistent business identity and contact facts")
    webpage = nodes_by_id.get(expected_url + "#webpage", {})
    if (
        webpage.get("url") != expected_url
        or webpage.get("isPartOf", {}).get("@id") != "https://al-marwaco.com/#website"
        or webpage.get("about", {}).get("@id") != organization_id
    ):
        fail(page, "page structured data must connect its canonical, website, and business")
    visible_text = " ".join(" ".join(document.visible_text).split())
    for node in structured_nodes:
        if node.get("@type") == "Service" and node.get("provider", {}).get("@id") != organization_id:
            fail(page, "service provider must reference the shared business identity")
        if node.get("@type") == "FAQPage":
            for question in node.get("mainEntity", []):
                for text in (question.get("name", ""), question.get("acceptedAnswer", {}).get("text", "")):
                    if not text or " ".join(text.split()) not in visible_text:
                        fail(page, f"FAQ structured data does not match visible content: {question.get('name')}")

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

# A service/route page must be discoverable through actual website links, and
# links into planning sections must land on a real fragment rather than a 404.
page_links: dict[str, set[str]] = {name: set() for name in parsed_documents}
for name, document in parsed_documents.items():
    ids = [attrs["id"] for _, attrs in document.tags if attrs.get("id")]
    if len(ids) != len(set(ids)):
        fail(ROOT / name, "contains duplicate HTML IDs")
    for tag, attrs in document.tags:
        target = attrs.get("href")
        if tag != "a" or not target:
            continue
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            continue
        target_name = parts.path or name
        if target_name not in parsed_documents:
            continue
        page_links[name].add(target_name)
        if parts.fragment:
            target_ids = {a.get("id") for _, a in parsed_documents[target_name].tags}
            if parts.fragment not in target_ids:
                fail(ROOT / name, f"broken section link: {target}")

reachable, pending = set(), ["index.html"]
while pending:
    name = pending.pop()
    if name in reachable:
        continue
    reachable.add(name)
    pending.extend(page_links.get(name, set()) - reachable)
for name in sorted(set(parsed_documents) - reachable):
    fail(ROOT / name, "is not reachable through links from the homepage")

expected_sitemap_urls = {
    "https://al-marwaco.com/" + ("" if page.name == "index.html" else page.name)
    for page in PUBLIC_PAGES
}
if set(sitemap_locations) != expected_sitemap_urls:
    errors.append("sitemap.xml: must contain exactly the indexable website pages")

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

robots = RobotFileParser()
robots.parse((ROOT / "robots.txt").read_text(encoding="utf-8").splitlines())
for agent in ("Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot"):
    for public_path in ["", "llms.txt", "sitemap.xml"] + [p.name for p in PUBLIC_PAGES]:
        if not robots.can_fetch(agent, f"https://al-marwaco.com/{public_path}"):
            errors.append(f"robots.txt: blocks {agent} from /{public_path}")
if "https://al-marwaco.com/sitemap.xml" not in (robots.site_maps() or []):
    errors.append("robots.txt: missing production sitemap declaration")

llms_text = (ROOT / "llms.txt").read_text(encoding="utf-8")
for url in re.findall(r"\]\((https://al-marwaco\.com/[^)]+)\)", llms_text):
    if not (ROOT / urlsplit(url).path.lstrip("/")).is_file():
        errors.append(f"llms.txt: broken local page reference: {url}")

if errors:
    print("SITE CHECK FAILED")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"SITE CHECK PASSED: {len(PUBLIC_PAGES)} public pages validated")
