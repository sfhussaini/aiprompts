"""
Scoring Engine Module - Phase 1, Module 1.1

NLP Responsibilities: Agent evaluates each metric (0-100 scale) for Action Completeness, Visual Interest, Lighting Quality, Composition, Narrative Significance
Python Responsibilities: Calculate weighted average; Filter frames >=85/100; Validate score ranges; Aggregate results

This module implements the core quality scoring calculation using a weighted formula.
It takes per-metric scores from `quality_metrics.py` and produces an aggregated production-ready score.

Formula: `(Action*0.3 + Visual*0.25 + Lighting*0.15 + Comp*0.15 + Narrative*0.15)`
"""

import json
from typing import Dict, List, Any, Optional, Tuple

# =============================================================================
# SCORING CONSTANTS & CONFIGURATION
# =============================================================================

# Weighted formula constants (configurable via YAML in Phase 3)
SCORING_WEIGHTS = {
    "action_completeness": 0.30,      # 30% - How well the frame completes its intended action/beat
    "visual_interest": 0.25,          # 25% - Visual appeal and composition interest
    "lighting_quality": 0.15,         # 15% - Lighting aesthetics and mood appropriateness
    "composition": 0.15,              # 15% - Framing, rule of thirds, visual balance
    "narrative_significance": 0.15    # 15% - How well it advances the story/narrative arc
}

# Validation thresholds
MIN_SCORE_THRESHOLD = 85.0           # Minimum score for production-ready frames
MAX_SCORE_THRESHOLD = 100.0          # Maximum possible score (for validation)

# Score ranges for categorization
SCORE_RANGES = {
    "peak": (95, 100),               # Peak quality - must-include frames
    "high": (85, 94),                # High quality - strong candidates
    "medium": (70, 84),              # Medium quality - consider based on context
    "low": (50, 69),                 # Low quality - review for edge cases
    "fail": (0, 49)                  # Fail threshold - typically filtered out
}

# =============================================================================
# SCORING FUNCTIONS (Python-heavy)
# =============================================================================

def calculate_weighted_score(
    action_completeness: float,
    visual_interest: float,
    lighting_quality: float,
    composition: float,
    narrative_significance: float
) -> Tuple[float, Dict[str, Any]]:
    """
    Python Job: Calculate weighted average score from per-metric evaluations.
    """
    metrics = {
        "action_completeness": action_completeness,
        "visual_interest": visual_interest,
        "lighting_quality": lighting_quality,
        "composition": composition,
        "narrative_significance": narrative_significance
    }
    
    weighted_score = 0.0
    breakdown = {"component_scores": {}, "weights_applied": {}}
    
    for metric, weight in SCORING_WEIGHTS.items():
        score = metrics.get(metric, 0.0)
        score = max(0.0, min(100.0, score))
        weighted_score += score * weight
        breakdown["component_scores"][metric] = score
        breakdown["weights_applied"][metric] = weight
        
    return round(weighted_score, 2), breakdown

def get_score_category(score: float) -> str:
    """Returns the quality category based on the final score."""
    for category, (low, high) in SCORE_RANGES.items():
        if low <= score <= high:
            return category
    return "unknown"

def filter_production_ready(score: float) -> bool:
    """Determines if a frame meets the production threshold."""
    return score >= MIN_SCORE_THRESHOLD



def calculate_batch_scores(frames: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Processes multiple frames and generates a batch summary.
    """
    results = []
    summary = {
        "total_frames": len(frames),
        "peak_count": 0,
        "high_count": 0,
        "medium_count": 0,
        "low_count": 0,
        "fail_count": 0,
        "average_score": 0.0
    }
    
    total_aggregated_score = 0.0
    
    for frame in frames:
        score, breakdown = calculate_weighted_score(
            frame.get("action_completeness", 0.0),
            frame.get("visual_interest", 0.0),
            frame.get("lighting_quality", 0.0),
            frame.get("composition", 0.0),
            frame.get("narrative_significance", 0.0)
        )
        
        category = get_score_category(score)
        summary[f"{category}_count"] += 1
        total_aggregated_score += score
        
        results.append({
            "frame_id": frame.get("id", "unknown"),
            "weighted_score": score,
            "category": category,
            "is_production_ready": filter_production_ready(score),
            "breakdown": breakdown
        })
        
    if summary["total_frames"] > 0:
        summary["average_score"] = round(total_aggregated_score / summary["total_frames"], 2)
        
    return results, summary

def aggregate_frame_scores(frames: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generates a final aggregated summary for a set of frames."""
    _, summary = calculate_batch_scores(frames)
    
    return {
        "total_frames": summary["total_frames"],
        "peak_frames": summary["peak_count"],
        "high_quality_frames": summary["high_count"],
        "medium_quality_frames": summary["medium_count"],
        "low_quality_frames": summary["low_count"],
        "fail_frames": summary["fail_count"]
    }


if __name__ == "__main__":
    print("🧪 Testing ScoringEngine...")
    
    sample_frames = [
        {
            "id": "frame_01", "title": "The Climax", 
            "action_completeness": 95, "visual_interest": 90, 
            "lighting_quality": 85, "composition": 90, "narrative_significance": 98
        },
        {
            "id": "frame_02", "title": "The Transition", 
            "action_completeness": 70, "visual_interest": 75, 
            "lighting_quality": 70, "composition": 60, "narrative_significance": 80
        },
        {
            "id": "frame_03", "title": "The Detail", 
            "action_completeness": 40, "visual_interest": 50, 
            "lighting_quality": 40, "composition": 30, "narrative_significance": 50
        }
    ]
    
    print("\n1. Individual Score Calculation:")
    for f in sample_frames:
        score, _ = calculate_weighted_score(
            f["action_completeness"], f["visual_interest"], 
            f["lighting_quality"], f["composition"], f["narrative_significance"]
        )
        print(f"   {f['title']} ({f['id']}): Score = {score}, Category = {get_score_category(score)}, Ready = {filter_production_ready(score)}")
        
    print("\n2. Batch Processing:")
    batch_results, batch_summary = calculate_batch_scores(sample_frames)
    print(f"   Processed {batch_summary['total_frames']} frames. Average Score: {batch_summary['average_score']}")
    
    print("\n3. Aggregated Summary:")
    agg = aggregate_frame_scores(sample_frames)
    print(f"   Production Ready: {agg['production_ready_count']}/{agg['total_frames']}")
    
    assert batch_results[0]['is_production_ready'] == True, "Frame 01 should be production ready"
    assert batch_results[2]['is_production_ready'] == False, "Frame 03 should not be production ready"
    
    print("\n✅ All ScoringEngine tests passed!")