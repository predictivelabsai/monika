"""
Monika landing page — Santa Monica / California sunset register.

Public marketing site for the Monika film financing operating system,
brought to you by Ashland Hill Media Finance (ashland-hill.com).

Structure ported from the founderscap landing site — adapted for film &
media finance, with a sunset-and-palms visual register, the real Ashland
Hill project slate, and the real Ashland Hill team.

The renderer is exposed as `landing_page()` and called from app.py's `/`
route when no user is signed in. Login, registration, and the dashboard
remain untouched.
"""

from fasthtml.common import (
    Html, Head, Body, Meta, Title, Link, Script, Style, NotStr,
    Nav, Main, Footer, Section, Article, Div, Span, A, P, H1, H2, H3, H4,
    Ul, Li, Img,
)


SITE_NAME = "Monika"
PARENT_NAME = "Ashland Hill Media Finance"
PARENT_SHORT = "Ashland Hill"
PARENT_URL = "https://ashland-hill.com"
PROJECTS_URL = "https://ashland-hill.com/projects"
TAGLINE = "The film financing operating system, brought to you by Ashland Hill Media Finance."
CONTACT_EMAIL = "info@ashland-hill.com"


# Sunset / Pacific palette — warm cream base, magenta-orange accents,
# deep palm-green and twilight-navy ink.
TAILWIND_CONFIG = """
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg:   { DEFAULT: '#FFF6EC', elevated: '#FFEDDB', raised: '#FFFAF2' },
        ink:  { DEFAULT: '#1B1F2E', muted: '#4D5366', dim: '#838997' },
        line: { DEFAULT: '#F1D4B0', bright: '#E2B27D' },
        accent: { DEFAULT: '#FF6B3D', deep: '#C73E12', dim: '#FFE0CD' },
        sun:    { 1: '#FFC07A', 2: '#FF8E53', 3: '#FF5A6E', 4: '#A03A8C' },
        palm:   { DEFAULT: '#1F4D3D', dim: '#2E6B57' },
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


# Inline CSS for the hero sunset + palm silhouettes. Keeps the landing page
# free of any external image dependencies.
LANDING_CSS = """
.sunset-bg {
  background:
    radial-gradient(120% 80% at 50% 100%, #FFC07A 0%, #FF8E53 28%, #FF5A6E 55%, #A03A8C 78%, #2C2455 100%);
}
.sunset-disc {
  position: absolute;
  bottom: 18%;
  left: 50%;
  width: 320px;
  height: 320px;
  margin-left: -160px;
  border-radius: 9999px;
  background: radial-gradient(circle, #FFE7B3 0%, #FFB76A 35%, #FF6B3D 60%, rgba(255,107,61,0) 78%);
  filter: blur(2px);
  opacity: 0.95;
  pointer-events: none;
}
.sunset-haze {
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(255,107,61,0) 0%, rgba(28,18,46,0.0) 55%, rgba(28,18,46,0.45) 100%);
  pointer-events: none;
}
.palm {
  position: absolute;
  bottom: 0;
  width: 220px;
  height: 360px;
  pointer-events: none;
  opacity: 0.92;
}
.palm--left  { left: -20px; }
.palm--right { right: -20px; transform: scaleX(-1); }
@media (min-width: 768px) {
  .palm { width: 320px; height: 480px; }
}
.horizon {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 28%;
  background: linear-gradient(180deg, rgba(28,18,46,0) 0%, rgba(28,18,46,0.65) 100%);
  pointer-events: none;
}
.product-card { transition: transform 200ms ease, border-color 200ms ease; }
.product-card:hover { transform: translateY(-2px); border-color: #FF6B3D; }
.poster {
  aspect-ratio: 2/3;
  width: 100%;
  object-fit: cover;
  background: #1B1F2E;
  display: block;
}
.poster-card { transition: transform 200ms ease; }
.poster-card:hover { transform: translateY(-3px); }
.poster-card:hover .poster { opacity: 0.92; }
.team-photo {
  aspect-ratio: 1/1;
  width: 100%;
  object-fit: cover;
  background: #FFEDDB;
  display: block;
  filter: saturate(0.9);
}
"""


PALM_SVG = NotStr(
    '<svg class="palm palm--left" viewBox="0 0 220 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<defs><linearGradient id="trunk" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#0d2018"/><stop offset="1" stop-color="#06120c"/>'
    '</linearGradient></defs>'
    '<path d="M120 360 C 110 280 116 200 124 130 C 130 90 132 70 130 50" '
    'stroke="url(#trunk)" stroke-width="14" fill="none" stroke-linecap="round"/>'
    '<g fill="#0d2018">'
    '<path d="M130 60 C 70 30 30 40 0 70 C 40 50 90 55 130 70 Z"/>'
    '<path d="M130 60 C 190 25 220 40 220 80 C 200 55 165 55 130 70 Z"/>'
    '<path d="M130 60 C 100 0 60 -5 30 30 C 70 10 110 25 132 60 Z"/>'
    '<path d="M130 60 C 160 0 200 0 220 30 C 195 15 160 25 132 60 Z"/>'
    '<path d="M130 60 C 60 80 25 115 10 160 C 55 115 100 90 132 70 Z"/>'
    '<path d="M130 60 C 195 80 215 115 220 165 C 200 115 160 90 132 70 Z"/>'
    '</g>'
    '<g fill="#06120c">'
    '<circle cx="124" cy="76" r="6"/><circle cx="138" cy="78" r="6"/><circle cx="131" cy="86" r="6"/>'
    '</g>'
    '</svg>'
)

PALM_SVG_RIGHT = NotStr(
    '<svg class="palm palm--right" viewBox="0 0 220 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<defs><linearGradient id="trunkR" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#0d2018"/><stop offset="1" stop-color="#06120c"/>'
    '</linearGradient></defs>'
    '<path d="M120 360 C 110 280 116 200 124 130 C 130 90 132 70 130 50" '
    'stroke="url(#trunkR)" stroke-width="14" fill="none" stroke-linecap="round"/>'
    '<g fill="#0d2018">'
    '<path d="M130 60 C 70 30 30 40 0 70 C 40 50 90 55 130 70 Z"/>'
    '<path d="M130 60 C 190 25 220 40 220 80 C 200 55 165 55 130 70 Z"/>'
    '<path d="M130 60 C 100 0 60 -5 30 30 C 70 10 110 25 132 60 Z"/>'
    '<path d="M130 60 C 160 0 200 0 220 30 C 195 15 160 25 132 60 Z"/>'
    '<path d="M130 60 C 60 80 25 115 10 160 C 55 115 100 90 132 70 Z"/>'
    '<path d="M130 60 C 195 80 215 115 220 165 C 200 115 160 90 132 70 Z"/>'
    '</g>'
    '<g fill="#06120c">'
    '<circle cx="124" cy="76" r="6"/><circle cx="138" cy="78" r="6"/><circle cx="131" cy="86" r="6"/>'
    '</g>'
    '</svg>'
)


# ---------------------------------------------------------------------------
# Small atoms
# ---------------------------------------------------------------------------

def _eyebrow(text, *, on_dark=False):
    color = "text-sun-1" if on_dark else "text-accent"
    return Span(text, cls=f"font-mono text-[11px] tracking-[0.18em] uppercase {color}")


def _heading(level, text, *, cls="", on_dark=False):
    tag = {1: H1, 2: H2, 3: H3, 4: H4}[level]
    base = {
        1: "text-4xl sm:text-5xl md:text-7xl font-medium tracking-tightest leading-[1.05] md:leading-[1.02]",
        2: "text-2xl sm:text-3xl md:text-5xl font-medium tracking-tighter leading-[1.12] md:leading-[1.08]",
        3: "text-lg sm:text-xl md:text-2xl font-medium tracking-tight",
        4: "text-base md:text-lg font-medium",
    }[level]
    color = "text-bg-raised" if on_dark else "text-ink"
    return tag(text, cls=f"{base} {color} {cls}".strip())


def _btn(text, *, href="#", primary=True, cls="", target=None):
    base = "inline-flex items-center gap-2 px-5 py-3 rounded-full text-sm font-medium transition-all duration-200"
    if primary:
        style = "bg-accent text-bg-raised hover:bg-accent-deep shadow-[0_0_0_1px_#FF6B3D] hover:shadow-[0_0_0_1px_#C73E12]"
    else:
        style = "bg-transparent text-ink border border-line-bright hover:border-accent hover:text-accent"
    kw = {"href": href, "cls": f"{base} {style} {cls}".strip()}
    if target:
        kw["target"] = target
        kw["rel"] = "noopener"
    return A(text, Span("→", cls="text-base"), **kw)


def _btn_on_dark(text, *, href="#", primary=True, cls=""):
    base = "inline-flex items-center gap-2 px-5 py-3 rounded-full text-sm font-medium transition-all duration-200"
    if primary:
        style = "bg-bg-raised text-ink hover:bg-accent hover:text-bg-raised"
    else:
        style = "bg-transparent text-bg-raised border border-bg-raised/40 hover:border-bg-raised hover:bg-bg-raised/10"
    return A(text, Span("→", cls="text-base"), href=href, cls=f"{base} {style} {cls}".strip())


def _pill(text):
    return Span(
        text,
        cls="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono tracking-wider uppercase text-ink-muted bg-bg-elevated border border-line",
    )


# ---------------------------------------------------------------------------
# Navbar / Footer
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("Products",   "#products"),
    ("How it works", "#how"),
    ("Slate",      "#slate"),
    ("Team",       "#team"),
    ("Ashland Hill", "#ashland"),
]


def _navbar():
    return Nav(
        Div(
            A(
                Span("◐", cls="text-accent mr-2"),
                Span(SITE_NAME, cls="font-medium tracking-tight"),
                href="/",
                cls="flex items-center text-ink text-base hover:text-accent transition-colors",
            ),
            Ul(
                *[
                    Li(A(label, href=href, cls="text-sm text-ink-muted hover:text-ink transition-colors"))
                    for label, href in NAV_ITEMS
                ],
                cls="hidden lg:flex items-center gap-7",
            ),
            Div(
                A("Sign in", href="/login",
                  cls="text-sm text-ink-muted hover:text-ink transition-colors"),
                A("Request access", href="/register",
                  cls="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium bg-ink text-bg-raised hover:bg-accent transition-colors"),
                cls="flex items-center gap-4",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6 flex items-center justify-between h-16 gap-4",
        ),
        cls="sticky top-0 z-50 backdrop-blur-md bg-bg/80 border-b border-line",
    )


def _footer():
    columns = [
        ("Platform", [
            ("Products", "#products"),
            ("How it works", "#how"),
            ("Slate", "#slate"),
            ("Sign in", "/login"),
        ]),
        ("Capabilities", [
            ("Sales Estimates", "#products"),
            ("Production Risk Scoring", "#products"),
            ("Smart Budgeting", "#products"),
            ("Soft Funding Discovery", "#products"),
            ("Talent Intelligence", "#products"),
        ]),
        ("Ashland Hill", [
            ("ashland-hill.com", PARENT_URL),
            ("Project archive", PROJECTS_URL),
            ("Meet the team", "#team"),
            ("Contact", f"mailto:{CONTACT_EMAIL}"),
        ]),
    ]
    col_divs = [
        Div(
            H4(title, cls="text-xs font-mono tracking-[0.18em] uppercase text-ink-muted mb-5"),
            Ul(
                *[Li(A(lbl, href=h, cls="text-sm text-ink hover:text-accent transition-colors"), cls="mb-2")
                  for lbl, h in links],
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
                        Span("◐", cls="text-accent mr-2"),
                        Span(SITE_NAME, cls="font-medium text-ink tracking-tight"),
                        href="/",
                        cls="flex items-center text-lg mb-4",
                    ),
                    P(TAGLINE, cls="text-ink-muted text-sm max-w-xs mb-5 leading-relaxed"),
                    P(
                        "Brought to you by ",
                        A(PARENT_NAME, href=PARENT_URL, target="_blank", rel="noopener",
                          cls="text-ink hover:text-accent underline decoration-accent/50 underline-offset-4"),
                        cls="text-ink-dim text-xs leading-relaxed",
                    ),
                    P("Santa Monica · California", cls="text-ink-dim text-xs mt-2"),
                ),
                *col_divs,
                cls="grid grid-cols-2 md:grid-cols-4 gap-10",
            ),
            Div(
                Div(f"© {__import__('datetime').datetime.now().year} {PARENT_NAME}. Monika is a product of Ashland Hill.",
                    cls="text-ink-dim text-xs"),
                Div(
                    A(PARENT_URL.replace("https://", ""), href=PARENT_URL, target="_blank", rel="noopener",
                      cls="text-ink-dim text-xs hover:text-accent mr-4"),
                    A(CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}",
                      cls="text-ink-dim text-xs hover:text-accent"),
                    cls="flex items-center flex-wrap gap-y-2",
                ),
                cls="mt-10 md:mt-14 pt-6 border-t border-line flex items-start md:items-center justify-between flex-wrap gap-4",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        cls="py-12 md:py-16 border-t border-line bg-bg-elevated",
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def _hero():
    return Section(
        Div(
            Div(
                Div(cls="sunset-disc"),
                Div(cls="sunset-haze"),
                PALM_SVG,
                PALM_SVG_RIGHT,
                Div(cls="horizon"),
                cls="absolute inset-0 sunset-bg overflow-hidden",
            ),
            Div(
                _eyebrow("Monika · From Ashland Hill Media Finance", on_dark=True),
                H1(
                    Span("The film financing "),
                    Span("operating system", cls="text-sun-1"),
                    Span(" for the next decade of independent cinema."),
                    cls="mt-5 md:mt-6 text-[40px] sm:text-5xl md:text-7xl lg:text-[78px] font-medium tracking-tightest text-bg-raised leading-[1.05] md:leading-[1.02] max-w-5xl",
                ),
                P(
                    "Monika is the AI-driven workspace for film and media finance — built by ",
                    A(PARENT_NAME, href=PARENT_URL, target="_blank", rel="noopener",
                      cls="underline decoration-sun-1/70 underline-offset-4 hover:decoration-sun-1 text-bg-raised"),
                    " in Santa Monica. Underwriting, sales estimates, production risk, smart budgets, soft-funding discovery, talent intelligence and a full data room — in one operator-grade workspace, run on a slate that has closed hundreds of deals and deployed billions to independent film and TV.",
                    cls="mt-6 md:mt-8 text-base md:text-xl text-bg-raised/85 max-w-2xl leading-relaxed",
                ),
                Div(
                    _btn_on_dark("Sign in", href="/login", primary=True),
                    _btn_on_dark("Request access", href="/register", primary=False),
                    cls="mt-8 md:mt-10 flex items-center gap-3 flex-wrap",
                ),
                cls="relative z-10 max-w-7xl mx-auto px-5 md:px-6 py-24 md:py-32",
            ),
            cls="relative min-h-[78vh] md:min-h-[86vh] flex items-center overflow-hidden",
        ),
        Div(
            Div(
                Div("A film-finance operating system", cls="text-[11px] md:text-xs font-mono tracking-[0.18em] uppercase text-ink-dim"),
                Div(
                    Span("10 product modules · ", cls="text-ink-muted text-xs md:text-sm"),
                    Span("18 AI tools · ", cls="text-accent text-xs md:text-sm font-mono"),
                    Span("16 global incentive programs", cls="text-ink-muted text-xs md:text-sm"),
                ),
                cls="max-w-7xl mx-auto px-5 md:px-6 py-4 md:py-5 flex items-center justify-between flex-wrap gap-3",
            ),
            cls="border-y border-line bg-bg-elevated/60",
        ),
    )


# ---------------------------------------------------------------------------
# Products grid
# ---------------------------------------------------------------------------

PRODUCTS = [
    ("01", "Film Financing OS",
     "Deals, sales & collections, credit ratings, accounting, contacts and communications — the underwriting workspace that runs your slate."),
    ("02", "Sales Estimates Generator",
     "TMDB- and OMDB-driven comps. Territory MG projections, box-office forecasting, ancillary revenue models — benchmarked against real comparable films."),
    ("03", "Production Risk Scoring",
     "AI scores six risk dimensions (0–100), assigns a tier and surfaces concrete mitigations — from cast attachment risk to weather exposure."),
    ("04", "Smart Budgeting",
     "Generative low / mid / high budget scenarios with line items — so producers and lenders can stress-test the same project from both sides."),
    ("05", "Production Scheduling",
     "AI-generated day-by-day shooting schedules with location clustering — turning a script breakdown into a realistic bond-grade plan."),
    ("06", "Soft Funding Discovery",
     "16 seeded global incentive programs and a rebate calculator — find the right tax credit, grant, or rebate for any production footprint."),
    ("07", "Deal Closing & Data Room",
     "Per-deal closing checklists and document tracking — the workspace where investment committee, finance and legal converge."),
    ("08", "Audience & Marketing Intelligence",
     "AI-predicted audience segments, marketing channels and release strategy — feeding directly back into your revenue model."),
    ("09", "Talent Intelligence",
     "TMDB-powered actor and director search with heat / fit / ROI scoring — cast packaging informed by data, not just instinct."),
    ("10", "Credit Scoring (ML)",
     "Random Forest and Logistic Regression models per collateral class — Pre-Sales, Gap, Tax Credit — with feature-importance and per-deal contribution charts."),
]


def _product_card(num, title, body):
    return Article(
        Div(
            Span("◆", cls="text-accent text-xl"),
            Span(num, cls="font-mono text-xs tracking-widest text-ink-dim ml-auto"),
            cls="flex items-center mb-6",
        ),
        _heading(3, title, cls="mb-3"),
        P(body, cls="text-ink-muted text-sm leading-relaxed"),
        cls="product-card p-7 rounded-2xl bg-bg-elevated border border-line h-full",
    )


def _products_section():
    return Section(
        Div(
            Div(
                _eyebrow("Products"),
                _heading(2, "Ten products, one operating system.", cls="mt-4 max-w-3xl"),
                P(
                    "Monika is the workspace that Ashland Hill built to run our own film-finance practice — and that we now offer to producers, sales agents, lenders and family offices financing independent and studio-adjacent film.",
                    cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed",
                ),
                cls="mb-14",
            ),
            Div(
                *[_product_card(n, t, b) for n, t, b in PRODUCTS],
                cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        id="products",
        cls="py-14 md:py-20 lg:py-28 border-b border-line",
    )


# ---------------------------------------------------------------------------
# How it works (3 steps)
# ---------------------------------------------------------------------------

STEPS = [
    ("01", "Originate & underwrite",
     "Drop a project package into Monika. The chat agent spins up a deal record, pulls comparable titles from TMDB / OMDB, and generates a first-pass underwriting view across budget, cast, territory and collateral type."),
    ("02", "Stress-test & structure",
     "Run AI-driven sales estimates, production risk scoring and smart budgeting side-by-side. ML credit scoring (Pre-Sales, Gap, Tax Credit) gives you a portfolio-grade view on a single deal — not just a one-off opinion."),
    ("03", "Close & manage",
     "The data room, closing checklists, transactions ledger and communications all live in the same workspace. Investment committee, sales and production accountant work off one source of truth."),
]


def _how():
    return Section(
        Div(
            Div(
                _eyebrow("How it works"),
                _heading(2, "From script package to closed deal — without leaving Monika.", cls="mt-4 max-w-4xl"),
                cls="mb-14",
            ),
            Div(
                *[
                    Div(
                        Div(
                            Div(num, cls="font-mono text-xs tracking-widest text-accent"),
                            cls="md:w-24 shrink-0",
                        ),
                        Div(
                            _heading(3, title, cls="mb-3"),
                            P(body, cls="text-ink-muted leading-relaxed"),
                            cls="flex-1",
                        ),
                        cls="flex flex-col md:flex-row gap-6 py-10",
                    )
                    for num, title, body in STEPS
                ],
                cls="divide-y divide-line border-y border-line",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        id="how",
    )


# ---------------------------------------------------------------------------
# Slate (Ashland Hill projects, real titles + posters)
# ---------------------------------------------------------------------------

# Real Ashland Hill project slate, scraped from ashland-hill.com/projects.
# Each entry is (title, poster_url). Posters are hot-linked to the canonical
# Ashland Hill CDN.
PROJECTS = [
    ("The Magic Faraway Tree", "https://ashland-hill.com/wp-content/uploads/2026/02/MFAT.jpg"),
    ("Eyes In The Trees",      "https://ashland-hill.com/wp-content/uploads/2025/05/eye-in-the-trees.jpg"),
    ("Harvest",                "https://ashland-hill.com/wp-content/uploads/2024/08/Harvest_Poster_2_AD.jpg"),
    ("Skyline Warpath",        "https://ashland-hill.com/wp-content/uploads/2025/09/skyline_vertical_final_370x545.png"),
    ("Return to Silent Hill",  "https://ashland-hill.com/wp-content/uploads/2024/02/poster-return-to-silent-hill.jpg"),
    ("The Absence of Eden",    "https://ashland-hill.com/wp-content/uploads/2024/03/AOE_1SH_FM2_LR.jpg"),
    ("Tornado",                "https://ashland-hill.com/wp-content/uploads/2024/05/tornado.jpg"),
    ("Young Werther",          "https://ashland-hill.com/wp-content/uploads/2024/07/Young-Werther.png"),
    ("Sneaks",                 "https://ashland-hill.com/wp-content/uploads/2025/03/sneaks.jpg"),
    ("Into The Deep",          "https://ashland-hill.com/wp-content/uploads/2025/09/shark_vertical_370x545.png"),
    ("Chief of Station",       "https://ashland-hill.com/wp-content/uploads/2023/05/poster-7-370x545-1.jpg"),
    ("The Mother and The Bear","https://ashland-hill.com/wp-content/uploads/2026/04/EP_TMATB_Cineplex_1080x1600-1.jpg"),
    ("Skyline Radial",         "https://ashland-hill.com/wp-content/uploads/2023/05/poster-8-370x545-1.jpg"),
    ("The Crow",               "https://ashland-hill.com/wp-content/uploads/2024/03/the-crow-24.jpg"),
    ("Duchess",                "https://ashland-hill.com/wp-content/uploads/2024/05/Duchess.png"),
    ("3 Days in Malay",        "https://ashland-hill.com/wp-content/uploads/2023/08/3-days-vp.jpg"),
    ("The Flood",              "https://ashland-hill.com/wp-content/uploads/2023/05/poster-11-370x545-1.jpg"),
    ("Fast Charlie",           "https://ashland-hill.com/wp-content/uploads/2023/12/poster-17.jpg"),
    ("57 Seconds",             "https://ashland-hill.com/wp-content/uploads/2023/08/57-seconds-vp.jpg"),
    ("Deep Fear",              "https://ashland-hill.com/wp-content/uploads/2023/05/poster-9-370x545-1.jpg"),
    ("The Lair",               "https://ashland-hill.com/wp-content/uploads/2024/04/The-Lair.jpg"),
]


def _poster_card(title, src):
    return A(
        Article(
            Img(src=src, alt=title, cls="poster rounded-xl border border-line"),
            Div(
                P(title, cls="text-ink text-sm font-medium leading-tight"),
                cls="mt-3",
            ),
            cls="poster-card",
        ),
        href=PROJECTS_URL,
        target="_blank",
        rel="noopener",
        cls="block",
    )


def _slate_section():
    return Section(
        Div(
            Div(
                Div(
                    _eyebrow("Slate"),
                    _heading(2, "The slate Monika was built on.", cls="mt-4 max-w-3xl"),
                    P(
                        "Ashland Hill projects are as diverse as the filmmakers who bring them to us — from franchise tentpoles to authentic genre pieces and groundbreaking independent film. Monika is the underwriting and portfolio workspace built around exactly this kind of slate. A selection of recent projects below; the full archive lives at ",
                        A("ashland-hill.com/projects", href=PROJECTS_URL, target="_blank", rel="noopener",
                          cls="text-ink underline decoration-accent/50 underline-offset-4 hover:text-accent"),
                        ".",
                        cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed",
                    ),
                    cls="md:max-w-3xl",
                ),
                cls="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-4",
            ),
            Div(
                *[_poster_card(t, src) for t, src in PROJECTS],
                cls="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-5",
            ),
            Div(
                _btn("Visit the project archive", href=PROJECTS_URL, primary=False, target="_blank"),
                cls="mt-10",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        id="slate",
        cls="py-14 md:py-20 lg:py-28 border-t border-line bg-bg-elevated/40",
    )


# ---------------------------------------------------------------------------
# Team (real Ashland Hill team)
# ---------------------------------------------------------------------------

# Real team data scraped from ashland-hill.com — name, role, headshot URL.
TEAM = [
    ("Joe Simpson",       "Managing Partner",                              "https://ashland-hill.com/wp-content/uploads/2023/05/team_5.1.jpg"),
    ("Simon Williams",    "Managing Partner",                              "https://ashland-hill.com/wp-content/uploads/2023/05/team_8.jpg"),
    ("Joe Jenckes",       "Senior Vice President, Production",             "https://ashland-hill.com/wp-content/uploads/2023/05/team_3.jpg"),
    ("Juliana Lubin",     "Senior Vice President, Investments",            "https://ashland-hill.com/wp-content/uploads/2023/05/team_4.jpg"),
    ("Andy Wang",         "Vice President, Investments",                   "https://ashland-hill.com/wp-content/uploads/2023/05/team_7.jpg"),
    ("Luigi Spitaleri",   "Vice President, Business Development & Strategy", "https://ashland-hill.com/wp-content/uploads/2024/10/Luigi-bw-2.jpg"),
    ("Merrick Stoller",   "Manager, Production",                           "https://ashland-hill.com/wp-content/uploads/2023/05/team_6.jpg"),
    ("Tre Caine",         "Associate, Finance and Operations",             "https://ashland-hill.com/wp-content/uploads/2025/02/Tre-Headshot.jpg"),
    ("Matthew Chausse",   "Consultant, Production",                        "https://ashland-hill.com/wp-content/uploads/2023/05/team_2.jpg"),
    ("Daemon Hillin",     "Consultant",                                    "https://ashland-hill.com/wp-content/uploads/2024/08/Daemon.jpg"),
    ("Sherry Angelique",  "Executive Assistant",                           "https://ashland-hill.com/wp-content/uploads/2024/05/Sherry-Headshot.jpeg"),
]


def _team_card(name, role, src):
    return Article(
        Img(src=src, alt=name, cls="team-photo rounded-xl border border-line"),
        Div(
            H4(name, cls="text-ink text-base font-medium mt-4"),
            P(role, cls="text-accent text-xs font-mono mt-1 leading-snug"),
            cls="px-1",
        ),
        cls="",
    )


def _team_section():
    return Section(
        Div(
            Div(
                _eyebrow("Team"),
                _heading(2, "Meet the Ashland Hill team.", cls="mt-4 max-w-3xl"),
                P(
                    "The team behind Monika is the same team that closes Ashland Hill's deals — international, spanning five countries, with decades of institutional and private film-finance experience.",
                    cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed",
                ),
                cls="mb-14",
            ),
            Div(
                *[_team_card(n, r, s) for n, r, s in TEAM],
                cls="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        id="team",
        cls="py-14 md:py-20 lg:py-28 border-t border-line",
    )


# ---------------------------------------------------------------------------
# Brought to you by Ashland Hill
# ---------------------------------------------------------------------------

def _ashland():
    return Section(
        Div(
            Div(
                Div(
                    _eyebrow("Brought to you by Ashland Hill"),
                    _heading(2, "A Santa Monica film-finance practice — now shipping its own software.", cls="mt-4 max-w-3xl"),
                    P(
                        "Ashland Hill Media Finance provides the capital required to help producers, filmmakers and storytellers turn their visions into reality. The team has closed hundreds of deals and deployed billions of dollars to independent film and TV — partnered with institutional investors and some of the industry's most experienced deal-closers.",
                        cls="mt-6 text-ink-muted text-lg max-w-2xl leading-relaxed",
                    ),
                    P(
                        "We're more than financiers — we're cinephiles with hands-on experience producing our own projects, so we know the process, the pain points, and how to get over, around and through them. Monika is the operating system we built for ourselves, and now offer to other capital providers and producers who want the same underwriting and portfolio discipline.",
                        cls="mt-4 text-ink-muted text-lg max-w-2xl leading-relaxed",
                    ),
                    Div(
                        _btn("Visit ashland-hill.com", href=PARENT_URL, primary=True, target="_blank"),
                        _btn("Sign in to Monika", href="/login", primary=False),
                        cls="mt-8 flex items-center gap-3 flex-wrap",
                    ),
                    cls="md:w-3/5",
                ),
                Div(
                    Div(
                        Div(
                            Span("◐", cls="text-accent text-2xl"),
                            Span("Ashland Hill", cls="ml-3 text-ink font-medium"),
                            cls="flex items-center mb-6",
                        ),
                        Div(
                            P("Santa Monica, California", cls="text-ink text-sm"),
                            P("Pacific time-zone media finance", cls="text-ink-dim text-xs mt-1"),
                            cls="mb-6",
                        ),
                        Ul(
                            Li(_pill("Pre-sales lending"), cls="mb-2"),
                            Li(_pill("Gap finance"), cls="mb-2"),
                            Li(_pill("Tax-credit lending"), cls="mb-2"),
                            Li(_pill("Minimum guarantees"), cls="mb-2"),
                            Li(_pill("Equity participation")),
                            cls="space-y-1",
                        ),
                        Div(
                            A(
                                Span("ashland-hill.com", cls="text-sm"),
                                Span("→", cls="text-sm"),
                                href=PARENT_URL,
                                target="_blank", rel="noopener",
                                cls="inline-flex items-center gap-2 text-ink hover:text-accent transition-colors mt-8",
                            ),
                        ),
                        cls="p-8 rounded-2xl bg-bg-elevated border border-line h-full",
                    ),
                    cls="md:w-2/5",
                ),
                cls="flex flex-col md:flex-row gap-10 items-stretch",
            ),
            cls="max-w-7xl mx-auto px-5 md:px-6",
        ),
        id="ashland",
        cls="py-14 md:py-20 lg:py-28 border-t border-line bg-bg-elevated/40",
    )


# ---------------------------------------------------------------------------
# CTA
# ---------------------------------------------------------------------------

def _cta():
    return Section(
        Div(
            Div(
                _eyebrow("Get started"),
                _heading(2, "Underwriting your next slate?", cls="mt-4 max-w-3xl"),
                P(
                    "Monika is in active use on Ashland Hill's own deal book. We open access selectively to producers, sales agents, lenders and family offices working in film and media finance.",
                    cls="mt-5 text-ink-muted text-lg max-w-2xl leading-relaxed",
                ),
                Div(
                    _btn("Request access", href="/register", primary=True),
                    _btn("Sign in", href="/login", primary=False),
                    cls="mt-8 flex items-center gap-3 flex-wrap",
                ),
                cls="max-w-7xl mx-auto px-6 py-20 md:py-28 relative z-10",
            ),
            Div(cls="absolute inset-0 bg-gradient-to-br from-accent/15 via-transparent to-sun-4/10 pointer-events-none"),
            cls="relative border-y border-line bg-bg-elevated/60 overflow-hidden",
        ),
    )


# ---------------------------------------------------------------------------
# Public renderer
# ---------------------------------------------------------------------------

def landing_page():
    """Render the Monika public landing page (HTML response)."""
    head_children = [
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Meta(name="description", content=TAGLINE),
        Title(f"{SITE_NAME} — {PARENT_NAME}"),
        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap",
        ),
        Script(src="https://cdn.tailwindcss.com"),
        Script(NotStr(TAILWIND_CONFIG)),
        Style(LANDING_CSS),
    ]
    body_children = [
        _navbar(),
        Main(
            _hero(),
            _products_section(),
            _how(),
            _slate_section(),
            _team_section(),
            _ashland(),
            _cta(),
            cls="min-h-screen",
        ),
        _footer(),
    ]
    return Html(
        Head(*head_children),
        Body(*body_children, cls="bg-bg text-ink font-sans antialiased"),
        lang="en",
    )
