import pytest
from app.services.search_service import build_tsquery

class TestBuildTsquery:
    def test_single_word(self):
        result = build_tsquery("chicken")
        assert result == "chicken"

    def test_multiple_words_joined_with_and(self):
        result = build_tsquery("chicken garlic soup")
        assert result == "chicken & garlic & soup"

    def test_strips_special_characters(self):
        result = build_tsquery("chicken! @garlic# $soup")
        assert "&" in result
        assert "!" not in result
        assert "@" not in result

    def test_empty_string_returns_none(self):
        result = build_tsquery("")
        assert result is None

    def test_only_special_chars_returns_none(self):
        result = build_tsquery("!!! @@@")
        assert result is None

    def test_lowercases_input(self):
        result = build_tsquery("Chicken Garlic")
        assert result == "chicken & garlic"

    def test_single_char_words_included(self):
        result = build_tsquery("a b c")
        assert result == "a & b & c"