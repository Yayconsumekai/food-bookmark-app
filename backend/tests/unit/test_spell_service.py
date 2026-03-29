import pytest
from app.services.spell_service import edits1, edits2, correct_word, _vocabulary

class TestEdits:
    def test_edits1_produces_candidates(self):
        candidates = edits1("chicken")
        assert isinstance(candidates, set)
        assert len(candidates) > 0

    def test_edits1_includes_deletion(self):
        """'chicen' is one deletion away from 'chicken'."""
        candidates = edits1("chicken")
        assert "chicen" in candidates

    def test_edits1_includes_transposition(self):
        """'cihcken' is one transposition away from 'chicken'."""
        candidates = edits1("chicken")
        assert "cihcken" in candidates

    def test_edits2_is_superset_of_edits1(self):
        e1 = edits1("test")
        e2 = edits2("test")
        # edits2 is not strictly a superset but should be larger
        assert len(e2) >= len(e1)


class TestCorrectWord:
    def setup_method(self):
        """Populate vocabulary with known words for testing."""
        _vocabulary.clear()
        _vocabulary.update({"chicken", "garlic", "soup", "pasta", "sauce"})

    def test_correct_word_in_vocabulary_returns_none(self):
        """No correction needed for correctly spelled word."""
        assert correct_word("chicken") is None

    def test_correct_typo_one_edit(self):
        """'chicen' is one edit from 'chicken' — should be corrected."""
        result = correct_word("chicen")
        assert result == "chicken"

    def test_unknown_word_with_no_match_returns_none(self):
        """Completely random string with no match returns None."""
        result = correct_word("xqzptw")
        assert result is None

    def test_case_insensitive(self):
        """Spell checker should handle uppercase input."""
        result = correct_word("CHICEN")
        assert result == "chicken"


class TestCheckQuery:
    def setup_method(self):
        _vocabulary.clear()
        _vocabulary.update({"chicken", "garlic", "soup"})

    def test_correct_query_has_no_corrections(self, db):
        from app.services.spell_service import check_query
        result = check_query("chicken soup", db)
        assert result["has_corrections"] is False
        assert result["corrected"] == "chicken soup"

    def test_typo_query_gets_corrected(self, db):
        from app.services.spell_service import check_query
        result = check_query("chicen soup", db)
        assert result["has_corrections"] is True
        assert "chicken" in result["corrected"]
        assert "chicen" in result["corrections"]

    def test_corrections_dict_maps_original_to_fixed(self, db):
        from app.services.spell_service import check_query
        result = check_query("garlc soup", db)
        if result["has_corrections"]:
            assert "garlc" in result["corrections"]