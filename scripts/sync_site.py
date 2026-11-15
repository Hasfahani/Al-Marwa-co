"""Build new content and synchronize navigation, discovery files and quote context."""
from pathlib import Path
from html import escape
import json
import re
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode=True
from business_content import BUSINESS_PAGES, INDUSTRIES
from build_freight_pages import main as build_pages
from site_navigation import header_markup
from routes_ar import ROUTES_AR

ROOT=Path(__file__).resolve().parents[1]
BASE='https://al-marwaco.com/'
LASTMOD='2026-11-16'


def update(path, fn):
    source=path.read_text(encoding='utf-8')
    revised=fn(source)
    if revised!=source:path.write_text(revised,encoding='utf-8')


def audience_cards():
    labels=['Importers & Wholesalers','Manufacturers & Industry','Project & Construction Teams']
    return '<div class="business-audience-grid">'+''.join(
        f'<a class="business-audience-card" href="{spec["slug"]}"><h3>{escape(label)} <span aria-hidden="true">↗</span></h3><p>{escape(spec["summary"])}</p></a>' for spec,label in zip(INDUSTRIES,labels)
    )+'</div>'


def shared(source,path):
    language=re.search(r'<html lang="([^"]+)"',source)[1]
    navigation=header_markup(language,path.name)
    # Existing pages vary in whitespace and menu wording; replace only these IDs.
    source=re.sub(r'^[ \t]*<header id="header"[^>]*>.*?</header>(?:\s*<nav id="menu"[^>]*>.*?</nav>)?',lambda m:navigation,source,count=1,flags=re.S|re.M)
    if language=='en':
        services=[('sea-freight-lebanon.html','FCL Worldwide'),('full-truckload-lebanon.html','Full Truckloads'),('heavy-equipment-shipping-lebanon.html','Machinery & Large Cargo'),('lcl-shipping-lebanon.html','Selected-Origin LCL'),('export-shipping-lebanon.html','FCL Exports from Lebanon')]
        markup='<nav class="footer-col" aria-label="Services links"><h3>Business Freight</h3><ul>'+''.join(f'<li><a href="{p}">{escape(label)}</a></li>' for p,label in services)+'</ul></nav>'
        source=re.sub(r'<nav class="footer-col" aria-label="Services links">.*?</nav>',lambda m:markup,source,flags=re.S)
        companies=[('index.html','Home'),('about.html','About Us'),('freight-forwarding-lebanon.html','For Businesses'),('shipping-routes-lebanon.html','Shipping Routes'),('freight-resources-lebanon.html','Planning Tools & Guides'),('contact.html','Contact')]
        markup='<nav class="footer-col" aria-label="Site links"><h3>Company & Resources</h3><ul>'+''.join(f'<li><a href="{p}">{escape(label)}</a></li>' for p,label in companies)+'</ul></nav>'
        source=re.sub(r'<nav class="footer-col" aria-label="Site links">.*?</nav>',lambda m:markup,source,flags=re.S)
    return source


CUSTOMER_FIT='''<section class="home-section" id="customer-fit"><div class="inner"><header class="section-heading"><p class="section-eyebrow">Who we work with</p><h2>Built for Businesses Moving Big Loads</h2><p class="section-lead">We do our best work for companies shipping full containers, full trucks and large equipment.</p></header><div class="business-audience-grid customer-fit-grid"><div class="business-audience-card"><h3>Our best fit</h3><ul><li>Importers and wholesalers bringing in full containers or full trucks</li><li>Manufacturers moving machinery, tanks, production lines and raw materials</li><li>Exporters shipping full containers from Lebanon to any country</li><li>Project and construction teams with heavy or oversized equipment</li></ul></div><div class="business-audience-card"><h3>Also handled</h3><ul><li>LCL into Lebanon from Ukraine, Jordan, Iraq, the UAE, Turkey, the UK and China</li><li>Air cargo for urgent commercial shipments</li><li>Customs documentation support for business cargo</li><li>Recurring shipments and supplier consolidation</li></ul></div><div class="business-audience-card"><h3>Not our service</h3><ul><li>Parcels, courier and single-box shipments</li><li>Household moves and personal effects</li><li>LCL from countries outside our seven origins. A single large item from anywhere can still ship as FCL</li></ul></div></div><p class="section-actions"><a href="contact.html" class="button primary">Get a B2B freight quote</a><a href="freight-planner-lebanon.html" class="button">Check which service fits</a></p></div></section>'''


