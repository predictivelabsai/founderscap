"""
Loads the five public-data CSVs in content/data/ and builds Plotly trace
dictionaries for the Signal page. Beige theme, ochre accent; charts picked
to communicate quickly (no decorative treemaps).
"""

import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

TEMPLATE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, system-ui, sans-serif", "color": "#5C5446", "size": 13},
    "margin": {"l": 60, "r": 20, "t": 30, "b": 60},
    "xaxis": {"gridcolor": "#E1D7BC", "linecolor": "#D8CDB3", "zerolinecolor": "#D8CDB3"},
    "yaxis": {"gridcolor": "#E1D7BC", "linecolor": "#D8CDB3", "zerolinecolor": "#D8CDB3"},
}

OCHRE = "#8A6F3B"
OCHRE_DEEP = "#5A4624"
OCHRE_LIGHT = "#BBA97E"

OCHRE_SCALE = [
    [0.0, "#F3ECDD"],
    [0.25, "#E9DFC3"],
    [0.55, "#BBA97E"],
    [0.8, "#8A6F3B"],
    [1.0, "#5A4624"],
]

# Palette cycle for donut/pie slices — beige-to-brown ordered.
SLICE_COLORS = [
    "#5A4624", "#8A6F3B", "#A38552", "#BBA97E",
    "#D6C79E", "#E9DFC3", "#C9B58A", "#9A7F4A",
    "#75553A", "#4F3C24", "#332311",
]


def _read(name):
    with open(DATA_DIR / name, newline="") as f:
        return list(csv.DictReader(f))


def _layout(title):
    return {
        **TEMPLATE,
        "title": {"text": title, "font": {"color": "#2A2722", "size": 15}, "x": 0.02},
    }


# ---------- European VC by country ----------

def european_vc_charts():
    rows = _read("european_vc.csv")
    rows = sorted(rows, key=lambda r: float(r["capital_usd_bn"]))
    countries = [r["country"] for r in rows]
    capital = [float(r["capital_usd_bn"]) for r in rows]
    deals = [int(r["deals"]) for r in rows]

    # Horizontal bar of capital deployed per country
    bars = {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": capital,
                "y": countries,
                "marker": {
                    "color": capital,
                    "colorscale": OCHRE_SCALE,
                    "line": {"color": "#FAF5E7", "width": 1},
                },
                "hovertemplate": "<b>%{y}</b><br>Capital deployed: $%{x:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("VC capital deployed by country (2024, USD bn)"),
            "margin": {"l": 130, "r": 20, "t": 40, "b": 40},
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "USD bn"}},
        },
    }

    # Scatter: capital vs deal count
    scatter = {
        "data": [
            {
                "type": "scatter",
                "mode": "markers+text",
                "x": deals,
                "y": capital,
                "text": countries,
                "textposition": "top center",
                "textfont": {"size": 10, "color": "#5C5446"},
                "marker": {
                    "size": [max(10, c * 2.5) for c in capital],
                    "color": OCHRE,
                    "opacity": 0.75,
                    "line": {"color": OCHRE_DEEP, "width": 1},
                },
                "hovertemplate": "<b>%{text}</b><br>%{x} deals · $%{y:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("Capital vs deal count"),
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "Deals (2024)"}},
            "yaxis": {**TEMPLATE["yaxis"], "title": {"text": "USD bn"}},
            "showlegend": False,
        },
    }
    return bars, scatter


# ---------- European VC by sector ----------

def sector_charts():
    rows = _read("vc_by_sector.csv")
    sectors = [r["sector"] for r in rows]
    capital = [float(r["capital_usd_bn"]) for r in rows]
    shares = [float(r["share_pct"]) for r in rows]

    donut = {
        "data": [
            {
                "type": "pie",
                "labels": sectors,
                "values": capital,
                "hole": 0.55,
                "marker": {"colors": SLICE_COLORS[: len(sectors)]},
                "textinfo": "label+percent",
                "textfont": {"color": "#FFF8E8", "size": 11},
                "hovertemplate": "<b>%{label}</b><br>$%{value:.1f}B · %{percent}<extra></extra>",
            }
        ],
        "layout": {
            **_layout("European VC capital by sector (2024)"),
            "showlegend": False,
        },
    }

    # Horizontal bar of sector share — easier comparison than slices
    pairs = sorted(zip(sectors, shares), key=lambda x: x[1])
    bars = {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": [s for _, s in pairs],
                "y": [s for s, _ in pairs],
                "marker": {
                    "color": [s for _, s in pairs],
                    "colorscale": OCHRE_SCALE,
                    "line": {"color": "#FAF5E7", "width": 1},
                },
                "hovertemplate": "<b>%{y}</b><br>%{x:.1f}% of 2024 European VC<extra></extra>",
            }
        ],
        "layout": {
            **_layout("Sector share of European VC (2024, %)"),
            "margin": {"l": 200, "r": 20, "t": 40, "b": 40},
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "% of total"}},
        },
    }
    return donut, bars


