#!/usr/bin/env python3
"""Legally Clean pitch prototype generator.

Plain HTML in WordPress core block markup, laid out like a Twenty Twenty-Four site:
Cover hero, Query Loop service cards and single service pages, and the theme's own patterns
(text-feature-grid-3-col, banner-project-description, text-project-details, testimonial-centered,
cta-services-image-left, text-faq, cta-subscribe-centered, footer). Fonts ship with official
WordPress themes: Source Serif 4 (Twenty Twenty-Two) and Libre Franklin (Twenty Seventeen).
Page transitions follow the WordPress Performance team's View Transitions plugin.
Run:  python3 tools/build_site.py <site-dir>. Every fact comes from the client's own channels; see facts.md.
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
FONTS = "https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&amp;display=swap"

OFFICES = [
    {"county": "Broward County", "label": "Main office", "street": "1773 N State Rd 7, Ste 101 I", "city": "Lauderhill, FL 33313",
     "phone": "(561) 467-4400", "tel": "+15614674400",
     "cities": "Fort Lauderdale, Hollywood, Pembroke Pines, Coral Springs, Miramar, Pompano Beach, Davie, Plantation, Sunrise and Weston"},
    {"county": "Miami-Dade County", "label": "Office", "street": "7900 NW 27th Ave, #236", "city": "Miami, FL 33147",
     "phone": "(561) 513-8138", "tel": "+15615138138",
     "cities": "Miami, Miami Lakes, Hialeah, Doral, Kendall, Coral Gables, Miami Gardens and Homestead"},
    {"county": "Palm Beach County", "label": "Office", "street": "401 N Rosemary Ave", "city": "West Palm Beach, FL 33401",
     "phone": "(561) 934-2594", "tel": "+15619342594",
     "cities": "West Palm Beach, Boca Raton, Delray Beach, Boynton Beach, Lake Worth, Wellington, Palm Beach Gardens and Jupiter"},
]

BUILD = time.strftime("%Y%m%d%H%M%S")
# If a browser shows a cached page from an older build, it reloads once to get the current one.
SELF_HEAL = ('<script>(function(){if(!window.fetch)return;fetch("ROOTversion.json",{cache:"no-store"})'
             '.then(function(r){return r.json()}).then(function(v){if(v.build&&v.build!=="BUILD"){var k="reload-"+v.build;'
             'try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1")}catch(e){}location.reload()}}).catch(function(){})})();</script>')

# Port of the WordPress Performance team's View Transitions plugin (plugins/view-transitions/js/view-transitions.js):
# header and main keep their own transition names; a service card's featured image and title morph into the
# single page's featured image and title, and back. Default animation: fade, 400ms. Runs before first render.
VIEW_TRANSITIONS = r"""<script>document.documentElement.classList.add("js");
(function(){if(!window.navigation||!("CSSViewTransitionRule" in window))return;
var cfg={globalTransitionNames:{"header":"header","main":"main"},postTransitionNames:{".wp-block-post-title":"post-title",".wp-post-image":"post-thumbnail"}};
function entries(article){var e=Object.entries(cfg.globalTransitionNames).map(function(p){return[document.body.querySelector(p[0]),p[1]]});
if(article)e=e.concat(Object.entries(cfg.postTransitionNames).map(function(p){return[article.querySelector(p[0]),p[1]]}));return e}
function articleForUrl(url){var links=document.querySelectorAll("main .wp-block-post.post a[href]");for(var i=0;i<links.length;i++){if(links[i].href===url)return links[i].closest(".wp-block-post.post")}return null}
function setNames(list,promise){list.forEach(function(p){if(p[0])p[0].style.viewTransitionName=p[1]});var clear=function(){list.forEach(function(p){if(p[0])p[0].style.viewTransitionName=""})};promise.then(clear,clear)}
function quiet(vt){var n=function(){};vt.ready.catch(n);vt.finished.catch(n)}
function pick(url){var b=document.body.classList;if(b.contains("single"))return entries(document.querySelector("article.post"));if(b.contains("home")||b.contains("archive"))return entries(url?articleForUrl(url):null);return entries(null)}
addEventListener("pageswap",function(e){if(!e.viewTransition)return;quiet(e.viewTransition);setNames(pick(e.activation&&e.activation.entry?e.activation.entry.url:null),e.viewTransition.finished)});
addEventListener("pagereveal",function(e){if(!e.viewTransition)return;quiet(e.viewTransition);var f=navigation.activation&&navigation.activation.from;setNames(pick(f&&f.url),e.viewTransition.ready)});})();</script>"""


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
    # WordPress core navigation icons
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M5 5v1.5h14V5H5zm0 7.8h14v-1.5H5v1.5zM5 19h14v-1.5H5V19z"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="m13.06 12 6.47-6.47-1.06-1.06L12 10.94 5.53 4.47 4.47 5.53 10.94 12l-6.47 6.47 1.06 1.06L12 13.06l6.47 6.47 1.06-1.06L13.06 12Z"/></svg>',
    # WordPress core image block "expand on click" icon
    "expand": '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path fill="#fff" d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z"/></svg>',
}
CUR = ' aria-current="page"'
CHEVRON = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" focusable="false"><path d="M1.50002 4L6.00002 8L10.5 4" stroke-width="1.5"></path></svg>'


def img(root, name, alt, sizes, cls="", eager=False, extra=""):
    widths, w, h = IMGS[name]
    default = widths[1] if len(widths) > 1 else widths[0]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    ss = (' srcset="' + ", ".join(f"{root}assets/img/{name}-{x}.webp {x}w" for x in widths) + f'" sizes="{sizes}"') if len(widths) > 1 else ""
    return f'<img{c} src="{root}assets/img/{name}-{default}.webp"{ss} width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{extra}>'


def figure(root, name, alt, sizes, cls="wp-block-image size-large is-style-rounded", caption="", lightbox=True):
    cap = f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ""
    if not lightbox:
        return f'<figure class="{cls}">{img(root, name, alt, sizes)}{cap}</figure>'
    return (f'<figure class="{cls} wp-lightbox-container">{img(root, name, alt, sizes)}'
            f'<button class="lightbox-trigger" type="button" aria-haspopup="dialog" aria-label="Enlarge: {alt}">{SVG["expand"]}</button>{cap}</figure>')


def button(href, label, style="", icon=None, attrs=""):
    cls = "wp-block-button" + (f" is-style-{style}" if style else "")
    lead = SVG[icon] if icon == "phone" else ""
    return f'<div class="{cls}"><a class="wp-block-button__link wp-element-button" href="{href}"{attrs}>{lead}{label}</a></div>'


def buttons(*items, center=False):
    j = " is-content-justification-center" if center else ""
    return f'<div class="wp-block-buttons is-layout-flex{j}">{"".join(items)}</div>'


def quote_link(root, service=None):
    return f"{root}quote/" + (f"?service={service}" if service else "")


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
<meta name="theme-color" content="#ffffff">
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
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" id="wp-block-library-css" href="{root}assets/css/wp-blocks.css?ver=11.2.0">
<link rel="stylesheet" id="legallyclean-style-css" href="{root}assets/css/site.css?ver={ver('assets/css/site.css')}">
<meta name="site-build" content="{BUILD}">
{VIEW_TRANSITIONS}
{SELF_HEAL.replace("ROOT", root).replace("BUILD", BUILD)}
<script type="speculationrules">{json.dumps(SPECULATION)}</script>
{extra}<script src="{root}assets/js/site.js?ver={ver('assets/js/site.js')}" defer></script>
</head>"""


