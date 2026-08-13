# LuaU-AIDS — Luau From-Scratch Training Dataset

**39,022 unique entries** | **124 MB** | **0 repetition** | **24 module types**

## What This Is

A synthetic Luau training dataset for from-scratch model training. Every entry contains a **complete, working Luau module** with proper types, error handling, and cleanup.

## Dataset Stats

| Metric | Value |
|--------|-------|
| Total entries | 39,022 |
| Unique code blocks | 39,022 (100% unique) |
| Total size | 124 MB |
| Validation errors | 0 |
| All have `--!strict` | Yes |
| All have reasoning | Yes |

## Files

| File | Size | Entries |
|------|------|---------|
| `dataset_part_00.jsonl` | 39 MB | 13,000 |
| `dataset_part_01.jsonl` | 40 MB | 13,000 |
| `dataset_part_02.jsonl` | 40 MB | 13,000 |
| `dataset_part_03.jsonl` | 69 KB | 22 |

Combine: `cat dataset_part_*.jsonl > dataset.jsonl`

## 24 Unique Module Types

| Module | Lines | Pattern |
|--------|:-----:|---------|
| **Signal** (4 variants) | 80-100 | Dictionary, sorted array, linked list, deferred batch |
| **Maid** (3 variants) | 70-90 | Standard, named-task, inspectable |
| **ObjectPool** (3 variants) | 90-120 | Factory, stack-only, ring-buffer |
| **Timer** | 90-110 | Frame-rate independent, state machine |
| **CooldownSystem** | 80-100 | Zero-cost, os.clock() precision |
| **HealthSystem** | 90-120 | Shields/armor/regen/resistances |
| **Inventory** | 80-100 | Stack-based, capacity, onChange |
| **SpatialGrid** | 80-100 | Cantor hash, O(1) operations |
| **LootTable** | 60-80 | Weighted random, quantity ranges |
| **RateLimiter** | 70-90 | Token bucket, burst support |
| **StateMachine** | 80-100 | 6 state set variants |
| **PriorityQueue** | 80-100 | Binary min-heap, sift operations |
| **BitBuffer** | 90-110 | Bit32 ops, auto-expanding |
| **EventBus** | 60-80 | Topic-based pub/sub |
| **InputManager** | 80-100 | Context stack, action mapping |
| **TweenScheduler** | 80-100 | Heartbeat-driven, auto-cleanup |
| **Leaderboard** | 80-100 | Lazy sorting, rank lookup |
| **SessionLock** | 70-90 | DataStore locking, stale detection |
| **PathManager** | 60-80 | Waypoint following, loop support |
| **DamageTypeSystem** | 60-80 | Elemental resistances |
| **ProximityAction** | 80-100 | Zone detection, enter/leave |
| **QuestTracker** | 80-100 | Multi-objective progress |
| **WaveSpawner** | 80-100 | Sequential wave spawning |
| **TeamManager** | 80-100 | Auto-assign, scoring |

## What Each Entry Teaches

Each entry is a complete module with:
- `--!strict` header
- `export type` declarations with full method signatures
- `type Internal` for private state
- Metatable-based OOP pattern
- Proper `new()` constructor
- All methods fully implemented
- `Destroy()` with cleanup
- Server-authoritative patterns
- Memory-safe connection management

## Context Variety

Each module appears with different context:
- **70+ game genres** (FPS, RPG, tower defense, racing, etc.)
- **48 NPC types** (zombie, dragon, robot, ghost, etc.)
- **33 item types** (sword, potion, gem, crystal, etc.)
- **26 abilities** (fireball, heal, dash, teleport, etc.)

## Format

3-message format: `system` → `user` → `assistant`

Each assistant includes:
- Design reasoning (why this approach)
- Complete code implementation
- Verification checklist

## Regenerate

```bash
python3 generate_dataset.py
```

Edit `TARGET_BYTES` to change size.

## License

MIT
