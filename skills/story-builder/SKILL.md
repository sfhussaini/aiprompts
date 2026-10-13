name: story-builder
description: |
  Generate a complete narrative story with cinematic vision, dialogue, and structured formatting. Use this skill when the user provides a "title" or "theme" and wants to develop a full story including setting, characters, plot progression, and visual direction.
MIT
metadata:
  author: "syed.hussaini@live.com"
  version: "1.1"
---

> **Version:** 1.1 · **Author:** syedhussaini@livecom · **License:** MIT

# SKILL: story-builder

## 🎯 Overview

This skill performs **** to achieve **cinematic story development**.

### Capabilities
- **Primary:** Transform raw ideas into structured narrative files with cinematic vision, dialogue, and plot progression.
- **Secondary:** Apply the output template structure to ensure consistent formatting across all generated stories.
- **Output Format:** .txt

### Constraints (When NOT to use)
- If the user is asking for a simple text description without full story development intent.
- For tasks requiring only image prompts (use `prompt-formula` skill instead).
- **Restricted to the workspace output directory. Never write outside the skill root.**.

### Security & Boundaries
- **Limited to the domains required for research. No arbitrary outbound calls.**.
- **Do not persist credentials, tokens, or personal data in outputs.**.
- **Scripts overwrite existing outputs only when `--force` is passed; otherwise they fail safely.**.
- **Requires Python 3.10+ and packages listed in `requirements.txt`.**.

---

## ⚙️ Operational Workflow

Execute these steps **sequentially**. Emit a status update only when a phase is long-running, blocked, or requires user input.

### 1. Validation Phase
- **Check:** Verify that Title, Theme, and Summary are present.
- **Action:** If any component is missing or brief (1-3 words), use `ask_question` to gather specific details before proceeding.

### 2. Research & Gathering Phase
- **Tools:** Use `read_files` for assets and `run_commands` if script checks are needed.
- **Goal:** Consult `assets/output_template.md` to confirm the required narrative structure and check `scripts/` for any logic scripts required before formatting.

### 3. Structuring Phase
    1. **Read & Split Brief**: Identify Fixed Content vs. Audience Decisions.
    2. **Fix Setting & Context**: Determine Location, Time of Day, and Atmosphere.
    3. **Write Opening Narration**: Describe medium, style, subject, and background/palette.
    4. **Inventory Characters & Dialogue**: List all characters' locations and any legible text in reading order.
    5. **Walk the Narrative Arc**: Follow specific paths (Opening -> Rising Action -> Climax -> Resolution) for plot progression.

### 4. Drafting Phase (Asset Integration)
- **Asset:** Use the `assets/output_template.md` using `read_files`.
- **Action:** Populate the template with researched data including narrative paragraphs, dialogue exchanges, and action details.
- **Output:** Save as `output/[filename].txt` using `write_file`.

### 5. Processing Phase (Script Execution)

#### 5.1 Processing Step
- **Script:** Execute `scripts/generate_story.py` via `run_commands`.
- **Command:** `python scripts/generate_story.py --path output/[input_path] --filename [output_filename] --content "[story_content]"`
- **Validation:** Confirm the script exits with code `0`, then verify the output file exists and is non-empty using `get_file_info`.

---

## 📥 Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| Title | String | Required | The working title for the story. | "The Last Guardian" |
| Theme | String | Required | The core concept or genre of the story. | "A cyberpunk tale about redemption and sacrifice" |
| Summary | String | Optional | A concise summary of what happens in the story. | "A rogue android discovers its creator's secret mission." |

---

## 📤 Output Specification

### Success

  ### Final Delivery Format
  
  Return the final result using this structure (based on `assets/output_template.md`):
  
  ```markdown
  # Story Title: [Title]
  
  ## Theme: [Theme]
  *A brief description of the core concept or genre.*
  
  ## Story Summary: [Summary]
  *A concise, compelling summary of what happens in this story. What is the main conflict?*
  
  ---
  
  ### Setting & Context
  **Location:** [Location]
  **Time of Day:** [Time of Day]
  
  ### Cinematic Vision
  **Camera Suggestion:** [Camera Shot Idea]
  
  ---
  
  ## Narrative & Dialogue (The Story)
  
  **(Start with a strong opening narration to set the mood and scene.)**
  
  [Narrative Paragraph 1: Establish the setting, introduce the main character(s), and hint at the central conflict. Use sensory details—what does it look like, sound like, smell like?]
  
  *Note: Prioritize using pronouns ('She', 'Her') over proper names unless it is a key moment of introduction.*
  
  ***
  
  **Character A:** "[Dialogue Line]"
  *(Action/Narration Detail: Describe what Character A is doing while speaking.)*
  
  [Narrative Paragraph 2: Develop the action. What happens next? Does the character react to something? Introduce tension.]
  
  ***
  
  **Character B:** "[Dialogue Line]"
  *(Action/Narration Detail: Describe Character B's reaction or movement.)*
  
  [... continue with plot progression ...]
  
  **(Concluding Narration):** [Final paragraph that resolves the immediate conflict, leaves a lingering question, or provides a powerful final image. Tie back to the Theme.]```
```

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "MISSING_INPUT",
    "message": "Required field '[field]' was not provided.",
    "recoverable": true
  },
  "metadata": {
    "version": "1.0",
    "processing_time": "0ms"
  }
}
```

**Error codes:** `MISSING_INPUT`, `INVALID_INPUT`, `SCRIPT_FAILURE`, `VALIDATION_FAILED`, `PERMISSION_DENIED`.

---

## 🛠️ Resource Map

| Resource | Path | Purpose |
|----------|------|---------|
| **Template** | `assets/output_template.md` | Provides the narrative blueprint (story.txt) for the output. |
| **Script** | `scripts/generate_story.py` | Handles the creation and writing of story files to specified directories. |
| **Dependencies** | `requirements.txt` | Python packages required by scripts. |

---

## ✅ Quality Checklist

Before confirming completion, verify:

- [ ] Check 1: Verify all sections from `assets/output_template.md` are present in the output.
- [ ] Check 2: Ensure narrative flow follows Opening -> Rising Action -> Climax -> Resolution structure.

> **Why?** Prevents premature completion with partial or corrupted data, ensuring downstream consumers receive valid inputs.

---

## 📚 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-10-13 | Initial template application from reference card. |