"""Selection Optimizer Module - Phase 1, Module 1.3


Responsibilities:
- Integrate scoring results from `scoring_engine.py`.
- Apply temporal rules (e.g., minimum frame gaps, scene transitions).
- Select peak frames for the final output while maintaining narrative flow.
"""

import json
from typing import Dict, List, Any, Optional



def apply_temporal_rules(frames: List[Dict[str, Any]], min_gap_seconds: float = 0.5) -> List[Dict[str, Any]]:
    """
    Applies temporal constraints to ensure smooth transitions between selected frames.

    Args:
        frames: List of scored frames from scoring_engine.py.
        min_gap_seconds: Minimum time gap required between consecutive frames.

    Returns:
        Filtered list of frames that meet the temporal requirements.
    """
    if not frames:
        return []

    # Sort by timestamp first, handling None timestamps gracefully
    sorted_frames = sorted(frames, key=lambda x: (x.get("timestamp") or 0))

    selected = [sorted_frames[0]]

    for frame in sorted_frames[1:]:
        last_frame = selected[-1]
        last_ts = last_frame.get("timestamp") or 0
        curr_ts = frame.get("timestamp") or 0
        
        time_gap = curr_ts - last_ts if (curr_ts is not None and last_ts is not None) else 0

        # Keep frame if it meets the minimum gap requirement
        if time_gap >= min_gap_seconds:
            selected.append(frame)

    return selected


def select_peak_frames(frames: List[Dict[str, Any]], target_count: Optional[int] = None, 
                       min_score_threshold: float = 85.0) -> List[Dict[str, Any]]:
    """
    Selects the best frames based on scoring results and temporal constraints.

    Args:
        frames: List of scored frames from scoring_engine.py.
        target_count: Optional target number of frames to select (for duration control).
        min_score_threshold: Minimum score required for a frame to be considered.

    Returns:
        Optimized list of peak frames ready for output transformation.
    """
    # Filter by minimum score threshold
    filtered_frames = [f for f in frames if f.get("weighted_score", 0) >= min_score_threshold]

    # Apply temporal rules to ensure smooth transitions
    optimized_frames = apply_temporal_rules(filtered_frames, min_gap_seconds=0.5)

    # If target count is specified, select the best frames while maintaining flow
    if target_count and len(optimized_frames) > target_count:
        # Sort by score (descending) to prioritize highest quality frames
        sorted_by_score = sorted(optimized_frames, key=lambda x: x.get("weighted_score", 0), reverse=True)

        selected = []
        for frame in sorted_by_score:
            if len(selected) >= target_count:
                break
            
            # Check if this frame adds significant value (high score or fills a time gap)
            if not selected:
                selected.append(frame)
            else:
                last_frame = selected[-1]
                last_ts = last_frame.get("timestamp") or 0
                curr_ts = frame.get("timestamp") or 0
                
                time_gap = curr_ts - last_ts if (curr_ts is not None and last_ts is not None) else 0

                # Add frame if it's high quality or fills a significant gap
                if frame.get("weighted_score", 0) >= 95 or time_gap > 1.0:
                    selected.append(frame)

        optimized_frames = selected

    return optimized_frames


def optimize_frame_selection(frames: List[Dict[str, Any]], 
                             min_score_threshold: float = 85.0,
                             target_duration_seconds: Optional[float] = None,
                             max_frames_per_scene: int = 3) -> Dict[str, Any]:
    """
    Generates a comprehensive optimization report with selected frames.

    Args:
        frames: List of scored frames from scoring_engine.py.
        min_score_threshold: Minimum score required for consideration.
        target_duration_seconds: Optional target total duration in seconds.
        max_frames_per_scene: Maximum frames to select per scene.

    Returns:
        Dictionary containing selected frames and optimization statistics.
    """
    # Filter by minimum score threshold
    filtered_frames = [f for f in frames if f.get("weighted_score", 0) >= min_score_threshold]

    # Apply temporal rules
    optimized_frames = apply_temporal_rules(filtered_frames, min_gap_seconds=0.5)

    # Calculate statistics
    total_frames = len(frames)
    filtered_count = len(filtered_frames)
    optimized_count = len(optimized_frames)

    peak_frames = [f for f in optimized_frames if f.get("weighted_score", 0) >= 95]
    high_quality_frames = [f for f in optimized_frames if 85 <= f.get("weighted_score", 0) < 95]

    # Calculate total duration
    timestamps = [f.get("timestamp") for f in optimized_frames if f.get("timestamp") is not None]
    total_duration = max(timestamps) - min(timestamps) if timestamps else 0

    result = {
        "selected_frames": optimized_frames,
        "statistics": {
            "total_input_frames": total_frames,
            "filtered_by_score": filtered_count,
            "optimized_after_temporal_rules": optimized_count,
            "peak_quality_frames": len(peak_frames),
            "high_quality_frames": len(high_quality_frames),
            "average_selected_score": sum(f.get("weighted_score", 0) for f in optimized_frames) / max(len(optimized_frames), 1),
            "total_duration_seconds": total_duration,
            "frames_per_second": optimized_count / max(total_duration, 0.001) if total_duration > 0 else optimized_count
        }
    }

    return result


if __name__ == "__main__":
    print("Testing SelectionOptimizer...")

    # Sample data from scoring_engine.py output format
    sample_frames = [
        {"frame_id": "F1", "timestamp": 0.5, "weighted_score": 92, "category": "peak"},
        {"frame_id": "F2", "timestamp": 1.0, "weighted_score": 88, "category": "high"},
        {"frame_id": "F3", "timestamp": 1.5, "weighted_score": 95, "category": "peak"},
        {"frame_id": "F4", "timestamp": 2.0, "weighted_score": 86, "category": "high"},
        {"frame_id": "F5", "timestamp": 3.0, "weighted_score": 97, "category": "peak"},
    ]

    print("\n1. Original Frames:")
    for f in sample_frames:
        print(f"   {f['frame_id']}: Score={f['weighted_score']}, Category={f['category']}")

    # Apply temporal rules first
    optimized = apply_temporal_rules(sample_frames, min_gap_seconds=0.5)
    
    print("\n2. After Temporal Rules (min_gap=0.5s):")
    for f in optimized:
        print(f"   {f['frame_id']}: Score={f['weighted_score']}")

    # Apply peak selection with target count
    selected = select_peak_frames(optimized, target_count=2)
    
    print("\n3. After Peak Selection (target_count=2):")
    for f in selected:
        print(f"   {f['frame_id']}: Score={f['weighted_score']}")

    # Full optimization report
    report = optimize_frame_selection(sample_frames, min_score_threshold=85.0, target_duration_seconds=2.5)
    stats = report["statistics"]
    
    print("\n4. Full Optimization Report:")
    print(f"   Input: {stats['total_input_frames']}, Filtered: {stats['filtered_by_score']}, Optimized: {stats['optimized_after_temporal_rules']}")
    print(f"   Peak Quality: {stats['peak_quality_frames']}, High Quality: {stats['high_quality_frames']}")
    print(f"   Avg Score: {stats['average_selected_score']:.2f}, Duration: {stats['total_duration_seconds']:.1f}s")

    # Run assertions once (removed duplicates)
    assert len(optimized) == 4, "Should have 4 frames after temporal rules (all gaps >= 0.5s)"
    assert len(selected) == 2, "Should select exactly 2 peak frames"

    print("\nSelectionOptimizer tests passed!")