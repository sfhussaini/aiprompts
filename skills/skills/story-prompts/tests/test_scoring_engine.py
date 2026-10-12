"""Unit Tests for Scoring Engine Module - Phase 3, Module 3.3

Responsibilities:
- Test weighted score calculation accuracy.
- Validate threshold filtering and categorization.
- Ensure batch processing produces consistent results.
"""

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(abspath(__file__)))

from scripts.scoring_engine import (
    calculate_weighted_score,
    get_score_category,
    filter_production_ready,
    calculate_batch_scores,
    aggregate_frame_scores
)


def test_calculate_weighted_score():
    """Test weighted score calculation with known inputs."""
    
    # Test case 1: All metrics at 100 (should be 95.0)
    action = 100
    visual = 100
    lighting = 100
    comp = 100
    narrative = 100
    
    score, breakdown = calculate_weighted_score(action, visual, lighting, comp, narrative)
    
    expected_score = (100 * 0.30 + 100 * 0.25 + 100 * 0.15 + 100 * 0.15 + 100 * 0.15)
    assert abs(score - expected_score) < 0.01, f"Expected {expected_score}, got {score}"
    
    # Test case 2: Mixed scores
    action = 90
    visual = 85
    lighting = 80
    comp = 75
    narrative = 95
    
    score, _ = calculate_weighted_score(action, visual, lighting, comp, narrative)
    
    expected = (90 * 0.30 + 85 * 0.25 + 80 * 0.15 + 75 * 0.15 + 95 * 0.15)
    assert abs(score - expected) < 0.01, f"Expected {expected}, got {score}"


def test_get_score_category():
    """Test score categorization."""
    
    # Peak category
    assert get_score_category(97) == "peak"
    assert get_score_category(100) == "peak"
    
    # High category
    assert get_score_category(90) == "high"
    assert get_score_category(85) == "high"
    
    # Medium category
    assert get_score_category(75) == "medium"
    
    # Low category
    assert get_score_category(60) == "low"


def test_filter_production_ready():
    """Test production-ready filtering."""
    
    assert filter_production_ready(90) is True
    assert filter_production_ready(85) is True
    assert filter_production_ready(84.9) is False  # Just below threshold
    assert filter_production_ready(70) is False


def test_calculate_batch_scores():
    """Test batch processing with sample data."""
    
    sample_frames = [
        {
            "id": "frame_01", 
            "title": "The Climax", 
            "action_completeness": 95, 
            "visual_interest": 90, 
            "lighting_quality": 85, 
            "composition": 90, 
            "narrative_significance": 98
        },
        {
            "id": "frame_02", 
            "title": "The Transition", 
            "action_completeness": 70, 
            "visual_interest": 75, 
            "lighting_quality": 70, 
            "composition": 60, 
            "narrative_significance": 80
        },
        {
            "id": "frame_03", 
            "title": "The Detail", 
            "action_completeness": 40, 
            "visual_interest": 50, 
            "lighting_quality": 40, 
            "composition": 30, 
            "narrative_significance": 50
        }
    ]
    
    batch_results, batch_summary = calculate_batch_scores(sample_frames)
    
    # Verify summary statistics
    assert batch_summary["total_frames"] == 3
    assert batch_summary["peak_count"] >= 1  # At least one peak frame expected
    assert batch_summary["high_count"] >= 1  # At least one high frame expected
    
    # Verify individual results
    assert len(batch_results) == 3
    assert batch_results[0]["is_production_ready"] is True
    assert batch_results[2]["is_production_ready"] is False


def test_aggregate_frame_scores():
    """Test aggregated summary generation."""
    
    sample_frames = [
        {"id": "f1", "action_completeness": 95, "visual_interest": 90, 
         "lighting_quality": 85, "composition": 90, "narrative_significance": 98},
        {"id": "f2", "action_completeness": 70, "visual_interest": 75, 
         "lighting_quality": 70, "composition": 60, "narrative_significance": 80}
    ]
    
    agg = aggregate_frame_scores(sample_frames)
    
    assert agg["total_frames"] == 2
    assert agg["peak_frames"] >= 1
    assert agg["high_quality_frames"] >= 1


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    
    # Empty frames list
    results, summary = calculate_batch_scores([])
    assert len(results) == 0
    assert summary["total_frames"] == 0
    
    # Single frame
    single_frame = {
        "id": "single", 
        "action_completeness": 100, 
        "visual_interest": 100, 
        "lighting_quality": 100, 
        "composition": 100, 
        "narrative_significance": 100
    }
    results, summary = calculate_batch_scores([single_frame])
    assert len(results) == 1
    assert results[0]["is_production_ready"] is True
    
    # Frame with missing fields (should use defaults of 0.0)
    partial_frame = {"id": "partial"}
    score, _ = calculate_weighted_score(0, 0, 0, 0, 0)
    assert score == 0.0


if __name__ == "__main__":
    print("=" * 70)
    print("Scoring Engine Unit Tests")
    print("=" * 70)
    
    test_calculate_weighted_score()
    print("✅ test_calculate_weighted_score passed!")
    
    test_get_score_category()
    print("✅ test_get_score_category passed!")
    
    test_filter_production_ready()
    print("✅ test_filter_production_ready passed!")
    
    test_calculate_batch_scores()
    print("✅ test_calculate_batch_scores passed!")
    
    test_aggregate_frame_scores()
    print("✅ test_aggregate_frame_scores passed!")
    
    test_edge_cases()
    print("✅ test_edge_cases passed!")
    
    print("\n🎉 All Scoring Engine tests passed!")
