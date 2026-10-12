---
name: story-builder
description: |
  Generates a structured, cinematic narrative based on a theme, idea, and tone. 
  Use when the user provides Theme, Story Idea, Tone, and FolderPath to generate a formatted story.txt file.
license: MIT
metadata:
  author: System
  version: "1.0"
---

## 🎯 Overview

This skill performs **Narrative Generation** to achieve **Cinematic Storytelling**.

### Capabilities
- **Primary:** Generates a formatted narrative including setting, camera cues, and dialogue.
- **Secondary:** Automatically creates the local directory structure and saves the output to a file.
- **Output Format:** .txt (via script execution).

### Constraints (When NOT to use)
- If the user only wants a short summary without cinematic cues or dialogue.
- For non-fiction technical documentation (use `technical-writer` instead).

---

## ⚙️ Operational Workflow

The agent MUST execute these steps **sequentially**. Provide a status update to the user after each phase.

### 1. Validation Phase
- **Check:** Verify `Theme`, `Story Idea`, `Tone`, and `FolderPath` are present.
- **Action:** If missing, use `ask_question` to gather specifics.

### 2. Research & Gathering Phase
- **Tools:** Use `fetch_web_content` or `search_codebase`.
- **Goal:** Gather thematic elements, cinematic tropes, and genre-specific cues to synthesize into the narrative.

### 3. Structuring Phase
- **Logic:** Organize data into a cinematic flow (Scene $\rightarrow$ Visual Cue $\rightarrow$ Dialogue).
- **Criteria:** Ensure the flow follows the "Pronoun Preference" rule (e.g., use "She" instead of "Maya") and aligns with the specified `Tone`.

### 4. Drafting Phase (Asset Integration)
- **Asset:** Read `assets/output_template.md` using `read_files`.
- **Action:** Populate the template with the researched narrative data.
- **Output:** Save as `story_draft.md` using the `editor` tool.

### 5. Processing Phase (Script Execution)
- **Script:** Execute `scripts/generate_story.py` via `run_commands`.
- **Command:** `python scripts/generate_story.py [story_draft.md] [FolderPath]`
- **Validation:** Verify the output file `story.txt` exists using `filesystem__get_file_info`.

---

## 📥 Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| Theme | String | Required | The core concept or genre | "Cyberpunk Noir" |
| Story Idea | String | Required | The specific plot or premise | "A detective finds a robot with human memories." |
| Tone | String | Required | The emotional atmosphere | "Melancholic and gritty" |
| FolderPath | String | Required | The local path where the file should be saved | "./projects/my_story" |

---

## 📤 Output Specification

### Final Delivery Format
Return the final result in this JSON structure:

```json
{
  "status": "success",
  "result": {
    "primary_output": "absolute/path/to/story.txt",
    "supporting_assets": ["absolute/path/to/story_draft.md"]
  },
  "metadata": {
    "version": "1.0",
    "processing_time": "0ms"
  }
}
```

---

## 🛠️ Resource Map

| Resource | Path | Purpose |
|----------|------|----------|
| **Template** | `assets/output_template.md` | Provides the structural blueprint for the cinematic narrative. |
| **Script** | `scripts/generate_story.py` | Handles the file system creation and saving the final story.txt. |
| **Docs** | `references/` | Reference guide for the agent to ensure quality. |