
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import losearch as ls


class TestLoSearchBasic(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.search = ls.LoSearch(enable_optimization=True)
        self.test_documents = [
            {"id": "1", "title": "Machine Learning", "content": "Introduction to machine learning algorithms"},
            {"id": "2", "title": "Python Programming", "content": "Learn Python programming language"},
            {"id": "3", "title": "Data Science", "content": "Data analysis and visualization techniques"}
        ]
    
    def test_add_documents(self):
        """Test adding documents to the search index."""
        result = self.search.add_documents(self.test_documents)
        self.assertIn('indexed_documents', result)
        self.assertEqual(result['indexed_documents'], 3)
    
    def test_basic_search(self):
        """Test basic search functionality."""
        self.search.add_documents(self.test_documents)
        results = self.search.search("machine learning")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_text_analysis(self):
        """Test text analysis functionality."""
        analysis = self.search.analyze_text("Machine learning is fascinating")
        self.assertIn('language', analysis)
        self.assertIn('terms', analysis)
        self.assertIn('word_count', analysis)


if __name__ == '__main__':
    unittest.main()
