---
name: visualize-story
description: |
  This skill acts as the primary orchestrator for content creation. It integrates three sub-skills—`story-builder`, `story-prompts`, and `prompt-formula`—to transform an initial idea into a structured production-ready prompt list. Use when the user provides a starting point for a story (e.g., an idea, or a specific scene) and wants the full pipeline of script creation and automated prompt generation performed automatically.
license: MIT
metadata:
  author: system
  version: "1.0"
---

## Overview

This skill performs **orchestration of content creation** on **initial story ideas/scenes** for **automated production-ready prompt generation**.

### What this skill does

- **Primary:** Integrates `story-builder` and `story-prompts` to transform raw ideas into structured data.
- **Secondary:** Handles narrative decomposition (Movie > Scene > Segment > Clip > Frame).
- **Output format:** JSON (`story.json`) and Text (`story.txt`).

### When NOT to use this skill

- If the user only wants a simple story summary without prompt generation.
- For tasks that do not require the specific `story-builder` or `story-prompts` pipeline.

---

## Instructions

1. **Skill Integrity:** The definitions of `story-builder`, `story-prompts` are strictly **READ-ONLY**. You must follow their internal instructions, rules, and formatting requirements exactly as written. Do not modify or simplify them during execution.
2. **Data Consistency:** Ensure that all narrative details (character descriptions, setting nuances, and specific plot points) remain consistent when passing data from the `story-builder` stage to the `story-prompts` stage.

---

## When to Use

Use this skill when:

- The user says: "generate a full production pipeline", "create a script and prompts", or "visualize my story".
- The input is of type: **"complete_story"** (an idea, scene, or narrative starting point).
- The goal is to: **transform an initial idea into a structured production-ready prompt list.**

---

## Workflow

Follow these steps **in order**:

1. **Story Generation:** 
   - Call the `story-builder` skill using the user's provided input.
   - This will generate a story folder containing the narrative file: `story.txt`.

2. **Narrative Decomposition:** 
   - Call the `story-prompts` skill, providing the path of the newly created `story.txt` as the input.
   - This will produce a nested JSON structure representing the hierarchy (Movie > Scene > Segment > Clip > Frame).

3. **Data Transformation & Export:** 
   - Run the script `scripts/transform_data.py`.
   - The script takes the output from the `story-prompts` step and consolidates it into a flattened JSON structure:
     ```json
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
     ```
   - The script saves this result as `story.json` in the same directory as `story.txt`.

4. **Completion:** 
   - Confirm to the user that both the narrative (`story.txt`) and the production-ready prompts (`story.json`) have been generated successfully.

---

## Input

### Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| complete_story | string | The initial idea, scene, or narrative starting point provided by the user. | "A cyberpunk detective finds a glowing chip in a rainy alley." |

---

## Output

### Output structure

The skill produces two files: `story.txt` (narrative) and `story.json` (flattened prompts). The final confirmation should follow the format in `assets/output_template.md`.
