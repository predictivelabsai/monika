# Ashland Hill Media Finance
## Technology & AI-Driven Solutions Platform

### FY2026 Q1 — Product Demo

---

## Slide 1: Platform Vision

**From Single-Picture Lender to Integrated Media Platform**

AHMF is a centralized, AI-driven operating system purpose-built for private credit and film finance. It replaces fragmented spreadsheets and siloed workflows with a unified data architecture.

- 9 product modules — all operational
- AI-powered intelligence across the full financing lifecycle
- Real-time portfolio visibility and deal management
- Powered by LangGraph + XAI Grok-3 AI

---

## Slide 2: Platform Architecture

**3-Pane Agentic UI**

| Component | Purpose |
|-----------|---------|
| Left Sidebar | Navigation across all 9 product modules |
| Center Pane | AI Chat + module content views (HTMX) |
| Right Pane | AI thinking trace + deal detail canvas |

**Tech Stack:** FastHTML, PostgreSQL, LangGraph, TMDB/OMDB APIs, WebSocket streaming

![Welcome Screen](static/guide/01_welcome.png)

---

## Slide 3: Product 1 — Film Financing Operating System

**The iOS/Windows of Ashland Hill's Media Finance unit**

6 integrated modules managing the full deal lifecycle:

| Module | Function |
|--------|----------|
| Deals | Pipeline dashboard, deal structuring, performance tracking |
| Contacts | Counterparty profiles, relationship mapping |
| Sales & Collections | Territory-based revenue tracking, receivable monitoring |
| Credit Rating | Distributor/producer scoring, payment reliability |
| Accounting | Multi-account balance tracking, audit trail |
| Communications | Task assignment, milestone notifications |

**Key Metrics:** 2 deals, $20M total committed, Pipeline/Active tracking

![Deal Pipeline](static/guide/02_deals.png)

---

## Slide 4: Product 2 — Sales Estimates Generator

**Quantitative valuation intelligence for greenlight and collateral appraisal**

- Script ingestion with PDF parsing
- Genre + comp benchmarking via TMDB & OMDB
- Territory-level MG projections
- Box office forecasting (domestic + international)
- Confidence score / model reliability rating
- Exportable reports

**Data Sources:** TMDB (movie budgets, revenue, cast), OMDB (ratings, box office), Tavily (web search)

![Sales Estimates](static/guide/06_estimates.png)

---

## Slide 5: Product 3 — Production Risk Scoring

**"Moody's for execution risk"**

AI evaluates 6 risk dimensions (0-100 scale):

| Dimension | What It Measures |
|-----------|-----------------|
| Script Complexity | Locations, stunts, VFX density |
| Budget Feasibility | Budget vs comparable films |
| Schedule Risk | Shoot days vs scope |
| Jurisdictional Risk | Labor laws, permits, political stability |
| Crew/Talent Risk | Availability, reliability, concentration |
| Completion Risk | Overall probability of on-time, on-budget delivery |

**Output:** Overall score, risk tier (Low/Moderate/Elevated/High), mitigation recommendations

![Risk Assessment Form](static/guide/08_risk_form.png)

---

## Slide 6: Product 4 — Smart Budgeting Tool

**Generative budgeting logic + live cost intelligence**

- AI generates 3 scenarios: Low / Mid / High
- 8-12 line items per scenario across 6 categories
- Categories: Above-the-Line, Below-the-Line (Production), Below-the-Line (Post), Insurance & Legal, Financing Costs, Contingency
- Inputs: genre, cast tier, VFX level, shoot days, locations

![Smart Budget](static/guide/09_budget.png)

---

## Slide 7: Product 5 — Automated Production Scheduling

**Predictive production efficiency software**

- AI generates day-by-day shooting schedules
- Location clustering optimization (minimize company moves)
- Day/night scene grouping
- Actor availability and labor law compliance
- Scenario comparison (schedule A vs B)

![Scheduling](static/guide/10_schedule.png)

---

## Slide 8: Product 6 — Soft Funding Discovery Engine

