# Overview
This document contains the internal logic, selection strategies, and scoring metrics used to determine which frames from the buffer are selected as "first", "middle", and "last" frames for production-ready output.

---

## 🎯 Frame Selection Strategy (First/Middle/Last)

To capture representative keyframes that define the temporal boundaries of each clip, the following rules must be applied:

### 1. Temporal Positioning Rule
*   **For clips with 4-5 frames:** Select **Frame 2** (first), **Frame 3** (middle), and **Frame 4** (last).
*   **For clips with 6-8 frames:** Select **Frame 2** (first), **Frame 5** (middle), and **Frame 7** (last).
*   **For quick transitions (3-4 frames):** Select **Frame 1** (first), **Frame 2** (middle), and **Frame 3** (last).

### 2. Action Boundary Detection
*   **First Frame:** Identify when the primary action begins or is in early stages. Choose frames where body positioning shows initial engagement with the scene.
*   **Middle Frame:** Identify when the primary action reaches its visual midpoint. Choose frames showing sustained dynamic poses or transitional states.
*   **Last Frame:** Identify when the primary action concludes or transitions to next state. Prefer frames with resolution of the main action sequence.

### 3. Visual Interest Maximization (Keyframes)
*   Select frames with best composition (centered subject, clear focal point).
*   Prioritize frames showing complete action sequences at their respective temporal positions.
*   Include transitional frames that show state changes between key moments.

### 4. Lighting & Mood Alignment (Keyframes)
*   Match golden hour lighting to skin tone highlights for all keyframe types.
*   Select frames with water reflections for nude bath sequences across all positions.
*   Target soft shadows that emphasize curves without harshness.

---

## 📊 Frame Quality Metrics & Scoring (For Keyframes)

When selecting "first", "middle", and "last" frames from each clip, evaluate against these metrics:

| Metric | Weight | Description | Target Range |
|--------|--------|-------------|--------------|
| **Action Completeness** | 30% | Is the primary action fully realized at this temporal position? | 80-100% |
| **Visual Interest** | 25% | Maximum body positioning/pose interest for keyframe type | High (dynamic poses) |
| **Lighting Quality** | 15% | Best lighting for mood/atmosphere | Golden hour => twilight transition |
| **Composition** | 15% | Centered subject, clear focal point | Medium-close to medium-full |
| **Narrative Significance** | 15% | Key turning point in story arc at this position | Peak emotional beats |

### Scoring Formula
Use the following calculation to determine the final score:

$$Best\ Frame\ Score = (Action\_Completeness \times 0.3) + (Visual\_Interest \times 0.25) + (Lighting\_Quality \times 0.15) + (Composition \times 0.15) + (Narrative\_Significance \times 0.15)$$

**Selection Threshold:** Only frames scoring **≥85/100** should be selected for the final production output.

---

## 🔄 Temporal Distribution Guidelines

### For Short Clips (3-4 Frames)
*   **First Frame:** Capture initial action engagement or scene entry
*   **Middle Frame:** Show transitional state or peak intensity
*   **Last Frame:** Resolve action or transition to next state

### For Medium Clips (5-6 Frames)
*   **First Frame:** Establish context and initial positioning
*   **Middle Frame:** Capture sustained dynamic pose or key interaction
*   **Last Frame:** Complete action sequence with resolution

### For Long Clips (7+ Frames)
*   **First Frame:** Set scene, establish subject state, begin action
*   **Middle Frame(s):** Select 1-2 frames showing peak visual interest
*   **Last Frame:** Conclude main action, show aftermath or transition

---

## 🎬 Use Cases

### When to Apply First/Middle/Last Selection:
*   Creating thumbnail previews for clip review
*   Generating quick visual summaries of narrative flow
*   Establishing continuity checkpoints between clips
*   Rapid prototyping before full frame generation

### When to Supplement with Peak Frame Detection:
*   Clips requiring detailed action coverage (6+ frames)
*   Complex multi-stage actions needing intermediate captures
*   High-visual-interest sequences requiring multiple keyframes

---

## 📝 Implementation Notes

1.  **Frame Numbering:** Use 1-based indexing for frame calculations.
2.  **Rounding:** For odd-numbered clips, middle = `(total_frames + 1) // 2`.
3.  **Buffer Storage:** Store keyframes in `story-prompts-buffer.json` with metadata indicating their temporal position type.
4.  **Quality Validation:** Apply same quality metrics as peak frame selection to ensure consistency.
