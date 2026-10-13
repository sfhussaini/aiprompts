name: prompt-formula
description: |
  Transform a user action into a highly descriptive, structured JSON image prompt for AI generators like Midjourney or Stable Diffusion. Use this skill when the user provides an "action" and wants to generate a detailed visual prompt including character details, clothing, and environment context. Trigger keywords: "image prompt", "midjourney", "stable diffusion", "prompt formula".
MIT
metadata:
  author: "syed.hussaini@live.com"
  version: "1.1"
---

> **Version:** 1.1 · **Author:** syedhussaini@livecom · **License:** MIT

# SKILL: prompt-formula

## Overview (Target)

This skill performs **Convert raw narrative descriptions into structured JSON objects containing positive prompts, negative prompts, and aspect ratios.** to achieve **AI image prompt generation**.

### Capabilities
- **Primary:** Convert raw narrative descriptions into structured JSON objects containing positive prompts, negative prompts, and aspect ratios.
- **Secondary:** Apply the RISCOR-GPV methodology to ensure high-quality visual output.
- **Output Format:** .json

### Constraints (When NOT to use)
- If the user is asking for a simple text description without image generation intent.
- For tasks requiring real-time image generation (this skill only generates the *prompt*).
- **Restricted to the workspace output directory. Never write outside the skill root.**

### Security & Boundaries
- **Limited to the domains required for research. No arbitrary outbound calls.**
- **Do not persist credentials, tokens, or personal data in outputs.**
- **Scripts overwrite existing outputs only when `--force` is passed; otherwise they fail safely.**
- **Requires Python 3.10+ and packages listed in `requirements.txt`.**

---

## Operational Workflow

Execute these steps **sequentially**. Emit a status update only when a phase is long-running, blocked, or requires user input.

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
- **Asset:** Use the `assets/output_template.md` using `read_files`.
- **Action:** Populate the template with researched data.
- **Output:** Save as `output/[filename].md` using `write_file`.

### 5. Processing Phase (Script Execution)

#### 5.1 Processing Step
- **Script:** Execute `scripts/validate_output.py` via `run_commands`.
- **Command:** `python scripts/validate_output.py output/[input_path] output/[output_path]`
- **Validation:** Confirm the script exits with code `0`, then verify the output file exists and is non-empty using `get_file_info`.

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

### Success

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

### Error

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

**Error codes:** MISSING_INPUT, INVALID_INPUT, SCRIPT_FAILURE, VALIDATION_FAILED, PERMISSION_DENIED.

---

## Resource Map

| Resource | Path | Purpose |
|----------|------|---------|
| **Template** | `assets/output_template.md` | Provides the structural blueprint for the JSON output. |
| **Dependencies** | `requirements.txt` | Python packages required by scripts. |

---

## Quality Checklist

Before confirming completion, verify:

- [ ] Check 1: Verify all 11 Mandatory Components are present in the output.
- [ ] Check 2: Ensure JSON structure matches `assets/output_template.md` exactly.

> **Why?** Prevents premature completion with partial or corrupted data, ensuring downstream consumers receive valid inputs.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-10-13 | Initial template application from reference card. |