# AHMF — Ashland Hill Media Finance AI

Film financing operating system with AI-driven intelligence tools.

## Stack

- **Python 3.13**, virtualenv at `.venv/`
- **FastHTML** 3-pane agentic UI (`app.py`, port 5010)
- **LangGraph** + XAI Grok-3 for AI chat agents
- **PostgreSQL** (`ahmf` schema on finespresso_db)
- **HTMX + WebSocket** for real-time streaming

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `modules/` | Product module routes (deals, contacts, sales, estimates, etc.) |
| `agents/` | LangGraph agents and tool definitions |
| `agents/tools/` | Structured tool functions for agents |
| `utils/` | Core utilities (db, auth, TMDB, OMDB, PDF extraction) |
| `utils/agui/` | AG-UI chat engine (vendored from alpatrade, adapted) |
| `sql/` | Database migrations |
| `config/` | App settings |
| `docs/` | Product roadmap PDF |

## Products (from Roadmap)

1. **Film Financing OS** (deep) — Deals, Sales & Collections, Credit Rating, Accounting, Contacts, Communications
2. **Sales Estimates Generator** (deep) — TMDB/OMDB comp analysis, territory MG projections, box office forecasting
3. Production Risk Scoring (scaffold)
4. Smart Budgeting Tool (scaffold)
5. Automated Production Scheduling (scaffold)
6. Soft Funding Discovery Engine (scaffold)
7. Deal Closing & Data Room Automation (scaffold)
8. Audience & Marketing Intelligence (scaffold)
9. Talent Intelligence (scaffold)

## Secrets Policy

**NEVER copy, persist, log, or document actual secret values.** API keys, tokens, passwords, and connection strings from `.env` must only be used transiently during runtime.
- Do not write secret values into source files, docs, markdown, YAML, or memory files
- Do not include secrets in commit messages, comments, or debug output
- Do not hardcode API keys — always read from environment variables
- Reference secrets by variable name only (e.g. `XAI_API_KEY=...`)
- Before committing, verify no secrets appear in `git diff` output

## Required Environment Variables (.env)

```
DB_URL=...                    # PostgreSQL connection string
XAI_API_KEY=...               # XAI Grok LLM
TMDB_API_KEY=...              # TMDB movie database
TMDB_API_READ_TOKEN=...       # TMDB read access token
OMDB_API_KEY=...              # OMDB movie data
TAVILY_API_KEY=...            # Tavily web search
JWT_SECRET=...                # JWT signing secret
ENCRYPTION_KEY=...            # Fernet encryption key
```

## Authentication

- **Email/password** registration + login with bcrypt password hashing
- **JWT tokens** for session management (7-day expiry)
- **Data isolation**: All tables have `created_by` / `user_id` column
- **Auth module**: `utils/auth.py`

## Running

```bash
# Activate venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run SQL migrations
psql $DB_URL -f sql/01_create_schema.sql
# ... run all sql/*.sql files in order

# Start the app
python app.py    # port 5010
```

## Chat Commands

```
deal:list                    List all deals
deal:new                     Create new deal
deal:DEAL_ID                 View deal details
contact:search NAME          Search contacts
estimate:TITLE               Generate sales estimate
portfolio                    Portfolio overview
help                         Show available commands
```

## Architecture

- **3-pane layout**: Left sidebar (260px nav) | Center (chat + module views) | Right (380px detail canvas)
- **Command interceptor**: Colon-syntax routed to handlers, free-form to LangGraph AI
- **WebSocket streaming**: LangGraph astream_events(v2) for real-time AI responses
- **HTMX module views**: Product pages swapped into center pane via hx-get/hx-swap
