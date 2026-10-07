#!/usr/bin/env python3
"""Legally Clean pitch prototype generator.

Plain HTML from WordPress core block markup, laid out with Twenty Twenty-Four patterns
(banner-project-description, text-project-details, cta-services-image-left, testimonial-centered,
text-faq, text-centered-statement, footer). Run:  python3 tools/build_site.py <site-dir>
Every fact in the copy comes from the client's own channels; see facts.md.
"""
import hashlib, json, os, sys, time
from urllib.parse import quote_plus

# ---- CONFIG ----
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
BASE_URL = "https://legallyclean.whitephoenixconsulting.com/"
NAME = "Legally Clean"
PHONE = "(561) 467-4400"
TEL = "+15614674400"
EMAIL = "sherry@legallyclean.com"
FACEBOOK = "https://www.facebook.com/legallyclean"
INSTAGRAM = "https://www.instagram.com/legallyclean/"
LINKEDIN = "https://www.linkedin.com/company/legallyclean/"
YELP = "https://www.yelp.com/biz/legally-clean-lauderhill-2"
GOOGLE = "https://share.google/gWSEJBkBaSyi1Ntzq"
HOURS_TEXT = "Mon to Sat, 8am to 6pm"

OFFICES = [
    {"id": "broward", "county": "Broward County", "label": "Main office", "street": "1773 N State Rd 7, Ste 101 I", "city": "Lauderhill, FL 33313",
     "phone": "(561) 467-4400", "tel": "+15614674400",
     "cities": "Fort Lauderdale, Hollywood, Pembroke Pines, Coral Springs, Miramar, Pompano Beach, Davie, Plantation, Sunrise and Weston"},
    {"id": "miami-dade", "county": "Miami-Dade County", "label": "Office", "street": "7900 NW 27th Ave, #236", "city": "Miami, FL 33147",
     "phone": "(561) 513-8138", "tel": "+15615138138",
     "cities": "Miami, Miami Lakes, Hialeah, Doral, Kendall, Coral Gables, Miami Gardens and Homestead"},
    {"id": "palm-beach", "county": "Palm Beach County", "label": "Office", "street": "401 N Rosemary Ave", "city": "West Palm Beach, FL 33401",
     "phone": "(561) 934-2594", "tel": "+15619342594",
     "cities": "West Palm Beach, Boca Raton, Delray Beach, Boynton Beach, Lake Worth, Wellington, Palm Beach Gardens and Jupiter"},
]

BUILD = time.strftime("%Y%m%d%H%M%S")
# If a browser shows a cached page from an older build, it reloads once to get the current one.
SELF_HEAL = ('<script>(function(){if(!window.fetch)return;fetch("ROOTversion.json",{cache:"no-store"})'
             '.then(function(r){return r.json()}).then(function(v){if(v.build&&v.build!=="BUILD"){var k="reload-"+v.build;'
             'try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1")}catch(e){}location.reload()}}).catch(function(){})})();</script>')


PAGEREVEAL = r"""<script>document.documentElement.classList.add("js");
/* Element-to-page transition: the element clicked on the last page morphs into its match here. */
addEventListener("pagereveal",function(e){var k,t;try{k=JSON.parse(sessionStorage.getItem("vt")||"null");sessionStorage.removeItem("vt")}catch(x){}
if(!e.viewTransition||!k||Date.now()-k.t>6000)return;t=document.querySelector('[data-vt-key="'+k.key+'"]');if(!t)return;
t.style.viewTransitionName="expand";document.documentElement.classList.add("vt-arrive");var r=t.closest(".clip-reveal");if(r)r.classList.add("is-revealed");
e.viewTransition.finished.finally(function(){t.style.viewTransitionName="";document.documentElement.classList.remove("vt-arrive")})});</script>"""