def homepage(source):
    source=re.sub(r'<section class="home-section [^"]+" hidden>.*?</section>','',source,flags=re.S)
    source=re.sub(r'<section class="home-section" id="customer-fit">.*?</section>\s*','',source,flags=re.S)
    source=source.replace('<section class="home-section" id="business-customer-groups">',CUSTOMER_FIT+'\n            <section class="home-section" id="business-customer-groups">',1)
    source=source.replace('Freight desk available','Business freight desk')
    if 'id="business-customer-groups"' not in source:
        section='<section class="home-section" id="business-customer-groups"><div class="inner"><header class="section-heading"><p class="section-eyebrow">Built around your business</p><h2>Freight for the Teams Moving Substantial Loads</h2><p class="section-lead">Choose a planning brief for your commercial stock, production inputs, or equipment project.</p></header>'+audience_cards()+'</div></section>'
        source=source.replace('<section class="home-section home-proof">',section+'\n            <section class="home-section home-proof">')
    if 'id="business-planning-tools"' not in source:
        section='''<section class="home-section" id="business-planning-tools"><div class="inner"><header class="section-heading"><p class="section-eyebrow">Prepare a useful freight inquiry</p><h2>Plan the Service. Measure the Load. Define the Scope.</h2><p class="section-lead">Practical tools for your team before requesting a commercial freight quote.</p></header><div class="business-audience-grid"><a href="freight-planner-lebanon.html" class="business-audience-card"><h3>Freight service planner ↗</h3><p>Check which published service should be reviewed for your route and shipment size.</p></a><a href="cargo-volume-calculator.html" class="business-audience-card"><h3>Cargo volume calculator ↗</h3><p>Calculate packed CBM, package count and supplied gross weights, then prepare a quote brief.</p></a><a href="container-shipping-costs-lebanon.html" class="business-audience-card"><h3>Container quote cost guide ↗</h3><p>Compare pickup, handling, main freight and final delivery on the same basis.</p></a></div><p class="section-actions"><a href="freight-resources-lebanon.html" class="button">All tools &amp; guides</a><a href="fcl-shipping-lebanon-ar.html" class="button" lang="ar" dir="rtl" hreflang="ar-LB">شحن الحاويات للشركات بالعربية</a></p></div></section>'''
        source=source.replace('<section class="home-section home-faq"',section+'\n            <section class="home-section home-faq"')
    match=re.search(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)
    graph=json.loads(match[1]);org=next(n for n in graph['@graph'] if n['@type']=='LocalBusiness')
    catalog=org['hasOfferCatalog']['itemListElement'];existing={n['itemOffered'].get('@id') for n in catalog}
    for spec in INDUSTRIES:
        entity_id=BASE+spec['slug']+'#service'
        if entity_id not in existing:catalog.append({'@type':'Offer','itemOffered':{'@type':'Service','@id':entity_id,'name':spec['heading'],'url':BASE+spec['slug']}})
    return source[:match.start(1)]+'\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n    '+source[match.end(1):]


def business_hub(source):
    if 'id="customer-planning-paths"' not in source:
        section='<section class="inner business-hub-panel" id="customer-planning-paths"><h2>Choose the Brief for Your Business</h2><p>Freight planning differs for stock replenishment, production inputs and project-site equipment. Start with your operating requirement.</p>'+audience_cards()+'<p><a href="freight-resources-lebanon.html">Planning tools, cost guidance and the downloadable quote checklist</a></p></section>'
        source=source.replace('</main>',section+'\n</main>',1)
    return source


