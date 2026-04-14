#!/usr/bin/env python3
"""Generate PDF version of the AHMF User Stories Questionnaire."""

import csv
import os
from fpdf import FPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "user_stories_questionnaire.csv")
PDF_PATH = os.path.join(SCRIPT_DIR, "user_stories_questionnaire.pdf")

# Open questions per module (from the MD questionnaire)
OPEN_QUESTIONS = {
    "Deal Pipeline": [
        "What deal statuses do you actually use beyond pipeline/active/closed/declined?",
        "What fields are missing from the current deal form that you need for your workflow?",
        "How many deals does your team typically manage concurrently?",
        "Do you need multi-currency deal amounts (e.g., EUR deal with USD reporting)?",
        "What does your current deal approval process look like (number of approvers, stages)?",
        "Do you track deal-level P&L (revenue vs. costs) — if so, what line items matter?",
    ],
    "Contacts": [
        "What CRM or system do you currently use for contact management?",
        "Do you need to track organizational hierarchies (parent company, subsidiaries)?",
        "What contact types are missing from the current list?",
        "How important is deduplication (same person at multiple companies)?",
        "Do you track contact sentiment or relationship health scores?",
    ],
    "Sales & Collections": [
        "How many territories do you typically sell per film?",
        "What collection payment terms are standard (30/60/90 days, milestone-based)?",
        "Do you need to track holdbacks, reserves, or escrow amounts?",
        "What does your waterfall structure look like (commission splits, priority of payments)?",
        "How do you currently handle FX risk on international collections?",
    ],
    "Credit Rating": [
        "Do you currently rate counterparties? If so, what methodology?",
        "What factors matter most when assessing a distributor's creditworthiness?",
        "Would you integrate external credit data (D&B, Moody's) or rely on internal scoring?",
        "How often do you re-rate a counterparty?",
        "Do you set credit limits per counterparty?",
    ],
    "Accounting": [
        "What accounting system do you use (QuickBooks, Xero, SAP, custom)?",
        "Do you need journal entry format (debit/credit) or is a simple ledger sufficient?",
        "What reporting periods matter (monthly, quarterly, annual)?",
        "Do you accrue interest daily, monthly, or at maturity?",
        "Do you need GL account mapping for transactions?",
    ],
    "Communications": [
        "Do you use email, Slack, or another tool for deal-related communications today?",
        "How many people are typically involved in a deal (internal team)?",
        "Do you need recurring tasks (e.g., quarterly compliance checks)?",
        "Would you want to send emails directly from the platform or just track internal notes?",
    ],
    "Sales Estimates": [
        "How many comp films do you typically use when building a sales estimate?",
        "What data sources do you trust for actual sales figures?",
        "Do you estimate by territory, by platform (theatrical, SVOD, AVOD), or both?",
        "How often do estimates get revised during a deal lifecycle?",
        "Do you share estimates with investors or distributors — if so, what format?",
    ],
    "Risk Scoring": [
        "What risk dimensions are missing from the current six?",
        "How do you quantify production risk today (spreadsheet, gut feel, external consultant)?",
        "Do you share risk reports with insurers or completion guarantors?",
        "What risk score threshold would trigger a deal rejection or additional due diligence?",
        "Are there regulatory requirements for risk documentation in your jurisdiction?",
    ],
    "Smart Budget": [
        "What budgeting tool do you use today (Movie Magic, Excel, Hot Budget)?",
        "What level of line-item detail do you need (top-sheet only, or account-level)?",
        "How important is it for AI budgets to follow a specific chart of accounts?",
        "Do you track actual vs. budget during production (cost reports)?",
        "What contingency percentage is standard for your projects?",
    ],
    "Scheduling": [
        "What scheduling tool do you use today (Movie Magic, StudioBinder, Gorilla, Excel)?",
        "How detailed does the schedule need to be (scenes, setups, cast availability per day)?",
        "Do you need to track actor availability / hold days?",
        "How often does the schedule change once shooting begins?",
        "Who consumes the schedule (director, AD, department heads)?",
    ],
    "Soft Funding": [
        "How many incentive programs do you typically evaluate per project?",
        "Do you use consultants or brokers for incentive applications?",
        "What countries/regions are most important for your slate?",
        "How critical is stacking (combining multiple programs)?",
        "Do you need to track application status and deadlines?",
    ],
    "Data Room": [
        "What items are missing from the current 20-item checklist?",
        "Do you use a virtual data room today (Intralinks, Datasite, Google Drive)?",
        "How many parties typically need data room access per deal?",
        "Do you need watermarking, download controls, or DRM on documents?",
        "How long does a typical deal closing take (weeks, months)?",
    ],
    "Audience Intel": [
        "Do you currently use audience research tools (NRG, Screen Engine, PostTrak)?",
        "At what stage do you typically start marketing planning?",
        "What P&A-to-production-budget ratio is standard for your films?",
        "Do you need social media analytics integration?",
        "How do you measure marketing effectiveness?",
    ],
    "Talent Intel": [
        "What talent databases do you use today (IMDB Pro, agency submissions, internal)?",
        "How do you currently assess an actor's bankability or sales value?",
        "Do you need to track talent relationships (agent, manager, lawyer, publicist)?",
        "How important is social media following as a talent valuation metric?",
        "Do you package talent before or after securing financing?",
    ],
    "Platform & UX": [
        "How many users would typically access the platform per organization?",
        "What user roles exist in your team (originator, analyst, legal, admin)?",
        "What devices/browsers do you primarily use?",
        "Do you need offline access or is always-online acceptable?",
        "What integrations matter most (email, Slack, accounting software, cloud storage)?",
        "How important is white-labeling (custom branding for your firm)?",
    ],
    "Reporting": [
        "What reports do you produce today and how often?",
        "Who are the primary report consumers (board, investors, internal team)?",
        "What format do stakeholders prefer (PDF, Excel, online dashboard)?",
        "Do you need comparison across time periods (QoQ, YoY)?",
        "What KPIs matter most for your business?",
    ],
}

