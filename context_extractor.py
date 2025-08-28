
import re
import math
from typing import Set, List, Dict, Tuple

class ContextExtractor:

    def find_best_sentence(self, query: str, content: str, text_processor, 
                           mode: str = 'simple', idf_scores: Dict[str, float] = None) -> str:
        
        top_sentences = self.find_top_sentences(query, content, text_processor, 
                                               top_n=1, mode=mode, idf_scores=idf_scores)
        return top_sentences[0] if top_sentences else ""

    def find_top_sentences(self, query: str, content: str, text_processor, 
                          top_n: int = 3, mode: str = 'simple', 
                          idf_scores: Dict[str, float] = None) -> List[str]:
        
        if not content:
            return []

        sentences = re.split(r'(?<=[.!?؟])\s+', content.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if not sentences:
            return [content[:250]] if content else []

        query_terms = set(text_processor.extract_terms(query))
        if not query_terms:
            return sentences[:top_n]

        scored_sentences = []

        for sentence in sentences:
            if mode == 'advanced' and idf_scores:
                score = self._score_sentence_advanced(sentence, query, query_terms, text_processor, idf_scores)
            else:
                score = self._score_sentence_simple(sentence, query_terms, text_processor)

            scored_sentences.append((sentence, score))

        scored_sentences.sort(key=lambda x: x[1], reverse=True)

        top_sentences = [sentence for sentence, score in scored_sentences[:top_n] if score > 0]

        
        if not top_sentences:
            top_sentences = sentences[:top_n]

        return top_sentences

    def find_top_sentences_with_scores(self, query: str, content: str, text_processor, 
                                     top_n: int = 3, mode: str = 'simple', 
                                     idf_scores: Dict[str, float] = None) -> List[Tuple[str, float]]:
        
        if not content:
            return []

        sentences = re.split(r'(?<=[.!?؟])\s+', content.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if not sentences:
            return [(content[:250], 0.0)] if content else []

        query_terms = set(text_processor.extract_terms(query))
        if not query_terms:
            return [(sentence, 0.0) for sentence in sentences[:top_n]]

        scored_sentences = []

        for sentence in sentences:
            if mode == 'advanced' and idf_scores:
                score = self._score_sentence_advanced(sentence, query, query_terms, text_processor, idf_scores)
            else:
                score = self._score_sentence_simple(sentence, query_terms, text_processor)

            scored_sentences.append((sentence, score))

        scored_sentences.sort(key=lambda x: x[1], reverse=True)

        return scored_sentences[:top_n]

    def _score_sentence_simple(self, sentence: str, query_terms: Set[str], text_processor) -> float:
        sentence_terms = set(text_processor.extract_terms(sentence))
        if not sentence_terms:
            return 0.0

        common_terms = query_terms.intersection(sentence_terms)

        score = len(common_terms) + (len(common_terms) / len(sentence_terms))
        return score

    def _score_sentence_advanced(self, sentence: str, query: str, query_terms: Set[str], 
                                 text_processor, idf_scores: Dict[str, float]) -> float:

        sentence_words = text_processor.extract_words(sentence, remove_stop_words=False)
        if not sentence_words:
            return 0.0

        sentence_terms = set(word for word in sentence_words if word in query_terms)
        if not sentence_terms:
            return 0.0

        tfidf_score = 0.0
        for term in sentence_terms:
            tf = sentence_words.count(term)
            idf = idf_scores.get(term, 1.0) 
            tfidf_score += tf * idf

        proximity_score = 0.0
        match_indices = [i for i, word in enumerate(sentence_words) if word in query_terms]
        if len(match_indices) > 1:
            span = max(match_indices) - min(match_indices)
            
            proximity_score = len(match_indices) / (span + 1)

        phrase_bonus = 0.0
        normalized_sentence = " ".join(sentence_words)
        if query.lower() in normalized_sentence:
            phrase_bonus = 5.0 
        final_score = (tfidf_score * 0.5) + (proximity_score * 0.3) + (phrase_bonus * 0.2)

        
        final_score /= math.log(len(sentence_words) + 1)

        return final_score
