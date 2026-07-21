#!/usr/bin/env python3
"""
Sanskar Elevator — static site generator.

Data and shared partials. This module defines the company details, service
content and the header/footer/banner components used by every page.

Company details, navigation and footer exist in exactly ONE place — edit the
SITE dict or the SERVICES list below, then rebuild:

    python make.py
"""

import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
#  COMPANY DETAILS — single source of truth
# =====================================================================
SITE = {
    "name": "Sanskar Elevator",
    "tagline": "Elevator Installation, Maintenance & Modernization across Madhya Pradesh",
    "established": "2000",
    "years": "25",
    "md": "Mr. Mahendra Sahu",
    "phone1": "+91 9179324294",
    "phone1_raw": "+919179324294",
    "phone2": "+91 9111320632",
    "phone2_raw": "+919111320632",
    "whatsapp": "919179324294",
    "email": "sanskarelevator@gmail.com",
    "addr_lines": ["Anjani Dham Colony", "Sekdhakedi Road", "Sehore",
                   "Madhya Pradesh", "PIN: 466001"],
    "addr_inline": "Anjani Dham Colony, Sekdhakedi Road, Sehore, Madhya Pradesh 466001",
    "locality": "Sehore",
    "region": "Madhya Pradesh",
    "pin": "466001",
    "hours": "Monday – Saturday, 9:00 AM – 7:00 PM",
    "domain": "https://www.sanskarelevator.com",
    "year": 2026,
}

CITIES = ["Bhopal", "Indore", "Sehore", "Ashta", "Kurawar", "Vidisha", "Khandwa"]

IMG = "https://images.unsplash.com/photo-{id}?fm=webp&fit=crop&w={w}&h={h}&q=82"


def img(pid, w, h):
    return IMG.format(id=pid, w=w, h=h)


