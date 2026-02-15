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
    
    def scrape_linkedin_manual(self, manual_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Use manually provided LinkedIn data instead of scraping.
        """
        if manual_data:
            manual_data['url'] = 'https://linkedin.com/in/wforney'
            manual_data['scraped_at'] = datetime.now().isoformat()
            return manual_data
        return None
    
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
    
    def create_jekyll_pages(self, results: Dict[str, Any]):
        """
        Create Jekyll-compatible markdown pages from scraped data.
        
        Args:
            results: Dictionary containing scraped data
        """
        try:
            # Create a comprehensive profile data page
            self._create_profile_data_page(results)
            
            # Update the about page with scraped content
            self._update_about_page(results)
            
            # Create individual notes from scraped profile sources
            self._create_profile_notes(results)
            
            print("✓ Jekyll pages created successfully")
        except Exception as e:
            print(f"Error creating Jekyll pages: {e}")
    
    def _create_profile_data_page(self, results: Dict[str, Any]):
        """Create a comprehensive profile data page."""
        output_file = 'profile-data.md'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Jekyll front matter
            f.write("---\n")
            f.write("layout: page\n")
            f.write("title: Profile Data\n")
            f.write("permalink: /profile-data/\n")
            f.write("---\n\n")
            
            f.write("# Profile Data\n\n")
            f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("This page contains aggregated profile information from various sources.\n\n")
            
            for source_name, data in results.items():
                if data:
                    f.write(f"## {source_name}\n\n")
                    
                    if data.get('description'):
                        f.write(f"{data['description']}\n\n")
                    
                    f.write(f"**Source:** [{data.get('url', 'N/A')}]({data.get('url', '#')})\n\n")
                    
                    if data.get('content'):
                        f.write("### Content\n\n")
                        # Split content into paragraphs for better formatting
                        content_lines = data['content'].split('\n')
                        for line in content_lines[:50]:  # Limit lines
                            if line.strip():
                                f.write(f"{line}\n\n")
                        if len(content_lines) > 50:
                            f.write("*[Content truncated for brevity]*\n\n")
                else:
                    f.write(f"## {source_name}\n\n")
                    f.write("*Content not available*\n\n")
        
        print(f"  - Created {output_file}")
    
    def _update_about_page(self, results: Dict[str, Any]):
        """Update the about page with scraped profile information."""
        output_file = 'about.md'
        
        # Check if we have any successful scrapes
        has_data = any(data is not None for data in results.values())
        
        if not has_data:
            print(f"  - Skipped updating {output_file} (no scraped data available)")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Jekyll front matter
            f.write("---\n")
            f.write("layout: page\n")
            f.write("title: About\n")
            f.write("permalink: /about/\n")
            f.write("---\n\n")
            
            f.write("# About Me\n\n")
            
            # Add content from scraped sources
            for source_name, data in results.items():
                if data and data.get('description'):
                    f.write(f"{data['description']}\n\n")
                    break  # Use first available description
            
            f.write("## Profile Information\n\n")
            f.write("This page aggregates information from my various online profiles:\n\n")
            
            for source_name, data in results.items():
                if data:
                    f.write(f"- **{source_name}**: [{data.get('url', 'N/A')}]({data.get('url', '#')})\n")
            
            f.write("\n")
            f.write("For detailed profile data, visit the [Profile Data](/profile-data/) page.\n\n")
            
            f.write("## Contact\n\n")
            f.write("Feel free to reach out through any of the profiles listed above.\n")
        
        print(f"  - Updated {output_file}")
    
    def _create_profile_notes(self, results: Dict[str, Any]):
        """Create individual notes from scraped profile sources."""
        notes_dir = '_notes'
        
        # Create notes directory if it doesn't exist
        os.makedirs(notes_dir, exist_ok=True)
        
        for source_name, data in results.items():
            if data:
                # Create a filename from source name
                filename = source_name.lower().replace(' ', '-').replace('.', '-')
                output_file = os.path.join(notes_dir, f'{filename}.md')
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    # Jekyll front matter
                    f.write("---\n")
                    f.write(f"title: {data.get('title', source_name)}\n")
                    f.write(f"date: {datetime.now().strftime('%Y-%m-%d')}\n")
                    f.write(f"categories: [profile, scraped-content]\n")
                    f.write("---\n\n")
                    
                    f.write(f"# {data.get('title', source_name)}\n\n")
                    
                    if data.get('description'):
                        f.write(f"{data['description']}\n\n")
                    
                    f.write(f"**Source:** [{data.get('url')}]({data.get('url')})\n\n")
                    f.write(f"*Scraped on: {data.get('scraped_at', 'N/A')}*\n\n")
                    
                    if data.get('content'):
                        f.write("## Content\n\n")
                        # Format content with proper line breaks
                        content_lines = data['content'].split('\n')
                        for line in content_lines[:100]:
                            if line.strip():
                                f.write(f"{line}\n\n")
                
                print(f"  - Created {output_file}")


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
        if name == 'LinkedIn Profile':
            data = scraper.scrape_linkedin(url)
            if not data:
                # Manual LinkedIn data
                manual_linkedin = {
                    'title': 'William Forney | LinkedIn',
                    'description': 'Professional with experience in data applications and cloud services.',
                    'headings': [
                        {'level': 'h1', 'text': 'William Forney'},
                        {'level': 'h2', 'text': 'Experience'},
                        {'level': 'h2', 'text': 'Skills'}
                    ],
                    'links': [
                        {'text': 'Website', 'href': 'https://williamforney.com'}
                    ],
                    'content': '''William Forney
Professional profile.

Experience
- Data applications and pipelines at Starbucks, focusing on cloud services and backend data flow.

Skills
- Programming, cloud technologies, data processing.'''
                }
                data = scraper.scrape_linkedin_manual(manual_linkedin)
        else:
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
    
    # Create Jekyll pages
    print(f"\n{'='*60}")
    print("Creating Jekyll pages...")
    print(f"{'='*60}")
    scraper.create_jekyll_pages(results)
    
    print("\n✓ Scraping complete!")
    print("\nOutput files:")
    print("  - profile_data.json (JSON format)")
    print("  - PROFILE_DATA.md (Markdown format)")
    print("  - profile-data.md (Jekyll page)")
    print("  - about.md (Updated Jekyll page)")
    print("  - _notes/*.md (Jekyll notes)")


if __name__ == '__main__':
    main()