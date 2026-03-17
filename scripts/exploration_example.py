#!/usr/bin/env python3
"""
Repository Exploration and Analysis Script

This script provides utilities for exploring and understanding
the yyworld7/skill repository structure when documentation is limited.

Usage:
    python exploration_example.py [--path PATH] [--verbose]

Requirements:
    - Python 3.6+
    - Standard library modules only (ast, os, sys, json, etc.)
"""

import os
import sys
import ast
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RepositoryInfo:
    """Container for repository exploration results."""
    path: str = ""
    python_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    doc_files: List[str] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    classes: List[Dict[str, Any]] = field(default_factory=list)
    functions: List[Dict[str, Any]] = field(default_factory=list)
    imports: Dict[str, List[str]] = field(default_factory=dict)


def explore_repository(path: str) -> RepositoryInfo:
    """
    Explore a repository and gather information about its structure.
    
    Args:
        path: Root directory path to explore
        
    Returns:
        RepositoryInfo object with exploration results
    """
    info = RepositoryInfo(path=path)
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"Error: Path '{path}' does not exist")
        return info
    
    # Collect files by type
    for file_path in path_obj.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(path_obj))
            
            if file_path.suffix == ".py":
                info.python_files.append(relative_path)
                
                # Identify test files
                if "test" in relative_path.lower() or file_path.name.startswith("test_"):
                    info.test_files.append(relative_path)
                
                # Identify entry points
                if file_path.name in ("__main__.py", "cli.py", "app.py", "main.py"):
                    info.entry_points.append(relative_path)
            
            # Configuration files
            elif file_path.suffix in (".json", ".yaml", ".yml", ".toml", ".cfg", ".ini"):
                info.config_files.append(relative_path)
            
            # Documentation files
            elif file_path.suffix in (".md", ".rst", ".txt", ".doc"):
                info.doc_files.append(relative_path)
    
    # Analyze Python files
    for py_file in info.python_files:
        file_path = path_obj / py_file
        analyze_python_file(file_path, info)
    
    return info


