
import re
import unicodedata
from collections import Counter, defaultdict
from typing import List, Dict, Any, Set, Tuple

class TextProcessor:
    
    def __init__(self):
        # Persian patterns
        self.persian_chars = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        self.persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        
        # Common stop words
        self.persian_stop_words = {
            'از', 'با', 'به', 'در', 'که', 'را', 'و', 'این', 'آن', 'است',
            'های', 'یک', 'تا', 'بر', 'برای', 'یا', 'اما', 'اگر'
        }
        
        self.english_stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this'
        }
        
        # Text patterns
        self.word_pattern = re.compile(r'[a-zA-Zآ-ی]+')
        self.persian_pattern = re.compile(r'[آ-ی]+')
        self.english_pattern = re.compile(r'[a-zA-Z]+')
    
    def extract_words(self, text: str, remove_stop_words: bool = True) -> List[str]:
        if not text:
            return []
            
        # Normalize text
        text = self.normalize_text(text)
        
        # Extract words
        words = self.word_pattern.findall(text.lower())
        
        # Remove stop words if requested
        if remove_stop_words:
            all_stop_words = self.persian_stop_words | self.english_stop_words
            words = [word for word in words if word not in all_stop_words]
        
        return words
    
    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
            
        # Unicode normalization
        text = unicodedata.normalize('NFKC', text)
        
        # Persian character normalization
        text = text.replace('ي', 'ی').replace('ك', 'ک')
        text = text.replace('ة', 'ه').replace('ء', '')
        
        # Persian digits to English
        for persian, english in zip(self.persian_digits, '0123456789'):
            text = text.replace(persian, english)
        
        # Clean extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_terms(self, text: str) -> List[str]:
        words = self.extract_words(text, remove_stop_words=True)
        
        # Filter minimum length
        terms = [word for word in words if len(word) >= 2]
        
        return terms
    
    def extract_phrases(self, text: str, max_phrase_length: int = 3) -> List[str]:
        words = self.extract_words(text, remove_stop_words=False)
        phrases = []
        
        for length in range(2, max_phrase_length + 1):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i + length])
                # Skip if contains stop words at boundaries
                if not (words[i] in self.get_all_stop_words() or 
                       words[i + length - 1] in self.get_all_stop_words()):
                    phrases.append(phrase)
        
        return phrases
    
    def get_all_stop_words(self) -> Set[str]:
        return self.persian_stop_words | self.english_stop_words
    
    def suggest_corrections(self, query: str, valid_terms: List[str]) -> Dict[str, Any]:
        query_words = self.extract_words(query, remove_stop_words=False)
        corrections = []
        corrected_query = query
        needs_correction = False
        
        valid_terms_set = set(term.lower() for term in valid_terms)
        
        for word in query_words:
            word_lower = word.lower()
            if word_lower not in valid_terms_set and len(word) > 2:
                # Find closest matches
                suggestions = self._find_similar_terms(word_lower, valid_terms, max_suggestions=3)
                if suggestions:
                    best_suggestion = suggestions[0]['term']
                    corrections.append({
                        'original': word,
                        'suggested': best_suggestion,
                        'confidence': suggestions[0]['similarity']
                    })
                    corrected_query = corrected_query.replace(word, best_suggestion)
                    needs_correction = True
        
        return {
            'original_query': query,
            'corrected_query': corrected_query,
            'needs_correction': needs_correction,
            'corrections': corrections,
            'suggestions': [c['suggested'] for c in corrections]
        }
    
    def _find_similar_terms(self, word: str, valid_terms: List[str], 
                           max_suggestions: int = 3) -> List[Dict[str, Any]]:
        suggestions = []
        
        for term in valid_terms:
            term_lower = term.lower()
            if len(term_lower) < 2:
                continue
                
            # Quick similarity check
            if abs(len(word) - len(term_lower)) > 2:
                continue
                
            similarity = self._calculate_similarity(word, term_lower)
            if similarity > 0.6:  # Threshold
                suggestions.append({
                    'term': term,
                    'similarity': similarity
                })
        
        # Sort by similarity and return top suggestions
        suggestions.sort(key=lambda x: x['similarity'], reverse=True)
        return suggestions[:max_suggestions]
    
    def _calculate_similarity(self, word1: str, word2: str) -> float:
        if word1 == word2:
            return 1.0
            
        # Levenshtein distance
        len1, len2 = len(word1), len(word2)
        if len1 == 0 or len2 == 0:
            return 0.0
            
        # Create distance matrix
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        # Initialize first row and column
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
        
        # Fill matrix
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if word1[i-1] == word2[j-1]:
                    cost = 0
                else:
                    cost = 1
                    
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # deletion
                    matrix[i][j-1] + 1,      # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )
        
        distance = matrix[len1][len2]
        max_len = max(len1, len2)
        
        return 1.0 - (distance / max_len)
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {
                'word_count': 0,
                'term_count': 0,
                'language': 'unknown',
                'words': [],
                'terms': [],
                'phrases': []
            }
        
        # Extract components
        words = self.extract_words(text, remove_stop_words=False)
        terms = self.extract_terms(text)
        phrases = self.extract_phrases(text)
        
        # Language detection
        language = self._detect_language(text)
        
        # Statistics
        word_freq = Counter(words)
        term_freq = Counter(terms)
        
        return {
            'word_count': len(words),
            'unique_words': len(set(words)),
            'term_count': len(terms),
            'unique_terms': len(set(terms)),
            'phrase_count': len(phrases),
            'language': language,
            'words': words,
            'terms': terms,
            'phrases': phrases,
            'word_frequency': dict(word_freq.most_common(10)),
            'term_frequency': dict(term_freq.most_common(10))
        }
    
    def _detect_language(self, text: str) -> str:
        persian_count = len(self.persian_pattern.findall(text))
        english_count = len(self.english_pattern.findall(text))
        
        if persian_count > english_count:
            return 'persian'
        elif english_count > persian_count:
            return 'english'
        elif persian_count > 0 and english_count > 0:
            return 'mixed'
        else:
            return 'unknown'