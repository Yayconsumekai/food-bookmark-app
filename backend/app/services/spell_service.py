from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import re

# In-memory vocabulary cache — built once on first request
_vocabulary: set[str] = set()

def load_vocabulary(db: Session):
    """Load all unique words from recipe names into memory."""
    global _vocabulary
    if _vocabulary:
        return  # already loaded

    print("Loading spell-check vocabulary...")
    rows = db.execute(text("SELECT name FROM recipes")).fetchall()
    for row in rows:
        words = re.findall(r'[a-zA-Z]+', row[0].lower())
        _vocabulary.update(words)
    print(f"Vocabulary loaded: {len(_vocabulary)} unique words")


def edits1(word: str) -> set[str]:
    """All strings one edit away from word (deletion, transposition, replacement, insertion)."""
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:]           for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]       for L, R in splits if R for c in letters]
    inserts    = [L + c + R           for L, R in splits         for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word: str) -> set[str]:
    """All strings two edits away — covers most real typos."""
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def correct_word(word: str) -> Optional[str]:
    """
    Return best spelling suggestion for a word, or None if word looks correct.
    Priority: exact match → 1-edit match → 2-edit match
    """
    w = word.lower()
    if w in _vocabulary:
        return None  # word is fine, no correction needed

    # Find candidates within 1 edit that exist in vocabulary
    candidates_1 = {w for w in edits1(w) if w in _vocabulary}
    if candidates_1:
        # Pick most "common" — approximate by shortest (heuristic)
        return min(candidates_1, key=len)

    # Fall back to 2 edits
    candidates_2 = {w for w in edits2(w) if w in _vocabulary}
    if candidates_2:
        return min(candidates_2, key=len)

    return None  # no suggestion found


def check_query(query: str, db: Session) -> dict:
    """
    Check every word in a query for spelling errors.
    Returns the corrected query and a map of corrections made.
    """
    load_vocabulary(db)

    words       = re.findall(r'[a-zA-Z]+', query)
    corrections = {}

    for word in words:
        suggestion = correct_word(word)
        if suggestion:
            corrections[word] = suggestion

    if not corrections:
        return {"has_corrections": False, "original": query, "corrected": query, "corrections": {}}

    corrected = query
    for original, fixed in corrections.items():
        corrected = re.sub(rf'\b{original}\b', fixed, corrected, flags=re.IGNORECASE)

    return {
        "has_corrections": True,
        "original":        query,
        "corrected":       corrected,
        "corrections":     corrections,   # e.g. {"chiken": "chicken", "garlc": "garlic"}
    }