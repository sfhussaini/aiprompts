---
name: visualize-story
description: |
  This skill orchestrates the full content creation pipeline. 
  Use when the user provides an initial story idea or scene to generate a structured production-ready prompt list (`story.json`) and narrative script (`story.txt`).
license: MIT
metadata:
  author: system
  version: "1.0"
---

## 🎯 Overview

This skill performs **content creation orchestration** to achieve **automated, production-ready prompt generation from raw story ideas**.

### Capabilities
- **Primary:** Integrates `story-builder`, `story-prompts`, and `prompt-formula` to transform raw ideas into structured data.
- **Secondary:** Flattens the narrative hierarchy (Movie > Scene > Segment > Clip > Frame) into a production-ready prompt list.
- **Output Format:** JSON (`story.json`) and Text (`story.txt`).

### Constraints (When NOT to use)
- If the user only wants a simple story summary without prompt generation.
- If the task does not require the `story-builder` or `story-prompts` pipeline.

---

## ⚙️ Operational Workflow

The agent MUST execute these steps **sequentially**. Provide a status update to the user after each phase.

### 1. Validation Phase
- **Check:** Verify `complete_story` input is present and contains sufficient narrative detail.
- **Action:** If missing or too brief, use `ask_question` to gather specifics (e.g., theme, tone, setting).

### 2. Research & Gathering Phase
- **Tools:** Use the `story-builder` skill.
- **Goal:** Generate a formatted narrative file (`story.txt`) with cinematic cues and dialogue from the user's `complete_story` input.

### 3. Structuring Phase
- **Pre-requisite (Directory Setup):** Execute `scripts/ensure_output_dir.py` via `run_commands`.
  - **Script:** Execute `scripts/transform_data.py` via `run_commands`.
  - **Command:** `python scripts/ensure_output_dir.py output`
  - **Validation:** Verify the output directory exists using `filesystem__get_file_info`.
- **Logic:** Organize the narrative into the hierarchy `Movie → Scene → Segment → Clip → Frame`.
- **Criteria:** Ensure the flow follows the `story-prompts` skill by passing the path of `story.txt` as input, and produce a nested JSON structure with prompt data for each frame.
- **Output:** Save the hierarchical JSON inside the validated `output` directory.

### 4. Drafting Phase (Asset Integration)
- **Asset:** Read the hierarchical JSON produced by `story-prompts` using `read_files`.
- **Action:** Populate the flattened output structure with `sno`, `scene`, `segment`, `clip`, `frame`, `positive_prompt`, and `negative_prompt` fields.
- **Output:** Save as `story.json` using the `editor` tool.

### 5. Processing Phase (Script Execution)
#### 5.1 Data Transformation
- **Script:** Execute `scripts/transform_data.py` via `run_commands`.
- **Command:** `python scripts/transform_data.py [input_json_path] [output_file_name]`
- **Validation:** Verify the output file `story.json` exists using `filesystem__get_file_info`.

---

## 📥 Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| complete_story | String | Required | The initial idea, scene, or narrative starting point provided by the user. | "A cyberpunk detective finds a glowing chip in a rainy alley." |

---

## 📤 Output Specification

### Final Delivery Format
Return the final result in this JSON structure:

```json
{
  "status": "success",
  "result": {
    "primary_output": "absolute/path/to/story.json",
    "supporting_assets": ["absolute/path/to/story.txt"]
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
| **Template** | `.agents/skills/story-builder/` | Provides the narrative blueprint (`story.txt`) for the output. |
| **Script** | `scripts/transform_data.py` | Handles the flattening and consolidation of nested JSON into production-ready format. |
| **Script** | `scripts/ensure_output_dir.py` | Creates the output directory if it does not exist before file generation. |
| **Docs** | `.agents/skills/story-prompts/` | Reference guide for narrative decomposition into hierarchical frame prompts. |

---
## 🔍 Quality Checklist

Before confirming completion, verify:
- [ ] `output/` directory exists.
- [ ] `story.txt` exists and contains formatted narrative with cinematic cues.
- [ ] `story.json` exists and is valid JSON (parseable).
- [ ] All images in `story.json` have non-empty `positive_prompt` fields.
- [ ] The flattened structure matches the expected schema (`sno`, `scene`, `segment`, `clip`, `frame`, `positive_prompt`, `negative_prompt`).
- [ ] Total image count is reasonable for the story length provided.

> **Why?** Prevents premature completion with partial or corrupted data. Ensures downstream consumers get valid inputs.