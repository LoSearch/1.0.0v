
# LoSearch Library - Complete Tutorial

LoSearch is a high-performance Python search library with intelligent relevance scoring, advanced indexing capabilities, and Persian/English multilingual support.

## Installation

```bash
pip install losearch
```

## Quick Start

```python
import losearch as ls

# Initialize search engine
search = ls.LoSearch(enable_optimization=True)

# Add documents
documents = [
    {"id": "1", "title": "MacBook Pro", "content": "High-performance laptop with M2 chip"},
    {"id": "2", "title": "iPhone 15", "content": "Latest smartphone with advanced camera"}
]

search.add_documents(documents)

# Search
results = search.search("laptop performance")
for result in results:
    print(f"{result['title']} - Score: {result['score']}")
```

## Core Classes

### Main LoSearch Class

```python
import losearch as ls

# Initialize with optimization (recommended)
search = ls.LoSearch(enable_optimization=True)

# Initialize without optimization
search = ls.LoSearch(enable_optimization=False)
```

### Advanced Components

```python
import losearch as ls

# Access core components directly:
engine = ls.core.engine.LoSearchEngine(enable_optimization=True)
optimizer = ls.core.speed_optimizer.SpeedOptimizer(cache_size=1000)
enhancer = ls.core.accuracy_enhancer.AccuracyEnhancer()
processor = ls.utils.text_processor.TextProcessor()
extractor = ls.utils.context_extractor.ContextExtractor()
```

## Document Management

### Adding Documents

```python
# Single batch of documents
products = [
    {
        "id": "laptop_001",
        "title": "Gaming Laptop",
        "content": "High-end gaming laptop with RTX 4080 graphics and 32GB RAM"
    },
    {
        "id": "phone_001", 
        "title": "iPhone 15 Pro",
        "content": "Latest smartphone with A17 Pro chip and titanium design"
    }
]

result = search.add_documents(products)
print(f"Indexed: {result['indexed_documents']} documents")
print(f"Total: {result['total_documents']} documents")
```

## Search Functions

### Basic Search

```python
# Simple search
results = search.search("gaming laptop")

# With custom limit
results = search.search("smartphone camera", limit=5)

# Process results
for result in results:
    print(f"ID: {result['id']}")
    print(f"Title: {result['title']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Preview: {result['content_preview'][:100]}")
```

### Smart Search with Auto-Correction

```python
# Smart search fixes typos automatically
result = search.smart_search("laptp gaming")  # Will correct "laptp" to "laptop"

print(f"Original: {result['original_query']}")
print(f"Corrected: {result['corrected_query']}")
print(f"Processing time: {result['processing_time']:.3f}s")

if result['correction_applied']:
    print("Corrections applied:")
    for correction in result.get('corrections', []):
        print(f"  '{correction['original']}' → '{correction['suggested']}'")

for item in result['search_results']:
    print(f"- {item['title']} (Score: {item['score']:.2f})")
```

### Contextual Search

```python
# Find relevant sentences in documents
result = search.contextual_search("machine learning algorithms", limit=5)

for doc in result['search_results']:
    print(f"Document: {doc['title']}")
    print(f"Best sentence: {doc['context_sentence']}")
    print("Top sentences:")
    for sentence in doc['context_sentences']:
        print(f"  - {sentence}")
```

### Contextual Search with Scores

```python
# Get sentences with relevance scores
result = search.contextual_search_with_scores(
    query="artificial intelligence",
    top_sentences=3,
    mode='advanced'
)

for doc in result['search_results']:
    print(f"Document: {doc['title']}")
    for sentence, score in doc['context_sentences_with_scores']:
        print(f"  Score: {score:.3f} | {sentence[:80]}...")
```

## Query Processing

### Query Correction

```python
# Fix typos and get suggestions
correction = search.fix_query("machne lerning")

print(f"Original: {correction['original_query']}")
print(f"Corrected: {correction['corrected_query']}")
print(f"Needs correction: {correction['needs_correction']}")

if correction['corrections']:
    for fix in correction['corrections']:
        print(f"'{fix['original']}' → '{fix['suggested']}'")
```

### Text Analysis

```python
# Analyze any text
analysis = search.analyze_text("Machine learning and AI are transforming technology")

print(f"Language: {analysis['language']}")
print(f"Words: {analysis['word_count']}")
print(f"Terms: {analysis['terms'][:5]}")
print(f"Phrases: {analysis['phrases'][:3]}")
```

