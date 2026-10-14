---
name: "story-to-prompt-converter"
description: >-
  Performs multi-stage story and frame selection to produce production-ready image generation prompts. Use when the user
  provides [raw idea] and needs [structured JSON prompt buffer].
license: MIT
allowed-tools:
  - ask_question
  - fetch_web_content
  - search_codebase
  - read_files
  - write_file
  - get_file_info
metadata:
  author: "syed.hussaini@live.com"
  version: "1.7"
  last-updated: "2026-10-13"
---

> **Version:** 1.7 · **Author:** Syed Fazalullah Hussaini· **License:** MIT

# SKILL: story-to-prompt-converter

## 🎯 Overview

This skill performs **[Idea-to-Prompt Transformation]** to achieve **[Production-Ready Image Generation Pipeline]**.

### Capabilities
- **Primary:** Transform raw user ideas into structured story text (`story.txt`) and fragmented JSON buffers (iteratively).
- **Secondary:** Apply frame selection logic (Peak/First-Middle-Last) and finalize image prompts using weighted scoring templates.
- **Output Format:** `final-frames.json` containing flattened prompt data for generation engines.

### Constraints (When NOT to use)
- [Constraint 1: If input idea is too vague (<50 words) without clarification].
- [Constraint 2: If `config.yaml` mode (`firstmiddlelast` vs `best`) is not defined in assets].

