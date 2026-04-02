"""
Seed Database with Sample Data

Loads CSVs from data/ directory and populates the ahmf schema.
Also fetches real movie data from TMDB/OMDB for comp_films table.

Usage: python data/seed_db.py
"""

import csv
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from sqlalchemy import text
from utils.db import get_pool

DATA_DIR = ROOT / "data"


def read_csv(filename):
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed_contacts(session):
    """Seed contacts from CSV."""
    rows = read_csv("contacts.csv")
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.contacts")).scalar()
    if existing > 5:
        print(f"  contacts: {existing} already exist, skipping")
        return
    count = 0
    for r in rows:
        session.execute(text("""
            INSERT INTO ahmf.contacts (name, company, role, email, phone, contact_type, notes)
            VALUES (:name, :company, :role, :email, :phone, :type, :notes)
            ON CONFLICT DO NOTHING
        """), {"name": r["name"], "company": r["company"], "role": r["role"],
               "email": r["email"], "phone": r["phone"], "type": r["contact_type"],
               "notes": r["notes"]})
        count += 1
    print(f"  contacts: {count} seeded")


def seed_deals(session):
    """Seed deals from CSV."""
    rows = read_csv("deals.csv")
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.deals")).scalar()
    if existing > 5:
        print(f"  deals: {existing} already exist, skipping")
        return
    count = 0
    for r in rows:
        session.execute(text("""
            INSERT INTO ahmf.deals (title, project_type, genre, status, loan_amount, currency,
                interest_rate, term_months, borrower_name, producer, director, cast_summary,
                budget, territory, collateral_type, origination_date, maturity_date)
            VALUES (:title, :type, :genre, :status, :loan, :curr, :rate, :term, :borrower,
                :producer, :director, :cast, :budget, :terr, :collateral, :orig, :mat)
            ON CONFLICT DO NOTHING
        """), {
            "title": r["title"], "type": r["project_type"], "genre": r["genre"],
            "status": r["status"], "loan": float(r["loan_amount"]) if r["loan_amount"] else None,
            "curr": r["currency"], "rate": float(r["interest_rate"]) if r["interest_rate"] else None,
            "term": int(r["term_months"]) if r["term_months"] else None,
            "borrower": r["borrower_name"], "producer": r["producer"], "director": r["director"],
            "cast": r["cast_summary"], "budget": float(r["budget"]) if r["budget"] else None,
            "terr": r["territory"], "collateral": r["collateral_type"],
            "orig": r["origination_date"] or None, "mat": r["maturity_date"] or None,
        })
        count += 1
    print(f"  deals: {count} seeded")


def seed_sales_contracts(session):
    """Seed sales contracts linked to deals and contacts."""
    rows = read_csv("sales_contracts.csv")
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.sales_contracts")).scalar()
    if existing > 3:
        print(f"  sales_contracts: {existing} already exist, skipping")
        return
    count = 0
    for r in rows:
        deal = session.execute(text("SELECT deal_id FROM ahmf.deals WHERE title = :t LIMIT 1"),
                               {"t": r["deal_title"]}).fetchone()
        dist = session.execute(text("SELECT contact_id FROM ahmf.contacts WHERE name = :n LIMIT 1"),
                               {"n": r["distributor_name"]}).fetchone()
        if not deal:
            continue
        session.execute(text("""
            INSERT INTO ahmf.sales_contracts (deal_id, territory, distributor_id, mg_amount, currency, status)
            VALUES (:did, :terr, :dist, :mg, :curr, :status)
        """), {"did": str(deal[0]), "terr": r["territory"],
               "dist": str(dist[0]) if dist else None,
               "mg": float(r["mg_amount"]), "curr": r["currency"], "status": r["status"]})
        count += 1
    print(f"  sales_contracts: {count} seeded")


