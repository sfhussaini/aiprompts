---
name: build-workshop
description: |
  Researches a topic and sub-topics to create a structured workshop outline in Markdown, then converts it into a .docx file. Use when the user provides a Topic and Sub Topics (CSV) to generate a full workshop curriculum.
license: MIT
metadata:
  author: system
  version: "1.2"
---

## Overview

This skill performs **workshop creation** on **research data** for **educational content production**.

### What this skill does

- **Primary:** Researches, structures, and formats a workshop curriculum.
- **Secondary:** Converts the final markdown document into a .docx file.
- **Output format:** A dedicated folder containing both .md and .docx versions.

### When NOT to use this skill

- If the input is missing a primary Topic or Sub Topics.
- For simple content generation that does not require a structured workshop format.

---

## When to Use

Use this skill when:

- The user says: "build a workshop", "create a workshop from these topics", or "generate workshop docx".
- The input is of type: **"Topic, Sub Topics CSV"**.
- The goal is to: **Generate a structured workshop document including stages, steps, and assessments.**

---

## Workflow

You MUST follow these steps **in order**. After each phase, provide a brief status update to the user.

1. **Validation Phase**
   - Verify that both a **Topic** and **Sub Topics** are provided.
   - If any are missing, use `ask_question` to request the missing information before proceeding.

2. **Research Phase**
   - Use `fetch_web_content` or `search_codebase` to gather detailed information on the Topic and each provided Sub Topic.
   - Synthesize the information into a cohesive knowledge base for the workshop.

3. **Structuring Phase**
   - Organize the researched content into a logical flow.
   - Break the workshop into **Stages** (e.g., Introduction, Core Concepts, Advanced Application, Summary).
   - Break each Stage into specific **Steps** (e.g., Lecture, Activity, Quiz).

4. **Folder Creation Phase**
   - Create a sanitized folder name based on the **Topic** (e.g., "Prompt_Engineering_Workshop").
   - Use `filesystem__create_directory` to create this folder in the current working directory.

5. **Drafting Phase**
   - Read the template file at `assets/output_template.md` using `read_files`.
   - Generate the full workshop content in Markdown, adhering strictly to the template structure.
   - Use `editor` to save the result as a `.md` file **inside the newly created folder** (e.g., `[FolderName]/workshop_output.md`).

6. **Conversion Phase**
   - Locate the conversion script at `scripts/markdown-to-docx.py`.
   - Execute the script using `run_commands` to convert the generated `.md` file into a `.docx` file **inside the same folder**.
   - Example command: `python scripts/markdown-to-docx.py [FolderName]/workshop_output.md [FolderName]/workshop_output.docx`

---

## Input

### Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Topic | string | The main subject of the workshop. | "Introduction to Python" |
| Sub Topics | CSV | A list of sub-topics provided in CSV format. | "Variables, Loops, Functions" |

---

## Output

### Output structure

Return the final result in the following JSON format:

```json
{
  "status": "success",
  "result": {
    "workshop_folder": "absolute/path/to/folder",
    "markdown_file": "absolute/path/to/folder/generated.md",
    "docx_file": "absolute/path/to/folder/generated.docx"
  },
  "metadata": {
    "source_topic": "Topic",
    "processing_time_ms": 0
  },
  "warnings": [],
  "errors": []
}
```