### Security & Boundaries
- **File writes:** Restricted to workspace output directory. Never write outside the skill root (e.g., `output\`, `final-frames.json`).
- **Network access:** Limited to domains required for research. No arbitrary outbound calls during processing.
- **PII / Secrets:** Do not persist credentials, tokens, or personal data in outputs.
- **Idempotency:** Files overwrite only when explicitly re-run; otherwise they fail safely.
- **Dependencies:** Requires **only** standard Python libraries (no external packages). The LLM handles all logic via native tools (`read_files`, `write_file`).

---

## 🧠 Core Philosophy

This skill operates on three guiding principles:

- **LLM-Centric:** The LLM is the "brain" that plans, executes, and verifies each phase.
- **Minimal Interaction:** Use `ask_question` ONLY when initial input validation fails (max 2 calls total).
- **Zero Python/Scripting:** No inline code blocks or external scripts required for content generation.

> **Why?** Ensures the LLM remains in control of the workflow, reducing dependency on external tools and keeping execution transparent and self-contained.

---

## ⚙️ Operational Workflow

Execute these steps **sequentially**. Emit a status update only when a phase is long-running, blocked, or requires user input.

### 1. Validation Phase
- **Check:** Verify [User Idea] and [Config Mode (`firstmiddlelast`/`best`)] are present in `config/config.yaml`.
- **Action:** If missing, use `ask_question` to gather specifics before proceeding.

### 2. Research & Gathering Phase (Interactive & Immersive)
- **Tools:** Use `read_files` on template schemas AND `ask_question` for story depth assessment.
- **Goal:** 
    - Load template schemas from `assets/`.
    - Assess if the initial idea has sufficient narrative depth (character, setting, conflict, tone).
    - If depth is lacking (<50 words or missing key elements), use `ask_question` to gather:
        - **Character Details** (Name, appearance, motivation)
        - **Setting Context** (Location, time period, atmosphere)
        - **Conflict/Plot** (Main challenge, stakes, resolution hint)
        - **Visual Tone** (Lighting style, color palette, mood)
- **Action:** 
    - **Craft Immersive Narration:** Transform raw responses into a rich, cinematic story with:
        - **Sensory Details** (sight, sound, smell, touch, taste)
        - **Character Dialogues** (natural-sounding conversations between characters including internal thoughts)
        - **Internal Monologues** (thoughts and emotions of key characters)
        - **Atmospheric Descriptions** (weather, lighting, environment interactions)
    - Structure the narrative to flow naturally from scene to scene.
- **Output:** Synthesize raw responses into a knowledge base for the Structuring Phase.
- **Limit:** Max 2 `ask_question` calls total across all phases.

### 3. Structuring Phase
- **Logic:** Organize data into [Story Text] using `assets\formatted-story-template.md`.
- **Criteria:** Ensure the flow follows [Narrative Arc — e.g., Setup → Conflict → Resolution].
- **Action:** Save as `output\story.txt` using `write_file`.

### 4. Drafting Phase (Iterative & Timeout-Safe)
- **Logic:** Fragment story into clips/frames in small batches (2-3 clips per iteration).
- **State Tracking:** Use a lightweight state file (`output\.drafting_state.json`) to track progress across iterations.
- **Timeout Safety:** Each batch should complete within ~30 seconds; if not, pause and resume from last checkpoint.
- **Action:** 
    - Read `assets\clipped-story-template.md` and `assets\clip-frames-template.md`.
    - Process first 2-3 clips → save as `output\buffers\clipped-story.json`.
    - Then process frames for each clip → save as `output\buffers\clipX-frames.json`.
- **Output:** Save intermediate results (`output\buffers\formatted-story.txt`) and JSON buffers.

### 5. Processing Phase (LLM Execution)

#### 5.1 Selection Logic
- **Logic:** Execute frame selection using `assets\logic\peak_selection_logic.md` OR `assets\logic\firstmiddlelast_selection_logic.md`.
- **Command:** Apply weighted scoring formula: $Score = (Action \times 0.3) + (Visual \times 0.25) + ...$
- **Validation:** Confirm selected frames meet threshold ($\ge$85.0).

#### 5.2 Final Assembly
- **Asset:** Read `assets\final-frames.json` and `assets\prompt-format.md` using `read_files`.
- **Action:** Process `output\buffers\selected-frames.json` by populating templates with frame data via LLM reasoning.
- **Command:** Use `write_file` to generate `final-frames.json` from selected frames and prompt format template.
- **Validation:** Confirm the output file exists and is non-empty using `get_file_info`. (No exit code check needed — pure file I/O).

---

## 📥 Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| idea | String | Required | The core concept or scene description. | "A cyberpunk detective in a rainy alley" |
| mode | String | Optional | Override for `firstmiddlelast` or `best`. | "best" |

---

## 📤 Output Specification

### Success

```json
{
  "status": "success",
  "result": {
    "primary_output": "final-frames.json",
    "supporting_assets": ["output\\story.txt", "output\\buffers\\clipped-story.json"]
  },
  "metadata": {
    "version": "1.7",
    "processing_time_ms": 0,
    "total_frames_selected": 5
  }
}
```

### Error

```json
{
  "status": "error",
  "error": {
    "code": "MISSING_INPUT",
    "message": "Required field 'idea' was not provided.",
    "recoverable": true
  },
  "metadata": {
    "version": "1.7",
    "processing_time_ms": 0
  }
}
```

**Error codes:** `MISSING_INPUT`, `INVALID_INPUT`, `SCRIPT_FAILURE`, `VALIDATION_FAILED`, `PERMISSION_DENIED`.

---

## 🛠️ Resource Map

| Resource | Path | Purpose |
|----------|------|---------|
| **Template (Story)** | `assets\formatted-story-template.md` | Structural blueprint for story text. |
| **Template (Clips)** | `assets\clipped-story-template.md` | JSON schema for clip fragmentation. |
| **Template (Frames)** | `assets\clip-frames-template.md` | JSON schema for frame-level prompts. |
| **Logic (Selection)** | `assets\logic\peak_selection_logic.md` / `firstmiddlelast_selection_logic.md` | Frame selection strategy. |
| **Final Template** | `assets\final-frames.json` | Output structure definition. |
| **Prompt Format** | `assets\prompt-format.md` | Prompt string template (positive/negative/wh_ratio). |

---

## ✅ Quality Checklist

Before confirming completion, verify:

- [ ] Check 1: Verify `output\story.txt` matches narrative flow.
- [ ] Check 2: Confirm `final-frames.json` contains valid prompt strings (not empty).
- [ ] Check 3: Ensure selection logic mode (`firstmiddlelast` vs `best`) is consistent with config.

> **Why?** Prevents premature completion with partial or corrupted data, ensuring downstream consumers receive valid inputs.

---

## 📚 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.7 | 2026-10-13 | Fixed **Step 5.2 Final Assembly** to use pure LLM `write_file` (no exit code check) for consistency with "Zero Python/Scripting" philosophy. Updated version to 1.7. |
| 1.6 | 2026-10-13 | Improved **Drafting Phase** to be iterative (batch processing + state tracking) for timeout safety; Fixed **Dependencies** to match "Zero Python/Scripting" philosophy. |
| 1.5 | 2026-10-13 | Improved **Research & Gathering Phase** to include interactive user questioning for story depth. |
| 1.4 | 2026-10-13 | Added **Core Philosophy** section (LLM-Centric, Minimal Interaction, Zero Python/Scripting). |
| 1.3 | 2026-10-13 | Corrected Step 5.2 to use `assets\final-frames.json` & `assets\prompt-format.md` instead of assumed script; Updated skill name to "story-to-prompt-converter". |
| x.x | dd-MON-rr | change done |