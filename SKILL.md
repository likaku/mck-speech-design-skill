---
name: mck-speech-design-skill
description: "Generate tailored, persona-fitted speech scripts and presentation talking points from user-provided materials (slides, briefs, notes, docs). This skill should be used when a user wants to write a speech, create talking points, draft a keynote script, prepare presentation notes, or generate an executive speaking framework. It guides a structured briefing process to understand the speaker's persona, audience, relationship context, event format, language, duration, and objectives — then produces a complete, ready-to-deliver speech script with per-slide/section timing, transitions, and speaker notes. When the user provides a PPTX file, the skill automatically writes the generated script back into each slide's speaker notes. Trigger on mentions of: speech, keynote, talking points, presentation script, speaking notes, executive exchange, pitch deck script, or conference talk preparation."
---

# McKinsey Speech Design Skill

Generate tailored, persona-fitted speech scripts from user-provided materials through a structured briefing and drafting workflow. When the source material is a PPTX file, automatically write the script back into each slide's speaker notes.

## Overview

This skill transforms raw materials (slide decks, briefs, notes, strategy docs) into polished, ready-to-deliver speech scripts. The key differentiator: every speech is fitted to the speaker's specific persona, audience relationship, and event context — not generic.

The workflow has 3 stages (+ an automatic 4th stage for PPTX input):
1. **Briefing**: Gather context about speaker, audience, relationship, event, objectives, language, and **speaking style reference**
2. **Architecture**: Design the speech structure, timing, and narrative arc (McKinsey Pyramid Principle)
3. **Drafting**: Write the full script with per-section talking points, transitions, and speaker notes — **informed by the chosen style reference**
4. **PPTX Injection** *(auto-triggered when input is .pptx)*: Write the script back into the PPTX file's speaker notes

## Dependencies

This skill requires the following Python packages:

| Package | Version | Used By |
|---------|---------|---------|
| `python-pptx` | ≥0.6.21 | inject_notes.py, PPTX extraction fallback |
| `python-docx` | ≥0.8.11 | speech_to_docx.py |

Install: `pip install python-pptx python-docx`

**Note**: `markitdown` is optional (used for PPTX text extraction but has a fallback).

## Stage 1: Briefing

Collect context through conversation before writing anything. Do NOT start drafting until sufficient context is gathered.

### Detect Input Type

First, check what the user has provided:
- **If PPTX file (.pptx)**:
  1. First try: `python -m markitdown <file.pptx>` to extract text content.
  2. If markitdown fails or returns empty: Fall back to python-pptx extraction:
     ```python
     from pptx import Presentation
     prs = Presentation("file.pptx")
     for i, slide in enumerate(prs.slides, 1):
         texts = []
         for shape in slide.shapes:
             if shape.has_text_frame:
                 texts.append(shape.text_frame.text)
         print(f"--- Slide {i} ---")
         print('\n'.join(texts))
     ```
  3. Also note the total slide count. Set `input_type = "pptx"` — this triggers Stage 4 later.
- **If images/screenshots**: Analyze the visual content directly.
- **If documents (.docx, .pdf, .md)**: Read the content with appropriate tools.

### Required Information (collect in priority order)

**Priority 1 — Must have before any drafting:**

1. **Source materials**: Ask for the slide deck, brief, or docs to base the speech on. Read all provided files thoroughly.
2. **Speech language**: "What language will you deliver this speech in?" — The script will be written in this single language only. Do not produce bilingual versions unless explicitly requested.
3. **Total duration**: "How long is your speaking slot?" — Including or excluding Q&A.
4. **Speaker persona**: Name, title, organization, role in this event. "How should you introduce yourself?"
5. **Core objective**: "If the audience remembers one thing, what should it be?"

**Priority 2 — Ask next, based on what's still missing:**

