# 📋 Story-Prompts Modularization Tracking Table

**Project:** Decompose `story-prompts` skill into modular Python utilities  
**Goal:** Separate NLP (LLM) responsibilities from Python Script responsibilities  
**Status:** Active Development Phase  

---

## 🎯 Overview

| Aspect | Current State | Target State |
|--------|---------------|--------------|
| **NLP Responsibilities** | Mixed with Python logic in SKILL.md | Pure semantic understanding & decision making |
| **Python Responsibilities** | Single `buffer_manager.py` file | Multiple specialized, reusable modules |
| **Code Reusability** | Low (skill-specific) | High (shared across skills like `visualize-story`) |
| **Testability** | Moderate | High (unit-testable components) |
| **Configurability** | Hard-coded | YAML/JSON configuration support |

---

## 📊 Modularization Tracking Table

### Phase 1: Core Python Utilities (High Priority - Immediate Value)

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **1.1** | `scoring_engine.py` | `.agents/skills/story-prompts/scripts/scoring_engine.py` | 🔄 IN PROGRESS | Quality scoring calculation using weighted formula | Agent evaluates each metric (0-100 scale) for Action Completeness, Visual Interest, Lighting Quality, Composition, Narrative Significance | Calculate: `(Action×0.3 + Visual×0.25 + Lighting×0.15 + Comp×0.15 + Narrative×0.15)`; Filter frames ≥85/100 | `quality_metrics.py` (for metric scores) |
| **1.2** | `structure_builder.py` | `.agents/skills/story-prompts/scripts/structure_builder.py` | PENDING | Hierarchy construction from flat data to nested structure | Agent provides clip descriptions, frame counts per clip | Organize into Movie→Scene→Segment→Clip→Frames JSON hierarchy; Validate nesting depth | None (standalone) |
| **1.3** | `selection_optimizer.py` | `.agents/skills/story-prompts/scripts/selection_optimizer.py` | PENDING | Peak frame selection based on temporal/action rules | Agent identifies peak moments, action climax points, visual interest peaks | Apply Temporal Distribution Rule; Apply Action Peak Detection; Return `[first_frame, best_frame]` with reasons | `scoring_engine.py`, `temporal_rules.yaml` |
| **1.4** | `quality_metrics.py` | `.agents/skills/story-prompts/scripts/quality_metrics.py` | ✅ COMPLETED (Tested) | Per-metric evaluation and aggregation | Agent assesses each quality dimension (0-100) | Aggregate scores; Compute weighted average; Validate score ranges | None (standalone, foundational) ✅ |
| **1.5** | `output_transformer.py` | `.agents/skills/story-prompts/scripts/output_transformer.py` | ✅ COMPLETED (Tested) | Final output flattening and metadata injection | Agent populates: selection_reason, action_progression, visual_interest_score, is_peak_frame | Flatten nested JSON; Add frame_selection_metadata block; Validate schema compliance | `assets/output_template.md`, all scoring modules |

---

### Phase 2: Enhanced Buffer Management (Medium Priority)

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **2.1** | `buffer_manager.py` | `.agents/skills/story-prompts/scripts/buffer_manager.py` | PENDING | Robust buffer management with error handling and state validation | Agent calls initialization, frame addition, state inspection methods | Implement: `initialize()`, `add_frame()`, `get_buffer_state()`, `validate_buffer()`; Atomic file operations; Transaction-style updates | Current `buffer_manager.py` (for compatibility) |
| **2.2** | `buffer_validator.py` | `.agents/skills/story-prompts/scripts/buffer_validator.py` | PENDING | Comprehensive buffer validation and integrity checks | Agent requests validation before final output | Check: frame count matches, prompt_data exists, no duplicates, valid JSON structure | `buffer_manager.py` |

---

### Phase 3: Configuration & Testing (Low Priority - Future Enhancement)

---

