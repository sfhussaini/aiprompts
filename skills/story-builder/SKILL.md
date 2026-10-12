---
name: story-builder
description: |
  Generates a structured narrative using cinematic cues and specific formatting. Use this when the user wants to create a "story" or "script" based on a theme, idea, and tone. 
  Trigger keywords: "create a story", "write a script", "build a narrative", "story_builder".
license: MIT
metadata:
  opencode/autoinvoke: true
---

## Overview

This skill transforms a raw concept into a structured, cinematic story draft using a predefined template and automated file generation.

### What this skill does
- **Primary:** Generates a formatted narrative including setting, camera cues, and dialogue.
- **Secondary:** Automatically creates the local directory structure and saves the output to a `.txt` file.
- **Output format:** A structured text file saved in the user's specified path.

### When NOT to use this skill
- If the user only wants a short summary without cinematic cues or dialogue.
- For non-fiction technical documentation (use `technical-writer` instead).

---

## When to Use

Use this skill when:
- The user says: "Create a story about [Topic]" or "Write a script for [Idea]".
- The input includes specific narrative elements like **Theme**, **Tone**, and **Story Idea**.
- The goal is to produce a physical file in a specific directory.

---

## Workflow

Follow these steps **in order**:

1. **Input Collection**
   - Collect the following from the user: `Theme`, `Story Idea`, `Tone`, and `FolderPath`.
   - If any are missing, ask the user for clarification before proceeding.

2. **Content Generation**
   - Reference the template in `assets/output_template.md`.
   - Populate the template with the provided `Theme`, `Story Idea`, and `Tone`. 
   - Ensure the narrative follows the "Pronoun Preference" rule (e.g., use "She" instead of "Maya").

3. **File System Execution**
   - Use the script `scripts/generate_story.py` to finalize the output.
   - Pass the generated content and the `FolderPath` as arguments to the script.
   - The script will create the folder (if missing) and save the file as `story.txt`.

4. **Confirmation**
   - Confirm to the user that the story has been successfully generated at the specified path.

---

## Input

### Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Theme | String | The core concept or genre (e.g., "Cyberpunk Noir"). | Cyberpunk Noir |
| Story Idea | String | The specific plot or premise. | A detective finds a robot with human memories. |
| Tone | String | The emotional atmosphere (e.g., Melancholic, High-octane). | Melancholic and gritty. |
| FolderPath | String | The local path where the file should be saved. | ./projects/my_story |

---

## Output

### Output structure

```json
{
  "status": "success",
  "result": {
    "file_path": "/path/to/story.txt",
    "content_preview": "First 100 characters of the story..."
  },
  "metadata": {
    "theme": "...",
    "tone": "..."
  },
  "warnings": [],
  "errors": []
}
