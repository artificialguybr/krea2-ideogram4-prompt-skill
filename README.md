# Krea 2 / Ideogram 4 Prompting — an agent skill for two image models

An [agent skill](https://github.com/anthropics/skills) for high-quality prompt engineering on **Krea 2** (RAW / Turbo / hosted) and **Ideogram 4.0** (natural language, structured JSON, Magic Prompt, Canvas/Edit) — plus **Ideogram 3.0 Edit** for pixel-preserving local edits.

The two models are conceptual relatives (both LLM-encoded, not CLIP), but their syntaxes do not interchange: Krea 2 wants dense natural prose; Ideogram 4 wants declarative hierarchy or JSON. This skill keeps them straight so prompts land in the right contract every time.

## What it does

- **Routes before writing.** A 12-row intent table picks model × surface × goal first — create from zero, strict layout control, style reference, moodboard, region edit, identity edit, inpaint/outpaint, typography, reverse-prompting, failure repair, genre presets — then loads exactly one reference file.
- **Non-negotiable guardrails on every output:** no quality-keyword confetti (`masterpiece, best quality, 8k…`), no SD-style weights `(word:1.3)` (Krea 2 ignores them — use restatement), rendered text always in double quotes and early in the prompt, one change per edit instruction, describe the *result* not the *operation*, positive constraints instead of negative prompts where the surface has no negative field.
- **Structured JSON for Ideogram 4** with the observed schema and sampler presets, plus a bundled validator:

  ```sh
  python scripts/validate_ideogram4_json.py my_prompt.json
  ```

- **Consistent output profile** — every delivered prompt comes as `FINAL PROMPT (EN)` plus positive constraints, negative prompt when the workflow supports one, suggested settings, and the single variable to change next iteration.
- **Failure diagnosis table** — symptom → likely cause → exact reference section (melting edits, style swallowing the subject, late text rendering wrong, whole-image regeneration on 4.0 Edit, etc.).

## Install

Copy the folder into your agent's skills directory (Claude-style harnesses: `~/.claude/skills/`; also works with Kimi/Codex skill folders):

```sh
git clone https://github.com/artificialguybr/krea2-ideogram4-prompt-skill.git
cp -R krea2-ideogram4-prompt-skill ~/.claude/skills/
```

`SKILL.md` loads on demand; the eight reference files load lazily — keep relative paths intact. See `INSTALL.md` for details and maintenance notes.

## Usage

Ask in plain language; the skill picks the route:

- "Make a minimal poster with the title 'SOLARIS' in big serif type." → typography reference.
- "Keep this person's face but put her in the black bodysuit." → Krea 2 Identity Edit rules.
- "Extend this photo to 16:9 keeping the left half untouched." → Ideogram Canvas Extend.
- "Only change the clock time in this photo, keep everything else pixel-identical." → routed to Ideogram **3.0** Edit (4.0 regenerates the whole image).

Final prompts are written in **English** (both models respond best to it); explanations and routing questions come in Portuguese.

## Structure

```text
SKILL.md                        # golden rule: route first; guardrails; output profile
INSTALL.md                      # install + maintenance pointers
references/model-facts.md         # per-variant parameters and quick facts
references/krea2-architecture.md # Krea 2 T2I, style reference, moodboard
references/ideogram4-json.md      # structured JSON schema, Magic Prompt, presets
references/editing.md            # Krea Edit, Identity Edit, Canvas, Ideogram 3.0 Edit
references/typography.md          # rendering text inside images
references/reverse-prompting.md  # extract/recreate prompts from images
references/failure-repair.md    # guardrails + symptom → fix tables
references/genre-presets.md      # shortcuts by genre
scripts/validate_ideogram4_json.py
```

## Honest limits

- The Ideogram schema here is a research reconstruction; validate against the official docs before production use — parameters change between versions.
- Ideogram 4 has **no seed and no negative_prompt** on the endpoint; the skill expresses exclusions as positive constraints instead.
- Localized edits that must preserve the rest of the image belong to Ideogram 3.0, not 4.0.

Built following the [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) structure. License: MIT.
