
# LocSearch

A high-performance Python search library that provides advanced search capabilities with intelligent relevance scoring. It features dual search engines: a legacy simple text-based search and an advanced inverted index engine with TF-IDF scoring, BM25 ranking, and sophisticated text processing.

## Features

- **Dual Search Engines**: Choose between simple text search or advanced inverted index with TF-IDF
- **Intelligent Scoring**: TF-IDF, BM25 ranking, and sophisticated relevance algorithms
- **High Performance**: Optimized database queries, caching, and bulk operations
- **Easy Integration**: Simple API with both sync and async operation modes
- **Analytics**: Built-in performance monitoring and search statistics
- **Flexible Storage**: SQLite by default, supports any SQLAlchemy-compatible database
- **Advanced Text Processing**: NLTK-powered stemming, stopword removal, and n-gram analysis
- **Smart Caching**: Redis-backed result caching with configurable TTL
- **Thread Safe**: Designed for concurrent operations with proper locking

## Quick Start

### Installation

```bash
pip install locsearch
```

### Basic Usage

```python
from locsearch import LocSearch

# Initialize search engine (uses advanced engine by default)
search = LocSearch(use_advanced_engine=True)

# Add documents
documents = [
    {"id": "1", "title": "Python Programming", "content": "Learn Python programming"},
    {"id": "2", "title": "Machine Learning", "content": "Introduction to ML algorithms"},
]
search.add_products_bulk(documents)

# Search
results = search.search_sync("Python programming")
for result in results:
    print(f"{result['title']} (Score: {result['score']:.2f})")
```

### One-liner Quick Search

```python
from locsearch import quick_search

documents = [
    {"id": "1", "title": "Python Guide", "content": "Python programming tutorial"},
    {"id": "2", "title": "Data Science", "content": "Data analysis with Python"},
]

results = quick_search("Python tutorial", documents, limit=5)
```

## Advanced Usage

### Asynchronous Search

```python
# Start async search
search_id = search.start_search("artificial intelligence")

# Get results later
import time
time.sleep(0.5)  # Simulate other work
async_results = search.get_search_results(search_id)
print(f"Status: {async_results['status']}")
print(f"Results: {len(async_results['results'])}")
```

### Custom Database Configuration

```python
# Use custom database
search = LocSearch(
    database_url="postgresql://user:pass@localhost/searchdb",
    use_advanced_engine=True
)

# Or use SQLite with custom path
search = LocSearch(
    database_url="sqlite:///my_search.db",
    use_advanced_engine=True
)
```

### Performance Monitoring

```python
# Get search statistics
stats = search.get_search_statistics()
print(f"Total searches: {stats['total_searches']}")
print(f"Average time: {stats['average_search_time_ms']:.2f}ms")

# Analyze performance for specific query
perf = search.analyze_performance("test query")
print(f"Processing time: {perf['search_processing_time']:.2f}ms")
```

### Data Export

```python
# Export to JSON
json_data = search.export_data('json')

# Export to CSV
csv_data = search.export_data('csv')
```

## Architecture

### Search Engines

1. **Legacy Engine**: Simple text-based search using basic word matching
2. **Advanced Engine** (Recommended): Sophisticated inverted index with:
   - TF-IDF scoring for relevance ranking
   - BM25 algorithm implementation
   - Advanced text processing with stemming
   - Efficient database indexing

### Text Processing

- **Basic Processor**: Simple word extraction and cleaning
- **Advanced Processor**: NLTK-powered linguistics with:
  - Stemming and lemmatization
  - Stopword removal
  - N-gram analysis
  - TF-IDF vectorization

### Performance Optimizations

- Database indexing on searchable fields
- Redis caching for search results
- Thread-safe operations with reentrant locks
- Bulk insert/update operations
- Query optimization for large datasets

## Requirements

- Python 3.9+
- SQLAlchemy 2.0+
- NLTK 3.9.1+
- scikit-learn 1.3.2+
- Redis 6.1.1+ (optional, for caching)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/locsearch/locsearch.git
cd locsearch

# Install in development mode
pip install -e ".[dev]"

# Run tests
python comprehensive_test.py
```

### Code Quality

```bash
# Format code
python -m black src/

# Lint code
python -m ruff check src/

# Type checking
python -m mypy src/locsearch --ignore-missing-imports
```

### Building and Publishing

```bash
# Build package
python -m build

# Check package
python -m twine check dist/*

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Performance Benchmarks

LocSearch is designed for high performance:

- **Indexing Speed**: 1000+ documents/second
- **Search Speed**: Sub-100ms for most queries
- **Memory Efficient**: Optimized for large document collections
- **Concurrent Safe**: Handles multiple simultaneous searches

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [SQLAlchemy](https://sqlalchemy.org/) for database operations
- Text processing powered by [NLTK](https://nltk.org/)
- Machine learning features using [scikit-learn](https://scikit-learn.org/)
- Caching support via [Redis](https://redis.io/)

## Support

If you encounter any issues or have questions, please:

1. Check the [documentation](README.md)
2. Search existing [issues](https://github.com/LocSearch/0.1.0v/issues)
3. Create a new issue if needed

---

**Made with care by the LocSearch Team**
