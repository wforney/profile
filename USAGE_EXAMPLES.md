# Example Usage and Expected Output

## Running the Scraper

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scrape_profile.py
```

## Example Output (when websites are accessible)

### Console Output
```
============================================================
Scraping: williamforney.com
============================================================
Scraping https://williamforney.com...
✓ Successfully scraped williamforney.com

============================================================
Scraping: LinkedIn Profile
============================================================
Note: LinkedIn may block automated scraping. Attempting to fetch https://linkedin.com/in/wforney...
Scraping https://linkedin.com/in/wforney...
✓ Successfully scraped LinkedIn Profile

============================================================
Saving results...
============================================================
Results saved to profile_data.json
Markdown report saved to PROFILE_DATA.md

✓ Scraping complete!

Output files:
  - profile_data.json (JSON format)
  - PROFILE_DATA.md (Markdown format)
```

### Expected JSON Structure (profile_data.json)
```json
{
  "williamforney.com": {
    "url": "https://williamforney.com",
    "title": "William Forney - Software Engineer",
    "description": "Portfolio and professional profile",
    "headings": [
      {
        "level": "h1",
        "text": "William Forney"
      },
      {
        "level": "h2",
        "text": "About Me"
      }
    ],
    "links": [
      {
        "text": "GitHub",
        "href": "https://github.com/wforney"
      }
    ],
    "content": "Main page content...",
    "scraped_at": "2026-02-15T01:20:00.000000"
  },
  "LinkedIn Profile": {
    "url": "https://linkedin.com/in/wforney",
    "title": "William Forney - LinkedIn",
    "description": "Professional profile on LinkedIn",
    "headings": [...],
    "links": [...],
    "content": "Profile content...",
    "scraped_at": "2026-02-15T01:20:05.000000"
  }
}
```

### Expected Markdown Report (PROFILE_DATA.md)
```markdown
# William Forney - Profile Data

*Generated on 2026-02-15 01:20:10*

## williamforney.com

**URL:** https://williamforney.com

**Title:** William Forney - Software Engineer

**Description:** Portfolio and professional profile

### Headings

- **h1:** William Forney
- **h2:** About Me
- **h2:** Projects
- **h2:** Contact

### Content Preview

\```
William Forney
Software Engineer

About Me
I am a passionate software engineer...
\```

## LinkedIn Profile

**URL:** https://linkedin.com/in/wforney

**Title:** William Forney - LinkedIn

...
```

## Alternative Data Collection Methods

Since LinkedIn restricts automated scraping, consider these alternatives:

### 1. LinkedIn Official API
- Register for API access at https://developer.linkedin.com/
- Use OAuth 2.0 authentication
- Access structured profile data

### 2. Manual Export
1. Log in to LinkedIn
2. Go to Settings & Privacy > Data Privacy > Get a copy of your data
3. Select "Want something in particular?" > Select data
4. Download your profile information

### 3. Public Profile URL
- LinkedIn public profiles have limited but accessible information
- Use the scraper with the public profile URL
- Note: May still encounter rate limiting

## Troubleshooting

### Network Issues
If you encounter DNS resolution errors:
- Check your internet connection
- Verify the URLs are accessible in a web browser
- Check firewall and proxy settings

### Authentication Required
For LinkedIn:
- Consider using browser automation tools (Selenium) with login
- Use LinkedIn's official API with proper credentials
- Export data manually from your profile

### Rate Limiting
If you see 429 errors:
- Add delays between requests
- Respect the website's robots.txt
- Use the API instead of scraping
