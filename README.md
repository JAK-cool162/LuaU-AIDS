# LuaU-AIDS — Luau Agentic Training Dataset (110MB)

**23,572 unique entries** for fine-tuning Luau AI models from scratch.

**License:** MIT

## Quality Verified

| Check | Result |
|-------|--------|
| Total entries | 23,572 |
| Unique code blocks | 23,572 (100% unique) |
| Has `--!strict` | 100% |
| Has THINK/ACT/VERIFY | 100% |
| Has `export type` | 100% |
| Structural errors | 0 |
| TODO/FIXME/placeholder | 0 |
| Deprecated APIs | 0 |

## Dataset

| File | Size | Entries |
|------|------|---------|
| `dataset_part_00.jsonl` | 54 MB | 12,000 |
| `dataset_part_01.jsonl` | 52 MB | 11,572 |

Combine: `cat dataset_part_*.jsonl > dataset.jsonl`

## Format

3-message agentic format: `system` → `user` → `assistant`

Each assistant follows: **THINK** (plan) → **ACT** (code) → **VERIFY** (check)

## 11 Template Types

| Template | Unique Variants | What it teaches |
|----------|:-:|----------------|
| **Signal** | 4 storage types | Event systems with error isolation |
| **Maid** | 3 cleanup styles | Memory-safe resource management |
| **ObjectPool** | 27 object types | GC-free instance recycling |
| **HealthSystem** | 4 feature types | Server-authoritative damage pipelines |
| **CooldownSystem** | per-ability | Zero-cost cooldown tracking |
| **LootTable** | per-NPC/item | Weighted random generation |
| **Timer** | per-ability | Frame-rate independent timing |
| **RateLimiter** | per-context | Token bucket abuse prevention |
| **StateMachine** | 6 state sets | NPC AI with validated transitions |
| **SpatialGrid** | per-entity | O(1) proximity detection |
| **Inventory** | per-item | Stack-based storage with capacity |

Each entry has unique context: game genre (80+), NPC type (36), item type (31), ability (26).

## Regenerate

```bash
python3 generate_dataset.py
```

Edit `TARGET_BYTES` in the script to change size.