# =====================================================================
#  SERVICES — drives both the services index and 11 detail pages
# =====================================================================
SERVICES = [
    {
        "slug": "passenger-elevators",
        "title": "Passenger Elevators",
        "short": "Smooth, energy-efficient lifts for apartments, offices and commercial buildings.",
        "img": "1592256410394-51c948ec13d5",
        "alt": "Stainless steel elevator doors with call button panels in a wood-panelled lobby",
        "intro": [
            "Passenger elevators are the backbone of any multi-storey building, and they are the product we install most often across Madhya Pradesh. We supply machine-room and machine-room-less (MRL) configurations from 4 to 20 passengers, with travel speeds matched to the height and traffic of your building.",
            "Every unit is configured around your actual shaft dimensions rather than a fixed catalogue size, so you get the largest usable cabin your structure allows. Cabin finishes range from powder-coated steel for budget-conscious projects through to hairline stainless steel, mirror panels and designer laminates for premium lobbies.",
        ],
        "features": [
            "Capacity from 4 to 20 passengers (272 kg to 1360 kg)",
            "Gearless and geared traction drives with VVVF control",
            "Machine-room-less option where headroom is limited",
            "Automatic and manual door configurations",
            "LED cabin lighting with low power consumption",
            "Digital position indicators and hall lanterns",
        ],
        "benefits": [
            "Smooth acceleration and accurate floor levelling for passenger comfort",
            "VVVF drives cut running costs compared with older two-speed motors",
            "Quiet operation suitable for residential buildings",
            "Cabin interiors customised to your architect's material palette",
            "Spare parts readily available, keeping long-term maintenance affordable",
        ],
        "safety": [
            "Automatic Rescue Device (ARD) moves the car to the nearest floor on power failure",
            "Overload sensing prevents the lift from starting when over capacity",
            "Overspeed governor with safety gear arrests the car in a free-fall condition",
            "Door sensors reopen the doors on any obstruction",
            "Emergency alarm, intercom and cabin lighting backed by battery supply",
        ],
    },
    {
        "slug": "home-elevators",
        "title": "Home Elevators",
        "short": "Compact residential lifts that fit existing homes with minimal civil work.",
        "img": "1699793982261-24c55bf385d5",
        "alt": "A single elevator door set into a plain wall on a residential landing",
        "intro": [
            "A home elevator returns the whole house to elderly parents and family members with limited mobility. Our residential lifts are designed for retrofit: they need a shallow pit, low headroom and a footprint as small as 1000 × 1000 mm, so they can usually be added to a stairwell void, courtyard or external glass shaft without rebuilding the structure.",
            "We handle the full process — site measurement, structural advice, fabrication of the shaft if required, installation and commissioning. Most home installations are complete within seven to ten working days once the site is ready.",
        ],
        "features": [
            "Footprint from approximately 1000 × 1000 mm",
            "Shallow pit and low headroom designs for existing buildings",
            "Capacity of 2 to 6 persons",
            "Glass, wooden, laminate or stainless steel cabin finishes",
            "Self-supporting steel structure where no masonry shaft exists",
            "Quiet drive suitable for use at night",
        ],
        "benefits": [
            "Restores full access to upper floors for elderly family members",
            "Adds long-term resale value to the property",
            "Minimal disruption during installation — no full-scale civil work",
            "Low power draw, running on a standard domestic supply",
            "Wheelchair-accessible configurations available",
        ],
        "safety": [
            "Automatic Rescue Device brings the car to a landing during a power cut",
            "Safety gear and overspeed governor fitted as standard",
            "Interlocked doors that cannot open unless the car is at a landing",
            "Emergency stop and alarm inside the cabin",
            "Battery-backed emergency lighting",
        ],
    },
    {
        "slug": "hospital-elevators",
        "title": "Hospital Elevators",
        "short": "Stretcher-depth cabins with jerk-free levelling for patient transfers.",
        "img": "1585293878107-569e3ebdab53",
        "alt": "Elevator doors in a stone-clad building lobby marked floor 2",
        "intro": [
            "Hospital lifts have to carry a stretcher, an attendant and equipment at the same time, which means a deep, narrow cabin and doors wide enough to roll a trolley through without manoeuvring. We build bed and stretcher elevators to those proportions, typically 1000 to 1600 kg with a clear opening of 1200 mm or more.",
            "Ride quality matters more here than anywhere else. Our hospital installations use VVVF gearless drives tuned for gradual acceleration and accurate levelling, so a patient on a trolley is not jolted at the start or end of a trip.",
        ],
        "features": [
            "Stretcher-depth cabins from 1000 kg to 1600 kg capacity",
            "Wide clear door openings for trolley and bed access",
            "Antibacterial and easily sanitised cabin surfaces",
            "Gearless VVVF drive tuned for gradual acceleration",
            "Handrails and protective bumper rails inside the cabin",
            "Priority and attendant-control operation modes",
        ],
        "benefits": [
            "Jerk-free travel and accurate levelling for patient comfort",
            "Cabin dimensions that genuinely fit a stretcher plus attendants",
            "Surfaces that stand up to repeated disinfection",
            "Reliable performance under continuous daily use",
            "Priority modes that keep the lift available for critical transfers",
        ],
        "safety": [
            "Automatic Rescue Device for immediate evacuation on power failure",
            "Fireman's operation mode for emergency service access",
            "Overspeed governor and safety gear",
            "Infrared door curtains covering the full door height",
            "Emergency intercom connected to the hospital control room",
        ],
    },
    {
        "slug": "goods-elevators",
        "title": "Goods & Freight Elevators",
        "short": "Heavy-duty platforms from 500 kg to 5 tonnes for industry and warehousing.",
        "img": "1547630824-eed1be6a27b0",
        "alt": "Interior of a steel elevator car with brushed metal wall panels",
        "intro": [
            "Goods elevators move raw material, finished stock and trolleys between floors in factories, warehouses, godowns and commercial kitchens. We build them for the load you actually handle — from a 500 kg service platform up to 5 tonne freight lifts capable of taking a loaded pallet truck.",
            "Construction is deliberately robust: heavier guide rails, chequered steel flooring, reinforced cabin walls and door types chosen to survive daily industrial handling rather than to look decorative.",
        ],
        "features": [
            "Capacity from 500 kg to 5000 kg",
            "Chequered plate or industrial-grade flooring",
            "Collapsible, imperforate or power-operated doors",
            "Heavy-duty guide rails and reinforced cabin structure",
            "Optional through-car or adjacent two-entrance layouts",
            "Traction or hydraulic drive depending on travel height",
        ],
        "benefits": [
            "Reduces manual handling and the injury risk that comes with it",
            "Speeds up movement of stock between production floors",
            "Built to withstand continuous industrial duty cycles",
            "Sized to your pallet, trolley or drum dimensions",
            "Straightforward, low-cost long-term maintenance",
        ],
        "safety": [
            "Overload sensing that prevents operation beyond rated capacity",
            "Safety gear and overspeed governor",
            "Door interlocks on every landing",
            "Emergency stop controls inside the car and at each landing",
            "Clear rated-load signage as required by lift regulations",
        ],
    },
    {
        "slug": "capsule-elevators",
        "title": "Capsule Elevators",
        "short": "Panoramic glass observation lifts that become an architectural feature.",
        "img": "1565417814737-6b4097de8a3a",
        "alt": "Two gold panoramic capsule elevators on the exterior of a building",
        "intro": [
            "A capsule elevator turns vertical transport into a feature of the building. Semi-circular, square or fully round glass cabins are used in hotel atriums, showrooms, malls and increasingly in private residences where the lift is visible from the main living space.",
            "These installations need careful coordination with the architect and the structural engineer, particularly where the shaft is external or the glass is part of the façade. We handle that coordination and fabricate the supporting structure as part of the scope.",
        ],
        "features": [
            "Semi-circular, square and full-round cabin geometries",
            "Toughened laminated safety glass throughout",
            "Decorative LED cabin and ceiling lighting",
            "Self-supporting glass or steel shaft structures",
            "Indoor atrium and external façade configurations",
            "Stainless steel or powder-coated trim finishes",
        ],
        "benefits": [
            "Becomes a visual centrepiece for lobbies and atriums",
            "Open outlook makes the ride comfortable for anxious passengers",
            "Natural light travels through the shaft rather than being blocked",
            "Strong impression for hotels, showrooms and retail spaces",
            "Fully customisable to the building's design language",
        ],
        "safety": [
            "Toughened laminated glass that holds together if broken",
            "Automatic Rescue Device fitted as standard",
            "Overspeed governor and progressive safety gear",
            "Door sensors and interlocks on every landing",
            "Emergency alarm, intercom and battery-backed lighting",
        ],
    },
    {
        "slug": "hydraulic-elevators",
        "title": "Hydraulic Elevators",
        "short": "Ideal for low-rise buildings where no overhead machine room is possible.",
        "img": "1719463814218-52e17f720e8a",
        "alt": "An elevator with its doors open showing the lit cabin interior",
        "intro": [
            "Hydraulic elevators raise the car on a piston driven by a power pack, which means the machinery sits at the bottom of the shaft rather than above it. That makes them the practical answer for low-rise buildings, heritage structures and any site where you cannot build an overhead machine room or where the roof cannot take the load.",
            "They suit travel heights up to roughly six floors and are commonly used for home lifts, small commercial buildings and goods platforms.",
        ],
        "features": [
            "No overhead machine room or rooftop structure required",
            "Power pack located in a small room beside the shaft",
            "Suitable for travel heights up to approximately six floors",
            "Lower structural loading on the building",
            "Available in passenger, home and goods configurations",
            "Manual lowering facility during a power failure",
        ],
        "benefits": [
            "Fits buildings where a traction lift is structurally impossible",
            "Reduced civil cost — no machine room to construct",
            "Very smooth and quiet ride quality",
            "Simple mechanical design, straightforward to service",
            "Good load capacity relative to the shaft footprint",
        ],
        "safety": [
            "Pipe rupture valve stops descent if a hydraulic line fails",
            "Manual lowering to the nearest floor during a power cut",
            "Pressure relief valve guarding against overload",
            "Door interlocks at every landing",
            "Emergency stop, alarm and battery-backed cabin lighting",
        ],
    },
    {
        "slug": "elevator-amc",
        "title": "Elevator AMC",
        "short": "Annual Maintenance Contracts with scheduled visits and guaranteed response.",
        "img": "1562654501-9a587e8638d8",
        "alt": "Close-up of an elevator button panel showing floor numbers",
        "intro": [
            "An Annual Maintenance Contract keeps a lift safe, available and cheaper to own. Regular preventive attention catches worn ropes, drifting door timing and failing contactors before they become a breakdown with passengers inside.",
            "We offer two plans. Semi-comprehensive covers scheduled visits, labour and minor consumables. Comprehensive additionally covers major components such as controllers, door operators, ropes and drive units. Both include emergency response, and we service lifts of most makes, not only our own.",
        ],
        "features": [
            "Scheduled preventive maintenance visits through the year",
            "Semi-comprehensive and comprehensive plan options",
            "Emergency breakdown response included in every plan",
            "Written service report after each visit",
            "Genuine replacement parts",
            "Contracts available for lifts of other manufacturers",
        ],
        "benefits": [
            "Fewer breakdowns and far less unplanned downtime",
            "Predictable annual budget instead of surprise repair bills",
            "Extends the working life of the equipment",
            "Maintains ride quality and door performance over time",
            "Documented service history for building records and audits",
        ],
        "safety": [
            "Periodic testing of safety gear and overspeed governor",
            "Brake torque inspection and adjustment",
            "Rope condition and tension checks",
            "Door interlock and sensor verification",
            "ARD battery testing so it works when it is actually needed",
        ],
    },
    {
        "slug": "elevator-repair",
        "title": "Elevator Repair",
        "short": "Fault diagnosis and component-level repair for lifts of any make.",
        "img": "1581092918056-0c4c3acd3789",
        "alt": "Close-up of hands repairing an electronic circuit board",
        "intro": [
            "When a lift stops working the priority is an accurate diagnosis, not a guessed part replacement. Our engineers trace the actual fault — controller, drive, door operator, governor, levelling or wiring — and quote the repair before starting work.",
            "We repair lifts of most manufacturers. If a component is genuinely at the end of its life we will say so and set out the modernization option alongside the repair cost, so you can make the decision on real numbers.",
        ],
        "features": [
            "Fault diagnosis across all major elevator makes",
            "Controller and VVVF drive repair or replacement",
            "Door operator, lock and sensor repairs",
            "Levelling and positioning system correction",
            "Rope, brake and traction machine servicing",
            "Written quotation before work begins",
        ],
        "benefits": [
            "Correct diagnosis avoids paying for parts you do not need",
            "Lift returned to service quickly",
            "Honest advice on repair versus modernization",
            "Genuine replacement components",
            "Available whether or not you hold an AMC with us",
        ],
        "safety": [
            "Full safety-circuit verification before the lift is handed back",
            "Safety gear and governor tested after any related repair",
            "Door interlock testing on every landing",
            "Load and brake testing following major component work",
            "Lift kept locked out of service until testing is complete",
        ],
    },
    {
        "slug": "elevator-modernization",
        "title": "Elevator Modernization",
        "short": "Upgrade ageing lifts without replacing the entire installation.",
        "img": "1665285255745-f1d9453d109c",
        "alt": "Ornate brass elevator doors with decorative metalwork",
        "intro": [
            "An older lift is often structurally sound while its controller, drive and cabin are long past their useful life. Modernization replaces those parts and leaves the shaft, guide rails and structure in place — typically at a fraction of the cost of a full replacement and with far less disruption to the building.",
            "Typical upgrades include a VVVF drive to replace a two-speed motor, a modern microprocessor controller, automatic doors in place of manual collapsible gates, ARD, and a new cabin interior. In occupied buildings we phase the work one car at a time so the building is never left without a lift.",
        ],
        "features": [
            "VVVF drive retrofit for smoother travel and lower energy use",
            "Microprocessor controller replacement",
            "Automatic doors in place of manual collapsible gates",
            "Automatic Rescue Device installation",
            "New cabin interiors, flooring and lighting",
            "Updated landing fixtures and position indicators",
        ],
        "benefits": [
            "Substantially cheaper than a complete lift replacement",
            "Noticeably better ride comfort and door performance",
            "Lower running cost through modern drive technology",
            "Improved reliability and easier parts availability",
            "Phased execution keeps the building in service throughout",
        ],
        "safety": [
            "Brings older installations up to current safety expectations",
            "ARD added so passengers are not trapped during power cuts",
            "New door interlocks and full-height infrared sensors",
            "Replacement of worn ropes, brakes and governor components",
            "Complete load and safety testing before handover",
        ],
    },
    {
        "slug": "installation-services",
        "title": "Installation Services",
        "short": "Turnkey installation from shaft survey through to commissioning.",
        "img": "1525273177952-67455d25871f",
        "alt": "An elevator doorway in a building interior still under construction",
        "intro": [
            "We handle elevator installation as a single accountable scope. That begins with a site survey and shaft measurement, continues through structural coordination with your civil contractor, and ends with erection, wiring, commissioning and handover training for your building staff.",
            "Where the shaft has not yet been built we provide the dimensioned drawings your contractor needs, and we flag pit depth, headroom and power supply requirements early — these are the issues that most often delay a lift installation.",
        ],
        "features": [
            "Free site survey and shaft measurement",
            "General arrangement drawings for your civil contractor",
            "Structural and electrical coordination",
            "Fabrication of steel shaft structures where required",
            "Complete erection, wiring and commissioning",
            "Handover training for building maintenance staff",
        ],
        "benefits": [
            "One accountable party for the whole installation",
            "Civil requirements identified early, avoiding costly rework",
            "Committed schedule with regular progress updates",
            "Installation carried out by our own trained teams",
            "Direct transition into a maintenance plan at handover",
        ],
        "safety": [
            "Full load testing before the lift is put into service",
            "Safety gear and overspeed governor testing at commissioning",
            "Verification of every landing door interlock",
            "Earthing and electrical safety checks",
            "Site safety procedures followed throughout erection",
        ],
    },
    {
        "slug": "emergency-breakdown-service",
        "title": "Emergency Breakdown Service",
        "short": "24×7 response for trapped passengers and sudden lift failures.",
        "img": "1596711684682-2f3ea5d2d739",
        "alt": "Glass elevator shafts with several cars inside a tall atrium",
        "intro": [
            "A trapped passenger is an emergency and we treat it as one. Our breakdown line is answered at any hour, and trapped-passenger calls take priority over all other work.",
            "For buildings under an AMC with us, response windows are written into the agreement. We also attend emergency calls for buildings without a contract, subject to engineer availability in your area.",
        ],
        "features": [
            "Breakdown helpline answered 24 hours a day, every day",
            "Trapped-passenger calls prioritised above all other work",
            "Engineers covering Sehore, Bhopal, Indore and surrounding districts",
            "Safe manual rescue procedure carried out by trained staff",
            "On-the-spot fault diagnosis after passengers are released",
            "Response windows written into AMC agreements",
        ],
        "benefits": [
            "Passengers released quickly and safely",
            "Reduces the risk and liability of a prolonged entrapment",
            "Reassurance for residents, staff and visitors",
            "Same team that maintains the lift attends the breakdown",
            "Available to non-contract buildings as well",
        ],
        "safety": [
            "Rescue performed only by trained personnel using the correct procedure",
            "Main supply isolated and locked off before manual rescue",
            "Lift withdrawn from service until the fault is corrected",
            "Full safety-circuit check before the lift is returned to use",
            "Written incident and fault report after every callout",
        ],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# =====================================================================
#  GALLERY
# =====================================================================
GALLERY = [
    ("1592256410394-51c948ec13d5", "commercial", "Passenger Elevator",
     "Stainless steel doors and call panel in a building lobby", 700, 900),
    ("1699793982261-24c55bf385d5", "home", "Home Elevator",
     "Compact residential lift door on an upper landing", 700, 520),
    ("1585293878107-569e3ebdab53", "hospital", "Institutional Elevator",
     "Wide lift doors in a stone-clad lobby", 700, 820),
    ("1565417814737-6b4097de8a3a", "commercial", "Capsule Elevators",
     "Panoramic glass observation lifts on a building facade", 700, 560),
    ("1547630824-eed1be6a27b0", "industrial", "Elevator Car Interior",
     "Brushed steel cabin panelling", 700, 880),
    ("1719463814218-52e17f720e8a", "home", "Lift with Doors Open",
     "Lit cabin interior at a landing", 700, 540),
    ("1665285255745-f1d9453d109c", "commercial", "Modernization Work",
     "Restored decorative brass lift doors", 700, 860),
    ("1562654501-9a587e8638d8", "maintenance", "Control Panel",
     "Elevator button panel checked during a service visit", 700, 520),
    ("1596711684682-2f3ea5d2d739", "commercial", "Glass Shaft Installation",
     "Panoramic lift shafts in a tall atrium", 700, 780),
    ("1525273177952-67455d25871f", "industrial", "Installation in Progress",
     "Lift doorway during building fit-out", 700, 560),
    ("1581092918056-0c4c3acd3789", "maintenance", "Component Repair",
     "Circuit board level repair of lift electronics", 700, 840),
    ("1566096650255-98ba2641071e", "commercial", "Panoramic Lift Shaft",
     "View upward through a glass elevator shaft", 700, 600),
]

GALLERY_FILTERS = [
    ("all", "All Work"), ("home", "Home Lifts"), ("commercial", "Commercial"),
    ("hospital", "Hospital"), ("industrial", "Industrial"), ("maintenance", "Maintenance"),
]

# =====================================================================
#  TESTIMONIALS  (initials monograms — we do not have client photographs)
# =====================================================================
TESTIMONIALS = [
    ("Manoj Goyal", "Kurawar",
     "Excellent elevator installation and outstanding after-sales service. Highly recommended."),
    ("Mahesh Mundra", "Ashta",
     "Professional team, timely installation, and excellent maintenance support."),
    ("Kapil Agrawal", "Sehore",
     "Very satisfied with the quality and safety standards. Great experience."),
]

# =====================================================================
#  FAQ
# =====================================================================
FAQS = [
    ("How long has Sanskar Elevator been in business?",
     "We were established in 2000 and have more than 25 years of experience in elevator installation, "
     "maintenance and modernization. The company is led by our Managing Director, Mr. Mahendra Sahu."),
    ("Which areas do you cover?",
     "We serve customers across all of Madhya Pradesh. Our most frequent installations are in Bhopal, "
     "Indore, Sehore, Ashta, Kurawar, Vidisha and Khandwa, and we travel to other districts on request."),
    ("How long does an elevator installation take?",
     "A standard passenger elevator in a ready shaft usually takes around two to four weeks from delivery "
     "to handover. Home elevators are often complete in seven to ten working days. The main variable is "
     "civil readiness, which we assess during the free site visit."),
    ("What does an AMC cover?",
     "Semi-comprehensive AMC covers scheduled preventive visits, labour and minor consumables. "
     "Comprehensive AMC additionally covers major components such as controllers, door operators, ropes "
     "and drive units. Both plans include emergency breakdown response."),
    ("Do you service elevators made by other companies?",
     "Yes. We maintain, repair and modernize lifts of most major manufacturers. We normally begin with a "
     "site inspection, then propose either a maintenance plan or a modernization scope with clear pricing."),
    ("Can an elevator be added to a house that is already built?",
     "In most cases, yes. Our home elevators need a shallow pit, low headroom and a footprint from around "
     "1000 × 1000 mm, so they can usually be fitted into a stairwell void, courtyard or an external shaft "
     "without major structural changes."),
    ("What happens if the power goes out while the lift is moving?",
     "Our installations include an Automatic Rescue Device. On power failure the car automatically travels "
     "to the nearest floor and opens its doors, so passengers are not left waiting inside."),
    ("How quickly do you respond to a breakdown?",
     "Our helpline operates 24×7 and trapped-passenger calls take priority over all other work. Response "
     "times depend on your location and are written into AMC agreements."),
    ("Do you provide a quotation before starting work?",
     "Yes. We provide a written quotation after the site visit for installations, and before beginning any "
     "repair work. There is no charge for the initial site visit and estimate."),
]

WHY_US = [
    ("25+ Years Experience", "Established in 2000 and installing lifts across Madhya Pradesh ever since."),
    ("500+ Happy Clients", "Homes, hospitals, factories and commercial buildings throughout the state."),
    ("Expert Engineers", "Trained technicians who handle installation and servicing in-house."),
    ("Affordable Pricing", "Transparent quotations with no hidden charges added later."),
    ("Genuine Parts", "Authentic components only — we do not fit refurbished spares."),
    ("Safety First", "ARD, overload sensing and governor safety gear on every installation."),
    ("Quick Installation", "Committed timelines with regular updates on progress."),
    ("Fast Service Support", "Local engineers who reach site quickly when you need them."),
    ("24×7 Assistance", "Breakdown helpline answered at any hour, every day of the year."),
    ("All Madhya Pradesh", "Service coverage across the entire state, not just the major cities."),
]

PROCESS = [
    ("Consultation", "We discuss your building, traffic and budget, then recommend a configuration."),
    ("Site Visit", "Our engineer measures the shaft, pit and headroom, and flags any civil work needed."),
    ("Quotation", "You receive a written quotation with the specification and timeline set out clearly."),
    ("Installation", "Our own team erects, wires and commissions the lift to the agreed schedule."),
    ("Testing", "Load, brake, levelling and safety-gear testing before the lift is handed over."),
    ("Maintenance", "Handover into an AMC plan with scheduled visits and 24×7 breakdown cover."),
]

# =====================================================================
#  PARTIALS
# =====================================================================
NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("testimonials.html", "Testimonials"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]


def rel(depth, path):
    """Resolve a root-relative path for a page nested `depth` levels deep."""
    return ("../" * depth) + path


def head(page, depth):
    """<head> block. `page` supplies title, desc, slug/canonical and og image."""
    canon = SITE["domain"] + "/" + page["url"]
    og_img = page.get("og") or img("1592256410394-51c948ec13d5", 1200, 630)
    a = lambda p: rel(depth, p)

    schema = ""
    if page.get("schema"):
        schema = '<script type="application/ld+json">%s</script>' % page["schema"]

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0F172A">

<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<meta name="author" content="{SITE['name']}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<meta name="geo.region" content="IN-MP">
<meta name="geo.placename" content="Sehore, Madhya Pradesh">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{SITE['name']} — {SITE['tagline']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['desc']}">
<meta name="twitter:image" content="{og_img}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&display=swap" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&display=swap"></noscript>

<link rel="stylesheet" href="{a('assets/css/style.css')}">
<link rel="icon" href="{a('assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{a('assets/img/favicon.svg')}">
{schema}
</head>
<body>"""


def local_business_schema():
    services_list = ",".join(
        '{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s"}}' % s["title"]
        for s in SERVICES
    )
    areas = ",".join('{"@type":"City","name":"%s"}' % c for c in CITIES)
    return ("""{"@context":"https://schema.org","@type":"LocalBusiness",
"@id":"%(domain)s/#business","name":"%(name)s",
"description":"Elevator installation, maintenance, modernization and repair services across Madhya Pradesh. Established in %(est)s.",
"url":"%(domain)s/","telephone":"%(p1)s","email":"%(email)s",
"foundingDate":"%(est)s",
"founder":{"@type":"Person","name":"%(md)s"},
"address":{"@type":"PostalAddress","streetAddress":"Anjani Dham Colony, Sekdhakedi Road",
"addressLocality":"Sehore","addressRegion":"Madhya Pradesh","postalCode":"466001","addressCountry":"IN"},
"areaServed":[%(areas)s,{"@type":"State","name":"Madhya Pradesh"}],
"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
"opens":"09:00","closes":"19:00"}],
"hasOfferCatalog":{"@type":"OfferCatalog","name":"Elevator Services","itemListElement":[%(svc)s]}}"""
            % {"domain": SITE["domain"], "name": SITE["name"], "est": SITE["established"],
               "p1": SITE["phone1_raw"], "email": SITE["email"], "md": SITE["md"],
               "areas": areas, "svc": services_list}).replace("\n", "")


def header(active, depth):
    a = lambda p: rel(depth, p)
    links = []
    for href, label in NAV:
        cls = "nav__link is-active" if href == active else "nav__link"
        aria = ' aria-current="page"' if href == active else ""
        if label == "Services":
            items = "".join(
                f'<li><a href="{a("services/" + s["slug"] + ".html")}">{s["title"]}</a></li>'
                for s in SERVICES
            )
            links.append(
                f'<li class="has-sub">'
                f'<a class="{cls}" href="{a(href)}"{aria}>Services'
                f'<svg class="caret" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></a>'
                f'<button class="sub-toggle" type="button" aria-expanded="false" aria-label="Show services menu"></button>'
                f'<ul class="submenu">{items}</ul></li>'
            )
        else:
            links.append(f'<li><a class="{cls}" href="{a(href)}"{aria}>{label}</a></li>')

    return f"""
