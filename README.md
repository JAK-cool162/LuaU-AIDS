# LuaU-AIDS — Luau AI Dataset for Instruction Tuning

Synthetic instruction-tuning dataset for training language models on Roblox Luau engineering.

**License:** MIT

## Dataset

**`dataset.jsonl`** — 1,000 entries, ~3.2 MB

Each entry is a JSON object with 4 messages:
- `system` — Expert Luau engineer identity
- `user` — Realistic engineering problem with constraints
- `analysis` — Architectural rationale and design decisions
- `assistant` — Complete, production-ready Luau code

## 40 Unique Code Modules

Each module is a structurally distinct implementation — not renamed copies.

| # | Module | Type | Key Pattern |
|---|--------|------|-------------|
| 01-04 | **Signal** (4 variants) | Shared | Callback dict, array+priority, linked-list, deferred batch |
| 05-07 | **Maid** (3 variants) | Shared | Standard LIFO, named-task, inspectable |
| 08-11 | **ObjectPool** (4 variants) | Shared | Factory, stack-only, ring-buffer, CollectionService tag |
| 12 | **Timer** | Shared | dt accumulation, state machine, callbacks |
| 13 | **PriorityQueue** | Shared | Binary min-heap, O(log n) |
| 14 | **SpatialGrid** | Shared | Cantor hash, O(1) insert/remove/move |
| 15 | **RateLimiter** | Server | Token bucket, os.clock() |
| 16 | **CooldownSystem** | Server | Two-level dict, zero background cost |
| 17 | **HealthSystem** | Server | Shield absorption, invulnerability |
| 18 | **Inventory** | Server | Stack limits, capacity, onChange |
| 19 | **Spring** | Shared | Semi-implicit Euler |
| 20 | **StateMachine** | Shared | enter/update/exit, transition guards |
| 21 | **LootTable** | Server | Weighted random, cumulative distribution |
| 22 | **InputManager** | Client | Context stack, action mapping |
| 23 | **BitBuffer** | Shared | Bit32 ops, auto-expanding |
| 24 | **CurrencyManager** | Server | Multi-currency, max caps |
| 25 | **EventBus** | Shared | Global pub/sub, topic-based |
| 26 | **TweenScheduler** | Shared | Batched tweens, auto-disconnect |
| 27 | **DamageNumbers** | Client | BillboardGui pooling |
| 28 | **Leaderboard** | Server | Lazy sorting, rank lookup |
| 29 | **SessionLock** | Server | DataStore stale detection |
| 30 | **PathManager** | Shared | Waypoint following, loop support |
| 31 | **InventorySync** | Mixed | Client-server replication |
| 32 | **AbilityCooldowns** | Server | Shared cooldown groups |
| 33 | **TeamManager** | Server | Auto-assign, per-team scoring |
| 34 | **ChatCommands** | Server | Prefix parser, admin-only |
| 35 | **Notifications** | Mixed | Server-to-client dispatch |
| 36 | **ProximityAction** | Server | Zone-based enter/leave |
| 37 | **QuestTracker** | Server | Multi-objective progress |
| 38 | **WaveSpawner** | Server | Enemy wave sequencing |
| 39 | **InventorySort** | Shared | Sort/filter by criteria |
| 40 | **DamageTypes** | Shared | Elemental resistances |

## Code Quality

- `--!strict` in every entry
- 4-space indentation, section dividers (`──────`)
- Full `export type` with method signatures
- No deprecated APIs (`wait()`, `spawn()`, `delay()`)
- Server-authoritative design patterns
- Memory-safe cleanup (Destroy, PlayerRemoving, Maid patterns)
- `os.clock()` for all timing

## Known Limitations

- **AI-generated code** — not validated against a running Roblox game
- **270 curated entries** with module-specific queries + 730 fill entries with generic queries
- **No human review** — code may contain edge-case bugs
- **No eval benchmarks** — training effectiveness not measured
- Best used as **augmentation data** mixed with real-world Luau code

## 50 Game Genres

Competitive FPS, battle royale, MMORPG, tower defense, racing, survival horror, fighting game, sandbox builder, roguelike dungeon, party game, pet simulator, tycoon, escape room, arena brawler, zombie survival, space shooter, pirate adventure, medieval siege, sci-fi RPG, kart racer, obstacle course, capture the flag, simulator, tactical shooter, farming RPG, detective mystery, cooking simulator, musical rhythm game, hide and seek, story adventure, battle arena, dungeon crawler, city builder, air combat, submarine game, mech combat, ninja platformer, wizard duel, kingdom defense, treasure hunt, survival crafting, racing sim, football manager, hacking game, stealth game, rhythm battler, card battler, deck builder, bullet heaven, rail shooter.
