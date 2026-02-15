# Profile Scraper

A Python-based web scraper to collect profile content from williamforney.com and LinkedIn, and automatically generate Jekyll pages.

## Overview

This tool scrapes content from:
- https://williamforney.com
- https://linkedin.com/in/wforney

The scraped content is saved in multiple formats:
- JSON format for data storage
- Markdown report for review
- **Jekyll pages for website integration**

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Scrape Real Data

Run the scraper to pull content from actual websites:

```bash
python scrape_profile.py
```

**Note:** This requires internet access and the target websites to be accessible. LinkedIn may block automated scraping.

### Option 2: Generate Sample Pages

Use pre-defined sample data to generate pages without web scraping:

```bash
python generate_sample_pages.py
```

This is useful for:
- Testing the page generation without network access
- Demonstrating the functionality
- Local development

## What Gets Generated

Both scripts will create the following files:

### Data Files (Excluded from Git)
- `profile_data.json` - Structured JSON data
- `PROFILE_DATA.md` - Human-readable Markdown report

### Jekyll Pages (Committed to Git)
- `profile-data.md` - Comprehensive profile data page at `/profile-data/`
- `about.md` - Updated about page with profile links
- `_notes/williamforney-com.md` - Note from williamforney.com content
- `_notes/linkedin-profile.md` - Note from LinkedIn profile content

## Workflow

1. **Run scraper or generator**:
   ```bash
   python scrape_profile.py        # Scrape real data
   # OR
   python generate_sample_pages.py # Use sample data
   ```

2. **Review generated pages**:
   - Check `profile-data.md`
   - Review updated `about.md`
   - View notes in `_notes/` directory

3. **Test locally** (optional):
   ```bash
   jekyll serve
   ```
   Visit http://localhost:4000/profile-data/

4. **Commit and deploy**:
   ```bash
   git add profile-data.md about.md index.md _notes/
   git commit -m "Update profile pages"
   git push
   ```

## Output Files

### profile_data.json
Contains structured data including:
- Page titles
- Meta descriptions
- Headings hierarchy
- Links
- Main content text
- Timestamp of scraping

### PROFILE_DATA.md
A formatted Markdown report with:
- Content organized by source
- Heading structure
- Content preview
- Generation timestamp

### Jekyll Pages
Jekyll-compatible markdown files with:
- Proper front matter (layout, title, permalink)
- Formatted content from scraped sources
- Cross-references between pages
- Timestamp and source attribution

## Important Notes

### LinkedIn Scraping
LinkedIn has strict policies against automated scraping. The scraper may:
- Be blocked without authentication
- Require manual login
- Show limited public information

For complete LinkedIn data, consider:
- Using LinkedIn's official API
- Exporting data directly from your LinkedIn profile
- Manual content collection
- Using the `generate_sample_pages.py` script with custom data

### Rate Limiting
To be respectful of web servers:
- The scraper includes appropriate delays
- Uses proper user agent strings
- Follows robots.txt guidelines

### Customization

You can customize the scraped URLs by editing `scrape_profile.py`:

```python
urls = {
    'williamforney.com': 'https://williamforney.com',
    'LinkedIn Profile': 'https://linkedin.com/in/wforney'
}
```

Or create custom sample data in `generate_sample_pages.py`:

```python
def create_sample_data():
    return {
        'Source Name': {
            'url': 'https://example.com',
            'title': 'Page Title',
            # ... more fields
        }
    }
```

## Troubleshooting

If you encounter errors:

1. **Connection Errors**: Check your internet connection and firewall settings
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Permission Errors**: Run the script with appropriate file permissions
4. **LinkedIn Blocking**: This is expected behavior; use `generate_sample_pages.py` instead

## License

See LICENSE file for details.
