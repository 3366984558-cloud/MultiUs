# MultiUs

> **We don't predict love. We simulate possibility.**
> Every possible version of us.

A Monte Carlo engine for one relationship. Two Digital Twins go in;
10,000 parallel five-year futures come out — with the statistics,
the representative worldlines, and the moments that decided them.

Built for a 5-minute hackathon demo. Zero backend, zero dependencies,
zero build step. Everything — engine, animation, sound — runs in one HTML file.

## Run it

Open `index.html` in a browser. That's it.

Or serve it (Kimi Work preview / sharing):

```bash
npm run dev        # → http://localhost:7100  (node dev-server.mjs, no deps)
```

## The 5-minute demo path

1. **Hero** — "Begin the jump" (or press **J** from anywhere, **A** for full autopilot)
2. **Digital Twins** — two people, six signals each (prefilled: Oscar × Mira)
3. **Compression** — twins materialize as structured JSON
4. **The Jump** — 10,000 worldlines tear, diverge, and collapse into 5 outcome streams (sound on);
   witnessed moments from random worlds scroll by while they diverge
5. **Results** — headline stat → outcome distribution → *The average five years, in one line*
   → **the multiverse wall**: twelve worlds you can *step into*, each with its own
   cinematic still (10 pre-rendered scene images, `assets/worlds/`) — inside a world,
   its full timeline, every moment clickable (`· watch`) for the agents' dialogue
   → *Where the worlds split* → **erase a moment from every world**
   → *What actually moves your futures* → **Copy this multiverse**

Full presenter run-of-show: [DEMO.md](DEMO.md)

## Architecture

Single file, four layers, no magic:

| Layer | What it is |
|---|---|
| `EVENTS` library | 23 life events, each with weight, conditions, cooldowns, state effects, and narrative lines |
| `simulateWorld()` | Seeded RNG (mulberry32) → deterministic world; 5-day ticks, drift + events + endings |
| `runSimulation()` | 10,000 worlds; stats, representative worlds, critical-decision bookkeeping |
| `playJump()` | Canvas: tear → divergence → convergence → silence; offscreen accumulation + baked crossfade (no per-frame stroking), adaptive line stride on weak GPUs; WebAudio score |

Outcomes: `marriage · still_dating · long_distance · cold_war · breakup`.

### The two agents, talking

Every logged event carries a **state snapshot** (trust / affection / communication /
stress / commitment at that day). Click any `· watch` row in a world timeline and
the two agents have a short exchange at that exact moment — driven by their traits
and that world's numbers, never canned.

- **With an LLM key** (gear: `LLM · OFF`, bottom-left): live 4-turn dialogue, turn by
  turn, each agent conditioned on persona + state + what the other just said.
  Any OpenAI-compatible endpoint (Gemini, OpenAI, DeepSeek, Ollama…).
  Key stays in the browser's localStorage; never in the file.
- **Without a key**: the engine renders its own state into words — deterministic,
  grounded in the snapshot, and honestly labeled `ENGINE-GROUNDED`.

### Counterfactuals

Decision cards can erase one event type (e.g. `move_city`) and rerun the same
10,000 seeds without it — a true counterfactual, not a fresh roll.

### Determinism

Every world is `seed = 1000 + runSalt·104729 + i·7919`. World #0417 is a real,
reproducible universe.

## Roadmap

- [ ] LLM-distilled Digital Twins from real chat history (channel ready — endpoint/key UI shipped; next: auto-fill the six signals from pasted chats)
- [x] The two agents, talking — click any moment in a world timeline, watch them text through it (live LLM or engine-grounded)
- [x] More timelines: ~~most unexpected~~ **the wildest world** (max trajectory swing)
- [x] Sensitivity analysis (one trait changed at a time, same 10,000 seeds)
- [x] Shareable multiverse links (`#t=…` — twins + run salt, exact reproduction)
- [x] Autopilot demo mode (press **A**, the whole show runs itself)
- [ ] Sensitivity heatmap (trait × outcome)

## Principles

- Demo > perfection.
- Animate for meaning, not decoration.
- Never cute. Never a quiz. Never a chatbot.
- Insight, not prediction.