## Advanced Core Engine Usage

### Using LoSearchEngine Directly

```python
import losearch as ls

engine = ls.core.engine.LoSearchEngine(enable_optimization=True)

# Add documents
docs = [{"id": "1", "title": "AI Guide", "content": "Complete AI tutorial"}]
result = engine.add_documents(docs)
print(f"Indexed: {result['indexed_documents']} documents")

# Basic search
results = engine.search("AI tutorial", limit=5)

# Smart search with full features
smart_results = engine.smart_search("AI tutorial", limit=5)

# Contextual search
contextual_results = engine.contextual_search(
    query="AI tutorial", 
    mode='advanced', 
    top_sentences=3
)

# Contextual search with scores
scored_results = engine.contextual_search_with_scores(
    query="AI tutorial",
    mode='advanced',
    top_sentences=3
)

# Fix query
correction = engine.fix_query("AI tutorail")

# Analyze text
analysis = engine.analyze_text("AI and machine learning")

# Get performance stats
stats = engine.get_performance_stats()
```

## Text Processing Utilities

### Complete TextProcessor Usage

```python
import losearch as ls

processor = ls.utils.text_processor.TextProcessor()

# Extract words
text = "Machine learning algorithms are powerful tools"
words = processor.extract_words(text, remove_stop_words=True)
print(f"Words: {words}")

# Extract words without removing stop words
all_words = processor.extract_words(text, remove_stop_words=False)
print(f"All words: {all_words}")

# Extract terms
terms = processor.extract_terms(text)
print(f"Terms: {terms}")

# Extract phrases
phrases = processor.extract_phrases(text, max_phrase_length=3)
print(f"Phrases: {phrases}")

# Normalize text
persian_text = "یادگیری ماشین و هوش مصنوعی"
normalized = processor.normalize_text(persian_text)
print(f"Normalized: {normalized}")

# Get all stop words
stop_words = processor.get_all_stop_words()
print(f"Stop words count: {len(stop_words)}")

# Get corrections
valid_terms = ["machine", "learning", "algorithm"]
corrections = processor.suggest_corrections("machne lerning", valid_terms)
print(f"Corrections: {corrections}")

# Complete text analysis
analysis = processor.analyze_text(text)
print(f"Analysis: {analysis}")

# Language detection (internal method usage)
language = processor._detect_language(text)
print(f"Language: {language}")

# Find similar terms (internal method)
similar = processor._find_similar_terms("machne", valid_terms, max_suggestions=3)
print(f"Similar terms: {similar}")

# Calculate similarity (internal method)
similarity = processor._calculate_similarity("machine", "machne")
print(f"Similarity: {similarity}")
```

## Context Extraction Utilities

### Complete ContextExtractor Usage

```python
import losearch as ls

extractor = ls.utils.context_extractor.ContextExtractor()
processor = ls.utils.text_processor.TextProcessor()

content = """
Machine learning enables computers to learn from data automatically.
It uses algorithms to find patterns and make predictions.
Deep learning is a subset that uses neural networks.
Neural networks are inspired by biological neural systems.
"""

query = "machine learning algorithms"

# Find best sentence
best = extractor.find_best_sentence(query, content, processor)
print(f"Best sentence: {best}")

# Find best sentence with advanced mode
best_advanced = extractor.find_best_sentence(
    query, content, processor, mode='advanced'
)
print(f"Best (advanced): {best_advanced}")

# Find top sentences
top = extractor.find_top_sentences(query, content, processor, top_n=2)
print(f"Top sentences: {top}")

# Find top sentences with advanced mode
top_advanced = extractor.find_top_sentences(
    query, content, processor, top_n=2, mode='advanced'
)
print(f"Top (advanced): {top_advanced}")

# Find top sentences with scores
scored = extractor.find_top_sentences_with_scores(
    query, content, processor, top_n=2
)
for sentence, score in scored:
    print(f"Score: {score:.3f} | {sentence}")

# Find top sentences with scores (advanced mode)
scored_advanced = extractor.find_top_sentences_with_scores(
    query, content, processor, top_n=2, mode='advanced'
)
for sentence, score in scored_advanced:
    print(f"Advanced Score: {score:.3f} | {sentence}")

# Internal scoring methods (for advanced users)
# Simple scoring
query_terms = set(processor.extract_terms(query))
simple_score = extractor._score_sentence_simple(
    "Machine learning uses algorithms", query_terms, processor
)
print(f"Simple score: {simple_score}")

# Advanced scoring (requires IDF scores)
idf_scores = {"machine": 1.5, "learning": 1.3, "algorithms": 1.8}
advanced_score = extractor._score_sentence_advanced(
    "Machine learning uses algorithms", query, query_terms, processor, idf_scores
)
print(f"Advanced score: {advanced_score}")
```

