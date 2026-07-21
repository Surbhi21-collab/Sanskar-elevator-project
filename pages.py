#!/usr/bin/env python3
"""Page builders for the Sanskar Elevator site. Run `python build.py`."""

from build import *   # noqa: F401,F403  (SITE, SERVICES, partials, helpers)


# ---------------------------------------------------------------- helpers
def contact_details_block(depth):
    addr = "<br>".join(SITE["addr_lines"])
    return f"""
<ul class="contact__list">
  <li>
    <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1116 0z"/><circle cx="12" cy="10" r="3"/></svg>
    <div><strong>Office Address</strong><address>{addr}</address></div>
  </li>
  <li>
    <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>
    <div><strong>Phone</strong><span><a href="tel:{SITE['phone1_raw']}">{SITE['phone1']}</a><br>
      <a href="tel:{SITE['phone2_raw']}">{SITE['phone2']}</a></span></div>
  </li>
  <li>
    <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2.5 6.5L12 13l9.5-6.5"/></svg>
    <div><strong>Email</strong><span><a href="mailto:{SITE['email']}">{SITE['email']}</a></span></div>
  </li>
  <li>
    <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>
    <div><strong>Working Hours</strong><span>Monday – Saturday<br>9:00 AM – 7:00 PM<br>
      <em>Emergency support available 24&times;7</em></span></div>
  </li>
</ul>
<a class="btn btn--whatsapp btn--block" href="https://wa.me/{SITE['whatsapp']}?text=Hello%20Sanskar%20Elevator%2C%20I%20would%20like%20a%20quotation."
   target="_blank" rel="noopener noreferrer">
  <svg class="icon" viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.1-.2 0-.4.1-.5l.4-.5c.1-.2.1-.3 0-.5l-.7-1.7c-.2-.4-.4-.4-.5-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.9 11.9 0 004.6 4 5 5 0 002.3.4 2.7 2.7 0 001.8-1.3 2.2 2.2 0 00.2-1.3c-.1-.1-.2-.2-.4-.3z"/></svg>
  Chat on WhatsApp
</a>"""


def map_embed(height=380):
    return f"""
<div class="map">
  <iframe title="Map showing {SITE['name']}, {SITE['addr_inline']}"
    src="https://maps.google.com/maps?q=Anjani%20Dham%20Colony%2C%20Sekdhakedi%20Road%2C%20Sehore%2C%20Madhya%20Pradesh%20466001&z=15&output=embed"
    width="100%" height="{height}" style="border:0" loading="lazy" allowfullscreen
    referrerpolicy="no-referrer-when-downgrade"></iframe>
</div>"""


def testimonial_cards(reveal=True):
    r = " reveal" if reveal else ""
    return "".join(f"""
      <article class="quote card{r}">
        <div class="stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
        <blockquote><p>{txt}</p></blockquote>
        <footer class="quote__by">
          <span class="avatar" aria-hidden="true">{n.split()[0][0]}{n.split()[-1][0]}</span>
          <span class="quote__who"><strong>{n}</strong><span>{city}</span></span>
        </footer>
      </article>""" for n, city, txt in TESTIMONIALS)


def faq_accordion(items):
    return "".join(f"""
    <div class="acc reveal">
      <h3><button class="acc__btn" type="button" aria-expanded="false">{q}
        <span class="acc__sign" aria-hidden="true"></span></button></h3>
      <div class="acc__panel"><p>{a}</p></div>
    </div>""" for q, a in items)


def faq_schema(items):
    ents = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (json_str(q), json_str(a)) for q, a in items)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % ents


