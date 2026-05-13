"""
Nth Letter Module - Extract and concatenate nth letters from words.

This module provides functionality to extract the nth letter from each word
in an array, where n is the position of the word in the array, and concatenate
them into a single string.
"""


def nth_letter(words: list[str]) -> str:
    """Extract the nth letter from each word and concatenate them.
    
    For each word at position n in the input list, extracts the character
    at index n and concatenates all extracted characters into a single string.
    Words that are too short for their index are skipped.
    
    Args:
        words: List of strings.
    
    Returns:
        A string containing the concatenated nth letters.
    
    Example:
        >>> nth_letter(["yoda", "best", "has"])
        'yes'
    """
    return "".join(
        word[index] for index, word in enumerate(words) if index < len(word)
    )
