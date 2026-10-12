import sys
import os
import subprocess

def convert_md_to_docx(md_path, docx_path=None):
    """
    Converts a markdown file to a .docx file using Pandoc.
    Requires Pandoc to be installed on the system path.
    """
    if not os.path.exists(md_path):
        print(f"Error: File {md_path} not found.")
        return

    if docx_path is None:
        docx_path = md_path.replace(".md", ".docx")

    try:
        # Pandoc command: pandoc -o output.docx input.md
        # We use a list for subprocess.run to handle paths with spaces correctly.
        result = subprocess.run(
            ["pandoc", md_path, "-o", docx_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully created: {docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc error: {e.stderr}")
    except FileNotFoundError:
        print("Error: Pandoc is not installed or not found in the system PATH.")
        print("Please install Pandoc from https://pandoc.org/installing.html")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown-to-docx.py <path_to_markdown_file> [path_to_output_docx]")
    else:
        input_md = sys.argv[1]
        output_docx = sys.argv[2] if len(sys.argv) > 2 else None
        convert_md_to_docx(input_md, output_docx)

