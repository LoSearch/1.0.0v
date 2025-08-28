

import re
import math
import difflib
from collections import defaultdict, Counter
from typing import List, Dict, Any, Set, Tuple

class AccuracyEnhancer:
    
    def __init__(self):
        # Persian/English patterns
        self.persian_chars = set('آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی')
        self.english_chars = set('abcdefghijklmnopqrstuvwxyz')
        
        # Query intent patterns
        self.intent_patterns = {
            'how_to': [r'چگونه', r'چطور', r'how to', r'how can'],
            'definition': [r'چیست', r'تعریف', r'what is', r'define'],
            'comparison': [r'مقایسه', r'تفاوت', r'compare', r'difference', r'vs'],
            'recommendation': [r'بهترین', r'پیشنهاد', r'best', r'recommend', r'suggest']
        }
    
    def enhance_search_accuracy(self, query: str, results: List[Dict], 
                              user_context: Dict = None) -> List[Dict]:
        """Main accuracy enhancement function"""
        if not results:
            return results
            
        # Step 1: Detect query intent
        intent_info = self._detect_query_intent(query)
        
        # Step 2: Calculate relevance scores
        enhanced_results = []
        for result in results:
            enhanced_result = result.copy()
            
            # Calculate multiple relevance signals
            relevance_score = self._calculate_relevance_score(
                query, result, intent_info
            )
            
            enhanced_result['relevance_score'] = relevance_score
            enhanced_result['intent_match'] = intent_info
            enhanced_results.append(enhanced_result)
        
        # Step 3: Sort by enhanced relevance
        enhanced_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Step 4: Diversity filtering
        final_results = self._apply_diversity_filter(enhanced_results)
        
        return final_results
    
    def _detect_query_intent(self, query: str) -> Dict[str, Any]:
        """Detect user intent from query"""
        query_lower = query.lower()
        detected_intents = []
        confidence_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    detected_intents.append(intent)
                    confidence_scores[intent] = confidence_scores.get(intent, 0) + 1
        
        # Determine primary intent
        primary_intent = 'general'
        max_confidence = 0
        
        if confidence_scores:
            primary_intent = max(confidence_scores.items(), key=lambda x: x[1])[0]
            max_confidence = confidence_scores[primary_intent]
        
        return {
            'primary_intent': primary_intent,
            'all_intents': detected_intents,
            'confidence': max_confidence,
            'language': self._detect_language(query)
        }
    
    def _detect_language(self, text: str) -> str:
        """Detect text language"""
        persian_count = sum(1 for char in text if char in self.persian_chars)
        english_count = sum(1 for char in text if char.lower() in self.english_chars)
        
        if persian_count > english_count:
            return 'persian'
        elif english_count > persian_count:
            return 'english'
        else:
            return 'mixed'
    
    def _calculate_relevance_score(self, query: str, result: Dict, 
                                 intent_info: Dict) -> float:
        """Calculate comprehensive relevance score"""
        signals = []
        
        # Signal 1: Text similarity
        text_similarity = self._calculate_text_similarity(query, result)
        signals.append(('text_similarity', text_similarity, 0.4))
        
        # Signal 2: Intent matching
        intent_match = self._calculate_intent_match(result, intent_info)
        signals.append(('intent_match', intent_match, 0.3))
        
        # Signal 3: Position relevance (title vs content)
        position_relevance = self._calculate_position_relevance(query, result)
        signals.append(('position_relevance', position_relevance, 0.2))
        
        # Signal 4: Language consistency
        language_consistency = self._calculate_language_consistency(query, result, intent_info)
        signals.append(('language_consistency', language_consistency, 0.1))
        
        # Weighted combination
        final_score = sum(score * weight for _, score, weight in signals)
        
        return min(final_score, 1.0)
    
    def _calculate_text_similarity(self, query: str, result: Dict) -> float:
        """Calculate text similarity score"""
        query_words = set(query.lower().split())
        title = result.get('title', '').lower()
        content = result.get('content_preview', '').lower()
        
        # Title similarity (higher weight)
        title_words = set(title.split())
        title_similarity = len(query_words & title_words) / max(len(query_words), 1) * 0.7
        
        # Content similarity
        content_words = set(content.split())
        content_similarity = len(query_words & content_words) / max(len(query_words), 1) * 0.3
        
        return title_similarity + content_similarity
    
    def _calculate_intent_match(self, result: Dict, intent_info: Dict) -> float:
        """Calculate intent matching score"""
        intent = intent_info['primary_intent']
        title = result.get('title', '').lower()
        content = result.get('content_preview', '').lower()
        text = title + ' ' + content
        
        # Intent-specific keywords
        intent_keywords = {
            'how_to': ['tutorial', 'guide', 'step', 'method', 'آموزش', 'راهنما'],
            'definition': ['definition', 'meaning', 'concept', 'تعریف', 'مفهوم'],
            'comparison': ['vs', 'comparison', 'difference', 'مقایسه', 'تفاوت'],
            'recommendation': ['best', 'top', 'recommended', 'بهترین', 'پیشنهاد']
        }
        
        if intent in intent_keywords:
            keywords = intent_keywords[intent]
            matches = sum(1 for keyword in keywords if keyword in text)
            return min(matches / len(keywords), 1.0)
        
        return 0.5  # Neutral for general queries
    
    def _calculate_position_relevance(self, query: str, result: Dict) -> float:
        """Calculate positional relevance (title has higher importance)"""
        query_lower = query.lower()
        title = result.get('title', '').lower()
        
        if query_lower in title:
            return 1.0
        
        # Check for partial matches in title
        query_words = query_lower.split()
        title_words = title.split()
        matches = sum(1 for word in query_words if word in title_words)
        
        return matches / max(len(query_words), 1) * 0.8
    
    def _calculate_language_consistency(self, query: str, result: Dict, 
                                      intent_info: Dict) -> float:
        """Calculate language consistency score"""
        query_lang = intent_info['language']
        title = result.get('title', '')
        result_lang = self._detect_language(title)
        
        if query_lang == result_lang or query_lang == 'mixed' or result_lang == 'mixed':
            return 1.0
        else:
            return 0.5  # Partial penalty for language mismatch
    
    def _apply_diversity_filter(self, results: List[Dict]) -> List[Dict]:
        """Apply diversity filtering to avoid too similar results"""
        if len(results) <= 3:
            return results
            
        diverse_results = [results[0]]  # Always include top result
        
        for result in results[1:]:
            # Check similarity with already selected results
            is_diverse = True
            for selected in diverse_results:
                similarity = self._calculate_result_similarity(result, selected)
                if similarity > 0.8:  # Too similar
                    is_diverse = False
                    break
            
            if is_diverse:
                diverse_results.append(result)
            
            # Limit diversity check to top 10 results
            if len(diverse_results) >= 10:
                break
        
        return diverse_results
    
    def _calculate_result_similarity(self, result1: Dict, result2: Dict) -> float:
        """Calculate similarity between two results"""
        title1 = result1.get('title', '').lower()
        title2 = result2.get('title', '').lower()
        
        return difflib.SequenceMatcher(None, title1, title2).ratio()
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get enhancement statistics"""
        return {
            'intent_patterns': len(self.intent_patterns),
            'supported_languages': ['persian', 'english', 'mixed'],
            'relevance_signals': ['text_similarity', 'intent_match', 'position_relevance', 'language_consistency'],
            'diversity_threshold': 0.8
        }
