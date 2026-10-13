#!/usr/bin/env python3
"""
ensure_output_dir.py

Purpose:
    Ensures that the specified output directory exists before the
    visualize-story pipeline writes any files (e.g., story.txt, story.json).
    This prevents "FileNotFoundError" when the output folder is missing.

Usage:
    python scripts/ensure_output_dir.py [output_dir]

Arguments:
    output_dir (optional, str): Path to the directory that should exist.
        Defaults to "output" if not provided.

Behavior:
    - Creates the directory (and any missing parent directories) using
      os.makedirs(path, exist_ok=True).
    - Prints the absolute path of the ready directory to stdout.
    - Exits with code 0 on success.

Example:
    $ python scripts/ensure_output_dir.py output
    Output directory ready: /absolute/path/to/output

Notes for LLM agents:
    - This script is idempotent; running it multiple times is safe.
    - It should be called as a pre-flight step before invoking story-builder
      or any other step that writes files into the output directory.
    - No return value; the side effect is the created directory.
"""

import os
import sys

def ensure_output_dir(path: str = "output") -> str:
    """
    Create the output directory if it does not exist.

    Args:
        path (str): Directory path to create. Defaults to "output".

    Returns:
        str: Absolute path of the created/existing directory.
    """
    os.makedirs(path, exist_ok=True)
    abs_path = os.path.abspath(path)
    print(f"Output directory ready: {abs_path}")
    return abs_path

if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "output"
    ensure_output_dir(output_dir)