<div class="scroll-progress" id="scrollProgress" role="presentation"></div>
<a class="skip-link" href="#main">Skip to main content</a>

<header class="header" id="header">
  <div class="container header__inner">
    <a href="{a('index.html')}" class="logo" aria-label="{SITE['name']} — home">
      <svg class="logo__mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
        <rect x="2" y="2" width="36" height="36" rx="9" fill="#D4AF37"/>
        <path d="M20 10l5 6h-10l5-6zM20 30l-5-6h10l-5 6z" fill="#0F172A"/>
        <rect x="12" y="18.6" width="16" height="2.8" rx="1.4" fill="#0F172A" opacity=".55"/>
      </svg>
      <span class="logo__text">Sanskar<strong>Elevator</strong></span>
    </a>

    <nav class="nav" id="nav" aria-label="Main navigation">
      <ul class="nav__list">{''.join(links)}</ul>
    </nav>

    <div class="header__actions">
      <a class="header__phone" href="tel:{SITE['phone1_raw']}" aria-label="Call {SITE['phone1']}">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>
        <span>{SITE['phone1']}</span>
      </a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Switch to dark mode" title="Toggle dark mode">
        <svg class="icon icon--sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8L6 18M18 6l1.8-1.8"/></svg>
        <svg class="icon icon--moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.3A8.5 8.5 0 019.7 3.5a8.5 8.5 0 1010.8 10.8z"/></svg>
      </button>
      <a class="btn btn--gold btn--sm header__cta" href="{a('contact.html')}">Get Free Quote</a>
      <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="nav-overlay" id="navOverlay" hidden></div>
