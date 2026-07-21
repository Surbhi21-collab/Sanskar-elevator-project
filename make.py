#!/usr/bin/env python3
"""
Build the Sanskar Elevator website.

    python make.py

Regenerates every HTML page from the shared partials in build.py and the page
builders in pages.py. Company details live in the SITE dict in build.py — change
them there once and re-run this script to update the whole site.
"""

import pages
from build import SERVICES


def main():
    written = []
    written.append(pages.build_home())
    written.append(pages.build_about())
    written.append(pages.build_services_index())
    for s in SERVICES:
        written.append(pages.build_service_page(s))
    written.append(pages.build_gallery())
    written.append(pages.build_testimonials())
    written.append(pages.build_faq())
    written.append(pages.build_contact())
    written.append(pages.build_privacy())
    written.append(pages.build_terms())
    n = pages.build_sitemap()

    print(f"Built {len(written)} pages:")
    for w in written:
        print("  ", w)
    print(f"sitemap.xml ({n} urls) + robots.txt")


if __name__ == "__main__":
    main()