## Speed Optimization

### Complete SpeedOptimizer Usage

```python
import losearch as ls

optimizer = ls.core.speed_optimizer.SpeedOptimizer(cache_size=1000)

# Define search function
def my_search(query, limit):
    # Your search logic here
    return {"search_results": [{"title": "Sample", "score": 0.8}]}

# Optimized search with caching
result = optimizer.optimized_search("test query", my_search, limit=10)
print(f"Results: {result}")

# Check performance statistics
stats = optimizer.get_stats()
print(f"Cache hit rate: {stats['hit_rate']}")
print(f"Total queries: {stats['total_queries']}")
print(f"Cache hits: {stats['cache_hits']}")
print(f"Cache misses: {stats['cache_misses']}")
print(f"Cache sizes: {stats['cache_sizes']}")

# Warm up cache with common queries
common_queries = ["machine learning", "AI", "deep learning"]
optimizer.warmup_cache(common_queries, my_search)

# Clear cache
optimizer.clear_cache()

# Create cache key (internal method)
cache_key = optimizer._create_cache_key("test query", 10)
print(f"Cache key: {cache_key}")

# Manual cache operations (internal methods)
test_result = {"search_results": []}
optimizer._cache_result(cache_key, test_result)
cached = optimizer._check_cache(cache_key)
print(f"Cached result: {cached}")
```

## Accuracy Enhancement

### Complete AccuracyEnhancer Usage

```python
import losearch as ls

enhancer = ls.core.accuracy_enhancer.AccuracyEnhancer()

# Sample results for enhancement
results = [
    {
        "id": "1",
        "title": "Machine Learning Guide", 
        "content_preview": "Complete guide to ML algorithms and techniques"
    },
    {
        "id": "2",
        "title": "AI Basics", 
        "content_preview": "Introduction to artificial intelligence fundamentals"
    }
]

# Enhance search accuracy
enhanced = enhancer.enhance_search_accuracy(
    query="machine learning tutorial",
    results=results,
    user_context={"language": "english", "domain": "technology"}
)

print(f"Enhanced results:")
for result in enhanced:
    print(f"- {result['title']} (Relevance: {result.get('relevance_score', 0):.3f})")

# Get enhancement statistics
stats = enhancer.get_enhancement_stats()
print(f"Enhancement stats: {stats}")

# Internal methods for advanced usage

# Detect query intent
intent = enhancer._detect_query_intent("how to learn machine learning")
print(f"Query intent: {intent}")

# Detect language
language = enhancer._detect_language("یادگیری ماشین")
print(f"Language: {language}")

# Calculate relevance score
relevance = enhancer._calculate_relevance_score(
    "machine learning", results[0], intent
)
print(f"Relevance score: {relevance}")

# Calculate text similarity
text_sim = enhancer._calculate_text_similarity("ML guide", results[0])
print(f"Text similarity: {text_sim}")

# Calculate intent match
intent_match = enhancer._calculate_intent_match(results[0], intent)
print(f"Intent match: {intent_match}")

# Calculate position relevance
pos_rel = enhancer._calculate_position_relevance("machine learning", results[0])
print(f"Position relevance: {pos_rel}")

# Calculate language consistency
lang_cons = enhancer._calculate_language_consistency(
    "machine learning", results[0], intent
)
print(f"Language consistency: {lang_cons}")

# Apply diversity filter
diverse = enhancer._apply_diversity_filter(enhanced)
print(f"Diverse results: {len(diverse)}")

# Calculate result similarity
result_sim = enhancer._calculate_result_similarity(results[0], results[1])
print(f"Result similarity: {result_sim}")
```

## Individual Function Usage