def href(root, h):
    return (root + h) or "./"


def brand(root):
    home = root or "./"
    return (f'<div class="site-brand"><div class="wp-block-site-logo"><a href="{home}" rel="home" class="custom-logo-link">'
            f'<img src="{root}assets/img/logo.webp" width="183" height="160" alt="{NAME}" class="custom-logo"></a></div>'
            f'<div><p class="wp-block-site-title"><a href="{home}" rel="home">{NAME}</a></p>'
            f'<p class="wp-block-site-tagline">Post-construction &amp; commercial cleaning</p></div></div>')


def mega_menu(root):
    cards = "".join(
        f'<a class="mega-card" href="{root}services/{s["slug"]}/">'
        f'<img src="{root}assets/img/{s["img"]}-{IMGS[s["img"]][0][0]}.webp" width="{IMGS[s["img"]][1]}" height="{IMGS[s["img"]][2]}" alt="" loading="lazy" decoding="async">'
        f'<span class="mega-card__title">{s["name"]}</span><span class="mega-card__text">{s["card"]}</span></a>'
        for s in SERVICES)
    return (f'<div class="mega-menu" id="mega-services"><div class="mega-menu__inner"><div class="mega-menu__grid">{cards}</div>'
            f'<p class="mega-menu__foot"><a href="{root}services/">All services</a></p></div></div>')


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
    sub = "".join(f'<li><a href="{root}services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    overlay = []
    for l, h in NAV:
        extra = f'<ul class="overlay-sub">{sub}</ul>' if h == "services/" else ""
        overlay.append(f'<li><a href="{href(root, h)}"{CUR if active == h else ""}>{l}</a>{extra}</li>')
    phone_svg = SVG["phone"].replace("<svg ", '<svg width="16" height="16" ')
    return f"""<a class="skip-link screen-reader-text" href="#wp--skip-link--target">Skip to content</a>
<header class="wp-block-template-part site-header has-global-padding">
  <div class="site-header__inner">
    {brand(root)}
    <nav class="wp-block-navigation" aria-label="Main"><ul class="wp-block-navigation__container">{"".join(items)}</ul></nav>
    <div class="header-tools">
      <a class="header-phone" href="tel:{TEL}">{phone_svg}{PHONE}</a>
      <a class="icon-button header-call" href="tel:{TEL}" aria-label="Call {PHONE}">{SVG["phone"]}</a>
      <div class="wp-block-button header-quote"><a class="wp-block-button__link wp-element-button" href="{root}quote/">Get a quote</a></div>
      <button class="wp-block-navigation__responsive-container-open icon-button" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="Open menu">{SVG["menu"]}</button>
    </div>
  </div>
  <div class="wp-block-navigation__responsive-container" role="dialog" aria-modal="true" aria-label="Menu">
    <button class="wp-block-navigation__responsive-container-close icon-button" type="button" aria-label="Close menu">{SVG["close"]}</button>
    <ul>{"".join(overlay)}</ul>
    {buttons(button(root + "quote/", "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}
  </div>
</header>"""


def footer(root):
    svc = "".join(f'<li><a href="{root}services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    offices = "".join(f'<li>{o["city"].split(",")[0]}: <a href="tel:{o["tel"]}">{o["phone"]}</a></li>' for o in OFFICES)
    return f"""<footer class="wp-block-template-part site-footer has-global-padding">
  <div class="site-footer__inner">
    <div class="wp-block-columns alignwide is-layout-flex footer-columns">
      <div class="wp-block-column footer-brand">
        {brand(root)}
        <p>We clean corners, so you don't have to.</p>
      </div>
      <div class="wp-block-column"><h2 class="wp-block-heading">Services</h2><ul>{svc}</ul></div>
      <div class="wp-block-column"><h2 class="wp-block-heading">Company</h2><ul>
        <li><a href="{root}projects/">Projects</a></li><li><a href="{root}about-us/">About</a></li><li><a href="{root}reviews/">Reviews</a></li>
        <li><a href="{root}contact-us/">Contact</a></li><li><a href="{root}quote/">Get a quote</a></li></ul></div>
      <div class="wp-block-column"><h2 class="wp-block-heading">Offices</h2><ul>{offices}</ul></div>
      <div class="wp-block-column"><h2 class="wp-block-heading">Contact</h2><ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{HOURS_TEXT}</li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li><li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> Legally Clean Inc. Licensed with the State of Florida, insured and bonded. Certified MWBE.</p>
      <p>Lauderhill, Miami and West Palm Beach</p>
    </div>
  </div>
</footer>"""


def mobile_actions(root):
    return f"""<div class="mobile-actions" role="region" aria-label="Quick actions">
  {button("tel:" + TEL, "Call", "outline", "phone")}
  {button(root + "quote/", "Get a quote")}
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
    {"id": "post-construction", "slug": "post-construction-cleanup", "name": "Post-construction cleanup", "img": "post-construction",
     "alt": "Legally Clean crew member vacuuming new cabinets during a school final clean",
     "card": "Rough, final and punch-list cleans for contractors, from the first debris haul to the owner walkthrough."},
    {"id": "janitorial", "slug": "commercial-janitorial", "name": "Commercial janitorial", "img": "janitorial",
     "alt": "Cleaner wiping down a desk in an office",
     "card": "A regular crew on a set schedule: daily, weekly or custom, worked around your business hours."},
    {"id": "deep-clean", "slug": "commercial-deep-cleaning", "name": "Commercial deep cleaning", "img": "deep-clean",
     "alt": "Stainless steel commercial kitchen",
     "card": "A periodic reset for kitchens, floors, vents and busy areas that the regular crew isn't scoped for."},
    {"id": "floors-windows", "slug": "floors-and-windows", "name": "Floors and windows", "img": "floors-windows",
     "alt": "Legally Clean crew member cleaning window frames along a glass wall",
     "card": "Strip and wax, construction haze off tile and concrete, and windows up to the upper floors."},
]

DETAIL = {
    "post-construction": {
        "lede": "Rough, final and punch-list cleans for general contractors, developers and property managers across Broward, Miami-Dade and Palm Beach.",
        "body": ["We handle the whole cleanup, from the first debris haul to the last touch-up before the owner walks the space. We coordinate with your site supervisor so cleaning never holds up closeout.",
                 "Each phase can be booked on its own, but most commercial jobs need all three. Skipping the punch-list clean is how fingerprints and resettled dust end up on an inspection report.",
                 "On a mid-size commercial build, a rough clean usually takes one to two days. All three phases usually run three to five days. Every quote comes with a timeline."],
        "lists": [("What's included", ["Rough clean during construction", "Final clean before handoff", "Punch-list and touch-up clean", "Floor cleaning, strip and wax", "Interior and exterior windows", "Pressure washing"]),
                  ("Projects", ["Retail and office buildouts", "Restaurant buildouts and renovations", "Warehouses and industrial", "New construction", "Remodels and renovations", "Demolition cleanup and debris removal"])]},
    "janitorial": {
        "lede": "Scheduled cleaning for offices, banks, schools, clinics and common areas, worked around your business hours.",
        "body": ["A regular crew that cleans your building the same way every visit. Daily, weekly, every other week, or a custom schedule.",
                 "Our crews are trained on the OSHA HazCom standard. They read Safety Data Sheets, know GHS chemical labels and track dilution, which matters in schools, clinics and banks."],
        "lists": [("Every visit", ["Trash out and fresh liners", "Floors swept, mopped and vacuumed", "Restrooms cleaned and restocked", "Break rooms and common areas", "Dusting and polishing", "Door handles, switches and shared equipment disinfected"]),
                  ("Buildings", ["Offices, law and real estate offices", "Banks", "Retail", "Clinics and medical facilities", "Schools", "Country clubs, gyms and condo common areas"])]},
    "deep-clean": {
        "lede": "A periodic reset for restaurants, offices, retail and bank branches, beyond what the regular crew is scoped for.",
        "body": ["Most janitorial contracts are scoped for upkeep. A deep clean is the reset: the grime in grout, the kitchen grease, the vents and baseboards a regular crew doesn't get to.",
                 "Book it quarterly, before an inspection, after a renovation, at lease turnover or before a reopening."],
        "lists": [("What's included", ["Floor cleaning and treatment (tile, VCT, grout)", "Kitchen and back-of-house degreasing", "Lobbies, teller stations and waiting areas", "Fixtures, glass, baseboards and vents", "Restrooms, break rooms and shared spaces"]),
                  ("Good for", ["Restaurants", "Offices", "Banks and financial branches", "Retail spaces"])]},
    "floors-windows": {
        "lede": "Floor stripping and waxing, construction haze removal, window cleaning up to the upper floors, and pressure washing.",
        "body": ["Construction leaves adhesive, paint and grout haze on tile, hardwood, laminate, concrete and VCT. We deep clean and strip it, then wax it for a new-floor shine. A typical 3,000 to 5,000 sq ft office floor takes about one working day.",
                 "Windows get cleaned inside and out, including exterior glass on the second story and up, with tracks and sills detailed. Outside, we pressure wash sidewalks, parking areas, dumpster pads and building exteriors."],
        "lists": [("Floors", ["Tile and grout", "VCT", "Concrete", "Hardwood and laminate", "Strip and wax"]),
                  ("Glass and outside", ["Exterior windows, 2nd story and up", "Tracks and sills", "Sidewalks and parking areas", "Dumpster pads", "Building exteriors"])]},
}

SERVICE_OPTIONS = [("post-construction", "Post-construction"), ("janitorial", "Janitorial"), ("deep-clean", "Deep cleaning"),
                   ("floors-windows", "Floors and windows"), ("pressure-washing", "Pressure washing"), ("something-else", "Something else")]
SERVICE_ICON = {
    "post-construction": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/>',
    "janitorial": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "deep-clean": '<path d="M9.94 14.06 4 20"/><path d="m14 4 1.1 2.9L18 8l-2.9 1.1L14 12l-1.1-2.9L10 8l2.9-1.1z"/><path d="M5 3v4M3 5h4M19 15v4M17 17h4"/>',
    "floors-windows": '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/>',
    "pressure-washing": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
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

CLIENT_LOGOS = [("kaufman-lynn", "Kaufman Lynn Construction", 108, 96), ("suffolk", "Suffolk", 517, 96), ("coastal", "Coastal Construction", 151, 96),
                ("d-stephenson", "D. Stephenson Construction", 559, 96), ("lunacon", "Lunacon", 246, 96), ("broward-health", "Broward Health", 588, 96)]

JOB_PHOTOS = [
    ("job-cabinets", "Legally Clean crew member wiping down new casework in a school lab", "Final clean, school lab"),
    ("job-hallway", "Crew in hard hats and safety vests cleaning a new corridor", "Corridor final clean"),
    ("job-atrium", "Atrium on an active job site with lifts and materials", "Rough clean while trades work"),
]

PHASES = [
    ("Rough clean", "While trades are still working: debris removal, bulk trash haul-off, sweeping and first dust control, so the crews on site can work safely."),
    ("Final clean", "After the last trade is done: floors, walls, baseboards, cabinets, countertops, fixtures and windows brought up to move-in standard."),
    ("Punch-list clean", "Right before the walkthrough: paint overspray, adhesive residue, fingerprints and dust that settles again after the final trades wrap."),
]

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

CREDS = [
    ("In business", "Since 2006, founded by Sherry W. Rudolph"),
    ("Licensing", "Licensed with the State of Florida. Broward County business license."),
    ("Insurance", "Fully insured and bonded"),
    ("Ownership", "Woman-owned. Certified Minority/Women Business Enterprise (MWBE)."),
    ("Vendor certifications", "Broward County, Miami-Dade County, Broward County Public Schools and Miami-Dade County Schools"),
    ("Safety training", "OSHA 10 and OSHA 30 trained crews. HazCom trained."),
    ("Recognition", "US Department of Commerce Firm of the Year recipient"),
]


# ---------- shared blocks ----------

def gfield(label, inner, required=False, width="", stack=True, desc="", group=False, cls=""):
    req = '<span class="gfield_required" aria-hidden="true">*</span>' if required else ""
    w = (f" gfield--width-{width}" + (" stack-sm" if stack else "")) if width else ""
    grp = " data-group-required" if group and required else ""
    d = f'<div class="gfield_description">{desc}</div>' if desc else ""
    if group:
        return (f'<fieldset class="gfield{w} {cls}"{grp}><legend class="gfield_label">{label}{req}</legend>'
                f'{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></fieldset>')
    return f'<div class="gfield{w} {cls}">{label.format(req=req)}{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></div>'


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
    return f'<ul class="gchoice-cards{" gchoice-cards--lg" if large else ""}">{"".join(items)}</ul>'


def radios(name, values, input_type="radio"):
    kind = "checkbox" if input_type == "checkbox" else "radio"
    return (f'<ul class="gfield_{kind} inline">' + "".join(
        f'<li><label class="gchoice"><input type="{input_type}" name="{name}" value="{v}"> {v}</label></li>' for v in values) + "</ul>")


HOURS = [("Monday", "8am to 6pm"), ("Tuesday", "8am to 6pm"), ("Wednesday", "8am to 6pm"), ("Thursday", "8am to 6pm"),
         ("Friday", "8am to 6pm"), ("Saturday", "8am to 6pm"), ("Sunday", "Closed")]


def hours_table():
    rows = "".join(f'<tr data-day="{d}"><td>{d}</td><td>{h}</td></tr>' for d, h in HOURS)
    return f'<table class="hours-table"><caption class="screen-reader-text">Opening hours</caption>{rows}</table>'


def status():
    return f'<p class="hours-status" data-hours-status><span class="status-dot"></span><span data-hours-text>{HOURS_TEXT}</span></p>'


def page_title(root, crumbs, title, lede):
    trail = " / ".join(f'<a href="{h}">{t}</a>' if h else t for t, h in crumbs)
    return f"""<section class="wp-block-group alignfull page-title has-global-padding">
  <div class="wide">
    <nav class="breadcrumbs has-small-font-size" aria-label="Breadcrumb"><a href="{root or './'}">Home</a> / {trail}</nav>
    <h1 class="wp-block-heading">{title}</h1>
    <p class="page-title__lede">{lede}</p>
  </div>
</section>"""


def section_head(title, text="", hid=""):
    i = f' id="{hid}"' if hid else ""
    p = f"<p>{text}</p>" if text else ""
    return f'<div class="section-head wp-reveal"><h2 class="wp-block-heading"{i}>{title}</h2>{p}</div>'


def query_loop(root, items=None, columns=4, heading_level=3):
    """Query Loop block: wp-block-post-template with wp-block-post items, as WordPress renders it."""
    posts = []
    for s in items or SERVICES:
        url = f"{root}services/{s['slug']}/"
        posts.append(f"""<li class="wp-block-post post type-page">
  <figure class="wp-block-post-featured-image"><a href="{url}" aria-hidden="true" tabindex="-1">{img(root, s["img"], s["alt"], "(min-width: 900px) 25vw, 50vw", cls="wp-post-image")}</a></figure>
  <h{heading_level} class="wp-block-post-title"><a href="{url}">{s["name"]}</a></h{heading_level}>
  <div class="wp-block-post-excerpt"><p class="wp-block-post-excerpt__excerpt">{s["card"]}</p><p class="wp-block-post-excerpt__more-text"><a class="wp-block-post-excerpt__more-link" href="{url}">Read more<span class="screen-reader-text"> about {s["name"]}</span></a></p></div>
</li>""")
    return f'<ul class="wp-block-post-template is-layout-grid columns-{columns} wp-reveal">{"".join(posts)}</ul>'


def client_logos(root):
    logos = "".join(f'<li><img src="{root}assets/img/clients/{k}.webp" width="{w}" height="{h}" alt="{n}" loading="lazy" decoding="async"></li>' for k, n, w, h in CLIENT_LOGOS)
    return f"""<section class="wp-block-group alignfull client-logos has-global-padding" aria-labelledby="clients-title">
  <div class="wide wp-reveal">
    <p class="client-logos__label has-small-font-size" id="clients-title">General contractors and facilities we've worked with</p>
    <ul>{logos}</ul>
    <p class="client-logos__more has-small-font-size">Also Balfour Beatty, Skanska USA and Pirtle Construction.</p>
  </div>
</section>"""


def process_section(root, bg=" has-base-2-background-color"):
    """Twenty Twenty-Four "text-feature-grid-3-col"."""
    cols = "".join(f'<div class="wp-block-column"><h3 class="wp-block-heading is-style-asterisk has-body-font-family has-medium-font-size">{t}</h3><p>{d}</p></div>' for t, d in PHASES)
    return f"""<section class="wp-block-group alignfull section has-global-padding{bg}" aria-labelledby="process-title">
  <div class="wp-reveal">
    <div class="feature-grid-head">
      <h2 class="wp-block-heading has-text-align-center is-style-asterisk" id="process-title">How post-construction cleanup works</h2>
      <p class="has-text-align-center">Construction cleanup isn't one pass with a broom. We phase it around your schedule so the space is ready when the owner walks it.</p>
    </div>
    <div class="wp-block-columns alignwide wide is-layout-flex feature-grid">{cols}</div>
    <p class="has-text-align-center feature-grid-note has-small-font-size">Add to any phase: floor stripping and waxing, windows on the second story and up, pressure washing, and HEPA vacuums for fine dust.</p>
  </div>
</section>"""


def project_banner(root, link=True):
    """Twenty Twenty-Four "banner-project-description" followed by "text-project-details"."""
    more = f'<p class="project-banner__more"><a href="{root}projects/">See more projects</a></p>' if link else ""
    return f"""<section class="wp-block-group alignfull section project-banner has-accent-background-color has-global-padding" aria-labelledby="bh-title">
  <div class="wide wp-reveal">
    <div class="wp-block-columns alignwide is-layout-flex">
      <div class="wp-block-column" style="flex-basis:40%"><h2 class="wp-block-heading has-body-font-family has-medium-font-size project-banner__label" id="bh-title">Broward Health Emergency Room, Sunrise</h2></div>
      <div class="wp-block-column" style="flex-basis:60%"><p class="has-heading-font-family has-x-large-font-size project-banner__statement">We handled the post-construction cleanup for Broward Health&rsquo;s brand new Emergency Room in Sunrise. From framing dust to opening day ready.</p>{more}</div>
    </div>
    {figure(root, "broward-health-er", "The new Broward Health Emergency Room in Sunrise, Florida", "(min-width: 1280px) 1280px, 100vw", "wp-block-image alignwide size-large is-style-rounded project-banner__image")}
    <dl class="project-facts">
      <div><dt>Client</dt><dd>Broward Health</dd></div>
      <div><dt>Location</dt><dd>Sunrise, Florida</dd></div>
      <div><dt>Scope</dt><dd>Post-construction cleanup</dd></div>
      <div><dt>Completed</dt><dd>2026</dd></div>
    </dl>
  </div>
</section>"""


def creds_section(root, bg=""):
    rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in CREDS)
    return f"""<section class="wp-block-group alignfull section has-global-padding{bg}" aria-labelledby="creds-title">
  <div class="wp-block-columns alignwide wide is-layout-flex creds wp-reveal">
    <div class="wp-block-column" style="flex-basis:40%">
      <h2 class="wp-block-heading" id="creds-title">Licensed, insured and certified</h2>
      <p>Contractors and property managers need a licensed, insured vendor on file before anyone sets foot on site. Ask, and we'll send our documents with your quote.</p>
      <p>Our MWBE certification is recognized by government and commercial procurement offices for supplier diversity programs.</p>
      {buttons(button(root + "contact-us/?topic=credentials", "Request our credentials", "outline"))}
    </div>
    <div class="wp-block-column" style="flex-basis:60%">
      <figure class="wp-block-table is-style-stripes"><table class="has-fixed-layout"><tbody>{rows}</tbody></table></figure>
    </div>
  </div>
</section>"""


def testimonial(root, key="scott", link=True):
    """Twenty Twenty-Four "testimonial-centered"."""
    name, text = REVIEWS[key]
    more = f'<p class="has-text-align-center testimonial__more"><a href="{root}reviews/">Read more reviews</a></p>' if link else ""
    return f"""<section class="wp-block-group alignfull section testimonial has-contrast-background-color has-global-padding" aria-label="Customer review">
  <div class="testimonial__inner wp-reveal">
    <p class="has-text-align-center has-heading-font-family testimonial__quote">&ldquo;{text}&rdquo;</p>
    <p class="has-text-align-center testimonial__name">{name}</p>
    <p class="has-text-align-center has-small-font-size testimonial__role">Legally Clean customer</p>
    {more}
  </div>
</section>"""


def owner_section(root):
    """Twenty Twenty-Four "cta-services-image-left"."""
    return f"""<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="owner-title">
  <div class="wp-block-columns alignwide wide is-layout-flex owner wp-reveal">
    <div class="wp-block-column" style="flex-basis:40%">{figure(root, "sherry", "Sherry W. Rudolph, founder and President of Legally Clean", "(min-width: 782px) 40vw, 100vw")}</div>
    <div class="wp-block-column" style="flex-basis:60%">
      <h2 class="wp-block-heading" id="owner-title">Owner-run since 2006</h2>
      <p>Sherry Rudolph founded Legally Clean in 2006, and contractors know her as the Pink Construction Hat Diva. She still shows up on the job. Clients mention it in their reviews: the owner on site, working next to her crew.</p>
      <p>The company hires with a purpose, too. Sherry spent more than 20 years as an employment specialist, and Legally Clean creates jobs for people who face real barriers to employment.</p>
      {buttons(button(root + "about-us/", "About us", "outline"))}
    </div>
  </div>
</section>"""


def gallery(root, photos=JOB_PHOTOS):
    figs = "".join(figure(root, n, alt, "(min-width: 782px) 33vw, 100vw", "wp-block-image size-large", cap) for n, alt, cap in photos)
    return f'<div class="wp-block-gallery has-nested-images columns-{len(photos)} is-cropped wp-reveal">{figs}</div>'


def gallery_section(root):
    return f"""<section class="wp-block-group alignfull section has-global-padding" style="padding-top:0" aria-labelledby="gallery-title">
  <div class="wide">
    {section_head("On the job", "Photos from our crews on South Florida job sites.", "gallery-title")}
    {gallery(root)}
  </div>
</section>"""


def offices_section(root, title="Offices in three counties"):
    cols = []
    for o in OFFICES:
        maps = "https://www.google.com/maps/search/?api=1&amp;query=" + quote_plus(o["street"] + ", " + o["city"])
        cols.append(f"""<div class="wp-block-column office">
  <h3 class="wp-block-heading">{o["county"]}</h3>
  <p class="office__label has-small-font-size">{o["label"]}</p>
  <p>{o["street"]}<br>{o["city"]}<br><a href="tel:{o["tel"]}">{o["phone"]}</a></p>
  <p class="has-small-font-size office__cities">{o["cities"]}, and the rest of the county.</p>
  <p class="has-small-font-size"><a href="{maps}" target="_blank" rel="noopener">Get directions</a></p>
</div>""")
    return f"""<section class="wp-block-group alignfull section has-base-2-background-color has-global-padding" aria-labelledby="offices-title">
  <div class="wide">
    {section_head(title, f"Crews cover all of Broward, Miami-Dade and Palm Beach. Open {HOURS_TEXT}.", "offices-title")}
    <div class="wp-block-columns alignwide is-layout-flex wp-reveal">{"".join(cols)}</div>
  </div>
</section>"""


def faq_section(root, faqs=FAQS):
    """Twenty Twenty-Four "text-faq": questions between wide separators, on the contrast color."""
    sep = '<hr class="wp-block-separator has-alpha-channel-opacity is-style-wide">'
    items = "".join(f'{sep}<details class="wp-block-details"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return f"""<section class="wp-block-group alignfull section faq has-contrast-background-color has-global-padding" aria-labelledby="faq-title">
  <div class="wide wp-reveal">
    <h2 class="wp-block-heading" id="faq-title">Frequently asked questions</h2>
    <div class="faq__list">{items}{sep}</div>
  </div>
</section>"""


def cta(root, title="Tell us about the job", text="Send the scope, the address and your dates. We'll come back with a timeline and a free quote.", btns=None):
    """Twenty Twenty-Four "cta-subscribe-centered"."""
    b = btns or buttons(button(root + "quote/", "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"), center=True)
    return f"""<section class="wp-block-group alignfull section has-accent-background-color has-global-padding">
  <div class="cta-centered wp-reveal">
    <h2 class="wp-block-heading has-text-align-center">{title}</h2>
    <p class="has-text-align-center">{text}</p>
    {b}
  </div>
</section>"""


# ---------- Home ----------

def home(root):
    return f"""
<div class="wp-block-cover alignfull hero-cover">
  {img(root, "hero", "", "100vw", cls="wp-block-cover__image-background", eager=True, extra=' data-object-fit="cover"')}
  <span aria-hidden="true" class="wp-block-cover__background has-background-dim-70 has-background-dim"></span>
  <div class="wp-block-cover__inner-container">
    <div class="wp-block-columns alignwide is-layout-flex">
      <div class="wp-block-column hero-text">
        <h1 class="wp-block-heading">Post-construction and commercial cleaning in South Florida</h1>
        <p class="hero-lede">Rough, final and punch-list cleans for general contractors, and janitorial and deep cleaning for the buildings once they open. Serving Broward, Miami-Dade and Palm Beach since 2006.</p>
        <div data-hero-cta>{buttons(button(root + "quote/", "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}</div>
        <p class="hero-meta">Woman-owned and MWBE certified. Licensed, insured and bonded. Most projects start within 24 hours.</p>
      </div>
      <div class="wp-block-column hero-form-col">
        <div class="quote-box">
          <h2 class="wp-block-heading">Request a free quote</h2>
          <p class="quote-box__sub">We'll get back to you {HOURS_TEXT}.</p>
          <div class="gform_wrapper">
            <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
            <form method="post" novalidate>
              <div class="gform_fields">
                {gfield(lab("h-name", "Name"), '<input id="h-name" name="name" type="text" autocomplete="name" required>', True, "half")}
                {gfield(lab("h-company", "Company"), '<input id="h-company" name="company" type="text" autocomplete="organization">', False, "half")}
                {gfield(lab("h-phone", "Phone"), '<input id="h-phone" name="phone" type="tel" autocomplete="tel" required>', True, "half", stack=False)}
                {gfield(lab("h-zip", "Project ZIP code"), '<input id="h-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, "half", stack=False)}
                {gfield("Service", service_choice_cards("radio", options=SERVICE_OPTIONS[:4]), True, group=True)}
              </div>
              <div class="gform_footer"><button class="wp-element-button" type="submit">Request my quote</button></div>
            </form>
            <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! We got your request.</h3><p>We'll be in touch during business hours. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

{client_logos(root)}

<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--40)" aria-labelledby="services-title">
  <div class="wide">
    {section_head("Our services", "One company for the build and everything after it: the post-construction clean first, then the regular janitorial program once the doors open.", "services-title")}
    {query_loop(root)}
  </div>
</section>

{process_section(root)}
{project_banner(root)}
{creds_section(root)}
{testimonial(root)}
{owner_section(root)}
{gallery_section(root)}
{offices_section(root)}
{faq_section(root)}
{cta(root)}
"""


# ---------- Services ----------

BUILDINGS = ["Offices", "Banks", "Retail", "Restaurants", "Schools", "Clinics and healthcare", "Warehouses", "Country clubs", "Condo common areas", "Gyms and rec centers"]


def services(root):
    blds = "".join(f"<li>{b}</li>" for b in BUILDINGS)
    return f"""
{page_title(root, [("Services", "")], "Services", "Post-construction cleanup for contractors, then janitorial, deep cleaning and floor care for the buildings once they open.")}
<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--40)" aria-label="Services">
  <div class="wide">{query_loop(root, columns=2, heading_level=2)}</div>
</section>
{process_section(root)}
<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="buildings-title">
  <div class="wide">
    {section_head("Buildings we clean", "Commercial and institutional spaces of all sizes, from a single office suite to multi-floor buildings and bank branch networks.", "buildings-title")}
    <ul class="wp-block-list buildings wp-reveal">{blds}</ul>
  </div>
</section>
{cta(root)}
"""


def service_single(s):
    d = DETAIL[s["id"]]

    def render(root):
        lists = "".join(f'<div class="service-list"><h2 class="wp-block-heading has-body-font-family has-medium-font-size">{t}</h2><ul class="wp-block-list">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for t, items in d["lists"])
        others = [o for o in SERVICES if o["id"] != s["id"]]
        return f"""
<article class="wp-block-post post type-page">
  <section class="wp-block-group alignfull section single-hero has-global-padding">
    <div class="wp-block-columns alignwide wide is-layout-flex">
      <div class="wp-block-column" style="flex-basis:55%">
        <nav class="breadcrumbs has-small-font-size" aria-label="Breadcrumb"><a href="{root}">Home</a> / <a href="{root}services/">Services</a> / {s["name"]}</nav>
        <h1 class="wp-block-post-title">{s["name"]}</h1>
        <p class="single-hero__lede">{d["lede"]}</p>
        {buttons(button(quote_link(root, s["id"]), "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}
      </div>
      <div class="wp-block-column" style="flex-basis:45%">
        <figure class="wp-block-post-featured-image">{img(root, s["img"], s["alt"], "(min-width: 782px) 45vw, 100vw", cls="wp-post-image", eager=True)}</figure>
      </div>
    </div>
  </section>
  <section class="wp-block-group alignfull section has-base-2-background-color has-global-padding">
    <div class="wp-block-columns alignwide wide is-layout-flex single-body">
      <div class="wp-block-column entry-content" style="flex-basis:58%">{"".join(f"<p>{p}</p>" for p in d["body"])}</div>
      <div class="wp-block-column" style="flex-basis:42%">{lists}</div>
    </div>
  </section>
</article>
<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="more-title">
  <div class="wide">
    {section_head("More services", "", "more-title")}
    {query_loop(root, others, columns=3)}
  </div>
</section>
{cta(root)}
"""
    return render


# ---------- Projects ----------

PROJECT_TYPES = ["Retail buildouts and renovations", "Commercial and office buildouts", "Restaurant buildouts and renovations",
                 "Industrial and warehouse construction", "New construction", "Home remodels and renovations", "Demolition cleanup and debris removal"]


def projects(root):
    types = "".join(f"<li>{t}</li>" for t in PROJECT_TYPES)

    def item(title, text, photos):
        figs = "".join(figure(root, n, alt, "(min-width: 782px) 30vw, 50vw") for n, alt in photos)
        single = " is-single" if len(photos) == 1 else ""
        return f"""<div class="wp-block-columns alignwide is-layout-flex project-item wp-reveal">
  <div class="wp-block-column" style="flex-basis:40%"><h2 class="wp-block-heading">{title}</h2><p>{text}</p></div>
  <div class="wp-block-column project-item__media{single}" style="flex-basis:60%">{figs}</div>
</div>"""

    return f"""
{page_title(root, [("Projects", "")], "Projects", "Healthcare, schools and commercial buildouts across South Florida, photographed by our crews.")}
{project_banner(root, link=False)}
<section class="wp-block-group alignfull section has-global-padding" aria-label="More projects">
  <div class="wide project-list">
    {item("School buildout, final clean", "Final clean on a new school building. New lab casework, countertops and floors brought up to move-in standard, with backpack vacuums pulling construction dust out of cabinets and drawers.", [("job-cabinets", "Crew member wiping down new casework in a school lab"), ("post-construction", "Crew member with a backpack vacuum cleaning new cabinets")])}
    {item("Rough and final cleans on large builds", "A rough clean around lifts and materials while trades are still working, then the corridor-by-corridor final clean once they're gone. Crews work in hard hats and high-visibility vests on active sites.", [("job-atrium", "Atrium on an active job site with lifts and materials"), ("job-hallway", "Crew in hard hats and safety vests cleaning a new corridor")])}
    {item("Window and frame detailing", "Glass walls collect paint overspray, sticker residue and dust in the tracks. We detail frames, tracks and sills, and clean exterior glass on the second story and up.", [("floors-windows", "Crew member cleaning window frames along a glass wall")])}
  </div>
</section>
<section class="wp-block-group alignfull section has-base-2-background-color has-global-padding" aria-labelledby="types-title">
  <div class="wide">
    {section_head("Projects we clean after", "If it was built, gutted or remodeled, we can clean it for handover.", "types-title")}
    <ul class="wp-block-list buildings wp-reveal">{types}</ul>
  </div>
</section>
{client_logos(root)}
{cta(root, "Have a project closing out?", "Send the address, the square footage and your walkthrough date. We'll send a timeline and a free quote.")}
"""


# ---------- About ----------

MEMBERSHIPS = ["NABWIC", "Lauderhill Regional Chamber of Commerce", "District 9 Broward Advisory Board", "Lauderhill Business Incubator", "Board member, MODCO"]
WHO = ["General contractors", "Property managers", "Developers", "Restaurant owners", "Office managers", "Bank branch managers", "Retail developers", "Schools and government", "Healthcare facilities"]


def about(root):
    return f"""
{page_title(root, [("About", "")], "About Legally Clean", "A woman-owned commercial cleaning company, founded by Sherry W. Rudolph in 2006 and based in Lauderhill.")}
<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--40)" aria-labelledby="story-title">
  <div class="wp-block-columns alignwide wide is-layout-flex owner wp-reveal">
    <div class="wp-block-column" style="flex-basis:40%">{figure(root, "sherry", "Sherry W. Rudolph, founder and President of Legally Clean", "(min-width: 782px) 40vw, 100vw")}</div>
    <div class="wp-block-column entry-content" style="flex-basis:60%">
      <h2 class="wp-block-heading" id="story-title">Twenty years of job sites</h2>
      <p>Sherry Rudolph started Legally Clean in 2006. In 2026 the company turns 20, with offices in Lauderhill, Miami and West Palm Beach and crews working with construction firms, government entities and healthcare facilities across the tri-county area.</p>
      <p>People in the industry call her the Pink Construction Hat Diva. She built the business on relationships and deadlines. Every construction job ends with a walkthrough date, and her systems are set up around hitting it.</p>
      <p>That track record earned her recognition as a US Department of Commerce Firm of the Year recipient.</p>
    </div>
  </div>
</section>
<section class="wp-block-group alignfull section has-contrast-background-color has-global-padding" aria-label="How we hire">
  <div class="statement wp-reveal">
    <p class="has-text-align-center has-heading-font-family has-x-large-font-size">We hire with a mission: real jobs for people who face real barriers to employment.</p>
    <p class="has-text-align-center statement__note">It comes from Sherry's 20-plus years as an employment specialist and her Bachelor of Social Work from Saginaw Valley State University.</p>
  </div>
</section>
{creds_section(root)}
<section class="wp-block-group alignfull section has-base-2-background-color has-global-padding">
  <div class="wp-block-columns alignwide wide is-layout-flex wp-reveal">
    <div class="wp-block-column"><h2 class="wp-block-heading">Who we work with</h2><ul class="wp-block-list buildings buildings--2">{"".join(f"<li>{w}</li>" for w in WHO)}</ul></div>
    <div class="wp-block-column"><h2 class="wp-block-heading">Memberships</h2><ul class="wp-block-list buildings buildings--1">{"".join(f"<li>{m}</li>" for m in MEMBERSHIPS)}</ul></div>
  </div>
</section>
{client_logos(root)}
{cta(root)}
"""


# ---------- Reviews ----------

def reviews(root):
    cards = "".join(f'<figure class="wp-block-quote review-card"><blockquote><p>&ldquo;{REVIEWS[k][1]}&rdquo;</p></blockquote><figcaption><cite>{REVIEWS[k][0]}</cite></figcaption></figure>'
                    for k in ["perry", "paul", "gyovanni", "colton"])
    review_btns = buttons(button(GOOGLE, "Review us on Google", "", None, ' target="_blank" rel="noopener"'),
                          button(YELP, "Yelp", "outline", None, ' target="_blank" rel="noopener"'),
                          button(FACEBOOK, "Facebook", "outline", None, ' target="_blank" rel="noopener"'), center=True)
    return f"""
{page_title(root, [("Reviews", "")], "Reviews", "What contractors, business owners and clients say about Sherry and her crews.")}
{testimonial(root, link=False)}
<section class="wp-block-group alignfull section has-global-padding" aria-label="More reviews">
  <div class="review-grid wide wp-reveal">{cards}</div>
</section>
{cta(root, "Worked with us recently?", "A short review helps other contractors and property managers find us.", review_btns)}
"""


# ---------- Contact ----------

def contact(root):
    offices = "".join(f'<div class="contact-line"><h3 class="wp-block-heading">{o["county"]}</h3><p>{o["street"]}, {o["city"]}<br><a href="tel:{o["tel"]}">{o["phone"]}</a></p></div>' for o in OFFICES)
    topics = radios("topic", ["A quote", "Credentials or vendor paperwork", "A current job", "Something else"])
    return f"""
{page_title(root, [("Contact", "")], "Contact us", f"Call the main line, email Sherry, or send the form. Open {HOURS_TEXT}.")}
<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--40)">
  <div class="contact-layout wide">
    <div class="contact-main">
      <div class="contact-line"><h3 class="wp-block-heading">Main line</h3><p><a class="contact-big" href="tel:{TEL}">{PHONE}</a></p></div>
      <div class="contact-line"><h3 class="wp-block-heading">Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="contact-line"><h3 class="wp-block-heading">Hours</h3>{status()}{hours_table()}</div>
      {offices}
      <div class="contact-line"><h3 class="wp-block-heading">Payment</h3><p>Visa, MasterCard, PayPal, Venmo and Zelle</p></div>
    </div>
    <div class="form-panel">
      <div class="gform_wrapper">
        <div class="gform_heading"><h2 class="gform_title">Send us a message</h2><span class="gform_description">Want a price? The <a href="{root}quote/">quote form</a> asks the right questions.</span></div>
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
"""


# ---------- Quote ----------

def quote(root):
    prev_btn = '<button class="wp-element-button gform_previous_button" type="button">Previous</button>'
    nxt = '<button class="wp-element-button gform_next_button" type="button">Next</button>'
    sub = '<button class="wp-element-button" type="submit">Send request</button>'

    def nav(prev, btn):
        return f'<div class="gform_page_footer">{prev_btn if prev else ""}{btn}</div>'

    paul_name, paul_text = REVIEWS["paul"]
    lede = f'Three short steps. Rather talk it through? Call <a href="tel:{TEL}">{PHONE}</a>.'
    return f"""
{page_title(root, [("Get a quote", "")], "Request a quote", lede)}
<section class="wp-block-group alignfull section has-global-padding" style="padding-top:var(--wp--preset--spacing--40)">
  <div class="quote-layout wide">
    <div class="form-panel">
      <div class="gform_wrapper">
        <div class="gf_progressbar_wrapper"><p class="gf_progressbar_title">Step 1 of 3 - Services</p><div class="gf_progressbar" aria-hidden="true"><div class="gf_progressbar_percentage" style="width:33%"><span>33%</span></div></div></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_page" data-title="Services">
            <div class="gform_fields">
              {gfield("What do you need?", service_choice_cards("checkbox", large=True), True, group=True, desc="Pick all that apply.")}
              {gfield("Which phases?", radios("phases", ["Rough clean", "Final clean", "Punch-list clean", "Not sure yet"], "checkbox"), False, group=True, desc="Not sure? We'll walk the site and tell you.", cls="js-phases")}
            </div>
            {nav(False, nxt)}
          </div>
          <div class="gform_page" data-title="The site" hidden>
            <div class="gform_fields">
              {gfield("Type of building", radios("building", ["Office", "Retail", "Restaurant", "School", "Healthcare", "Bank", "Warehouse", "Multifamily or condo", "Other"]), True, group=True)}
              {gfield(lab("q-size", "Approximate size (sq ft)"), '<input id="q-size" name="size" type="text" inputmode="numeric">', False, "half")}
              {gfield(lab("q-zip", "Project ZIP code"), '<input id="q-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, "half")}
              {gfield(lab("q-date", "Start or walkthrough date"), '<input id="q-date" name="date" type="date">', False, "half")}
              {gfield(lab("q-files", "Plans or scope (optional)"), '<input id="q-files" name="files" type="file" multiple accept=".pdf,image/*">', False, "half")}
              {gfield(lab("q-details", "Anything else we should know?"), '<textarea id="q-details" name="details" rows="4"></textarea>')}
            </div>
            {nav(True, nxt)}
          </div>
          <div class="gform_page" data-title="Your details" hidden>
            <div class="gform_fields">
              {gfield(lab("q-name", "Name"), '<input id="q-name" name="name" type="text" autocomplete="name" required>', True, "half")}
              {gfield(lab("q-company", "Company"), '<input id="q-company" name="company" type="text" autocomplete="organization">', False, "half")}
              {gfield("Your role", radios("role", ["General contractor", "Property or facility manager", "Business owner", "Other"]), False, group=True)}
              {gfield(lab("q-phone", "Phone"), '<input id="q-phone" name="phone" type="tel" autocomplete="tel" required>', True, "half")}
              {gfield(lab("q-email", "Email"), '<input id="q-email" name="email" type="email" autocomplete="email" required>', True, "half")}
              {gfield("Best way to reach you", radios("contact_pref", ["Phone call", "Email"]), False, group=True)}
              {gfield("Vendor paperwork", '<label class="gchoice"><input type="checkbox" name="credentials" value="yes"> Send your license, insurance and certification documents with the quote</label>', False, group=True)}
            </div>
            {nav(True, sub)}
          </div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! Your request is in.</h3><p>We'll get back to you during business hours with next steps and a timeline. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
    <aside class="widget-area" aria-label="Sidebar">
      <section class="widget">
        <h2 class="widget-title">Rather talk?</h2>
        <p class="widget-phone"><a href="tel:{TEL}">{PHONE}</a></p>
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
        <p>&ldquo;{paul_text.strip()}&rdquo;</p>
        <p class="has-small-font-size">{paul_name}</p>
      </section>
    </aside>
  </div>
</section>
"""


def notfound(root):
    return f"""
<section class="wp-block-group alignfull section notfound has-global-padding">
  <h1 class="wp-block-heading has-text-align-center">Page not found</h1>
  <p class="has-text-align-center">This page got swept up with the debris. Try the homepage or give us a call.</p>
  {buttons(button(root, "Go to the homepage"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}
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
    preload = ('<link rel="preload" as="image" href="assets/img/hero-1280.webp" '
               'imagesrcset="assets/img/hero-800.webp 800w, assets/img/hero-1280.webp 1280w, assets/img/hero-1920.webp 1920w" imagesizes="100vw" fetchpriority="high">\n')
    page(0, "", "Post-Construction &amp; Commercial Cleaning in South Florida | Legally Clean",
         f"Rough, final and punch-list cleans for contractors, plus janitorial and deep cleaning in Broward, Miami-Dade and Palm Beach. Since 2006. Call {PHONE}.",
         "", home, extra_head=preload + jsonld(), body_class="home page")
    page(1, "services/", "Services | Legally Clean",
         "Post-construction cleanup, commercial janitorial, deep cleaning, floors and windows across Broward, Miami-Dade and Palm Beach.", "services/", services, body_class="archive page")
    for s in SERVICES:
        page(2, f"services/{s['slug']}/", f"{s['name']} in South Florida | Legally Clean", DETAIL[s["id"]]["lede"], "services/", service_single(s), body_class="single page")
    page(1, "projects/", "Projects | Legally Clean",
         "Post-construction cleanup for Broward Health, schools and commercial buildouts across South Florida.", "projects/", projects)
    page(1, "about-us/", "About Us | Legally Clean",
         "Woman-owned, MWBE-certified commercial cleaning company founded by Sherry W. Rudolph in 2006.", "about-us/", about)
    page(1, "reviews/", "Reviews | Legally Clean", "What contractors and clients say about Legally Clean.", "reviews/", reviews)
    page(1, "contact-us/", f"Contact Us | Legally Clean | {PHONE}",
         f"Call {PHONE}, email or send a message. Offices in Lauderhill, Miami and West Palm Beach. Open {HOURS_TEXT}.", "contact-us/", contact)
    page(1, "quote/", "Request a Quote | Legally Clean",
         "Request a free quote for post-construction cleanup, janitorial or deep cleaning in South Florida.", None, quote, actions=False)
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
