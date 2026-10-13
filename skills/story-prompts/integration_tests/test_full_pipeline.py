"""
End-to-End Integration Test for Story-Prompts Modular Pipeline
Flow: Raw Data -> StructureBuilder -> ScoringEngine -> SelectionOptimizer -> BufferManager -> BufferValidator -> OutputTransformer
"""

import sys
from os.path import dirname, abspath
# Ensure the project root is in the path
sys.path.insert(0, abspath(dirname(abspath(__file__)) + "/.."))

# Import functional components
from scripts.structure_builder import build_story_hierarchy 
from scripts.scoring_engine import calculate_batch_scores
from scripts.selection_optimizer import optimize_frame_selection
from scripts.buffer_manager_v2 import initialize_buffer, add_frame_to_buffer, get_buffer_data
from scripts.buffer_validator import validate_buffer_comprehensive
from scripts.output_transformer import flatten_hierarchy_to_production # FIXED NAME

def run_integration_test():
    print("🚀 Starting End-to-End Integration Test...\n")

    # 1. INPUT DATA: Raw frame data as received from the Agent
    raw_data = [
        {"id": "f1", "movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C1", "frame_id": "f1", "action": 90, "visual": 80, "light": 70, "comp": 80, "narr": 90, "timestamp": 0.5},
        {"id": "f2", "movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C1", "frame_id": "f2", "action": 95, "visual": 95, "light": 90, "comp": 90, "narr": 95, "timestamp": 1.2},
        {"id": "f3", "movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C1", "frame_id": "f3", "action": 70, "visual": 60, "light": 60, "comp": 70, "narr": 60, "timestamp": 2.0},
        {"id": "f4", "movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C2", "frame_id": "f4", "action": 80, "visual": 80, "light": 80, "comp": 80, "narr": 80, "timestamp": 0.5},
        {"id": "f5", "movie_id": "M1", "scene_id": "S1", "segment_id": "Seg1", "clip_id": "C2", "frame_id": "f5", "action": 98, "visual": 98, "light": 95, "comp": 95, "narr": 98, "timestamp": 1.5},
    ]

    # 2. STRUCTURE BUILDER: Organize raw data into hierarchy
    print("Step 1: Structuring Data...")
    hierarchy = build_story_hierarchy(raw_data)
    assert "movies" in hierarchy, "Hierarchy failed to build"
    print("✅ Structure built successfully.")

    # 3. SCORING ENGINE: Calculate weighted scores
    print("Step 2: Scoring Frames...")
    scoring_input = []
    for f in raw_data:
        scoring_input.append({
            "id": f["id"],
            "frame_id": f["frame_id"],
            "timestamp": f["timestamp"],
            "action_completeness": f["action"],
            "visual_interest": f["visual"],
            "lighting_quality": f["light"],
            "composition": f["comp"],
            "narrative_significance": f["narr"]
        })
    
    scored_frames, summary = calculate_batch_scores(scoring_input)
    assert len(scored_frames) == len(raw_data), "Scoring dropped frames"
    print(f"✅ Scoring complete. Avg Score: {summary['avg_score']:.2f}")

    # 4. SELECTION OPTIMIZER: Pick the peak frames
    print("Step 3: Optimizing Selection...")
    optimization_report = optimize_frame_selection(scored_frames, min_score_threshold=85.0, target_duration_seconds=2.5)
    optimized_frames = optimization_report["selected_frames"]
    
    assert len(optimized_frames) > 0, "Optimizer failed to select any frames"
    print(f"✅ Selection optimized. Picked {len(optimized_frames)} frames.")

    # 5. BUFFER MANAGER: Save selected frames
    print("Step 4: Buffering Frames...")
    clip_title = "Integration_Test_Clip"
    initialize_buffer(clip_title)
    for frame in optimized_frames:
        frame_id = frame.get("id") or frame.get("frame_id")
        try:
            frame_num = int(''.join(filter(str.isdigit, frame_id)))
        except:
            frame_num = 0
            
        add_frame_to_buffer(
            frame_number=frame_num, 
            title=f"Frame {frame_id}", 
            prompt_data={"positive_prompt": "High quality cinematic shot", "negative_prompt": "blurry", "wh_ratio": "3:2"},
            clip_title=clip_title
        )
    print("✅ Frames buffered.")

    # 6. BUFFER VALIDATOR: Ensure integrity before final export
    print("Step 5: Validating Buffer...")
    buffer_data = get_buffer_data(clip_title)
    is_valid, errors = validate_buffer_comprehensive(buffer_data)
    assert is_valid, f"Buffer validation failed: {errors}"
    print("✅ Buffer integrity verified.")

    # 7. OUTPUT TRANSFORMER: Final packaging
    print("Step 6: Transforming Output...")
    # The transformer expects a hierarchical format. 
    # For the integration test, we use the buffer data we just validated.
    final_output = flatten_hierarchy_to_production(buffer_data, movie_title="Integration Test Movie")
    assert "movie" in final_output, "Transformation failed"
    print("✅ Final output packaged.")

    print("\n🎉 INTEGRATION TEST PASSED: Pipeline is fully operational!")

if __name__ == "__main__":
    try:
        run_integration_test()
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
