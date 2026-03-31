"""
AHMF Test Suite

Tests all key functionality: DB operations, auth, API integrations,
module tools, and command interceptor. Populates test data if needed
and writes results to test-data/*.json.

Usage: python tests/test_suite.py
"""

import sys, os, json, time, asyncio
from pathlib import Path

# Setup path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

RESULTS_DIR = ROOT / "test-data"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Test framework
# ---------------------------------------------------------------------------

_results = []
_pass = 0
_fail = 0


def test(name):
    """Decorator to register a test function."""
    def wrapper(fn):
        fn._test_name = name
        _tests.append(fn)
        return fn
    return wrapper

_tests = []


def run_test(fn):
    global _pass, _fail
    name = fn._test_name
    try:
        result = fn()
        _pass += 1
        status = "PASS"
        detail = result if isinstance(result, str) else "OK"
        print(f"  \033[32mPASS\033[0m  {name}")
    except Exception as e:
        _fail += 1
        status = "FAIL"
        detail = str(e)
        print(f"  \033[31mFAIL\033[0m  {name}: {e}")
    _results.append({"test": name, "status": status, "detail": detail})


def save_results(filename, data):
    """Write test data to JSON file."""
    path = RESULTS_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return str(path)


# ===========================================================================
# 1. Database Connection
# ===========================================================================

@test("DB connection")
def test_db_connection():
    from utils.db import get_pool
    pool = get_pool()
    from sqlalchemy import text
    with pool.get_session() as s:
        result = s.execute(text("SELECT 1")).scalar()
    assert result == 1
    return "Connected"


@test("DB schema tables exist")
def test_db_schema():
    from utils.db import get_pool
    from sqlalchemy import text
    pool = get_pool()
    with pool.get_session() as s:
        rows = s.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'ahmf' ORDER BY table_name"
        )).fetchall()
    tables = [r[0] for r in rows]
    expected = ["audience_reports", "budget_items", "budgets", "chat_conversations", "chat_messages",
                "checklist_items", "closing_checklists", "collections", "comp_films", "contact_activities",
                "contacts", "credit_ratings", "deal_approvals", "deal_balances", "deal_contacts",
                "deal_documents", "deal_incentives", "deals", "incentive_programs", "messages",
                "risk_assessments", "sales_contracts", "sales_estimates", "schedule_days", "schedules",
                "talent_reports", "transactions", "users"]
    missing = [t for t in expected if t not in tables]
    assert not missing, f"Missing tables: {missing}"
    save_results("db_tables.json", {"tables": tables, "count": len(tables)})
    return f"{len(tables)} tables"


# ===========================================================================
# 2. Auth
# ===========================================================================

@test("Auth: create user")
def test_auth_create_user():
    from utils.auth import create_user, get_user_by_email
    # Check if test user exists
    existing = get_user_by_email("test@ahmf.local")
    if existing:
        return "Test user already exists"
    user = create_user("test@ahmf.local", "testpass123", display_name="Test User")
    assert user is not None, "Failed to create user"
    save_results("auth_user.json", user)
    return f"Created {user['email']}"


@test("Auth: authenticate")
def test_auth_authenticate():
    from utils.auth import authenticate
    user = authenticate("test@ahmf.local", "testpass123")
    assert user is not None, "Authentication failed"
    assert user["email"] == "test@ahmf.local"
    return f"Authenticated {user['display_name']}"


@test("Auth: bad password fails")
def test_auth_bad_password():
    from utils.auth import authenticate
    user = authenticate("test@ahmf.local", "wrongpassword")
    assert user is None, "Bad password should fail"
    return "Correctly rejected"


@test("Auth: JWT create & decode")
def test_auth_jwt():
    from utils.auth import create_jwt_token, decode_jwt_token, get_user_by_email
    user = get_user_by_email("test@ahmf.local")
    token = create_jwt_token(user["user_id"], user["email"])
    assert token, "Token not created"
    payload = decode_jwt_token(token)
    assert payload is not None, "Token decode failed"
    assert payload["email"] == "test@ahmf.local"
    save_results("auth_jwt.json", {"token_length": len(token), "payload_keys": list(payload.keys())})
    return "JWT OK"


# ===========================================================================
# 3. Seed test data
# ===========================================================================

_test_deal_id = None
_test_contact_id = None

@test("Seed: create test deal")
def test_seed_deal():
    global _test_deal_id
    from utils.db import get_pool
    from sqlalchemy import text
    pool = get_pool()
    with pool.get_session() as s:
        existing = s.execute(text("SELECT deal_id FROM ahmf.deals WHERE title = 'Test Film Alpha' LIMIT 1")).fetchone()
        if existing:
            _test_deal_id = str(existing[0])
            return f"Already exists: {_test_deal_id[:8]}"
        result = s.execute(text("""
            INSERT INTO ahmf.deals (title, project_type, genre, status, loan_amount, currency,
                interest_rate, term_months, borrower_name, producer, director, cast_summary,
                budget, territory)
            VALUES ('Test Film Alpha', 'feature_film', 'Action', 'active', 15000000, 'USD',
                8.5, 24, 'Alpha Productions LLC', 'Jane Producer', 'John Director',
                'Actor A, Actor B, Actor C', 25000000, 'Domestic (US/Canada)')
            RETURNING deal_id
        """))
        _test_deal_id = str(result.scalar())
    save_results("seed_deal.json", {"deal_id": _test_deal_id, "title": "Test Film Alpha"})
    return f"Created deal {_test_deal_id[:8]}"


