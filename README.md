# LuaU-AIDS — Luau Chain-of-Thought Training Dataset

Training data that teaches AI models **how to think about Luau engineering problems**, not just what code to produce.

**License:** MIT

## Format

Each entry: `system` → `user` (problem) → `assistant` (step-by-step reasoning + code)

The assistant response contains **explicit reasoning steps** before the code:
- What's the problem?
- What are the options?
- Why choose this approach?
- What are the edge cases?
- What security/performance concerns exist?
- Then: the implementation

## Dataset

**`dataset.jsonl`** — 1,000 entries, ~1.6 MB

| Category | Count | What it teaches |
|----------|:-----:|----------------|
| Design from requirements | 67 | Thinking through architecture before coding |
| Debug broken code | 5+ | Identifying vulnerabilities and fixing them |
| Security threat modeling | 10+ | Attack vectors and defensive patterns |
| Performance analysis | 10+ | Why code is slow, how to fix it |
| Architecture decisions | 10+ | Tradeoffs between approaches |
| Module design (15 modules) | 247 | Why each design choice was made |
| General reasoning | 600+ | Step-by-step engineering thinking |

## 15 Modules Covered with Full Reasoning

Signal, Maid, ObjectPool, Timer, CooldownSystem, HealthSystem, Inventory, SpatialGrid, RateLimiter, StateMachine, PriorityQueue, LootTable, Spring, BitBuffer, InputManager

Each module entry explains **why** — not just **what**.

## Code Standards

- `--!strict` in every entry
- Full type annotations
- No deprecated Roblox APIs
- Server-authoritative patterns
- Memory-safe cleanup

## Use Case

This dataset is designed for **training from scratch** or **fine-tuning** a model that reasons about Luau problems step by step. The CoT format teaches the model to think before coding, producing better-architected solutions.