# Colors
BLUE = (0, 102, 204)
DARK = (30, 41, 59)
MEDIUM = (71, 85, 105)
LIGHT_BG = (248, 250, 252)
WHITE = (255, 255, 255)
TABLE_HEADER_BG = (15, 23, 42)
TABLE_HEADER_FG = (255, 255, 255)
TABLE_ROW_ALT = (241, 245, 249)
STATUS_BUILT = (22, 163, 74)
STATUS_PARTIAL = (202, 138, 4)
STATUS_NOT_STARTED = (148, 163, 184)


def sanitize(text):
    """Replace unicode chars that Helvetica can't encode."""
    return (
        text.replace("\u2014", "-")   # em-dash
            .replace("\u2013", "-")   # en-dash
            .replace("\u2018", "'")   # left single quote
            .replace("\u2019", "'")   # right single quote
            .replace("\u201c", '"')   # left double quote
            .replace("\u201d", '"')   # right double quote
            .replace("\u2026", "...")  # ellipsis
    )


class UserStoryPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return  # Cover page has custom header
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*MEDIUM)
        self.cell(0, 8, "AHMF User Stories Questionnaire", align="L")
        self.cell(0, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*MEDIUM)
        self.cell(0, 10, "Ashland Hill Media Finance  |  Confidential", align="C")

    def cover_page(self):
        self.add_page()
        self.ln(30)
        # Title
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*BLUE)
        self.cell(0, 16, "AHMF User Stories", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*DARK)
        self.cell(0, 12, "Questionnaire", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)
        # Subtitle
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*MEDIUM)
        self.cell(0, 8, sanitize("Ashland Hill Media Finance — Film Financing Operating System"), align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, "Version 1.0  |  April 2026", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(16)
        # Divider
        self.set_draw_color(*BLUE)
        self.set_line_width(0.5)
        cx = self.w / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(16)
        # Purpose
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        purpose_lines = [
            "Purpose: Validate current features, discover gaps, and prioritize",
            "roadmap items with users and stakeholders.",
            "",
            "For each user story, please fill in:",
            "  - Priority: Critical / High / Medium / Low / Not Needed",
            "  - Your Notes: Pain points, missing fields, workflow changes, edge cases",
        ]
        for line in purpose_lines:
            self.cell(0, 6, line, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(12)
        # Stats
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*BLUE)
        self.cell(0, 8, "120 User Stories  |  16 Modules  |  80+ Open Questions", align="C", new_x="LMARGIN", new_y="NEXT")

    def summary_page(self, module_stats):
        self.add_page()
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*DARK)
        self.cell(0, 12, "Summary", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        col_widths = [70, 25, 25, 25, 25]
        headers = ["Module", "Stories", "Built", "Partial", "Not Started"]

        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*TABLE_HEADER_BG)
        self.set_text_color(*TABLE_HEADER_FG)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C" if i > 0 else "L")
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 9)
        totals = [0, 0, 0, 0]
        for idx, (module, stats) in enumerate(module_stats.items()):
            if idx % 2 == 0:
                self.set_fill_color(*TABLE_ROW_ALT)
            else:
                self.set_fill_color(*WHITE)
            self.set_text_color(*DARK)
            self.cell(col_widths[0], 7, module, border=1, fill=True)
            vals = [stats["total"], stats["built"], stats["partial"], stats["not_started"]]
            for j, v in enumerate(vals):
                totals[j] += v
                self.cell(col_widths[j + 1], 7, str(v), border=1, fill=True, align="C")
            self.ln()

        # Totals
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*LIGHT_BG)
        self.set_text_color(*DARK)
        self.cell(col_widths[0], 8, "TOTAL", border=1, fill=True)
        for j, t in enumerate(totals):
            self.cell(col_widths[j + 1], 8, str(t), border=1, fill=True, align="C")
        self.ln()

    def module_section(self, module_name, stories):
        self.add_page()
        # Module title
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, module_name, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

        # Table
        col_widths = [12, 130, 30, 25, 60]
        headers = ["#", "User Story", "Role", "Status", "Priority / Notes"]

        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(*TABLE_HEADER_BG)
        self.set_text_color(*TABLE_HEADER_FG)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C" if i in (0, 3, 4) else "L")
        self.ln()

        self.set_font("Helvetica", "", 7.5)
        for idx, story in enumerate(stories):
            if idx % 2 == 0:
                self.set_fill_color(*TABLE_ROW_ALT)
            else:
                self.set_fill_color(*WHITE)

            # Calculate row height based on story text length
            story_text = story["User Story"]
            # Remove "As a ..." prefix for brevity, keep the want and so-that
            story_text = story_text.replace(f'As a {story["Role"].lower()}, ', "").replace(f'As a {story["Role"]}, ', "").replace(f'As an {story["Role"].lower()}, ', "").replace(f'As an {story["Role"]}, ', "")
            story_text = sanitize(story_text)

            # Estimate lines needed
            chars_per_line = 85
            lines_needed = max(1, (len(story_text) // chars_per_line) + 1)
            row_h = max(7, lines_needed * 4.5)

            # Check page break
            if self.get_y() + row_h > self.h - 25:
                self.add_page()
                self.set_font("Helvetica", "B", 8)
                self.set_fill_color(*TABLE_HEADER_BG)
                self.set_text_color(*TABLE_HEADER_FG)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 8, h, border=1, fill=True, align="C" if i in (0, 3, 4) else "L")
                self.ln()
                self.set_font("Helvetica", "", 7.5)
                if idx % 2 == 0:
                    self.set_fill_color(*TABLE_ROW_ALT)
                else:
                    self.set_fill_color(*WHITE)

            self.set_text_color(*DARK)
            y_start = self.get_y()
            x_start = self.get_x()

            # ID
            self.cell(col_widths[0], row_h, story["ID"], border=1, fill=True, align="C")
            # Story text (multi-cell)
            x_story = self.get_x()
            self.multi_cell(col_widths[1], row_h / lines_needed, story_text, border=1, fill=True)
            y_after = self.get_y()
            actual_h = y_after - y_start

            # Go back to draw remaining cells at correct height
            self.set_xy(x_story + col_widths[1], y_start)

            # Role
            self.set_font("Helvetica", "", 7)
            self.cell(col_widths[2], actual_h, story["Role"], border=1, fill=True, align="C")

            # Status with color
            status = story["Status"]
            if status == "Built":
                self.set_text_color(*STATUS_BUILT)
            elif status == "Partial":
                self.set_text_color(*STATUS_PARTIAL)
            else:
                self.set_text_color(*STATUS_NOT_STARTED)
            self.set_font("Helvetica", "B", 7)
            self.cell(col_widths[3], actual_h, status, border=1, fill=True, align="C")

            # Notes (empty for user to fill)
            self.set_text_color(*MEDIUM)
            self.set_font("Helvetica", "I", 7)
            self.cell(col_widths[4], actual_h, "", border=1, fill=True)

            self.set_text_color(*DARK)
            self.set_font("Helvetica", "", 7.5)
            self.set_xy(x_start, y_start + actual_h)

        # Open questions — keep header + at least first 2 questions together
        questions = OPEN_QUESTIONS.get(module_name, [])
        if questions:
            self.ln(4)
            # Need ~12mm per question + 12mm for header; check if header + 2 Qs fit
            min_block = 12 + 2 * 12
            if self.get_y() + min_block > self.h - 20:
                self.add_page()

            self.set_font("Helvetica", "B", 11)
            self.set_text_color(*DARK)
            self.cell(0, 8, sanitize(f"Open Questions - {module_name}"), new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

            self.set_font("Helvetica", "", 9)
            self.set_text_color(*MEDIUM)
            for i, q in enumerate(questions, 1):
                if self.get_y() + 12 > self.h - 20:
                    self.add_page()
                self.cell(8, 6, f"{i}.")
                self.cell(0, 6, sanitize(q), new_x="LMARGIN", new_y="NEXT")
                # Answer line
                self.set_draw_color(200, 200, 200)
                self.set_line_width(0.2)
                y = self.get_y() + 1
                self.line(self.l_margin + 8, y, self.w - self.r_margin, y)
                self.ln(4)


def main():
    # Read CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Group by module
    modules = {}
    for row in rows:
        mod = row["Module"]
        modules.setdefault(mod, []).append(row)

    # Compute stats
    module_stats = {}
    for mod, stories in modules.items():
        built = sum(1 for s in stories if s["Status"] == "Built")
        partial = sum(1 for s in stories if s["Status"] == "Partial")
        not_started = sum(1 for s in stories if s["Status"] in ("Not Started", "Planned"))
        module_stats[mod] = {
            "total": len(stories),
            "built": built,
            "partial": partial,
            "not_started": not_started,
        }

    # Build PDF
    pdf = UserStoryPDF()
    pdf.cover_page()
    pdf.summary_page(module_stats)
    for mod, stories in modules.items():
        pdf.module_section(mod, stories)

    pdf.output(PDF_PATH)
    print(f"PDF generated: {PDF_PATH}")


if __name__ == "__main__":
    main()
