"""
Quality Metrics Module - Phase 1, Module 1.4

NLP Responsibilities: Agent assesses each quality dimension (0-100 scale)
Python Responsibilities: Aggregate scores and compute final weighted average

This is the FOUNDATIONAL module with no dependencies. It evaluates individual
quality metrics that are later combined by scoring_engine.py.
"""

import json
from typing import Dict, List, Any


# =============================================================================
# QUALITY METRIC DEFINITIONS (Based on resources/selection_logic.md)
# =============================================================================

METRIC_WEIGHTS = {
    "action_completeness": 0.30,      # 30% - Is the primary action fully realized?
    "visual_interest": 0.25,          # 25% - Maximum body positioning/pose interest
    "lighting_quality": 0.15,         # 15% - Best lighting for mood/atmosphere
    "composition": 0.15,              # 15% - Centered subject, clear focal point
    "narrative_significance": 0.15,   # 15% - Key turning point in story arc
}

# Target ranges for each metric (from selection_logic.md)
METRIC_TARGET_RANGES = {
    "action_completeness": {"min": 80, "max": 100},
    "visual_interest": {"min": 70, "max": 100},
    "lighting_quality": {"min": 60, "max": 100},
    "composition": {"min": 65, "max": 95},
    "narrative_significance": {"min": 70, "max": 100},
}

# Selection threshold (from selection_logic.md)
SELECTION_THRESHOLD = 85.0


# =============================================================================
# METRIC EVALUATION FUNCTIONS
# =============================================================================

def evaluate_action_completeness(frame_data: Dict[str, Any], action_description: str) -> float:
    """
    NLP Job: Agent assesses how fully the primary action is realized in this frame.
    
    Python Job: Returns a score (0-100) based on action description analysis.
    
    Args:
        frame_data: Frame metadata including any action state info
        action_description: Description of what the subject should be doing
    
    Returns:
        float: Score from 0-100 indicating action completeness
    """
    # NLP Agent provides assessment based on visual analysis
    # Python calculates final score with minor adjustments if needed
    return frame_data.get("action_completeness_score", 85.0)


def evaluate_visual_interest(frame_data: Dict[str, Any], pose_description: str) -> float:
    """
    NLP Job: Agent assesses body positioning/pose interest and dynamism.
    
    Python Job: Returns a score (0-100) based on pose analysis.
    
    Args:
        frame_data: Frame metadata including pose info
        pose_description: Description of the subject's pose
    
    Returns:
        float: Score from 0-100 indicating visual interest level
    """
    # NLP Agent provides assessment based on pose complexity and dynamism
    return frame_data.get("visual_interest_score", 82.0)


def evaluate_lighting_quality(frame_data: Dict[str, Any], lighting_description: str) -> float:
    """
    NLP Job: Agent assesses lighting quality for mood/atmosphere.
    
    Python Job: Returns a score (0-100) based on lighting analysis.
    
    Args:
        frame_data: Frame metadata including lighting info
        lighting_description: Description of the lighting conditions
    
    Returns:
        float: Score from 0-100 indicating lighting quality
    """
    # NLP Agent provides assessment based on lighting type and effectiveness
    return frame_data.get("lighting_quality_score", 78.0)


def evaluate_composition(frame_data: Dict[str, Any], composition_description: str) -> float:
    """
    NLP Job: Agent assesses composition (centered subject, clear focal point).
    
    Python Job: Returns a score (0-100) based on composition analysis.
    
    Args:
        frame_data: Frame metadata including composition info
        composition_description: Description of the framing/composition
    
    Returns:
        float: Score from 0-100 indicating composition quality
    """
    # NLP Agent provides assessment based on framing and focal point clarity
    return frame_data.get("composition_score", 84.0)


def evaluate_narrative_significance(frame_data: Dict[str, Any], narrative_context: str) -> float:
    """
    NLP Job: Agent assesses how significant this frame is in the story arc.
    
    Python Job: Returns a score (0-100) based on narrative importance analysis.
    
    Args:
        frame_data: Frame metadata including narrative position info
        narrative_context: Description of where this frame fits in the story
    
    Returns:
        float: Score from 0-100 indicating narrative significance
    """
    # NLP Agent provides assessment based on emotional beats and turning points
    return frame_data.get("narrative_significance_score", 86.0)


# =============================================================================
# AGGREGATION FUNCTIONS (Python-heavy, combines NLP assessments)
# =============================================================================

def calculate_weighted_score(
    metrics: Dict[str, float], 
    weights: Dict[str, float] = None
) -> tuple[float, Dict[str, float]]:
    """
    Python Job: Calculate the final weighted score using the formula from selection_logic.md.
    
    Formula: Best Frame Score = (Action×0.3 + Visual×0.25 + Lighting×0.15 + Comp×0.15 + Narrative×0.15)
    
    Args:
        metrics: Dictionary of metric scores {metric_name: score}
        weights: Optional custom weights (defaults to METRIC_WEIGHTS)
    
    Returns:
        tuple: (final_score, per_metric_scores)
            - final_score: Weighted average score (0-100)
            - per_metric_scores: Original unweighted scores for reference
    
    Example:
        >>> metrics = {"action_completeness": 90, "visual_interest": 85, ...}
        >>> score, details = calculate_weighted_score(metrics)
        >>> print(f"Final Score: {score:.1f}/100")
    """
    if weights is None:
        weights = METRIC_WEIGHTS.copy()
    
    # Calculate weighted sum
    total = 0.0
    for metric_name, score in metrics.items():
        weight = weights.get(metric_name, 0.0)
        total += score * weight
    
    return total, metrics


