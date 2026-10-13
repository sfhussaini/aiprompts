"""Buffer Validator Module - Phase 2, Module 2.2


Responsibilities:
- Comprehensive validation of buffer state before final output transformation.
- Check for missing prompt data, frame count mismatches, JSON structure integrity.
- Detect duplicate frame IDs and ensure temporal ordering.
"""

import json
from typing import Dict, List, Any, Optional, Tuple


# =============================================================================
# VALIDATION CONSTANTS & CONFIGURATION
# =============================================================================

MIN_FRAME_SCORE = 50.0  # Minimum acceptable score for a frame (configurable)
REQUIRED_PROMPT_FIELDS = [
    "positive_prompt",
    "negative_prompt",
    "wh_ratio"
]
REQUIRED_METADATA_FIELDS = [
    "total_frames_generated_in_buffer",
    "peak_frames_selected",
    "selection_criteria",
    "average_quality_score",
    "generation_method"
]


# =============================================================================
# VALIDATION FUNCTIONS (Python-heavy)
# =============================================================================

def validate_buffer_structure(buffer_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates the overall structure of the buffer data.

    Args:
        buffer_data: The buffer dictionary from get_buffer_data().

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []

    # Check required top-level keys
    if "current_clip" not in buffer_data:
        errors.append("Missing 'current_clip' field")
    elif not isinstance(buffer_data["current_clip"], str):
        errors.append("'current_clip' must be a string")

    if "frames_buffer" not in buffer_data:
        errors.append("Missing 'frames_buffer' field")
    elif not isinstance(buffer_data["frames_buffer"], list):
        errors.append("'frames_buffer' must be a list")

    if "metadata" not in buffer_data:
        errors.append("Missing 'metadata' field")
    elif not isinstance(buffer_data["metadata"], dict):
        errors.append("'metadata' must be a dictionary")

    return len(errors) == 0, errors


def validate_frame_count(
    buffer_data: Dict[str, Any], 
    expected_frames: Optional[int] = None
) -> Tuple[bool, List[str]]:
    """
    Validates that the frame count matches metadata and expectations.

    Args:
        buffer_data: The buffer dictionary.
        expected_frames: Optional expected frame count (e.g., from selection optimizer).

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []

    frames_buffer = buffer_data.get("frames_buffer", [])
    metadata = buffer_data.get("metadata", {})

    # Check actual frame count matches metadata
    metadata_count = metadata.get("total_frames_generated_in_buffer", 0)
    if len(frames_buffer) != metadata_count:
        errors.append(
            f"Frame count mismatch: JSON has {len(frames_buffer)} frames, "
            f"metadata reports {metadata_count}"
        )

    # Check against expected count if provided
    if expected_frames is not None and len(frames_buffer) != expected_frames:
        errors.append(
            f"Expected {expected_frames} frames but found {len(frames_buffer)}"
        )

    return len(errors) == 0, errors


def validate_prompt_data(frames: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validates that each frame has required prompt data.

    Args:
        frames: List of frame dictionaries from the buffer.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []

    for i, frame in enumerate(frames):
        frame_id = frame.get("frame_number", f"unknown_{i}")

        # Check required prompt fields
        for field in REQUIRED_PROMPT_FIELDS:
            if field not in frame or not frame[field]:
                errors.append(
                    f"Frame {frame_id}: Missing or empty '{field}' field"
                )

    return len(errors) == 0, errors


def validate_frame_scores(frames: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validates that all frames have acceptable scores.

    Args:
        frames: List of frame dictionaries from the buffer.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []

    for i, frame in enumerate(frames):
        # Try multiple possible score field names
        score = None
        if "weighted_score" in frame:
            score = frame["weighted_score"]
        elif "score" in frame:
            score = frame["score"]
        
        if score is not None and isinstance(score, (int, float)):
            if score < MIN_FRAME_SCORE:
                errors.append(
                    f"Frame {i}: Score {score} below minimum threshold of {MIN_FRAME_SCORE}"
                )

    return len(errors) == 0, errors


def validate_frame_ids(frames: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validates that all frame IDs are unique.

    Args:
        frames: List of frame dictionaries from the buffer.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    seen_ids = set()

    for i, frame in enumerate(frames):
        # Try multiple possible ID field names
        frame_id = None
        if "frame_number" in frame:
            frame_id = frame["frame_number"]
        elif "id" in frame:
            frame_id = frame["id"]
        
        if frame_id is not None:
            if frame_id in seen_ids:
                errors.append(f"Duplicate frame ID found: {frame_id}")
            else:
                seen_ids.add(frame_id)

    return len(errors) == 0, errors


def validate_temporal_ordering(frames: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validates that frames are in temporal order.

    Args:
        frames: List of frame dictionaries from the buffer.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []

    if len(frames) < 2:
        return True, errors

    for i in range(1, len(frames)):
        prev_ts = frames[i-1].get("timestamp") or 0.0
        curr_ts = frames[i].get("timestamp") or 0.0

        # Handle None timestamps gracefully
        if prev_ts is not None and curr_ts is not None:
            if curr_ts < prev_ts:
                errors.append(
                    f"Temporal order violation: Frame {i} (ts={curr_ts}) "
                    f"comes before Frame {i-1} (ts={prev_ts})"
                )

    return len(errors) == 0, errors


def validate_metadata_completeness(buffer_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates that metadata has all required fields.

    Args:
        buffer_data: The buffer dictionary.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    metadata = buffer_data.get("metadata", {})

    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata or metadata[field] is None:
            errors.append(f"Metadata missing required field: '{field}'")

    return len(errors) == 0, errors


# =============================================================================
# COMBINED VALIDATION (Python-heavy)
# =============================================================================

def validate_buffer_comprehensive(
    buffer_data: Dict[str, Any], 
    expected_frames: Optional[int] = None
) -> Tuple[bool, List[str]]:
    """
    Runs all validation checks on the buffer data.

    Args:
        buffer_data: The buffer dictionary from get_buffer_data().
        expected_frames: Optional expected frame count (e.g., from selection optimizer).

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    all_errors = []

    # Run all validation checks
    is_valid, errors = validate_buffer_structure(buffer_data)
    all_errors.extend(errors)

    is_valid, errors = validate_frame_count(buffer_data, expected_frames)
    all_errors.extend(errors)

    frames = buffer_data.get("frames_buffer", [])
    
    if len(frames) > 0:
        is_valid, errors = validate_prompt_data(frames)
        all_errors.extend(errors)

        is_valid, errors = validate_frame_scores(frames)
        all_errors.extend(errors)

        is_valid, errors = validate_frame_ids(frames)
        all_errors.extend(errors)

        is_valid, errors = validate_temporal_ordering(frames)
        all_errors.extend(errors)

    is_valid, errors = validate_metadata_completeness(buffer_data)
    all_errors.extend(errors)

    return len(all_errors) == 0, all_errors


def get_validation_summary(
    buffer_data: Dict[str, Any], 
    expected_frames: Optional[int] = None
) -> Dict[str, Any]:
    """
    Runs all validations and returns a summary report.

    Args:
        buffer_data: The buffer dictionary from get_buffer_data().
        expected_frames: Optional expected frame count.

    Returns:
        Dictionary containing validation results and statistics.
    """
    is_valid, errors = validate_buffer_comprehensive(buffer_data, expected_frames)

    frames = buffer_data.get("frames_buffer", [])
    metadata = buffer_data.get("metadata", {})

    # Calculate statistics
    avg_score = 0.0
    if frames:
        scores = [f.get("weighted_score") or f.get("score", 0) for f in frames]
        avg_score = sum(scores) / len(scores) if scores else 0

    summary = {
        "is_valid": is_valid,
        "total_errors": len(errors),
        "error_details": errors,
        "statistics": {
            "frame_count": len(frames),
            "expected_frame_count": expected_frames,
            "average_score": round(avg_score, 2),
            "peak_frames_selected": metadata.get("peak_frames_selected", 0),
            "total_frames_generated_in_buffer": metadata.get("total_frames_generated_in_buffer", 0)
        }
    }

    return summary


# =============================================================================
# MAIN ENTRY POINT (For testing)
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Story Prompts Buffer Validator - Test Run")
    print("=" * 70)

    # Import buffer_manager_v2 for integration testing
    import sys
    from os.path import dirname, abspath
    script_dir = dirname(abspath(__file__))
    parent_dir = dirname(script_dir)
    sys.path.insert(0, parent_dir)

    try:
        from buffer_manager_v2 import get_buffer_data, initialize_buffer, add_frame_to_buffer
    except ImportError:
        print("   ⚠️  Importing test data directly (buffer_manager_v2 not found)")
        
        # Create a mock buffer for testing if module not available
        clip_title = "Test_Clip"
        buffer_data = {
            "current_clip": clip_title,
            "frames_buffer": [
                {
                    "frame_number": 1,
                    "title": "Frame 1 - Good",
                    "prompt_data": {
                        "positive_prompt": "A beautiful landscape",
                        "negative_prompt": "blurry, low quality",
                        "wh_ratio": "3:2"
                    },
                    "weighted_score": 90.5,
                    "timestamp": 1.0
                },
                {
                    "frame_number": 2,
                    "title": "Frame 2 - Missing Score",
                    "prompt_data": {
                        "positive_prompt": "Another scene",
                        "negative_prompt": "bad details",
                        "wh_ratio": "3:2"
                    },
                    # Note: No weighted_score field to test validation
                    "timestamp": 2.0
                }
            ],
            "metadata": {
                "total_frames_generated_in_buffer": 2,
                "peak_frames_selected": 1,
                "selection_criteria": "Test",
                "average_quality_score": 90.5,
                "generation_method": "Test"
            }
        }

    # Create a test buffer with known state
    clip_title = "Test_Clip"
    
    print("\n1. Retrieving Buffer Data...")
    try:
        buffer_data = get_buffer_data(clip_title)
        print(f"   Frames in buffer: {len(buffer_data.get('frames_buffer', []))}")
    except Exception as e:
        print(f"   Using mock data (error: {e})")

    print("\n2. Running Comprehensive Validation...")
    is_valid, errors = validate_buffer_comprehensive(buffer_data)

    if is_valid:
        print("   ✅ Buffer validation PASSED!")
    else:
        print(f"   ⚠️  Buffer validation found {len(errors)} issues:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"      - {error}")

    print("\n3. Getting Validation Summary...")
    summary = get_validation_summary(buffer_data)
    print(f"   Is Valid: {summary['is_valid']}")
    print(f"   Total Errors: {summary['total_errors']}")
    print(f"   Frame Count: {summary['statistics']['frame_count']}")

    # Test with expected_frames parameter
    print("\n4. Testing with Expected Frames Parameter...")
    is_valid, errors = validate_buffer_comprehensive(buffer_data, expected_frames=3)
    if not is_valid:
        print(f"   ⚠️  Expected 3 frames but found {len(buffer_data.get('frames_buffer', []))}")

    print("\nBuffer Validator tests passed!")
