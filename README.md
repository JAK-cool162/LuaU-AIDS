# LuaU-AIDS — Luau Agentic Training Dataset (120MB)

Massive Luau training dataset for fine-tuning from scratch.

**License:** MIT

## Dataset

**22,035 entries** | **120 MB** | Split into parts under 100MB for GitHub

| File | Size | Entries |
|------|------|---------|
| `dataset_part_00.jsonl` | 58 MB | 11,000 |
| `dataset_part_01.jsonl` | 58 MB | 11,000 |
| `dataset_part_02.jsonl` | 186 KB | 35 |

To combine: `cat dataset_part_*.jsonl > dataset.jsonl`

## Format

3-message agentic format: `system` → `user` → `assistant`

Each assistant follows: **THINK** → **ACT** → **VERIFY**

## 9 Template Types

Each template generates thousands of variations with different:
- Game genres (80+ contexts)
- NPCs, items, abilities
- Variant parameters (different internal structures)

| Template | What it teaches |
|----------|----------------|
| **Signal** | 4 storage variants (dict, array, linked-list, deferred) |
| **Maid** | 3 variants (standard, named, inspectable) |
| **ObjectPool** | 15 object types (projectiles, VFX, damage numbers, etc.) |
| **HealthSystem** | 4 features (shields, armor, regen, damage types) |
| **Inventory** | 4 features (stacks, equipment, weight, durability) |
| **SpatialGrid** | Proximity detection with O(1) operations |
| **CooldownSystem** | Per-player ability tracking |
| **RateLimiter** | Token bucket with burst support |
| **StateMachine** | NPC AI with configurable states |

## Regenerate

```bash
python3 generate_dataset.py
```

Generates 120MB+ in ~5 seconds. Adjust `TARGET_BYTES` in the script.

## Code Quality

- `--!strict` in every code block
- Full type annotations (export type, typed parameters)
- Section header dividers
- Server-authoritative patterns
- Memory-safe cleanup (PlayerRemoving, Destroy)
- No deprecated Roblox APIs