"""


def cta_banner(depth):
    a = lambda p: rel(depth, p)
    return f"""
<section class="cta-banner" aria-labelledby="ctaHeading">
  <div class="container cta-banner__inner">
    <div>
      <h2 id="ctaHeading">Planning a lift for your building?</h2>
      <p>Free site visit and written quotation across Madhya Pradesh. Talk to our engineers today.</p>
    </div>
    <div class="cta-banner__actions">
      <a class="btn btn--gold" href="tel:{SITE['phone1_raw']}">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>
        {SITE['phone1']}
      </a>
      <a class="btn btn--ghost" href="{a('contact.html')}">Send an Enquiry</a>
    </div>
  </div>
</section>
"""


def footer(depth):
    a = lambda p: rel(depth, p)
    quick = "".join(f'<li><a href="{a(h)}">{l}</a></li>' for h, l in NAV)
    quick += f'<li><a href="{a("privacy-policy.html")}">Privacy Policy</a></li>'
    quick += f'<li><a href="{a("terms-conditions.html")}">Terms &amp; Conditions</a></li>'
    svc = "".join(
        f'<li><a href="{a("services/" + s["slug"] + ".html")}">{s["title"]}</a></li>'
        for s in SERVICES[:8]
    )
    addr = "<br>".join(SITE["addr_lines"])

    return f"""