def json_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---------------------------------------------------------------- HOME
def build_home():
    d = 0
    svc_cards = "".join(f"""
      <article class="card service reveal">
        <a class="service__link" href="services/{s['slug']}.html">
          <span class="service__media">
            <img src="{img(s['img'], 600, 400)}" alt="{s['alt']}" loading="lazy"
                 decoding="async" width="600" height="400">
          </span>
          <span class="service__body">
            <h3>{s['title']}</h3>
            <span class="service__desc">{s['short']}</span>
            <span class="link-arrow">Learn More <span aria-hidden="true">&rarr;</span></span>
          </span>
        </a>
      </article>""" for s in SERVICES[:6])

    why = "".join(f'<article class="feature reveal"><h3>{t}</h3><p>{b}</p></article>'
                  for t, b in WHY_US)
    steps = "".join(f'<li class="tl reveal"><span class="tl__dot">{i+1}</span>'
                    f'<h3>{t}</h3><p>{b}</p></li>'
                    for i, (t, b) in enumerate(PROCESS))

    hid = "1566096650255-98ba2641071e"
    aid = "1525273177952-67455d25871f"

    page = {
        "title": "Sanskar Elevator | Elevator Installation, AMC & Repair in Madhya Pradesh",
        "desc": (f"Sanskar Elevator — established {SITE['established']}, {SITE['years']}+ years experience. "
                 f"Elevator installation, maintenance, modernization and repair in Sehore, Bhopal, Indore "
                 f"and across Madhya Pradesh. Call {SITE['phone1']}."),
        "url": "index.html",
        "schema": local_business_schema(),
    }

    body = f"""
<div class="preloader" id="preloader" aria-hidden="true">
  <div class="preloader__shaft"><span class="preloader__car"></span></div>
  <p class="preloader__label">SANSKAR<span>ELEVATOR</span></p>
</div>
{header('index.html', d)}
<main id="main">

<section class="hero" id="home">
  <div class="hero__bg">
    <img src="{img(hid, 1920, 1080)}"
      srcset="{img(hid, 960, 540)} 960w, {img(hid, 1440, 810)} 1440w,
              {img(hid, 1920, 1080)} 1920w, {img(hid, 2560, 1440)} 2560w"
      sizes="100vw" alt="View upward through a glass elevator shaft in a modern building"
      width="1920" height="1080" fetchpriority="high" decoding="async">
  </div>
  <div class="hero__overlay" aria-hidden="true"></div>
  <div class="container hero__inner">
    <p class="hero__eyebrow reveal">Established {SITE['established']} &middot; {SITE['years']}+ Years of Experience</p>
    <h1 class="hero__title reveal">Trusted Elevator Solutions across <span class="text-gold">Madhya Pradesh</span></h1>
    <p class="hero__sub reveal">Sanskar Elevator installs, maintains and modernizes lifts for homes,
      hospitals, factories and commercial buildings. Experienced engineers, genuine parts,
      safety-focused installations and 24&times;7 support.</p>
    <div class="hero__cta reveal">
      <a class="btn btn--gold" href="contact.html">Request a Free Quote
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      <a class="btn btn--ghost" href="tel:{SITE['phone1_raw']}">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>
        {SITE['phone1']}</a>
    </div>
    <ul class="stats reveal">
      <li class="stat"><span class="stat__num"><span class="counter" data-target="500">0</span>+</span><span class="stat__label">Happy Clients</span></li>
      <li class="stat"><span class="stat__num"><span class="counter" data-target="25">0</span>+</span><span class="stat__label">Years Experience</span></li>
      <li class="stat"><span class="stat__num">{SITE['established']}</span><span class="stat__label">Established In</span></li>
      <li class="stat"><span class="stat__num">24&times;7</span><span class="stat__label">Support</span></li>
    </ul>
  </div>
</section>

<section class="trust" aria-label="Company highlights">
  <div class="container trust__inner">
    <span>Serving All Madhya Pradesh</span><i aria-hidden="true"></i>
    <span>Professional Installation</span><i aria-hidden="true"></i>
    <span>Genuine Parts</span><i aria-hidden="true"></i>
    <span>24&times;7 Support</span>
  </div>
</section>

<section class="section">
  <div class="container about">
    <div class="about__media reveal">
      <img class="about__img about__img--main" src="{img(aid, 900, 1100)}"
        srcset="{img(aid, 600, 733)} 600w, {img(aid, 900, 1100)} 900w, {img(aid, 1400, 1711)} 1400w"
        sizes="(max-width:900px) 90vw, 44vw"
        alt="An elevator doorway in a building interior still under construction" loading="lazy"
        decoding="async" width="900" height="1100">
      <div class="about__badge">
        <strong>{SITE['years']}+</strong><span>Years serving<br>Madhya Pradesh</span>
      </div>
    </div>
    <div class="about__body">
      <p class="eyebrow reveal">About Sanskar Elevator</p>
      <h2 class="reveal">A trusted elevator company since {SITE['established']}</h2>
      <p class="lead reveal">Sanskar Elevator was established in {SITE['established']} and has spent more
        than {SITE['years']} years installing, servicing and modernizing lifts across Madhya Pradesh.
        Under the leadership of our Managing Director, {SITE['md']}, the company has grown through
        repeat customers and referrals.</p>
      <p class="reveal">We work directly with building owners, architects and contractors — from a single
        home lift in Sehore to passenger and goods elevators for commercial and industrial projects in
        Bhopal, Indore and across the state.</p>
      <ul class="checklist reveal">
        <li>Experienced engineers who handle installation and servicing in-house</li>
        <li>Quality products and genuine replacement parts</li>
        <li>Safety-focused installations with ARD fitted as standard</li>
        <li>Customer-first approach with clear, honest quotations</li>
        <li>Reliable maintenance support backed by a 24&times;7 helpline</li>
      </ul>
      <a class="btn btn--navy reveal" href="about.html">More About Us
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Our Services</p>
      <h2 class="reveal">Complete elevator services under one roof</h2>
      <p class="section__lead reveal">Installation, maintenance, modernization and emergency repair —
        for every type of lift and every kind of building.</p>
    </header>
    <div class="grid grid--3 services">{svc_cards}</div>
    <p class="center-cta reveal"><a class="btn btn--navy" href="services.html">View All Services
      <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></p>
  </div>
</section>

{cta_banner(d)}

<section class="section section--navy">
  <div class="container">
    <header class="section__head section__head--light">
      <p class="eyebrow reveal">Why Choose Us</p>
      <h2 class="reveal">Why customers across Madhya Pradesh choose us</h2>
    </header>
    <div class="grid grid--5 features">{why}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">How We Work</p>
      <h2 class="reveal">From first call to long-term maintenance</h2>
    </header>
    <ol class="timeline">{steps}</ol>
  </div>
</section>

{service_areas_section(d)}

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Customer Reviews</p>
      <h2 class="reveal">What our customers say</h2>
    </header>
    <div class="grid grid--3">{testimonial_cards()}</div>
    <p class="center-cta reveal"><a class="btn btn--navy" href="testimonials.html">Read All Reviews
      <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></p>
  </div>
</section>

{emergency_section()}

<section class="section section--alt" id="enquiry">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Get in Touch</p>
      <h2 class="reveal">Request a free quotation</h2>
      <p class="section__lead reveal">Tell us about your building and our engineers will get back to you.
        There is no charge for the site visit or the estimate.</p>
    </header>
    <div class="contact">
      <div class="reveal">{enquiry_form('homeEnquiry')}</div>
      <div class="contact__side reveal">{contact_details_block(d)}</div>
    </div>
  </div>
</section>

</main>
{footer(d)}
{floating(d)}"""
    return write("index.html", head(page, d) + body)