def services(source):
    for label in ['Popular logistics pages','Additional logistics pages']:
        source=re.sub(r'<div class="intro-panel" aria-label="'+label+r'">.*?</div>','',source,flags=re.S)
    if 'id="service-business-audiences"' not in source:
        section='<div class="intro-panel" id="service-business-audiences"><h2>Services Around Your Business Load</h2>'+audience_cards()+'<p><a href="freight-resources-lebanon.html">Explore the freight planner, cargo volume calculator and B2B quote checklist</a></p></div>'
        source=source.replace('<div class="service-stack">',section+'\n            <div class="service-stack">',1)
    return source


def sea_freight(source):
    if 'id="fcl-quote-scope"' not in source:
        section='''<section class="topic-panel" id="fcl-quote-scope"><h2>FCL, LCL or a Truckload: Start With the Business Load</h2><p>Full Container Load means dedicated container use. A shipment does not have to occupy every cubic metre to be reviewed as FCL. For machinery, large items and recurring commercial orders, container fit, loading access and the complete service scope matter as much as volume.</p><ul class="planning-list"><li><strong>FCL worldwide:</strong> our main specialty for substantial business imports to Lebanon and exports from Lebanon.</li><li><strong>Selected-origin LCL:</strong> smaller commercial imports only from Ukraine, Jordan, Iraq, UAE, Turkey, the United Kingdom and China into Lebanon.</li><li><strong>Full truckloads:</strong> by road from Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China into Lebanon.</li></ul><p>Compare the same pickup and delivery points and identify the handling tasks included. A volume total or one freight-rate line does not establish the complete loading plan or shipment cost.</p><div class="quick-links"><a class="button" href="freight-planner-lebanon.html">Find the service to review</a><a class="button" href="cargo-volume-calculator.html">Calculate packed volume</a><a class="button" href="container-shipping-costs-lebanon.html">Understand quote scope</a><a class="button" href="fcl-shipping-lebanon-ar.html" lang="ar" dir="rtl" hreflang="ar-LB">معلومات الشحن بالعربية</a></div></section>'''
        source=source.replace('<h2>Frequently Asked Questions</h2>', '<h2>Frequently Asked Questions</h2>',1)
        marker='<section class="topic-panel">\n                        <h2>Frequently Asked Questions</h2>'
        assert marker in source
        source=source.replace(marker,section+'\n                    '+marker,1)
    return source


def contact(source):
    if 'id="cargo-category"' not in source:
        fields='''<div class="field"><label for="cargo-category">Business Cargo Category (Optional)</label><select id="cargo-category" name="cargo_category"><option value="">Choose category</option><option>Commercial Stock</option><option>Manufacturing Inputs</option><option>Machinery / Equipment</option><option>Project Cargo</option><option>Other Business Cargo</option></select></div><div class="field"><label for="container-requirement">If FCL: Container Requirement (Optional)</label><input id="container-requirement" name="container_requirement" type="text" maxlength="150" placeholder="e.g., 2 x 40 ft; or need advice"></div>'''
        marker='<div class="field">\n                                    <label for="shipment-frequency">'
        assert marker in source
        source=source.replace(marker,fields+'\n                                '+marker,1)
        source=source.replace('id="load-details" name="load_details" required','id="load-details" name="load_details" required maxlength="2000"')
        source=source.replace('<p class="field-hint" id="shipment-scope-note">','<p class="field-hint"><a href="cargo-volume-calculator.html">Calculate packed cargo volume</a> or <a href="downloads/b2b-freight-quote-checklist.txt" download>download the quote checklist</a> before completing your brief.</p><p class="field-hint" id="shipment-scope-note">',1)
    return source


