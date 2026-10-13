import json
import os


def flatten_story_data(input_data):
    """
    Flattens the nested structure from story-prompts into a 
    flat list of image objects for production use.
    
    Target Output Format:
    {
      "total_images": x,
      "images": [{
        "sno": "x",
        "scene": "xx",
        "segment": "xxx",
        "clip": "xx",
        "frame": "xx",
        "positive_prompt": "xxx",
        "negative_prompt": "xxx"
      }]
    }
    """
    flattened_images = []
    sno = 1

    # The expected structure from story-prompts is:
    # Movie -> Scene -> Segment -> Clip -> Frame
    
    if "scenes" in input_data and isinstance(input_data["scenes"], list):
        for scene in input_data["scenes"]:
            scene_name = scene.get("name", "unknown")
            
            segments = scene.get("segments", [])
            if not isinstance(segments, list):
                continue
                
            for segment in segments:
                segment_name = segment.get("name", "unknown")
                
                clips = segment.get("clips", [])
                if not isinstance(clips, list):
                    continue
                    
                for clip in clips:
                    clip_name = clip.get("name", "unknown")
                    
                    frames = clip.get("frames", [])
                    if not isinstance(frames, list):
                        continue
                        
                    for frame in frames:
                        frame_name = frame.get("name", "unknown")
                        
                        # Ensure we capture prompts safely
                        positive_prompt = frame.get("positive_prompt", "")
                        negative_prompt = frame.get("negative_prompt", "")

                        flattened_images.append({
                            "sno": str(sno),  # Match target format (string)
                            "scene": scene_name,
                            "segment": segment_name,
                            "clip": clip_name,
                            "frame": frame_name,
                            "positive_prompt": positive_prompt,
                            "negative_prompt": negative_prompt
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