def seed_collections(session):
    """Create collection records for active sales contracts."""
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.collections")).scalar()
    if existing > 3:
        print(f"  collections: {existing} already exist, skipping")
        return
    contracts = session.execute(text("""
        SELECT contract_id, mg_amount, status FROM ahmf.sales_contracts WHERE status IN ('active','completed')
    """)).fetchall()
    count = 0
    for c in contracts:
        mg = float(c[1]) if c[1] else 0
        if c[2] == "completed":
            session.execute(text("""
                INSERT INTO ahmf.collections (contract_id, amount_due, amount_received, due_date, received_date, status)
                VALUES (:cid, :due, :recv, '2025-12-01', '2025-11-28', 'received')
            """), {"cid": str(c[0]), "due": mg, "recv": mg})
        else:
            # First installment received, second pending
            half = mg / 2
            session.execute(text("""
                INSERT INTO ahmf.collections (contract_id, amount_due, amount_received, due_date, received_date, status)
                VALUES (:cid, :due, :recv, '2025-12-01', '2025-11-20', 'received')
            """), {"cid": str(c[0]), "due": half, "recv": half})
            session.execute(text("""
                INSERT INTO ahmf.collections (contract_id, amount_due, amount_received, due_date, status)
                VALUES (:cid, :due, 0, '2026-06-01', 'pending')
            """), {"cid": str(c[0]), "due": half})
        count += 1
    print(f"  collections: {count} contracts with payments seeded")


def seed_transactions(session):
    """Seed accounting transactions."""
    rows = read_csv("transactions.csv")
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.transactions")).scalar()
    if existing > 5:
        print(f"  transactions: {existing} already exist, skipping")
        return
    count = 0
    for r in rows:
        deal = session.execute(text("SELECT deal_id FROM ahmf.deals WHERE title = :t LIMIT 1"),
                               {"t": r["deal_title"]}).fetchone()
        cparty = session.execute(text("SELECT contact_id FROM ahmf.contacts WHERE name = :n LIMIT 1"),
                                 {"n": r["counterparty_name"]}).fetchone()
        if not deal:
            continue
        session.execute(text("""
            INSERT INTO ahmf.transactions (deal_id, txn_type, amount, currency, counterparty_id, reference, posted_date)
            VALUES (:did, :type, :amt, :curr, :cid, :ref, :date)
        """), {"did": str(deal[0]), "type": r["txn_type"], "amt": float(r["amount"]),
               "curr": r["currency"], "cid": str(cparty[0]) if cparty else None,
               "ref": r["reference"], "date": r["posted_date"]})
        count += 1
    print(f"  transactions: {count} seeded")


def seed_messages(session):
    """Seed communications/tasks."""
    rows = read_csv("messages.csv")
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.messages")).scalar()
    if existing > 5:
        print(f"  messages: {existing} already exist, skipping")
        return
    count = 0
    for r in rows:
        deal = session.execute(text("SELECT deal_id FROM ahmf.deals WHERE title = :t LIMIT 1"),
                               {"t": r["deal_title"]}).fetchone()
        session.execute(text("""
            INSERT INTO ahmf.messages (deal_id, subject, body, message_type, due_date, status)
            VALUES (:did, :subj, :body, :type, :due, :status)
        """), {"did": str(deal[0]) if deal else None, "subj": r["subject"], "body": r["body"],
               "type": r["message_type"], "due": r["due_date"] or None, "status": r["status"]})
        count += 1
    print(f"  messages: {count} seeded")


