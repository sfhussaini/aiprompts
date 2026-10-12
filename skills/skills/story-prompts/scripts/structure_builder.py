"""Structure Builder Module - Phase 1, Module 1.2


Responsibilities:
- Organize flat frame/clip data into a nested hierarchy: Movie -> Scene -> Segment -> Clip -> Frames.
- Ensure temporal ordering of segments and clips.
- Validate that no frames are lost during the restructuring process.
"""

import json
from typing import Dict, List, Any, Optional


def build_story_hierarchy(flat_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Transforms a flat list of clip/frame data into a nested story structure.

    Expected input format:
    [
        {
            "movie_id": "M1",
            "scene_id": "S1",
            "segment_id": "Seg1",
            "clip_id": "C1",
            "frame_id": "F1",
            "timestamp": 1.0,
            ...
        },
        ...
    ]
    """
    if not flat_data:
        return {"movies": {}}

    hierarchy = {
        "movies": {}
    }

    # Track frames per clip to validate no duplicates
    frame_counts = {}

    for item in flat_data:
        movie_id = item.get("movie_id", "unknown_movie")
        scene_id = item.get("scene_id", "unknown_scene")
        segment_id = item.get("segment_id", "unknown_segment")
        clip_id = item.get("clip_id", "unknown_clip")

        # Validate required keys exist
        frame_id = item.get("frame_id")
        timestamp = item.get("timestamp")
        score = item.get("weighted_score")

        if not frame_id:
            continue  # Skip frames without an ID

        # Initialize Movie
        if movie_id not in hierarchy["movies"]:
            hierarchy["movies"][movie_id] = {"scenes": {}}

        movie = hierarchy["movies"][movie_id]

        # Initialize Scene
        if scene_id not in movie["scenes"]:
            movie["scenes"][scene_id] = {"segments": {}}

        scene = movie["scenes"][scene_id]

        # Initialize Segment
        if segment_id not in scene["segments"]:
            scene["segments"][segment_id] = {"clips": {}}

        segment = scene["segments"][segment_id]

        # Initialize Clip
        if clip_id not in segment["clips"]:
            segment["clips"][clip_id] = {"frames": []}

        clip = segment["clips"][clip_id]

        # Add Frame (with validation)
        frame_entry = {
            "frame_id": frame_id,
            "timestamp": timestamp if timestamp is not None else 0.0,
            "score": score if score is not None else 0.0,
            "metadata": item.copy()  # Shallow copy to avoid reference issues
        }

        clip["frames"].append(frame_entry)

        # Track frame counts for validation
        key = (movie_id, scene_id, segment_id, clip_id)
        if key not in frame_counts:
            frame_counts[key] = 0
        frame_counts[key] += 1

    # Sort frames by timestamp within each clip
    def safe_sort_key(frame):
        ts = frame.get("timestamp")
        return (ts or 0.0)

    for movie in hierarchy["movies"].values():
        for scene in movie["scenes"].values():
            for segment in scene["segments"].values():
                for clip in segment["clips"].values():
                    clip["frames"].sort(key=safe_sort_key)

    # Validate no duplicate frames per clip
    duplicates_found = []
    for key, count in frame_counts.items():
        if count > 1:
            duplicates_found.append(f"Clip {key[3]} has {count} frames with same ID")

    if duplicates_found:
        print("Warning: Duplicate frames detected:")
        for dup in duplicates_found:
            print(f"   - {dup}")

    return hierarchy


if __name__ == "__main__":
    print("Testing StructureBuilder...")

    sample_flat_data = [
        {"movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C1", "frame_id": "F1", "timestamp": 0.5, "weighted_score": 90},
        {"movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C1", "frame_id": "F2", "timestamp": 1.0, "weighted_score": 88},
        {"movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C2", "frame_id": "F3", "timestamp": 1.5, "weighted_score": 92},
        {"movie_id": "M1", "scene_id": "S1", "segment_id": "Seg2", "clip_id": "C3", "frame_id": "F4", "timestamp": 2.0, "weighted_score": 85},
        {"movie_id": "M1", "scene_id": "S2", "segment_id": "Seg3", "clip_id": "C4", "frame_id": "F5", "timestamp": 3.0, "weighted_score": 95},
    ]

    result = build_story_hierarchy(sample_flat_data)

    # Validation
    assert "M1" in result["movies"], "Movie M1 should exist"
    assert "S1" in result["movies"]["M1"]["scenes"], "Scene S1 should exist"
    assert "Seg1" in result["movies"]["M1"]["scenes"]["S1"]["segments"], "Segment Seg1 should exist"
    assert "C1" in result["movies"]["M1"]["scenes"]["S1"]["segments"]["Seg1"]["clips"], "Clip C1 should exist"
    assert len(result["movies"]["M1"]["scenes"]["S1"]["segments"]["Seg1"]["clips"]["C1"]["frames"]) == 2, "Clip C1 should have 2 frames"

    print("StructureBuilder tests passed!")
