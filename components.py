"""
Shared FastHTML components for the Founders Capital landing site.

Light-beige, sovereign-capital register. Design tokens come from Tailwind via
CDN with a small inline config block. Custom CSS lives in static/site.css.
"""

from fasthtml.common import (
    Html, Head, Body, Meta, Title, Link, Script, Style, NotStr,
    Nav, Main, Footer, Header, Section, Article, Aside, Div, Span, A, Img, Svg,
    H1, H2, H3, H4, H5, H6, P, Ul, Ol, Li, Button, Small, Strong, Em, I,
)

SITE_NAME = "Founders Capital"
SITE_TAGLINE = "European sovereign-AI capital, from founders who have built in Europe."
CONTACT_EMAIL = "info@founderscap.eu"
LINKEDIN_URL = "https://www.linkedin.com/company/founders-capital-ltd/"

NAV_ITEMS = [
    ("Thesis", "/thesis"),
    ("Sectors", None, [
        ("Sovereign & defense AI", "/sectors/defense"),
        ("Health & life sciences", "/sectors/healthcare"),
        ("Energy & resilience", "/sectors/energy"),
        ("Financial services", "/sectors/financial"),
    ]),
    ("Portfolio", "/portfolio"),
    ("Case studies", "/case-studies"),
    ("Signal", "/signal"),
    ("Team", "/team"),
    ("Contact", "/contact"),
]


# Beige, cream, tobacco-brown palette. Accent is a warm ochre.
TAILWIND_CONFIG = """
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: { DEFAULT: '#F3ECDD', elevated: '#FAF5E7', raised: '#FFF8E8' },
        ink: { DEFAULT: '#2A2722', muted: '#5C5446', dim: '#8C8270' },
        line: { DEFAULT: '#D8CDB3', bright: '#BBA97E' },
        accent: { DEFAULT: '#8A6F3B', dim: '#E9DFC3', deep: '#5A4624' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
      },
      letterSpacing: {
        tightest: '-0.04em',
        tighter: '-0.025em',
      },
    },
  },
};
"""


def Eyebrow(text, *, href=None):
    cls = "font-mono text-[11px] tracking-[0.18em] uppercase text-accent"
    if href:
        return A(text, href=href, cls=cls + " hover:text-ink transition-colors")
    return Span(text, cls=cls)


SECTOR_HREF = {
    "health": "/sectors/healthcare",
    "healthcare": "/sectors/healthcare",
    "hospital": "/sectors/healthcare",
    "clinical": "/sectors/healthcare",
    "defense": "/sectors/defense",
    "defence": "/sectors/defense",
    "sovereign": "/sectors/defense",
    "sovereign-ai": "/sectors/defense",
    "dual-use": "/sectors/defense",
    "energy": "/sectors/energy",
    "resilience": "/sectors/energy",
    "financial": "/sectors/financial",
    "fintech": "/sectors/financial",
}


def SectorLink(label: str, *, sector: str | None = None, cls: str = ""):
    key = (sector or label).lower().strip()
    href = SECTOR_HREF.get(key)
    if href is None:
        return Span(label)
    return A(
        label,
        href=href,
        cls=f"text-ink underline decoration-accent/60 decoration-1 underline-offset-4 hover:decoration-accent hover:text-accent transition-colors {cls}".strip(),
    )


def Heading(level, text, *, cls=""):
    tag = {1: H1, 2: H2, 3: H3, 4: H4}[level]
    base = {
        1: "text-4xl sm:text-5xl md:text-7xl font-medium tracking-tightest text-ink leading-[1.05] md:leading-[1.02]",
        2: "text-2xl sm:text-3xl md:text-5xl font-medium tracking-tighter text-ink leading-[1.12] md:leading-[1.08]",
        3: "text-lg sm:text-xl md:text-2xl font-medium tracking-tight text-ink",
        4: "text-base md:text-lg font-medium text-ink",
    }[level]
    return tag(text, cls=f"{base} {cls}".strip())


def Body_(text, *, cls="", muted=True):
    tone = "text-ink-muted" if muted else "text-ink"
    return P(text, cls=f"text-base md:text-lg leading-relaxed {tone} {cls}".strip())


