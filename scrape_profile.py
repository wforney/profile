#!/usr/bin/env python3
"""
Web scraper for William Forney's profile content.
Scrapes content from williamforney.com and LinkedIn profile.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class ProfileScraper:
    """Scraper for William Forney's profile content."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_website(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape content from a given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing scraped content or None if failed
        """
        try:
            print(f"Scraping {url}...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'No title'
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '').strip() if meta_desc else ''
            
            # Extract main content
            # Try to find main content areas
            main_content = None
            for tag in ['main', 'article', 'div[role="main"]', '.content', '#content']:
                main_content = soup.select_one(tag)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.find('body')
            
            content_text = main_content.get_text(separator='\n', strip=True) if main_content else ''
            
            # Extract all headings
            headings = []
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                headings.append({
                    'level': heading.name,
                    'text': heading.get_text().strip()
                })
            
            # Extract all links
            links = []
            for link in soup.find_all('a', href=True):
                links.append({
                    'text': link.get_text().strip(),
                    'href': link['href']
                })
            
            return {
                'url': url,
                'title': title_text,
                'description': description,
                'headings': headings,
                'links': links,
                'content': content_text[:5000],  # Limit content length
                'scraped_at': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None
    
    def scrape_linkedin(self, profile_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape LinkedIn profile.
        
        Note: LinkedIn has strict scraping policies and may block automated access.
        This method attempts basic scraping but may not work without authentication.
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Dictionary containing scraped content or None if failed
        """
        print(f"Note: LinkedIn may block automated scraping. Attempting to fetch {profile_url}...")
        return self.scrape_website(profile_url)
    
    def save_results(self, results: Dict[str, Any], output_file: str = 'profile_data.json'):
        """
        Save scraped results to a JSON file.
        
        Args:
            results: Dictionary containing scraped data
            output_file: Output filename
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def create_markdown_report(self, results: Dict[str, Any], output_file: str = 'PROFILE_DATA.md'):
        """
        Create a markdown report from scraped data.
        
        Args:
            results: Dictionary containing scraped data
            output_file: Output markdown filename
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# William Forney - Profile Data\n\n")
                f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                for source_name, data in results.items():
                    if data:
                        f.write(f"## {source_name}\n\n")
                        f.write(f"**URL:** {data.get('url', 'N/A')}\n\n")
                        f.write(f"**Title:** {data.get('title', 'N/A')}\n\n")
                        
                        if data.get('description'):
                            f.write(f"**Description:** {data['description']}\n\n")
                        
                        if data.get('headings'):
                            f.write("### Headings\n\n")
                            for heading in data['headings'][:20]:  # Limit to first 20 headings
                                f.write(f"- **{heading['level']}:** {heading['text']}\n")
                            f.write("\n")
                        
                        if data.get('content'):
                            f.write("### Content Preview\n\n")
                            f.write("```\n")
                            f.write(data['content'][:2000])  # Limit content preview
                            if len(data['content']) > 2000:
                                f.write("\n... (content truncated)")
                            f.write("\n```\n\n")
                    else:
                        f.write(f"## {source_name}\n\n")
                        f.write("*Failed to scrape content*\n\n")
                
            print(f"Markdown report saved to {output_file}")
        except Exception as e:
            print(f"Error creating markdown report: {e}")


def main():
    """Main function to run the scraper."""
    scraper = ProfileScraper()
    
    # URLs to scrape
    urls = {
        'williamforney.com': 'https://williamforney.com',
        'LinkedIn Profile': 'https://linkedin.com/in/wforney'
    }
    
    results = {}
    
    # Scrape each URL
    for name, url in urls.items():
        print(f"\n{'='*60}")
        print(f"Scraping: {name}")
        print(f"{'='*60}")
        data = scraper.scrape_website(url)
        results[name] = data
        if data:
            print(f"✓ Successfully scraped {name}")
        else:
            print(f"✗ Failed to scrape {name}")
    
    # Save results
    print(f"\n{'='*60}")
    print("Saving results...")
    print(f"{'='*60}")
    scraper.save_results(results)
    scraper.create_markdown_report(results)
    
    print("\n✓ Scraping complete!")
    print("\nOutput files:")
    print("  - profile_data.json (JSON format)")
    print("  - PROFILE_DATA.md (Markdown format)")


if __name__ == '__main__':
    main()
