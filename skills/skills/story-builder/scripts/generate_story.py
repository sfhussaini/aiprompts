import os
import sys
import argparse

def create_story_file(folder_path, filename, content):
    """Creates a directory and writes the story content to a file."""
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created directory: {folder_path}")
        
        # Construct full path
        file_path = os.path.join(folder_path, filename)
        
        # Write the content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully created story file at: {file_path}")
    except Exception as e:
        print(f"Error creating story file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a story file in a specified directory.")
    parser.add_argument("--path", required=True, help="The path where the folder should be created.")
    parser.add_argument("--filename", default="story.txt", help="The name of the output file (default: story.txt)")
    parser.add_argument("--content", required=True, help="The full content of the story to write.")

    args = parser.parse_args()
    create_story_file(args.path, args.filename, args.content)
