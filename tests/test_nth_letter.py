"""
Unit tests for the Nth Letter module.

Comprehensive test suite for the nth_letter function covering:
- Basic extraction and concatenation
- Various array lengths
- Single character words
- Edge cases and special characters
"""

import pytest
from src.nth_letter import nth_letter


class TestNthLetter:
    """Test cases for the nth_letter function."""
    
    # Basic functionality
    def test_basic_example(self) -> None:
        """Test the provided example from requirements."""
        result = nth_letter(['yoda', 'best', 'has'])
        assert result == 'yes'
    
    def test_single_word(self) -> None:
        """Test with a single word."""
        result = nth_letter(['hello'])
        assert result == 'h'
    
    def test_two_words(self) -> None:
        """Test with two words."""
        result = nth_letter(['ab', 'cd'])
        assert result == 'ad'
    
    # Different word lengths
    def test_all_single_chars(self) -> None:
        """Test words with increasing lengths starting from one character."""
        result = nth_letter(['a', 'bb', 'ccc', 'dddd'])
        assert result == 'abcd'
    
    def test_increasing_lengths(self) -> None:
        """Test words with increasing length."""
        # word[0] = 'a'[0] = 'a'
        # word[1] = 'ab'[1] = 'b'
        # word[2] = 'abc'[2] = 'c'
        # word[3] = 'abcd'[3] = 'd'
        result = nth_letter(['a', 'ab', 'abc', 'abcd'])
        assert result == 'abcd'
    
    def test_all_same_length(self) -> None:
        """Test with all words having the same length."""
        result = nth_letter(['abc', 'def', 'ghi'])
        assert result == 'aei'
    
    # Empty and edge cases
    def test_empty_array(self) -> None:
        """Test with an empty array."""
        result = nth_letter([])
        assert result == ''
    
    def test_long_words(self) -> None:
        """Test with longer words."""
        words = ['abcdefghij', 'bcdefghijk', 'cdefghijkl', 'defghijklm']
        # 'abcdefghij'[0] = 'a'
        # 'bcdefghijk'[1] = 'c'
        # 'cdefghijkl'[2] = 'e'
        # 'defghijklm'[3] = 'g'
        result = nth_letter(words)
        assert result == 'aceg'
    
    # Real-world examples
    def test_english_words_example1(self) -> None:
        """Test with English words and valid lengths."""
        result = nth_letter(['code', 'cracking', 'isx', 'funk'])
        assert result == 'crxk'
    
    def test_numeric_chars(self) -> None:
        """Test with numeric characters in strings."""
        result = nth_letter(['123', '4567', '89012'])
        # '123'[0] = '1'
        # '4567'[1] = '5'
        # '89012'[2] = '0'
        assert result == '150'
    
    def test_special_characters(self) -> None:
        """Test with special characters."""
        result = nth_letter(['!@#', '$%^&', '*()'])
        # '!@#'[0] = '!'
        # '$%^&'[1] = '%'
        # '*()' - only 3 chars, needs index 2 = ')'
        assert result == '!%)'
    
    def test_spaces_in_words(self) -> None:
        """Test with spaces in strings."""
        result = nth_letter(['a b', 'c d e', 'f g h i'])
        # 'a b'[0] = 'a'
        # 'c d e'[1] = ' '
        # 'f g h i'[2] = 'g'
        assert result == 'a g'
    
    def test_unicode_characters(self) -> None:
        """Test with unicode/special characters."""
        result = nth_letter(['café', 'naïve', 'résumé'])
        # 'café'[0] = 'c'
        # 'naïve'[1] = 'a'
        # 'résumé'[2] = 's'
        assert result == 'cas'
    
    # Case sensitivity
    def test_case_sensitivity(self) -> None:
        """Test that the function is case-sensitive."""
        result = nth_letter(['HELLO', 'WORLD'])
        # 'HELLO'[0] = 'H'
        # 'WORLD'[1] = 'O'
        assert result == 'HO'
    
    def test_mixed_case(self) -> None:
        """Test with mixed case."""
        result = nth_letter(['Python', 'isAwesome', 'really'])
        # 'Python'[0] = 'P'
        # 'isAwesome'[1] = 's'
        # 'really'[2] = 'a'
        assert result == 'Psa'
    
    # Different scenarios
    def test_alphabet_extraction(self) -> None:
        """Test extracting specific letters from alphabet."""
        words = [
            'a',          # [0] = 'a'
            'ab',         # [1] = 'b'
            'abc',        # [2] = 'c'
            'abcd',       # [3] = 'd'
            'abcde',      # [4] = 'e'
        ]
        result = nth_letter(words)
        assert result == 'abcde'
    
    def test_repeated_extraction(self) -> None:
        """Test extracting from repeated patterns."""
        result = nth_letter(['a', 'bb', 'ccc', 'dddd'])
        # 'a'[0] = 'a'
        # 'bb'[1] = 'b'
        # 'ccc'[2] = 'c'
        # 'dddd'[3] = 'd'
        assert result == 'abcd'
    
    def test_long_array(self) -> None:
        """Test with a longer array."""
        # Create array where word at index i has length i+1
        words = ['a' * (i+1) for i in range(10)]
        # Each extraction will get 'a'
        result = nth_letter(words)
        assert result == 'a' * 10
    
    def test_complex_real_word_example(self) -> None:
        """Test with actual words forming a different sentence."""
        result = nth_letter(['python', 'is', 'amazing'])
        # 'python'[0] = 'p'
        # 'is'[1] = 's'
        # 'amazing'[2] = 'a'
        assert result == 'psa'
    
    # Return type validation
    def test_return_type_is_string(self) -> None:
        """Test that return value is a string."""
        result = nth_letter(['test'])
        assert isinstance(result, str)
    
    def test_concatenation_order(self) -> None:
        """Test that characters are in correct order."""
        result = nth_letter(['a', 'bb', 'ccc', 'dddd', 'eeeee'])
        assert result == 'abcde'
        assert len(result) == 5
    
    # Immutability test
    def test_original_array_unchanged(self) -> None:
        """Test that the function doesn't modify the input array."""
        original = ['yoda', 'best', 'has']
        original_copy = original.copy()
        
        nth_letter(original)
        
        assert original == original_copy
    
    # Additional edge cases
    def test_very_long_word_chain(self) -> None:
        """Test with very long words."""
        words = [
            'a' * 100,
            'b' * 100,
            'c' * 100,
        ]
        result = nth_letter(words)
        # 'aaa...a'[0] = 'a'
        # 'bbb...b'[1] = 'b'
        # 'ccc...c'[2] = 'c'
        assert result == 'abc'
    
    def test_punctuation_extraction(self) -> None:
        """Test extracting punctuation marks."""
        result = nth_letter(['!', '..', '???'])
        # '!'[0] = '!'
        # '..'[1] = '.'
        # '???'[2] = '?'
        assert result == '!.?'
