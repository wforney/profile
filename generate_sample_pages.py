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
            'title': 'William Forney - Software Engineer & Developer',
            'description': 'Professional portfolio and profile of William Forney, a software engineer specializing in web development, cloud technologies, and open source contributions.',
            'headings': [
                {'level': 'h1', 'text': 'William Forney'},
                {'level': 'h2', 'text': 'About Me'},
                {'level': 'h2', 'text': 'Skills & Expertise'},
                {'level': 'h3', 'text': 'Programming Languages'},
                {'level': 'h3', 'text': 'Frameworks & Technologies'},
                {'level': 'h2', 'text': 'Professional Experience'},
                {'level': 'h3', 'text': 'Senior Software Engineer'},
                {'level': 'h3', 'text': 'Software Developer'},
                {'level': 'h2', 'text': 'Projects'},
                {'level': 'h3', 'text': 'Open Source Contributions'},
                {'level': 'h2', 'text': 'Education'},
                {'level': 'h2', 'text': 'Contact Information'}
            ],
            'links': [
                {'text': 'GitHub', 'href': 'https://github.com/wforney'},
                {'text': 'LinkedIn', 'href': 'https://linkedin.com/in/wforney'},
                {'text': 'Email', 'href': 'mailto:contact@williamforney.com'}
            ],
            'content': '''William Forney
Software Engineer & Developer

About Me
I am a passionate software engineer with extensive experience in building scalable web applications, cloud infrastructure, and enterprise software solutions. My expertise spans across multiple programming languages and modern development frameworks.

Skills & Expertise

Programming Languages
- Python (Advanced)
- JavaScript/TypeScript (Advanced)
- C# .NET (Proficient)
- Java (Proficient)
- Go (Intermediate)

Frameworks & Technologies
- React, Angular, Vue.js
- Node.js, Express
- Django, Flask
- Docker, Kubernetes
- AWS, Azure, GCP
- PostgreSQL, MongoDB

Professional Experience

Senior Software Engineer
Leading development of cloud-native applications using microservices architecture. Implementing CI/CD pipelines and infrastructure as code. Mentoring junior developers and conducting code reviews.

Software Developer
Developed full-stack web applications using modern JavaScript frameworks. Collaborated with cross-functional teams to deliver high-quality software solutions.

Projects

Open Source Contributions
Active contributor to various open source projects including web frameworks, developer tools, and documentation improvements.

Education
Bachelor's degree in Computer Science with a focus on software engineering and distributed systems.

Contact Information
Feel free to reach out via GitHub, LinkedIn, or email for collaboration opportunities.''',
            'scraped_at': datetime.now().isoformat()
        },
        'LinkedIn Profile': {
            'url': 'https://linkedin.com/in/wforney',
            'title': 'William Forney | LinkedIn',
            'description': 'Software Engineer with 10+ years of experience in full-stack development, cloud architecture, and DevOps. Passionate about building scalable solutions and mentoring developers.',
            'headings': [
                {'level': 'h1', 'text': 'William Forney'},
                {'level': 'h2', 'text': 'Experience'},
                {'level': 'h3', 'text': 'Senior Software Engineer'},
                {'level': 'h3', 'text': 'Software Development Engineer'},
                {'level': 'h2', 'text': 'Education'},
                {'level': 'h2', 'text': 'Skills'},
                {'level': 'h2', 'text': 'Certifications'},
                {'level': 'h2', 'text': 'Recommendations'}
            ],
            'links': [
                {'text': 'GitHub', 'href': 'https://github.com/wforney'},
                {'text': 'Website', 'href': 'https://williamforney.com'}
            ],
            'content': '''William Forney
Software Engineer | Cloud Architect | Open Source Advocate

Headline
Software Engineer with 10+ years of experience in full-stack development, cloud architecture, and DevOps. Passionate about building scalable solutions and mentoring developers.

Experience

Senior Software Engineer
Tech Company | 2020 - Present
• Lead development of microservices-based applications serving millions of users
• Designed and implemented cloud infrastructure on AWS using Terraform
• Established CI/CD best practices reducing deployment time by 60%
• Mentor team of 5 junior developers through code reviews and pair programming

Software Development Engineer
Previous Company | 2017 - 2020
• Built RESTful APIs and SPAs using React and Node.js
• Implemented automated testing achieving 90% code coverage
• Collaborated with product team to deliver features on schedule
• Optimized database queries improving application performance by 40%

Education

Bachelor of Science in Computer Science
University Name | 2013 - 2017

Skills
• Programming: Python, JavaScript, TypeScript, C#, Java
• Frontend: React, Angular, Vue.js
• Backend: Node.js, Django, .NET Core
• Cloud: AWS, Azure, Google Cloud
• DevOps: Docker, Kubernetes, Jenkins, GitLab CI
• Databases: PostgreSQL, MySQL, MongoDB, Redis

Certifications
• AWS Certified Solutions Architect
• Microsoft Azure Developer Associate
• Certified Kubernetes Administrator (CKA)

Recommendations
"William is an exceptional engineer who brings both technical expertise and leadership to every project..." - Former Manager

Connect with me to discuss technology, collaboration opportunities, or mentorship.''',
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
