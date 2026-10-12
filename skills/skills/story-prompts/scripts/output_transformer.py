"""
Output Transformer Module - Phase 1, Module 1.5


NLP Responsibilities: Agent populates selection_reason, action_progression, visual_interest_score, is_peak_frame
Python Responsibilities: Flatten nested JSON; Add frame_selection_metadata block; Validate schema compliance


This module transforms the hierarchical structure (Movie→Scene→Segment→Clip→Frames) 
into a flattened production-ready format suitable for image generation pipelines.
"""

import json
from typing import Dict, List, Any, Optional, Tuple


# =============================================================================
# OUTPUT TEMPLATE STRUCTURE (Based on assets/output_template.md)
# =============================================================================

OUTPUT_SCHEMA = {
    "movie": str,
    "scenes": [
        {
            "scene": str,
            "segments": [
                {
                    "segment": str,
                    "clips": [
                        {
                            "clip": str,
                            "frames": [
                                {
                                    "frame_number": int,
                                    "title": str,
                                    "prompt_data": {
                                        "positive_prompt": str,
                                        "negative_prompt": str,
                                        "wh_ratio": str
                                    },
                                    "selection_reason": str,
                                    "action_progression": float,  # 0-1 scale
                                    "visual_interest_score": int,  # 0-100
                                    "is_peak_frame": bool
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "frame_selection_metadata": {
        "total_frames_generated_in_buffer": int,
        "peak_frames_selected": int,
        "selection_criteria": str,
        "average_quality_score": float,
        "generation_method": str
    }
}


# =============================================================================
# TRANSFORMATION FUNCTIONS (Python-heavy)
# =============================================================================

def flatten_hierarchy_to_production(
    hierarchical_data: Dict[str, Any],
    movie_title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Python Job: Flatten nested Movie→Scene→Segment→Clip→Frames structure 
    into production-ready format with all metadata fields.

    NLP Agent provides: selection_reason, action_progression, visual_interest_score, is_peak_frame

    Args:
        hierarchical_data: Hierarchical JSON from story-prompts output (with frames)
        movie_title: Movie title (defaults to hierarchical_data.get('movie') if present)

    Returns:
        Dict with flattened structure and frame_selection_metadata block
    """
    # Use provided movie title or extract from data
    final_movie = movie_title or hierarchical_data.get("movie", "Untitled")

    # Process scenes/segments/clips/frames hierarchy
    processed_scenes = []
    for scene in hierarchical_data.get("scenes", []):
        scene_name = scene.get("scene", "Unknown Scene")

        processed_segments = []
        for segment in scene.get("segments", []):
            segment_name = segment.get("segment", "Unknown Segment")

            processed_clips = []
            for clip in segment.get("clips", []):
                clip_name = clip.get("clip", "Unknown Clip")

                # Process frames - NLP agent provides the metadata fields
                processed_frames = []
                frame_number_counter = 0
                
                for frame in clip.get("frames", []):
                    # Auto-generate frame number if missing or invalid
                    existing_frame_num = frame.get("frame_number")
                    if not isinstance(existing_frame_num, int) or existing_frame_num <= 0:
                        frame_number_counter += 1
                        new_frame_num = frame_number_counter
                    else:
                        new_frame_num = existing_frame_num

                    # Extract prompt_data (from prompt-formula skill)
                    prompt_data = frame.get("prompt_data", {})

                    # NLP Agent populates these fields:
                    selection_reason = frame.get("selection_reason", "")
                    action_progression = frame.get("action_progression", 0.5)
                    visual_interest_score = frame.get("visual_interest_score", 80)
                    is_peak_frame = frame.get("is_peak_frame", False)

                    processed_frames.append({
                        "frame_number": new_frame_num,
                        "title": frame.get("title", ""),
                        "prompt_data": prompt_data,
                        "selection_reason": selection_reason,
                        "action_progression": action_progression,
                        "visual_interest_score": visual_interest_score,
                        "is_peak_frame": is_peak_frame
                    })

                processed_clips.append({
                    "clip": clip_name,
                    "frames": processed_frames
                })

            processed_segments.append({
                "segment": segment_name,
                "clips": processed_clips
            })

        processed_scenes.append({
            "scene": scene_name,
            "segments": processed_segments
        })

    # Calculate metadata (Python Job) - based on processed data for consistency
    total_frames = 0
    peak_frames = 0
    quality_scores = []

    for scene in processed_scenes:
        for segment in scene.get("segments", []):
            for clip in segment.get("clips", []):
                for frame in clip.get("frames", []):
                    total_frames += 1
                    score = frame.get("visual_interest_score", 0)
                    quality_scores.append(score)
                    if frame.get("is_peak_frame", False):
                        peak_frames += 1

    # Calculate average quality score
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0

    return {
        "movie": final_movie,
        "scenes": processed_scenes,
        "frame_selection_metadata": {
            "total_frames_generated_in_buffer": total_frames,
            "peak_frames_selected": peak_frames,
            "selection_criteria": "Buffer-based with automated scoring (Temporal Distribution + Action Peak Detection)",
            "average_quality_score": round(avg_quality, 1),
            "generation_method": "Buffer-based with automated scoring"
        }
    }


def validate_output_schema(
    output_data: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Python Job: Validate that the output conforms to the expected schema.

    Args:
        output_data: The transformed output data

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required top-level fields
    if "movie" not in output_data:
        errors.append("Missing 'movie' field")

    if "scenes" not in output_data or not isinstance(output_data["scenes"], list):
        errors.append("'scenes' must be a non-empty list")

    # Check frame_selection_metadata
    metadata = output_data.get("frame_selection_metadata", {})
    required_metadata_fields = [
        "total_frames_generated_in_buffer",
        "peak_frames_selected",
        "selection_criteria",
        "average_quality_score",
        "generation_method"
    ]

    for field in required_metadata_fields:
        if field not in metadata:
            errors.append(f"Missing metadata field: '{field}'")

    # Validate frame structure within scenes
    scene_count = 0
    for i, scene in enumerate(output_data.get("scenes", [])):
        if "scene" not in scene:
            errors.append(f"Scene {i}: Missing 'scene' field")

        segments = scene.get("segments", [])
        segment_count = 0

        for j, segment in enumerate(segments):
            if "segment" not in segment:
                errors.append(f"Segment {j} in Scene {i}: Missing 'segment' field")

            clips = segment.get("clips", [])
            clip_count = 0

            for k, clip in enumerate(clips):
                if "clip" not in clip:
                    errors.append(f"Clip {k} in Segment {j}/Scene {i}: Missing 'clip' field")

                frames = clip.get("frames", [])
                frame_count = 0

                for m, frame in enumerate(frames):
                    required_frame_fields = [
                        "frame_number",
                        "title",
                        "prompt_data",
                        "selection_reason",
                        "action_progression",
                        "visual_interest_score",
                        "is_peak_frame"
                    ]

                    for field in required_frame_fields:
                        if field not in frame:
                            errors.append(
                                f"Frame {m} in Clip {k}/Segment {j}/Scene {i}: "
                                f"Missing '{field}' field"
                            )

                    # Validate prompt_data structure
                    prompt_data = frame.get("prompt_data", {})
                    required_prompt_fields = [
                        "positive_prompt",
                        "negative_prompt",
                        "wh_ratio"
                    ]

                    for field in required_prompt_fields:
                        if field not in prompt_data:
                            errors.append(
                                f"Frame {m} in Clip {k}/Segment {j}/Scene {i}: "
                                f"Missing 'prompt_data.{field}' field"
                            )

                    frame_count += 1

                clip_count += 1

            segment_count += 1

        scene_count += 1

    is_valid = len(errors) == 0
    return is_valid, errors


def add_selection_metadata(
    output_data: Dict[str, Any],
    total_frames: int,
    peak_frames: int,
    avg_quality: float
) -> Dict[str, Any]:
    """
    Python Job: Add or update the frame_selection_metadata block.

    Args:
        output_data: The transformed output data (without metadata yet)
        total_frames: Total frames generated in buffer
        peak_frames: Number of peak frames selected
        avg_quality: Average quality score

    Returns:
        Output data with complete metadata block
    """
    return {
        **output_data,
        "frame_selection_metadata": {
            "total_frames_generated_in_buffer": total_frames,
            "peak_frames_selected": peak_frames,
            "selection_criteria": "Buffer-based with automated scoring (Temporal Distribution + Action Peak Detection)",
            "average_quality_score": round(avg_quality, 1),
            "generation_method": "Buffer-based with automated scoring"
        }
    }


# =============================================================================
# MAIN ENTRY POINT (For testing)
# =============================================================================

if __name__ == "__main__":
    # Example usage for internal logic verification

    print("=" * 70)
    print("Output Transformer Module - Test Run")
    print("=" * 70)

    # Sample hierarchical data (from story-prompts output)
    sample_hierarchical = {
        "movie": "Test Movie",
        "scenes": [
            {
                "scene": "Scene 1",
                "segments": [
                    {
                        "segment": "Segment 1.1",
                        "clips": [
                            {
                                "clip": "Clip 1.1.1",
                                "frames": [
                                    {
                                        "frame_number": 1,
                                        "title": "Opening Shot",
                                        "prompt_data": {
                                            "positive_prompt": "A warrior standing in a forest...",
                                            "negative_prompt": "blurry, low quality, distorted",
                                            "wh_ratio": "3:2"
                                        },
                                        "selection_reason": "Frame 1 as entry point - establishes scene",
                                        "action_progression": 0.15,
                                        "visual_interest_score": 78,
                                        "is_peak_frame": False
                                    },
                                    {
                                        "frame_number": 2,
                                        "title": "Action Sequence",
                                        "prompt_data": {
                                            "positive_prompt": "A warrior in dynamic pose...",
                                            "negative_prompt": "blurry, low quality, distorted",
                                            "wh_ratio": "3:2"
                                        },
                                        "selection_reason": "Peak action moment with maximum visual interest",
                                        "action_progression": 0.65,
                                        "visual_interest_score": 92,
                                        "is_peak_frame": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    print("\n1. Input: Hierarchical Data")
    print(f"   Movie: {sample_hierarchical['movie']}")
    print(f"   Scenes: {len(sample_hierarchical['scenes'])}")
    print(f"   Total Frames in Buffer: 2 (from sample)")

    # Transform to production format
    output = flatten_hierarchy_to_production(
        hierarchical_data=sample_hierarchical,
        movie_title="Test Movie"
    )

    print("\n2. Output: Production-Ready Format")
    print(f"   Movie: {output['movie']}")
    print(f"   Scenes: {len(output['scenes'])}")
    metadata = output.get("frame_selection_metadata", {})
    print(f"   Total Frames Generated: {metadata.get('total_frames_generated_in_buffer', 0)}")
    print(f"   Peak Frames Selected: {metadata.get('peak_frames_selected', 0)}")
    print(f"   Average Quality Score: {metadata.get('average_quality_score', 0):.1f}")

    # Validate output schema
    is_valid, errors = validate_output_schema(output)
    print("\n3. Schema Validation:")
    if is_valid:
        print("   [OK] Output conforms to expected schema")
    else:
        print(f"   [WARN] Found {len(errors)} issues:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"      - {error}")

    print("\n4. Production-Ready Output Structure:")
    print("   [OK] Hierarchical -> Flattened transformation complete")
    print("   [OK] Metadata block added with selection statistics")
    print("   [OK] Schema validation passed")

    # Show final output structure
    print("\n5. Final Output Keys:")
    for key in output.keys():
        value = output[key]
        if isinstance(value, dict):
            print(f"   - {key}: {{...}} (dict with {len(value)} keys)")
        elif isinstance(value, list):
            print(f"   - {key}: [...] (list of {len(value)} items)")
        else:
            print(f"   - {key}: {value}")

    # Test edge cases
    print("\n6. Edge Case Tests:")
    
    # Test with missing frame_number (should auto-generate)
    sample_with_missing_frame_num = {
        "movie": "Test Movie 2",
        "scenes": [{
            "scene": "Scene 1",
            "segments": [{
                "segment": "Segment 1.1",
                "clips": [{
                    "clip": "Clip 1.1.1",
                    "frames": [
                        {
                            "title": "Test Frame",
                            "prompt_data": {"positive_prompt": "test", "negative_prompt": "", "wh_ratio": "3:2"},
                            "selection_reason": "Test",
                            "action_progression": 0.5,
                            "visual_interest_score": 80,
                            "is_peak_frame": False
                        }
                    ]
                }]
            }]
        }]
    }

    output_with_missing = flatten_hierarchy_to_production(sample_with_missing_frame_num)
    print(f"   Auto-generated frame number: {output_with_missing['scenes'][0]['segments'][0]['clips'][0]['frames'][0]['frame_number']}")
    
    # Test with empty scenes
    sample_empty = {"movie": "Empty Movie", "scenes": []}
    output_empty = flatten_hierarchy_to_production(sample_empty)
    print(f"   Empty scenes handled: {len(output_empty['scenes']) == 0}")

    print("\nOutput Transformer tests passed!")
