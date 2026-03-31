"""
OMDB API client for movie ratings and box office data.

Complements TMDB with IMDb ratings, Rotten Tomatoes scores, and box office figures.
"""

import os
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "http://www.omdbapi.com/"


def _get_api_key():
    return os.getenv("OMDB_API_KEY")


def search_movie(title: str, year: int = None) -> Optional[dict]:
    """Search for a movie by title and optionally year."""
    params = {"apikey": _get_api_key(), "t": title, "type": "movie"}
    if year:
        params["y"] = year
    resp = httpx.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("Response") == "False":
        return None
    return _parse_movie(data)


def get_by_imdb_id(imdb_id: str) -> Optional[dict]:
    """Get movie details by IMDb ID."""
    params = {"apikey": _get_api_key(), "i": imdb_id}
    resp = httpx.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("Response") == "False":
        return None
    return _parse_movie(data)


def _parse_movie(data: dict) -> dict:
    """Parse OMDB response into a clean dict."""
    def _parse_number(val):
        if not val or val == "N/A":
            return 0
        return int(val.replace(",", "").replace("$", ""))

    ratings = {}
    for r in data.get("Ratings", []):
        source = r.get("Source", "")
        if "Internet Movie" in source:
            ratings["imdb"] = r["Value"]
        elif "Rotten Tomatoes" in source:
            ratings["rotten_tomatoes"] = r["Value"]
        elif "Metacritic" in source:
            ratings["metacritic"] = r["Value"]

    return {
        "title": data.get("Title", ""),
        "year": data.get("Year", ""),
        "rated": data.get("Rated", ""),
        "runtime": data.get("Runtime", ""),
        "genre": data.get("Genre", ""),
        "director": data.get("Director", ""),
        "actors": data.get("Actors", ""),
        "plot": data.get("Plot", ""),
        "language": data.get("Language", ""),
        "country": data.get("Country", ""),
        "awards": data.get("Awards", ""),
        "imdb_id": data.get("imdbID", ""),
        "imdb_rating": data.get("imdbRating", "N/A"),
        "imdb_votes": data.get("imdbVotes", "N/A"),
        "box_office": _parse_number(data.get("BoxOffice", "N/A")),
        "production": data.get("Production", "N/A"),
        "ratings": ratings,
    }