# ---------------------------------------------------------------- ABOUT
def build_about():
    d = 0
    why = "".join(f'<article class="feature reveal"><h3>{t}</h3><p>{b}</p></article>'
                  for t, b in WHY_US)
    steps = "".join(f'<li class="tl reveal"><span class="tl__dot">{i+1}</span>'
                    f'<h3>{t}</h3><p>{b}</p></li>'
                    for i, (t, b) in enumerate(PROCESS))
    aid = "1504307651254-35680f356dfd"

    page = {
        "title": f"About Us | {SITE['name']} — Established {SITE['established']}, {SITE['years']}+ Years",
        "desc": (f"Sanskar Elevator was established in {SITE['established']} and has {SITE['years']}+ years "
                 f"of experience. Led by {SITE['md']}, we serve customers across Madhya Pradesh with "
                 f"quality products, expert engineers and safety-focused installations."),
        "url": "about.html",
    }

    body = f"""
{header('about.html', d)}
<main id="main">
{page_banner("About Sanskar Elevator",
             f"Established in {SITE['established']} &middot; {SITE['years']}+ years of experience &middot; Serving all of Madhya Pradesh",
             [("About", "about.html")], d, "1592256410394-51c948ec13d5")}

<section class="section">
  <div class="container about">
    <div class="about__media reveal">
      <img class="about__img about__img--main" src="{img(aid, 900, 1100)}"
        srcset="{img(aid, 600, 733)} 600w, {img(aid, 900, 1100)} 900w, {img(aid, 1400, 1711)} 1400w"
        sizes="(max-width:900px) 90vw, 44vw"
        alt="Construction workers on a building site during structural work"
        loading="lazy" decoding="async" width="900" height="1100">
      <div class="about__badge"><strong>{SITE['established']}</strong><span>Year the company<br>was established</span></div>
    </div>
    <div class="about__body">
      <p class="eyebrow reveal">Our Story</p>
      <h2 class="reveal">{SITE['years']}+ years of vertical transport experience</h2>
      <p class="lead reveal">Sanskar Elevator was established in {SITE['established']}. Over more than
        {SITE['years']} years we have installed, serviced and modernized lifts in homes, hospitals,
        factories, showrooms and commercial buildings throughout Madhya Pradesh.</p>
      <p class="reveal">The company is led by our Managing Director, <strong>{SITE['md']}</strong>.
        From our base in Sehore we serve Bhopal, Indore, Ashta, Kurawar, Vidisha, Khandwa and districts
        across the state. Much of our work comes from customers who have used us before, or who were
        referred by someone who has.</p>
      <p class="reveal">Our approach is straightforward: recommend the right lift for the building rather
        than the most expensive one, quote honestly, install it properly, and answer the phone when
        something goes wrong.</p>
      <a class="btn btn--gold reveal" href="contact.html">Talk to Our Team
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="grid grid--3">
      <article class="card mv__card reveal">
        <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8" fill="currentColor"/></svg>
        <h2>Our Mission</h2>
        <p>To make every vertical journey safe and dependable — through quality products, careful
           installation and maintenance support that customers can actually rely on.</p>
      </article>
      <article class="card mv__card reveal">
        <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><path d="M1.8 12S5.6 5 12 5s10.2 7 10.2 7-3.8 7-10.2 7S1.8 12 1.8 12z"/><circle cx="12" cy="12" r="3"/></svg>
        <h2>Our Vision</h2>
        <p>To remain the elevator company that building owners across Madhya Pradesh recommend first,
           known for safety, fair pricing and service that responds quickly.</p>
      </article>
      <article class="card mv__card reveal">
        <svg class="icon icon--gold" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.6 6.3 6.8.5-5.2 4.4 1.6 6.6L12 16.4 6.2 19.8l1.6-6.6L2.6 8.8l6.8-.5z"/></svg>
        <h2>Our Values</h2>
        <p>Safety before shortcuts, genuine parts over cheap substitutes, and a customer-first approach
           that treats after-sales service as part of the job, not an afterthought.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <header class="section__head section__head--light">
      <p class="eyebrow reveal">Why Choose Us</p>
      <h2 class="reveal">What sets our work apart</h2>
    </header>
    <div class="grid grid--5 features">{why}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Our Process</p>
      <h2 class="reveal">How a project runs from start to finish</h2>
    </header>
    <ol class="timeline">{steps}</ol>
  </div>
</section>

{service_areas_section(d)}
{cta_banner(d)}
</main>
{footer(d)}
{floating(d)}"""
    return write("about.html", head(page, d) + body)