<footer class="footer">
  <div class="container footer__grid">
    <div class="footer__col footer__col--brand">
      <a href="{a('index.html')}" class="logo logo--footer">
        <svg class="logo__mark" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="9" fill="#D4AF37"/><path d="M20 10l5 6h-10l5-6zM20 30l-5-6h10l-5 6z" fill="#0F172A"/><rect x="12" y="18.6" width="16" height="2.8" rx="1.4" fill="#0F172A" opacity=".55"/></svg>
        <span class="logo__text">Sanskar<strong>Elevator</strong></span>
      </a>
      <p>Established in {SITE['established']}. More than {SITE['years']} years installing, maintaining and
      modernizing elevators for homes, hospitals, factories and commercial buildings across Madhya Pradesh.</p>
      <p class="footer__md"><strong>Managing Director:</strong> {SITE['md']}</p>
      <ul class="social" aria-label="Social media">
        <li><a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1z"/></svg></a></li>
        <li><a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></svg></a></li>
        <li><a href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.1-.2 0-.4.1-.5l.4-.5c.1-.2.1-.3 0-.5l-.7-1.7c-.2-.4-.4-.4-.5-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.9 11.9 0 004.6 4 5 5 0 002.3.4 2.7 2.7 0 001.8-1.3 2.2 2.2 0 00.2-1.3c-.1-.1-.2-.2-.4-.3z"/></svg></a></li>
      </ul>
    </div>

    <nav class="footer__col" aria-label="Quick links">
      <h2>Quick Links</h2>
      <ul>{quick}</ul>
    </nav>

    <nav class="footer__col" aria-label="Services">
      <h2>Services</h2>
      <ul>{svc}<li><a href="{a('services.html')}"><strong>View all services →</strong></a></li></ul>
    </nav>

    <div class="footer__col">
      <h2>Contact</h2>
      <address class="footer__contact">
        <p>{addr}</p>
        <p><a href="tel:{SITE['phone1_raw']}">{SITE['phone1']}</a><br>
           <a href="tel:{SITE['phone2_raw']}">{SITE['phone2']}</a></p>
        <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
        <p>{SITE['hours']}</p>
      </address>
      <div class="footer__map">
        <iframe title="{SITE['name']} location map"
          src="https://maps.google.com/maps?q=Anjani%20Dham%20Colony%2C%20Sehore%2C%20Madhya%20Pradesh%20466001&z=14&output=embed"
          width="100%" height="160" style="border:0" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>

  <div class="container footer__bottom">
    <p>&copy; {SITE['year']} {SITE['name']}. All Rights Reserved.</p>
    <p><a href="{a('privacy-policy.html')}">Privacy Policy</a> &middot;
       <a href="{a('terms-conditions.html')}">Terms &amp; Conditions</a></p>
  </div>
