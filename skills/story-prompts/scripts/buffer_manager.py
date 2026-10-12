import json
import os

BUFFER_FILE = 'story-prompts-buffer.json'

def initialize_buffer(clip_title):
    """
    Initializes the buffer structure in a physical JSON file for a specific clip.
    This ensures state is preserved during the multi-step generation process.
    """
    data = {
        "current_clip": clip_title,
        "frames_buffer": []
    }
    with open(BUFFER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Initialized {BUFFER_FILE} for clip: {clip_title}")
    return data

def add_frame_to_buffer(frame_number, title, prompt_data):
    """
    Appends a new frame's data to the existing buffer file.
    """
    if not os.path.exists(BUFFER_FILE):
        # Fallback if called without prior initialization
        data = {"current_clip": "unknown", "frames_buffer": []}
    else:
        with open(BUFFER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

    entry = {
        "frame_number": frame_number,
        "title": title,
        "prompt_data": prompt_data
    }
    data["frames_buffer"].append(entry)
    
    with open(BUFFER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Added frame {frame_number} to {BUFFER_FILE}")

if __name__ == "__main__":
    # Example usage for internal logic verification
    initialize_buffer("Intro Scene")
    add_frame_to_buffer(1, "Opening Shot", {"postive_prompt": "...", "negative_prompt": "...", "wh_ratio": "3:2"})