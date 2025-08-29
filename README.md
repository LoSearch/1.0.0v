# LoSearch - Advanced Search Engine Library

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-0.1.2-green.svg)](https://github.com/yourusername/losearch)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A high-performance Python search library with intelligent relevance scoring, advanced indexing capabilities, and multilingual support for Persian and English.

## Features

- **Fast Document Search** - Optimized indexing and retrieval
- **Smart Query Correction** - Automatic typo detection and correction
- **Contextual Search** - Extract relevant sentences with context
- **Multilingual Support** - Persian and English language processing
- **Performance Optimization** - Intelligent caching and speed enhancements
- **Accuracy Enhancement** - Advanced relevance scoring algorithms
- **Text Analysis** - Comprehensive text processing utilities
- **Flexible API** - Simple yet powerful interface

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

# Search with automatic optimization
results = search.search("laptop performance")
for result in results:
    print(f"{result['title']} - Score: {result['score']}")
```

## Core Components

### Main Classes

- **LoSearch** - Primary interface for all search operations
- **LoSearchEngine** - Advanced search engine with optimization
- **TextProcessor** - Text normalization and language processing
- **ContextExtractor** - Intelligent context and sentence extraction
- **SpeedOptimizer** - Performance optimization and caching
- **AccuracyEnhancer** - Result quality improvement

### Search Methods

#### Basic Search
```python
results = search.search("machine learning", limit=10)
```

#### Smart Search with Auto-Correction
```python
result = search.smart_search("machne lerning")  # Automatically corrects typos
```

#### Contextual Search
```python
result = search.contextual_search("AI algorithms", mode='advanced')
```

#### Contextual Search with Scoring
```python
result = search.contextual_search_with_scores("deep learning", top_sentences=3)
```

## Advanced Usage

### Text Analysis
```python
analysis = search.analyze_text("Machine learning and artificial intelligence")
print(f"Language: {analysis['language']}")
print(f"Terms: {analysis['terms']}")
```

### Query Correction
```python
correction = search.fix_query("machne lerning")
print(f"Corrected: {correction['corrected_query']}")
print(f"Confidence: {correction['confidence']}")
```

### Performance Monitoring
```python
stats = search.get_performance_stats()
print(f"Documents indexed: {stats['documents_indexed']}")
print(f"Cache hit rate: {stats['speed_optimizer']['hit_rate']}")
```

## Multilingual Support

LoSearch provides seamless support for both Persian and English with automatic language detection:

```python
# English search
english_results = search.search("machine learning algorithms")

# Persian search  
persian_results = search.search("یادگیری ماشین")

# Mixed language documents
mixed_docs = [
    {"id": "1", "title": "AI Research", "content": "تحقیقات هوش مصنوعی"},
    {"id": "2", "title": "Python Programming", "content": "برنامه نویسی پایتون"}
]
```

## Architecture

```
src/losearch/
├── core/                    # Core search functionality
│   ├── engine.py           # Main LoSearchEngine class
│   ├── search_engine.py    # Base search engine
│   ├── speed_optimizer.py  # Caching and optimization
│   └── accuracy_enhancer.py # Result accuracy improvement
├── utils/                   # Utility modules
│   ├── text_processor.py   # Text processing and normalization
│   └── context_extractor.py # Context and sentence extraction
└── __init__.py             # Library interface
```

## Performance Features

### Speed Optimization
- Intelligent query caching
- Index optimization
- Memory-efficient processing

### Accuracy Enhancement
- Advanced relevance scoring
- Context-aware ranking
- Language-specific processing

## Use Cases

- E-commerce product search
- Document management systems
- Knowledge base applications
- Content discovery platforms
- Research and academic tools
- Multilingual applications

## Documentation

For comprehensive documentation, examples, and advanced usage:

**[Complete Tutorial](LoSearch_Tutorial.md)**

## Performance Tips

1. Enable optimization for better performance:
```python
search = ls.LoSearch(enable_optimization=True)
```

2. Use batch operations for multiple documents:
```python
search.add_documents(all_documents)  # Preferred over individual adds
```

3. Use advanced mode for better contextual results:
```python
result = search.contextual_search(query, mode='advanced')
```

## Version 1.0.0

### What's New
- Complete rewrite with modular architecture
- Multi-language support (Persian/English)
- Smart query correction and auto-completion
- Contextual search with sentence extraction
- Performance optimization with intelligent caching
- Comprehensive text analysis capabilities
- Enhanced accuracy scoring algorithms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue on GitHub for bug reports
- Check the [Complete Tutorial](LoSearch_Tutorial.md) for documentation
- Review examples in the documentation

---

**LoSearch** - Making search intelligent and fast
