"""
TMDB API client for movie data lookups.

Used by the Sales Estimates Generator for comparable film analysis.
"""

import os
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.themoviedb.org/3"


def _get_api_key():
    return os.getenv("TMDB_API_KEY")


def search_movies(query: str, year: int = None, limit: int = 10) -> list[dict]:
    """Search TMDB for movies by title."""
    params = {"api_key": _get_api_key(), "query": query, "language": "en-US"}
    if year:
        params["year"] = year
    resp = httpx.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results", [])[:limit]
    return [
        {
            "tmdb_id": m["id"],
            "title": m["title"],
            "year": m.get("release_date", "")[:4],
            "overview": m.get("overview", ""),
            "vote_average": m.get("vote_average", 0),
            "vote_count": m.get("vote_count", 0),
            "popularity": m.get("popularity", 0),
            "genre_ids": m.get("genre_ids", []),
        }
        for m in results
    ]


def get_movie_details(tmdb_id: int) -> Optional[dict]:
    """Get detailed movie info including budget and revenue."""
    resp = httpx.get(
        f"{BASE_URL}/movie/{tmdb_id}",
        params={"api_key": _get_api_key(), "language": "en-US"},
        timeout=10,
    )
    resp.raise_for_status()
    m = resp.json()
    return {
        "tmdb_id": m["id"],
        "title": m["title"],
        "year": m.get("release_date", "")[:4],
        "genres": [g["name"] for g in m.get("genres", [])],
        "budget": m.get("budget", 0),
        "revenue": m.get("revenue", 0),
        "runtime": m.get("runtime", 0),
        "vote_average": m.get("vote_average", 0),
        "vote_count": m.get("vote_count", 0),
        "popularity": m.get("popularity", 0),
        "overview": m.get("overview", ""),
        "production_countries": [c["name"] for c in m.get("production_countries", [])],
        "original_language": m.get("original_language", ""),
        "status": m.get("status", ""),
    }


def get_movie_credits(tmdb_id: int) -> dict:
    """Get cast and crew for a movie."""
    resp = httpx.get(
        f"{BASE_URL}/movie/{tmdb_id}/credits",
        params={"api_key": _get_api_key()},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    cast = [
        {"name": c["name"], "character": c.get("character", ""), "popularity": c.get("popularity", 0)}
        for c in data.get("cast", [])[:10]
    ]
    directors = [
        c["name"] for c in data.get("crew", []) if c.get("job") == "Director"
    ]
    producers = [
        c["name"] for c in data.get("crew", []) if c.get("job") == "Producer"
    ][:5]
    return {"cast": cast, "directors": directors, "producers": producers}


def discover_similar(genre_id: int, budget_min: int = 0, budget_max: int = 0,
                     year_min: int = 0, year_max: int = 0, limit: int = 10) -> list[dict]:
    """Discover movies similar to a target profile using TMDB discover endpoint."""
    params = {
        "api_key": _get_api_key(),
        "language": "en-US",
        "sort_by": "revenue.desc",
        "with_genres": str(genre_id),
        "page": 1,
    }
    if year_min:
        params["primary_release_date.gte"] = f"{year_min}-01-01"
    if year_max:
        params["primary_release_date.lte"] = f"{year_max}-12-31"

    resp = httpx.get(f"{BASE_URL}/discover/movie", params=params, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results", [])[:limit]
    return [
        {
            "tmdb_id": m["id"],
            "title": m["title"],
            "year": m.get("release_date", "")[:4],
            "vote_average": m.get("vote_average", 0),
            "popularity": m.get("popularity", 0),
        }
        for m in results
    ]


def get_genre_list() -> dict:
    """Get TMDB genre ID to name mapping."""
    resp = httpx.get(
        f"{BASE_URL}/genre/movie/list",
        params={"api_key": _get_api_key(), "language": "en-US"},
        timeout=10,
    )
    resp.raise_for_status()
    return {g["id"]: g["name"] for g in resp.json().get("genres", [])}
