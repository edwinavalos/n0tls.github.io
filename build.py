#!/usr/bin/env python3
"""
Static blog generator for GitHub Pages
Converts markdown posts to HTML using Jinja2 templates
"""

import os
import re
from datetime import datetime
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader
import yaml

# Directories
POSTS_DIR = Path("posts")
TEMPLATES_DIR = Path("templates")
OUTPUT_DIR = Path(".")
TAG_DIR = OUTPUT_DIR / "tag"

# Ensure tag directory exists
TAG_DIR.mkdir(exist_ok=True)


def parse_post(filepath):
    """Parse a markdown post with YAML front matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        raise ValueError(f"No front matter found in {filepath}")

    front_matter = yaml.safe_load(match.group(1))
    markdown_content = match.group(2)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'tables', 'nl2br'])
    html_content = md.convert(markdown_content)

    # Extract metadata
    title = front_matter.get('title', 'Untitled')
    date_str = front_matter.get('date', '')
    tags = front_matter.get('tags', [])
    excerpt = front_matter.get('excerpt', '')

    # Parse date
    if isinstance(date_str, str):
        date = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date = date_str

    # Generate URL from filename
    filename = filepath.stem
    url = f"/{filename}.html"

    return {
        'title': title,
        'date': date,
        'date_str': date.strftime('%Y-%m-%d'),
        'date_formatted': date.strftime('%B %d, %Y'),
        'tags': tags if isinstance(tags, list) else [tags] if tags else [],
        'excerpt': excerpt,
        'content': html_content,
        'url': url,
        'filename': filename,
        'filepath': filepath
    }


def generate_rss(posts, output_file='feed.xml'):
    """Generate RSS feed"""
    rss_items = []

    for post in posts[:10]:  # Latest 10 posts
        item = f"""
    <item>
        <title>{post['title']}</title>
        <link>https://n0tls.com{post['url']}</link>
        <guid>https://n0tls.com{post['url']}</guid>
        <pubDate>{post['date'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <description>{post['excerpt']}</description>
    </item>"""
        rss_items.append(item)

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>n0tls</title>
        <link>https://n0tls.com</link>
        <description>Personal blog by n0tls</description>
        <language>en-us</language>
        <atom:link href="https://n0tls.com/feed.xml" rel="self" type="application/rss+xml"/>
        {''.join(rss_items)}
    </channel>
</rss>"""

    with open(OUTPUT_DIR / output_file, 'w', encoding='utf-8') as f:
        f.write(rss_feed)

    print(f"✓ Generated {output_file}")


def main():
    """Main build process"""
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

    # Get all markdown files
    post_files = sorted(POSTS_DIR.glob("*.md"), reverse=True)

    if not post_files:
        print("No posts found in posts/ directory")
        return

    # Parse all posts
    posts = []
    for post_file in post_files:
        try:
            post = parse_post(post_file)
            posts.append(post)
            print(f"✓ Parsed: {post['title']}")
        except Exception as e:
            print(f"✗ Error parsing {post_file}: {e}")
            continue

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p['date'], reverse=True)

    # Generate individual post pages
    post_template = env.get_template('post.html')
    for post in posts:
        html = post_template.render(
            title=post['title'],
            date=post['date_str'],
            date_formatted=post['date_formatted'],
            tags=post['tags'],
            excerpt=post['excerpt'],
            content=post['content'],
            year=datetime.now().year
        )

        output_file = OUTPUT_DIR / f"{post['filename']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated: {output_file}")

    # Generate index page
    index_template = env.get_template('index.html')
    html = index_template.render(
        posts=posts,
        year=datetime.now().year
    )

    with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated: index.html")

    # Generate tag pages
    tags_dict = {}
    for post in posts:
        for tag in post['tags']:
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(post)

    tag_template = env.get_template('tag.html')
    for tag, tag_posts in tags_dict.items():
        html = tag_template.render(
            tag=tag,
            posts=tag_posts,
            year=datetime.now().year
        )

        output_file = TAG_DIR / f"{tag}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated: tag/{tag}.html")

    # Generate RSS feed
    generate_rss(posts)

    print(f"\n✓ Build complete! Generated {len(posts)} posts, {len(tags_dict)} tag pages, and RSS feed.")


if __name__ == '__main__':
    main()