# ---------------------------------------------------------------- SERVICES INDEX
def build_services_index():
    d = 0
    cards = "".join(f"""
      <article class="card service reveal">
        <a class="service__link" href="services/{s['slug']}.html">
          <span class="service__media">
            <img src="{img(s['img'], 600, 400)}" alt="{s['alt']}" loading="lazy"
                 decoding="async" width="600" height="400">
          </span>
          <span class="service__body">
            <h2>{s['title']}</h2>
            <span class="service__desc">{s['short']}</span>
            <span class="link-arrow">Learn More <span aria-hidden="true">&rarr;</span></span>
          </span>
        </a>
      </article>""" for s in SERVICES)

    page = {
        "title": f"Elevator Services | Installation, AMC, Repair & Modernization | {SITE['name']}",
        "desc": ("Passenger, home, hospital, goods, capsule and hydraulic elevators, plus AMC, repair, "
                 "modernization, installation and 24×7 emergency breakdown service across Madhya Pradesh."),
        "url": "services.html",
    }

    body = f"""
{header('services.html', d)}
<main id="main">
{page_banner("Our Services",
             "Installation, maintenance, modernization and emergency support for every type of lift.",
             [("Services", "services.html")], d, "1596711684682-2f3ea5d2d739")}

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">What We Offer</p>
      <h2 class="reveal">Eleven services, one accountable company</h2>
      <p class="section__lead reveal">Whether you need a new lift installed, an old one modernized or an
        engineer on site tonight, it is handled by our own team — not subcontracted out.</p>
    </header>
    <div class="grid grid--3 services">{cards}</div>
  </div>
</section>

{cta_banner(d)}
{service_areas_section(d)}
{emergency_section()}
</main>
{footer(d)}
{floating(d)}"""
    return write("services.html", head(page, d) + body)