### Single-Process Functions

```python
import losearch as ls

# Direct simple search function
documents = [
    {"id": "1", "title": "Python Guide", "content": "Learn Python programming"},
    {"id": "2", "title": "AI Tutorial", "content": "Artificial intelligence basics"}
]

# Simple search function
search_results = ls.search("Python programming", documents, limit=5)
print(f"Simple search results: {search_results}")

# Smart search function
smart_results = ls.smart_search("Pythun programing", documents, limit=5)
print(f"Smart search results: {smart_results}")

# Text analysis function
text_analysis = ls.analyze_text("Python is great for machine learning")
print(f"Text analysis: {text_analysis}")
```

### Core Search Engine Methods

```python
import losearch as ls

# Create core search engine
core_engine = ls.core.search_engine.LoSearch(use_advanced_engine=True)

# Add documents in bulk
docs = [{"id": "1", "title": "Test", "content": "Test content"}]
result = core_engine.add_products_bulk(docs)
print(f"Bulk add result: {result}")

# Synchronous search
sync_results = core_engine.search_sync("test", limit=10)
print(f"Sync search: {sync_results}")

# Internal word extraction
words = core_engine._extract_words("machine learning algorithms")
print(f"Extracted words: {words}")

# Internal score calculation
score = core_engine._calculate_score(["machine", "learning"], docs[0])
print(f"Calculated score: {score}")
```

### Text Processor Internal Methods

```python
import losearch as ls

processor = ls.utils.text_processor.TextProcessor()

# Access internal attributes
print(f"Persian characters: {processor.persian_chars[:10]}...")
print(f"Persian digits: {processor.persian_digits}")
print(f"Persian stop words: {list(processor.persian_stop_words)[:5]}...")
print(f"English stop words: {list(processor.english_stop_words)[:5]}...")

# Pattern matching
text = "یادگیری ماشین و machine learning"
persian_matches = processor.persian_pattern.findall(text)
english_matches = processor.english_pattern.findall(text)
print(f"Persian matches: {persian_matches}")
print(f"English matches: {english_matches}")

# Word pattern extraction
word_matches = processor.word_pattern.findall(text)
print(f"Word matches: {word_matches}")
```

### Context Extractor Internal Methods

```python
import losearch as ls

extractor = ls.utils.context_extractor.ContextExtractor()
processor = ls.utils.text_processor.TextProcessor()

# Internal scoring demonstrations
sentence = "Machine learning algorithms are powerful tools for data analysis"
query = "machine learning"
query_terms = set(processor.extract_terms(query))

# Simple sentence scoring
simple_score = extractor._score_sentence_simple(sentence, query_terms, processor)
print(f"Simple sentence score: {simple_score}")

# Advanced sentence scoring (with IDF scores)
idf_scores = {"machine": 1.2, "learning": 1.1, "algorithms": 1.5, "data": 0.8}
advanced_score = extractor._score_sentence_advanced(
    sentence, query, query_terms, processor, idf_scores
)
print(f"Advanced sentence score: {advanced_score}")
```

## Real-World Examples

### E-commerce Product Search

```python
import losearch as ls

# Setup
search = ls.LoSearch(enable_optimization=True)

# Products
products = [
    {
        "id": "p1",
        "title": "MacBook Pro 16-inch",
        "content": "Apple laptop with M2 Max chip, 32GB RAM, professional performance"
    },
    {
        "id": "p2",
        "title": "Dell XPS 15",
        "content": "Windows laptop with Intel i9, 32GB RAM, NVIDIA graphics"
    }
]

search.add_documents(products)

# Search with typo correction
result = search.smart_search("macbok laptop")
print(f"Found {len(result['search_results'])} products")
```

### Document Search

```python
# Technical documents
docs = [
    {
        "id": "doc1",
        "title": "Machine Learning Introduction",
        "content": "ML is AI subset that learns from data without explicit programming"
    },
    {
        "id": "doc2", 
        "title": "Deep Learning Guide",
        "content": "DL uses neural networks with multiple layers for complex pattern recognition"
    }
]

search.add_documents(docs)

# Contextual search
result = search.contextual_search("neural networks", mode='advanced')
for doc in result['search_results']:
    print(f"Doc: {doc['title']}")
    print(f"Context: {doc['context_sentence']}")
```

### Multilingual Search

