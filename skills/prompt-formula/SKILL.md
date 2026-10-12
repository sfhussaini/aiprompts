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

### What this skill does

- **Primary:** Converts raw narrative descriptions into structured JSON objects containing positive prompts, negative prompts, and aspect ratios.
- **Secondary:** Applies the RISCOR-GPV methodology to ensure high-quality visual output.
- **Output format:** JSON

### When NOT to use this skill

- If the user is asking for a simple text description without image generation intent.
- For tasks requiring real-time image generation (this skill only generates the *prompt*).

---

## When to Use

Use this skill when:

- The user says: "generate an image prompt", "create a midjourney prompt", or "transform action into a prompt".
- The input is of type: **Action, Subject/Character, Clothing, Dialogues**.
- The goal is to: **Generate a structured JSON object for AI art generation.**

---

## Workflow

Follow these steps **in order**:

1. **Input Validation**
   - Verify the user has provided the core components: Action, Subject/Character, Clothing, and Dialogues.
   - If any component is missing or brief (1-3 words), prepare to add descriptive weight during processing.

2. **Reference Assets**
   - Consult `assets/output_template.md` to ensure the final output strictly follows the required JSON structure.
   - Check `scripts/` for any additional logic scripts that need execution before final formatting.

3. **Core Processing (T2I Workflow)**
   Follow these 8 steps exactly:
   1. **Read & Split Brief**: Identify Fixed Content (exact strings, colors, counts) vs. Audience Decisions (lighting, expressions).
   2. **Fix Frame & Ratio**: Determine orientation; default to `3:2` (horizontal) or `2:3` (vertical).
   3. **Write Opening Sentence**: Describe medium, style, subject, and background/palette.
   4. **Inventory**: List all elements' locations and any legible text in reading order.
   5. **Walk the Frame**: If Regional, follow: Background -> Top Band -> Left Side -> Center -> Right Side -> Bottom Band. If Subject-Focused: Background -> Pose -> Head/Face -> Body/Garard -> Held Objects -> Edges.
   6. **Set Text Details**: Describe text placement, weight, color, case, and size.
   7. **Lighting Sentence**: Dedicate one sentence to source, direction, quality, and shadows.
   8. **Close with Summary**: One final sentence summarizing the overall composition/mood.

4. **Final Construction**
   - Apply "Core Rules & Constraints": Use gendered pronouns (HE/SHE), consolidate context, use common anatomical terms, avoid quality boosters in prose, and ensure no bullet points are used in the narrative paragraph.
   - Ensure all 11 Mandatory Components are included: [Subject/Character], [Primary Action], [Facial expressions], [Body posture], [Clothing Detail], [Revealed Body Part(s)], [Covered Body Part(s) / Clothing Detail], [Scene/Environment Context], [Camera], [Visual Style & Quality Modifiers], and [Dialogues shown as Callouts].
   - Format the final result into the JSON structure defined in `assets/output_template.md`.

---

## Input

### Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Action | String | The primary action or movement of the subject. | "Running through a forest" |
| Subject/Character | String | The identity, gender, and description of the character. | "A brave warrior woman" |
| Clothing | String | Details about what the character is wearing. | "Leather armor and a tattered cape" |
| Dialogues | String | Any text to be displayed as callouts in the image. | "Victory is ours!" |

---

## Output

### Output structure

```json
{
  "postive_prompt": "<[Subject/Character] is [Primary Action] with [Facial expressions] and [Body posture]. Dressed in [Clothing Detail], they reveal [Revealed Body Part(s)] while keeping [Covered Body Part(s) / Clothing Detail] covered. The scene takes place in [Scene/Environment Context], captured as a [Camera] shot with [Visual Style & Quality Modifiers]. [Dialogues] are shown as callouts over [Subject/Character].>",
  "negative_prompt": "<the csv list>",
  "wh_ratio": "<e.g., 3:2>"
}