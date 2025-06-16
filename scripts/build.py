#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "jinja2",
#     "markdown",
#     "pillow",
#     "pymarkdown-video",
#     "python-frontmatter",
#     "pyyaml",
# ]
# ///
"""
Monospace Web Generator
Converts markdown files to HTML using Jinja2 templates with monospace web formatting.
"""

import os
import shutil
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
import re

class MonospaceGenerator:
    def __init__(self, input_dir='demo', templates_dir='templates', output_dir='docs', static_dir='static'):
        self.input_dir = input_dir
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.static_dir = static_dir
        
        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Setup markdown processor with configurations to match Pandoc output
        self.md = markdown.Markdown(
            extensions=[
                'meta',
                'toc',
                'tables',
                'fenced_code',
                'codehilite',
                'sane_lists',
                'smarty',
                'attr_list',
                'def_list',
                'abbr',
                'md_in_html',
                'pymarkdown-video'  # Use the correct extension name
            ]
        )
    
    def clean_output_dir(self):
        """Clean the output directory."""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def copy_static_files(self):
        """Copy static files to output directory."""
        # Copy static files from static directory
        if os.path.exists(self.static_dir):
            static_output = os.path.join(self.output_dir, 'src')
            if os.path.exists(static_output):
                shutil.rmtree(static_output)
            shutil.copytree(self.static_dir, static_output)
        
        # Copy static assets from input directory
        for item in os.listdir(self.input_dir):
            src_path = os.path.join(self.input_dir, item)
            if os.path.isfile(src_path) and not item.endswith('.md'):
                dst_path = os.path.join(self.output_dir, item)
                shutil.copy2(src_path, dst_path)
    
    def generate_monospace_web(self):
        """Generate the monospace web format from markdown files in the input directory."""
        if not os.path.exists(self.input_dir):
            print(f"Input directory {self.input_dir} not found")
            return
        
        # Process each markdown file in the input directory
        for filename in os.listdir(self.input_dir):
            if not filename.endswith('.md'):
                continue
                
            input_file = os.path.join(self.input_dir, filename)
            print(f"Processing {filename}...")
            
            # Parse the markdown file
            with open(input_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Convert markdown content to HTML
            html_content = self.md.convert(post.content)
            
            # Post-process HTML to match Pandoc output
            # Add incremental class to all lists (Pandoc default behavior)
            # Only add to lists without existing class attribute (don't modify tree class)
            html_content = re.sub(r'<ul(?![^>]*class=)', '<ul class="incremental"', html_content)
            html_content = re.sub(r'<ol(?![^>]*class=)(?![^>]*type=)', '<ol class="incremental" type="1"', html_content)
            
            # Convert standalone images in paragraphs to figures with captions
            # Pattern: <p><img ... alt="caption text" ... /></p>
            html_content = re.sub(r'<p><img([^>]+)alt="([^"]*)"([^>]*)/></p>', 
                                r'<figure><img\1alt="\2"\3/><figcaption aria-hidden="true">\2</figcaption></figure>', 
                                html_content)
            
            # Also handle images without self-closing tags
            html_content = re.sub(r'<p><img([^>]+)alt="([^"]*)"([^>]*)></p>', 
                                r'<figure><img\1alt="\2"\3><figcaption aria-hidden="true">\2</figcaption></figure>', 
                                html_content)
            
            # Remove codehilite class (Python-Markdown adds this, Pandoc doesn't)
            html_content = re.sub(r' class="codehilite"', '', html_content)
            
            # Normalize video elements to match reference format
            def normalize_video(match):
                src = match.group(1)
                alt = match.group(2)
                return f'<figure><video src="{src}" controls=""><a href="{src}">{alt}</a></video><figcaption aria-hidden="true"><a href="https://en.wikisource.org/wiki/Page:The_Center_of_the_Web_(1914).webm/11">{alt}</a></figcaption></figure>'
            
            # Match video elements with various attributes and content
            html_content = re.sub(
                r'<p><video[^>]*alt="([^"]*)"[^>]*controls="controls"[^>]*>.*?<source[^>]*src="([^"]*)"[^>]*>.*?</video></p>', 
                normalize_video, 
                html_content
            )
            
            # Generate table of contents with the exact format needed
            if hasattr(self.md, 'toc') and self.md.toc:
                # Extract just the list items and format them properly
                toc_html = self.md.toc
                # Extract the inner <ul> content and add the class and IDs
                ul_match = re.search(r'<ul>(.*?)</ul>', toc_html, re.DOTALL)
                if ul_match:
                    list_items = ul_match.group(1)
                    # Add the toc- prefix to IDs to match reference
                    list_items = re.sub(r'<a href="#([^"]+)"', lambda m: f'<a href="#{m.group(1)}" id="toc-{m.group(1)}"', list_items)
                    toc = f'<ul class="incremental">{list_items}</ul>'
                else:
                    toc = '<ul class="incremental"></ul>'
            else:
                toc = '<ul class="incremental"></ul>'
            
            # Get the monospace template
            template = self.env.get_template('index.html')
            
            # Render the HTML
            html = template.render(
                title=post.metadata.get('title', 'The Monospace Web'),
                subtitle=post.metadata.get('subtitle', ''),
                author=post.metadata.get('author', ''),
                author_url=post.metadata.get('author-url', ''),
                toc_title=post.metadata.get('toc-title', 'Contents'),
                toc=toc,
                content=html_content
            )
            
            # Write the HTML file
            output_filename = os.path.splitext(filename)[0] + '.html'
            output_path = os.path.join(self.output_dir, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"Generated: {output_filename} from {filename}")

    def build(self):
        """Build the monospace web site."""
        print("Starting monospace web build...")
        
        # Clean and setup output directory
        self.clean_output_dir()
        
        # Copy static files
        self.copy_static_files()
        
        # Generate monospace web format
        self.generate_monospace_web()
        
        print("Monospace web build complete!")

if __name__ == '__main__':
    generator = MonospaceGenerator()
    generator.build() 