```python
# Mixed language documents
mixed_docs = [
    {
        "id": "m1",
        "title": "هوش مصنوعی و AI",
        "content": "هوش مصنوعی شامل machine learning و deep learning است"
    },
    {
        "id": "m2",
        "title": "Python for AI",
        "content": "Python best language for artificial intelligence programming"
    }
]

search.add_documents(mixed_docs)

# Search in Persian
persian_results = search.search("یادگیری ماشین")

# Search in English  
english_results = search.search("artificial intelligence")
```

### Advanced Component Integration

```python
import losearch as ls

# Create all components
engine = ls.core.engine.LoSearchEngine(enable_optimization=True)
optimizer = ls.core.speed_optimizer.SpeedOptimizer(cache_size=500)
enhancer = ls.core.accuracy_enhancer.AccuracyEnhancer()
processor = ls.utils.text_processor.TextProcessor()
extractor = ls.utils.context_extractor.ContextExtractor()

# Complex workflow
documents = [
    {"id": "1", "title": "AI Research", "content": "Latest AI research and developments"},
    {"id": "2", "title": "ML Applications", "content": "Real-world machine learning applications"}
]

# Step 1: Add documents
engine.add_documents(documents)

# Step 2: Analyze query
query = "AI research and machine learning applications"
analysis = processor.analyze_text(query)
print(f"Query analysis: {analysis}")

# Step 3: Get corrections if needed
corrections = processor.suggest_corrections(query, ["AI", "research", "machine", "learning"])
print(f"Query corrections: {corrections}")

# Step 4: Perform optimized search
def search_func(q, l):
    return engine.search(q, l)

optimized_result = optimizer.optimized_search(query, search_func, limit=10)
print(f"Optimized search: {optimized_result}")

# Step 5: Enhance accuracy
enhanced_results = enhancer.enhance_search_accuracy(
    query, optimized_result.get('search_results', [])
)
print(f"Enhanced results: {enhanced_results}")

# Step 6: Extract context
for result in enhanced_results:
    if 'content' in result:
        best_sentence = extractor.find_best_sentence(
            query, result['content'], processor, mode='advanced'
        )
        print(f"Best context for {result['title']}: {best_sentence}")
```

## Performance Monitoring

```python
# Get comprehensive performance statistics
stats = search.get_performance_stats()

print(f"Optimization: {stats['optimization_enabled']}")
print(f"Documents: {stats['documents_indexed']}")
print(f"Cache terms: {stats['cached_terms_count']}")
print(f"IDF terms: {stats['idf_terms_count']}")

if 'speed_optimizer' in stats:
    opt_stats = stats['speed_optimizer']
    print(f"Cache hit rate: {opt_stats['hit_rate']}")
    print(f"Total queries: {opt_stats['total_queries']}")
    print(f"Cache sizes: {opt_stats['cache_sizes']}")

# Individual component stats
if hasattr(search.engine, 'speed_optimizer') and search.engine.speed_optimizer:
    optimizer_stats = search.engine.speed_optimizer.get_stats()
    print(f"Optimizer stats: {optimizer_stats}")

if hasattr(search.engine, 'accuracy_enhancer') and search.engine.accuracy_enhancer:
    enhancer_stats = search.engine.accuracy_enhancer.get_enhancement_stats()
    print(f"Enhancer stats: {enhancer_stats}")
```

## Performance Tips

1. **Always enable optimization**:
```python
search = ls.LoSearch(enable_optimization=True)
```

2. **Batch document operations**:
```python
# Good
search.add_documents(all_documents)

# Avoid
for doc in documents:
    search.add_documents([doc])
```

3. **Use smart search for typos**:
```python
result = search.smart_search("query with typos")
```

4. **Use advanced mode for better context**:
```python
result = search.contextual_search(query, mode='advanced')
```

5. **Warm up cache for common queries**:
```python
optimizer = ls.core.speed_optimizer.SpeedOptimizer()
common_queries = ["AI", "machine learning", "data science"]
optimizer.warmup_cache(common_queries, search_function)
```

## Troubleshooting

### Memory Usage
```python
stats = search.get_performance_stats()
print(f"Cached terms: {stats['cached_terms_count']}")

# Clear cache if needed
if hasattr(search.engine, 'speed_optimizer') and search.engine.speed_optimizer:
    search.engine.speed_optimizer.clear_cache()
```

