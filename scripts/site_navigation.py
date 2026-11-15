"""Shared navigation for the static website, including native language links."""
from html import escape


def header_markup(language='en', current=''):
    labels = {
        'en': ['Services', 'Routes', 'For Businesses', 'Planning Tools', 'About', 'Get B2B Quote', 'Menu', 'Home', 'Contact'],
        'de': ['Leistungen', 'Routen', 'Für Unternehmen', 'Planung', 'Über uns', 'B2B-Angebot', 'Menü', 'Startseite', 'Kontakt'],
        'ar': ['الخدمات', 'المسارات', 'للشركات', 'أدوات التخطيط', 'من نحن', 'طلب عرض للشركات', 'القائمة', 'الرئيسية', 'تواصل معنا'],
    }[language]
    paths = ['services.html', 'shipping-routes-lebanon.html', 'freight-forwarding-lebanon.html', 'freight-resources-lebanon.html', 'about.html']

    def item(path, label):
        active=' aria-current="page"' if path==current else ''
        return f'<li><a href="{path}"{active}>{escape(label)}</a></li>'

    primary='\n'.join(item(path,label) for path,label in zip(paths,labels[:5]))
    mobile=item('index.html',labels[7])+primary+item('contact.html',labels[8])
    mobile+='''<li><a href="sea-freight-lebanon.html" lang="en" hreflang="en-LB">English · FCL</a></li>
<li><a href="fcl-shipping-lebanon-ar.html" lang="ar" dir="rtl" hreflang="ar-LB">العربية · شحن الحاويات</a></li>
<li><a href="spedition-libanon-deutschland.html" lang="de" hreflang="de-DE">Deutsch · B2B</a></li>'''
    return f'''        <header id="header" class="alt">
            <a href="index.html" class="logo" aria-label="AL MARWA CO home"><span class="brand-symbol" aria-hidden="true">AM</span><span class="brand-wordmark" aria-hidden="true"><strong>AL MARWA</strong><small>Freight Forwarding</small></span></a>
            <nav aria-label="{'التنقل الرئيسي' if language=='ar' else 'Main navigation'}">
                <ul class="desktop-nav">{primary}</ul>
                <a href="contact.html" class="nav-quote-btn">{labels[5]}</a>
                <a href="#menu">{labels[6]}</a>
            </nav>
        </header>
        <nav id="menu" aria-label="{'القائمة' if language=='ar' else 'Mobile navigation'}"><ul class="links">{mobile}</ul></nav>'''
