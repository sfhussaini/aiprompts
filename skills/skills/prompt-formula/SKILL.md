---
name: prompt-formula
description: |
  Transform a user action into a highly descriptive, structured JSON image prompt for AI generators like Midjourney or Stable Diffusion. Use this skill when the user provides an "action" and wants to generate a detailed visual prompt including character details, clothing, and environment context. Trigger keywords: "image prompt", "midjourney", "stable diffusion", "prompt formula".
license: MIT
metadata:
  author: system
  version: "1.0"
---

## Overview

This skill performs **prompt engineering** on **user-provided actions** for **AI image generation (Qwen Image 2.1 T2I)**.

### Capabilities
- **Primary:** Convert raw narrative descriptions into structured JSON objects containing positive prompts, negative prompts, and aspect ratios.
- **Secondary:** Apply the RISCOR-GPV methodology to ensure high-quality visual output.
- **Output Format:** .json

### Constraints (When NOT to use)
- If the user is asking for a simple text description without image generation intent.
- For tasks requiring real-time image generation (this skill only generates the *prompt*).

---

## Operational Workflow

The agent MUST execute these steps **sequentially**. Provide a status update to the user after each phase.

### 1. Validation Phase
- **Check:** Verify that Action, Subject/Character, Clothing, and Dialogues are present.
- **Action:** If any component is missing or brief (1-3 words), use `ask_question` to gather specific details before proceeding.

### 2. Research & Gathering Phase
- **Tools:** Use `read_files` for assets and `run_commands` if script checks are needed.
- **Goal:** Consult `assets/output_template.md` to confirm the required JSON structure and check `scripts/` for any logic scripts required before formatting.

### 3. Structuring Phase
- **Logic:** Follow the 8-step T2I Workflow to organize data:
  1. **Read & Split Brief**: Identify Fixed Content vs. Audience Decisions.
  2. **Fix Frame & Ratio**: Determine orientation (default: 3:2 or 2:3).
  3. **Write Opening Sentence**: Describe medium, style, subject, and background/palette.
  4. **Inventory**: List all elements' locations and any legible text in reading order.
  5. **Walk the Frame**: Follow specific paths (Background -> Top Band -> Left Side -> Center -> Right Side -> Bottom Band) for regional or subject-focused shots.
  6. **Set Text Details**: Describe text placement, weight, color, case, and size.
  7. **Lighting Sentence**: Dedicate one sentence to source, direction, quality, and shadows.
  8. **Close with Summary**: One final sentence summarizing the overall composition/mood.

### 4. Drafting Phase (Asset Integration)
- **Action:** Apply "Core Rules & Constraints": Use gendered pronouns (HE/SHE), consolidate context, use common anatomical terms, avoid quality boosters in prose, and ensure no bullet points are used.
- **Constraint Check:** Ensure all 11 Mandatory Components are included: [Subject/Character], [Primary Action], [Facial expressions], [Body posture], [Clothing Detail], [Revealed Body Part(s)], [Covered Body Part(s) / Clothing Detail], [Scene/Environment Context], [Camera], [Visual Style & Quality Modifiers], and [Dialogues shown as Callouts].
- **Output:** Construct the final result using the structure in `assets/output_template.md`.

---

## Input Specification

| Field | Type | Requirement | Description | Example |
|-------|------|-------------|-------------|---------|
| Action | String | Required | The primary action or movement of the subject. | "Running through a forest" |
| Subject/Character | String | Required | The identity, gender, and description of the character. | "A brave warrior woman" |
| Clothing | String | Required | Details about what the character is wearing. | "Leather armor and a tattered cape" |
| Dialogues | String | Optional | Any text to be displayed as callouts in the image. | "Victory is ours!" |

---

## Output Specification

### Final Delivery Format
Return the final result in this JSON structure:

```json
{
  "status": "success",
  "result": {
    "primary_output": "{ \"postive_prompt\": \"...\", \"negative_prompt\": \"...\", \"wh_ratio\": \"...\" }",
    "supporting_assets": ["assets/output_template.md"]
  },
  "metadata": {
    "version": "1.0",
    "processing_time": "0ms"
  }
}
```

---

## Resource Map

| Resource | Path | Purpose |
|----------|------|----------|
| **Template** | `assets/output_template.md` | Provides the structural blueprint for the JSON output.
| **Scripts** | `scripts/` | Contains scripts for logic handling and pre-processing.