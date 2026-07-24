# Changelog

## 2026-07-23 (evening) — the multiverse gets a face

### The unfold moment

- **Multiverse wall** on the results page: twelve of the ten thousand worlds as
  cinematic tiles (representative four + two per outcome band, deduped by seed —
  verified 12/12 unique, all five outcomes covered). Tiles stagger-fade in after
  the stats land — the moment the multiverse actually *opens*.
- **Step into any world**: full-screen overlay with a Ken Burns still header,
  the world's fate line, its final stats, and the complete timeline with
  `· watch` moments. ESC returns to the wall.
- **10 pre-rendered scene images** (`assets/worlds/`, ~100 KB each after
  JPEG compression, watermark cropped): two per outcome — rings on a rainy
  windowsill, an airport suitcase at night, two phones face down at 2am,
  keys on an empty table… all in the app's neon-on-black palette.

### De-geeked

- Copy pass across every scene: "A Monte Carlo engine for one relationship" →
  *"Somewhere, you said yes. Somewhere, you didn't."* · "SIMULATION COMPLETE" →
  *"Ten thousand lives, lived"* · "worlds simulated" → *"futures lived"* ·
  "Run simulation" → *"Live ten thousand lives"* · "10,000 WORLDS DIVERGING" →
  *"EVERY CHOICE SPLITS"* · "COLLAPSING INTO STATISTICS" → *"EVERY UNIVERSE CHOOSES"*.

### Two nasty bugs found by live verification

- `pick` name collision: the dialogue fallback's `pick(jr, arr)` overwrote the
  engine's `pick(arr)` across script blocks, crashing every simulation start.
  Renamed to `pickJ`.
- TDZ cascade: `llmFab()` ran in the boot section *before* `const LLM` was
  initialized — one ReferenceError silently killed the entire script's tail
  (J/A shortcuts, permalink boot, wall data). Moved to the last line of the
  script. Lesson: in one big script, boot calls go last.
- Live-verified end-to-end: 12-tile wall renders with images, world overlay
  opens (17/17 moments clickable), moment dialogue plays (engine-grounded),
  89 fps jump, permalink + autopilot + J all alive again.

## 2026-07-23 (later) — performance + the agents get a voice

### Performance (the lag is gone)

- Jump animation re-architected: phase B now accumulates worldlines on an
  **offscreen canvas** and blits once per frame; phase C crossfades between the
  diverged layer and a **pre-baked converged layer** — zero per-frame polyline
  stroking (was 800 × 183 lineTo per frame).
- strokeStyle strings cached (5 colors × 13 mix steps); color-mix hoisted out of
  the per-line loop.
- Adaptive quality: frame-time EMA > 26 ms → alternate lines update per frame.
- Measured in a foreground tab: **89 fps** through divergence and convergence.

### The two agents, talking

- Every logged event now carries a **state snapshot** (trust / affection /
  communication / stress / commitment / LD flag at that day) — verified headless:
  34/34 entries.
- World-timeline rows gained a `· watch` affordance: opens a dialogue overlay
  where the two agents text each other through that exact moment, driven by
  persona + that world's numbers.