# ---------- Defense-tech funding trend ----------

def defense_charts():
    rows = _read("defense_tech.csv")
    years = [r["year"] for r in rows]
    capital = [float(r["capital_usd_bn"]) for r in rows]

    line = {
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "x": years,
                "y": capital,
                "line": {"color": OCHRE_DEEP, "width": 3, "shape": "spline"},
                "marker": {"color": OCHRE, "size": 10, "line": {"color": "#FFF8E8", "width": 2}},
                "fill": "tozeroy",
                "fillcolor": "rgba(138,111,59,0.18)",
                "hovertemplate": "<b>%{x}</b><br>Funding: $%{y:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("European defense-tech venture funding (USD bn)"),
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "Year"}},
            "yaxis": {**TEMPLATE["yaxis"], "title": {"text": "USD bn"}},
        },
    }

    nato_rows = sorted(_read("nato_spend.csv"),
                       key=lambda r: float(r["spend_usd_bn"]), reverse=True)[:12]
    countries = [r["country"] for r in nato_rows]
    spend = [float(r["spend_usd_bn"]) for r in nato_rows]
    gdp_share = [float(r["gdp_share_pct"]) for r in nato_rows]

    nato_chart = {
        "data": [
            {
                "type": "bar",
                "x": countries,
                "y": spend,
                "marker": {
                    "color": gdp_share,
                    "colorscale": OCHRE_SCALE,
                    "cmin": 1.2,
                    "cmax": 4.2,
                    "showscale": True,
                    "colorbar": {
                        "title": {"text": "% GDP", "font": {"color": "#5C5446"}},
                        "tickfont": {"color": "#5C5446"},
                    },
                    "line": {"color": "#FAF5E7", "width": 1},
                },
                "hovertemplate": "<b>%{x}</b><br>Spend: $%{y:.1f}B<br>%GDP: %{marker.color:.2f}%<extra></extra>",
            }
        ],
        "layout": {
            **_layout("European NATO defence spend 2024 · USD bn (shade = % GDP)"),
            "xaxis": {**TEMPLATE["xaxis"], "tickangle": -35},
            "yaxis": {**TEMPLATE["yaxis"], "title": {"text": "USD bn"}},
        },
    }
    return line, nato_chart


# ---------- Cleantech investment by subsector ----------

def cleantech_charts():
    rows = _read("cleantech_vc.csv")
    rows = sorted(rows, key=lambda r: float(r["capital_usd_bn"]))
    subs = [r["subsector"] for r in rows]
    capital = [float(r["capital_usd_bn"]) for r in rows]
    deals = [int(r["deals"]) for r in rows]

    bars = {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": capital,
                "y": subs,
                "marker": {
                    "color": capital,
                    "colorscale": OCHRE_SCALE,
                    "line": {"color": "#FAF5E7", "width": 1},
                },
                "hovertemplate": "<b>%{y}</b><br>$%{x:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("European cleantech VC by subsector (2024, USD bn)"),
            "margin": {"l": 200, "r": 20, "t": 40, "b": 40},
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "USD bn"}},
        },
    }

    deals_bar = {
        "data": [
            {
                "type": "bar",
                "x": subs,
                "y": deals,
                "marker": {"color": OCHRE, "line": {"color": OCHRE_DEEP, "width": 1}},
                "hovertemplate": "<b>%{x}</b><br>Deals: %{y}<extra></extra>",
            }
        ],
        "layout": {
            **_layout("Deal count by cleantech subsector"),
            "xaxis": {**TEMPLATE["xaxis"], "tickangle": -35},
            "yaxis": {**TEMPLATE["yaxis"], "title": {"text": "Deals"}},
        },
    }
    return bars, deals_bar


# ---------- Global AI private investment ----------