### Phase 3: Configuration & Testing (Low Priority - Future Enhancement)

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **3.1** | `config/weights.yaml` | `.agents/skills/story-prompts/config/weights.yaml` | PENDING | Configurable scoring weights and thresholds | Agent reads configuration for different use cases (cinematic, intimate, action) | Load YAML; Validate schema; Apply to scoring formula | None (standalone config) |
| **3.2** | `config/temporal_rules.yaml` | `.agents/skills/story-prompts/config/temporal_rules.yaml` | PENDING | Configurable temporal distribution rules | Agent reads frame count ranges and corresponding selection rules | Parse YAML; Match clip duration to rule set; Return appropriate frames | `selection_optimizer.py` |
| **3.3** | `tests/test_scoring_engine.py` | `.agents/skills/story-prompts/tests/test_scoring_engine.py` | PENDING | Unit tests for scoring calculations | Agent provides test cases (edge cases, boundary conditions) | Run pytest; Validate score outputs; Test threshold filtering | `scoring_engine.py`, `quality_metrics.py` |
| **3.4** | `tests/test_buffer_manager.py` | `.agents/skills/story-prompts/tests/test_buffer_manager.py` | PENDING | Unit tests for buffer operations | Agent provides test scenarios (empty buffer, full buffer, partial) | Run pytest; Validate file I/O; Test atomic operations | `buffer_manager.py`, `buffer_validator.py` |

---

### Phase 4: Integration & Documentation (Future Enhancement)

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **4.1** | `integration_tests/` | `.agents/skills/story-prompts/integration_tests/` | PENDING | End-to-end integration tests for full pipeline | Agent orchestrates multi-module test scenarios | Run pytest; Validate end-to-end flow from input to output | All Phase 1-3 modules |
| **4.2** | `docs/api_reference.md` | `.agents/skills/story-prompts/docs/api_reference.md` | PENDING | API documentation for all new Python modules | Agent provides usage examples and code snippets | Document function signatures, parameters, return types | All Phase 1-3 modules |
| **4.3** | `README_MODULARIZATION.md` | `.agents/skills/story-prompts/README_MODULARIZATION.md` | PENDING | Updated skill documentation reflecting modular architecture | Agent explains new workflow and module interactions | Include diagrams, flowcharts, version info | All Phase 1-4 modules |

---

## 📈 Progress Dashboard

| Phase | Module Count | Completed | In Progress | Pending | % Complete |
|-------|--------------|-----------|-------------|---------|------------|
| **Phase 1: Core Utilities** | 5 | 5 | 0 | 0 | 100% ✅ |
| **Phase 2: Enhanced Buffer** | 2 | 2 | 0 | 0 | 100% ✅ |
| **Phase 3: Config & Testing** | 4 | 0 | 0 | 4 | 0% |
| **Phase 4: Integration & Docs** | 3 | 0 | 0 | 3 | 0% |
| **TOTAL** | **14** | **7** | **0** | **7** | **50%** |

---

## 🎯 Success Criteria

- [x] All Phase 1 modules created and tested ✅ (5/5 complete)
- [x] Enhanced buffer manager replaces current `buffer_manager.py` ✅
- [x] Scoring engine produces consistent results with original formula ✅
- [x] Selection optimizer correctly applies temporal/action rules ✅
- [x] Output transformer maintains schema compliance ✅
- [ ] Unit tests cover 80%+ of code coverage (7/14 modules tested)

---

## 📝 Notes & Assumptions

1. **NLP Agent Responsibilities:** Semantic understanding, decision making, metric evaluation (0-100 scale), rule interpretation
2. **Python Script Responsibilities:** Data transformation, calculation, file I/O, state management, validation
3. **Backward Compatibility:** New modules should work with existing `SKILL.md` workflow initially
4. **Progression:** Move through phases sequentially; don't start Phase 4 until Phase 1-3 are stable

---

**Last Updated:** October 12, 2026  
**Version:** 1.3 (Phases 1 & 2 Complete, Phase 3 Pending)  
**Maintained By:** System Agent  

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **3.1** | `config/weights.yaml` | `.agents/skills/story-prompts/config/weights.yaml` | PENDING | Configurable scoring weights and thresholds | Agent reads configuration for different use cases (cinematic, intimate, action) | Load YAML; Validate schema; Apply to scoring formula | None (standalone config) |
| **3.2** | `config/temporal_rules.yaml` | `.agents/skills/story-prompts/config/temporal_rules.yaml` | PENDING | Configurable temporal distribution rules | Agent reads frame count ranges and corresponding selection rules | Parse YAML; Match clip duration to rule set; Return appropriate frames | `selection_optimizer.py` |
| **3.3** | `tests/test_scoring_engine.py` | `.agents/skills/story-prompts/tests/test_scoring_engine.py` | PENDING | Unit tests for scoring calculations | Agent provides test cases (edge cases, boundary conditions) | Run pytest; Validate score outputs; Test threshold filtering | `scoring_engine.py`, `quality_metrics.py` |
| **3.4** | `tests/test_buffer_manager.py` | `.agents/skills/story-prompts/tests/test_buffer_manager.py` | PENDING | Unit tests for buffer operations | Agent provides test scenarios (empty buffer, full buffer, partial) | Run pytest; Validate file I/O; Test atomic operations | `buffer_manager.py`, `buffer_validator.py` |

