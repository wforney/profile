#!/usr/bin/env python3
"""
Simple tests for the profile scraper.
Tests basic functionality without making actual network requests.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import the scraper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrape_profile import ProfileScraper


class TestProfileScraper(unittest.TestCase):
    """Test cases for ProfileScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = ProfileScraper()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertIsNotNone(self.scraper.session)
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    @patch('scrape_profile.requests.Session.get')
    def test_scrape_website_success(self, mock_get):
        """Test successful website scraping."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'''
            <html>
                <head>
                    <title>Test Page</title>
                    <meta name="description" content="Test description">
                </head>
                <body>
                    <h1>Test Heading</h1>
                    <p>Test content</p>
                    <a href="/link">Test Link</a>
                </body>
            </html>
        '''
        mock_get.return_value = mock_response
        
        result = self.scraper.scrape_website('https://example.com')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['title'], 'Test Page')
        self.assertEqual(result['description'], 'Test description')
        self.assertGreater(len(result['headings']), 0)
        self.assertGreater(len(result['links']), 0)
    
    @patch('scrape_profile.requests.Session.get')
    def test_scrape_website_failure(self, mock_get):
        """Test handling of scraping failure."""
        mock_get.side_effect = Exception('Network error')
        
        result = self.scraper.scrape_website('https://example.com')
        
        self.assertIsNone(result)
    
    def test_save_results(self):
        """Test saving results to JSON file."""
        import tempfile
        import json
        
        test_data = {
            'test_site': {
                'url': 'https://test.com',
                'title': 'Test',
                'content': 'Test content'
            }
        }
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            self.scraper.save_results(test_data, temp_file)
            
            # Verify file was created and contains correct data
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(saved_data, test_data)
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_create_markdown_report(self):
        """Test creating markdown report."""
        import tempfile
        
        test_data = {
            'test_site': {
                'url': 'https://test.com',
                'title': 'Test Site',
                'description': 'Test description',
                'headings': [
                    {'level': 'h1', 'text': 'Main Heading'}
                ],
                'content': 'Test content here'
            }
        }
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            temp_file = f.name
        
        try:
            self.scraper.create_markdown_report(test_data, temp_file)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify content
            with open(temp_file, 'r') as f:
                content = f.read()
            
            self.assertIn('test_site', content)
            self.assertIn('https://test.com', content)
            self.assertIn('Test Site', content)
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == '__main__':
    unittest.main()
