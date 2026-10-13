## Overview
This document contains the internal logic, selection strategies, and scoring metrics used to determine which frames from the buffer are selected as "peak" frames for production-ready output.

---

## 🎯 Frame Selection Strategy
To capture the most representative, descriptive, and visually compelling frames from the buffer, the following rules must be applied:

### 1. Temporal Distribution Rule
*   **For clips with 4-5 frames:** Select **Frame 3** (middle-late transition).
*   **For clips with 6-8 frames:** Select **Frame 5 & Frame 6** (late peak moment).
*   **For quick transitions (3-4 frames):** Select **Frame 2 & Frame 3**.

### 2. Action Peak Detection
*   Identify when the primary action reaches its visual climax.
*   Choose frames where body positioning is most dynamic/interesting.
*   Prefer frames with maximum revealed anatomy during vulnerable moments.

### 3. Visual Interest Maximization
*   Select frames with best composition (centered subject, clear focal point).
*   Prioritize frames showing complete action sequences.
*   Include transitional frames that show state changes (e.g., standing => squatting).

### 4. Lighting & Mood Alignment
*   Match golden hour lighting to skin tone highlights.
*   Select frames with water reflections for nude bath sequences.
*   Target soft shadows that emphasize curves without harshness.

---

## 🔥 Body Reveal Maximization (For Intimate Moments)
When selecting best frames for intimate/fetish sequences, apply the following specific optimizations:

### Vulnerability Peak Detection
*   Identify when subject is most exposed/confidently nude.
*   Select frames showing complete body awareness (not awkward transitions).
*   Target: 70-85% of clip duration for peak vulnerability.

### Anatomical Focus Optimization
*   **For squatting/urination acts:** Frame 3-4 (full reveal + action completion).
*   **For standing/washing acts:** Frame 5-6 (dynamic movement captured).
*   **For bathing acts:** Frame 6-7 (water interaction + body positioning).

### Lighting-Body Synergy
*   Match golden hour lighting to skin tone highlights.
*   Select frames with water reflections for nude bath sequences.
*   Target soft shadows that emphasize curves without harshness.

---

## 📊 Frame Quality Metrics & Scoring
When selecting the "best" frame from each clip, evaluate against these metrics:

| Metric | Weight | Description | Target Range |
|--------|--------|-------------|--------------|
| **Action Completeness** | 30% | Is the primary action fully realized? | 80-100% |
| **Visual Interest** | 25% | Maximum body positioning/pose interest | High (dynamic poses) |
| **Lighting Quality** | 15% | Best lighting for mood/atmosphere | Golden hour => twilight transition |
| **Composition** | 15% | Centered subject, clear focal point | Medium-close to medium-full |
| **Narrative Significance** | 15% | Key turning point in story arc | Peak emotional beats |

### Scoring Formula
Use the following calculation to determine the final score:

$$Best\ Frame\ Score = (Action\_Completeness \times 0.3) + (Visual\_Interest \times 0.25) + (Lighting\_Quality \times 0.15) + (Composition \times 0.15) + (Narrative\_Significance \times 0.15)$$

**Selection Threshold:** Only frames scoring **$\ge$85/100** should be selected for the final production output.