</footer>
"""


def floating(depth):
    a = lambda p: rel(depth, p)
    return f"""
<a class="fab fab--whatsapp" href="https://wa.me/{SITE['whatsapp']}?text=Hello%20Sanskar%20Elevator%2C%20I%20would%20like%20a%20quotation."
   target="_blank" rel="noopener noreferrer" aria-label="Chat with us on WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.1-.2 0-.4.1-.5l.4-.5c.1-.2.1-.3 0-.5l-.7-1.7c-.2-.4-.4-.4-.5-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.9 11.9 0 004.6 4 5 5 0 002.3.4 2.7 2.7 0 001.8-1.3 2.2 2.2 0 00.2-1.3c-.1-.1-.2-.2-.4-.3z"/></svg>
</a>
<a class="fab fab--call" href="tel:{SITE['phone1_raw']}" aria-label="Call {SITE['phone1']}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>
</a>
<button class="fab fab--top" id="backToTop" type="button" aria-label="Back to top">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>
</button>

<div class="cookie" id="cookieBar" role="region" aria-label="Cookie notice" hidden>
  <p>This website uses cookies to improve your browsing experience. See our
     <a href="{a('privacy-policy.html')}">Privacy Policy</a>.</p>
  <div class="cookie__actions">
    <button class="btn btn--ghost btn--sm" id="cookieDecline" type="button">Decline</button>
    <button class="btn btn--gold btn--sm" id="cookieAccept" type="button">Accept</button>
  </div>