def ai_charts():
    rows = _read("ai_investment.csv")
    rows = sorted(rows, key=lambda r: float(r["private_ai_investment_usd_bn"]))
    countries = [r["country"] for r in rows]
    capital = [float(r["private_ai_investment_usd_bn"]) for r in rows]

    bars = {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": capital,
                "y": countries,
                "marker": {
                    "color": capital,
                    "colorscale": OCHRE_SCALE,
                    "line": {"color": "#FAF5E7", "width": 1},
                },
                "hovertemplate": "<b>%{y}</b><br>$%{x:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("Private AI investment by country (2024, USD bn)"),
            "margin": {"l": 150, "r": 20, "t": 40, "b": 40},
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "USD bn"}},
        },
    }

    # Europe-only view — aggregates the European entries
    european_countries = {"United Kingdom", "Germany", "France", "Sweden",
                          "Netherlands", "Switzerland"}
    europe_rows = [(r["country"], float(r["private_ai_investment_usd_bn"]))
                   for r in rows if r["country"] in european_countries]
    europe_rows = sorted(europe_rows, key=lambda x: x[1])
    europe_bars = {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": [v for _, v in europe_rows],
                "y": [c for c, _ in europe_rows],
                "marker": {"color": OCHRE, "line": {"color": OCHRE_DEEP, "width": 1}},
                "hovertemplate": "<b>%{y}</b><br>$%{x:.1f}B<extra></extra>",
            }
        ],
        "layout": {
            **_layout("Europe only — private AI investment (2024)"),
            "margin": {"l": 150, "r": 20, "t": 40, "b": 40},
            "xaxis": {**TEMPLATE["xaxis"], "title": {"text": "USD bn"}},
        },
    }
    return bars, europe_bars


def all_charts():
    vc_a, vc_b = european_vc_charts()
    sec_a, sec_b = sector_charts()
    def_a, def_b = defense_charts()
    ct_a, ct_b = cleantech_charts()
    ai_a, ai_b = ai_charts()
    return {
        "european_vc": {
            "title": "European VC",
            "eyebrow": "Atomico · Dealroom",
            "summary": "Venture capital deployed into European startups in 2024 — by country of headquarters and deal count. The shape of the market our portfolio operates in.",
            "source": {
                "label": "State of European Tech 2024 · Dealroom European venture review",
                "url": "https://stateofeuropeantech.com/",
            },
            "primary": vc_a,
            "secondary": vc_b,
        },
        "sectors": {
            "title": "Sector allocation",
            "eyebrow": "European VC · 2024",
            "summary": "Where European venture capital actually went in 2024. AI and climate absorbed half; defense and dual-use grew off a small base. These are the sectors we back.",
            "source": {
                "label": "State of European Tech 2024 · Dealroom",
                "url": "https://stateofeuropeantech.com/",
            },
            "primary": sec_a,
            "secondary": sec_b,
        },
        "defense": {
            "title": "Defense-tech",
            "eyebrow": "Dealroom · NATO",
            "summary": "European defense-tech venture funding 2019–2025 alongside NATO defence expenditure. Venture dollars are accelerating off a small base; the underlying procurement budget is an order of magnitude larger and growing.",
            "source": {
                "label": "Dealroom defence + security · NATO Defence Expenditure release",
                "url": "https://www.nato.int/cps/en/natohq/topics_49198.htm",
            },
            "primary": def_a,
            "secondary": def_b,
        },
        "cleantech": {
            "title": "Cleantech",
            "eyebrow": "Cleantech for Europe",
            "summary": "European cleantech venture investment in 2024 — where the energy-transition capital lands once it hits startups.",
            "source": {
                "label": "Cleantech for Europe 2024 Investment Review · IEA",
                "url": "https://www.cleantechforeurope.com/",
            },
            "primary": ct_a,
            "secondary": ct_b,
        },
        "ai": {
            "title": "AI",
            "eyebrow": "Stanford AI Index 2025",
            "summary": "Private AI investment by country in 2024 — the global shape of the sovereign-AI conversation, and Europe's position in it.",
            "source": {
                "label": "Stanford HAI · AI Index 2025",
                "url": "https://aiindex.stanford.edu/",
            },
            "primary": ai_a,
            "secondary": ai_b,
        },
    }


def teaser_chart():
    """Chart used on the home page signal teaser. Shows European VC by
    country as a simple horizontal bar — legible at a glance, aligned
    with the fund thesis."""
    bars, _ = european_vc_charts()
    bars = json.loads(json.dumps(bars))
    bars["layout"]["title"]["text"] = "European VC capital deployed · 2024"
    bars["layout"]["margin"] = {"l": 130, "r": 20, "t": 40, "b": 40}
    return bars


def as_json():
    return json.dumps(all_charts(), separators=(",", ":"))