@test("Seed: create test contact")
def test_seed_contact():
    global _test_contact_id
    from utils.db import get_pool
    from sqlalchemy import text
    pool = get_pool()
    with pool.get_session() as s:
        existing = s.execute(text("SELECT contact_id FROM ahmf.contacts WHERE name = 'Test Distributor Corp' LIMIT 1")).fetchone()
        if existing:
            _test_contact_id = str(existing[0])
            return f"Already exists: {_test_contact_id[:8]}"
        result = s.execute(text("""
            INSERT INTO ahmf.contacts (name, company, role, email, contact_type, notes)
            VALUES ('Test Distributor Corp', 'DistCo International', 'Head of Sales',
                'dist@test.local', 'distributor', 'Test contact for regression suite')
            RETURNING contact_id
        """))
        _test_contact_id = str(result.scalar())
    save_results("seed_contact.json", {"contact_id": _test_contact_id})
    return f"Created contact {_test_contact_id[:8]}"


@test("Seed: second deal (pipeline)")
def test_seed_deal_pipeline():
    from utils.db import get_pool
    from sqlalchemy import text
    pool = get_pool()
    with pool.get_session() as s:
        existing = s.execute(text("SELECT deal_id FROM ahmf.deals WHERE title = 'Test Horror Beta' LIMIT 1")).fetchone()
        if existing:
            return "Already exists"
        s.execute(text("""
            INSERT INTO ahmf.deals (title, project_type, genre, status, loan_amount, budget, borrower_name, producer, director)
            VALUES ('Test Horror Beta', 'feature_film', 'Horror', 'pipeline', 5000000, 8000000,
                'Beta Films Inc', 'Producer B', 'Director B')
        """))
    return "Created"


# ===========================================================================
# 4. Deal tools
# ===========================================================================

@test("Tool: search_deals")
def test_search_deals():
    from app import search_deals
    result = search_deals("")
    assert "Deals" in result or "No deals" in result, f"Unexpected result: {result[:100]}"
    save_results("tool_search_deals.json", {"result": result})
    return f"{len(result)} chars"


@test("Tool: get_deal_detail")
def test_get_deal_detail():
    from app import get_deal_detail
    assert _test_deal_id, "No test deal ID"
    result = get_deal_detail(_test_deal_id)
    assert "Test Film Alpha" in result, f"Deal not found in result"
    save_results("tool_deal_detail.json", {"result": result})
    return "OK"


@test("Tool: get_portfolio_overview")
def test_portfolio_overview():
    from app import get_portfolio_overview
    result = get_portfolio_overview()
    assert "Portfolio" in result or "Total" in result, f"Unexpected: {result[:100]}"
    save_results("tool_portfolio.json", {"result": result})
    return "OK"


@test("Tool: search_contacts")
def test_search_contacts():
    from app import search_contacts
    result = search_contacts("Test")
    assert "Contacts" in result or "No contacts" in result
    save_results("tool_contacts.json", {"result": result})
    return "OK"


# ===========================================================================
# 5. External API integrations
# ===========================================================================

@test("TMDB: search movies")
def test_tmdb_search():
    from utils.tmdb_util import search_movies
    results = search_movies("Inception", limit=3)
    assert len(results) > 0, "No TMDB results"
    assert results[0]["title"] == "Inception"
    save_results("tmdb_search.json", results)
    return f"{len(results)} results"


@test("TMDB: movie details")
def test_tmdb_details():
    from utils.tmdb_util import get_movie_details
    movie = get_movie_details(27205)  # Inception
    assert movie["title"] == "Inception"
    assert movie["budget"] > 0
    save_results("tmdb_details.json", movie)
    return f"Budget: ${movie['budget']:,}"


@test("TMDB: movie credits")
def test_tmdb_credits():
    from utils.tmdb_util import get_movie_credits
    credits = get_movie_credits(27205)
    assert len(credits["cast"]) > 0
    assert len(credits["directors"]) > 0
    save_results("tmdb_credits.json", credits)
    return f"{len(credits['cast'])} cast, {len(credits['directors'])} directors"


@test("TMDB: search people")
def test_tmdb_people():
    from utils.tmdb_util import search_people
    results = search_people("Leonardo DiCaprio", limit=3)
    assert len(results) > 0
    assert "DiCaprio" in results[0]["name"]
    save_results("tmdb_people.json", results)
    return f"{results[0]['name']} (pop: {results[0]['popularity']:.0f})"


@test("OMDB: search movie")
def test_omdb_search():
    from utils.omdb_util import search_movie
    movie = search_movie("Inception", year=2010)
    assert movie is not None, "No OMDB result"
    assert movie["title"] == "Inception"
    assert movie["box_office"] > 0
    save_results("omdb_search.json", movie)
    return f"Box office: ${movie['box_office']:,}"