# ---------------------------------------------------------------- SERVICE DETAIL
def build_service_page(s):
    d = 1
    feats = "".join(f"<li>{f}</li>" for f in s["features"])
    bens = "".join(f"<li>{b}</li>" for b in s["benefits"])
    safe = "".join(f"<li>{x}</li>" for x in s["safety"])
    intro = "".join(f"<p>{p}</p>" for p in s["intro"])

    others = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    related = "".join(f"""
      <article class="card service reveal">
        <a class="service__link" href="{o['slug']}.html">
          <span class="service__media">
            <img src="{img(o['img'], 600, 400)}" alt="{o['alt']}" loading="lazy"
                 decoding="async" width="600" height="400">
          </span>
          <span class="service__body"><h3>{o['title']}</h3>
            <span class="service__desc">{o['short']}</span>
            <span class="link-arrow">Learn More <span aria-hidden="true">&rarr;</span></span>
          </span>
        </a>
      </article>""" for o in others)

    schema = ('{"@context":"https://schema.org","@type":"Service","name":%s,'
              '"description":%s,"serviceType":%s,'
              '"provider":{"@type":"LocalBusiness","name":"%s","telephone":"%s",'
              '"address":{"@type":"PostalAddress","addressLocality":"Sehore",'
              '"addressRegion":"Madhya Pradesh","postalCode":"466001","addressCountry":"IN"}},'
              '"areaServed":{"@type":"State","name":"Madhya Pradesh"}}'
              % (json_str(s["title"]), json_str(s["short"]), json_str(s["title"]),
                 SITE["name"], SITE["phone1_raw"]))

    page = {
        "title": f"{s['title']} in Madhya Pradesh | {SITE['name']}",
        "desc": f"{s['short']} {SITE['name']} — established {SITE['established']}, {SITE['years']}+ years experience. Serving Sehore, Bhopal, Indore and all of Madhya Pradesh. Call {SITE['phone1']}.",
        "url": f"services/{s['slug']}.html",
        "og": img(s["img"], 1200, 630),
        "schema": schema,
    }

    body = f"""
{header('services.html', d)}
<main id="main">
{page_banner(s['title'], s['short'], [("Services", "services.html"), (s['title'], "")], d, s['img'])}

<section class="section">
  <div class="container svc">
    <div class="svc__main">
      <p class="eyebrow reveal">Overview</p>
      <h2 class="reveal">{s['title']} from {SITE['name']}</h2>
      <div class="prose reveal">{intro}</div>

      <figure class="svc__figure reveal">
        <img src="{img(s['img'], 1000, 620)}"
             srcset="{img(s['img'], 700, 434)} 700w, {img(s['img'], 1000, 620)} 1000w, {img(s['img'], 1500, 930)} 1500w"
             sizes="(max-width:900px) 92vw, 62vw"
             alt="{s['alt']}" loading="lazy" decoding="async" width="1000" height="620">
      </figure>

      <h3 class="reveal">Features</h3>
      <ul class="checklist reveal">{feats}</ul>

      <h3 class="reveal">Benefits</h3>
      <ul class="checklist reveal">{bens}</ul>

      <h3 class="reveal">Safety Standards</h3>
      <ul class="checklist checklist--shield reveal">{safe}</ul>

      <div class="svc__cta reveal">
        <h3>Request a quotation for {s['title'].lower()}</h3>
        <p>Free site visit and written estimate anywhere in Madhya Pradesh.</p>
        <div class="svc__cta-actions">
          <a class="btn btn--gold" href="../contact.html">Get a Free Quote
            <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
          <a class="btn btn--navy" href="tel:{SITE['phone1_raw']}">Call {SITE['phone1']}</a>
        </div>
      </div>
    </div>

    <aside class="svc__aside" aria-label="Contact and other services">
      <div class="card svc__box reveal">
        <h3>Speak to an engineer</h3>
        <p>Tell us your building type, number of floors and required capacity — we will do the rest.</p>
        <a class="btn btn--gold btn--block" href="tel:{SITE['phone1_raw']}">{SITE['phone1']}</a>
        <a class="btn btn--whatsapp btn--block" href="https://wa.me/{SITE['whatsapp']}?text=Hello%2C%20I%20would%20like%20details%20about%20{s['title'].replace(' ', '%20')}."
           target="_blank" rel="noopener noreferrer">WhatsApp Us</a>
        <p class="svc__box-note">{SITE['hours']}<br>Emergency support 24&times;7</p>
      </div>
      <nav class="card svc__box reveal" aria-label="All services">
        <h3>All Services</h3>
        <ul class="svc__list">
          {"".join(f'<li><a href="{o["slug"]}.html"{" class=is-current" if o["slug"]==s["slug"] else ""}>{o["title"]}</a></li>' for o in SERVICES)}
        </ul>
      </nav>
    </aside>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">More Services</p>
      <h2 class="reveal">You may also need</h2>
    </header>
    <div class="grid grid--3 services">{related}</div>
  </div>
</section>

{emergency_section()}
</main>
{footer(d)}
{floating(d)}"""
    return write(f"services/{s['slug']}.html", head(page, d) + body)


