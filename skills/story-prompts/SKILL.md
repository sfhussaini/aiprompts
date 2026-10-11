---
name: story-prompts
description: This skill is used to decompose a narrative from the highest level (Movie) down to the atomic visual unit (Frame). It organizes the story into a logical progression and integrates specific image prompt generation for every frame.
---


================================================================================
                    STORY-PROMPTS SKILL DOCUMENTATION
              Decompose Narrative into Hierarchical Frame Prompts
================================================================================

# 🎬 Story Decomposition Template

This skill is used to decompose a narrative from the highest level (Movie) down 
to the atomic visual unit (Frame). It organizes the story into a logical progression 
and integrates specific image prompt generation for every frame.

## Structure Flow Reference

**Movie** => **Scene** => **Segment** => **Clip** => **Frames (Buffer)** => **Selected Frames**

*Note: Intermediate frames are stored in `frames_buffer` before selection.*

---

## 🛠️ Integration Logic: Frame Generation

For every entry in the `frames` list, you must apply the logic from the **`prompt-formula`** skill. 

### PREPROCESSING STEP
Before applying @prompt-formula, review the extracted narrative description. If the action relies on a subject established in the previous sentence (e.g., 'She lifts her saree'), rewrite that clause to be fully self-contained and explicit (e.g., 'Lifting her saree...'). Ensure every descriptive phrase clearly states *who* is performing the action.

### BUFFER INITIALIZATION
- For each Clip, initialize `frames_buffer = []` before generating frames
- Generate full sequence (4-8 frames) per clip into buffer
- Store with metadata: `{frame_number, title, prompt_data}`

---

## 🔄 3-Step Frame Selection Pipeline

The skill now uses a buffer-based approach for efficient frame generation and selection:

**Step 1 - Generate Frames in Buffer:** Create all frames (4-8 per clip) temporarily  
**Step 2 - Select First + Best Frame:** Apply automated scoring to pick optimal frames  
**Step 3 - Update Final JSON:** Transform selected frames into flattened output structure  

This reduces final output from 120+ frames to 6-8 production-ready images while maintaining quality.

---

## 🎯 Frame Selection Strategy

To capture the most representative, descriptive, and visually compelling frames from the buffer:

### Step 1 - Temporal Distribution Rule
- For clips with 4-5 frames: Select **Frame 3** (middle-late transition)
- For clips with 6-8 frames: Select **Frame 5-6** (late peak moment)
- For quick transitions (3-4 frames): Select **Frame 2-3**

### Step 2 - Action Peak Detection
- Identify when the primary action reaches its visual climax
- Choose frames where body positioning is most dynamic/interesting
- Prefer frames with maximum revealed anatomy during vulnerable moments

### Step 3 - Visual Interest Maximization
- Select frames with best composition (centered subject, clear focal point)
- Prioritize frames showing complete action sequences
- Include transitional frames that show state changes (e.g., standing → squatting)

### Step 4 - Lighting & Mood Alignment
- Match golden hour lighting to skin tone highlights
- Select frames with water reflections for nude bath sequences
- Target soft shadows that emphasize curves without harshness

---

## 💃 Body Reveal Maximization (For Intimate Moments)

When selecting best frames for intimate/featish sequences:

### Vulnerability Peak Detection
- Identify when subject is most exposed/confidently nude
- Select frames showing complete body awareness (not awkward transitions)
- Target: 70-85% of clip duration for peak vulnerability

### Anatomical Focus Optimization
- For squatting/urination acts: Frame 3-4 (full reveal + action completion)
- For standing/washing acts: Frame 5-6 (dynamic movement captured)
- For bathing acts: Frame 6-7 (water interaction + body positioning)

### Lighting-Body Synergy
- Match golden hour lighting to skin tone highlights
- Select frames with water reflections for nude bath sequences
- Target soft shadows that emphasize curves without harshness

---

## 📈 Frame Quality Metrics (For Production Selection)

When selecting the "best" frame from each clip, evaluate against these metrics:

| Metric | Weight | Description | Target Range |
|--------|--------|-------------|--------------|
| **Action Completeness** | 30% | Is the primary action fully realized? | 80-100% |
| **Visual Interest** | 25% | Maximum body positioning/pose interest | High (dynamic poses) |
| **Lighting Quality** | 15% | Best lighting for mood/atmosphere | Golden hour → twilight transition |
| **Composition** | 15% | Centered subject, clear focal point | Medium-close to medium-full |
| **Narrative Significance** | 15% | Key turning point in story arc | Peak emotional beats |

### Scoring Formula
```
Best Frame Score = (Action_Completeness × 0.3) + 
                   (Visual_Interest × 0.25) + 
                   (Lighting_Quality × 0.15) + 
                   (Composition × 0.15) + 
                   (Narrative_Significance × 0.15)
```

**Target:** Select frames scoring **≥85/100** for production-ready output.

---

## 📋 Enhanced JSON Output Structure

Modify the JSON schema to include frame selection metadata and buffer tracking:

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

### New Fields Added
- `selection_reason`: Human-readable explanation for frame selection
- `action_progression`: Normalized value (0-1 scale) indicating position in clip
- `visual_interest_score`: Quality metric score (target ≥85/100)
- `is_peak_frame`: Boolean flag identifying best frames
- `frame_selection_metadata`: Top-level metadata block with buffer stats

---

## 📊 Implementation Flow Steps

The 3-step pipeline follows this flow:

### Step 1 - Parse Story
Extract Clips from narrative

### Step 2 - Generate Frames in Buffer (Per Clip)
- Initialize `frames_buffer = []`
- Generate ALL frames (4-8) per clip into buffer
- Store with metadata: `{frame_number, title, prompt_data}`

### Step 3 - Apply Selection Rules
- Select Frame 1 as Entry Point
- Calculate Scores for All Frames using quality formula
- Pick Best from 61-90% Range
- Store [first_frame, best_frame] in output

### Step 4 - Transform to Flattened JSON
- Add `selection_reason` field
- Add `action_progression` (0-1 scale)
- Add `visual_interest_score`
- Add `is_peak_frame` boolean

### Step 5 - Write Final JSON with Metadata
- Include all selected frames in output
- Add `frame_selection_metadata` block

---

## 📈 Summary of Changes to `story-prompts` Skill

| Phase | Action | Tool/Variable |
|-------|--------|---------------|
| **Generation** | Create buffer per clip | `frames_buffer = []` |
| **Scoring** | Apply quality formula | Calculate for all frames |
| **Selection** | Pick Frame 1 + Best (61-90%) | Automated selection logic |
| **Transformation** | Add metadata fields | `selection_reason`, `action_progression`, etc. |
| **Export** | Flatten to final JSON | Write only selected frames |

This creates a **production-ready pipeline** where you generate more frames than needed, then intelligently select the best ones for efficiency and quality!

---

================================================================================
                    END OF STORY-PROMPTS SKILL DOCUMENTATION
================================================================================