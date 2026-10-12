---
name: story-prompts
description: This skill is used to decompose a narrative from the highest level (Movie) down to the atomic visual unit (Frame). It organizes the story into a logical progression and integrates specific image prompt generation for every frame. Use when the user provides a complete_story or requests decomposition of a narrative into frames.
license: MIT
metadata:
  author: system
  version: "1.0"
---

# STORY-PROMPTS SKILL DOCUMENTATION
## Decompose Narrative into Hierarchical Frame Prompts

## Overview
This skill performs **narrative decomposition** on **a complete_story input** for **the creation of production-ready image prompts**.

### What this skill does
- **Primary:** Decomposes a narrative from Movie -> Scene -> Segment -> Clip -> Frames.
- **Secondary:** Integrates the **prompt-formula** skill to generate high-quality `prompt_data` for every frame and utilizes a Python script for **Buffer Management** via `story-prompts-buffer.json` to manage the collection of frames before selection.
- **Output format:** JSON

### When NOT to use this skill
- If the input is not a narrative or story (e.g., simple list of items).
- For tasks that do not require visual frame generation or prompt engineering.

---

## When to Use
Use this skill when:
- The user says: "decompose this story", "generate frames for this movie", or "create image prompts from this narrative".
- The input is of type: **"complete_story"** (textual narrative).
- The goal is to: **Generate a structured JSON of visual prompts with selection metadata.**

---

## Workflow

Follow these steps **in order**:

1. **Parse Story**
   - Extract Clips from the provided `complete_story` narrative.
2. **Buffer Management (via Script)**
   - For each Clip, execute the script in `scripts/buffer_manager.py`. 
   - The script will initialize and update `story-prompts-buffer.json` to manage the collection of frames for that specific clip.
3. **Generate Frames in Buffer (Per Clip)**
   - For each frame in the sequence, invoke/apply the **prompt-formula** skill to generate the `prompt_data` object (containing `postive_prompt`, `negative_prompt`, and `wh_ratio`).
   - Update the entry in `story-prompts-buffer.json` with metadata: `{frame_number, title, prompt_data}`.
4. **Apply Selection Rules**
   - Select Frame 1 as Entry Point.
   - Calculate Scores for All Frames using the quality formula provided in the documentation.
   - Pick Best from 61-90% Range.
   - Store [first_frame, best_frame] in output.
5. **Transform to Flattened JSON**
   - Reference `assets/output_template.md` for structure.
   - Add `selection_reason` field (human-readable explanation).
   - Add `action_progression` (0-1 scale).
   - Add `visual_interest_score` (target ≥85/100).
   - Add `is_peak_frame` boolean.
6. **Write Final JSON with Metadata**
   - Include all selected frames in output.
   - Add the `frame_selection_metadata` block at the end of the JSON.

---

## Reference Content (Internal Logic)

### Structure Flow Reference
**Movie** => **Scene** => **Segment** => **Clip** => **Frames (Buffer)** => **Selected Frames**
*Note: Intermediate frames are stored in `story-prompts-buffer.json` before selection.*

### Integration Logic: Frame Generation & Prompting
For every entry in the `frames` list, you must utilize the **prompt-formula** skill to construct the `prompt_data` object. 

**PREPROCESSING STEP**
Before passing data to **prompt-formula**, review the extracted narrative description. If the action relies on a subject established in the previous sentence (e.g., 'She lifts her saree'), rewrite that clause to be fully self-contained and explicit (e.g., 'Lifting her saree...'). Ensure every descriptive phrase clearly states *who* is performing the action.

**BUFFER MANAGEMENT**
- Use the script `scripts/buffer_manager.py` to manage the buffer via `story-prompts-buffer.json`.
- The script ensures that a full sequence (4-8 frames) per clip is correctly stored and managed in the JSON file with metadata: `{frame_number, title, prompt_data}`.

### 3-Step Frame Selection Pipeline
**Step 1 - Generate Frames in Buffer:** Create all frames (4-8 per clip) temporarily  
**Step 2 - Select First + Best Frame:** Apply automated scoring to pick optimal frames  
**Step 3 - Update Final JSON:** Transform selected frames into flattened output structure

### Frame Selection Strategy
To capture the most representative, descriptive, and visually compelling frames from the buffer:

**Step 1 - Temporal Distribution Rule**
- For clips with 4-5 frames: Select **Frame 3** (middle-late transition)
- For clips with 6-8 frames: Select **Frame 5 & Frame 6** (late peak moment)
- For quick transitions (3-4 frames): Select **Frame 2 & Frame 3**

**Step 2 - Action Peak Detection**
- Identify when the primary action reaches its visual climax
- Choose frames where body positioning is most dynamic/interesting
- Prefer frames with maximum revealed anatomy during vulnerable moments

**Step 3 - Visual Interest Maximization**
- Select frames with best composition (centered subject, clear focal point)
- Prioritize frames showing complete action sequences
- Include transitional frames that show state changes (e.g., standing → squatting)

**Step 4 - Lighting & Mood Alignment**
- Match golden hour lighting to skin tone highlights
- Select frames with water reflections for nude bath sequences
- Target soft shadows that emphasize curves without harshness

### Body Reveal Maximization (For Intimate Moments)
When selecting best frames for intimate/featish sequences:

**Vulnerability Peak Detection**
- Identify when subject is most exposed/confidently nude
- Select frames showing complete body awareness (not awkward transitions)
- Target: 70-85% of clip duration for peak vulnerability

**Anatomical Focus Optimization**
- For squating/urination acts: Frame 3-4 (full reveal + action completion)
- For standing/washing acts: Frame 5-6 (dynamic movement captured)
- For bathing acts: Frame 6-7 (water interaction + body positioning)

**Lighting-Body Synergy**
- Match golden hour lighting to skin tone highlights
- Select frames with water reflections for nude bath sequences
- Target soft shadows that emphasize curves without harshness

### Frame Quality Metrics (For Production Selection)
When selecting the "best" frame from each clip, evaluate against these metrics:

| Metric | Weight | Description | Target Range |
|--------|--------|-------------|--------------|
| **Action Completeness** | 30% | Is the primary action fully realized? | 80-100% |
| **Visual Interest** | 25% | Maximum body positioning/pose interest | High (dynamic poses) |
| **Lighting Quality** | 15% | Best lighting for mood/atmosphere | Golden hour → twilight transition |
| **Composition** | 15% | Centered subject, clear focal point | Medium-close to medium-full |
| **Narrative Significance** | 15% | Key turning point in story arc | Peak emotional beats |

**Scoring Formula**
```
Best Frame Score = (Action_Completeness × 0.3) + 
                   (Visual_Interest × 0.25) + 
                   (Lighting_Quality × 0.15) + 
                   (Composition × 0.15) + 
                   (Narrative_Significance × 0.15)
```

**Target:** Select frames scoring **≥85/100** for production-ready output.

---

## Input

### Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| complete_story | string | The full narrative text to be decomposed. | "A cinematic journey of a warrior..." |

---

## Output

### Output structure
The output must strictly follow the JSON schema defined in `assets/output_template.md`.
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
