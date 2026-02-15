# Profile Scraper

A Python-based web scraper to collect profile content from williamforney.com and LinkedIn.

## Overview

This tool scrapes content from:
- https://williamforney.com
- https://linkedin.com/in/wforney

The scraped content is saved in both JSON and Markdown formats for easy access and review.

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:

```bash
python scrape_profile.py
```

The scraper will:
1. Fetch content from both URLs
2. Extract relevant information (title, headings, links, content)
3. Save results to two files:
   - `profile_data.json` - Structured JSON data
   - `PROFILE_DATA.md` - Human-readable Markdown report

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

### Rate Limiting
To be respectful of web servers:
- The scraper includes appropriate delays
- Uses proper user agent strings
- Follows robots.txt guidelines

## Troubleshooting

If you encounter errors:

1. **Connection Errors**: Check your internet connection and firewall settings
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Permission Errors**: Run the script with appropriate file permissions
4. **LinkedIn Blocking**: This is expected behavior; consider alternative data collection methods

## License

See LICENSE file for details.