</div>

<script src="{a('assets/js/main.js')}" defer></script>
</body>
</html>"""


def page_banner(title, subtitle, crumbs, depth, pid="1545558014-8692077e9b5c"):
    """Compact hero used on every inner page."""
    a = lambda p: rel(depth, p)
    trail = f'<a href="{a("index.html")}">Home</a>'
    for label, href in crumbs[:-1]:
        trail += f' <span aria-hidden="true">/</span> <a href="{a(href)}">{label}</a>'
    trail += f' <span aria-hidden="true">/</span> <span aria-current="page">{crumbs[-1][0]}</span>'

    return f"""
<section class="banner">
  <img class="banner__bg" src="{img(pid, 1600, 600)}"
       srcset="{img(pid, 800, 300)} 800w, {img(pid, 1600, 600)} 1600w, {img(pid, 2400, 900)} 2400w"
       sizes="100vw" alt="" width="1600" height="600" fetchpriority="high" decoding="async">
  <div class="banner__overlay" aria-hidden="true"></div>
  <div class="container banner__inner">
    <nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
</section>
"""


def service_areas_section(depth):
    a = lambda p: rel(depth, p)
    chips = "".join(f'<li>{c}</li>' for c in CITIES)
    return f"""
<section class="section section--alt" id="service-areas">
  <div class="container">
    <header class="section__head">
      <p class="eyebrow reveal">Service Areas</p>
      <h2 class="reveal">Serving all of Madhya Pradesh</h2>
      <p class="section__lead reveal">We provide elevator installation, maintenance, modernization and
      repair services throughout Madhya Pradesh. These are the cities we work in most often — contact us
      for any other district in the state.</p>
    </header>
    <ul class="chips reveal">{chips}</ul>
    <p class="chips__note reveal">Services available across <strong>all of Madhya Pradesh</strong>.
       <a class="link-arrow" href="{a('contact.html')}">Check availability in your area <span aria-hidden="true">→</span></a></p>
  </div>
