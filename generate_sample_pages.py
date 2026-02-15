#!/usr/bin/env python3
"""
Generate sample profile pages using mock scraped data.
This demonstrates the page generation functionality without requiring actual web scraping.
"""

from datetime import datetime
from scrape_profile import ProfileScraper


def create_sample_data():
    """Create sample scraped data for demonstration."""
    return {
        'williamforney.com': {
            'url': 'https://williamforney.com',
            'title': 'William Forney',
            'description': 'Personal blog covering technology, programming, and daily musings.',
            'headings': [
                {'level': 'h1', 'text': 'William Forney'},
                {'level': 'h2', 'text': 'Recent Posts'},
                {'level': 'h2', 'text': 'About'}
            ],
            'links': [
                {'text': 'GitHub', 'href': 'https://github.com/wforney'},
                {'text': 'LinkedIn', 'href': 'https://linkedin.com/in/wforney'}
            ],
            'content': '''William Forney
Personal blog and notes.

About
I live in Mount Vernon, WA, and work on data applications and pipelines at Starbucks, handling cloud services to move data from store registers to backend systems. I enjoy programming, technology, and sharing insights on .NET, web development, and more.

Recent work includes updating shared code NuGet packages for .NET 9, and past projects with Aurelia, ASP.NET Core, and Windows development.

Interests: Software development, cloud computing, open source contributions.''',
            'scraped_at': datetime.now().isoformat()
        },
        'LinkedIn Profile': {
            'url': 'https://linkedin.com/in/wforney',
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
- Programming, cloud technologies, data processing.''',
            'scraped_at': datetime.now().isoformat()
        }
    }


def main():
    """Generate sample Jekyll pages using mock data."""
    print("="*60)
    print("Generating Sample Profile Pages")
    print("="*60)
    print()
    
    # Create sample data
    print("Creating sample profile data...")
    sample_data = create_sample_data()
    
    # Initialize scraper
    scraper = ProfileScraper()
    
    # Save sample results
    print("\nSaving sample data...")
    scraper.save_results(sample_data)
    scraper.create_markdown_report(sample_data)
    
    # Create Jekyll pages
    print("\nCreating Jekyll pages...")
    scraper.create_jekyll_pages(sample_data)
    
    print("\n" + "="*60)
    print("✓ Sample pages generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  - profile_data.json (Sample JSON data)")
    print("  - PROFILE_DATA.md (Sample report)")
    print("  - profile-data.md (Jekyll profile page)")
    print("  - about.md (Updated about page)")
    print("  - _notes/williamforney-com.md (Profile note)")
    print("  - _notes/linkedin-profile.md (LinkedIn note)")
    print()
    print("You can now:")
    print("  1. Run 'jekyll serve' to view the pages locally")
    print("  2. Commit and push to update GitHub Pages")
    print("  3. Run 'python scrape_profile.py' to scrape real data")


if __name__ == '__main__':
    main()