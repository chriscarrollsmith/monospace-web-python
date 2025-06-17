"""
Test framework to verify our generated HTML matches the reference monospace-web files.
This implements TDD to ensure exact replication of styling, structure, and functionality.
"""

import os
import sys
import difflib
import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.element import Tag

# Add the parent directory to the path so we can import the build script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build import MonospaceGenerator

class MonospaceReplicationTest:
    def __init__(self):
        """Initialize test paths and directories."""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(self.test_dir)
        self.reference_dir = os.path.join(self.test_dir, 'reference')
        self.generated_dir = os.path.join(self.test_dir, 'generated')
        self.input_dir = os.path.join(self.test_dir, 'input')
        
        # Define file paths
        self.reference_files = {
            'html': os.path.join(self.reference_dir, 'index.html'),
            'index_css': os.path.join(self.reference_dir, 'src', 'index.css'),
            'reset_css': os.path.join(self.reference_dir, 'src', 'reset.css'),
            'js': os.path.join(self.reference_dir, 'src', 'index.js')
        }
        self.generated_files = {
            'html': os.path.join(self.generated_dir, 'index.html'),
            'index_css': os.path.join(self.generated_dir, 'src', 'index.css'),
            'reset_css': os.path.join(self.generated_dir, 'src', 'reset.css'),
            'js': os.path.join(self.generated_dir, 'src', 'index.js')
        }
        self.input_files = {
            'markdown': os.path.join(self.input_dir, 'index.md'),
            'castle': os.path.join(self.input_dir, 'castle.jpg')
        }
        
        # Create directories if they don't exist
        os.makedirs(self.reference_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
        os.makedirs(self.input_dir, exist_ok=True)
    
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
        
        # Split into lines and normalize each line
        ref_lines = [line.strip() for line in reference_content.splitlines()]
        gen_lines = [line.strip() for line in generated_content.splitlines()]
        
        # Remove empty lines
        ref_lines = [line for line in ref_lines if line]
        gen_lines = [line for line in gen_lines if line]
        
        # Generate diff
        diff = list(difflib.unified_diff(
            ref_lines,
            gen_lines,
            fromfile=str(reference_path),
            tofile=str(generated_path),
            n=3,
            lineterm=''  # Don't add newlines since we're already working with lines
        ))
        
        return False, '\n'.join(diff)
    
    def prettify_html(self, html_content):
        """Prettify HTML content using BeautifulSoup."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.prettify()
    
    def extract_section(self, html, section_name):
        """Extract a section of HTML between h2 tags."""
        soup = BeautifulSoup(html, 'html.parser')
        section = soup.find('h2', id=section_name)
        if not section:
            return ""
        
        # Get all elements until the next h2
        elements = []
        current = section.next_sibling
        while current and not (isinstance(current, Tag) and current.name == 'h2'):
            elements.append(str(current))
            current = current.next_sibling
        
        return ''.join(elements)
    
    def test_html_structure(self):
        """Test that the generated HTML structure matches the reference."""
        print("\n=== Testing HTML Structure ===")
        
        # Read both files
        with open(self.reference_files['html'], 'r', encoding='utf-8') as f:
            reference_content = f.read()
        with open(self.generated_files['html'], 'r', encoding='utf-8') as f:
            generated_content = f.read()
        
        # Prettify both contents
        reference_content = self.prettify_html(reference_content)
        generated_content = self.prettify_html(generated_content)
        
        # Compare specific sections
        sections_to_check = ['media', 'tables', 'lists', 'forms']
        all_diffs = []
        
        for section in sections_to_check:
            ref_section = self.extract_section(reference_content, section)
            gen_section = self.extract_section(generated_content, section)
            
            if ref_section != gen_section:
                diff = list(difflib.unified_diff(
                    ref_section.splitlines(),
                    gen_section.splitlines(),
                    fromfile=f'reference/{section}',
                    tofile=f'generated/{section}',
                    lineterm=''
                ))
                if diff:
                    all_diffs.append(f"\nDifferences in {section} section:")
                    all_diffs.extend(diff)
        
        if all_diffs:
            print("✗ HTML structure differs from reference")
            print("Differences:")
            print('\n'.join(all_diffs))
            return False
        else:
            print("✓ HTML structure matches reference")
            return True
    
    def test_css_styling(self):
        """Test that CSS styling matches reference."""
        print("\n=== Testing CSS Styling ===")
        
        # Test index CSS
        index_match, index_diff = self.compare_files(
            self.reference_files['index_css'],
            self.generated_files['index_css'],
            'css'
        )
        
        if index_match:
            print("✓ Index CSS matches reference")
            index_css_match = True
        else:
            print("✗ Index CSS differs from reference")
            print("Differences:")
            print(index_diff[:2000])
            index_css_match = False
        
        # Test reset CSS
        reset_match, reset_diff = self.compare_files(
            self.reference_files['reset_css'],
            self.generated_files['reset_css'],
            'css'
        )
        
        if reset_match:
            print("✓ Reset CSS matches reference")
            reset_css_match = True
        else:
            print("✗ Reset CSS differs from reference")
            print("Differences:")
            print(reset_diff[:2000])
            reset_css_match = False
        
        return index_css_match and reset_css_match
    
    def test_static_assets(self):
        """Test that static assets are properly copied."""
        print("\n=== Testing Static Assets ===")
        
        # Check if castle.jpg exists in the output directory
        castle_path = os.path.join(self.generated_dir, 'castle.jpg')
        if os.path.exists(castle_path):
            print("✓ castle.jpg found in output directory")
            return True
        else:
            print("✗ castle.jpg not found in output directory")
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
        css_content = self.read_file(self.reference_files['index_css'])
        if css_content:
            print(f"✓ Reference Index CSS: {len(css_content)} characters")
            
            # Count CSS rules
            rule_count = len(re.findall(r'[^{}]+{[^{}]*}', css_content))
            print(f"  Approximate CSS rules: {rule_count}")
        
        # Analyze JavaScript
        js_content = self.read_file(self.reference_files['js'])
        if js_content:
            print(f"✓ Reference JavaScript: {len(js_content)} characters")
    
    def cleanup_generated(self):
        """Clean up the generated directory before running tests."""
        if os.path.exists(self.generated_dir):
            try:
                shutil.rmtree(self.generated_dir)
            except PermissionError as e:
                print(f"Warning: Could not fully clean generated directory: {e}")
                # Try to remove individual files if directory removal fails
                for root, dirs, files in os.walk(self.generated_dir):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                        except PermissionError:
                            pass
            except Exception as e:
                print(f"Warning: Error during cleanup: {e}")
        os.makedirs(self.generated_dir, exist_ok=True)
    
    def setup_test_assets(self):
        """Set up test assets by copying castle.jpg from demo to input directory."""
        demo_castle = os.path.join(self.project_dir, 'demo', 'castle.jpg')
        input_castle = os.path.join(self.input_dir, 'castle.jpg')
        
        if os.path.exists(demo_castle) and not os.path.exists(input_castle):
            shutil.copy2(demo_castle, input_castle)
            print(f"✓ Copied castle.jpg from demo to input directory")
        elif os.path.exists(input_castle):
            print(f"✓ castle.jpg already exists in input directory")
        else:
            print(f"✗ castle.jpg not found in demo directory")
            return False
        return True
    
    def cleanup_test_assets(self):
        """Clean up test assets by removing castle.jpg from input directory."""
        input_castle = os.path.join(self.input_dir, 'castle.jpg')
        demo_castle = os.path.join(self.project_dir, 'demo', 'castle.jpg')
        
        # Only remove if it exists in demo (source) and input (copy)
        if os.path.exists(input_castle) and os.path.exists(demo_castle):
            try:
                os.remove(input_castle)
                print(f"✓ Cleaned up castle.jpg from input directory")
            except Exception as e:
                print(f"Warning: Could not remove castle.jpg from input: {e}")
    
    def run_build_and_test(self):
        """Run the build process and test the results."""
        print("=== Running Build Process ===")
        
        # Set up test assets first
        if not self.setup_test_assets():
            print("✗ Failed to set up test assets")
            return False
        
        # Clean up any previous test output
        self.cleanup_generated()
        
        try:
            # Use the test output directory instead of docs/
            # Fix templates path to point to project root templates
            templates_dir = os.path.join(self.project_dir, 'templates')
            static_dir = os.path.join(self.project_dir, 'static')
            generator = MonospaceGenerator(
                input_dir=str(self.input_dir),
                templates_dir=str(templates_dir),
                output_dir=str(self.generated_dir),
                static_dir=str(static_dir)
            )
            generator.build()
            print("✓ Build completed successfully")
        except Exception as e:
            print(f"✗ Build failed: {e}")
            self.cleanup_test_assets()  # Clean up even on build failure
            return False
        
        # Run all tests
        html_test = self.test_html_structure()
        css_test = self.test_css_styling()
        static_test = self.test_static_assets()
        
        # Clean up test assets after tests are done
        self.cleanup_test_assets()
        
        # Summary
        print("\n=== Test Summary ===")
        print(f"HTML Structure: {'PASS' if html_test else 'FAIL'}")
        print(f"CSS Styling: {'PASS' if css_test else 'FAIL'}")
        print(f"Static Assets: {'PASS' if static_test else 'FAIL'}")
        
        all_passed = html_test and css_test and static_test
        print(f"\nOverall Result: {'ALL TESTS PASS' if all_passed else 'SOME TESTS FAILED'}")
        
        # Final cleanup of generated files after tests complete
        print("\n=== Final Cleanup ===")
        self.cleanup_generated()
        print("✓ Generated files cleaned up")
        
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