import time
import re
import math
from typing import List, Dict, Any, Optional
from collections import Counter
import json

from .search_engine import LoSearch
from .speed_optimizer import SpeedOptimizer
from .accuracy_enhancer import AccuracyEnhancer
from ..utils.text_processor import TextProcessor
from ..utils.context_extractor import ContextExtractor

class LoSearchEngine:

    def __init__(self, enable_optimization: bool = True):
        self.core_engine = LoSearch(use_advanced_engine=True)
        self.text_processor = TextProcessor()
        self.context_extractor = ContextExtractor()

        self.optimization_enabled = enable_optimization
        if enable_optimization:
            self.speed_optimizer = SpeedOptimizer()
            self.accuracy_enhancer = AccuracyEnhancer()
        else:
            self.speed_optimizer = None
            self.accuracy_enhancer = None

        self._documents_indexed = False
        self._cached_valid_terms = None
        self._doc_lookup = {}
        self.idf_scores = {}

    def _update_doc_lookup(self):
        self._doc_lookup = {}
        for i, doc in enumerate(self.core_engine.documents):
            doc_id = str(doc.get('id', i))
            self._doc_lookup[doc_id] = doc

    def _calculate_idf(self):
        total_docs = len(self.core_engine.documents)
        if total_docs == 0:
            return

        # Uses the inverted index from the core engine
        for term, doc_indices in self.core_engine.inverted_index.items():
            doc_freq = len(set(doc_indices))
            self.idf_scores[term] = math.log(total_docs / (1 + doc_freq))

    def add_documents(self, documents: List[Dict]) -> Dict[str, Any]:
        result = self.core_engine.add_products_bulk(documents)
        self._documents_indexed = True
        self._update_doc_lookup()
        self._calculate_idf() # Calculate IDF scores after indexing
        return result

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        if self.optimization_enabled and self.speed_optimizer:
            def search_func(q, l):
                return self.core_engine.search_sync(q, limit=l)

            result = self.speed_optimizer.optimized_search(query, search_func, limit)
            return result.get('search_results', result if isinstance(result, list) else [])
        else:
            return self.core_engine.search_sync(query, limit=limit)

    def smart_search(self, query: str, documents: List[Dict] = None, 
                    limit: int = 10) -> Dict[str, Any]:
        start_time = time.time()

        results = {
            'original_query': query,
            'search_results': [],
            'search_stats': {},
            'processing_time': 0,
            'correction_applied': False,
            'optimization_applied': self.optimization_enabled
        }

        if documents and not self._documents_indexed:
            self.add_documents(documents)

        if self.optimization_enabled and self.speed_optimizer:
            def search_func(q, l):
                return {'search_results': self.core_engine.search_sync(q, limit=l)}

            search_result = self.speed_optimizer.optimized_search(
                query, lambda q, l: search_func(q, l), limit
            )
            initial_results = search_result.get('search_results', [])

            if initial_results and self.accuracy_enhancer:
                initial_results = self.accuracy_enhancer.enhance_search_accuracy(
                    query, initial_results, user_context={}
                )
        else:
            initial_results = self.core_engine.search_sync(query, limit=limit)

        if len(initial_results) < 3:
            correction_info = self.fix_query(query, documents if not self._cached_valid_terms else None)
            if correction_info['needs_correction'] and correction_info['corrected_query'] != query:
                corrected_results = self.search(correction_info['corrected_query'], limit)
                if len(corrected_results) > len(initial_results):
                    results['corrected_query'] = correction_info['corrected_query']
                    results['correction_applied'] = True
                    results['suggestions'] = correction_info['suggestions']
                    initial_results = corrected_results

        results['search_results'] = initial_results
        processing_time = time.time() - start_time
        results['search_stats'] = {
            'total_results': len(initial_results),
            'processing_time': processing_time,
            'has_corrections': results['correction_applied']
        }
        results['processing_time'] = processing_time

        return results

    def contextual_search(self, query: str, documents: List[Dict] = None, 
                          limit: int = 10, mode: str = 'simple', top_sentences: int = 3) -> Dict[str, Any]:
        start_time = time.time()

        results = {
            'original_query': query,
            'search_results': [],
            'search_stats': {},
            'processing_time': 0,
            'correction_applied': False,
            'optimization_applied': self.optimization_enabled
        }

        if documents and not self._documents_indexed:
            self.add_documents(documents)

        # Validate mode
        if mode not in ['simple', 'advanced']:
            raise ValueError("Mode must be either 'simple' or 'advanced'")

        initial_results = self.search(query, limit)
        final_query = query

        if len(initial_results) < 3:
            correction_info = self.fix_query(query, documents if not self._cached_valid_terms else None)
            if correction_info['needs_correction'] and correction_info['corrected_query'] != query:
                corrected_results = self.search(correction_info['corrected_query'], limit)
                if len(corrected_results) > len(initial_results):
                    results['corrected_query'] = correction_info['corrected_query']
                    results['correction_applied'] = True
                    results['suggestions'] = correction_info['suggestions']
                    initial_results = corrected_results
                    final_query = correction_info['corrected_query']

        contextual_results = []
        for res in initial_results:
            doc_id = str(res.get('id'))
            full_doc = self._doc_lookup.get(doc_id)

            new_res = res.copy()
            if full_doc and 'content' in full_doc:
                # استفاده از قابلیت جدید برای دریافت چندین جمله برتر
                top_sentences_list = self.context_extractor.find_top_sentences(
                    final_query, full_doc['content'], self.text_processor,
                    top_n=top_sentences, mode=mode, idf_scores=self.idf_scores
                )
                new_res['context_sentences'] = top_sentences_list
                # حفظ سازگاری با نسخه قبل
                new_res['context_sentence'] = top_sentences_list[0] if top_sentences_list else ''
            else:
                preview = new_res.get('content_preview', '')
                new_res['context_sentences'] = [preview] if preview else []
                new_res['context_sentence'] = preview

            if 'content_preview' in new_res:
                del new_res['content_preview']
            contextual_results.append(new_res)

        results['search_results'] = contextual_results
        processing_time = time.time() - start_time
        results['processing_time'] = processing_time
        results['search_stats'] = {
            'total_results': len(contextual_results),
            'processing_time': processing_time,
            'mode': mode,
            'top_sentences': top_sentences,
            'has_corrections': results['correction_applied']
        }

        return results

    def contextual_search_with_scores(self, query: str, documents: List[Dict] = None, 
                                    limit: int = 10, mode: str = 'simple', 
                                    top_sentences: int = 3) -> Dict[str, Any]:
        """
        جستجوی متنی با برگرداندن جملات برتر همراه با امتیازاتشان
        """
        start_time = time.time()

        results = {
            'original_query': query,
            'search_results': [],
            'search_stats': {},
            'processing_time': 0,
            'correction_applied': False,
            'optimization_applied': self.optimization_enabled
        }

        if documents and not self._documents_indexed:
            self.add_documents(documents)

        if mode not in ['simple', 'advanced']:
            raise ValueError("Mode must be either 'simple' or 'advanced'")

        initial_results = self.search(query, limit)
        final_query = query

        if len(initial_results) < 3:
            correction_info = self.fix_query(query, documents if not self._cached_valid_terms else None)
            if correction_info['needs_correction'] and correction_info['corrected_query'] != query:
                corrected_results = self.search(correction_info['corrected_query'], limit)
                if len(corrected_results) > len(initial_results):
                    results['corrected_query'] = correction_info['corrected_query']
                    results['correction_applied'] = True
                    results['suggestions'] = correction_info['suggestions']
                    initial_results = corrected_results
                    final_query = correction_info['corrected_query']

        contextual_results = []
        for res in initial_results:
            doc_id = str(res.get('id'))
            full_doc = self._doc_lookup.get(doc_id)

            new_res = res.copy()
            if full_doc and 'content' in full_doc:
                # دریافت جملات برتر همراه با امتیازات
                sentences_with_scores = self.context_extractor.find_top_sentences_with_scores(
                    final_query, full_doc['content'], self.text_processor,
                    top_n=top_sentences, mode=mode, idf_scores=self.idf_scores
                )
                new_res['context_sentences_with_scores'] = sentences_with_scores
                new_res['context_sentences'] = [sentence for sentence, score in sentences_with_scores]
                new_res['context_sentence'] = sentences_with_scores[0][0] if sentences_with_scores else ''
            else:
                preview = new_res.get('content_preview', '')
                new_res['context_sentences_with_scores'] = [(preview, 0.0)] if preview else []
                new_res['context_sentences'] = [preview] if preview else []
                new_res['context_sentence'] = preview

            if 'content_preview' in new_res:
                del new_res['content_preview']
            contextual_results.append(new_res)

        results['search_results'] = contextual_results
        processing_time = time.time() - start_time
        results['processing_time'] = processing_time
        results['search_stats'] = {
            'total_results': len(contextual_results),
            'processing_time': processing_time,
            'mode': mode,
            'top_sentences': top_sentences,
            'has_corrections': results['correction_applied'],
            'includes_scores': True
        }

        return results

    def fix_query(self, query: str, documents: List[Dict] = None) -> Dict[str, Any]:
        if not hasattr(self, '_cached_valid_terms') or self._cached_valid_terms is None:
            if documents:
                all_text = ""
                for doc in documents[:100]:
                    all_text += " " + doc.get('title', '') + " " + doc.get('content', '')

                self._cached_valid_terms = set(self.text_processor.extract_words(all_text))
            else:
                self._cached_valid_terms = {'machine', 'learning', 'python', 'programming', 
                                          'database', 'security', 'web', 'development'}

        return self.text_processor.suggest_corrections(query, list(self._cached_valid_terms))

    def analyze_text(self, text: str) -> Dict[str, Any]:
        return self.text_processor.analyze_text(text)

    def get_performance_stats(self) -> Dict[str, Any]:
        stats = {
            'optimization_enabled': self.optimization_enabled,
            'documents_indexed': self._documents_indexed,
            'cached_terms_count': len(self._cached_valid_terms) if self._cached_valid_terms else 0,
            'idf_terms_count': len(self.idf_scores)
        }

        if self.speed_optimizer:
            stats['speed_optimizer'] = self.speed_optimizer.get_stats()

        return stats
