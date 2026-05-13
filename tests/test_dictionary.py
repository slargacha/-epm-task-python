"""
Unit tests for the Dictionary module.

Comprehensive test suite for the Dictionary class covering:
- Adding new entries
- Looking up existing entries
- Handling missing entries
- Edge cases and special characters
"""

import pytest
from src.dictionary import Dictionary


class TestDictionary:
    """Test cases for the Dictionary class."""
    
    @pytest.fixture
    def empty_dict(self) -> Dictionary:
        """Fixture providing an empty Dictionary instance."""
        return Dictionary()
    
    @pytest.fixture
    def filled_dict(self) -> Dictionary:
        """Fixture providing a Dictionary with sample entries."""
        d = Dictionary()
        d.newentry('Apple', 'A fruit that grows on trees')
        d.newentry('Banana', 'A yellow tropical fruit')
        d.newentry('Python', 'A programming language')
        return d
    
    # Tests for newentry method
    def test_newentry_single_entry(self, empty_dict: Dictionary) -> None:
        """Test adding a single entry to the dictionary."""
        empty_dict.newentry('Apple', 'A fruit that grows on trees')
        assert empty_dict.look('Apple') == 'A fruit that grows on trees'
    
    def test_newentry_multiple_entries(self, empty_dict: Dictionary) -> None:
        """Test adding multiple entries to the dictionary."""
        empty_dict.newentry('Apple', 'A fruit that grows on trees')
        empty_dict.newentry('Banana', 'A yellow tropical fruit')
        
        assert empty_dict.look('Apple') == 'A fruit that grows on trees'
        assert empty_dict.look('Banana') == 'A yellow tropical fruit'
    
    def test_newentry_overwrite_existing(self, filled_dict: Dictionary) -> None:
        """Test overwriting an existing entry."""
        filled_dict.newentry('Apple', 'A red fruit')
        assert filled_dict.look('Apple') == 'A red fruit'
    
    def test_newentry_empty_definition(self, empty_dict: Dictionary) -> None:
        """Test adding an entry with an empty definition."""
        empty_dict.newentry('Empty', '')
        assert empty_dict.look('Empty') == ''
    
    def test_newentry_special_characters(self, empty_dict: Dictionary) -> None:
        """Test adding entries with special characters."""
        empty_dict.newentry('C++', 'A programming language with ++ operator')
        empty_dict.newentry('🍎', 'Apple emoji')
        empty_dict.newentry('Café', 'A place to drink coffee')
        
        assert empty_dict.look('C++') == 'A programming language with ++ operator'
        assert empty_dict.look('🍎') == 'Apple emoji'
        assert empty_dict.look('Café') == 'A place to drink coffee'
    
    def test_newentry_long_definition(self, empty_dict: Dictionary) -> None:
        """Test adding entry with very long definition."""
        long_def = 'A' * 1000
        empty_dict.newentry('Test', long_def)
        assert empty_dict.look('Test') == long_def
    
    # Tests for look method
    def test_look_existing_entry(self, filled_dict: Dictionary) -> None:
        """Test looking up an existing entry."""
        result = filled_dict.look('Apple')
        assert result == 'A fruit that grows on trees'
    
    def test_look_missing_entry(self, filled_dict: Dictionary) -> None:
        """Test looking up a non-existent entry."""
        result = filled_dict.look('Orange')
        assert result == "Can't find entry for Orange"
    
    def test_look_case_sensitive(self, filled_dict: Dictionary) -> None:
        """Test that lookups are case-sensitive."""
        result = filled_dict.look('apple')  # lowercase
        assert result == "Can't find entry for apple"
    
    def test_look_empty_dictionary(self, empty_dict: Dictionary) -> None:
        """Test looking up in an empty dictionary."""
        result = empty_dict.look('AnyWord')
        assert result == "Can't find entry for AnyWord"
    
    # Edge cases
    def test_numeric_keys(self, empty_dict: Dictionary) -> None:
        """Test using numeric strings as keys."""
        empty_dict.newentry('42', 'The answer to everything')
        assert empty_dict.look('42') == 'The answer to everything'
        assert empty_dict.look('43') == "Can't find entry for 43"
    
    def test_whitespace_in_key(self, empty_dict: Dictionary) -> None:
        """Test keys with whitespace."""
        empty_dict.newentry('New York', 'A city in the USA')
        assert empty_dict.look('New York') == 'A city in the USA'
        assert empty_dict.look('NewYork') == "Can't find entry for NewYork"
    
    def test_multiple_lookups_same_word(self, filled_dict: Dictionary) -> None:
        """Test that multiple lookups return consistent results."""
        result1 = filled_dict.look('Python')
        result2 = filled_dict.look('Python')
        result3 = filled_dict.look('Python')
        
        assert result1 == result2 == result3
        assert result1 == 'A programming language'
    
    def test_definition_with_quotes(self, empty_dict: Dictionary) -> None:
        """Test definitions containing quotes."""
        definition = 'A "special" definition with \'quotes\''
        empty_dict.newentry('Quoted', definition)
        assert empty_dict.look('Quoted') == definition
    
    def test_definition_with_newlines(self, empty_dict: Dictionary) -> None:
        """Test definitions with newline characters."""
        definition = 'Line 1\nLine 2\nLine 3'
        empty_dict.newentry('MultiLine', definition)
        assert empty_dict.look('MultiLine') == definition
    
    def test_very_long_key(self, empty_dict: Dictionary) -> None:
        """Test very long word keys."""
        long_key = 'A' * 500
        empty_dict.newentry(long_key, 'Definition for long key')
        assert empty_dict.look(long_key) == 'Definition for long key'
        assert empty_dict.look(long_key + 'B') == f"Can't find entry for {long_key}B"
