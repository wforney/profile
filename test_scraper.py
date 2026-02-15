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
    
    def test_create_jekyll_pages(self):
        """Test creating Jekyll pages from scraped data."""
        import tempfile
        import shutil
        
        test_data = {
            'Test Site': {
                'url': 'https://test.com',
                'title': 'Test Site Title',
                'description': 'Test description',
                'headings': [
                    {'level': 'h1', 'text': 'Main Heading'}
                ],
                'content': 'Test content here',
                'scraped_at': '2026-02-15T00:00:00'
            }
        }
        
        # Create temporary directory for testing
        temp_dir = tempfile.mkdtemp()
        original_dir = os.getcwd()
        
        try:
            os.chdir(temp_dir)
            
            # Create the scraper and generate pages
            self.scraper.create_jekyll_pages(test_data)
            
            # Verify profile-data.md was created
            self.assertTrue(os.path.exists('profile-data.md'))
            with open('profile-data.md', 'r') as f:
                content = f.read()
            self.assertIn('---', content)  # Jekyll front matter
            self.assertIn('layout: page', content)
            self.assertIn('Test Site', content)  # Source name
            self.assertIn('Test description', content)  # Description
            
            # Verify notes were created
            self.assertTrue(os.path.exists('_notes'))
            self.assertTrue(os.path.exists('_notes/test-site.md'))
            with open('_notes/test-site.md', 'r') as f:
                note_content = f.read()
            self.assertIn('---', note_content)  # Jekyll front matter
            self.assertIn('categories: [profile, scraped-content]', note_content)
            self.assertIn('Test Site Title', note_content)  # Title in note
            
        finally:
            os.chdir(original_dir)
            shutil.rmtree(temp_dir)
    
    def test_create_jekyll_pages_with_no_data(self):
        """Test creating Jekyll pages when scraping fails."""
        import tempfile
        import shutil
        
        test_data = {
            'test_site': None
        }
        
        # Create temporary directory for testing
        temp_dir = tempfile.mkdtemp()
        original_dir = os.getcwd()
        
        try:
            os.chdir(temp_dir)
            
            # Create the scraper and generate pages
            self.scraper.create_jekyll_pages(test_data)
            
            # Verify profile-data.md was created even with no data
            self.assertTrue(os.path.exists('profile-data.md'))
            with open('profile-data.md', 'r') as f:
                content = f.read()
            self.assertIn('Content not available', content)
            
        finally:
            os.chdir(original_dir)
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