def Button_(text, *, href="#", primary=True, cls=""):
    base = "inline-flex items-center gap-2 px-5 py-3 rounded-full text-sm font-medium transition-all duration-200"
    if primary:
        style = "bg-accent text-bg-raised hover:bg-accent-deep shadow-[0_0_0_1px_#8A6F3B] hover:shadow-[0_0_0_1px_#5A4624]"
    else:
        style = "bg-transparent text-ink border border-line-bright hover:border-accent hover:text-accent"
    return A(text, Span("→", cls="text-base"), href=href, cls=f"{base} {style} {cls}".strip())


def Pill(text, *, cls=""):
    return Span(
        text,
        cls=f"inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono tracking-wider uppercase text-ink-muted bg-bg-elevated border border-line {cls}".strip(),
    )


def Navbar(current_path: str = "/"):
    def _nav_item(item):
        if len(item) == 2:
            label, href = item
            active = current_path == href
            return Li(
                A(
                    label,
                    href=href,
                    cls=f"text-sm text-ink-muted hover:text-ink transition-colors {'text-ink' if active else ''}",
                )
            )
        label, _, children = item
        return Li(
            Div(
                Span(label, cls="text-sm text-ink-muted hover:text-ink transition-colors flex items-center gap-1 cursor-default"),
                Span("▾", cls="text-xs text-ink-dim"),
                cls="flex items-center gap-1",
            ),
            Ul(
                *[
                    Li(
                        A(
                            sub_label,
                            href=sub_href,
                            cls="block px-4 py-2 text-sm text-ink-muted hover:text-ink hover:bg-bg-raised",
                        )
                    )
                    for sub_label, sub_href in children
                ],
                cls="absolute right-0 mt-3 w-64 rounded-xl border border-line bg-bg-elevated py-2 shadow-2xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200",
            ),
            cls="relative group",
        )

    def _flat_mobile():
        out = []
        for item in NAV_ITEMS:
            if len(item) == 2:
                out.append(item)
            else:
                label, _, children = item
                out.append((label, None))
                out.extend(children)
        return out

    mobile_items = [
        Li(Span(lbl, cls="block text-xs font-mono tracking-widest uppercase text-ink-dim pt-3"))
        if href is None
        else Li(A(lbl, href=href, cls=f"block py-2 text-base {'text-accent' if current_path == href else 'text-ink hover:text-accent'}"))
        for lbl, href in _flat_mobile()
    ]

    return Nav(
        Div(
            A(
                Span("◆", cls="text-accent mr-2"),
                Span(SITE_NAME, cls="font-medium tracking-tight"),
                href="/",
                cls="flex items-center text-ink text-base hover:text-accent transition-colors",
            ),
            Ul(
                *[_nav_item(i) for i in NAV_ITEMS],
                cls="hidden lg:flex items-center gap-7",
            ),
            A(
                "Talk to us",
                href="/contact",
                cls="hidden lg:inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium bg-ink text-bg-raised hover:bg-accent transition-colors",
            ),
            Button(
                Span("☰", id="nav-burger-icon", cls="text-2xl leading-none"),
                type="button",
                aria_label="Open menu",
                onclick=(
                    "const m=document.getElementById('mobile-nav');"
                    "const i=document.getElementById('nav-burger-icon');"
                    "const open=m.classList.toggle('hidden')===false;"
                    "i.textContent=open?'✕':'☰';"
                ),
                cls="lg:hidden text-ink hover:text-accent w-10 h-10 flex items-center justify-center rounded-full border border-line",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6 flex items-center justify-between h-16 gap-4",
        ),
        Div(
            Ul(*mobile_items, cls="px-5 pb-5 pt-2 space-y-1"),
            Div(
                A(
                    "Talk to us",
                    href="/contact",
                    cls="block text-center px-4 py-3 rounded-full text-sm font-medium bg-accent text-bg-raised mx-5 mb-5",
                ),
            ),
            id="mobile-nav",
            cls="hidden lg:hidden border-t border-line bg-bg-elevated",
        ),
        cls="sticky top-0 z-50 backdrop-blur-md bg-bg/80 border-b border-line",
    )


def Section_(*content, bleed=False, cls=""):
    inner_cls = "max-w-7xl mx-auto px-5 md:px-6" if not bleed else "w-full"
    return Section(Div(*content, cls=inner_cls), cls=f"py-14 md:py-20 lg:py-28 {cls}".strip())


def Footer_():
    columns = [
        ("Fund", [
            ("Thesis", "/thesis"),
            ("Portfolio", "/portfolio"),
            ("Case studies", "/case-studies"),
            ("Signal", "/signal"),
        ]),
        ("Sectors", [
            ("Sovereign & defense AI", "/sectors/defense"),
            ("Health & life sciences", "/sectors/healthcare"),
            ("Energy & resilience", "/sectors/energy"),
            ("Financial services", "/sectors/financial"),
        ]),
        ("Firm", [
            ("Team", "/team"),
            ("Contact", "/contact"),
            ("LinkedIn", LINKEDIN_URL),
        ]),
    ]

    col_divs = [
        Div(
            H4(title, cls="text-xs font-mono tracking-[0.18em] uppercase text-ink-muted mb-5"),
            Ul(
                *[Li(A(label, href=href, cls="text-sm text-ink hover:text-accent transition-colors"), cls="mb-2") for label, href in links],
                cls="space-y-2",
            ),
        )
        for title, links in columns
    ]

    return Footer(
        Div(
            Div(
                Div(
                    A(
                        Span("◆", cls="text-accent mr-2"),
                        Span(SITE_NAME, cls="font-medium text-ink tracking-tight"),
                        href="/",
                        cls="flex items-center text-lg mb-4",
                    ),
                    P(SITE_TAGLINE, cls="text-ink-muted text-sm max-w-xs mb-5 leading-relaxed"),
                    P(
                        "Founders Capital Ltd", NotStr("<br>"),
                        "155 Minories Street, Suite 275", NotStr("<br>"),
                        "London, EC3N 1AD, United Kingdom",
                        cls="text-ink-dim text-xs leading-relaxed",
                    ),
                ),
                *col_divs,
                cls="grid grid-cols-2 md:grid-cols-4 gap-10",
            ),
            Div(
                Div(f"© {__import__('datetime').datetime.now().year} Founders Capital Ltd.", cls="text-ink-dim text-xs"),
                Div(
                    A("LinkedIn", href=LINKEDIN_URL, cls="text-ink-dim text-xs hover:text-accent mr-4"),
                    A(CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}", cls="text-ink-dim text-xs hover:text-accent break-all"),
                    cls="flex items-center flex-wrap gap-y-2",
                ),
                cls="mt-10 md:mt-14 pt-6 border-t border-line flex items-start md:items-center justify-between flex-wrap gap-4",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        cls="py-12 md:py-16 border-t border-line bg-bg-elevated",
    )


def page(title: str, current_path: str = "/", *content, head_extra=None, body_extra=None):
    head_children = [
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Meta(name="description", content=f"{SITE_NAME} — {SITE_TAGLINE}"),
        Title(f"{title} · {SITE_NAME}"),
        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap",
        ),
        Script(src="https://cdn.tailwindcss.com"),
        Script(NotStr(TAILWIND_CONFIG)),
        Link(rel="stylesheet", href="/static/site.css"),
    ]
    if head_extra:
        head_children.extend(head_extra if isinstance(head_extra, list) else [head_extra])

    body_children = [
        Navbar(current_path),
        Main(*content, cls="min-h-screen"),
        Footer_(),
    ]
    if body_extra:
        body_children.extend(body_extra if isinstance(body_extra, list) else [body_extra])

    return Html(
        Head(*head_children),
        Body(*body_children, cls="bg-bg text-ink font-sans antialiased"),
        lang="en",
    )


# ---------- Higher-level building blocks ----------

def Hero(*, eyebrow="European sovereign capital", headline=None, lede=None, ctas=None, canvas=True, tall=True):
    headline = headline or (
        Span("Backing European founders in "),
        Span("sovereign AI,", cls="text-accent"),
        Span(" defense, health and energy."),
    )
    lede = lede or (
        "Founders Capital is a founder-led early-stage fund built on two decades of operating across European ",
        SectorLink("fintech", sector="financial"), " — and now focused on the ",
        SectorLink("sovereign-AI"), ", ",
        SectorLink("defense"), ", ",
        SectorLink("health"), " and ",
        SectorLink("energy"),
        " platforms that Europe needs to build at home.",
    )
    ctas = ctas or [("See the portfolio", "/portfolio", True), ("Read the thesis", "/thesis", False)]

    height = "min-h-[78vh] md:min-h-[86vh]" if tall else "min-h-[54vh] md:min-h-[58vh]"

    canvas_div = Div(id="three-hero", cls="absolute inset-0 z-10 opacity-50 pointer-events-none") if canvas else None

    lede_nodes = lede if isinstance(lede, tuple) else (lede,)

    return Section(
        Div(
            canvas_div,
            Div(cls="absolute inset-0 z-20 bg-gradient-to-b from-bg/10 via-transparent to-bg pointer-events-none"),
            Div(
                Eyebrow(eyebrow),
                H1(*headline if isinstance(headline, tuple) else [headline], cls="mt-5 md:mt-6 text-[40px] sm:text-5xl md:text-7xl lg:text-[84px] font-medium tracking-tightest text-ink leading-[1.05] md:leading-[1.02] max-w-5xl"),
                P(*lede_nodes, cls="mt-6 md:mt-8 text-base md:text-xl text-ink-muted max-w-2xl leading-relaxed"),
                Div(
                    *[Button_(text, href=href, primary=primary) for text, href, primary in ctas],
                    cls="mt-8 md:mt-10 flex items-center gap-3 flex-wrap",
                ),
                cls="relative z-30 max-w-7xl mx-auto px-5 md:px-6 py-16 md:py-0",
            ),
            cls=f"relative {height} flex items-center overflow-hidden bg-bg",
        ),
        Div(
            Div(
                Div("A founder-led European fund", cls="text-[11px] md:text-xs font-mono tracking-[0.18em] uppercase text-ink-dim"),
                Div(
                    Span("Portfolio capital deployed across ", cls="text-ink-muted text-xs md:text-sm"),
                    Span("€2.5B+ ", cls="text-accent text-xs md:text-sm font-mono"),
                    Span("lent · 100k+ investors", cls="text-ink-muted text-xs md:text-sm"),
                ),
                cls="max-w-7xl mx-auto px-5 md:px-6 py-4 md:py-5 flex items-center justify-between flex-wrap gap-3",
            ),
            cls="border-y border-line bg-bg-elevated/60",
        ),
    )


def Pillar(number: str, title: str, body: str, *, icon="◆"):
    return Div(
        Div(
            Span(icon, cls="text-accent text-xl"),
            Span(number, cls="font-mono text-xs tracking-widest text-ink-dim ml-auto"),
            cls="flex items-center mb-6",
        ),
        Heading(3, title, cls="mb-3"),
        P(body, cls="text-ink-muted text-sm leading-relaxed"),
        cls="p-7 rounded-2xl bg-bg-elevated border border-line hover:border-accent/50 transition-colors group",
    )


def MetricTile(value, unit, caption, *, cls=""):
    return Div(
        Div(
            Span(value, cls="text-4xl md:text-5xl font-medium tracking-tighter text-ink"),
            Span(unit, cls="text-lg text-accent ml-1"),
            cls="flex items-baseline",
        ),
        P(caption, cls="text-ink-muted text-sm mt-2"),
        cls=f"p-6 rounded-2xl bg-bg-elevated border border-line {cls}".strip(),
    )


def CaseStudyCard(cs, *, compact=False):
    tech = Div(
        *[Pill(t) for t in cs.get("tech", [])[:6]],
        cls="flex flex-wrap gap-2 mt-5",
    )
    return Article(
        Div(
            Span(cs["flag"], cls="text-xl mr-2"),
            Span(cs["country"], cls="text-xs font-mono tracking-widest text-ink-muted uppercase"),
            Span("·", cls="text-ink-dim mx-2"),
            Span(cs["sector"], cls="text-xs font-mono tracking-widest text-ink-muted uppercase"),
            Span(cs["status"], cls="ml-auto text-xs font-mono text-accent px-2 py-1 rounded-full border border-accent/40"),
            cls="flex items-center mb-5",
        ),
        Heading(3, cs["title"], cls="mb-2"),
        P(cs["buyer"], cls="text-ink-muted text-sm font-mono mb-5"),
        Div(
            Div(
                Div("Problem", cls="text-[10px] font-mono tracking-widest uppercase text-ink-dim mb-1"),
                P(cs["problem"], cls="text-ink-muted text-sm leading-relaxed"),
                cls="mb-4",
            ),
            Div(
                Div("Approach", cls="text-[10px] font-mono tracking-widest uppercase text-ink-dim mb-1"),
                P(cs["approach"], cls="text-ink text-sm leading-relaxed"),
                cls="mb-4",
            ),
            Div(
                Div("Outcome", cls="text-[10px] font-mono tracking-widest uppercase text-ink-dim mb-1"),
                P(cs["capability"], cls="text-ink-muted text-sm leading-relaxed italic"),
            ) if not compact else None,
        ),
        tech if not compact else None,
        cls="p-7 rounded-2xl bg-bg-elevated border border-line hover:border-accent/40 transition-colors",
    )


def PortfolioCard(p):
    """Card for the portfolio page — logo, company name, one-liner, sector tag."""
    logo_src = p.get("logo")
    logo_node = (
        Img(src=logo_src, alt=p["name"], cls="w-14 h-14 rounded-xl object-contain bg-bg-raised border border-line p-2")
        if logo_src
        else Div(p["initials"], cls="w-14 h-14 rounded-xl bg-bg-raised border border-line flex items-center justify-center text-ink font-mono text-base")
    )
    return A(
        Article(
            Div(
                logo_node,
                Div(
                    Heading(3, p["name"], cls="mb-1"),
                    P(p["url_label"], cls="text-ink-dim text-xs font-mono"),
                ),
                Span(p["sector"], cls="ml-auto text-[10px] font-mono tracking-widest uppercase text-accent"),
                cls="flex items-center gap-4 mb-5",
            ),
            P(p["tagline"], cls="text-ink-muted text-sm leading-relaxed mb-5"),
            Div(*[Pill(t) for t in p.get("tags", [])], cls="flex flex-wrap gap-2"),
            cls="p-7 rounded-2xl bg-bg-elevated border border-line hover:border-accent/50 transition-all h-full",
        ),
        href=p["url"],
        target="_blank",
        rel="noopener",
        cls="block",
    )


def NewsSection(*, category: str, title: str = "From the feed",
                subtitle: str | None = None, eyebrow: str = "News"):
    """Render a compact news block from the in-memory news cache."""
    from content import news as _news

    items = _news.items_for(category)
    if not items:
        return Div()

    def _item(it):
        pub = _news.format_published(it.get("published"))
        meta = [Span(it["source"], cls="text-ink-dim text-xs font-mono")]
        if pub:
            meta.append(Span("·", cls="text-ink-dim text-xs mx-2"))
            meta.append(Span(pub, cls="text-ink-dim text-xs"))
        return A(
            Div(
                H4(it["title"], cls="text-ink text-base md:text-lg font-medium leading-snug mb-3 group-hover:text-accent transition-colors"),
                Div(*meta, cls="flex items-center flex-wrap"),
                cls="p-5 md:p-6 h-full rounded-2xl bg-bg-elevated border border-line group-hover:border-accent/60 transition-colors",
            ),
            href=it["url"],
            target="_blank",
            rel="noopener",
            cls="block group",
        )

    last = _news.last_refresh_iso()

    return Section_(
        Div(
            Div(
                Eyebrow(eyebrow),
                Heading(2, title, cls="mt-4 max-w-3xl"),
                P(subtitle, cls="mt-4 text-ink-muted max-w-2xl leading-relaxed") if subtitle else None,
                cls="md:flex-1",
            ),
            Div(
                Span("Refreshed hourly from public VC and sector RSS feeds.",
                     cls="text-ink-dim text-xs"),
                Span(NotStr("&nbsp;·&nbsp;") + f"Last refresh: {last}" if last else "",
                     cls="text-ink-dim text-xs"),
                cls="text-left md:text-right md:max-w-xs mt-4 md:mt-0",
            ),
            cls="mb-10 flex flex-col md:flex-row md:items-end md:justify-between gap-4",
        ),
        Div(
            *[_item(it) for it in items],
            cls="grid md:grid-cols-2 gap-4",
        ),
        cls="border-t border-line",
    )


def CTASection(*, headline="Building something European worth backing?",
               body="Founders Capital backs founders operating in the European public interest — sovereign AI, defense, health, energy. Pre-seed to Series A. Tell us what you're building.",
               cta_label="Get in touch", cta_href="/contact"):
    return Section(
        Div(
            Div(
                Eyebrow("Engage"),
                Heading(2, headline, cls="mt-4 max-w-3xl"),
                P(body, cls="mt-5 text-ink-muted text-lg max-w-2xl leading-relaxed"),
                Div(
                    Button_(cta_label, href=cta_href, primary=True),
                    Button_("See portfolio", href="/portfolio", primary=False),
                    cls="mt-8 flex items-center gap-3 flex-wrap",
                ),
                cls="max-w-7xl mx-auto px-6 py-20 md:py-28 relative z-10",
            ),
            Div(cls="absolute inset-0 bg-gradient-to-br from-accent/10 via-transparent to-transparent pointer-events-none"),
            cls="relative border-y border-line bg-bg-elevated/60 overflow-hidden",
        ),
    )