6. **Audience profile**: Who's in the room — titles, seniority, organization, knowledge level.
7. **Relationship context**: First meeting or ongoing? What's been discussed before? What's the rapport level?
8. **Event type**: Keynote, roundtable, pitch, workshop, executive exchange?
9. **Tone preference**: Formal, conversational, data-driven, inspirational? See [references/tone-and-style-guide.md](references/tone-and-style-guide.md) for the full spectrum.
10. **Speaking style reference** *(NEW)*: Present the style menu from [references/speech-style-guide.md](references/speech-style-guide.md) and let the user pick a style to reference. See details in the [Speaking Style Reference](#speaking-style-reference) section below.
11. **Must-include / must-avoid**: Topics that absolutely must or must not appear.

**Priority 3 — Nice to have, ask if time allows:**

12. **Likely skepticisms**: What doubts might the audience bring?
13. **Case studies or data points**: Specific numbers, stories, or examples to highlight.
14. **Call to action**: What should the audience do after the speech?
15. **Other speakers**: Who else is presenting? What are they covering?
16. **Cultural considerations**: Formality norms, humor appetite, directness level.

For the complete checklist with example prompts, see [references/context-gathering-checklist.md](references/context-gathering-checklist.md).

### Speaking Style Reference

This is a **new feature** that lets the user choose a famous speaker's style as a flavor reference for the speech script.

**How to present**: When asking Priority 2 questions, display the following category menu and ask the user to pick one (or skip):

---

> **🎤 演讲风格参考（可选）**
>
> 你可以选择一位名人的演讲风格作为参考，我会在写台词时融入TA的节奏、用语习惯和叙事方式。
>
> | # | 分类 | 可选风格 |
> |---|------|----------|
> | **一** | **科技圈领袖** | 1. Elon Musk · 2. Steve Jobs · 3. Donald Trump · 4. Jeff Bezos |
> | **二** | **中国商业领袖** | 5. 马云 · 6. 任正非 · 7. 雷军 · 8. 周鸿祎 · 9. 刘强东 |
> | **三** | **阿里系（按职级）** | 10. P7-P8 · 11. P9 · 12. P10 · 13. P11-P12 |
> | **四** | **字节系** | 14. 张一鸣 · 15. 字节中高层通用 |
> | **五** | **华为系** | 16. 任正非 · 17. 余承东 · 18. 华为中高层通用 |
> | **六** | **腾讯系** | 19. 马化腾 · 20. 腾讯中高层通用 |
> | **七** | **经典演说家** | 21. 马丁·路德·金 · 22. 奥巴马 · 23. 丘吉尔 |
> | **八** | **新生代网红/意见领袖** | 24. 罗振宇 · 25. 俞敏洪 · 26. 李开复 · 27. 罗永浩 |
>
> 选一个编号，或回复"不需要"跳过。

---

**After user selects**: Read the corresponding style profile from [references/speech-style-guide.md](references/speech-style-guide.md). Note the key attributes:
- Speaking tempo and rhythm
- Humor type
- Narrative structure
- Signature phrases and sentence patterns
- Emotional arc
- Vocabulary level

**Store the selection** as `style_reference` for use in Stage 3.

### Briefing Guidelines

- Ask 3-5 questions per message, not all at once. Start with Priority 1.
- Accept answers in any format — shorthand, bullet points, info dumps.
- If the user provides reference documents, read them fully and extract: key themes, data points, organizational structure, implicit audience assumptions.
- Infer what you can from provided materials — don't ask questions already answered in the docs.
- When enough context is gathered (all Priority 1 items answered), confirm understanding with a brief summary and ask if anything is missing before moving to Stage 2.

## Stage 2: Architecture

Design the speech structure before writing prose.

### Select a Structure Pattern

Based on event type and objectives, select from the patterns in [references/speech-structure-patterns.md](references/speech-structure-patterns.md):

| Event Type | Recommended Pattern |
|-----------|-------------------|
| Client/partner meeting | Executive Briefing |
| Conference keynote | Thought Leadership |
| Sales/partnership pitch | Pitch/Proposal |
| Training/workshop | Workshop/Interactive |

### Build the Timing Table

Create a section-by-section or slide-by-slide timing allocation:

```markdown
| Section / Slide | Topic | Duration |
|----------------|-------|----------|
| S1 | Opening & Framing | ~3 min |
| S2 | [Topic] | ~2 min |
| ... | ... | ... |
| Total | | ~[X] min |
```

Use pacing guidelines from the structure patterns reference:
- ~130-150 words per minute spoken
- Chapter dividers: 0 min
- Data-heavy sections: 1.5-2x average time
- Buffer 15-20% for pauses and audience reactions

### Define the Narrative Arc (Pyramid Principle)

Apply the **McKinsey Pyramid Principle** (Barbara Minto) to structure the narrative:

1. **Top-down conclusion first**: Open with the single overarching message — the "so what" — before presenting supporting evidence. The audience hears the answer, then the reasoning.
2. **MECE grouping**: Organize supporting arguments into 2-4 mutually exclusive, collectively exhaustive groups. Each group is a chapter/section of the speech.
3. **Vertical logic**: Each level answers "why?" or "how?" from the level above. If the top-level claim is "X is the right approach," each chapter proves one pillar of that claim.
4. **Horizontal logic**: Within each group, points follow either:
   - **Deductive order** (major premise → minor premise → conclusion)
   - **Inductive order** (similar facts → pattern → insight)
5. **Situation–Complication–Resolution (SCR)**: Use this as the opening frame:
   - **Situation**: Common ground the audience already agrees with
   - **Complication**: The tension, change, or problem that disrupts the status quo
   - **Resolution**: Your key message / thesis (= the pyramid's apex)

Then fill in:
- **Opening frame**: SCR hook — situation the audience recognizes → complication that creates urgency → your resolution (the core message)
- **Core thread**: 2-4 MECE supporting pillars, each with its own evidence layer
- **Closing frame**: Restate the apex message, synthesize the pillars, and deliver the call to action

Present the architecture to the user for approval before proceeding to Stage 3.

## Stage 3: Drafting

Write the complete speech script section by section.

### Script Format

**When input is PPTX** — map each section to its corresponding slide number. This mapping is critical for Stage 4 (auto-injection into speaker notes).

For each section, produce:

```markdown
## [Section Title] — Slide [N]

### Purpose
[One sentence: what this section accomplishes]

### Talking Points
- [Key point 1]
- [Key point 2]
- [Key point 3]

### Script
[Full spoken text, written in the designated language]

### Transition → Next Section
> "[Bridge sentence to the next topic]"
```

### Writing Principles

1. **One language only**: Write the script in the language specified during briefing. Do not produce dual-language versions unless the user explicitly requests bilingual delivery.

2. **Fit the persona**: The script should sound like *this specific person* speaking — matching their seniority, style, and relationship with the audience. A CEO sounds different from a product manager. A first meeting sounds different from a fifth.

3. **Apply the style reference** *(NEW)*: If a `style_reference` was selected in Stage 1, weave its characteristics into the script as a **flavor layer**:

   - **Borrow 3-5 signature phrases or sentence patterns** from the selected style — adapt them to the speech content, don't copy verbatim. For example, if the user chose "Elon Musk", transform a technical insight into: *"What people don't realize is... [insight]. And that's... that's actually insane when you think about it."*
   - **Match the emotional arc**: E.g., Musk = flat baseline → excited at vision moments; Jobs = controlled buildup → dramatic reveal; 马云 = storytelling warmup → inspirational climax.
   - **Adopt the humor style**: E.g., Musk's cold/meme humor, 周鸿祎's roast-style directness, 罗永浩's self-deprecating comedy, 雷军's wholesome data-nerd enthusiasm.
   - **Mirror the vocabulary level**: E.g., Trump = extremely simple repetitive words; 任正非 = literary/military metaphors; 张一鸣 = precise analytical language.
   - **Use the narrative structure**: E.g., Musk's "problem → current approach is absurd → first principles → solution"; Jobs's "buildup → One more thing → reveal"; 马云's "skepticism → reversal → deeper truth → golden quote".
   - **Intensity calibration**: If the user's actual seniority/context differs significantly from the chosen style (e.g., a junior engineer referencing "Alibaba P11-P12"), **tone down the intensity by 50%** while keeping the flavor. The style is inspiration, not cosplay.

4. **Trust-building tone**: Default to transparency and fact-based persuasion. Avoid over-promising. Acknowledge limitations honestly. Let data speak. See [references/tone-and-style-guide.md](references/tone-and-style-guide.md) for detailed guidance.

5. **Self-Q&A technique**: Where appropriate, pose questions the audience is likely thinking, then answer them. This creates engagement and demonstrates empathy. Use sparingly — 3-5 times per 30-minute speech.

6. **Concrete over abstract**: Use specific numbers, named examples, and tangible comparisons instead of vague claims.

7. **Natural spoken rhythm**: Short sentences (10-20 words average). Vary pace. Use **bold** for words to stress. Use em-dashes for pauses. Front-load key information.

8. **Transitions are mandatory**: Every section must end with a bridge to the next. Never have abrupt topic shifts.

9. **Timing discipline**: Each section's word count should match its allocated time at 130-150 words/minute.

### Drafting Process

1. Draft sections sequentially following the approved architecture
2. After completing the full draft, do a coherence review:
   - Check for consistency in tone and terminology across sections
   - Verify timing adds up to the allocated total
   - Ensure transitions flow naturally
   - Confirm all must-include topics are covered and must-avoid topics are absent
   - **Verify style reference consistency**: If a style was selected, check that the chosen flavor is present throughout (not just in the opening) — signature phrases should appear in opening, middle, and closing sections
3. Present the complete draft to the user
4. Iterate based on feedback — use targeted edits, not full rewrites

### Output Deliverables

The final output includes:

1. **Speech script** (markdown) — Complete section-by-section script with per-slide talking points and transitions
2. **Timing overview table** — Section-by-section time allocation
3. **Speaker preparation notes** (appendix) — Key data points to memorize, potential Q&A topics, tone reminders, **and a summary of the applied style reference with 5 key phrases to practice**

## Stage 4: PPTX Injection (Auto-triggered)

**This stage runs automatically when the user's input was a .pptx file.** No need to ask — just do it.

### What goes where

| Content | Location |
|---------|----------|
| Per-slide **Script** + **Transition** only | **Each corresponding slide's** speaker notes |
| Timing overview, Q&A prep, tone reminders, talking points | **Markdown speech file only** (NOT injected into PPT) |

> **Design principle**: Speaker notes in PowerPoint should be *concise and scannable* during presentation. Detailed preparation materials (timetable, Q&A, talking points, purpose) belong in the separate markdown/Word deliverable, not cluttering the notes pane.

### Per-Slide Notes Format

For each slide, the injected speaker note should contain **only** the script and transition — clean, readable plain text:

```
[Script]
Full spoken text for this slide...

[Transition] → Bridge sentence to next section
```

Do NOT include `[Purpose]`, `[Talking Points]`, timing tables, Q&A preparation, or tone reminders in the PPT notes. Those belong in the markdown speech file.

### Injection Workflow

1. **Generate the notes JSON**: After drafting is complete, produce a JSON file **using a Python script** (do NOT manually write JSON with `write_to_file`).

> ⚠️ **Critical**: When the speech content contains non-ASCII characters (Chinese, Japanese, special punctuation like `""`, `——`), you MUST generate the JSON programmatically to avoid encoding issues:
>
> ```python
> import json
> slide_notes = {
>     "1": "第一页的演讲内容...",
>     "2": "第二页的演讲内容...",
> }
> with open('notes.json', 'w', encoding='utf-8') as f:
>     json.dump({"slide_notes": slide_notes}, f, ensure_ascii=False, indent=2)
> ```
>
> This ensures all special characters are properly escaped.

The JSON structure:

```json
{
    "slide_notes": {
        "1": "[Script]\nFull spoken text for slide 1...\n\n[Transition] → Bridge to next section",
        "2": "[Script]\nFull spoken text for slide 2...\n\n[Transition] → Bridge to next section",
        "3": "[Script]\nFull spoken text for slide 3..."
    }
}
```

> Note: The JSON contains **only** `slide_notes`. There is no `cover_note` field.
> Each slide's value contains only `[Script]` and `[Transition]` — no Purpose, Talking Points, timing, or Q&A.

2. **Run the injection script**:

```bash
python scripts/inject_notes.py <original.pptx> <notes.json> [output.pptx]
```

The script path is relative to the skill root. Locate it with:
```bash
find . -name "inject_notes.py" -path "*/mck-speech-design-skill/*"
```

If the script is not available locally (e.g., skill loaded via GitHub URL), download it:
```bash
curl -o inject_notes.py https://raw.githubusercontent.com/likaku/mck-speech-design-skill/main/scripts/inject_notes.py
```

3. **Verify** (automated): The injection script includes built-in in-memory verification — it validates all notes are correctly set before saving, without re-reading the file from disk. If you need an independent post-hoc check:

```python
from pptx import Presentation
prs = Presentation("output.pptx")
for i, slide in enumerate(prs.slides, 1):
    if slide.has_notes_slide:
        text = slide.notes_slide.notes_text_frame.text
        print(f"Slide {i}: {len(text)} chars ✅")
    else:
        print(f"Slide {i}: NO NOTES ❌")
```

If any slide shows ❌ or the file cannot be opened, fall back to manual delivery mode.

4. **Deliver**: Present the output file to the user. The user now has a PPTX with all speech content embedded in speaker notes — ready to present.

### If injection fails

If the Python script encounters errors:
1. Fall back to manual mode: output the markdown speech script as a separate file
2. Inform the user that notes could not be auto-injected
3. Provide the notes JSON file so they can use it with other tools

### Export to Word (Automatic)

After PPTX injection, **always** also export the full speech markdown file to a `.docx` Word document. This is the complete reference document containing all preparation materials.

Run the export script:

```bash
python scripts/speech_to_docx.py <speech.md> [output.docx]
```

The script path is relative to the skill root. It converts the markdown speech file into a professionally formatted Word document with:
- Title and speaker info header
- Timing overview table
- Section-by-section script with clear headings
- Q&A preparation section
- Key data points appendix
- Speaker notes / tone reminders

The user receives **two deliverables**:
1. **PPTX** with speaker notes (Script + Transition only — scannable during presentation)
2. **Word document** with the full speech content (complete reference for preparation)
