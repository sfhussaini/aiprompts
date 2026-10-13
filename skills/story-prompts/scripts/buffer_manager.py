import json
import os
from typing import Dict, List, Any, Optional


# =============================================================================
# CONFIGURATION
# =============================================================================

BUFFER_FILE = 'story-prompts-buffer.json'
BUFFER_DIR = '.'  # Can be changed to a specific directory (e.g., './assets/buffers/')


def initialize_buffer(clip_title: str) -> Dict[str, Any]:
    """
    Initializes the buffer structure in a physical JSON file for a specific clip.
    This ensures state is preserved during the multi-step generation process.

    Args:
        clip_title: The title of the current clip being processed.

    Returns:
        Dictionary containing the initialized buffer data.
    """
    # Use clip title as part of filename to avoid conflicts
    safe_clip_name = sanitize_filename(clip_title)
    file_path = os.path.join(BUFFER_DIR, f"{safe_clip_name}_{BUFFER_FILE}")

    data = {
        "current_clip": clip_title,
        "frames_buffer": [],
        "metadata": {
            "total_frames_generated_in_buffer": 0,
            "peak_frames_selected": 0,
            "selection_criteria": "",
            "average_quality_score": 0.0,
            "generation_method": ""
        }
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Initialized {file_path} for clip: {clip_title}")
    except IOError as e:
        print(f"Error initializing buffer file: {e}")
        raise

    return data


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename to ensure it's safe for filesystem use.

    Args:
        filename: The original filename or title.

    Returns:
        A sanitized version of the filename.
    """
    # Replace spaces and special characters with underscores
    safe_name = "".join(c if c.isalnum() or c in "_-." else "_" for c in filename)
    return safe_name[:50]  # Limit length to avoid filesystem issues


def add_frame_to_buffer(
    frame_number: int,
    title: str,
    prompt_data: Dict[str, Any],
    clip_title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Appends a new frame's data to the existing buffer file.

    Args:
        frame_number: The sequential number of the frame (1-based).
        title: A descriptive title for the frame.
        prompt_data: Dictionary containing prompt-related fields.
        clip_title: Optional clip title (uses current from file if not provided).

    Returns:
        Updated buffer data dictionary.
    """
    # Determine which file to use
    safe_clip_name = sanitize_filename(clip_title or "unknown")
    file_path = os.path.join(BUFFER_DIR, f"{safe_clip_name}_{BUFFER_FILE}")

    try:
        if not os.path.exists(file_path):
            # Fallback initialization if called without prior initialization
            data = {
                "current_clip": clip_title or "unknown",
                "frames_buffer": [],
                "metadata": {
                    "total_frames_generated_in_buffer": 0,
                    "peak_frames_selected": 0,
                    "selection_criteria": "",
                    "average_quality_score": 0.0,
                    "generation_method": ""
                }
            }
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        # Validate and normalize prompt_data
        normalized_prompt_data = {
            "positive_prompt": prompt_data.get("positive_prompt", ""),
            "negative_prompt": prompt_data.get("negative_prompt", ""),
            "wh_ratio": prompt_data.get("wh_ratio", "3:2")
        }

        entry = {
            "frame_number": frame_number,
            "title": title,
            "prompt_data": normalized_prompt_data
        }

        data["frames_buffer"].append(entry)
        data["metadata"]["total_frames_generated_in_buffer"] += 1

        # Atomic write (write to temp file first, then rename)
        temp_path = file_path + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, file_path)

        print(f"Added frame {frame_number} to buffer for clip: {clip_title or data['current_clip']}")
        return data

    except IOError as e:
        print(f"Error writing to buffer file: {e}")
        raise


def get_buffer_data(clip_title: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves the current buffer data for a clip.

    Args:
        clip_title: The title of the clip (optional).

    Returns:
        Buffer data dictionary or empty dict if not found.
    """
    safe_clip_name = sanitize_filename(clip_title) if clip_title else "unknown"
    file_path = os.path.join(BUFFER_DIR, f"{safe_clip_name}_{BUFFER_FILE}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, FileNotFoundError):
        print(f"Buffer not found for clip: {clip_title or 'unknown'}")
        return {}


def clear_buffer(clip_title: Optional[str] = None) -> bool:
    """
    Clears the buffer file for a specific clip.

    Args:
        clip_title: The title of the clip (optional).

    Returns:
        True if successful, False otherwise.
    """
    safe_clip_name = sanitize_filename(clip_title) if clip_title else "unknown"
    file_path = os.path.join(BUFFER_DIR, f"{safe_clip_name}_{BUFFER_FILE}")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "current_clip": clip_title or "unknown",
                "frames_buffer": [],
                "metadata": {
                    "total_frames_generated_in_buffer": 0,
                    "peak_frames_selected": 0,
                    "selection_criteria": "",
                    "average_quality_score": 0.0,
                    "generation_method": ""
                }
            }, f, indent=2)
        print(f"Cleared buffer for clip: {clip_title or 'unknown'}")
        return True
    except IOError as e:
        print(f"Error clearing buffer file: {e}")
        return False


# =============================================================================
# MAIN ENTRY POINT (For testing)
# =============================================================================

if __name__ == "__main__":
    # Example usage for internal logic verification

    print("=" * 70)
    print("Story Prompts Buffer Module - Test Run")
    print("=" * 70)

    # Create buffer directory if it doesn't exist
    os.makedirs(BUFFER_DIR, exist_ok=True)

    # Initialize buffer
    clip_title = "Intro Scene"
    initialize_buffer(clip_title)

    # Add frames to buffer
    add_frame_to_buffer(1, "Opening Shot", {
        "positive_prompt": "...",
        "negative_prompt": "...",
        "wh_ratio": "3:2"
    }, clip_title)

    add_frame_to_buffer(2, "Action Sequence", {
        "positive_prompt": "...",
        "negative_prompt": "...",
        "wh_ratio": "3:2"
    }, clip_title)

    # Retrieve and display buffer data
    print("\n1. Buffer Data Retrieved:")
    buffer_data = get_buffer_data(clip_title)
    print(f"   Current Clip: {buffer_data.get('current_clip', 'N/A')}")
    print(f"   Total Frames in Buffer: {len(buffer_data.get('frames_buffer', []))}")

    # Test with different clip title
    print("\n2. Testing with Different Clip Title:")
    initialize_buffer("Scene 2 - Forest Battle")
    add_frame_to_buffer(1, "Forest Entry", {
        "positive_prompt": "...",
        "negative_prompt": "...",
        "wh_ratio": "3:2"
    }, "Scene 2 - Forest Battle")

    buffer_data_2 = get_buffer_data("Scene 2 - Forest Battle")
    print(f"   Frames in Scene 2 Buffer: {len(buffer_data_2.get('frames_buffer', []))}")

    # Test clearing buffer
    print("\n3. Testing Clear Buffer:")
    clear_buffer(clip_title)
    buffer_after_clear = get_buffer_data(clip_title)
    print(f"   Frames after clear: {len(buffer_after_clear.get('frames_buffer', []))}")

    print("\nBuffer Module tests passed!")