def analyze_python_file(file_path: Path, info: RepositoryInfo) -> None:
    """
    Analyze a Python file for classes, functions, and imports.
    
    Args:
        file_path: Path to the Python file
        info: RepositoryInfo to populate with analysis results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            # Find class definitions
            if isinstance(node, ast.ClassDef):
                info.classes.append({
                    "name": node.name,
                    "file": str(file_path),
                    "lineno": node.lineno,
                    "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            
            # Find function definitions
            elif isinstance(node, ast.FunctionDef):
                info.functions.append({
                    "name": node.name,
                    "file": str(file_path),
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "is_async": isinstance(node, ast.AsyncFunctionDef)
                })
            
            # Track imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split('.')[0]
                    if module not in info.imports:
                        info.imports[module] = []
                    info.imports[module].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split('.')[0]
                    if module not in info.imports:
                        info.imports[module] = []
                    for alias in node.names:
                        info.imports[module].append(f"{node.module}.{alias.name}")
    
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not analyze {file_path}: {e}")


def print_summary(info: RepositoryInfo) -> None:
    """Print a summary of the repository analysis."""
    print("=" * 60)
    print("REPOSITORY EXPLORATION SUMMARY")
    print("=" * 60)
    print(f"Path: {info.path}")
    print(f"Analysis Date: {datetime.now().isoformat()}")
    print()
    
    print(f"Python Files: {len(info.python_files)}")
    print(f"Test Files: {len(info.test_files)}")
    print(f"Config Files: {len(info.config_files)}")
    print(f"Documentation Files: {len(info.doc_files)}")
    print(f"Potential Entry Points: {len(info.entry_points)}")
    print()
    
    if info.classes:
        print(f"Classes Found: {len(info.classes)}")
        for cls in info.classes:
            print(f"  - {cls['name']} ({', '.join(cls['bases']) or 'no base'})")
            print(f"    Location: {cls['file']}")
            print(f"    Methods: {', '.join(cls['methods'][:5])}")
        print()
    
    if info.functions:
        print(f"Functions Found: {len(info.functions)}")
        # Show top 10 functions
        for func in info.functions[:10]:
            args = ', '.join(func['args'][:3]) or "(no args)"
            async_str = "async " if func['is_async'] else ""
            print(f"  - {async_str}{func['name']}({args})")
        if len(info.functions) > 10:
            print(f"  ... and {len(info.functions) - 10} more")
        print()
    
    if info.imports:
        print("External Dependencies:")
        for module, imports in sorted(info.imports.items()):
            if any(m not in ('os', 'sys', 'typing', 'collections', 'itertools', 
                            'pathlib', 'abc', 'dataclasses', 'contextlib') 
                   for m in [module]):
                unique_imports = list(set(imports))
                print(f"  - {module}: {', '.join(unique_imports[:5])}")
        print()


def find_main_modules(info: RepositoryInfo) -> List[str]:
    """
    Identify potential main modules that should be examined first.
    
    Returns:
        List of file paths to examine first
    """
    priorities = []
    
    for file_path in info.python_files:
        filename = Path(file_path).name
        
        # Priority files
        if filename in ("__init__.py", "__main__.py", "cli.py", "app.py", "main.py"):
            priorities.append(file_path)
    
    # Add test files for understanding usage patterns
    for test_file in info.test_files[:3]:
        if test_file not in priorities:
            priorities.append(test_file)
    
    return priorities


def generate_usage_guide(info: RepositoryInfo) -> str:
    """
    Generate a usage guide based on the repository structure.
    
    Args:
        info: RepositoryInfo with analysis results
        
    Returns:
        Markdown-formatted usage guide
    """
    guide = []
    guide.append("# Auto-Generated Usage Guide")
    guide.append("")
    guide.append(f"*Generated from repository analysis on {datetime.now().isoformat()}*")
    guide.append("")
    guide.append("## Installation")
    guide.append("")
    guide.append("```bash")
    
    if any(f.endswith("setup.py") for f in info.python_files):
        guide.append("pip install -e .")
    elif any(f.endswith("pyproject.toml") for f in info.python_files):
        guide.append("pip install -e .")
    elif any("requirements.txt" in f for f in info.config_files):
        guide.append("pip install -r requirements.txt")
    
    guide.append("```")
    guide.append("")
    guide.append("## Quick Start")
    guide.append("")
    
    # Try to determine the main module
    main_modules = find_main_modules(info)
    
    if info.classes:
        guide.append("### Available Classes")
        for cls in info.classes[:5]:
            guide.append(f"- `{cls['name']}` - {cls['file']}")
        guide.append("")
    
    if info.entry_points:
        guide.append("### Entry Points")
        for entry in info.entry_points:
            guide.append(f"- `{entry}`")
        guide.append("")
    
    if main_modules:
        guide.append("### Recommended Reading Order")
        for i, module in enumerate(main_modules, 1):
            guide.append(f"{i}. `{module}`")
        guide.append("")
    
    guide.append("## Dependencies")
    guide.append("")
    guide.append("```python")
    
    # List external dependencies
    external_deps = set()
    for module, imports in info.imports.items():
        if module not in ('os', 'sys', 'typing', 'collections', 'itertools',
                          'pathlib', 'abc', 'dataclasses', 'contextlib', 're',
                          'json', 'math', 'datetime', 'warnings', 'functools',
                          'operator', 'string', 'types', 'copy', 'io'):
            external_deps.add(module)
    
    for dep in sorted(external_deps)[:10]:
        guide.append(f"# Requires: {dep}")
    
    guide.append("```")
    guide.append("")
    
    return "\n".join(guide)


def main() -> int:
    """Main entry point for the exploration script."""
    parser = argparse.ArgumentParser(
        description="Explore and analyze a repository structure"
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Path to explore (default: current directory)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for usage guide (optional)"
    )
    
    args = parser.parse_args()
    
    # Explore repository
    info = explore_repository(args.path)
    
    # Print summary
    print_summary(info)
    
    # Generate and optionally save usage guide
    guide = generate_usage_guide(info)
    
    if args.verbose:
        print("\n" + "=" * 60)
        print("GENERATED USAGE GUIDE")
        print("=" * 60)
        print(guide)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(guide)
        print(f"\nUsage guide saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
