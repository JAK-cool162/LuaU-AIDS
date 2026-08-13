# LuaU-AIDS — Luau Quality Training Dataset

**2,416 entries** focused on **real substance** — debugging, refactoring, performance, and multi-file reasoning.

**License:** MIT

## What Changed

| Before | After |
|--------|-------|
| 23,572 entries of cosmetic template variations | 2,416 entries with real engineering substance |
| 100% same code structure, different game names | Real bugs, real refactoring, real performance issues |
| Model learns to copy patterns | Model learns to **reason about problems** |

## Dataset Composition

| Category | Count | What it teaches |
|----------|:-----:|----------------|
| **Refactoring** | ~1,980 | Clean up messy code — add types, module patterns, cleanup |
| **Performance** | ~453 | Fix slow code — spatial hashing, pooling, caching |
| **Debugging** | ~5 | Find and fix real security/logic bugs |
| **Multi-file** | ~8 | Trace data flow across multiple files |

## Entry Format

3-message agentic format: `system` → `user` → `assistant`

Each assistant follows: **THINK** (analyze) → **ACT** (fix) → **VERIFY** (check)

## Bug Types Covered

- Client-controlled damage/price (security)
- Memory leaks from forgotten connections
- DataStore without pcall (crash on failure)
- Touch detection without debounce/validation
- Combat without server-side validation
- Deprecated API usage (wait, spawn, delay)
- Instance.new with parent in constructor
- String concatenation in loops (O(n²))
- Missing PlayerRemoving cleanup

## File

`dataset.jsonl` — 2,416 entries, 7.6 MB