# ---------------------------------------------------------------- GALLERY
def build_gallery():
    d = 0
    filters = "".join(
        f'<button class="filter{" is-active" if k=="all" else ""}" role="tab" '
        f'aria-selected="{"true" if k=="all" else "false"}" data-filter="{k}">{label}</button>'
        for k, label in GALLERY_FILTERS)

    tiles = "".join(f"""
      <figure class="tile reveal" data-cat="{cat}">
        <img src="{img(pid, w, h)}" alt="{title} — {cap}" loading="lazy"
             decoding="async" width="{w}" height="{h}">
        <figcaption><strong>{title}</strong><span>{cap}</span></figcaption>
      </figure>""" for pid, cat, title, cap, w, h in GALLERY)

    page = {
        "title": f"Gallery | Elevator Installations & Projects | {SITE['name']}",
        "desc": ("Photo gallery of elevator installations, home lifts, passenger lifts, hospital lifts, "
                 "commercial projects and maintenance work by Sanskar Elevator across Madhya Pradesh."),
        "url": "gallery.html",
    }

    body = f"""
{header('gallery.html', d)}
<main id="main">
{page_banner("Gallery",
             "Elevator installations, home lifts, commercial projects and maintenance work.",
             [("Gallery", "gallery.html")], d, "1565417814737-6b4097de8a3a")}

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Our Work</p>
      <h2 class="reveal">Installations and service work</h2>
      <p class="section__lead reveal">A selection of the elevator types we install and maintain.
        Select a category to filter, or click any image to view it larger.</p>
    </header>
    <div class="filters reveal" role="tablist" aria-label="Filter gallery by category">{filters}</div>
    <div class="masonry" id="gallery">{tiles}</div>
  </div>
</section>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
  <button class="lightbox__close" id="lbClose" type="button" aria-label="Close viewer">&times;</button>
  <button class="lightbox__nav lightbox__nav--prev" id="lbPrev" type="button" aria-label="Previous image">&#8249;</button>
  <figure class="lightbox__figure"><img id="lbImg" src="" alt=""><figcaption id="lbCap"></figcaption></figure>
  <button class="lightbox__nav lightbox__nav--next" id="lbNext" type="button" aria-label="Next image">&#8250;</button>
</div>

{cta_banner(d)}
</main>
{footer(d)}
{floating(d)}"""
    return write("gallery.html", head(page, d) + body)


# ---------------------------------------------------------------- TESTIMONIALS
def build_testimonials():
    d = 0
    page = {
        "title": f"Customer Testimonials & Reviews | {SITE['name']}",
        "desc": ("Read reviews from Sanskar Elevator customers in Kurawar, Ashta and Sehore about our "
                 "elevator installation, maintenance and after-sales service."),
        "url": "testimonials.html",
    }
    body = f"""
{header('testimonials.html', d)}
<main id="main">
{page_banner("Customer Testimonials",
             "What building owners across Madhya Pradesh say about our work.",
             [("Testimonials", "testimonials.html")], d, "1719463814218-52e17f720e8a")}

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Customer Reviews</p>
      <h2 class="reveal">In our customers' words</h2>
      <p class="section__lead reveal">Most of our work comes from repeat customers and referrals.
        Here is what some of them have said.</p>
    </header>
    <div class="grid grid--3">{testimonial_cards()}</div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <header class="section__head section__head--light">
      <p class="eyebrow reveal">Why Customers Return</p>
      <h2 class="reveal">The reasons they give us</h2>
    </header>
    <div class="grid grid--5 features">
      {"".join(f'<article class="feature reveal"><h3>{t}</h3><p>{b}</p></article>' for t, b in WHY_US)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow center">
    <h2 class="reveal">Have you worked with us?</h2>
    <p class="section__lead reveal">We would be glad to hear about your experience — and if something
      was not right, we would rather know so we can put it in order.</p>
    <p class="center-cta reveal">
      <a class="btn btn--gold" href="contact.html">Share Your Feedback</a>
      <a class="btn btn--navy" href="tel:{SITE['phone1_raw']}">Call {SITE['phone1']}</a>
    </p>
  </div>
</section>

{cta_banner(d)}
</main>
{footer(d)}
{floating(d)}"""
    return write("testimonials.html", head(page, d) + body)


