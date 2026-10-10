---
name: visualize-story
description: This skill acts as the primary orchestrator for content creation. It integrates three sub-skills—`story-builder`, `story-prompts`, and `prompt-formula`—to transform an initial idea into a structured production-ready prompt list.
---

# visualize-story

This skill acts as the primary orchestrator for content creation. It integrates three sub-skills—`story-builder`, `story-prompts`, and `prompt-formula`—to transform an initial idea into a structured production-ready prompt list.

## Instructions

1. **Skill Integrity:** The definitions of `story-builder`, `story-prompts`, and `prompt-formula` are strictly **READ-ONLY**. You must follow their internal instructions, rules, and formatting requirements exactly as written. Do not modify or simplify them during execution.
2. **Data Consistency:** Ensure that all narrative details (character descriptions, setting nuances, and specific plot points) remain consistent when passing data from the `story-builder` stage to the `story-prompts` stage.
3. **Prompt Quality:** When processing frames in Step 2, you must ensure that the `positive_prompt` and `negative_prompt` adhere strictly to the **RISCOR-GPV** standards (no "masterpiece" keywords, correct use of pronouns, and detailed lighting/composition).

## Usage

Use this skill when a user provides a starting point for a story (e.g., an idea, a theme, or a specific scene) and wants the full pipeline of script creation and automated prompt generation performed automatically.
```

## Steps

1. **Story Generation:** Call the `story-builder` skill using the user's provided input to generate the full narrative.
2. **File Organization:** 
   - Create a new directory named after the story's title (e.g., `[Story_Title]`).
   - Create a file named `story.txt` inside that folder.
   - Save the complete output from the `story-builder` into this `story.txt` file.
3. **Narrative Decomposition:** Call the `story-prompts` skill, providing the path of the newly created `story.txt` as the input. This will break the story into a structured hierarchy (Movie > Scene > Segment > Clip > Frame).
4. **Data Transformation & Export:** 
   - Take the nested output from `story-prompts` and transform it into the following flattened JSON structure:
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
   - Save this finalized JSON content to a file named `story.json` as a sibling of `story.txt`.
5. **Completion:** Confirm to the user that both the narrative (`story.txt`) and the production-ready prompts (`story.json`) have been generated successfully.