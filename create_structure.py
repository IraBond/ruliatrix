#!/usr/bin/env python3
"""
Ruliatrix Project Structure Generator

This script creates a philosophically recursive folder hierarchy that reflects
the core algorithmic principles and computational domains of the Ruliatrix framework.

The Pascal–Euler–Galois Fractal Ruliard Algorithm (PEGFRA) structure is mirrored
in this organization, enabling symbolic mathematical computations within a cohesive framework.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


class RuliatrixStructureGenerator:
    """
    Generates the folder structure and boilerplate files for the Ruliatrix project.
    """
    
    def __init__(self, base_dir="."):
        """Initialize the structure generator with base directory."""
        self.base_dir = Path(base_dir) / "ruliatrix"
        self.folders = [
            # Documentation
            "docs/theory",
            "docs/diagrams/architecture_diagrams",
            "docs/diagrams/concept_maps",
            "docs/examples",
            
            # Source code
            "src/core/pascal",
            "src/core/euler",
            "src/core/galois",
            "src/core/fractal",
            "src/quantum",
            "src/neural",
            "src/applications",
            "src/visualization",
            
            # Tests
            "tests/core_tests",
            "tests/quantum_tests",
            "tests/neural_tests",
            "tests/integration_tests",
            
            # Examples
            "examples/quantum_examples",
            "examples/neural_examples",
            "examples/application_examples",
            
            # Tools and Notebooks
            "tools",
            "notebooks/exploration",
            "notebooks/tutorials",
            "notebooks/demonstrations",
            
            # GitHub
            ".github/workflows",
            ".github/ISSUE_TEMPLATE",
        ]
        
        # Track src/ directories for __init__.py files
        self.src_dirs = [d for d in self.folders if d.startswith("src")]
    
    def create_directory_structure(self):
        """Create the directory structure."""
        print("\n🔄 Creating Ruliatrix directory structure...")
        
        for folder in self.folders:
            folder_path = self.base_dir / folder
            try:
                os.makedirs(folder_path, exist_ok=True)
                print(f"✅ Created {folder_path}")
            except Exception as e:
                print(f"❌ Error creating {folder_path}: {e}")
    
    def create_init_files(self):
        """Create __init__.py files in src/ directories."""
        print("\n🔄 Creating __init__.py files in src/ directories...")
        
        # Get all src directories and subdirectories
        src_dirs = [self.base_dir / d for d in self.src_dirs]
        all_dirs = []
        
        # Find the src/ directory and all its subdirectories
        src_base = self.base_dir / "src"
        for root, dirs, _ in os.walk(src_base):
            for d in dirs:
                all_dirs.append(Path(root) / d)
        
        # Add the src/ directory itself
        all_dirs.append(src_base)
        
        # Create __init__.py in each directory
        for d in all_dirs:
            init_file = d / "__init__.py"
            try:
                with open(init_file, 'w') as f:
                    f.write(f'"""\n{d.name.title()} module for the Ruliatrix framework.\n"""\n\n')
                print(f"✅ Created {init_file}")
            except Exception as e:
                print(f"❌ Error creating {init_file}: {e}")
    
    def create_boilerplate_files(self):
        """Create basic project files."""
        print("\n🔄 Creating boilerplate files...")
        
        # README.md
        readme_content = f"""# Ruliatrix

A symbolic computation framework based on the Pascal–Euler–Galois Fractal Ruliard Algorithm (PEGFRA).

## Overview

Ruliatrix unifies mathematical domains through a cohesive computational framework:

- **Pascal's Triangle**: Combinatorial structures and patterns
- **Euler's Methods**: Mathematical analysis and transformations
- **Galois Theory**: Algebraic structures and symmetries
- **Fractal Recursion**: Self-similar patterns across dimensions

## Structure

The project follows a philosophically recursive organization that reflects the mathematical principles
of PEGFRA:

```
ruliatrix/
├── docs/ - Documentation and theory
├── src/ - Source code organized by mathematical domain
├── tests/ - Comprehensive test suite
├── examples/ - Example applications
├── tools/ - Utility scripts and tools
├── notebooks/ - Interactive explorations and tutorials
```

## Getting Started

```python
# Example: Computing a high-dimensional Pascal structure
from ruliatrix.core.pascal import generate_higher_dimensional
from ruliatrix.visualization import plot_3d_projection

# Generate a 5-dimensional Pascal structure
pascal_5d = generate_higher_dimensional(dimension=5, depth=10)

# Visualize its 3D projection
plot_3d_projection(pascal_5d)
```

## License

MIT License - See LICENSE file for details

## Created

{datetime.now().strftime('%Y-%m-%d')}
"""
        
        # LICENSE
        license_content = """MIT License

Copyright (c) {0} Ruliatrix Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(datetime.now().year)
        
        # setup.py
        setup_content = """from setuptools import setup, find_packages

setup(
    name="ruliatrix",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "sympy>=1.8",
        "matplotlib>=3.4.0",
        "networkx>=2.6.0",
        "plotly>=5.3.0",
    ],
    author="Ruliatrix Contributors",
    author_email="info@ruliatrix.org",
    description="A symbolic computation framework based on PEGFRA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruliatrix/ruliatrix",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
)
"""
        
        # requirements.txt
        requirements_content = """# Core dependencies
numpy>=1.20.0
scipy>=1.7.0
sympy>=1.8
matplotlib>=3.4.0
networkx>=2.6.0
plotly>=5.3.0

# Visualization tools
streamlit>=1.10.0
jupyter>=1.0.0
ipywidgets>=7.6.0

# Testing
pytest>=6.2.5
pytest-cov>=2.12.0

# Documentation
sphinx>=4.0.0
sphinx-rtd-theme>=0.5.2
"""
        
        files = {
            "README.md": readme_content,
            "LICENSE": license_content,
            "setup.py": setup_content,
            "requirements.txt": requirements_content
        }
        
        for filename, content in files.items():
            file_path = self.base_dir / filename
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✅ Created {file_path}")
            except Exception as e:
                print(f"❌ Error creating {file_path}: {e}")
    
    def generate(self):
        """Execute the full generation process."""
        print("🚀 Starting Ruliatrix project structure generation...")
        
        # Create main project directory
        os.makedirs(self.base_dir, exist_ok=True)
        print(f"✅ Created main project directory: {self.base_dir}")
        
        # Create the structure
        self.create_directory_structure()
        self.create_init_files()
        self.create_boilerplate_files()
        
        print("\n✨ Ruliatrix project structure generation complete! ✨")
        print(f"📁 Project created at: {self.base_dir.absolute()}")


if __name__ == "__main__":
    # Default to current directory if no argument is provided
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Create and execute the generator
    generator = RuliatrixStructureGenerator(base_dir)
    generator.generate()