# ---------------------------------------------------------------- FAQ
def build_faq():
    d = 0
    page = {
        "title": f"Frequently Asked Questions | {SITE['name']}",
        "desc": ("Answers to common questions about elevator installation time, AMC coverage, service "
                 "areas in Madhya Pradesh, power failure rescue, pricing and breakdown response."),
        "url": "faq.html",
        "schema": faq_schema(FAQS),
    }
    body = f"""
{header('faq.html', d)}
<main id="main">
{page_banner("Frequently Asked Questions",
             "Installation timelines, AMC coverage, service areas and emergency response.",
             [("FAQ", "faq.html")], d, "1562654501-9a587e8638d8")}

<section class="section">
  <div class="container container--narrow">
    <header class="section__head">
      <p class="eyebrow reveal">FAQ</p>
      <h2 class="reveal">Questions we are asked most</h2>
    </header>
    <div class="accordion" id="accordion">{faq_accordion(FAQS)}</div>

    <div class="faq__more reveal">
      <h3>Still have a question?</h3>
      <p>Call us on <a href="tel:{SITE['phone1_raw']}">{SITE['phone1']}</a> or
         <a href="tel:{SITE['phone2_raw']}">{SITE['phone2']}</a>, or send an enquiry and we will reply.</p>
      <a class="btn btn--gold" href="contact.html">Contact Us
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>
</section>

{emergency_section()}
{cta_banner(d)}
</main>
{footer(d)}
{floating(d)}"""
    return write("faq.html", head(page, d) + body)


# ---------------------------------------------------------------- CONTACT
def build_contact():
    d = 0
    page = {
        "title": f"Contact Us | {SITE['name']}, Sehore — {SITE['phone1']}",
        "desc": (f"Contact Sanskar Elevator: {SITE['addr_inline']}. Phone {SITE['phone1']} / "
                 f"{SITE['phone2']}, email {SITE['email']}. Open Monday to Saturday, 9:00 AM – 7:00 PM."),
        "url": "contact.html",
        "schema": local_business_schema(),
    }
    body = f"""
{header('contact.html', d)}
<main id="main">
{page_banner("Contact Us",
             "Free site visit and written quotation anywhere in Madhya Pradesh.",
             [("Contact", "contact.html")], d, "1585293878107-569e3ebdab53")}

<section class="section">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Enquiry</p>
      <h2 class="reveal">Send us your requirement</h2>
      <p class="section__lead reveal">Fill in the form and our team will get back to you. For anything
        urgent, please call — the phone is faster than email.</p>
    </header>
    <div class="contact">
      <div class="reveal">{enquiry_form('contactForm')}</div>
      <div class="contact__side reveal">{contact_details_block(d)}</div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Find Us</p>
      <h2 class="reveal">Our office in Sehore</h2>
      <p class="section__lead reveal">{SITE['addr_inline']}</p>
    </header>
    <div class="reveal">{map_embed(420)}</div>
  </div>
</section>

{service_areas_section(d)}
{emergency_section()}
</main>
{footer(d)}
{floating(d)}"""
    return write("contact.html", head(page, d) + body)


# ---------------------------------------------------------------- LEGAL PAGES
def legal_page(filename, title, banner_sub, sections, desc):
    d = 0
    body_sections = "".join(
        f'<h2 class="reveal">{h}</h2>' + "".join(f'<p class="reveal">{p}</p>' for p in ps)
        for h, ps in sections)
    page = {"title": f"{title} | {SITE['name']}", "desc": desc, "url": filename}
    body = f"""
{header('', d)}
<main id="main">
{page_banner(title, banner_sub, [(title, filename)], d, "1547630824-eed1be6a27b0")}
<section class="section">
  <div class="container container--narrow prose prose--legal">
    <p class="legal__updated reveal"><strong>Last updated:</strong> 1 January {SITE['year']}</p>
    {body_sections}
    <h2 class="reveal">Contact</h2>
    <p class="reveal">For any question about this page, contact us at
      <a href="mailto:{SITE['email']}">{SITE['email']}</a> or
      <a href="tel:{SITE['phone1_raw']}">{SITE['phone1']}</a>.<br>
      {SITE['name']}, {SITE['addr_inline']}.</p>
  </div>
</section>
</main>
{footer(d)}
{floating(d)}"""
    return write(filename, head(page, d) + body)


