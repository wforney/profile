# Profile

My personal profile and public notes repository, hosted with GitHub Pages.

## About

This repository contains my personal profile page and public notes. It uses Markdown for content and Jekyll for static site generation.

## Structure

- `index.md` - Main landing page
- `about.md` - About me page (auto-updated from scraped content)
- `profile-data.md` - Aggregated profile data page
- `notes.md` - Notes index page
- `_notes/` - Collection of note articles (includes scraped profile content)
- `_config.yml` - Jekyll configuration

## Web Scraper

This repository includes a Python web scraper that automatically generates Jekyll pages from profile content scraped from:
- https://williamforney.com
- https://linkedin.com/in/wforney

### Quick Start with Scraper

```bash
# Install dependencies
pip install -r requirements.txt

# Option 1: Scrape real data (requires internet access)
python scrape_profile.py

# Option 2: Generate sample pages (works offline)
python generate_sample_pages.py
```

The scraper automatically creates and updates:
- `profile-data.md` - Comprehensive profile page
- `about.md` - About page with profile links
- `_notes/williamforney-com.md` - Profile content note
- `_notes/linkedin-profile.md` - LinkedIn content note

See [SCRAPER_README.md](SCRAPER_README.md) for detailed instructions and [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for examples.

## Local Development

To run this site locally:

```bash
# Install Jekyll (requires Ruby)
gem install bundler jekyll

# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

## GitHub Pages

This site is designed to be hosted on GitHub Pages. To enable:

1. Go to repository Settings
2. Navigate to Pages section
3. Select the branch (e.g., `main`) as the source
4. Save

The site will be available at `https://wforney.github.io/profile/`

## Updating Profile Content

1. Run the scraper to pull latest content:
   ```bash
   python scrape_profile.py
   ```

2. Review the generated pages

3. Commit and push:
   ```bash
   git add profile-data.md about.md _notes/
   git commit -m "Update profile content"
   git push
   ```

## Content

All content is written in Markdown format, making it easy to read, write, and maintain.

## License

See [LICENSE](LICENSE) file for details.
