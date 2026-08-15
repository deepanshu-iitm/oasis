# Oasis

**Brief to storyboard to launch reel.**

Oasis is an AI video director for product launches. Give it a product brief and it creates a structured production plan, a readable storyboard, and a polished vertical MP4.

Built for the OpenAI Codex Community Hackathon - Bengaluru.

## The problem

A launch video normally starts with a blank timeline: somebody has to turn a product brief into a script, decide the story arc, write on-screen copy, choose pacing, and build a video composition. That work is slow, difficult to repeat, and often blocks a product launch.

Oasis turns that workflow into one focused render lane:

```text
Product brief
  -> AI Director
  -> production plan
  -> storyboard
  -> vertical MP4
```

The goal is not to generate arbitrary video code at runtime. Oasis creates a stable, editable video plan and sends it through one reliable Remotion composition.

## What it does

- Uses an OpenAI-powered director to turn a brief into a five-beat launch arc: hook, value, product, proof, and CTA.
- Enforces a structured, renderer-safe production-plan schema.
- Runs a critique step to check timing, scene types, CTA information, and the complete beat arc.
- Writes both `plan.json` and a presenter-friendly `storyboard.md`.
- Renders a 9:16, 30 FPS MP4 whose duration is derived from the proposed beats.
- Shows every runtime tool step in the CLI, making the agent workflow visible during a demo.
- Includes a deterministic offline fallback when an API key is unavailable.

## Demo

```powershell
python -m director "Pulseboard is a collaborative planning workspace for small product teams. It turns scattered decisions into clear weekly plans." --ai --out out/demo
```

Oasis writes:

```text
out/demo/
  plan.json
  storyboard.md
  remotion-props.json
  final.mp4
```

For a fast planning-only run, skip the render:

```powershell
python -m director "A planning workspace for product teams." --ai --no-render --out out/plan-only
```

The agent logs look like this:

```text
[director] openai_director
[director] map_assets
[director] critique_plan
[director] write_outputs
[director] render_video
```

## Quick start

### Prerequisites

- Python 3.10+
- Node.js 20+
- An OpenAI API key for `--ai` mode

### Install

```powershell
git clone https://github.com/deepanshu-iitm/oasis.git
cd oasis
python -m pip install -r requirements.txt
npm --prefix remotion install
Copy-Item .env.example .env
```

Add your key to the newly created `.env` file:

```env
OPENAI_API_KEY=your_key_here
OASIS_MODEL=gpt-5.6-luna
```

`.env` is ignored by Git. Never commit or share an API key.

### Run

Use the OpenAI director and render a video:

```powershell
python -m director "Orbit is a lightweight budgeting app that helps freelancers see their cash flow clearly." --ai --out out/orbit
```

Or use the local fallback planner, which does not make an API call:

```powershell
python -m director "Orbit is a lightweight budgeting app for freelancers." --out out/orbit-fallback
```

## How it works

```text
                         +-------------------+
                         | Product brief     |
                         +---------+---------+
                                   |
                                   v
+----------------+       +-------------------+       +--------------------+
| OpenAI         | ----> | Oasis director    | ----> | VideoPlan schema   |
| Responses API  |       | + local tools     |       | + critique          |
+----------------+       +---------+---------+       +---------+----------+
                                   |                           |
                                   v                           v
                         +-------------------+       +--------------------+
                         | plan.json         |       | storyboard.md      |
                         +---------+---------+       +--------------------+
                                   |
                                   v
                         +-------------------+
                         | Remotion          |
                         | DirectorReel      |
                         +---------+---------+
                                   |
                                   v
                              final.mp4
```

### The director workflow

1. `openai_director` generates a strict JSON production plan in AI mode.
2. `map_assets` attaches optional asset references to relevant beats.
3. `critique_plan` checks the five-beat narrative, timing, scene support, and CTA.
4. `write_outputs` creates the JSON plan and Markdown storyboard.
5. `render_video` converts the plan to Remotion props and renders the MP4.

The OpenAI director uses the Responses API with structured JSON output. The default model is `gpt-5.6-luna`, chosen for cost-efficient planning; it can be changed with `OASIS_MODEL`. See the [OpenAI API quickstart](https://developers.openai.com/api/docs/quickstart) and [model guide](https://developers.openai.com/api/docs/models).

## Project structure

```text
 director/                 Python director pipeline
   ai.py                   OpenAI structured-plan generator
   agent.py                Tool workflow coordinator
   render.py               Python-to-Remotion bridge
   schema.py               Shared Brand, Beat, and VideoPlan structures
   tools/                  Parse, propose, map, critique, and output tools
 remotion/                 Props-driven 9:16 video renderer
   src/DirectorReel.tsx    Polished kinetic composition
   src/Root.tsx            Composition registration and dynamic duration
 out/                      Ignored generated plans, storyboards, and videos
```

## How Codex was used

Codex was used as an engineering collaborator, not just as autocomplete.

- It helped decompose the project into small, verifiable pieces: schema, director tools, CLI, renderer, and API integration.
- Each focused change was validated with real commands and saved in a separate Git commit.
- It helped inspect local Remotion patterns for inspiration without copying private source or assets.
- It diagnosed TypeScript and renderer issues, including dynamic timing and compatibility fixes.
- It was used to build and refine the runtime agent workflow itself: visible tool steps, plan critique, structured output, and the Python-to-Remotion bridge.

The application demonstrates the same agentic idea at runtime: an OpenAI director makes a creative decision, while explicit local tools validate, serialize, and render the result.

## Current scope

Oasis deliberately focuses on one dependable end-to-end path.

- The visual engine is kinetic, text-led motion rather than a full video studio.
- The AI director is optional; the deterministic fallback keeps planning usable offline.
- Screenshot references are stored in the plan for future visual scene support.
- Authentication, billing, multi-tenancy, voiceover generation, and multiple render engines are intentionally out of scope for the hackathon build.

## License

MIT