def seed_comp_films_from_tmdb(session):
    """Fetch real comparable film data from TMDB and OMDB."""
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.comp_films")).scalar()
    if existing > 5:
        print(f"  comp_films: {existing} already exist, skipping")
        return

    from utils.tmdb_util import get_movie_details, get_movie_credits
    from utils.omdb_util import search_movie

    # Ensure unique index exists for ON CONFLICT
    session.execute(text("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_comp_films_tmdb_unique
        ON ahmf.comp_films(tmdb_id) WHERE tmdb_id IS NOT NULL
    """))

    # Real films as comps — mix of genres/budgets relevant to film finance
    tmdb_ids = [
        27205,   # Inception
        680,     # Pulp Fiction
        550,     # Fight Club
        597,     # Titanic
        120,     # LOTR: Fellowship
        155,     # The Dark Knight
        13,      # Forrest Gump
        278,     # Shawshank Redemption
        11,      # Star Wars: A New Hope
        603,     # The Matrix
        98,      # Gladiator
        238,     # The Godfather
        807,     # Se7en
        769,     # GoodFellas
        424,     # Schindler's List
    ]

    count = 0
    for tmdb_id in tmdb_ids:
        try:
            details = get_movie_details(tmdb_id)
            if not details:
                continue
            credits = get_movie_credits(tmdb_id)
            cast_names = [c["name"] for c in credits.get("cast", [])[:5]]
            directors = credits.get("directors", [])

            # Get OMDB data for box office
            omdb = search_movie(details["title"], year=int(details["year"])) if details.get("year") else None
            box_office = omdb.get("box_office", 0) if omdb else 0

            session.execute(text("""
                INSERT INTO ahmf.comp_films (tmdb_id, title, year, genre, budget, worldwide_gross,
                    domestic_gross, cast_names, director, popularity)
                VALUES (:tid, :title, :year, :genre, :budget, :ww, :dom, :cast, :dir, :pop)
                ON CONFLICT (tmdb_id) WHERE tmdb_id IS NOT NULL DO NOTHING
            """), {
                "tid": tmdb_id, "title": details["title"],
                "year": int(details["year"]) if details.get("year") else None,
                "genre": ", ".join(details.get("genres", [])),
                "budget": details.get("budget", 0),
                "ww": details.get("revenue", 0),
                "dom": box_office,
                "cast": cast_names, "dir": directors[0] if directors else None,
                "pop": details.get("popularity", 0),
            })
            count += 1
            print(f"    TMDB {tmdb_id}: {details['title']} (${details.get('budget',0):,} / ${details.get('revenue',0):,})")
        except Exception as e:
            print(f"    TMDB {tmdb_id}: error — {e}")
    print(f"  comp_films: {count} fetched from TMDB/OMDB")


def seed_credit_ratings(session):
    """Create credit ratings for key contacts."""
    existing = session.execute(text("SELECT COUNT(*) FROM ahmf.credit_ratings")).scalar()
    if existing > 3:
        print(f"  credit_ratings: {existing} already exist, skipping")
        return
    import json
    ratings_data = [
        ("Lionsgate Films", 82, 88, "AA", {"track_record": "Strong slate, consistent releases", "financial_stability": "Public company, solid balance sheet", "market_position": "Top indie distributor", "payment_history": "On-time payments consistently"}),
        ("StudioCanal", 78, 85, "AA", {"track_record": "Major European player", "financial_stability": "Vivendi subsidiary", "market_position": "Strong in UK/France/Germany", "payment_history": "Reliable, occasional 15-day delays"}),
        ("A24 Films", 75, 80, "A", {"track_record": "Premium brand, award winners", "financial_stability": "Private, growth-stage", "market_position": "Cultural dominance in indie space", "payment_history": "Good, structured payment schedules"}),
        ("Blumhouse Productions", 85, 90, "AAA", {"track_record": "Exceptional ROI model", "financial_stability": "Universal deal provides stability", "market_position": "Horror genre leader", "payment_history": "Excellent, always early"}),
        ("Wild Bunch International", 60, 65, "BBB", {"track_record": "Solid arthouse catalog", "financial_stability": "Recent restructuring", "market_position": "Strong Cannes presence", "payment_history": "Occasional delays, 30-60 days"}),
        ("Entertainment One", 72, 78, "A", {"track_record": "Global distribution network", "financial_stability": "Hasbro parent company", "market_position": "Strong in Canada/UK", "payment_history": "Reliable corporate payments"}),
    ]
    count = 0
    for name, score, reliability, tier, factors in ratings_data:
        contact = session.execute(text("SELECT contact_id FROM ahmf.contacts WHERE name = :n LIMIT 1"), {"n": name}).fetchone()
        if not contact:
            continue
        session.execute(text("""
            INSERT INTO ahmf.credit_ratings (contact_id, score, payment_reliability, risk_tier, factors)
            VALUES (:cid, :score, :rel, :tier, :factors)
        """), {"cid": str(contact[0]), "score": score, "rel": reliability, "tier": tier, "factors": json.dumps(factors)})
        count += 1
    print(f"  credit_ratings: {count} seeded")


def main():
    print(f"\n{'='*60}")
    print(f"  AHMF Database Seed")
    print(f"{'='*60}\n")

    pool = get_pool()

    with pool.get_session() as session:
        seed_contacts(session)

    with pool.get_session() as session:
        seed_deals(session)

    with pool.get_session() as session:
        seed_sales_contracts(session)

    with pool.get_session() as session:
        seed_collections(session)

    with pool.get_session() as session:
        seed_transactions(session)

    with pool.get_session() as session:
        seed_messages(session)

    with pool.get_session() as session:
        seed_credit_ratings(session)

    with pool.get_session() as session:
        seed_comp_films_from_tmdb(session)

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}\n")
    with pool.get_session() as session:
        for t in ["users", "deals", "contacts", "sales_contracts", "collections",
                   "credit_ratings", "transactions", "messages", "comp_films", "incentive_programs"]:
            r = session.execute(text(f"SELECT COUNT(*) FROM ahmf.{t}")).scalar()
            print(f"  {t}: {r}")
    print()


if __name__ == "__main__":
    main()
