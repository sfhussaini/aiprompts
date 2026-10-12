# Output Template: Story Prompt JSON Structure

The following structure must be used for the final output of the story decomposition process. Ensure all fields are populated according to the calculation logic and selection rules defined in the skill documentation.

```json
{
  "movie": "title",
  "scenes": [
    {
      "scene": "title",
      "segments": [
        {
          "segment": "title",
          "clips": [
            {
              "clip": "title",
              "frames": [
                {
                  "frame_number": 120,
                  "title": "title",
                  "prompt_data": {
                    "postive_prompt": "...",
                    "negative_prompt": "...",
                    "wh_ratio": "3:2"
                  },
                  "selection_reason": "...",
                  "action_progression": 0.65,
                  "visual_interest_score": 87,
                  "is_peak_frame": true
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "frame_selection_metadata": {
    "total_frames_generated_in_buffer": 24,
    "peak_frames_selected": 6,
    "selection_criteria": "...",
    "average_quality_score": 84.3,
    "generation_method": "Buffer-based with automated scoring"
  }
}