def main():
    # Update the shared source before rendering dependent pages.
    update(ROOT/'index.html',homepage)
    update(ROOT/'services.html',services)
    update(ROOT/'freight-forwarding-lebanon.html',business_hub)
    update(ROOT/'sea-freight-lebanon.html',sea_freight)
    update(ROOT/'contact.html',contact)
    for path in ROOT.glob('*.html'):update(path,lambda source,p=path:shared(source,p))
    build_pages()

    alternates={'en-LB':BASE+'sea-freight-lebanon.html','de-DE':BASE+'seefracht-deutschland-libanon.html','ar-LB':BASE+'fcl-shipping-lebanon-ar.html','x-default':BASE+'sea-freight-lebanon.html'}
    for name in ['sea-freight-lebanon.html','seefracht-deutschland-libanon.html','fcl-shipping-lebanon-ar.html']:
        def add_alternates(source):
            source=re.sub(r'\s*<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*/?>','',source)
            markup='\n'+''.join(f'    <link rel="alternate" hreflang="{locale}" href="{url}" />\n' for locale,url in alternates.items())
            return source.replace('</head>',markup+'</head>',1)
        update(ROOT/name,add_alternates)

    sitemap_namespace='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'; images='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('',sitemap_namespace);ET.register_namespace('xhtml',xhtml);ET.register_namespace('image',images)
    path=ROOT/'sitemap.xml';tree=ET.parse(path);root=tree.getroot()
    existing={n.findtext('{'+sitemap_namespace+'}loc'):n for n in root}
    for page in sorted(ROOT.glob('*.html')):
        if page.name=='404.html':continue
        url=BASE+('' if page.name=='index.html' else page.name)
        if url not in existing:
            entry=ET.SubElement(root,'{'+sitemap_namespace+'}url')
            ET.SubElement(entry,'{'+sitemap_namespace+'}loc').text=url
            ET.SubElement(entry,'{'+sitemap_namespace+'}lastmod').text=LASTMOD
            existing[url]=entry
    for name in ['sea-freight-lebanon.html','seefracht-deutschland-libanon.html','fcl-shipping-lebanon-ar.html']:
        entry=existing[BASE+name]
        for old in list(entry.findall('{'+xhtml+'}link')):entry.remove(old)
        for locale,url in alternates.items():ET.SubElement(entry,'{'+xhtml+'}link',{'rel':'alternate','hreflang':locale,'href':url})
    for ar in ROUTES_AR:
        pair={'en-LB':BASE+ar['en_slug'],'ar-LB':BASE+ar['slug'],'x-default':BASE+ar['en_slug']}
        for name in (ar['en_slug'],ar['slug']):
            entry=existing[BASE+name]
            for old in list(entry.findall('{'+xhtml+'}link')):entry.remove(old)
            for locale,url in pair.items():ET.SubElement(entry,'{'+xhtml+'}link',{'rel':'alternate','hreflang':locale,'href':url})
    for entry in root:
        lastmod=entry.find('{'+sitemap_namespace+'}lastmod')
        if lastmod is not None:lastmod.text=LASTMOD
    ET.indent(tree,space='  ');tree.write(path,encoding='utf-8',xml_declaration=True)

    def ai_summary(source):
        source=re.sub(r'\n## Business customers and planning resources\n.*?(?=\n## |\Z)','',source,flags=re.S)
        block='\n## Business customers and planning resources\n\n'+''.join(f'- [{s["heading"]}]({BASE+s["slug"]}): {s["summary"]}\n' for s in BUSINESS_PAGES)
        block+='\n## Arabic route pages\n\n'+''.join(f'- [{s["heading"]}]({BASE+s["slug"]})\n' for s in ROUTES_AR)
        block+='\n## Best fit and not a fit\n\nBest fit: importers, wholesalers, manufacturers, exporters and project teams shipping full containers (FCL), full truckloads (FTL) or large equipment such as machinery and tanks. Not offered: parcels, courier, single-box shipments, household moves or personal effects, and LCL from origins outside the seven listed countries. A single large item from any country can still be shipped as FCL.\n'
        block+='\nPlanning tools run in the browser and do not quote prices, confirm container fit, approve cargo or establish live routes. Commercial stock, manufacturing inputs and project equipment have distinct planning guides. The native Arabic FCL page provides the same core business scope.\n'
        return re.sub(r'\n{3,}','\n\n',source.replace('## Quote information',block+'\n## Quote information'))
    update(ROOT/'llms.txt',ai_summary)
    for path in ROOT.glob('*.html'):
        update(path,lambda source:re.sub(r'(?m)[ \t]+$','',source))
    print('Synchronized navigation, customer paths, quote fields, Arabic FCL alternates and discovery files.')


if __name__=='__main__':main()
