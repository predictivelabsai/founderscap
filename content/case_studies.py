"""
Case studies — deep-dive founder narratives from the Founders Capital
operating track record. Bondora, EstateGuru and Investly are the three
named precedents that anchor the firm's credibility and thesis.
"""

FOUNDER_CASES = [
    {
        "id": "bondora",
        "title": "Bondora — from €10k seed to Europe's largest consumer-credit marketplace",
        "buyer": "Bondora · consumer lending · EU",
        "country": "Estonia / pan-EU",
        "flag": "🇪🇺",
        "sector": "FinTech · Consumer credit",
        "status": "Named precedent",
        "problem": "In 2007 European consumer credit was dominated by domestic retail banks with limited cross-border portfolios and an expensive distribution stack. A retail-investor marketplace for short-term consumer loans — liquid, transparent, yield-bearing — did not yet exist at the scale it demanded.",
        "approach": "One of four co-founders. Co-defined the go-to-market and technology strategy, advised the management team through seed, bridge and Series A rounds raised from Valinor Capital and Global Founders Capital / Rocket Internet. Provided industry insight, advised on governance and strategy, and opened relevant market introductions.",
        "capability": "Founding cheque of €10,000 (2007) seeded a business now carrying a reference valuation of €200M — a cumulative return of roughly 20,000× over the holding period. Bondora today has over 1.4M registered customers, €2B+ invested on the platform and €1.6B+ originated in loans.",
        "tech": ["Consumer credit", "Marketplace lending", "Seed → Series A", "20,000× multiple"],
    },
    {
        "id": "estateguru",
        "title": "EstateGuru — short-term property finance across eight European markets",
        "buyer": "EstateGuru · property-bridge lending · EU",
        "country": "Estonia / pan-EU",
        "flag": "🇪🇺",
        "sector": "FinTech · Property finance",
        "status": "Named precedent",
        "problem": "Small and mid-sized property developers across Central and Northern Europe were underserved by traditional bank real-estate finance — particularly for short-duration bridge financing — while retail investors had no clean way to access the asset class at ticket level.",
        "approach": "One of three co-founders. Co-defined the go-to-market and technology strategy, advised management through seed, bridge and Series A rounds raised from Speedinvest and Seedrs. Provided industry insight, advised on governance and strategy, and introduced the business into relevant European markets.",
        "capability": "Founding cheque of €50,000 (2013) seeded a business now carrying a reference valuation of €25M — a cumulative return of roughly 500× over the holding period. EstateGuru today has over €940M lent across 7,700+ property-backed loans, 159k+ investors and a live presence across eight European markets.",
        "tech": ["Property finance", "Bridge lending", "Seed → Series A", "500× multiple"],
    },
    {
        "id": "investly",
        "title": "Investly — open-banking-native invoice finance for European SMEs",
        "buyer": "Investly · SME finance · UK / EE",
        "country": "Estonia / United Kingdom",
        "flag": "🇪🇺",
        "sector": "FinTech · SME finance",
        "status": "Named precedent",
        "problem": "European SMEs — particularly in the UK and Nordics — were underserved by bank receivables finance: slow to underwrite, expensive to service and structurally priced for large enterprise counterparties rather than small businesses.",
        "approach": "One of two co-founders. Co-defined the go-to-market and technology strategy, advised management through seed, bridge and pre-Series A rounds raised from Speedinvest and Seedrs. Provided industry insight, advised on governance and strategy, and supported relevant market introductions.",
        "capability": "Founding cheque of €20,000 (2013) seeded a business now carrying a reference valuation of €5M — a cumulative return of roughly 250× over the holding period. The operational blueprint — open-banking-underwritten, marketplace-funded receivables finance — has since been widely replicated across European working-capital FinTech.",
        "tech": ["Invoice finance", "Open banking", "SME credit", "250× multiple"],
    },
]


# Tabular summary used on /case-studies to anchor the narrative.
FOUNDER_SUMMARY = [
    {
        "company": "Bondora",
        "url": "https://bondora.com",
        "founded": 2007,
        "initial": "€10,000",
        "valuation": "€200M",
        "multiple": "~20,000×",
        "growth": "≈ 2,000,000%",
        "note": "Consumer lending · EU · 1.4M+ customers · €1.6B+ lent",
    },
    {
        "company": "EstateGuru",
        "url": "https://estateguru.co",
        "founded": 2013,
        "initial": "€50,000",
        "valuation": "€25M",
        "multiple": "~500×",
        "growth": "≈ 50,000%",
        "note": "Property finance · 8 EU markets · 159k+ investors · €940M+ lent",
    },
    {
        "company": "Investly",
        "url": "https://investly.co",
        "founded": 2013,
        "initial": "€20,000",
        "valuation": "€5M",
        "multiple": "~250×",
        "growth": "≈ 25,000%",
        "note": "SME invoice finance · UK / EE · open-banking-native",
    },
]


# Backward-compatibility aliases.
ALL = FOUNDER_CASES
BID_DERIVED = []
NAMED_PRECEDENTS = FOUNDER_CASES
