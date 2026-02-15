---
layout: page
title: Notes
permalink: /notes/
---

# Notes

Welcome to my notes section! Here I document my learnings, thoughts, and insights on various topics.

## Categories

Browse through my notes organized by topics:

- Development
- Technology
- Best Practices
- Learning Resources

## Latest Notes

{% for note in site.notes %}
- [{{ note.title }}]({{ note.url }})
{% endfor %}

---

*This is a living document that grows over time. Check back regularly for new content!*