</section>
"""


def emergency_section():
    return f"""
<section class="emergency" aria-labelledby="emergencyHeading">
  <div class="container emergency__inner">
    <span class="emergency__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24"><path d="M13 2L4.5 13H12l-1 9 8.5-11H12z"/></svg>
    </span>
    <div class="emergency__text">
      <h2 id="emergencyHeading">Lift breakdown or trapped passenger?</h2>
      <p>Our emergency helpline is answered 24 hours a day, every day. Trapped-passenger
         calls take priority over all other work.</p>
    </div>
    <div class="emergency__actions">
      <a class="btn btn--gold" href="tel:{SITE['phone1_raw']}">Call {SITE['phone1']}</a>
      <a class="btn btn--ghost" href="tel:{SITE['phone2_raw']}">Call {SITE['phone2']}</a>
    </div>
  </div>
</section>
"""


def enquiry_form(form_id="enquiryForm"):
    opts = "".join(f"<option>{s['title']}</option>" for s in SERVICES)
    city_opts = "".join(f"<option>{c}</option>" for c in CITIES)
    return f"""
<form class="card contact__form" id="{form_id}" novalidate>
  <div class="field-row">
    <div class="field">
      <label for="f-name">Name <span aria-hidden="true">*</span></label>
      <input type="text" id="f-name" name="name" required minlength="2" autocomplete="name" placeholder="Your full name">
      <small class="error" data-error-for="f-name"></small>
    </div>
    <div class="field">
      <label for="f-phone">Phone Number <span aria-hidden="true">*</span></label>
      <input type="tel" id="f-phone" name="phone" required pattern="[0-9+\\-\\s()]{{10,18}}" autocomplete="tel" placeholder="+91 00000 00000">
      <small class="error" data-error-for="f-phone"></small>
    </div>
  </div>
  <div class="field-row">
    <div class="field">
      <label for="f-email">Email</label>
      <input type="email" id="f-email" name="email" autocomplete="email" placeholder="you@example.com">
      <small class="error" data-error-for="f-email"></small>
    </div>
    <div class="field">
      <label for="f-city">City <span aria-hidden="true">*</span></label>
      <input type="text" id="f-city" name="city" required minlength="2" list="cityList" placeholder="Your city">
      <datalist id="cityList">{city_opts}</datalist>
      <small class="error" data-error-for="f-city"></small>
    </div>
  </div>
  <div class="field">
    <label for="f-service">Service Required</label>
    <select id="f-service" name="service">{opts}<option>Other Enquiry</option></select>
  </div>
  <div class="field">
    <label for="f-message">Message <span aria-hidden="true">*</span></label>
    <textarea id="f-message" name="message" rows="4" required minlength="10"
      placeholder="Building type, number of floors, capacity required, and any other details."></textarea>
    <small class="error" data-error-for="f-message"></small>
  </div>
  <button class="btn btn--gold btn--block" type="submit">
    Send Enquiry
    <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
  </button>
  <p class="form-status" id="{form_id}Status" role="status" aria-live="polite"></p>
</form>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path
