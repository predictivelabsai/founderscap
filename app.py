"""
Founders Capital — multipage FastHTML landing site.

Founder-led European VC: fintech roots → sovereign AI, defense, health, energy.
Content lives in content/*.py; routes are thin composition over components.py.
"""

from fasthtml.common import (
    fast_app, serve, Div, Span, A, P, Ul, Li, Section, Article, Header, Table,
    Thead, Tbody, Tr, Th, Td, NotStr, Script, Style, H1, H2, H3, H4, Button,
)

from components import (
    page, Hero, Pillar, MetricTile, CaseStudyCard, PortfolioCard, CTASection,
    NewsSection, Section_, Heading, Eyebrow, Pill, Button_, SectorLink,
    CONTACT_EMAIL, LINKEDIN_URL,
)
from content.case_studies import FOUNDER_CASES, FOUNDER_SUMMARY
from content.portfolio import PORTFOLIO
from content.team import TEAM
from content import signal as signal_mod
from content import news as news_mod

news_mod.start_background_refresh()


app, rt = fast_app(live=False, static_path=".", pico=False)


# ---------- /  Home ----------

@rt("/")
def home():
    pillars = [
        ("01", "Sovereign AI platforms", "Capital and operator support for founders building European alternatives in AI compute, foundation models, agent runtimes and data infrastructure."),
        ("02", "Defense & dual-use", "Sensors, autonomy, situation pictures, secure comms, and the dual-use software that European forces and critical-infrastructure operators will procure this decade."),
        ("03", "Health & life sciences", "Clinician-safe AI across real-world evidence, hospital operations, diagnostics and mental wellness — privacy-preserving by construction."),
        ("04", "Energy & resilience", "Grid intelligence, industrial decarbonisation, and resilience software for a continent reshaping its energy mix under geopolitical pressure."),
    ]

    home_portfolio = PORTFOLIO[:6]

    return page(
        "European sovereign-AI capital",
        "/",
        Hero(),

        # Portfolio strip
        Section_(
            Div(
                Eyebrow("Portfolio"),
                Heading(2, "A founder-led portfolio, built company by company.", cls="mt-4 max-w-3xl"),
                P(
                    "From European FinTech marketplaces that cumulatively deployed over €2.5B, through to the sovereign-AI, defense, health and energy platforms that Europe is now building.",
                    cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed",
                ),
                cls="mb-14",
            ),
            Div(
                *[PortfolioCard(p) for p in home_portfolio],
                cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
            Div(
                Button_("See the full portfolio", href="/portfolio", primary=False),
                cls="mt-10",
            ),
            cls="border-b border-line",
        ),

        # Thesis pillars
        Section_(
            Div(
                Eyebrow("Thesis"),
                Heading(2, "Four sectors Europe has to own.", cls="mt-4 max-w-4xl"),
                P(
                    "The sovereign-AI moment is not a UK phenomenon — it is a European one. Founders Capital backs the founders building the compute, the models, the operational software and the infrastructure that Europe cannot buy in.",
                    cls="mt-5 text-ink-muted text-lg max-w-3xl",
                ),
                cls="mb-14",
            ),
            Div(
                *[Pillar(n, t, b) for n, t, b in pillars],
                cls="grid md:grid-cols-2 lg:grid-cols-4 gap-5",
            ),
        ),

        # Sector focus
        Section_(
            Div(
                Eyebrow("Where we invest"),
                Heading(2, "Four programme sectors, one commercial root.", cls="mt-4 max-w-4xl"),
                cls="mb-14",
            ),
            Div(
                _sector_link("Sovereign & defense AI", "Decision support, autonomy and dual-use software for European defense and critical-infrastructure operators — with clear boundaries between AI assistance and human authority.", "/sectors/defense"),
                _sector_link("Health & life sciences", "Real-world evidence, hospital operations, clinical documentation and mental wellness — privacy-preserving pipelines built for EU regulation.", "/sectors/healthcare"),
                _sector_link("Energy & resilience", "Grid intelligence, industrial decarbonisation and resilience software for a continent reshaping its energy mix.", "/sectors/energy"),
                _sector_link("Financial services", "Our commercial root — the marketplace-lending and regulated-finance thesis that seeded Founders Capital. Now a disciplined adjacency.", "/sectors/financial"),
                cls="grid md:grid-cols-2 gap-5",
            ),
            cls="border-y border-line bg-bg-elevated/40",
        ),

        # Case-study strip
        Section_(
            Div(
                Eyebrow("Case studies"),
                Heading(2, "Founder precedents.", cls="mt-4 max-w-3xl"),
                P("Three European FinTech marketplaces we co-founded — the track record that anchors how we operate with founders today.",
                  cls="mt-5 text-ink-muted text-lg max-w-2xl leading-relaxed"),
                cls="mb-14 flex flex-col md:flex-row md:items-end md:justify-between gap-4",
            ),
            Div(
                *[CaseStudyCard(c, compact=True) for c in FOUNDER_CASES],
                cls="grid md:grid-cols-3 gap-5",
            ),
            Div(
                Button_("Read the full case studies", href="/case-studies", primary=False),
                cls="mt-10",
            ),
        ),

        # Signal teaser
        Section_(
            Div(
                Div(
                    Eyebrow("Signal"),
                    Heading(2, "We read the data our sectors run on — every day.", cls="mt-4 max-w-3xl"),
                    P(
                        "A live view of European public data: NHS waiting lists, NATO ",
                        SectorLink("defence"), " spend, ",
                        SectorLink("energy"), " mix, AI readiness and education outcomes — the canvases the sovereign-AI thesis runs against.",
                        cls="mt-5 text-ink-muted text-lg max-w-2xl leading-relaxed",
                    ),
                    Button_("Open Signal", href="/signal", primary=True, cls="mt-8"),
                    cls="md:w-2/5",
                ),
                Div(
                    Div(id="signal-teaser", cls="w-full h-[360px]"),
                    cls="md:w-3/5 p-3 rounded-2xl bg-bg-elevated border border-line",
                ),
                cls="flex flex-col md:flex-row gap-10 items-stretch",
            ),
            cls="border-y border-line",
        ),

        NewsSection(
            category="home",
            title="What's moving in European sovereign AI.",
            subtitle="A rolling mix of AI, defense, health, energy and FinTech funding and policy news from public VC and sector feeds. Refreshed hourly.",
        ),

        CTASection(),

        body_extra=[
            Script(src="https://cdn.plot.ly/plotly-2.35.2.min.js"),
            Script(NotStr(f"window.PLOTLY_TEASER = {_teaser_json()};")),
            Script(src="/static/signal.js"),
            Script(src="/static/three-hero.js", type="module"),
        ],
    )


def _sector_link(title, body, href):
    return A(
        Div(
            Div(
                Span(title, cls="text-ink text-xl font-medium tracking-tight"),
                Span("→", cls="text-accent text-xl ml-auto"),
                cls="flex items-center mb-3",
            ),
            P(body, cls="text-ink-muted text-sm leading-relaxed"),
            cls="p-7 rounded-2xl border border-line bg-bg-elevated hover:border-accent/50 hover:bg-bg-raised transition-all",
        ),
        href=href,
        cls="block",
    )


def _teaser_json():
    import json
    from content import signal as s
    nhs, _ = s.nhs_charts()
    nhs["layout"]["title"]["text"] = "NHS England waiting list · treemap by specialty"
    nhs["layout"]["margin"] = {"l": 0, "r": 0, "t": 30, "b": 0}
    return json.dumps(nhs)


# ---------- /thesis ----------

@rt("/thesis")
def thesis():
    pillars = [
        ("01", "Sovereign AI platforms", "Back the European founders building compute, foundation models, agent runtimes, data layers, evaluation harnesses and enterprise AI infrastructure. Europe cannot buy sovereignty — it has to build it."),
        ("02", "Defense & dual-use", "The decade ahead is defined by European re-armament and critical-infrastructure resilience. We invest in the sensors, autonomy, situation-picture and dual-use software that forces and operators will procure this cycle."),
        ("03", "Health & life sciences", "Real-world evidence, hospital operations, clinical documentation, diagnostics and mental wellness — built under GDPR and the EU AI Act, with clinicians in authority."),
        ("04", "Energy & resilience", "Grid intelligence, industrial decarbonisation and operational-resilience software for a continent reshaping its energy mix under geopolitical pressure."),
    ]

    commitments = [
        ("Operator-first capital", "Every cheque comes with founder-to-founder support. We have lived the seed → Series A journey; we help portfolio teams price, govern and hire through it."),
        ("European at the core", "We build the firm from London and operate across the EU. Most of the portfolio is EU-headquartered, and market introductions are a first-order service we provide."),
        ("Sovereign by design", "Our companies run in European data centres where the law requires it, and on infrastructure that founders own. Sovereignty is an architectural choice, not a branding one."),
        ("Disciplined governance", "Pre-seed to Series A. Clean cap tables, aligned incentives, founder-friendly terms — and clear board practice from day one."),
    ]

    return page(
        "Thesis",
        "/thesis",
        Section_(
            Eyebrow("Thesis"),
            Heading(1, "Europe's sovereign-AI decade, backed by founders who have built in Europe.", cls="mt-5 max-w-5xl"),
            P(
                "A nation state — the United Kingdom — has joined the venture market as a sovereign investor, with up to £20M cheques and 1M GPU-hours for AI founders. Founders Capital takes that signal as confirmation of a much wider European thesis: that ",
                SectorLink("sovereign AI"), ", ",
                SectorLink("defense"), ", ",
                SectorLink("health"), " and ",
                SectorLink("energy"),
                " software are the four categories Europe has to own — and that the founders who will build them need operator-grade capital, not passive cheques.",
                cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow("Four pillars"),
                Heading(2, "Where the cheques go.", cls="mt-4"),
                cls="mb-14",
            ),
            Div(*[_thesis_row(n, t, b) for n, t, b in pillars], cls="divide-y divide-line border-y border-line"),
        ),
        Section_(
            Div(
                Eyebrow("How we operate"),
                Heading(2, "Four commitments to founders.", cls="mt-4 max-w-4xl"),
                cls="mb-14",
            ),
            Div(
                *[Div(
                    Heading(3, title, cls="mb-2"),
                    P(body, cls="text-ink-muted text-sm leading-relaxed"),
                    cls="p-7 rounded-2xl bg-bg-elevated border border-line",
                ) for title, body in commitments],
                cls="grid md:grid-cols-2 gap-5",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        CTASection(),
        body_extra=[Script(src="/static/three-hero.js", type="module")],
    )


def _thesis_row(number, title, body):
    return Div(
        Div(
            Div(number, cls="font-mono text-xs tracking-widest text-accent"),
            cls="md:w-24 shrink-0",
        ),
        Div(
            Heading(3, title, cls="mb-3"),
            P(body, cls="text-ink-muted leading-relaxed"),
            cls="flex-1",
        ),
        cls="flex flex-col md:flex-row gap-6 py-10",
    )


# ---------- /sectors/* ----------

SECTORS = {
    "defense": {
        "title": "Sovereign & defense AI",
        "eyebrow": "Sovereign & defense AI",
        "headline": "A European defense-tech decade, now a category in its own right.",
        "lede": "We back founders building the sensors, autonomy, situation pictures, secure comms and dual-use software that European forces, NATO operators and critical-infrastructure bodies will procure this decade.",
        "pillars": [
            ("Sensors & autonomy", "UAV, counter-UAV and maritime autonomy platforms — built on European compute and European ground stations."),
            ("Situation pictures & OSINT", "Operational views fusing sensor data, satellite imagery and open-source intelligence for defense and critical-infrastructure operators."),
            ("Dual-use software", "Cyber, secure comms and AI-infrastructure plays that serve defense, critical-infrastructure and commercial buyers from the same stack."),
        ],
        "register": ["Sovereign deployment", "Dual-use friendly", "EU data residency"],
    },
    "healthcare": {
        "title": "Health & life sciences",
        "eyebrow": "Health & life sciences",
        "headline": "Clinical-grade AI with patient data treated as such.",
        "lede": "Real-world evidence, hospital operations, clinical documentation, diagnostics and mental wellness — on privacy-preserving, regulatory-grade pipelines, under the EU AI Act.",
        "pillars": [
            ("Real-world evidence", "Pipelines over inpatient records, dispensing data and registries — with protocol templates that compress follow-up cycles."),
            ("Hospital operations", "Elective-recovery forecasting, capacity planning and clinical-workflow automation for national hospital systems."),
            ("Mental wellness & access", "Conversational AI for mental health, clinician-supervised, multilingual and privacy-first."),
        ],
        "register": ["GDPR-native", "EU AI Act readiness", "Clinician in authority"],
    },
    "energy": {
        "title": "Energy & resilience",
        "eyebrow": "Energy & resilience",
        "headline": "A continent rebuilding its energy system — software-first.",
        "lede": "Grid intelligence, industrial decarbonisation, supply-chain resilience and operational software for the European energy transition.",
        "pillars": [
            ("Grid & flexibility", "Forecasting, balancing and flexibility software for European TSOs, DSOs and industrial consumers."),
            ("Industrial decarbonisation", "Measurement, reporting and optimisation software for heavy industry on a Net Zero trajectory."),
            ("Resilience & supply chain", "Software that measures, scores and hardens the energy and critical-materials supply chain across Europe."),
        ],
        "register": ["Net Zero aligned", "Operator-deployed", "Sovereign infrastructure"],
    },
    "financial": {
        "title": "Financial services",
        "eyebrow": "Financial services",
        "headline": "Our commercial root — marketplace lending and regulated FinTech.",
        "lede": "Founders Capital has its operating roots in European FinTech. We co-founded Bondora, EstateGuru and Investly — three of the leading VC-backed European lending marketplaces. Financial services remains a disciplined adjacency on the fund.",
        "pillars": [
            ("Marketplace lending", "Consumer credit, property bridge and SME invoice finance — the product lineage that built the firm."),
            ("AI in regulated finance", "Underwriting, monitoring, compliance and document intelligence for regulated European institutions."),
            ("Alternative assets", "AI-native infrastructure for private credit, venture and alternative-asset allocators."),
        ],
        "register": ["Regulated finance", "Marketplace DNA", "EU/UK distribution"],
    },
}


SECTOR_NEWS = {
    "defense": ("defense", "Defence-tech and sovereign-security signal.", "Latest from NATO, European Defence Fund, defense-tech funding and dual-use deployments."),
    "healthcare": ("healthcare", "Health and life-sciences signal.", "Digital-health funding across Europe, EHDS rollout, and life-sciences AI developments."),
    "energy": ("energy", "Energy and resilience signal.", "Climate-tech funding, grid-intelligence announcements and European energy-security news."),
    "financial": ("financial", "Financial-services signal.", "European FinTech funding, regulated-AI deployment and open-banking-era infrastructure."),
}


def _sector_page(slug):
    s = SECTORS[slug]
    news_key, news_title, news_sub = SECTOR_NEWS[slug]

    return page(
        s["title"],
        f"/sectors/{slug}",
        Section_(
            Eyebrow(s["eyebrow"]),
            Heading(1, s["headline"], cls="mt-5 max-w-5xl"),
            P(s["lede"], cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            Div(
                *[Pill(r) for r in s["register"]],
                cls="mt-10 flex flex-wrap gap-2",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow("Where we focus"),
                Heading(2, "Three focal points in this sector.", cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[Pillar(f"0{i+1}", t, b) for i, (t, b) in enumerate(s["pillars"])],
                cls="grid md:grid-cols-3 gap-5",
            ),
        ),
        NewsSection(category=news_key, title=news_title, subtitle=news_sub),
        CTASection(),
    )


@rt("/sectors/defense")
def sec_defense():
    return _sector_page("defense")


@rt("/sectors/healthcare")
def sec_health():
    return _sector_page("healthcare")


@rt("/sectors/energy")
def sec_energy():
    return _sector_page("energy")


@rt("/sectors/financial")
def sec_financial():
    return _sector_page("financial")


# ---------- /portfolio ----------

@rt("/portfolio")
def portfolio():
    return page(
        "Portfolio",
        "/portfolio",
        Section_(
            Eyebrow("Portfolio"),
            Heading(1, "Nine companies across four European sectors.", cls="mt-5 max-w-4xl"),
            P("From European FinTech marketplaces — Bondora, EstateGuru, Investly — that cumulatively deployed over €2.5B, through to the sovereign-AI, defense, health and energy platforms Europe is now building.",
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                *[PortfolioCard(p) for p in PORTFOLIO],
                cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
        ),
        NewsSection(
            category="ai",
            title="Portfolio-adjacent AI signal.",
            subtitle="Sector trends from public VC and AI sources.",
        ),
        CTASection(),
    )


# ---------- /case-studies ----------

@rt("/case-studies")
def case_studies():
    return page(
        "Case studies",
        "/case-studies",
        Section_(
            Eyebrow("Case studies"),
            Heading(1, "Three founder precedents that built the firm.", cls="mt-5 max-w-4xl"),
            P("The operating history behind Founders Capital — three European FinTech marketplaces co-founded from small cheques, collectively deploying over €2.5B. These are the engagements that shape how we back founders today.",
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow("At a glance"),
                Heading(2, "Initial cheques → reference valuations.", cls="mt-4 max-w-3xl"),
                cls="mb-10",
            ),
            Div(
                _summary_table(FOUNDER_SUMMARY),
                cls="overflow-x-auto",
            ),
            P(
                "Valuations are reference marks for narrative purposes; Founders Capital and its partners do not represent that any specific return has been realised or is available to new investors.",
                cls="mt-5 text-ink-dim text-xs italic max-w-3xl",
            ),
            cls="border-b border-line",
        ),
        Section_(
            Div(
                Eyebrow("Deep dives"),
                Heading(2, "Each case, in the founder's voice.", cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[CaseStudyCard(c) for c in FOUNDER_CASES],
                cls="grid md:grid-cols-3 gap-5",
            ),
        ),
        CTASection(),
    )


def _summary_table(rows):
    header = Thead(
        Tr(
            Th("Company", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
            Th("Founded", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
            Th("Initial cheque", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
            Th("Reference valuation (2026)", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
            Th("Multiple", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
            Th("Cumulative growth", cls="text-left py-3 pr-6 text-xs font-mono tracking-widest uppercase text-ink-muted"),
        ),
    )
    body_rows = []
    for r in rows:
        body_rows.append(
            Tr(
                Td(
                    A(r["company"], href=r["url"], target="_blank", cls="text-ink hover:text-accent font-medium"),
                    Div(r["note"], cls="text-ink-dim text-xs mt-1"),
                    cls="py-4 pr-6 align-top",
                ),
                Td(str(r["founded"]), cls="py-4 pr-6 text-ink-muted text-sm align-top"),
                Td(r["initial"], cls="py-4 pr-6 text-ink-muted text-sm align-top"),
                Td(r["valuation"], cls="py-4 pr-6 text-ink-muted text-sm align-top"),
                Td(r["multiple"], cls="py-4 pr-6 text-accent text-sm font-mono align-top"),
                Td(r["growth"], cls="py-4 pr-6 text-ink-muted text-sm font-mono align-top"),
                cls="border-t border-line",
            )
        )
    return Table(header, Tbody(*body_rows), cls="min-w-full text-sm")


# ---------- /signal ----------

@rt("/signal")
def signal():
    charts = signal_mod.all_charts()
    tabs = []
    panels = []
    for key, block in charts.items():
        tabs.append(
            Button(
                block["title"],
                type="button",
                cls="signal-tab",
                **{"data-signal-tab": key},
            )
        )
        panels.append(
            Div(
                Div(
                    Eyebrow(block["eyebrow"]),
                    Heading(2, block["title"], cls="mt-4"),
                    P(block["summary"], cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed"),
                    cls="mb-10",
                ),
                Div(
                    Div(
                        Div(id=f"chart-{key}-primary", cls="w-full"),
                        cls="chart-frame md:col-span-2",
                    ),
                    Div(
                        Div(id=f"chart-{key}-secondary", cls="w-full"),
                        cls="chart-frame",
                    ),
                    cls="grid md:grid-cols-3 gap-5",
                ),
                Div(
                    Span("Source: ", cls="text-ink-dim text-xs"),
                    A(block["source"]["label"], href=block["source"]["url"], target="_blank", cls="text-accent text-xs hover:underline"),
                    cls="mt-4",
                ),
                cls="hidden",
                **{"data-signal-panel": key},
            )
        )

    return page(
        "Signal",
        "/signal",
        Section_(
            Eyebrow("Signal"),
            Heading(1, "European public data, visualised as fund-level context.", cls="mt-5 max-w-5xl"),
            P("Five canvases across the sectors we invest in. Every figure is sourced from a named public dataset and cited below its chart.",
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(*tabs, cls="flex flex-wrap gap-3 mb-10"),
            Div(*panels),
            cls="border-t border-line",
        ),
        CTASection(
            headline="Operating in any of these canvases?",
            body="Signal is how we keep our sector picture live. If you're building in one of these canvases, tell us what you're seeing on the ground.",
        ),
        body_extra=[
            Script(src="https://cdn.plot.ly/plotly-2.35.2.min.js"),
            Script(NotStr(f"window.PLOTLY_DATA = {signal_mod.as_json()};")),
            Script(src="/static/signal.js"),
        ],
    )


# ---------- /team ----------

@rt("/team")
def team():
    return page(
        "Team",
        "/team",
        Section_(
            Eyebrow("Team"),
            Heading(1, "A small, founder-built firm.", cls="mt-5 max-w-4xl"),
            P("Two operators — a managing partner and a venture partner — with two decades of building and exiting European FinTech between them. We keep the partnership deliberately small and the portfolio engagement deliberately deep.",
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                *[_member_card(m) for m in TEAM],
                cls="grid md:grid-cols-2 gap-5",
            ),
        ),
        CTASection(headline="Thinking of raising?",
                   body="If you are building in sovereign AI, defense, health or energy — and want operator-grade capital from founders who have been through seed → Series A — tell us.",
                   cta_label="Write to us"),
    )


def _member_card(m):
    return Article(
        Div(
            Div(m["initials"], cls="w-14 h-14 rounded-full bg-bg-raised border border-line flex items-center justify-center text-ink font-mono text-sm"),
            Div(
                Heading(3, m["name"], cls="mb-1"),
                P(m["role"], cls="text-accent text-sm font-mono"),
            ),
            cls="flex items-center gap-4 mb-5",
        ),
        P(m["bio"], cls="text-ink-muted leading-relaxed mb-6"),
        A(
            Span("LinkedIn", cls="text-sm"),
            Span("→", cls="text-sm"),
            href=m["linkedin"],
            target="_blank",
            cls="inline-flex items-center gap-2 text-ink hover:text-accent transition-colors",
        ),
        cls="p-8 rounded-2xl bg-bg-elevated border border-line",
    )


# ---------- /contact ----------

@rt("/contact")
def contact():
    return page(
        "Contact",
        "/contact",
        Section_(
            Eyebrow("Contact"),
            Heading(1, "Tell us what you're building.", cls="mt-5 max-w-4xl"),
            P("We back founders operating in sovereign AI, defense, health and energy across Europe. Pre-seed to Series A. Send us the thesis — we'll tell you if we can help.",
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                Div(
                    Eyebrow("Write to us"),
                    Heading(2, CONTACT_EMAIL, cls="mt-4 break-all"),
                    P("A short note on what you're building, where you're based and what round you are raising is enough to start a conversation.",
                      cls="mt-5 text-ink-muted leading-relaxed"),
                    Div(
                        Button_("Email " + CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}", primary=True),
                        cls="mt-8",
                    ),
                    cls="p-10 rounded-2xl bg-bg-elevated border border-line",
                ),
                Div(
                    Div(
                        H3("Registered office", cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Founders Capital Ltd", cls="text-ink"),
                        P("155 Minories Street, Suite 275", cls="text-ink-muted"),
                        P("London, EC3N 1AD", cls="text-ink-muted"),
                        P("United Kingdom", cls="text-ink-muted"),
                        cls="mb-10",
                    ),
                    Div(
                        H3("Channels", cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        A("LinkedIn", href=LINKEDIN_URL, target="_blank", cls="block text-ink hover:text-accent mb-2"),
                    ),
                    cls="p-10 rounded-2xl bg-bg-elevated border border-line",
                ),
                cls="grid md:grid-cols-2 gap-5",
            ),
        ),
    )


if __name__ == "__main__":
    serve()