### Search Quality
```python
# Check query correction
correction = search.fix_query("query")
if correction['needs_correction']:
    corrected_query = correction['corrected_query']
    
# Use advanced contextual search
results = search.contextual_search(query, mode='advanced')
```

### Language Detection
```python
analysis = search.analyze_text("your text")
print(f"Language: {analysis['language']}")

# Normalize text manually
processor = ls.utils.text_processor.TextProcessor()
normalized = processor.normalize_text("text")
```

### Component Integration Issues
```python
# Check if optimization is enabled
engine = ls.core.engine.LoSearchEngine(enable_optimization=True)
print(f"Optimization enabled: {engine.optimization_enabled}")

# Verify component availability
print(f"Speed optimizer: {engine.speed_optimizer is not None}")
print(f"Accuracy enhancer: {engine.accuracy_enhancer is not None}")

# Check document indexing
print(f"Documents indexed: {engine._documents_indexed}")
print(f"Document lookup size: {len(engine._doc_lookup)}")
print(f"IDF scores: {len(engine.idf_scores)}")
```

## API Reference

### Main Classes and Methods

#### LoSearch Class
- `__init__(enable_optimization=True)` - Initialize search engine
- `add_documents(documents)` - Index documents
- `search(query, limit=10)` - Fast search
- `smart_search(query, documents=None, limit=10)` - Smart search with corrections
- `analyze_text(text)` - Text analysis
- `fix_query(query, documents=None)` - Query correction

#### LoSearchEngine Class
- `__init__(enable_optimization=True)` - Initialize advanced engine
- `add_documents(documents)` - Index documents with IDF calculation
- `search(query, limit=10)` - Optimized search
- `smart_search(query, documents=None, limit=10)` - Advanced smart search
- `contextual_search(query, documents=None, limit=10, mode='simple', top_sentences=3)` - Context-aware search
- `contextual_search_with_scores(query, documents=None, limit=10, mode='simple', top_sentences=3)` - Context search with scores
- `fix_query(query, documents=None)` - Query correction
- `analyze_text(text)` - Text analysis
- `get_performance_stats()` - Performance statistics

#### TextProcessor Class
- `__init__()` - Initialize text processor
- `extract_words(text, remove_stop_words=True)` - Extract words
- `normalize_text(text)` - Normalize text
- `extract_terms(text)` - Extract terms
- `extract_phrases(text, max_phrase_length=3)` - Extract phrases
- `get_all_stop_words()` - Get stop words
- `suggest_corrections(query, valid_terms)` - Suggest corrections
- `analyze_text(text)` - Complete text analysis

#### ContextExtractor Class
- `find_best_sentence(query, content, text_processor, mode='simple', idf_scores=None)` - Find best sentence
- `find_top_sentences(query, content, text_processor, top_n=3, mode='simple', idf_scores=None)` - Find top sentences
- `find_top_sentences_with_scores(query, content, text_processor, top_n=3, mode='simple', idf_scores=None)` - Find sentences with scores

#### SpeedOptimizer Class
- `__init__(cache_size=1000)` - Initialize optimizer
- `optimized_search(query, search_func, limit=10)` - Optimized search
- `get_stats()` - Get statistics
- `clear_cache()` - Clear cache
- `warmup_cache(common_queries, search_func)` - Warm up cache

#### AccuracyEnhancer Class
- `__init__()` - Initialize enhancer
- `enhance_search_accuracy(query, results, user_context=None)` - Enhance search accuracy
- `get_enhancement_stats()` - Get enhancement statistics

### Standalone Functions
- `ls.search(query, documents, limit=10)` - Simple search function
- `ls.smart_search(query, documents=None, limit=10)` - Smart search function
- `ls.analyze_text(text)` - Text analysis function

### Configuration Options
- `enable_optimization`: Enable/disable optimization (default: True)
- `cache_size`: Cache size for SpeedOptimizer (default: 1000)
- `limit`: Maximum number of results (default: 10)
- `mode`: Search mode 'simple' or 'advanced' (default: 'simple')
- `top_sentences`: Number of top sentences to extract (default: 3)
- `max_phrase_length`: Maximum phrase length (default: 3)
- `remove_stop_words`: Remove stop words flag (default: True)