---

### Phase 4: Integration & Documentation (Future Enhancement)

| # | Module Name | File Path | Status | Description | NLP Responsibilities | Python Responsibilities | Dependencies |
|---|-------------|-----------|--------|-------------|---------------------|------------------------|--------------|
| **4.1** | `integration_tests/` | `.agents/skills/story-prompts/integration_tests/` | PENDING | End-to-end integration tests for full pipeline | Agent orchestrates multi-module test scenarios | Run pytest; Validate end-to-end flow from input to output | All Phase 1-3 modules |
| **4.2** | `docs/api_reference.md` | `.agents/skills/story-prompts/docs/api_reference.md` | PENDING | API documentation for all new Python modules | Agent provides usage examples and code snippets | Document function signatures, parameters, return types | All Phase 1-3 modules |
| **4.3** | `README_MODULARIZATION.md` | `.agents/skills/story-prompts/README_MODULARIZATION.md` | PENDING | Updated skill documentation reflecting modular architecture | Agent explains new workflow and module interactions | Include diagrams, flowcharts, version info | All Phase 1-4 modules |

---

## 🔄 Current Workflow vs. Target Workflow

### **Current (Monolithic) Workflow:**
```
NLP Agent:
1. Validation → 2. Research → 3. Structuring → 4. Drafting → 5. Processing → 6. Transformation
   ↓
Single Script: buffer_manager.py (handles initialization, frame addition, state management)
```

### **Target (Modularized) Workflow:**
```
NLP Agent:
1. Validation → 2. Research → 3. Preprocessing
   ↓
4. Structuring (Call structure_builder.py) 
   ↓
5. Scoring (Evaluate via quality_metrics.py + scoring_engine.py)
   ↓
6. Selection (Apply rules via selection_optimizer.py)
   ↓
7. Drafting (Invoke prompt-formula for each frame)
   ↓
8. Processing (Execute enhanced buffer_manager.py)
   ↓
9. Transformation (Call output_transformer.py)
```

---

## 📈 Progress Dashboard

| Phase | Module Count | Completed | In Progress | Pending | % Complete |
|-------|--------------|-----------|-------------|---------|------------|
| **Phase 1: Core Utilities** | 5 | 2 | 0 | 3 | 40% |
| **Phase 2: Enhanced Buffer** | 2 | 0 | 0 | 2 | 0% |
| **Phase 3: Config & Testing** | 4 | 0 | 0 | 4 | 0% |
| **Phase 4: Integration & Docs** | 3 | 0 | 0 | 3 | 0% |
| **TOTAL** | **14** | **2** | **0** | **12** | **14%** |

---

## 🎯 Success Criteria

- [ ] All Phase 1 modules created and tested ✅ (2/5 complete)
- [ ] Enhanced buffer manager replaces current `buffer_manager.py`
- [ ] Scoring engine produces consistent results with original formula
- [ ] Selection optimizer correctly applies temporal/action rules
- [ ] Output transformer maintains schema compliance ✅
- [ ] Unit tests cover 80%+ of code coverage

---

## 📝 Notes & Assumptions

1. **NLP Agent Responsibilities:** Semantic understanding, decision making, metric evaluation (0-100 scale), rule interpretation
2. **Python Script Responsibilities:** Data transformation, calculation, file I/O, state management, validation
3. **Backward Compatibility:** New modules should work with existing `SKILL.md` workflow initially
4. **Progression:** Move through phases sequentially; don't start Phase 3 until Phase 1-2 are stable

---

**Last Updated:** October 12, 2026  
**Version:** 1.2 (Two Modules Complete & Tested)  
**Maintained By:** System Agent  