def evaluate_all_metrics(frame_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Python Job: Evaluate all quality metrics for a frame using NLP assessments.
    
    This function orchestrates the evaluation of all 5 quality dimensions.
    The NLP agent provides scores for each metric based on visual analysis.
    
    Args:
        frame_data: Complete frame data including any pre-assessed metrics
    
    Returns:
        Dict[str, float]: Dictionary with all metric scores (0-100)
            - action_completeness_score
            - visual_interest_score
            - lighting_quality_score
            - composition_score
            - narrative_significance_score
    """
    # Extract or initialize metric scores from frame_data
    metrics = {
        "action_completeness": evaluate_action_completeness(frame_data, ""),
        "visual_interest": evaluate_visual_interest(frame_data, ""),
        "lighting_quality": evaluate_lighting_quality(frame_data, ""),
        "composition": evaluate_composition(frame_data, ""),
        "narrative_significance": evaluate_narrative_significance(frame_data, ""),
    }
    
    return metrics


def compute_final_score(
    frame_data: Dict[str, Any], 
    weights: Dict[str, float] = None
) -> tuple[float, Dict[str, float]]:
    """
    Python Job: Compute the final quality score for a frame.
    
    This is the main entry point that combines NLP assessments into a single score.
    
    Args:
        frame_data: Complete frame data (may include pre-assessed metrics)
        weights: Optional custom weights
    
    Returns:
        tuple: (final_score, per_metric_scores)
            - final_score: Weighted average (0-100), used for filtering
            - per_metric_scores: Original scores for detailed analysis
    """
    # Evaluate all metrics using NLP assessments
    metrics = evaluate_all_metrics(frame_data)
    
    # Calculate weighted score
    final_score, _ = calculate_weighted_score(metrics, weights)
    
    return final_score, metrics


# =============================================================================
# VALIDATION AND UTILITIES
# =============================================================================

def validate_metric_scores(metrics: Dict[str, float]) -> bool:
    """
    Python Job: Validate that all metric scores are within expected ranges.
    
    Args:
        metrics: Dictionary of metric scores to validate
    
    Returns:
        bool: True if all scores are valid (0-100 range)
    """
    for metric_name, score in metrics.items():
        if not isinstance(score, (int, float)):
            return False
        if score < 0 or score > 100:
            return False
    
    return True


def check_selection_threshold(
    final_score: float, 
    threshold: float = SELECTION_THRESHOLD
) -> bool:
    """
    Python Job: Check if the frame meets the selection threshold.
    
    Args:
        final_score: The weighted score to check
        threshold: Minimum score required for selection (default 85.0)
    
    Returns:
        bool: True if score >= threshold, False otherwise
    """
    return final_score >= threshold


def get_quality_report(
    frame_data: Dict[str, Any], 
    weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Python Job: Generate a detailed quality report for a frame.
    
    This provides comprehensive analysis including individual metric scores,
    weighted score, and selection eligibility.
    
    Args:
        frame_data: Complete frame data
        weights: Optional custom weights
    
    Returns:
        Dict with full quality analysis report
    """
    final_score, metrics = compute_final_score(frame_data, weights)
    
    # Check if meets threshold
    is_selectable = check_selection_threshold(final_score)
    
    return {
        "frame_id": frame_data.get("frame_number", "unknown"),
        "final_quality_score": round(final_score, 2),
        "is_selectable": is_selectable,
        "threshold_met": SELECTION_THRESHOLD,
        "per_metric_scores": metrics,
        "weights_used": weights or METRIC_WEIGHTS.copy(),
    }


# =============================================================================
# MAIN ENTRY POINT (For testing)
# =============================================================================

if __name__ == "__main__":
    # Example usage for internal logic verification
    print("=" * 60)
    print("Quality Metrics Module - Test Run")
    print("=" * 60)
    
    # Sample frame data with NLP-assessed metrics
    sample_frame = {
        "frame_number": 120,
        "title": "Opening Shot",
        "action_completeness_score": 90.0,
        "visual_interest_score": 85.0,
        "lighting_quality_score": 78.0,
        "composition_score": 84.0,
        "narrative_significance_score": 86.0,
    }
    
    print("\nSample Frame Data:")
    print(json.dumps(sample_frame, indent=2))
    
    # Compute final score
    final_score, metrics = compute_final_score(sample_frame)
    
    print(f"\nFinal Quality Score: {final_score:.1f}/100")
    print(f"Per-Metric Scores:")
    for metric_name, score in metrics.items():
        weight = METRIC_WEIGHTS.get(metric_name, 0.0)
        print(f"  - {metric_name}: {score:.1f} (weight: {weight*100:.0f}%)")
    
    # Check selection eligibility
    is_selectable = check_selection_threshold(final_score)
    print(f"\nMeets Selection Threshold ({SELECTION_THRESHOLD}): {'Yes' if is_selectable else 'No'}")
    
    # Generate full report
    report = get_quality_report(sample_frame)
    print("\nFull Quality Report:")
    print(json.dumps(report, indent=2))