def ver(rel):
    """Cache-busting version, like WordPress's ?ver= on enqueued assets."""
    with open(os.path.join(OUT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


IMGS = {
    "hero": ([800, 1280, 1920], 1920, 1280),
    "post-construction": ([640, 1000, 1179], 1179, 1329),
    "janitorial": ([640, 1000, 1400], 1400, 832),
    "deep-clean": ([640, 1000, 1400], 1400, 935),
    "floors-windows": ([520], 520, 629),
    "job-cabinets": ([640, 1000, 1179], 1179, 1332),
    "job-hallway": ([640, 1000, 1280], 1280, 1706),
    "job-atrium": ([450], 450, 600),
    "broward-health-er": ([640, 1000, 1472], 1472, 700),
    "sherry": ([525], 525, 768),
}

SVG = {
    "phone": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "arrow": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"/></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    # WordPress core navigation icons
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M5 5v1.5h14V5H5zm0 7.8h14v-1.5H5v1.5zM5 19h14v-1.5H5V19z"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="m13.06 12 6.47-6.47-1.06-1.06L12 10.94 5.53 4.47 4.47 5.53 10.94 12l-6.47 6.47 1.06 1.06L12 13.06l6.47 6.47 1.06-1.06L13.06 12Z"/></svg>',
    # WordPress core image block "expand on click" icon
    "expand": '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path fill="#fff" d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z"/></svg>',
}
CUR = ' aria-current="page"'
CHEVRON = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" focusable="false"><path d="M1.50002 4L6.00002 8L10.5 4" stroke-width="1.5"></path></svg>'


def srcset(root, name):
    widths, w, h = IMGS[name]
    return ", ".join(f"{root}assets/img/{name}-{x}.webp {x}w" for x in widths)


def img(root, name, alt, sizes, cls="", eager=False, extra=""):
    widths, w, h = IMGS[name]
    default = widths[1] if len(widths) > 1 else widths[0]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    ss = f' srcset="{srcset(root, name)}" sizes="{sizes}"' if len(widths) > 1 else ""
    return (f'<img{c} src="{root}assets/img/{name}-{default}.webp"{ss} '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{extra}>')


def lightbox_figure(root, name, alt, sizes, cls="wp-block-image size-large is-style-rounded clip-reveal", caption="", key=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    k = f' data-vt-key="{key}"' if key else ""
    return (f'<figure class="{cls} wp-lightbox-container">{img(root, name, alt, sizes, extra=k)}'
            f'<button class="lightbox-trigger" type="button" aria-haspopup="dialog" aria-label="Enlarge: {alt}">{SVG["expand"]}</button>{cap}</figure>')


def button(href, label, style="", icon=None, attrs=""):
    cls = "wp-block-button" + (f" is-style-{style}" if style else "")
    ic = SVG[icon] if icon else ""
    lead = ic if icon == "phone" else ""
    trail = ic if icon == "arrow" else ""
    return f'<div class="{cls}"><a class="wp-block-button__link wp-element-button" href="{href}"{attrs}>{lead}{label}{trail}</a></div>'


def buttons(*items, center=False):
    j = " is-content-justification-center" if center else ""
    return f'<div class="wp-block-buttons is-layout-flex{j}">{"".join(items)}</div>'


def quote_link(root, service=None, extra=None):
    params = []
    if service:
        params.append("service=" + service)
    if extra:
        params.append(extra)
    return f"{root}quote/" + ("?" + "&amp;".join(params) if params else "")


def reveal(i=0):
    return f' style="--reveal-delay:{i * 0.08:.2f}s"' if i else ""


def asterisk_h2(text, hid="", center=False):
    i = f' id="{hid}"' if hid else ""
    c = " has-text-align-center" if center else ""
    return f'<h2 class="wp-block-heading is-style-asterisk{c}"{i}>{text}</h2>'


NAV = [("Home", ""), ("Services", "services/"), ("Projects", "projects/"), ("About", "about-us/"), ("Reviews", "reviews/"), ("Contact", "contact-us/")]
SPECULATION = {"prerender": [{"source": "document", "where": {"and": [{"href_matches": "/*"},
               {"not": {"href_matches": "/*\\?*"}}, {"not": {"selector_matches": "a[rel~=nofollow]"}}]}, "eagerness": "moderate"}]}


def head(root, title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Prototype preview. Remove this noindex line at launch. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#151515">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&amp;family=Inter:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" id="wp-block-library-css" href="{root}assets/css/wp-blocks.css?ver=11.2.0">
<link rel="stylesheet" id="twentytwentyfour-child-style-css" href="{root}assets/css/site.css?ver={ver('assets/css/site.css')}">
<meta name="site-build" content="{BUILD}">
{PAGEREVEAL}
{SELF_HEAL.replace("ROOT", root).replace("BUILD", BUILD)}
<script type="speculationrules">{json.dumps(SPECULATION)}</script>
{extra}<script src="{root}assets/js/site.js?ver={ver('assets/js/site.js')}" defer></script>
</head>"""


def href(root, h):
    return (root + h) or "./"


def brand(root, tag="div"):
    home = root or "./"
    return (f'<a class="site-brand" href="{home}" rel="home" aria-label="{NAME}, home">'
            f'<img src="{root}assets/img/logo.webp" width="183" height="160" alt="">'
            f'<span class="site-brand__text"><span class="wp-block-site-title">{NAME}</span>'
            f'<span class="wp-block-site-tagline">Post-construction &amp; commercial cleaning</span></span></a>')


def mega_menu(root):
    cards = "".join(
        f'<a class="mega-card" href="{root}services/#{s["id"]}" data-vt>'
        f'<img src="{root}assets/img/{s["img"]}-{IMGS[s["img"]][0][0]}.webp" width="{IMGS[s["img"]][1]}" height="{IMGS[s["img"]][2]}" alt="" loading="lazy" decoding="async" data-vt-key="svc-{s["id"]}">'
        f'<span class="mega-card__title">{s["name"]}</span><span class="mega-card__text">{s["card"]}</span></a>'
        for s in SERVICES)
    return (f'<div class="mega-menu" id="mega-services"><div class="mega-menu__inner">'
            f'<div class="mega-menu__intro"><h2 class="wp-block-heading is-style-asterisk">Services</h2>'
            f'<p>From the first debris haul on a new build to the nightly clean once it opens.</p>'
            f'<a class="more-link" href="{root}services/">All services {SVG["arrow"]}</a></div>'
            f'<div class="mega-menu__grid">{cards}</div></div></div>')


def topbar():
    return f"""<div class="topbar has-global-padding">
  <div class="topbar__inner">
    <ul><li><strong>Since 2006</strong> &middot; Broward, Miami-Dade and Palm Beach</li><li>Woman-owned &middot; Certified MWBE</li></ul>
    <ul><li><span data-hours-status><span data-hours-text>{HOURS_TEXT}</span></span></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
  </div>
</div>"""


def header(root, active):
    items = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        link = f'<a class="wp-block-navigation-item__content" href="{href(root, h)}"{cur}>{l}</a>'
        if h == "services/":
            items.append(f'<li class="wp-block-navigation-item has-child open-on-hover-click wp-block-navigation-submenu has-mega-menu">{link}'
                         f'<button class="wp-block-navigation__submenu-icon wp-block-navigation-submenu__toggle" type="button" aria-expanded="false" aria-controls="mega-services" aria-label="Services submenu">{CHEVRON}</button>'
                         f'{mega_menu(root)}</li>')
        else:
            items.append(f'<li class="wp-block-navigation-item">{link}</li>')
    sub = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    overlay = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        extra = f'<ul class="overlay-sub">{sub}</ul>' if h == "services/" else ""
        overlay.append(f'<li><a href="{href(root, h)}"{cur}>{l}</a>{extra}</li>')
    phone_svg = SVG["phone"].replace("<svg ", '<svg width="17" height="17" ')
    return f"""<a class="skip-link screen-reader-text" href="#wp--skip-link--target">Skip to content</a>
{topbar()}
<header class="wp-block-template-part site-header has-global-padding">
  <div class="site-header__inner">
    {brand(root)}
    <nav class="wp-block-navigation" aria-label="Main"><ul class="wp-block-navigation__container">{"".join(items)}</ul></nav>
    <div class="header-tools">
      <a class="header-phone" href="tel:{TEL}">{phone_svg}{PHONE}</a>
      <a class="icon-button header-call" href="tel:{TEL}" aria-label="Call {PHONE}">{SVG["phone"]}</a>
      <div class="wp-block-button header-quote"><a class="wp-block-button__link wp-element-button" href="{root}quote/" data-vt>Request a quote</a></div>
      <button class="wp-block-navigation__responsive-container-open icon-button" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="Open menu">{SVG["menu"]}</button>
    </div>
  </div>
  <div class="wp-block-navigation__responsive-container" role="dialog" aria-modal="true" aria-label="Menu">
    <button class="wp-block-navigation__responsive-container-close icon-button" type="button" aria-label="Close menu">{SVG["close"]}</button>
    <ul>{"".join(overlay)}</ul>
    {buttons(button(root + "quote/", "Request a quote", "", None, " data-vt"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}
    <p class="overlay-meta">{HOURS_TEXT} &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</header>"""


def footer(root):
    svc = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    offices = "".join(f'<li>{o["city"].split(",")[0]}: <a href="tel:{o["tel"]}">{o["phone"]}</a></li>' for o in OFFICES)
    return f"""<footer class="wp-block-template-part site-footer has-global-padding">
  <div class="site-footer__inner">
    <div class="footer-top">
      <div class="footer-brand">
        {brand(root)}
        <p>We clean corners, so you don't have to. Post-construction and commercial cleaning across South Florida since 2006.</p>
      </div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="{root}projects/">Projects</a></li>
        <li><a href="{root}about-us/">About us</a></li>
        <li><a href="{root}reviews/">Reviews</a></li>
        <li><a href="{root}contact-us/">Contact</a></li>
        <li><a href="{root}quote/">Request a quote</a></li>
      </ul></div>
      <div><h2>Offices</h2><ul>{offices}</ul></div>
      <div><h2>Get in touch</h2><ul>
        <li><a href="tel:{TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{HOURS_TEXT}</li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &middot; <a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
      </ul></div>
    </div>
    <p class="footer-creds">Licensed with the State of Florida &middot; Insured and bonded &middot; Certified MWBE &middot; Broward County Public Schools certified vendor &middot; OSHA 10 and OSHA 30 trained crews &middot; US Department of Commerce Firm of the Year recipient</p>
    <div class="footer-bottom"><p>&copy; <span data-year>2026</span> Legally Clean Inc.</p><button class="swept" type="button" data-swept title="Sweep again">Page swept clean <span data-swept-text>just now</span></button><p>Lauderhill &middot; Miami &middot; West Palm Beach</p></div>
  </div>
</footer>"""


def mobile_actions(root):
    return f"""<div class="mobile-actions" role="region" aria-label="Quick actions">
  {button("tel:" + TEL, "Call", "outline", "phone")}
  {button(root + "quote/", "Request a quote", "", "arrow", " data-vt")}
</div>"""


def page(depth, path, title, desc, active, main, extra_head="", actions=True, body_class="page"):
    root = "../" * depth
    html = f"""{head(root, title, desc, path, extra_head)}
<body class="{body_class}{" has-mobile-actions" if actions else ""}">
<div class="wp-site-blocks">
{header(root, active)}
<main class="wp-block-group" id="wp--skip-link--target">
{main(root)}
</main>
{footer(root)}
</div>
{mobile_actions(root) if actions else ""}
</body>
</html>
"""
    target = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as f:
        f.write(html)
    print("wrote", os.path.relpath(target, OUT))


# ---------- content ----------

SERVICES = [
    {"id": "post-construction", "name": "Post-construction cleanup", "short": "Post-construction", "img": "post-construction",
     "alt": "Legally Clean crew member vacuuming new cabinets during a school final clean",
     "card": "Rough, final and punch-list cleans for contractors, from the first debris haul to the owner walkthrough.",
     "for": "General contractors, developers, property managers"},
    {"id": "janitorial", "name": "Commercial janitorial", "short": "Janitorial", "img": "janitorial",
     "alt": "Cleaner wiping down a desk in an office",
     "card": "A regular crew on a set schedule: daily, weekly or custom, worked around your business hours.",
     "for": "Offices, banks, schools, clinics, condo common areas"},
    {"id": "deep-clean", "name": "Commercial deep cleaning", "short": "Deep cleaning", "img": "deep-clean",
     "alt": "Stainless steel commercial kitchen",
     "card": "A periodic reset for kitchens, floors, vents and busy areas that the regular crew isn't scoped for.",
     "for": "Restaurants, offices, retail, bank branches"},
    {"id": "floors-windows", "name": "Floors and windows", "short": "Floors and windows", "img": "floors-windows",
     "alt": "Legally Clean crew member cleaning window frames along a glass wall",
     "card": "Strip and wax, construction haze off tile and concrete, and windows up to the upper floors.",
     "for": "Buildouts, tenant turnovers, ongoing upkeep"},
]

SERVICE_OPTIONS = [("post-construction", "Post-construction"), ("janitorial", "Janitorial"), ("deep-clean", "Deep cleaning"),
                   ("floors-windows", "Floors and windows"), ("pressure-washing", "Pressure washing"), ("something-else", "Something else")]
SERVICE_ICON = {
    # hard hat
    "post-construction": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/>',
    # building
    "janitorial": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    # sparkles
    "deep-clean": '<path d="M9.94 14.06 4 20"/><path d="m14 4 1.1 2.9L18 8l-2.9 1.1L14 12l-1.1-2.9L10 8l2.9-1.1z"/><path d="M5 3v4M3 5h4M19 15v4M17 17h4"/>',
    # window
    "floors-windows": '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/>',
    # droplets
    "pressure-washing": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    # plus in circle
    "something-else": '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>',
}
SERVICE_DESC = {
    "post-construction": "Rough, final or punch-list clean",
    "janitorial": "Recurring cleaning on a schedule",
    "deep-clean": "One-time or quarterly reset",
    "floors-windows": "Strip and wax, glass inside and out",
    "pressure-washing": "Sidewalks, parking, dumpster pads",
    "something-else": "Tell us in the next step",
}
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"/></svg>'

REVIEWS = {
    "scott": ("Scott M.", "I have known Sherri and her team for many years. They&rsquo;re always on time always on budget and always have a smile whether it be a personal home or an Airbnb or a construction site. She is always there and always reasonable. I can&rsquo;t say enough about her."),
    "perry": ("Perry C.", "Legally Clean performed commercial cleaning services on a kitchen that had long been neglected. One particularly stubborn area was a stainless steel wall that had been painted over. Legally Clean implored several different cleaning techniques to clean the wall without damaging the finish. They were relentless in their efforts, delivering a superb clean once all was done."),
    "paul": ("Paul G.", "Sherry is amazing!! I highly recommend legally clean if you need commercial cleaning. They are super responsive and do an amazing job, definitely will use them again ."),
    "gyovanni": ("Gyovanni H.", "Legally Clean provided exceptional service at an affordable price! What stood out the most was that Sherry, the owner, personally showed up and worked alongside her team to ensure everything was done right. My home is now truly legally clean, and I&rsquo;m definitely looking forward to working with them again in the future!"),
    "colton": ("Colton M.", "Sherry and her team did a great job, went the extra mile to make sure our family was happy. We felt like we were in a new home once they were done! Very clean, highly recommended."),
}

CLIENT_LOGOS = [("kaufman-lynn", "Kaufman Lynn Construction", 108, 96, "is-tall"), ("suffolk", "Suffolk", 517, 96, "is-wordmark"),
                ("coastal", "Coastal Construction", 151, 96, "is-tall"), ("d-stephenson", "D. Stephenson Construction", 559, 96, ""),
                ("lunacon", "Lunacon", 246, 96, "is-tall"), ("broward-health", "Broward Health", 588, 96, "")]

JOB_PHOTOS = [
    ("job-cabinets", "Legally Clean crew member wiping down new casework in a school lab", "Final clean, school lab casework"),
    ("job-hallway", "Crew in hard hats and safety vests cleaning a new corridor", "Corridor final clean"),
    ("job-atrium", "Atrium on an active job site with lifts and materials", "Rough clean while trades work"),
]
STATS = [("20", "", "years on South Florida job sites", "is-pink"), ("24", "h", "Most projects start within 24 hours of booking", "")]

FAQS = [
    ("Who usually pays for the final clean, the GC or the owner?",
     "It depends on the contract. Most general contractors owe a broom clean before handoff. The detailed post-construction clean is often a separate scope that the owner or developer arranges. We work for either side."),
    ("When should we book the final clean?",
     "As soon as you have a completion date. We schedule it right behind the last trade (flooring, paint, electrical, plumbing) and before inspections and move-in, so dust from late work doesn't undo it."),
    ("How fast can you start?",
     f"Most projects can start within 24 hours. Call {PHONE} to check availability for your dates."),
    ("Can you send insurance and certifications before we start?",
     "Yes. We're licensed with the State of Florida, insured and bonded, and our credentials are available on request. Ask for them when you request a quote."),
    ("Do you clean after hours?",
     "Yes. Janitorial and deep cleaning are scheduled around your business hours, so staff and customers aren't working around us."),
    ("Which areas do you cover?",
     "All of Broward, Miami-Dade and Palm Beach counties, from offices in Lauderhill, Miami and West Palm Beach."),
]


# ---------- shared sections ----------

def gfield(label, inner, required=False, width="", stack=True, desc="", group=False, cls="", desc_below=False):
    req = '<span class="gfield_required" aria-hidden="true">*</span>' if required else ""
    w = (f" gfield--width-{width}" + (" stack-sm" if stack else "")) if width else ""
    grp = " data-group-required" if group and required else ""
    d = f'<div class="gfield_description{" below" if desc_below else ""}">{desc}</div>' if desc else ""
    if group:
        return (f'<fieldset class="gfield{w} {cls}"{grp}><legend class="gfield_label">{label}{req}</legend>'
                f'{"" if desc_below else d}<div class="ginput_container">{inner}</div>{d if desc_below else ""}<div class="validation_message" aria-live="polite"></div></fieldset>')
    return (f'<div class="gfield{w} {cls}">{label.format(req=req)}{"" if desc_below else d}<div class="ginput_container">{inner}</div>'
            f'{d if desc_below else ""}<div class="validation_message" aria-live="polite"></div></div>')


def lab(for_id, text):
    return f'<label class="gfield_label" for="{for_id}">{text}{{req}}</label>'


def service_choice_cards(input_type, large=False, options=None):
    items = []
    for v, l in options or SERVICE_OPTIONS:
        icon = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{SERVICE_ICON[v]}</svg>'
        desc = f'<span class="gcard__desc">{SERVICE_DESC[v]}</span>' if large else ""
        items.append(f'<li><label class="gcard"><input type="{input_type}" name="service" value="{v}">'
                     f'<span class="gcard__box"><span class="gcard__icon">{icon}</span><span class="gcard__text">{l}{desc}</span>'
                     f'<span class="gcard__tick">{TICK}</span></span></label></li>')
    cls = "gchoice-cards" + (" gchoice-cards--lg" if large else "")
    return f'<ul class="{cls}">{"".join(items)}</ul>'


def pills(name, values, input_type="radio"):
    return '<ul class="pill-choices">' + "".join(
        f'<li><label><input type="{input_type}" name="{name}" value="{v}"><span>{v}</span></label></li>' for v in values) + "</ul>"


HOURS = [("Monday", "8am to 6pm"), ("Tuesday", "8am to 6pm"), ("Wednesday", "8am to 6pm"), ("Thursday", "8am to 6pm"),
         ("Friday", "8am to 6pm"), ("Saturday", "8am to 6pm"), ("Sunday", "Closed")]


def hours_table():
    rows = "".join(f'<tr data-day="{d}"><td>{d}</td><td>{h}</td></tr>' for d, h in HOURS)
    return f'<table class="hours-table"><caption class="screen-reader-text">Opening hours</caption>{rows}</table>'


def status():
    return f'<span class="hours-status" data-hours-status><span class="status-dot"></span><span data-hours-text>{HOURS_TEXT}</span></span>'


def banner(root, crumb, title, lede):
    return f"""<section class="wp-block-group alignfull page-banner has-global-padding">
  <div class="page-banner__inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{root or './'}">Home</a> / {crumb}</nav>
    <h1 class="wp-block-heading" data-split>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def job_strip(root):
    figs = [f'<figure class="wp-block-image size-large wp-lightbox-container clip-reveal">{img(root, n, alt, "(min-width: 700px) 20vw, 62vw")}'
            f'<button class="lightbox-trigger" type="button" aria-haspopup="dialog" aria-label="Enlarge: {alt}">{SVG["expand"]}</button>'
            f'<figcaption class="wp-element-caption">{cap}</figcaption></figure>'
            for n, alt, cap in JOB_PHOTOS]
    stats = [f'<div class="stat-tile {c}"><p class="stat-tile__num"><span data-count="{n}">{n}</span>{suf}</p><p>{t}</p></div>' for n, suf, t, c in STATS]
    tiles = [figs[0], stats[0], figs[1], stats[1], figs[2]]
    return f"""<section class="wp-block-group alignfull job-strip has-global-padding" aria-label="Recent job sites">
  <div class="wp-block-gallery has-nested-images columns-5 is-cropped wp-reveal">{"".join(tiles)}</div>
</section>"""


def client_logos(root, label="General contractors and facilities we've worked with"):
    logos = "".join(f'<li><img class="{c}" src="{root}assets/img/clients/{k}.webp" width="{w}" height="{h}" alt="{n}" loading="lazy" decoding="async"></li>'
                    for k, n, w, h, c in CLIENT_LOGOS)
    return f"""<section class="wp-block-group alignfull client-logos has-global-padding" aria-label="Clients">
  <div class="client-logos__inner wp-reveal">
    <p class="client-logos__label kicker">{label}</p>
    <ul>{logos}</ul>
    <p class="client-logos__more">Also trusted by Balfour Beatty, Skanska USA and Pirtle Construction.</p>
  </div>
</section>"""


def service_cards(root, link_to_anchor=True):
    cards = []
    for i, s in enumerate(SERVICES):
        h = f"{root}services/#{s['id']}" if link_to_anchor else f"#{s['id']}"
        cards.append(f"""<div class="svc-card wp-reveal"{reveal(i)}>
  <a href="{h}" data-vt>
    <figure class="wp-block-image clip-reveal">{img(root, s["img"], s["alt"], "(min-width: 900px) 25vw, 50vw", extra=' data-vt-key="svc-' + s["id"] + '"')}</figure>
    <span class="svc-card__num">0{i + 1}</span>
    <h3 class="wp-block-heading">{s["name"]}</h3>
    <p>{s["card"]}</p>
    <p class="svc-card__for"><strong>Good for:</strong> {s["for"]}</p>
    <span class="more-link">Learn more {SVG["arrow"]}</span>
  </a>
</div>""")
    return f'<div class="svc-grid">{"".join(cards)}</div>'


PHASES = [
    ("1", "Rough clean", "While trades are still working",
     "Debris removal, bulk trash haul-off, sweeping and first dust control, so the crews still on site can work safely.",
     ["Bulk debris and packaging out", "Sweeping and dust control", "Keeps the site workable"]),
    ("2", "Final clean", "After the last trade is done",
     "Every surface brought up to move-in standard: floors, walls, baseboards, cabinets, countertops, fixtures and windows.",
     ["Floors, walls and baseboards", "Cabinets, counters and fixtures", "Glass inside and accessible outside"]),
    ("3", "Punch-list clean", "Right before the walkthrough",
     "One more pass for what shows up after the final trades wrap: paint overspray, adhesive residue, fingerprints and dust that settles again.",
     ["Items flagged at walkthrough", "Overspray and sticker residue", "Resettled dust"]),
]


def phases_section(root):
    track = "".join(f'<li data-step="{n}"><span class="phase-when">{w}</span></li>' for n, t, w, _, _ in PHASES)
    cols = "".join(
        f'<div class="phase wp-reveal" data-step="{n}"{reveal(i)}><h3 class="wp-block-heading">{t}</h3><p>{d}</p>'
        f'<ul class="wp-block-list is-style-checkmark-list punch">{"".join(f"<li style=--i:{j}>{x}</li>" for j, x in enumerate(items))}</ul></div>'
        for i, (n, t, w, d, items) in enumerate(PHASES))
    return f"""<section class="wp-block-group alignfull section has-accent-background-color has-global-padding" aria-labelledby="phases-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">
      <div><span class="kicker">Post-construction</span>{asterisk_h2('Rough, final, <span class="nowrap">punch-list</span>. One crew for all three.', "phases-title")}</div>
      <p>Construction cleanup isn't one pass with a broom. We phase it around your schedule so the space is ready when the owner walks it.</p>
    </div>
    <div class="phases-head wp-reveal"><ol class="phases-track" aria-hidden="true">{track}</ol><p class="inspection-stamp" aria-hidden="true"><span>Ready for</span>walkthrough</p></div>
    <div class="phases">{cols}</div>
    <p class="timing-note wp-reveal">On a mid-size commercial build, a rough clean usually takes one to two days. All three phases usually run three to five days. Every quote comes with a timeline.</p>
    <div class="addons wp-reveal"><strong>Add to any phase:</strong><span>Floor stripping and waxing</span><span>Windows, 2nd story and up</span><span>Pressure washing</span><span>HEPA vacuums for fine dust</span></div>
  </div>
</section>"""


def project_banner(root, heading_tag="h2", link=True):
    more = f'<p style="margin-top:22px"><a class="more-link" href="{root}projects/" data-vt="bh-er">See more projects {SVG["arrow"]}</a></p>' if link else ""
    return f"""<section class="wp-block-group alignfull section project-banner has-base-2-background-color has-global-padding" aria-labelledby="bh-title">
  <div class="wide">
    <div class="wp-block-columns alignwide is-layout-flex wp-reveal">
      <div class="wp-block-column project-banner__label">
        <span class="kicker">Featured project</span>
        <{heading_tag} class="wp-block-heading has-body-font-family has-medium-font-size" id="bh-title" style="margin-top:10px;font-weight:600">Broward Health Emergency Room</{heading_tag}>
        <p>Sunrise, Florida</p>
      </div>
      <div class="wp-block-column">
        <p class="project-banner__statement has-heading-font-family">We handled the post-construction cleanup for Broward Health&rsquo;s brand new Emergency Room in Sunrise. From framing dust to opening day ready.</p>
        {more}
      </div>
    </div>
    <div class="wp-reveal">{lightbox_figure(root, "broward-health-er", "The new Broward Health Emergency Room in Sunrise, Florida", "(min-width: 1280px) 1280px, 100vw", "wp-block-image alignwide size-large is-style-rounded clip-reveal", key="bh-er")}</div>
    <dl class="project-facts wp-reveal">
      <div><dt>Client</dt><dd>Broward Health</dd></div>
      <div><dt>Location</dt><dd>Sunrise, FL</dd></div>
      <div><dt>Scope</dt><dd>Post-construction cleanup</dd></div>
      <div><dt>Completed</dt><dd>2026</dd></div>
    </dl>
  </div>
</section>"""


CREDS = [
    ("In business", "Since 2006, founded by Sherry W. Rudolph"),
    ("Licensing", "Licensed with the State of Florida. Broward County business license."),
    ("Insurance", "Fully insured and bonded"),
    ("Ownership", "Woman-owned. Certified Minority/Women Business Enterprise (MWBE)."),
    ("Vendor certifications", "Broward County, Miami-Dade County, Broward County Public Schools and Miami-Dade County Schools"),
    ("Safety training", "OSHA 10 and OSHA 30 trained crews. HazCom trained: Safety Data Sheets, GHS labels, chemical dilution."),
    ("Recognition", "US Department of Commerce Firm of the Year recipient"),
]


def spec_table():
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in CREDS)
    return f'<figure class="wp-block-table spec-table"><table><caption class="screen-reader-text">Legally Clean credentials</caption><tbody>{rows}</tbody></table></figure>'


def creds_section(root, bg=""):
    return f"""<section class="wp-block-group alignfull section has-global-padding{bg}" aria-labelledby="creds-title">
  <div class="creds wide">
    <div class="creds__intro wp-reveal">
      <span class="kicker">For GCs and facility managers</span>
      {asterisk_h2("Paperwork ready before the first crew shows up", "creds-title")}
      <p>Contractors and property managers need a licensed, insured vendor on file before anyone sets foot on site. Here's what we bring. Ask, and we'll send the documents with your quote.</p>
      <p>Our MWBE certification is recognized by government and commercial procurement offices for supplier diversity programs.</p>
      {buttons(button(root + "contact-us/?topic=credentials", "Request our credentials", "dark", "arrow"))}
    </div>
    <div class="wp-reveal"{reveal(1)}>{spec_table()}</div>
  </div>
</section>"""


def testimonial(root, key="scott", link=True):
    name, text = REVIEWS[key]
    more = f'<a class="more-link" href="{root}reviews/">Read more reviews {SVG["arrow"]}</a>' if link else ""
    return f"""<section class="wp-block-group alignfull section testimonial-centered has-contrast-background-color has-global-padding" aria-label="Customer review">
  <div class="wp-reveal">
    <blockquote class="wp-block-quote is-style-plain"><p>&ldquo;{text}&rdquo;</p><cite><strong>{name}</strong><span>Legally Clean customer</span></cite></blockquote>
    {more}
  </div>
</section>"""


def owner_section(root):
    return f"""<section class="wp-block-group alignfull section owner has-global-padding" aria-labelledby="owner-title">
  <div class="wide">
    <div class="wp-block-columns alignwide is-layout-flex">
      <div class="wp-block-column wp-reveal">{lightbox_figure(root, "sherry", "Sherry W. Rudolph, founder and President of Legally Clean", "(min-width: 782px) 38vw, 300px", key="sherry")}</div>
      <div class="wp-block-column owner__text wp-reveal"{reveal(1)}>
        <span class="kicker">The owner</span>
        {asterisk_h2("Sherry Rudolph, the Pink Construction Hat Diva", "owner-title")}
        <p>Sherry founded Legally Clean in 2006 and still shows up on the job. Clients mention it in their reviews: the owner on site, working next to her crew.</p>
        <p>The company hires with a purpose, too. Sherry spent more than 20 years as an employment specialist, and Legally Clean creates jobs for people who face real barriers to employment.</p>
        {buttons(button(root + "about-us/", "About Legally Clean", "outline", "arrow", ' data-vt="sherry"'))}
      </div>
    </div>
  </div>
</section>"""


def offices_section(root, heading="Three offices, three counties", bg=" has-accent-background-color"):
    cols = []
    for i, o in enumerate(OFFICES):
        maps = "https://www.google.com/maps/search/?api=1&amp;query=" + quote_plus(o["street"] + ", " + o["city"])
        cols.append(f"""<div class="office wp-reveal"{reveal(i)}>
  <span class="kicker">{o["label"]}</span>
  <h3 class="wp-block-heading">{o["county"]}</h3>
  <address>{o["street"]}<br>{o["city"]}</address>
  <a class="office-phone" href="tel:{o["tel"]}">{o["phone"]}</a>
  <p class="office-cities">{o["cities"]}, and the rest of the county.</p>
  <a class="more-link" href="{maps}" target="_blank" rel="noopener">Open in Maps {SVG["arrow"]}</a>
</div>""")
    return f"""<section class="wp-block-group alignfull section has-global-padding{bg}" aria-labelledby="offices-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">
      {asterisk_h2(heading, "offices-title")}
      <p>Crews cover all of Broward, Miami-Dade and Palm Beach. Open {HOURS_TEXT}. {status()}</p>
    </div>
    <div class="offices">{"".join(cols)}</div>
  </div>
</section>"""


def faq_section(root, faqs=FAQS):
    items = "".join(f'<details class="wp-block-details is-style-arrow-icon-details"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return f"""<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="faq-title">
  <div class="faq wide">
    <div class="faq__intro wp-reveal">
      {asterisk_h2("Questions contractors ask us", "faq-title")}
      <p>Something else? Call <a href="tel:{TEL}">{PHONE}</a> and ask for Sherry.</p>
    </div>
    <div class="faq__list wp-reveal"{reveal(1)}>{items}</div>
  </div>
</section>"""


def band(root):
    return f"""<div class="wp-block-cover alignfull has-parallax band-cover" data-dust>
  <div role="img" aria-label="Worker sweeping debris off plastic floor protection" class="wp-block-cover__image-background has-parallax" style="background-position:50% 50%;background-image:url({root}assets/img/hero-1280.webp)"></div>
  <span aria-hidden="true" class="wp-block-cover__background has-background-dim-80 has-background-dim" style="background-color:#151515"></span>
  <div class="wp-block-cover__inner-container has-text-align-center wp-reveal">
    <span class="band-kicker">24 hours</span>
    <h2 class="wp-block-heading">Walkthrough coming up?</h2>
    <p>Most projects can start within 24 hours. Send the details or call, and we'll get a crew on the schedule.</p>
    {buttons(button(root + "quote/", "Request a quote", "", "arrow", " data-vt"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"), center=True)}
  </div>
  <p class="dust-hint" hidden><span class="dust-hint__mouse">Go on, wipe the glass.</span><span class="dust-hint__touch">Drag to wipe the glass.</span> The dust settles again, which is why there's a punch-list clean.</p>
</div>"""


def cta(root, title="Tell us about the job", text="Send the scope, the address and your dates. We'll come back with a timeline and a free quote."):
    return f"""<section class="wp-block-group alignfull section has-contrast-background-color has-global-padding">
  <div class="has-text-align-center wp-reveal" style="max-width:720px;margin:0 auto">
    {asterisk_h2(title, "", True)}
    <p style="margin:16px auto 0;max-width:48ch;color:rgb(255 255 255 / .74)">{text}</p>
    <div style="margin-top:28px">{buttons(button(root + "quote/", "Request a quote", "", "arrow", " data-vt"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"), center=True)}</div>
  </div>
</section>"""


# ---------- Home ----------

def home(root):
    check = SVG["check"]
    clock = SVG["clock"]
    return f"""
<section class="wp-block-group alignfull hero has-contrast-background-color has-global-padding" aria-labelledby="hero-title">
  <div class="hero__grid">
    <div>
      <span class="is-style-pill">Since 2006 &middot; Woman-owned &middot; Certified MWBE</span>
      <h1 class="wp-block-heading" id="hero-title" data-split>Post-construction and commercial cleaning across <em>South Florida</em></h1>
      <p class="hero-lede">Rough, final and punch-list cleans for general contractors. Janitorial and deep cleaning for the buildings once they open. Broward, Miami-Dade and Palm Beach.</p>
      <div data-hero-cta>{buttons(button(root + "quote/", "Request a quote", "", "arrow", " data-vt"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}</div>
      <ul class="hero-points">
        <li>{check}Most projects start within 24 hours</li>
        <li>{check}Licensed, insured and bonded</li>
        <li>{check}OSHA 10 and OSHA 30 trained crews</li>
        <li data-hours-status>{clock}<span data-hours-text>{HOURS_TEXT}</span></li>
      </ul>
    </div>
    <div class="quote-card">
      <div class="quote-card__head"><h2 class="wp-block-heading">Request a quote</h2><p>Free, no obligation.<br>Or call <a href="tel:{TEL}">{PHONE}</a></p></div>
      <div class="gform_wrapper">
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_fields">
            {gfield(lab("h-name", "Name"), '<input id="h-name" name="name" type="text" autocomplete="name" required>', True, "half")}
            {gfield(lab("h-company", "Company"), '<input id="h-company" name="company" type="text" autocomplete="organization">', False, "half")}
            {gfield(lab("h-phone", "Phone"), '<input id="h-phone" name="phone" type="tel" autocomplete="tel" required>', True, "half", stack=False)}
            {gfield(lab("h-zip", "Project ZIP"), '<input id="h-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, "half", stack=False)}
            {gfield("What do you need?", service_choice_cards("radio", options=SERVICE_OPTIONS[:4]), True, group=True)}
          </div>
          <div class="gform_footer"><button class="wp-element-button" type="submit">Get my free quote</button></div>
          <p class="gform_note">We reply {HOURS_TEXT}.</p>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! We got your request.</h3><p>We'll be in touch during business hours. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
  </div>
</section>

{job_strip(root)}
{client_logos(root)}

<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--30)" aria-labelledby="services-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">
      {asterisk_h2("What we clean", "services-title")}
      <p>One company for the build and everything after it: the post-construction clean first, then the regular janitorial program once the doors open.</p>
    </div>
    {service_cards(root)}
  </div>
</section>

{phases_section(root)}
{project_banner(root)}
{creds_section(root)}
{testimonial(root)}
{owner_section(root)}
{offices_section(root)}
{faq_section(root)}
{band(root)}
"""


# ---------- Services ----------

DETAIL = {
    "post-construction": {
        "img": "post-construction", "alt": "Legally Clean crew member vacuuming new cabinets during a school final clean", "kicker": "For contractors and developers",
        "body": ["We handle the whole cleanup, from the first debris haul to the last touch-up before the owner walks the space. We coordinate with your site supervisor so cleaning never holds up closeout.",
                 "Each phase can be booked on its own, but most commercial jobs need all three. Skipping the punch-list clean is how fingerprints and resettled dust end up on an inspection report."],
        "lists": [("What's included", ["Rough clean during construction", "Final clean before handoff", "Punch-list and touch-up clean", "Floor cleaning, strip and wax", "Interior and exterior windows", "Pressure washing"]),
                  ("Projects", ["Retail and office buildouts", "Restaurant buildouts and renovations", "Warehouses and industrial", "New construction", "Remodels and renovations", "Demolition cleanup and debris removal"])]},
    "janitorial": {
        "img": "janitorial", "alt": "Cleaner wiping down a desk in an office", "kicker": "Recurring",
        "body": ["A regular crew that cleans your building the same way every visit. Daily, weekly, every other week, or a custom schedule, worked around your business hours.",
                 "Our crews are trained on the OSHA HazCom standard. They read Safety Data Sheets, know GHS chemical labels and track dilution, which matters in schools, clinics and banks."],
        "lists": [("Every visit", ["Trash out and fresh liners", "Floors swept, mopped and vacuumed", "Restrooms cleaned and restocked", "Break rooms and common areas", "Dusting and polishing", "Door handles, switches and shared equipment disinfected"]),
                  ("Buildings", ["Offices and law or real estate offices", "Banks", "Retail", "Clinics and medical facilities", "Schools", "Country clubs, gyms, condo common areas"])]},
    "deep-clean": {
        "img": "deep-clean", "alt": "Stainless steel commercial kitchen", "kicker": "Periodic",
        "body": ["Most janitorial contracts are scoped for upkeep. A deep clean is the reset: the grime in grout, the kitchen grease, the vents and baseboards a regular crew doesn't get to.",
                 "Book it quarterly, before an inspection, after a renovation, at lease turnover or before a reopening."],
        "lists": [("What's included", ["Floor cleaning and treatment (tile, VCT, grout)", "Kitchen and back-of-house degreasing", "Lobbies, teller stations and waiting areas", "Fixtures, glass, baseboards and vents", "Restrooms, break rooms and shared spaces"]),
                  ("Good for", ["Restaurants", "Offices", "Banks and financial branches", "Retail spaces"])]},
    "floors-windows": {
        "img": "floors-windows", "alt": "Legally Clean crew member cleaning window frames along a glass wall", "kicker": "Specialty",
        "body": ["Construction leaves adhesive, paint and grout haze on tile, hardwood, laminate, concrete and VCT. We deep clean and strip it, then wax it for a new-floor shine. A typical 3,000 to 5,000 sq ft office floor takes about one working day.",
                 "Windows get cleaned inside and out, including exterior glass on the second story and up, with tracks and sills detailed. Outside, we pressure wash sidewalks, parking areas, dumpster pads and building exteriors."],
        "lists": [("Floors", ["Tile and grout", "VCT", "Concrete", "Hardwood and laminate", "Strip and wax"]),
                  ("Glass and outside", ["Exterior windows, 2nd story and up", "Tracks and sills", "Sidewalks and parking areas", "Dumpster pads", "Building exteriors"])]},
}
BUILDINGS = ["Offices", "Banks", "Retail", "Restaurants", "Schools", "Clinics and healthcare", "Warehouses", "Country clubs", "Condo common areas", "Gyms and rec centers"]


def services(root):
    rows = []
    for i, s in enumerate(SERVICES):
        d = DETAIL[s["id"]]
        flip = " svc-row--flip" if i % 2 else ""
        bg = " has-base-2-background-color" if i % 2 else ""
        lists = "".join(f'<div><h3 class="wp-block-heading">{t}</h3><ul class="wp-block-list is-style-checkmark-list">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for t, items in d["lists"])
        rows.append(f"""<section class="wp-block-group alignfull section has-global-padding{bg}" id="{s["id"]}" aria-labelledby="{s["id"]}-title">
  <div class="svc-row{flip} wide wp-reveal">
    {lightbox_figure(root, d["img"], d["alt"], "(min-width: 900px) 50vw, 100vw", key="svc-" + s["id"])}
    <div class="svc-row__body">
      <span class="kicker">0{i + 1} &middot; {d["kicker"]}</span>
      {asterisk_h2(s["name"], s["id"] + "-title")}
      {"".join(f"<p>{p}</p>" for p in d["body"])}
      <div class="svc-row__lists">{lists}</div>
      {buttons(button(quote_link(root, s["id"]), "Request a quote", "", "arrow", " data-vt"), button("tel:" + TEL, "Call us", "outline", "phone"))}
    </div>
  </div>
</section>""")
    jump = "".join(f'<a href="#{s["id"]}">{s["name"]}</a>' for s in SERVICES)
    blds = "".join(f'<li><span class="is-style-asterisk" aria-hidden="true"></span>{b}</li>' for b in BUILDINGS)
    return f"""
{banner(root, "Services", "Commercial cleaning services", "Post-construction cleanup for contractors, then janitorial, deep cleaning and floor care for the buildings once they open. Broward, Miami-Dade and Palm Beach.")}
<section class="wp-block-group alignfull has-global-padding" style="padding-top:24px" aria-label="Jump to a service"><nav class="svc-jump wide">{jump}</nav></section>
{"".join(rows)}
<section class="wp-block-group alignfull section has-accent-background-color has-global-padding" aria-labelledby="buildings-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">
      {asterisk_h2("Buildings we clean", "buildings-title")}
      <p>Commercial and institutional spaces of all sizes, from a single office suite to multi-floor buildings and bank branch networks.</p>
    </div>
    <ul class="buildings wp-reveal">{"".join(f"<li>{b}</li>" for b in BUILDINGS)}</ul>
  </div>
</section>
{cta(root)}
"""


# ---------- Projects ----------

PROJECT_TYPES = ["Retail buildouts and renovations", "Commercial and office buildouts", "Restaurant buildouts and renovations",
                 "Industrial and warehouse construction", "New construction", "Home remodels and renovations", "Demolition cleanup and debris removal"]


def projects(root):
    types = "".join(f"<li>{t}</li>" for t in PROJECT_TYPES)
    return f"""
{banner(root, "Projects", "Projects", "Healthcare, schools and commercial buildouts across South Florida. A few recent jobs, photographed by our crews.")}
{project_banner(root, link=False)}
<section class="wp-block-group alignfull section has-global-padding" aria-label="More projects">
  <div class="project-list wide">
    <article class="project-item wp-reveal">
      <div class="project-item__text">
        <span class="kicker">Education</span>
        <h2 class="wp-block-heading">School buildout, final clean</h2>
        <p>Final clean on a new school building. New lab casework, countertops and floors brought up to move-in standard, with backpack vacuums pulling construction dust out of cabinets and drawers.</p>
        <ul class="wp-block-list is-style-checkmark-list"><li>Casework and countertops</li><li>Cabinet and drawer interiors</li><li>Floors and baseboards</li></ul>
      </div>
      <div class="project-item__media">
        {lightbox_figure(root, "job-cabinets", "Crew member wiping down new casework in a school lab", "(min-width: 900px) 28vw, 50vw")}
        {lightbox_figure(root, "post-construction", "Crew member with a backpack vacuum cleaning new cabinets", "(min-width: 900px) 28vw, 50vw")}
      </div>
    </article>
    <article class="project-item wp-reveal">
      <div class="project-item__text">
        <span class="kicker">Commercial</span>
        <h2 class="wp-block-heading">Rough and final cleans on large builds</h2>
        <p>A rough clean around lifts and materials while trades are still working, then the corridor-by-corridor final clean once they're gone. Crews work in hard hats and high-visibility vests on active sites.</p>
        <ul class="wp-block-list is-style-checkmark-list"><li>Debris and dust control during construction</li><li>Corridors, walls and floors before handoff</li><li>Window frames and glass walls</li></ul>
      </div>
      <div class="project-item__media">
        {lightbox_figure(root, "job-atrium", "Atrium on an active job site with lifts and materials", "(min-width: 900px) 28vw, 50vw")}
        {lightbox_figure(root, "job-hallway", "Crew in hard hats and safety vests cleaning a new corridor", "(min-width: 900px) 28vw, 50vw")}
      </div>
    </article>
    <article class="project-item wp-reveal">
      <div class="project-item__text">
        <span class="kicker">Glass</span>
        <h2 class="wp-block-heading">Window and frame detailing</h2>
        <p>Glass walls collect paint overspray, sticker residue and dust in the tracks. We detail frames, tracks and sills, and clean exterior glass on the second story and up.</p>
        <ul class="wp-block-list is-style-checkmark-list"><li>Frames, tracks and sills</li><li>Overspray and sticker residue</li><li>Upper-floor exterior glass</li></ul>
      </div>
      <div class="project-item__media is-single">
        {lightbox_figure(root, "floors-windows", "Crew member cleaning window frames along a glass wall", "(min-width: 900px) 40vw, 100vw")}
      </div>
    </article>
  </div>
</section>
<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="types-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">{asterisk_h2("Projects we clean after", "types-title")}<p>If it was built, gutted or remodeled, we can clean it for handover.</p></div>
    <ul class="project-types wp-reveal">{types}</ul>
  </div>
</section>
{client_logos(root)}
{cta(root, "Have a project closing out?", "Send the address, the square footage and your walkthrough date. We'll send a timeline and a free quote.")}
"""


# ---------- About ----------

MEMBERSHIPS = ["NABWIC", "Lauderhill Regional Chamber of Commerce", "District 9 Broward Advisory Board", "Lauderhill Business Incubator", "Board member, MODCO"]
WHO = ["General contractors", "Property managers", "Developers", "Restaurant owners", "Office managers", "Bank branch managers", "Retail developers", "Schools and government", "Healthcare facilities"]


def about(root):
    mem = "".join(f"<li>{m}</li>" for m in MEMBERSHIPS)
    who = "".join(f"<li>{w}</li>" for w in WHO)
    return f"""
{banner(root, "About us", "About Legally Clean", "A woman-owned commercial cleaning company, founded by Sherry W. Rudolph in 2006 and based in Lauderhill.")}
<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="story-title">
  <div class="wide">
    <div class="wp-block-columns alignwide is-layout-flex" style="align-items:center">
      <div class="wp-block-column wp-reveal">
        <div class="overlapped">
          {lightbox_figure(root, "sherry", "Sherry W. Rudolph, founder and President of Legally Clean", "(min-width: 782px) 36vw, 78vw", key="sherry")}
          {lightbox_figure(root, "job-hallway", "Legally Clean crew cleaning a new corridor", "(min-width: 782px) 22vw, 46vw")}
        </div>
      </div>
      <div class="wp-block-column about-story wp-reveal"{reveal(1)}>
        <span class="kicker">Our story</span>
        {asterisk_h2("Twenty years of job sites", "story-title")}
        <p>Sherry Rudolph started Legally Clean in 2006. In 2026 the company turns 20, with offices in Lauderhill, Miami and West Palm Beach and crews working with construction firms, government entities and healthcare facilities across the tri-county area.</p>
        <p>People in the industry call her the Pink Construction Hat Diva. She built the business on relationships and deadlines. Every construction job ends with a walkthrough date, and her systems are set up around hitting it.</p>
        <p>That track record earned her recognition as a US Department of Commerce Firm of the Year recipient.</p>
      </div>
    </div>
  </div>
</section>
<section class="wp-block-group alignfull section has-contrast-background-color has-global-padding" aria-label="How we hire">
  <div class="statement wp-reveal">
    <span class="kicker">How we hire</span>
    <p class="has-heading-font-family has-x-large-font-size">We hire with a mission: real jobs for people who face real barriers to employment.</p>
    <p style="margin-top:20px;color:rgb(255 255 255 / .7)">It comes from Sherry's 20-plus years as an employment specialist and her Bachelor of Social Work from Saginaw Valley State University.</p>
  </div>
</section>
{creds_section(root)}
<section class="wp-block-group alignfull section has-accent-background-color has-global-padding" aria-labelledby="who-title">
  <div class="wide">
    <div class="wp-block-columns alignwide is-layout-flex" style="align-items:flex-start">
      <div class="wp-block-column wp-reveal">
        {asterisk_h2("Who we work with", "who-title")}
        <ul class="buildings" style="margin-top:24px;grid-template-columns:repeat(2,minmax(0,1fr))">{who}</ul>
      </div>
      <div class="wp-block-column wp-reveal"{reveal(1)}>
        <h2 class="wp-block-heading is-style-asterisk">Memberships</h2>
        <ul class="memberships" style="margin-top:24px">{mem}</ul>
      </div>
    </div>
  </div>
</section>
{client_logos(root)}
{cta(root)}
"""


# ---------- Reviews ----------

def reviews(root):
    cards = "".join(f'<figure class="review-card wp-reveal"{reveal(i % 2)}><blockquote><p>&ldquo;{REVIEWS[k][1]}&rdquo;</p></blockquote><figcaption><cite>{REVIEWS[k][0]}</cite></figcaption></figure>'
                    for i, k in enumerate(["perry", "paul", "gyovanni", "colton"]))
    return f"""
{banner(root, "Reviews", "Reviews", "What contractors, business owners and clients say about Sherry and her crews.")}
{testimonial(root, link=False)}
<section class="wp-block-group alignfull section has-global-padding" aria-label="More reviews">
  <div class="review-grid wide">{cards}</div>
</section>
<section class="wp-block-group alignfull section has-accent-background-color has-global-padding">
  <div class="has-text-align-center wp-reveal" style="max-width:680px;margin:0 auto">
    {asterisk_h2("Worked with us recently?", "", True)}
    <p style="margin-top:14px;color:var(--wp--preset--color--contrast-2)">A short review helps other contractors and property managers find us.</p>
    <div style="margin-top:24px">{buttons(button(GOOGLE, "Review us on Google", "", None, ' target="_blank" rel="noopener"'), button(YELP, "Yelp", "outline", None, ' target="_blank" rel="noopener"'), button(FACEBOOK, "Facebook", "outline", None, ' target="_blank" rel="noopener"'), center=True)}</div>
  </div>
</section>
{cta(root)}
"""


# ---------- Contact ----------

def contact(root):
    offices = "".join(
        f'<div class="contact-line"><span class="kicker">{o["county"]}</span><p>{o["street"]}, {o["city"]}</p><a href="tel:{o["tel"]}">{o["phone"]}</a></div>'
        for o in OFFICES)
    topics = pills("topic", ["A quote", "Credentials or vendor paperwork", "A current job", "Something else"])
    return f"""
{banner(root, "Contact", "Contact us", f"Call the main line, email Sherry, or send the form. Open {HOURS_TEXT}.")}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="contact-layout">
    <div class="contact-main wp-reveal">
      <div class="contact-line"><span class="kicker">Main line</span><a class="big" href="tel:{TEL}">{PHONE}</a></div>
      <div class="contact-line"><span class="kicker">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="contact-line"><span class="kicker">Hours</span>{status()}{hours_table()}</div>
      {offices}
      <div class="contact-line"><span class="kicker">Payment</span><p>Visa, MasterCard, PayPal, Venmo and Zelle</p></div>
    </div>
    <div class="form-panel wp-reveal"{reveal(1)}>
      <div class="gform_wrapper">
        <div class="gform_heading"><h2 class="gform_title">Send us a message</h2><span class="gform_description">We'll get back to you during business hours. Want a price? The <a href="{root}quote/">quote form</a> asks the right questions.</span></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_fields">
            {gfield(lab("c-name", "Name"), '<input id="c-name" name="name" type="text" autocomplete="name" required>', True, "half")}
            {gfield(lab("c-company", "Company"), '<input id="c-company" name="company" type="text" autocomplete="organization">', False, "half")}
            {gfield(lab("c-phone", "Phone"), '<input id="c-phone" name="phone" type="tel" autocomplete="tel" required>', True, "half")}
            {gfield(lab("c-email", "Email"), '<input id="c-email" name="email" type="email" autocomplete="email" required>', True, "half")}
            {gfield("What's it about?", topics, True, group=True)}
            {gfield(lab("c-msg", "Message"), '<textarea id="c-msg" name="message" rows="5" required></textarea>', True)}
          </div>
          <div class="gform_footer"><button class="wp-element-button" type="submit">Send message</button></div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks for getting in touch!</h3><p>We'll get back to you during business hours. If it's urgent, call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
  </div>
</section>
{offices_section(root, "Our offices")}
"""


# ---------- Quote ----------

def quote(root):
    prev_btn = '<button class="wp-element-button gform_previous_button" type="button">Previous</button>'
    nxt = '<button class="wp-element-button gform_next_button" type="button">Next</button>'
    sub = '<button class="wp-element-button" type="submit">Send request</button>'

    def nav(prev, btn):
        return f'<div class="gform_page_footer">{prev_btn if prev else ""}{btn}</div>'

    lede = f'Three short steps. Rather talk it through? Call <a href="tel:{TEL}">{PHONE}</a>.'
    phases = pills("phases", ["Rough clean", "Final clean", "Punch-list clean", "Not sure yet"], "checkbox")
    buildings = pills("building", ["Office", "Retail", "Restaurant", "School", "Healthcare", "Bank", "Warehouse", "Multifamily or condo", "Other"])
    roles = pills("role", ["General contractor", "Property or facility manager", "Business owner", "Other"])
    contact_pref = pills("contact_pref", ["Phone call", "Email"])
    paul_name, paul_text = REVIEWS["paul"]
    return f"""
{banner(root, "Request a quote", "Request a quote", lede)}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="quote-layout">
    <div class="form-panel" data-vt-key="quote-panel">
      <div class="gform_wrapper">
        <div class="gf_progressbar_wrapper"><p class="gf_progressbar_title">Step 1 of 3 - Services</p><div class="gf_progressbar" aria-hidden="true"><div class="gf_progressbar_percentage" style="width:33%"><span>33%</span></div></div></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_page" data-title="Services">
            <div class="gform_fields">
              {gfield("What do you need?", service_choice_cards("checkbox", large=True), True, group=True, desc="Pick all that apply.")}
              {gfield("Which phases?", phases, False, group=True, desc="Not sure? We'll walk the site and tell you.", cls="js-phases")}
            </div>
            {nav(False, nxt)}
          </div>
          <div class="gform_page" data-title="The site" hidden>
            <div class="gform_fields">
              {gfield("Type of building", buildings, True, group=True)}
              {gfield(lab("q-size", "Approximate size (sq ft)"), '<input id="q-size" name="size" type="text" inputmode="numeric" placeholder="For example: 12,000">', False, "half")}
              {gfield(lab("q-zip", "Project ZIP code"), '<input id="q-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, "half")}
              {gfield(lab("q-date", "Start or walkthrough date"), '<input id="q-date" name="date" type="date">', False, "half", desc="If you have one.", desc_below=True)}
              {gfield(lab("q-files", "Plans or scope"), '<input id="q-files" name="files" type="file" multiple accept=".pdf,image/*">', False, "half", desc="PDF or photos, optional.", desc_below=True)}
              {gfield(lab("q-details", "Anything else we should know?"), '<textarea id="q-details" name="details" rows="4" placeholder="For example: three floors of office buildout, CO inspection on the 14th, after-hours access only"></textarea>')}
            </div>
            {nav(True, nxt)}
          </div>
          <div class="gform_page" data-title="Your details" hidden>
            <div class="gform_fields">
              {gfield(lab("q-name", "Name"), '<input id="q-name" name="name" type="text" autocomplete="name" required>', True, "half")}
              {gfield(lab("q-company", "Company"), '<input id="q-company" name="company" type="text" autocomplete="organization">', False, "half")}
              {gfield("Your role", roles, False, group=True)}
              {gfield(lab("q-phone", "Phone"), '<input id="q-phone" name="phone" type="tel" autocomplete="tel" required>', True, "half")}
              {gfield(lab("q-email", "Email"), '<input id="q-email" name="email" type="email" autocomplete="email" required>', True, "half")}
              {gfield("Best way to reach you", contact_pref, False, group=True)}
              {gfield("Vendor paperwork", '<label class="gchoice"><input type="checkbox" name="credentials" value="yes"> Send your license, insurance and certification documents with the quote</label>', False, group=True)}
            </div>
            {nav(True, sub)}
          </div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! Your request is in.</h3><p>We'll get back to you during business hours with next steps and a timeline. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
    <aside class="widget-area" aria-label="Sidebar">
      <section class="widget widget--dark">
        <h2 class="widget-title">Rather talk?</h2>
        <a class="widget-phone" href="tel:{TEL}">{PHONE}</a>
        {status()}
        {hours_table()}
      </section>
      <section class="widget">
        <h2 class="widget-title">Fast starts</h2>
        <p>Most projects can start within 24 hours of booking.</p>
      </section>
      <section class="widget">
        <h2 class="widget-title">Vendor paperwork</h2>
        <p>Licensed with the State of Florida, insured and bonded, certified MWBE. Credentials are available on request: tick the box in step 3.</p>
      </section>
      <section class="widget">
        <h2 class="widget-title">From a client</h2>
        <blockquote>&ldquo;{paul_text.strip()}&rdquo;</blockquote>
        <p class="has-contrast-2-color has-small-font-size">{paul_name}</p>
      </section>
    </aside>
  </div>
</section>
"""


def notfound(root):
    return f"""
<section class="wp-block-group alignfull notfound has-global-padding">
  <p class="notfound__code has-heading-font-family">404</p>
  <h1 class="wp-block-heading" data-split>This page got swept up with the debris</h1>
  <p>We clean corners, not broken links. Try the homepage or give us a call.</p>
  {buttons(button(root, "Go to the homepage", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}
</section>
"""


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Legally Clean Inc.", "alternateName": "Legally Clean",
        "url": "https://www.legallyclean.com/", "logo": BASE_URL + "assets/img/logo.png", "image": BASE_URL + "assets/img/og-image.jpg",
        "telephone": "+1-561-467-4400", "email": EMAIL, "foundingDate": "2006",
        "founder": {"@type": "Person", "name": "Sherry W. Rudolph"},
        "address": {"@type": "PostalAddress", "streetAddress": "1773 N State Rd 7, Ste 101 I", "addressLocality": "Lauderhill",
                    "addressRegion": "FL", "postalCode": "33313", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ["Broward County", "Miami-Dade County", "Palm Beach County"]],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00"}],
        "sameAs": [FACEBOOK, INSTAGRAM, LINKEDIN, YELP],
    }
    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'


if __name__ == "__main__":
    page(0, "", "Post-Construction &amp; Commercial Cleaning in South Florida | Legally Clean",
         f"Rough, final and punch-list cleans for contractors, plus janitorial and deep cleaning in Broward, Miami-Dade and Palm Beach. Since 2006. Call {PHONE}.",
         "", home, extra_head=jsonld(), body_class="home page")
    page(1, "services/", "Commercial Cleaning Services | Legally Clean",
         "Post-construction cleanup, commercial janitorial, deep cleaning, floors and windows across Broward, Miami-Dade and Palm Beach.", "services/", services)
    page(1, "projects/", "Projects | Legally Clean",
         "Post-construction cleanup for Broward Health, schools and commercial buildouts across South Florida.", "projects/", projects)
    page(1, "about-us/", "About Us | Legally Clean",
         "Woman-owned, MWBE-certified commercial cleaning company founded by Sherry W. Rudolph in 2006.", "about-us/", about)
    page(1, "reviews/", "Reviews | Legally Clean",
         "What contractors and clients say about Legally Clean.", "reviews/", reviews)
    page(1, "contact-us/", f"Contact Us | Legally Clean | {PHONE}",
         f"Call {PHONE}, email or send a message. Offices in Lauderhill, Miami and West Palm Beach. Open {HOURS_TEXT}.", "contact-us/", contact)
    page(1, "quote/", "Request a Quote | Legally Clean",
         "Request a free quote for post-construction cleanup, janitorial or deep cleaning in South Florida.", None, quote, actions=False)
    # 404 uses absolute links because GitHub Pages serves it at any depth
    out = f"""{head(BASE_URL, "Page not found | Legally Clean", "This page could not be found.", "404.html")}
<body class="error404 has-mobile-actions">
<div class="wp-site-blocks">
{header(BASE_URL, None)}
<main class="wp-block-group" id="wp--skip-link--target">{notfound(BASE_URL)}</main>
{footer(BASE_URL)}
</div>
{mobile_actions(BASE_URL)}
</body>
</html>
"""
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(out)
    print("wrote 404.html")
    with open(os.path.join(OUT, "version.json"), "w") as f:
        json.dump({"build": BUILD}, f)
    print("wrote version.json", BUILD)
