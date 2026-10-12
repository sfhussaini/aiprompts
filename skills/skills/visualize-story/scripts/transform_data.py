import json
import os

def flatten_story_data(input_data):
    """
    Flattens the nested structure from story-prompts into a 
    flat list of image objects for production use.
    """
    flattened_images = []
    sno = 1

    # The expected structure from story-prompts is:
    # Movie -> Scene -> Segment -> Clip -> Frame
    
    if "scenes" in input_data:
        for scene in input_data["scenes"]:
            scene_name = scene.get("name", "unknown")
            for segment in scene.get("segments", []):
                segment_name = segment.get("name", "unknown")
                for clip in segment.get("clips", []):
                    clip_name = clip.get("name", "unknown")
                    for frame in clip.get("frames", []):
                        frame_name = frame.get("name", "unknown")
                        
                        flattened_images.append({
                            "sno": str(sno),
                            "scene": scene_name,
                            "segment": segment_name,
                            "clip": clip_name,
                            "frame": frame_name,
                            "positive_prompt": frame.get("positive_prompt", ""),
                            "negative_prompt": frame.get("negative_prompt", "")
                        })
                        sno += 1

    return {
        "total_images": len(flattened_images),
        "images": flattened_images
    }

def main():
    # The input is the JSON output from the story-prompts skill.
    # If it's passed as a file path, we load it; otherwise, we process the data.
    input_path = "temp_prompts.json" 
    
    if not os.path.exists(input_path):
        # Fallback for cases where the input is piped or missing
        print("Warning: Input file not found. Attempting to process as raw string if available.")
        data = {"scenes": []}
    else:
        with open(input_path, 'r') as f:
            data = json.load(f)

    flattened = flatten_story_data(data)

    # Save the final consolidated file
    output_file = "story.json"
    with open(output_file, "w") as f:
        json.dump(flattened, f, indent=2)
    
    print(f"Successfully consolidated data into {output_file}")

if __name__ == "__main__":
    main()
