"""
Test framework to verify our generated HTML matches the reference monospace-web files.
This implements TDD to ensure exact replication of styling, structure, and functionality.
"""

import os
import sys
import difflib
import re
from pathlib import Path

# Add the parent directory to the path so we can import the build script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build import MonospaceGenerator

class MonospaceReplicationTest:
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.project_dir = self.test_dir.parent
        self.reference_files = {
            'html': self.test_dir / 'reference' / 'index.html',
            'css': self.test_dir / 'reference' / 'src' / 'index.css',
            'reset_css': self.test_dir / 'reference' / 'src' / 'reset.css',
            'js': self.test_dir / 'reference' / 'src' / 'index.js'
        }
        self.generated_files = {
            'html': self.project_dir / 'docs' / 'index.html',
            'css': self.project_dir / 'src' / 'style.css',
            'reset_css': self.project_dir / 'src' / 'reset.css',
            'js': self.project_dir / 'src' / 'index.js'
        }
    
    def read_file(self, filepath):
        """Read a file and return its contents."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def normalize_html(self, html_content):
        """Normalize HTML for comparison by removing whitespace differences."""
        if not html_content:
            return ""
        
        # More aggressive whitespace normalization while preserving structure
        # Remove all whitespace between tags
        html_content = re.sub(r'>\s+<', '><', html_content)
        # Normalize whitespace within text content to single spaces
        html_content = re.sub(r'\s+', ' ', html_content)
        # Remove whitespace around tag content
        html_content = re.sub(r'<([^>]+)>\s+', r'<\1>', html_content)
        html_content = re.sub(r'\s+</', r'</', html_content)
        # Normalize attribute spacing
        html_content = re.sub(r'\s*=\s*', '=', html_content)
        html_content = re.sub(r'\s+(?=[^<]*>)', ' ', html_content)
        html_content = html_content.strip()
        
        return html_content
    
    def normalize_css(self, css_content):
        """Normalize CSS for comparison."""
        if not css_content:
            return ""
        
        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        # Remove extra whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        css_content = re.sub(r';\s*}', '}', css_content)
        css_content = re.sub(r'{\s*', '{', css_content)
        css_content = css_content.strip()
        
        return css_content
    
    def normalize_js(self, js_content):
        """Normalize JavaScript for comparison."""
        if not js_content:
            return ""
        
        # Remove comments
        js_content = re.sub(r'//.*?$', '', js_content, flags=re.MULTILINE)
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        # Remove extra whitespace
        js_content = re.sub(r'\s+', ' ', js_content)
        js_content = js_content.strip()
        
        return js_content
    
    def compare_files(self, reference_path, generated_path, file_type='text'):
        """Compare two files and return differences."""
        reference_content = self.read_file(reference_path)
        generated_content = self.read_file(generated_path)
        
        if reference_content is None:
            return False, f"Reference file not found: {reference_path}"
        
        if generated_content is None:
            return False, f"Generated file not found: {generated_path}"
        
        # Normalize content based on file type
        if file_type == 'html':
            reference_content = self.normalize_html(reference_content)
            generated_content = self.normalize_html(generated_content)
        elif file_type == 'css':
            reference_content = self.normalize_css(reference_content)
            generated_content = self.normalize_css(generated_content)
        elif file_type == 'js':
            reference_content = self.normalize_js(reference_content)
            generated_content = self.normalize_js(generated_content)
        
        if reference_content == generated_content:
            return True, "Files match exactly"
        
        # Generate diff
        diff = list(difflib.unified_diff(
            reference_content.splitlines(keepends=True),
            generated_content.splitlines(keepends=True),
            fromfile=str(reference_path),
            tofile=str(generated_path),
            n=3
        ))
        
        return False, ''.join(diff)
    
    def test_html_structure(self):
        """Test that HTML structure matches reference."""
        print("\n=== Testing HTML Structure ===")
        
        match, diff = self.compare_files(
            self.reference_files['html'],
            self.generated_files['html'],
            'html'
        )
        
        if match:
            print("✓ HTML structure matches reference")
            return True
        else:
            print("✗ HTML structure differs from reference")
            print("Differences:")
            print(diff[:2000])  # Limit output
            if len(diff) > 2000:
                print("... (output truncated)")
            return False
    
    def test_css_styling(self):
        """Test that CSS styling matches reference."""
        print("\n=== Testing CSS Styling ===")
        
        # Test main CSS
        match, diff = self.compare_files(
            self.reference_files['css'],
            self.generated_files['css'],
            'css'
        )
        
        if match:
            print("✓ Main CSS matches reference")
            css_match = True
        else:
            print("✗ Main CSS differs from reference")
            print("Differences:")
            print(diff[:2000])
            css_match = False
        
        # Test reset CSS
        reset_match, reset_diff = self.compare_files(
            self.reference_files['reset_css'],
            self.generated_files['reset_css'],
            'css'
        )
        
        if reset_match:
            print("✓ Reset CSS matches reference")
        else:
            print("✗ Reset CSS differs from reference")
            print("Reset CSS Differences:")
            print(reset_diff[:2000])
            css_match = False
        
        return css_match and reset_match
    
    def test_javascript_functionality(self):
        """Test that JavaScript functionality matches reference."""
        print("\n=== Testing JavaScript Functionality ===")
        
        match, diff = self.compare_files(
            self.reference_files['js'],
            self.generated_files['js'],
            'js'
        )
        
        if match:
            print("✓ JavaScript matches reference")
            return True
        else:
            print("✗ JavaScript differs from reference")
            print("Differences:")
            print(diff[:2000])
            return False
    
    def analyze_reference_structure(self):
        """Analyze the reference files to understand structure."""
        print("\n=== Analyzing Reference Structure ===")
        
        # Analyze HTML structure
        html_content = self.read_file(self.reference_files['html'])
        if html_content:
            print(f"✓ Reference HTML: {len(html_content)} characters")
            
            # Extract key elements
            title_match = re.search(r'<title>(.*?)</title>', html_content)
            if title_match:
                print(f"  Title: {title_match.group(1)}")
            
            # Count major elements
            header_count = len(re.findall(r'<h[1-6]', html_content))
            table_count = len(re.findall(r'<table', html_content))
            form_count = len(re.findall(r'<form', html_content))
            
            print(f"  Headers: {header_count}, Tables: {table_count}, Forms: {form_count}")
        
        # Analyze CSS
        css_content = self.read_file(self.reference_files['css'])
        if css_content:
            print(f"✓ Reference CSS: {len(css_content)} characters")
            
            # Count CSS rules
            rule_count = len(re.findall(r'[^{}]+{[^{}]*}', css_content))
            print(f"  Approximate CSS rules: {rule_count}")
        
        # Analyze JavaScript
        js_content = self.read_file(self.reference_files['js'])
        if js_content:
            print(f"✓ Reference JavaScript: {len(js_content)} characters")
    
    def run_build_and_test(self):
        """Run the build process and test the results."""
        print("=== Running Build Process ===")
        
        try:
            generator = MonospaceGenerator(input_file=str(self.test_dir / 'index.md'))
            generator.build()
            print("✓ Build completed successfully")
        except Exception as e:
            print(f"✗ Build failed: {e}")
            return False
        
        # Run all tests
        html_test = self.test_html_structure()
        css_test = self.test_css_styling()
        js_test = self.test_javascript_functionality()
        
        # Summary
        print("\n=== Test Summary ===")
        print(f"HTML Structure: {'PASS' if html_test else 'FAIL'}")
        print(f"CSS Styling: {'PASS' if css_test else 'FAIL'}")
        print(f"JavaScript: {'PASS' if js_test else 'FAIL'}")
        
        all_passed = html_test and css_test and js_test
        print(f"\nOverall Result: {'ALL TESTS PASS' if all_passed else 'SOME TESTS FAILED'}")
        
        return all_passed
    
    def run_analysis_only(self):
        """Run analysis of reference files without building."""
        self.analyze_reference_structure()

def main():
    """Main test runner."""
    test_runner = MonospaceReplicationTest()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--analyze':
        test_runner.run_analysis_only()
    else:
        success = test_runner.run_build_and_test()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()