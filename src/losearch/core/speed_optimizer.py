"""
LoSearch Speed Optimization Engine
موتور بهینه‌سازی سرعت LoSearch
"""

import time
import hashlib
from collections import defaultdict, OrderedDict
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import json

class SpeedOptimizer:
    
    def __init__(self, cache_size: int = 1000):
        # Multi-level caching system
        self.result_cache = OrderedDict()  # Level 1: Complete results
        self.term_cache = OrderedDict()    # Level 2: Term pairs
        self.index_cache = OrderedDict()   # Level 3: Index data
        
        self.cache_size = cache_size
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_queries = 0
        
    def optimized_search(self, query: str, search_func, limit: int = 10) -> Dict[str, Any]:
        """Main optimized search function"""
        start_time = time.time()
        self.total_queries += 1
        
        # Step 1: Quick cache check
        cache_key = self._create_cache_key(query, limit)
        cached_result = self._check_cache(cache_key)
        if cached_result:
            self.cache_hits += 1
            cached_result['processing_time'] = time.time() - start_time
            cached_result['cache_hit'] = True
            return cached_result
            
        self.cache_misses += 1
        
        # Step 2: Parallel search execution
        try:
            future = self.thread_pool.submit(search_func, query, limit)
            result = future.result(timeout=5.0)
            
            # Ensure proper format
            if isinstance(result, list):
                result = {'search_results': result, 'search_stats': {'total_results': len(result)}}
            elif not isinstance(result, dict):
                result = {'search_results': [], 'search_stats': {'total_results': 0}}
                
            # Cache the result
            self._cache_result(cache_key, result)
            
            result['processing_time'] = time.time() - start_time
            result['cache_hit'] = False
            result['optimization_applied'] = True
            
            return result
            
        except Exception as e:
            return {
                'search_results': [],
                'search_stats': {'total_results': 0, 'error': str(e)},
                'processing_time': time.time() - start_time,
                'cache_hit': False,
                'optimization_applied': True
            }
    
    def _create_cache_key(self, query: str, limit: int) -> str:
        query_normalized = query.lower().strip()
        return hashlib.md5(f"{query_normalized}:{limit}".encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[Dict]:
        # Level 1: Result cache
        if cache_key in self.result_cache:
            # Move to end (LRU)
            result = self.result_cache.pop(cache_key)
            self.result_cache[cache_key] = result
            return result.copy()
            
        return None
    
    def _cache_result(self, cache_key: str, result: Dict):
        # Level 1: Result cache
        if len(self.result_cache) >= self.cache_size:
            # Remove oldest
            self.result_cache.popitem(last=False)
            
        self.result_cache[cache_key] = result.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        hit_rate = (self.cache_hits / self.total_queries * 100) if self.total_queries > 0 else 0
        return {
            'total_queries': self.total_queries,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_sizes': {
                'result_cache': len(self.result_cache),
                'term_cache': len(self.term_cache),
                'index_cache': len(self.index_cache)
            }
        }
    
    def clear_cache(self):
        
        self.result_cache.clear()
        self.term_cache.clear()
        self.index_cache.clear()
        
    def warmup_cache(self, common_queries: List[str], search_func):
        for query in common_queries:
            try:
                self.optimized_search(query, search_func, limit=10)
            except:
                continue
