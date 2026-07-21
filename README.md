# Sanskar Elevator — Website

Production-ready static site. 20 HTML pages, no framework, no runtime dependencies.
Upload the folder to any static host (Hostinger, Netlify, Vercel, GitHub Pages, cPanel, S3).

## Structure

```
finalwebsite/
├── index.html              Home
├── about.html              About
├── services.html           Services index
├── gallery.html            Gallery + lightbox
├── testimonials.html       Customer reviews
├── faq.html                FAQ (with FAQPage schema)
├── contact.html            Contact form + Google Map
├── privacy-policy.html
├── terms-conditions.html
├── services/               11 individual service pages
│   ├── passenger-elevators.html      home-elevators.html
│   ├── hospital-elevators.html       goods-elevators.html
│   ├── capsule-elevators.html        hydraulic-elevators.html
│   ├── elevator-amc.html             elevator-repair.html
│   ├── elevator-modernization.html   installation-services.html
│   └── emergency-breakdown-service.html
├── assets/
│   ├── css/style.css       Design tokens + all styles (18 sections)
│   ├── js/main.js          15 self-contained modules
│   └── img/favicon.svg
├── robots.txt
├── sitemap.xml             All 20 URLs
│
├── build.py                DATA: company details, services, gallery, FAQ + partials
├── pages.py                Page builders
└── make.py                 Run this to rebuild
```

## Editing content

**The HTML files are generated. Do not edit them directly** — your changes will be
overwritten on the next build. Edit the source, then rebuild:

```bash
python make.py
```

| To change… | Edit |
|---|---|
| Phone, email, address, MD name, year | `SITE` dict at the top of `build.py` |
| Service pages (text, features, images) | `SERVICES` list in `build.py` |
| Gallery images and captions | `GALLERY` in `build.py` |
| Testimonials | `TESTIMONIALS` in `build.py` |
| FAQ questions | `FAQS` in `build.py` |
| "Why Choose Us" points | `WHY_US` in `build.py` |
| Service area cities | `CITIES` in `build.py` |
| Header / footer / nav | the partial functions in `build.py` |

Because every page pulls from these, changing a phone number in one place updates
all 20 pages, the footer, the WhatsApp links and the structured data together.

## Before you go live — required steps

**1. Connect the enquiry form to a backend.**
The form validates fully and shows success/error states, but does not yet send
anywhere. In `assets/js/main.js`, module 12, replace the `setTimeout` under
`// ---- Submission hook ----` with a real request:

```js
fetch('https://formspree.io/f/YOUR_ID', {
  method: 'POST',
  body: new FormData(form),
  headers: { Accept: 'application/json' }
})
```

Formspree, Getform or Web3Forms need no server. If your host supports PHP, post
to a small `send.php` instead.

**2. Replace the stock photography.**
All images are Unsplash stock photos of *generic* elevators — not Sanskar
Elevator's own work. For a real business site these should be replaced with
photographs of your actual installations. When you swap an image, update the
`alt` text in `build.py` to describe the new picture accurately.

**3. Set your real domain.**
`SITE["domain"]` in `build.py` is `https://www.sanskarelevator.com`. Change it to
your real domain and rebuild so the canonical tags, Open Graph URLs and sitemap
are correct.

**4. Confirm the map pin.**
The Google Map searches for "Anjani Dham Colony, Sekdhakedi Road, Sehore". If the
pin lands slightly off, get an exact embed from Google Maps (Share → Embed a map)
and paste its `src` into `map_embed()` in `pages.py`.

**5. Social links.**
Footer icons currently point at facebook.com / instagram.com. Put your real
profile URLs in the `footer()` function in `build.py`, or delete the ones you
don't use.

## What's included

**Pages** — 20, all interlinked, no dead links (verified: 1354 links resolve).

**Features** — sticky header with services dropdown, mobile off-canvas nav,
scroll progress bar, preloader, animated counters, reveal-on-scroll, filterable
gallery with keyboard-accessible lightbox, FAQ accordion, validated enquiry form,
floating WhatsApp + call buttons, back-to-top, dark mode (persisted), cookie notice,
CTA banners, service-area section, emergency contact strip.

**SEO** — unique title + meta description per page, canonical URLs, Open Graph and
Twitter cards, `LocalBusiness` schema (with founder, address, service area and
offer catalog), `Service` schema on each service page, `FAQPage` schema on the FAQ,
sitemap.xml and robots.txt.

**Accessibility** — one `<h1>` per page with no heading-level jumps, all images have
alt text, all form fields have labels, all iframes titled, breadcrumbs with
`aria-current`, visible focus rings, keyboard-operable gallery and menus, and full
`prefers-reduced-motion` support. Body text sits at ~7.2:1 contrast (AAA).

**Rendering** — no `backdrop-filter`, no `filter`, no `scale()` on text or images,
whole-pixel transforms only, and OS-default font smoothing, so text stays sharp.

## Performance

Zero third-party JavaScript. Fonts preloaded and applied non-blockingly. Images are
WebP at q=82, lazy-loaded below the fold, with explicit `width`/`height` (no layout
shift) and `srcset` on the large ones. Scroll handlers are `requestAnimationFrame`
throttled and passive.

To minify before deploying:

```bash
npx clean-css-cli -o assets/css/style.min.css assets/css/style.css
npx terser assets/js/main.js -c -m -o assets/js/main.min.js
```

Then point the `<link>` and `<script>` in `head()` / `floating()` in `build.py` at
the `.min` files and rebuild. Enabling gzip or brotli on your host matters more
than minification.