# ===========================================================================
# 6. Module tools
# ===========================================================================

@test("Tool: search_incentives")
def test_search_incentives():
    from modules.funding import search_incentives_tool
    result = search_incentives_tool(country="USA")
    assert "Georgia" in result, "Georgia incentive not found"
    save_results("tool_incentives.json", {"result": result})
    return "OK"


@test("Tool: search_talent")
def test_search_talent():
    from modules.talent import search_talent_tool
    result = search_talent_tool("Margot Robbie")
    assert "Robbie" in result, "Talent not found"
    save_results("tool_talent_search.json", {"result": result})
    return "OK"


@test("Tool: generate_closing_checklist")
def test_closing_checklist():
    from modules.dataroom import generate_closing_checklist_tool
    assert _test_deal_id, "No test deal"
    result = generate_closing_checklist_tool(_test_deal_id)
    assert "checklist" in result.lower() or "already exists" in result.lower(), f"Unexpected: {result[:100]}"
    save_results("tool_closing.json", {"result": result})
    return "OK"


# ===========================================================================
# 7. Command interceptor
# ===========================================================================

@test("Command: help")
def test_cmd_help():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("help"))
    assert "Available Commands" in result
    return "OK"


@test("Command: deal:list")
def test_cmd_deal_list():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("deal:list"))
    assert result is not None
    assert "Deals" in result or "No deals" in result
    return "OK"


@test("Command: portfolio")
def test_cmd_portfolio():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("portfolio"))
    assert result is not None
    assert "Portfolio" in result or "Total" in result
    return "OK"


@test("Command: incentives")
def test_cmd_incentives():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("incentives"))
    assert result is not None
    assert "Incentive" in result
    return "OK"


@test("Command: talent:search")
def test_cmd_talent_search():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("talent:search Brad Pitt"))
    assert result is not None
    assert "Pitt" in result or "Talent" in result
    return "OK"


@test("Command: unknown falls through")
def test_cmd_fallthrough():
    result = asyncio.get_event_loop().run_until_complete(
        _run_cmd("what is the weather"))
    assert result is None, "Unknown command should return None"
    return "Falls through to AI"


async def _run_cmd(msg):
    from app import _command_interceptor
    return await _command_interceptor(msg, {})


# ===========================================================================
# 8. Chat store
# ===========================================================================

@test("Chat: save & load conversation")
def test_chat_store():
    from utils.agui.chat_store import save_conversation, save_message, load_conversation_messages, delete_conversation
    import uuid
    thread_id = f"test-{uuid.uuid4()}"
    save_conversation(thread_id, title="Test Chat")
    save_message(thread_id, "user", "Hello test")
    save_message(thread_id, "assistant", "Hello! How can I help?")
    msgs = load_conversation_messages(thread_id)
    assert len(msgs) == 2, f"Expected 2 messages, got {len(msgs)}"
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"
    save_results("chat_store.json", msgs)
    delete_conversation(thread_id)
    return "OK"


# ===========================================================================
# 9. Config
# ===========================================================================

@test("Config: settings load")
def test_config():
    from config.settings import (APP_NAME, GENRES, TERRITORIES, RISK_DIMENSIONS,
                                  RISK_TIERS, CLOSING_CHECKLIST_TEMPLATE, BUDGET_CATEGORIES)
    assert APP_NAME == "Ashland Hill Media Finance"
    assert len(GENRES) >= 16
    assert len(TERRITORIES) >= 19
    assert len(RISK_DIMENSIONS) == 6
    assert len(CLOSING_CHECKLIST_TEMPLATE) >= 20
    return f"Genres: {len(GENRES)}, Territories: {len(TERRITORIES)}"


# ===========================================================================
# 10. PDF extractor
# ===========================================================================

@test("PDF extractor: import OK")
def test_pdf_extractor():
    from utils.pdf_extractor import extract_text, extract_script_metadata
    # Just test import and the metadata function with sample text
    meta = extract_script_metadata("INT. OFFICE - DAY\n\nJOHN walks in.\n\nJOHN\nHello there.\n\nEXT. PARK - NIGHT\n\nJANE\nGoodbye.")
    assert meta["scene_count"] == 2, f"Expected 2 scenes, got {meta['scene_count']}"
    assert "JOHN" in meta["character_names"]
    save_results("pdf_extractor.json", meta)
    return f"Scenes: {meta['scene_count']}, Chars: {len(meta['character_names'])}"


# ===========================================================================
# Run
# ===========================================================================

def main():
    print(f"\n{'='*60}")
    print(f"  AHMF Test Suite")
    print(f"{'='*60}\n")

    for fn in _tests:
        run_test(fn)

    print(f"\n{'='*60}")
    print(f"  Results: {_pass} passed, {_fail} failed, {_pass + _fail} total")
    print(f"{'='*60}\n")

    # Save summary
    summary = {
        "passed": _pass,
        "failed": _fail,
        "total": _pass + _fail,
        "tests": _results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_results("test_summary.json", summary)
    print(f"  Results written to test-data/\n")

    return _fail == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
