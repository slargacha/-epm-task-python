"""
Dictionary Module - Store and retrieve word definitions.

This module provides a simple dictionary/vocabulary manager that stores
word-definition pairs and allows lookup of definitions by word.
"""


class Dictionary:
    """A dictionary class for storing word definitions.
    
    This class allows users to add new word entries with their definitions
    and look up definitions by word. Missing entries return a friendly message.
    
    Attributes:
        _entries (dict): Internal dictionary storing word-definition pairs.
    """
    
    def __init__(self) -> None:
        """Initialize an empty dictionary."""
        self._entries: dict[str, str] = {}
    
    def newentry(self, word: str, definition: str) -> None:
        """Add a new word entry with its definition.
        
        Args:
            word: The word to add to the dictionary.
            definition: The definition of the word.
        
        Example:
            >>> d = Dictionary()
            >>> d.newentry('Apple', 'A fruit that grows on trees')
        """
        self._entries[word] = definition
    
    def look(self, word: str) -> str:
        """Look up a word in the dictionary.
        
        Args:
            word: The word to search for.
        
        Returns:
            The definition if found, otherwise a message indicating
            the word was not found.
        
        Example:
            >>> d = Dictionary()
            >>> d.newentry('Apple', 'A fruit that grows on trees')
            >>> d.look('Apple')
            'A fruit that grows on trees'
            >>> d.look('Banana')
            "Can't find entry for Banana"
        """
        if word in self._entries:
            return self._entries[word]
        else:
            return f"Can't find entry for {word}"
