"""
PDF script extraction utility.

Extracts text from screenplay PDFs for analysis by AI agents.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def extract_text(file_path: str) -> Tuple[bool, str, dict]:
    """
    Extract text from a PDF file.

    Returns:
        (success, text, metadata) where metadata includes page_count, word_count, char_count.
    """
    try:
        import pdfplumber

        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        full_text = "\n\n".join(text_parts)
        word_count = len(full_text.split())
        char_count = len(full_text)

        metadata = {
            "page_count": page_count,
            "word_count": word_count,
            "char_count": char_count,
            "file_path": str(file_path),
        }

        if not full_text.strip():
            return False, "", metadata

        return True, full_text, metadata

    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return False, "", {"error": str(e)}


def extract_script_metadata(text: str) -> dict:
    """
    Extract basic screenplay metadata from extracted text.

    Looks for title page patterns, character names, scene headings.
    """
    lines = text.split("\n")
    metadata = {
        "title": "",
        "scene_count": 0,
        "character_names": [],
        "estimated_runtime_minutes": 0,
    }

    # Count scene headings (INT./EXT.)
    scene_count = 0
    characters = set()
    for line in lines:
        stripped = line.strip().upper()
        if stripped.startswith("INT.") or stripped.startswith("EXT."):
            scene_count += 1
        # Character names are typically all-caps lines
        if stripped and stripped.isupper() and len(stripped.split()) <= 3 and len(stripped) < 30:
            if not stripped.startswith(("INT.", "EXT.", "FADE", "CUT TO", "DISSOLVE")):
                characters.add(stripped)

    metadata["scene_count"] = scene_count
    metadata["character_names"] = sorted(list(characters))[:20]
    # Rough estimate: 1 page ~= 1 minute, ~250 words per page
    word_count = len(text.split())
    metadata["estimated_runtime_minutes"] = max(1, word_count // 250)

    # Try to extract title from first few lines
    for line in lines[:10]:
        stripped = line.strip()
        if stripped and len(stripped) > 3 and not stripped.startswith(("INT.", "EXT.", "FADE")):
            metadata["title"] = stripped
            break

    return metadata