def build_privacy():
    return legal_page(
        "privacy-policy.html", "Privacy Policy",
        "How we handle the information you share with us.",
        [
            ("Information we collect", [
                "When you submit an enquiry through this website we collect the details you provide: your name, phone number, email address, city, the service you are interested in and your message. We collect this only so that we can respond to your enquiry.",
                "We do not require you to create an account, and we do not ask for payment information through this website."]),
            ("How we use your information", [
                "Your details are used to respond to your enquiry, prepare a quotation, arrange a site visit, and provide ongoing service or maintenance support if you become a customer.",
                "We do not sell, rent or trade your personal information to third parties."]),
            ("Cookies", [
                "This website uses a small amount of browser storage to remember your display preference (light or dark theme) and whether you have dismissed the cookie notice. This information stays in your browser and is not transmitted to us.",
                "The embedded Google Map and the web fonts used on this site are loaded from Google's servers, and Google may set its own cookies. Please refer to Google's privacy policy for details of their practices."]),
            ("Data retention", [
                "We keep enquiry details for as long as needed to respond and, where you become a customer, for the duration of our working relationship and any statutory record-keeping period that applies."]),
            ("Your rights", [
                "You may ask us what information we hold about you, ask us to correct it, or ask us to delete it. Contact us using the details below and we will action your request."]),
            ("Changes to this policy", [
                "We may update this policy from time to time. The date at the top of this page shows when it was last revised."]),
        ],
        "Privacy Policy for Sanskar Elevator — what information we collect through this website, how we use it, and your rights.")


def build_terms():
    return legal_page(
        "terms-conditions.html", "Terms & Conditions",
        "The terms on which we provide this website and our services.",
        [
            ("Use of this website", [
                "This website is provided for information about Sanskar Elevator and the services we offer. You may use it to learn about our products and to contact us. You may not use it in any way that damages the site or interferes with other people's use of it."]),
            ("Accuracy of information", [
                "We take care to keep the information on this site accurate and current. Specifications, capacities and dimensions shown are indicative and are confirmed at the time of quotation, since every installation depends on the individual building.",
                "Images on this site are illustrative of the product types we supply."]),
            ("Quotations and pricing", [
                "Prices are provided by written quotation following a site visit. A quotation remains valid for the period stated on it. Quotations are based on the site conditions observed at the time, and may be revised if those conditions change.",
                "The initial site visit and estimate are provided free of charge."]),
            ("Installation and delivery", [
                "Installation timelines given in a quotation assume the building is ready — including shaft, pit, headroom and power supply as specified in our drawings. Delays caused by site readiness may extend the timeline.",
                "Responsibility for civil work rests with the customer or their contractor unless our quotation expressly includes it."]),
            ("Warranty", [
                "New installations carry a warranty period stated in the quotation and covering manufacturing defects. The warranty does not cover damage from misuse, unauthorised modification, water ingress, power supply faults, or work carried out by third parties.",
                "Warranty terms for individual components may vary according to the manufacturer of that component."]),
            ("Maintenance contracts", [
                "The scope of an Annual Maintenance Contract is set out in the individual agreement, which specifies whether it is semi-comprehensive or comprehensive, the number of scheduled visits, and the emergency response window that applies."]),
            ("Limitation of liability", [
                "Nothing in these terms limits our liability for death or personal injury caused by negligence, or for any other liability that cannot be excluded under applicable law."]),
            ("Governing law", [
                "These terms are governed by the laws of India, and any dispute is subject to the jurisdiction of the courts of Sehore, Madhya Pradesh."]),
        ],
        "Terms and Conditions for Sanskar Elevator — website use, quotations, installation, warranty and maintenance contract terms.")


# ---------------------------------------------------------------- SITEMAP / ROBOTS
def build_sitemap():
    today = date.today().isoformat()
    urls = [("index.html", "1.0", "weekly"), ("about.html", "0.8", "monthly"),
            ("services.html", "0.9", "monthly"), ("gallery.html", "0.7", "monthly"),
            ("testimonials.html", "0.6", "monthly"), ("faq.html", "0.6", "monthly"),
            ("contact.html", "0.9", "monthly"),
            ("privacy-policy.html", "0.3", "yearly"),
            ("terms-conditions.html", "0.3", "yearly")]
    urls += [(f"services/{s['slug']}.html", "0.8", "monthly") for s in SERVICES]

    entries = "".join(
        f"  <url>\n    <loc>{SITE['domain']}/{u}</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{p}</priority>\n  </url>\n"
        for u, p, cf in urls)

    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + entries + '</urlset>\n')

    write("robots.txt",
          "User-agent: *\nAllow: /\n\n"
          f"Sitemap: {SITE['domain']}/sitemap.xml\n")
    return len(urls)
