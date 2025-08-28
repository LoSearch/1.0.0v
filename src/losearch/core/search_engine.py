
import time
import math
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict

class LoSearch:

    def __init__(self, use_advanced_engine: bool = True):
        self.documents = []
        self.inverted_index = defaultdict(list)
        self.use_advanced_engine = use_advanced_engine

    def add_products_bulk(self, documents: List[Dict]) -> Dict[str, Any]:
        self.documents.extend(documents)

        for i, doc in enumerate(documents):
            doc_index = len(self.documents) - len(documents) + i
            text = (doc.get('title', '') + ' ' + doc.get('content', '')).lower()
            words = self._extract_words(text)

            for word in words:
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                self.inverted_index[word].append(doc_index)

        return {
            'indexed_documents': len(documents),
            'total_documents': len(self.documents),
            'index_size': len(self.inverted_index)
        }

    def search_sync(self, query: str, limit: int = 10) -> List[Dict]:
        if not self.documents:
            return []

        query_words = self._extract_words(query.lower())
        if not query_words:
            return []

        candidates = set()
        for word in query_words:
            if word in self.inverted_index:
                candidates.update(self.inverted_index[word])

        if not candidates:
            return []

        scored_results = []
        for doc_idx in candidates:
            if doc_idx < len(self.documents):
                doc = self.documents[doc_idx]
                score = self._calculate_score(query_words, doc)

                result = {
                    'id': doc.get('id', str(doc_idx)),
                    'title': doc.get('title', ''),
                    'content_preview': doc.get('content', '')[:200],
                    'score': score
                }
                scored_results.append(result)

        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return scored_results[:limit]

    def _extract_words(self, text: str) -> List[str]:
        import re
        words = re.findall(r'[a-zA-Zآ-ی]+', text)
        return [word for word in words if len(word) >= 2]

    def _calculate_score(self, query_words: List[str], document: Dict) -> float:
        title = document.get('title', '').lower()
        content = document.get('content', '').lower()

        title_words = self._extract_words(title)
        content_words = self._extract_words(content)

        score = 0.0

        title_matches = sum(1 for word in query_words if word in title_words)
        score += title_matches * 3.0

        content_matches = sum(1 for word in query_words if word in content_words)
        score += content_matches * 1.0

        full_text = title + ' ' + content
        if ' '.join(query_words) in full_text:
            score += 2.0

        doc_length = len(title_words) + len(content_words)
        if doc_length > 0:
            score = score / math.log(doc_length + 1)

        return score
