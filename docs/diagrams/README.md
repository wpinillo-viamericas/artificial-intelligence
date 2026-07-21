# Diagrams

Regenerable, Viamericas-themed diagrams for the Data & AI agents. Diagram-as-code so they are diffable, version-controlled, and easy to re-theme.

## Files

| File | Role | Edit? |
|---|---|---|
| `brand_palette.json` | **Single source of truth for colors** (shared by every diagram). | ✅ edit |
| `agent_operating_model.mmd.tpl` | Structure for the **portfolio / operating-model** view. Mermaid template with `{{token}}` color placeholders. | ✅ edit |
| `glue_job_monitor.mmd.tpl` | Structure for the **Glue Job Monitor** view (Option A Claude Code vs. Option B Bedrock). | ✅ edit |
| `render.py` | Generator: injects the palette into every template listed in its `DIAGRAMS` table. | ✅ edit (rarely) |
| `<name>.mmd` | Generated raw Mermaid. | ⛔ generated |
| `<name>.md` | Generated — fenced ```` ```mermaid ```` block that renders **inline on GitHub**. | ⛔ generated |
| `<name>.svg` | Generated only if `mmdc` is installed — transparent background, vector. | ⛔ generated |
| `<name>.png` | Generated only if `mmdc` is installed — white background, 2× raster. | ⛔ generated |

> The `.mmd` / `.md` / `.svg` outputs are **generated**. Never hand-edit them — change the palette or template and regenerate.
>
> **To add a diagram:** create `<name>.mmd.tpl` (use `{{token}}` placeholders from the palette) and add a `("<name>", "Title")` row to the `DIAGRAMS` list in `render.py`, then re-run.

## Regenerate

```bash
python docs/diagrams/render.py
```

- **Change colors** → edit `brand_palette.json`, re-run.
- **Change structure** (nodes, edges, labels, styling) → edit `agent_operating_model.mmd.tpl`, re-run.

`render.py` errors loudly if the template references a `{{token}}` that is not defined in the palette's `colors`.

## View / export

- **GitHub:** open `agent_operating_model.md` — it renders inline.
- **VS Code:** open `agent_operating_model.mmd` with a Mermaid preview extension.
- **Web:** paste `agent_operating_model.mmd` into <https://mermaid.live>.
- **SVG/PNG:** install mermaid-cli (`npm i -g @mermaid-js/mermaid-cli`) and re-run `render.py`; it will also emit `agent_operating_model.svg`.

## Brand colors — IMPORTANT

`brand_palette.json` currently holds a **best-effort, UNVERIFIED** Viamericas palette (deep blue + orange/gold + neutrals). Official hex codes could not be confirmed from public sources.

To make it official, do either:
1. Replace the hex values in `brand_palette.json` with the official brand-kit values, **or**
2. Drop the Viamericas logo (SVG/PNG) in the repo and color-pick the exact values.

Then run `python docs/diagrams/render.py`. That one change re-themes every diagram.

## Palette tokens

`primary`, `primary_dark`, `primary_light`, `accent`, `accent_dark`, `on_primary`, `on_accent`, `neutral`, `neutral_light`, `ink`, `surface`. Add a new token to `colors` before referencing it as `{{token}}` in a template.
