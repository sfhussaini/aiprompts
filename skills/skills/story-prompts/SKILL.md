---
name: story-prompts
description: |
  This skill is used to decompose a narrative from the highest level (Movie) down to the atomic visual unit (Frame). 
  Use when the user provides a `complete_story` or requests decomposition of a narrative into frames.
license: MIT
metadata:
  author: system
  version: "1.0"
---

## 🎯 Overview

This skill performs **narrative decomposition** to achieve **the creation of production-ready image prompts**.

### Capabilities
- **Primary:** Decomposes a narrative from Movie => Scene => Segment => Clip => Frames.
- **Secondary:** Integrates the `prompt-formula` skill for high-quality `prompt_data` generation and utilizes Python scripts for Buffer Management via `story-proms-buffer.json`.
- **Output Format:** JSON

### Constraints (When NOT to use)
- If the input is not a narrative or story (e.g., simple list of items).
- For tasks that do not require visual frame generation or prompt engineering.

---

## ⚙️ Operational Workflow

The agent MUST execute these steps **sequentially**. Provide a status update to the user after each phase.

### 1. Validation Phase
- **Check:** Verify `complete_story` is present and constitutes a narrative.
- **Action:** If input is not a narrative or is missing, use `ask_question` to request a valid story.

### 2. Research & Gathering Phase
- **Tool:** Internal Logic Processing.
- **Goal:** Extract Clips from the `complete_story`.
- **Preprocessing Step:** Before passing data to `prompt-formula`, review the narrative. If an action relies on a subject established in a previous sentence (e.g., 'She lifts her saree'), rewrite it to be fully self-contained and explicit (e.g., 'Lifting her saree...'). Ensure every descriptive phrase clearly states *who* is performing the action.

### 3. Structuring Phase
- **Logic:** Organize data into a hierarchy: Movie => Scene => Segment => Clip => Frames.
- **Criteria:** Apply "Frame Selection Strategy" (Temporal Distribution, Action Peak Detection, Visual Interest Maximization, and Lighting/Mood Alignment). 
- **Scoring:** Calculate scores for all frames using the formula: `(Action_Completeness × 0.3) + (Visual_Interest × 0.25) + (Lighting_Quality × 0.15) + (Composition × 0.15) + (Narrative_Significance × 0.15)`. Target >=85/100.

### 4. Drafting Phase (Asset Integration)
- **Asset:** Use the `prompt-formula` skill to generate the `prompt_data` object (containing `postive_prompt`, `negative_prompt`, and `wh_ratio`) for every frame.
- **Action:** Map selected frames to the structure defined in `assets/output_template.md`.
- **Fields:** Populate `selection_reason`, `action_progression` (0-1), `visual_interest_score`, and `is_peak_frame`.

### 5. Processing Phase (Script Execution)
- **Script:** Execute `scripts/buffer_manager.py` via `run_commands`.
- **Command:** `python scripts/buffer_manager.py [input_path] [output_path]`
- **Validation:** Ensure the script successfully manages the `story-prompts-buffer.json` and that all frames are correctly stored before final flattening.

---

## 📥 Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| complete_story | String | Required | The full narrative text to be decomposed. | "A cinematic journey of a warrior..." |

---

## 📤 Output Specification

### Final Delivery Format
Return the final result in this JSON structure:

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
```

---

## 🛠️ Resource Map

| Resource | Path | Purpose |
|----------|------|----------|
| **Template** | `assets/output_template.md` | Provides the structural blueprint for the final JSON output. |
| **Script** | `scripts/buffer_manager.py` | Manages the collection of frames in `story-prompts-buffer.json`. |
| **Docs** | `resources/selection_logic.md` | Contains "Frame Selection Strategy", "Body Reveal Maximization" (including specific rules for squatting, urination, and bathing), and "Quality Metrics". |
```