**"Kayak for film incentives"**

- Database of 16+ global incentive programs across 11 countries
- Average rebate: 27.8%
- Filter by country, incentive type
- Built-in rebate calculator
- Programs: Georgia (30%), Ireland (32%), Colombia (40%), UK (25.5%), Hungary (30%), and more

![Soft Funding](static/guide/04_funding.png)

---

## Slide 9: Product 7 — Deal Closing & Data Room

**Infrastructure layer for streamlined closings**

- Auto-generated 20-item closing checklists
- 6 categories: Legal, Insurance, Financial, Distribution, Tax Incentives, Compliance
- Interactive progress tracking with checkboxes
- Document status monitoring
- Per-deal closing dashboards with progress bars

![Data Room Checklist](static/guide/13_checklist.png)

---

## Slide 10: Product 8 — Audience & Marketing Intelligence

**Campaign simulator meets audience heat map**

AI-powered analysis outputs:
- Audience segment prediction (3-5 segments with % share)
- Marketing channel allocation and spend estimates
- Release window optimization
- Platform strategy (theatrical, streaming, hybrid)
- Festival positioning recommendations

![Audience Intel](static/guide/11_audience.png)

---

## Slide 11: Product 9 — Talent Intelligence

**Taste graph meets market intelligence**

- Live TMDB actor/director search with popularity data
- AI cast recommendations scored on:
  - Heat Index (1-10, market popularity)
  - Genre Fit (1-10)
  - Salary Tier (Low/Mid/High/Premium)
  - International Sales Impact
- Package simulation: test cast combinations for projected revenue
- Comparable role analysis

![Talent Intel](static/guide/14_talent_search.png)

---

## Slide 12: AI Chat — The Intelligence Layer

**14 AI tools accessible via natural language or structured commands**

The AI assistant can:
- Look up and create deals
- Search contacts and distributors
- Query TMDB/OMDB for film comparisons
- Analyze production risk
- Generate budgets and schedules
- Search global tax incentives
- Recommend cast with package simulations
- Predict audience segments and marketing strategy

![Chat Commands](static/guide/15_chat_help.png)

---

## Slide 13: Product Roadmap

**From A (Single-Picture Lender) to B (Integrated Media Platform)**

```
1. End-to-End Film Financing OS         [LIVE]
2. Sales Estimates Generator             [LIVE]
3. Production Risk Scoring System        [LIVE]
4. Smart Budgeting Tool                  [LIVE]
5. Automated Production Scheduling       [LIVE]
6. Soft Funding Discovery Engine         [LIVE]
7. Deal Closing & Data Room Automation   [LIVE]
8. Audience & Marketing Intelligence     [LIVE]
9. Talent Intelligence                   [LIVE]
```

All 9 products operational. Foundation built for continued depth and integrations.

---

## Slide 14: Technical Summary

| Component | Detail |
|-----------|--------|
| Frontend | FastHTML + HTMX (server-rendered, no React) |
| AI Engine | LangGraph + XAI Grok-3 (14 tools) |
| Database | PostgreSQL (28 tables, `ahmf` schema) |
| Film Data | TMDB + OMDB APIs |
| Auth | Email/password + JWT sessions |
| Deployment | Docker + Coolify |
| Test Suite | 30 automated tests |

---

## Slide 15: Next Steps

1. **Deepen Product 1**: Full CRUD on Sales & Collections, Credit Rating, Accounting
2. **Sales Estimate Pipeline**: 5-node LangGraph pipeline (analyze > comps > territory > forecast > report)
3. **PDF Script Ingestion**: Upload screenplays for automated analysis
4. **Closing Workflow Automation**: Drawdown requests, digital signatures
5. **Portfolio Analytics Dashboard**: IRR tracking, collection monitoring, variance analysis
6. **Mobile Responsive**: Tablet-optimized layout for on-the-go deal review

---

*Ashland Hill Media Finance — Private & Confidential*
*Contact: Joe Simpson, Managing Partner*
