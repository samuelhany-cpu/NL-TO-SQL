"""
Error correction utility for Natural Language to SQL Parser

This module provides fuzzy string matching and error correction capabilities
to help users with typos and similar errors in their natural language queries.
"""

import difflib
from typing import Dict, Tuple, Optional, List


class ErrorCorrector:
    """
    Handles error correction and suggestions for natural language queries.
    """
    
    def __init__(self, vocabulary: List[str]):
        """
        Initialize the error corrector with a vocabulary.
        
        Args:
            vocabulary: List of recognized words
        """
        self.vocabulary = [word.lower() for word in vocabulary]
        self.cutoff = 0.6  # Minimum similarity threshold
    
    def suggest_corrections(self, query: str) -> Tuple[Dict[str, str], Optional[str]]:
        """
        Suggest corrections for a query string.
        
        Args:
            query: The input query string
            
        Returns:
            Tuple containing:
            - Dict of original->corrected word mappings
            - Corrected query string (or None if no corrections)
        """
        words = query.split()
        suggestions = {}
        corrected_query = query.lower()
        
        for word in words:
            word_lower = word.lower()
            close_matches = difflib.get_close_matches(
                word_lower, 
                self.vocabulary, 
                n=1, 
                cutoff=self.cutoff
            )
            
            if close_matches and close_matches[0] != word_lower:
                suggestions[word] = close_matches[0]
                # Replace in corrected query (case-insensitive)
                corrected_query = corrected_query.replace(word_lower, close_matches[0])
        
        return suggestions, corrected_query if suggestions else None
    
    def get_word_suggestions(self, word: str, n: int = 3) -> List[str]:
        """
        Get multiple suggestions for a single word.
        
        Args:
            word: The word to find suggestions for
            n: Maximum number of suggestions to return
            
        Returns:
            List[str]: List of suggested corrections
        """
        return difflib.get_close_matches(
            word.lower(), 
            self.vocabulary, 
            n=n, 
            cutoff=self.cutoff
        )
    
    def calculate_similarity(self, word1: str, word2: str) -> float:
        """
        Calculate similarity between two words.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        return difflib.SequenceMatcher(None, word1.lower(), word2.lower()).ratio()
    
    def add_to_vocabulary(self, words: List[str]) -> None:
        """
        Add new words to the vocabulary.
        
        Args:
            words: List of words to add
        """
        for word in words:
            word_lower = word.lower()
            if word_lower not in self.vocabulary:
                self.vocabulary.append(word_lower)
    
    def remove_from_vocabulary(self, words: List[str]) -> None:
        """
        Remove words from the vocabulary.
        
        Args:
            words: List of words to remove
        """
        for word in words:
            word_lower = word.lower()
            if word_lower in self.vocabulary:
                self.vocabulary.remove(word_lower)
    
    def get_vocabulary_stats(self) -> Dict[str, int]:
        """
        Get statistics about the vocabulary.
        
        Returns:
            Dict containing vocabulary statistics
        """
        return {
            'total_words': len(self.vocabulary),
            'unique_first_letters': len(set(word[0] for word in self.vocabulary if word)),
            'average_length': sum(len(word) for word in self.vocabulary) / len(self.vocabulary) if self.vocabulary else 0,
            'shortest_word': min(len(word) for word in self.vocabulary) if self.vocabulary else 0,
            'longest_word': max(len(word) for word in self.vocabulary) if self.vocabulary else 0
        }
    
    def set_similarity_threshold(self, threshold: float) -> None:
        """
        Set the similarity threshold for suggestions.
        
        Args:
            threshold: New threshold value (0.0 to 1.0)
        """
        if 0.0 <= threshold <= 1.0:
            self.cutoff = threshold
        else:
            raise ValueError("Threshold must be between 0.0 and 1.0")
    
    def check_word_exists(self, word: str) -> bool:
        """
        Check if a word exists in the vocabulary.
        
        Args:
            word: Word to check
            
        Returns:
            bool: True if word exists in vocabulary
        """
        return word.lower() in self.vocabulary
    
    def get_correction_confidence(self, original: str, corrected: str) -> float:
        """
        Get confidence score for a correction.
        
        Args:
            original: Original word
            corrected: Corrected word
            
        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        return self.calculate_similarity(original, corrected)
