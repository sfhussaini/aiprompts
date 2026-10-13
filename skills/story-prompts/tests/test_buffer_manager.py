"""Unit Tests for Buffer Manager Module - Phase 3, Module 3.4

Responsibilities:
- Test buffer initialization and frame addition.
- Validate file I/O operations.
- Test atomic operations (read-modify-write).
- Ensure state consistency across multiple operations.
"""

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(abspath(__file__)))

from scripts.buffer_manager_v2 import (
    initialize_buffer,
    add_frame_to_buffer,
    get_buffer_data,
    clear_buffer
)


def test_initialize_buffer():
    """Test buffer initialization."""
    
    clip_title = "Test_Clip"
    data = initialize_buffer(clip_title)
    
    assert data["current_clip"] == clip_title
    assert len(data["frames_buffer"]) == 0
    assert "metadata" in data


def test_add_frame_to_buffer():
    """Test adding frames to buffer."""
    
    clip_title = "Test_Clip_2"
    initialize_buffer(clip_title)
    
    # Add first frame
    add_frame_to_buffer(1, "Frame 1", {
        "positive_prompt": "A beautiful scene",
        "negative_prompt": "blurry, low quality",
        "wh_ratio": "3:2"
    }, clip_title)
    
    buffer_data = get_buffer_data(clip_title)
    assert len(buffer_data["frames_buffer"]) == 1
    assert buffer_data["frames_buffer"][0]["frame_number"] == 1


def test_add_multiple_frames():
    """Test adding multiple frames."""
    
    clip_title = "Test_Clip_3"
    initialize_buffer(clip_title)
    
    for i in range(1, 6):
        add_frame_to_buffer(i, f"Frame {i}", {
            "positive_prompt": f"Scene {i}",
            "negative_prompt": f"bad quality",
            "wh_ratio": "3:2"
        }, clip_title)
    
    buffer_data = get_buffer_data(clip_title)
    assert len(buffer_data["frames_buffer"]) == 5


def test_get_buffer_data():
    """Test retrieving buffer data."""
    
    clip_title = "Test_Clip_4"
    initialize_buffer(clip_title)
    add_frame_to_buffer(1, "Frame 1", {
        "positive_prompt": "Scene 1",
        "negative_prompt": "bad",
        "wh_ratio": "3:2"
    }, clip_title)
    
    buffer_data = get_buffer_data(clip_title)
    
    assert buffer_data["current_clip"] == clip_title
    assert len(buffer_data["frames_buffer"]) == 1


def test_clear_buffer():
    """Test clearing buffer."""
    
    clip_title = "Test_Clip_5"
    initialize_buffer(clip_title)
    add_frame_to_buffer(1, "Frame 1", {
        "positive_prompt": "Scene 1",
        "negative_prompt": "bad",
        "wh_ratio": "3:2"
    }, clip_title)
    
    assert len(get_buffer_data(clip_title)["frames_buffer"]) == 1
    
    clear_buffer(clip_title)
    
    buffer_after_clear = get_buffer_data(clip_title)
    assert len(buffer_after_clear["frames_buffer"]) == 0


def test_multiple_clips():
    """Test managing multiple clips."""
    
    clip1 = "Clip_A"
    clip2 = "Clip_B"
    
    initialize_buffer(clip1)
    add_frame_to_buffer(1, "Frame A", {
        "positive_prompt": "Scene A",
        "negative_prompt": "bad",
        "wh_ratio": "3:2"
    }, clip1)
    
    initialize_buffer(clip2)
    add_frame_to_buffer(1, "Frame B", {
        "positive_prompt": "Scene B",
        "negative_prompt": "bad",
        "wh_ratio": "3:2"
    }, clip2)
    
    # Verify both clips have their own buffers
    assert len(get_buffer_data(clip1)["frames_buffer"]) == 1
    assert len(get_buffer_data(clip2)["frames_buffer"]) == 1


def test_metadata_tracking():
    """Test that metadata is properly tracked."""
    
    clip_title = "Test_Clip_6"
    initialize_buffer(clip_title)
    
    for i in range(1, 4):
        add_frame_to_buffer(i, f"Frame {i}", {
            "positive_prompt": f"Scene {i}",
            "negative_prompt": "bad",
            "wh_ratio": "3:2"
        }, clip_title)
    
    buffer_data = get_buffer_data(clip_title)
    metadata = buffer_data["metadata"]
    
    assert metadata["total_frames_generated_in_buffer"] == 3


def test_edge_cases():
    """Test edge cases."""
    
    # Empty frames list after clear
    clip_title = "Test_Clip_7"
    initialize_buffer(clip_title)
    clear_buffer(clip_title)
    
    buffer_data = get_buffer_data(clip_title)
    assert len(buffer_data["frames_buffer"]) == 0
    
    # Buffer with special characters in title (sanitized filename)
    clip_title_special = "Clip/With:Special?Chars"
    initialize_buffer(clip_title_special)
    add_frame_to_buffer(1, "Frame", {
        "positive_prompt": "Scene",
        "negative_prompt": "bad",
        "wh_ratio": "3:2"
    }, clip_title_special)
    
    buffer_data = get_buffer_data(clip_title_special)
    assert len(buffer_data["frames_buffer"]) == 1


if __name__ == "__main__":
    print("=" * 70)
    print("Buffer Manager Unit Tests")
    print("=" * 70)
    
    test_initialize_buffer()
    print("✅ test_initialize_buffer passed!")
    
    test_add_frame_to_buffer()
    print("✅ test_add_frame_to_buffer passed!")
    
    test_add_multiple_frames()
    print("✅ test_add_multiple_frames passed!")
    
    test_get_buffer_data()
    print("✅ test_get_buffer_data passed!")
    
    test_clear_buffer()
    print("✅ test_clear_buffer passed!")
    
    test_multiple_clips()
    print("✅ test_multiple_clips passed!")
    
    test_metadata_tracking()
    print("✅ test_metadata_tracking passed!")
    
    test_edge_cases()
    print("✅ test_edge_cases passed!")
    
    print("\n🎉 All Buffer Manager tests passed!")
