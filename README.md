# LuaU-AIDS — Luau Agentic Training Dataset

Training data that teaches AI models **how to think and act as a Luau programming agent** — from basics to advanced systems.

**License:** MIT

## Format

3-message format: `system` → `user` → `assistant`

The assistant follows an agent workflow:
- **THINK** — Plan the approach, identify APIs, consider edge cases
- **ACT** — Write the code with proper types
- **VERIFY** — Check correctness, security, and cleanup

## Learning Progression

| Level | Topics | Count |
|-------|--------|:-----:|
| **0 — Luau Basics** | Variables, types, functions, tables, metatables, strings, control flow, errors | 6 |
| **1 — Roblox APIs** | Services, instances, player lifecycle, events/connections, remotes, CFrame/Vector3 | 6 |
| **2 — Simple Systems** | Kill bricks, shops, teleport pads, countdown timers, enemy AI, disappearing platforms | 6 |
| **3 — Intermediate** | Inventory + DataStore, raycasting, ProximityPrompt, shop GUI, camera shake | 6 |
| **4 — General** | 40+ topics covering common game dev patterns | 976 |

## Dataset

**`dataset.jsonl`** — 1,000 entries, ~937 KB

- Starts from Luau language fundamentals
- Builds up to Roblox API usage
- Covers simple then complex game systems
- Every entry shows THINK → ACT → VERIFY workflow
- 327 entries include `--!strict` code
- 30 game genre contexts

## What This Teaches

A model trained on this data will:
1. **Plan before coding** — think through architecture, APIs, and edge cases
2. **Write correct Luau** — proper types, modern APIs, no deprecated patterns
3. **Verify their work** — check for bugs, security issues, and cleanup
4. **Start from fundamentals** — explain concepts from the ground up
5. **Follow Roblox conventions** — Instance creation order, server authority, cleanup patterns
