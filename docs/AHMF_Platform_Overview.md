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

**The core operating system — 6 fully operational modules**

| Module | Function |
|--------|----------|
| Deals | Pipeline dashboard, deal structuring, performance tracking |
| Contacts | Counterparty profiles, relationship mapping |
| Sales & Collections | Territory contracts, MG tracking, collection payments, variance analysis |
| Credit Rating | AI-powered counterparty scoring (AAA-CCC tiers), payment reliability, risk factors |
| Accounting | Transaction ledger, disbursements/repayments/fees/interest, multi-currency, net position |
| Communications | Deal-linked messages & tasks, due dates, completion tracking, overdue flagging |

![Deal Pipeline](static/guide/02_deals.png)

---

## Slide 3b: Sales & Collections

**Territory-based revenue tracking and collateral monitoring**

- Sales contracts linked to deals and distributors
- Territory-based MG (Minimum Guarantee) commitments
- Collection payment recording with due dates
- Status tracking: pending, received, overdue
- Variance analysis: projected vs actual collections

![Sales & Collections](static/guide/05_sales.png)

---

## Slide 3c: Credit Rating

**AI-powered counterparty strength assessment**

- Credit Score (0-100) and Payment Reliability (0-100)
- Risk Tier classification (AAA through CCC)
- Factor analysis: track record, financial stability, market position, payment history
- Per-contact rating history

![Credit Rating](static/guide/17_credit.png)

---

## Slide 3d: Accounting

**Transaction-level financial integrity**

- Full transaction ledger across all deals
- Types: Disbursement, Repayment, Fee, Interest, Adjustment
- Multi-currency support (7 currencies)
- Net position tracking and counterparty audit trail

![Accounting](static/guide/18_accounting.png)

---

## Slide 3e: Communications

**Execution control layer for deal teams**

- Deal-linked messages, tasks, and notifications
- Task assignment with due dates and deadlines
- Interactive checkboxes for task completion
- Overdue task flagging

![Communications](static/guide/19_comms.png)

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

**18 AI tools accessible via natural language or structured commands**

The AI assistant can:
- Look up deals, portfolio stats, sales contracts, transactions, messages
- Search contacts and generate credit ratings
- Query TMDB/OMDB for film comparisons
- Analyze production risk, generate budgets and schedules
- Search global tax incentives
- Recommend cast with package simulations
- Predict audience segments and marketing strategy

![Chat Commands](static/guide/15_chat_help.png)

---

## Slide 13: Product Roadmap

**From A (Single-Picture Lender) to B (Integrated Media Platform)**

```
1. End-to-End Film Financing OS         [LIVE - 6 modules]
2. Sales Estimates Generator             [LIVE]
3. Production Risk Scoring System        [LIVE]
4. Smart Budgeting Tool                  [LIVE]
5. Automated Production Scheduling       [LIVE]
6. Soft Funding Discovery Engine         [LIVE]
7. Deal Closing & Data Room Automation   [LIVE]
8. Audience & Marketing Intelligence     [LIVE]
9. Talent Intelligence                   [LIVE]
```

All 9 products fully operational — no placeholders remaining.

---

## Slide 14: Technical Summary

| Component | Detail |
|-----------|--------|
| Frontend | FastHTML + HTMX (server-rendered, no React) |
| AI Engine | LangGraph + XAI Grok-3 (18 tools) |
| Database | PostgreSQL (28 tables, `ahmf` schema) |
| Film Data | TMDB + OMDB APIs |
| Auth | Email/password + JWT sessions |
| Deployment | Docker + Coolify |
| Test Suite | 30 automated tests |

---

## Slide 15: Next Steps

1. **Sales Estimate Pipeline**: 5-node LangGraph pipeline (analyze > comps > territory > forecast > report)
2. **PDF Script Ingestion**: Upload screenplays for automated analysis
3. **Closing Workflow Automation**: Drawdown requests, digital signatures
4. **Portfolio Analytics Dashboard**: IRR tracking, collection monitoring, variance analysis
5. **Investor Reporting**: Automated LP/capital partner reports
6. **Mobile Responsive**: Tablet-optimized layout for on-the-go deal review

---

*Ashland Hill Media Finance — Private & Confidential*
*Contact: Joe Simpson, Managing Partner | Simon Williams, Managing Partner*