- **LLM channel**: settings panel (bottom-left `LLM · OFF`), any
  OpenAI-compatible endpoint (`/chat/completions`), key persisted in
  localStorage only, one-click connection test. With a key, dialogue is a live
  4-turn agent exchange (each turn conditioned on persona, state snapshot, and
  the partner's previous lines). Without a key, an engine-grounded fallback
  renders the same snapshot into words — deterministic, honestly labeled.
- ESC closes overlays; `LLM · LIVE` indicator when configured.

## 2026-07-23 — autonomous /loop, 10 goals (G1–G10)

All verified in a real browser (WebBridge-driven Chrome) and, where applicable,
by headless engine runs of 5,000–10,000 worlds per scenario.

### Engine

- **G1 — Event library 17 → 23.** New events fill the quiet middle years:
  therapy, rekindle, anniversary rituals, money-alignment talks, and more.
  Events now support cooldowns (`cd` days) so rare events stay rare.
- **G2 — Engine pressure test.** Five extreme persona combos × 5,000 worlds each.
  Fixed: stress floor now scales with attachment/conflict traits
  (`sFloor = 20 + anx·4 + avd·3 + avoA·6`); career gap > 0.5 halves
  long-distance refusal and reconciliation rates; proposal requires
  commitment > 68 && trust > 48; a postponed wedding closes the marriage path
  (`postponed` flag); marriage ending requires commitment > 70 && trust > 50
  && stress < 64 && !postponed && 85% roll.
  Result — default Oscar×Mira: 32 married / 26 cold war / 19 dating / 16 breakup / 8 LD.
  Both-avoidant: 60 cold war. Both-anxious: 48 married but 28 breakup (volatile).
  Extreme career gap: 59 married, 26 LD. Both-secure-family: 88 married.
  No NaN, no collapse, all directions plausible.
- Fixed latent `avgWorld` bug (`Math.floor(sortedByHealth/2)` → `.length/2`).

### Experience

- **G3 — Sensitivity analysis.** Results page: *What actually moves your futures.*
  Six what-ifs (each twin secure, both repair, each career-priority −0.3,
  money values aligned), rerun on the same 10,000 seeds, ranked by |Δpp|.
  Verified live: "both repair" +22.1 pp, "money aligned" +10.3 pp,
  "Oscar secure" +9.1 pp on the default twins.
- **G4 — The average five years, in one line.** Mean relationship-health
  trajectory across all worlds, inline SVG sparkline with a gold endpoint.
- **G5 — Jump event ticker.** During divergence, witnessed moments from random
  worlds fade in at bottom-left (`WORLD #9503 · DAY 1800 — …`).
  Interval-driven so it survives background-tab rAF stalls.
- **G6 — Autopilot.** Press **A** on the hero: the whole demo runs itself
  (twins → JSON → jump → results), ESC aborts. Verified end-to-end.
- **G7 — Shareable multiverses.** Every run writes a `#t=<base64url>` permalink
  (twins + run salt). Opening it replays the *identical* universe — verified
  byte-for-byte same headline (32% married). *Copy this multiverse* button on
  the results page.
- **G8 — Meta/OG/noscript.** Description, OG tags, theme color, and a styled
  no-JS fallback page.
- **G9 — Mobile pass (390×844).** Verified hero/twins/results via device
  emulation. Fixed: world tabs wrap with smaller type, sensitivity rows stack,
  jump ticker widens to 72vw. (Also confirmed hero fade-up delay in QA was
  background-tab timer throttling, not a bug.)

### Prior loop (same day, earlier)

- Google Fonts no longer blocks first paint (`media=print` onload swap).
- Jump animation: four phases (tear / diverge / converge / silence) with
  WebAudio score and SOUND toggle; overexposure fixed (alpha 0.15/0.14);
  legend moved top-left; safety timeout lands on results even in hidden tabs.
- Counterfactuals: erase a moment type from every world, same seeds rerun
  (measured: erasing `move_city` moved marriage 45.3% → 56.7% on an earlier
  engine tune).
- J shortcut from anywhere; results page reruns on J.

## 2026-07-25 — the multiverse gets merch, a letter, and a second playthrough

Driven by the Kimi Code CLI loop (every 5 min, backlog in `.qa/_backlog_win.md`,
progress ledger in `.qa/_loop_progress.md`). All CDP-verified, console-clean,
390×844 overflow-free. Backup chain now at `index-v15-cn.html`.

### Story first, quiz dead (commit 0994655, awaiting Oscar's sign-off to deploy)

- **Fill-in-the-blank narrative input** replaces the persona sliders as the
  default: "还记得你们上次吵架吗？因为 ___。后来 ___ 先开了口，说了句 ___。
  那一刻，你心里想的是 ___。" — 25 spoken-word options across four blanks map
  covertly to the nine engine parameters (engine untouched; the raw sliders
  live on inside a fold-out "我懂心理学，直接调参数" panel; controls stay the
  single source of truth).
- **The reveal**: results page gets a horoscope-toned verdict line
  ("宇宙批注 · 你们吵架的模式：冷战高手 × 冷战高手。建议备点小纸条……"),
  nine conflict-style combos × two punchlines each.
- **Name editing on results**: click a name, retype, hit 重新算 — same salt
  ladder. If the top outcome flips, a toast confesses:
  "你以为你改的是名字，其实你改的是宇宙。"
- **Temperature copy system**: five outcome-pools × six lines, warm teasing
  for marriage/dating, only gentleness for breakup, neutral for cold war/LD.
  Marquee + headline pools destructively edited (16 rewritten, 6 deleted —
  zero 排比/鸡汤/「震撼」left).
- Loop-agent wreckage repaired along the way: five duplicated `],` syntax
  errors, a naked `#adv-panel`, an `.out-headline` flex overlap, a null
  `pickChip`.

### Motion quartet (already live, commit b27de08 era)

- Jump gains a 0.9s chaos prelude — all 1,200 worldlines explode outward
  (70→30 Hz boom) before diverging; screen-shake finale when the five
  streams converge. Runtime 4.7s → 5.6s, offscreen architecture untouched.
- Timeline key events carry icons (💍⚡✈️💔, id- and keyword-matched,
  LLM-rewrite-safe) with a 1.2× pulse, reduced-motion exempt.
- Moment dialogues boot like a CRT (0.32s horizontal-line unfold).
- Universe openings flash a hand-drawn 5×7 dot-matrix `UNIVERSE #…`
  that dissolves pixel by pixel.

### Keepsakes & doubles — Tripo 3D (sponsor track, visibly used)

- **14 universe keepsakes** (two leaning pebbles, a cat loaf, tangled
  earphones, a bowl of luosifen…): Tripo text-to-3D → weld/simplify 8%/
  quantize → 216K–2.4M GLBs (`assets/keepsakes/`, raw 176MB archived in
  `_gen/`). Static renders in `assets/keepsakes/render/` double as the
  file:// fallback and the ID-card stamp.
- **Chibi Tomodachi-style doubles** for Oscar & Mira (756K/684K).
- model-viewer **UMD** vendored to `assets/lib/` (v4 ships ESM only — dead
  on file://; v3 UMD double-clicks fine). `keepsakes-gallery.html` (16
  models, 18MB single file) and `avatars-proto.html` tour the whole set.
- Integration plan for the acceptance window: `.qa/_keepsake_integration.md`.

### Share & second-play loop

- **Handwritten zero-dependency QR generator** (`qr-proto.html`): byte mode,
  EC-M, auto version 1-10, RS over GF(256), format+version info — verified
  scannable by independent OpenCV decode (site URL, 110-char permalink,
  Chinese text), not by eyeball.
- **Share landing page**: `#t=` links now arrive as a letter
  ("有人给你寄了一万个宇宙 · A × B · 拆开看看 / 也算算我们的 →") instead of
  an instant jump — the judge-facing "play it with YOUR names" loop closes.
- Counterfactuals & sensitivity demoted to an easter egg ("给工程师和杠精
  看的部分 →") — fate first, engineering on request (second LLM review,
  `.qa/review2.md`).
- Timeline gains a **poignancy layer** (old movie stubs / 3am fever run /
  the old code word at the reunion) — rare (w≈0.17), late-game only,
  smoke-tested over 3,000 engine runs.

### Docs

- `DEMO.md` rewritten as a 3-minute run-of-show (fill-in laugh → explosion
  wow → reveal laugh → 1s rock-universe flash → keepsake hands-on → ID card
  → "pull out YOUR phone" CTA); fallback counterfactual beat kept for
  technical judges.
- `README.md` re-aligned: story input, Tripo pipeline, principles updated
  ("Absurd ≠ childish" replaces the dead "Never cute").
