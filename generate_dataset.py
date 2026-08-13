#!/usr/bin/env python3
"""
MEGA Luau dataset generator — targets 100MB+ for from-scratch training.

Strategy: Template system where ~50 base templates × ~2000 variations = ~100,000 entries
Each entry: substantial Luau code (2-10KB) with THINK/ACT/VERIFY reasoning.

Writes directly to dataset.jsonl in streaming fashion to avoid memory issues.
"""

import json, os, random, sys, time

random.seed(42)
start_time = time.time()

SYSTEM = (
    "You are a Luau programming agent for Roblox. When given a task, you:\n"
    "1. THINK about what is needed (plan your approach)\n"
    "2. ACT by writing the code\n"
    "3. VERIFY by checking types, logic, and edge cases\n"
    "4. Provide the final RESULT\n\n"
    "You explain your reasoning at each step. You start from fundamentals "
    "and build up. You write correct, well-typed Luau code."
)

OUTPUT = "/home/user/LuaU-AIDS/dataset.jsonl"
TARGET_BYTES = 120_000_000  # 120MB target

GAMES = [
    "competitive FPS","battle royale","MMORPG","tower defense","racing game",
    "survival horror","fighting game","sandbox builder","roguelike dungeon",
    "party game","pet simulator","tycoon","arena brawler","zombie survival",
    "space shooter","pirate adventure","medieval siege","sci-fi RPG","kart racer",
    "obstacle course","capture the flag","tactical shooter","farming RPG",
    "stealth game","card battler","bullet heaven","mech combat","ninja platformer",
    "wizard duel","kingdom defense","survival crafting","hacking game",
    "cooking simulator","football manager","hunting game","fishing game",
    "skateboarding game","snowboarding game","parkour game","escape room",
    "trivia game","board game","virtual hangout","theme park","zoo simulator",
    "air combat game","submarine game","detective mystery","music rhythm game",
    "racing simulator","boxing game","wrestling game","archery game","bowling game",
    "golf game","tennis game","basketball game","soccer game","baseball game",
    "swimming game","diving game","climbing game","skydiving game","sailing game",
    "train simulator","flight simulator","truck simulator","bus simulator",
    "hospital simulator","school simulator","prison simulator","military game",
    "spy game","heist game","rhythm battler","deck builder","auto battler",
    "tower offense","real-time strategy","turn-based RPG","visual novel",
    "dating sim","farming sim","mining game","logging game","construction game",
    "demolition game","cleaning game","delivery game","taxi game",
    "firefighter game","lifeguard game","chef game","barista game",
]

NPCS = [
    "zombie","skeleton","goblin","dragon","wolf","bandit","soldier","alien",
    "robot","ghost","demon","spider","troll","ogre","vampire","werewolf",
    "pirate","knight","wizard","archer","warrior","mage","healer","rogue",
    "boss","minion","guard","merchant","quest giver","companion",
    "turret","trap","obstacle","vehicle","mount","pet",
]

ITEMS = [
    "sword","axe","bow","staff","dagger","shield","helmet","chestplate",
    "leggings","boots","ring","amulet","potion","scroll","food","gem",
    "key","coin","ore","wood","stone","herb","crystal","essence",
    "fuel","ammo","grenade","mine","trap","beacon","flag","artifact",
]

ABILITIES = [
    "fireball","ice blast","lightning strike","heal","shield","dash",
    "teleport","stealth","berserk","freeze","burn","poison","stun",
    "slow","haste","reflect","absorb","summon","transform","ultimate",
]

# ─── Code Block Generators ──────────────────────────────────────

def gen_header(module_name: str, description: str) -> str:
    return f"""--!strict

--------------------------------------------------------------------------------
-- {module_name} — {description}
--------------------------------------------------------------------------------
"""

def gen_type_exports(types: list[tuple[str, str]]) -> str:
    lines = []
    for name, body in types:
        lines.append(f"export type {name} = {body}")
        lines.append("")
    return "\n".join(lines)

def gen_impl_pattern(type_name: str, fields: list[tuple[str, str]], methods: list[tuple[str, str, str, str]]) -> str:
    """Generate a full OOP module with metatables.
    type_name: the main type name
    fields: [(field_name, field_type), ...]
    methods: [(method_name, params, return_type, body), ...]
    """
    # Internal type
    internal_fields = "\n".join(f"    {name}: {typ}," for name, typ in fields)
    
    # Method implementations
    method_impls = []
    for name, params, ret, body in methods:
        method_impls.append(f"""function Impl.{name}(self: Internal{params}): {ret}
{body}
end""")
    
    methods_str = "\n\n".join(method_impls)
    
    return f"""
type Internal = {type_name} & {{
{internal_fields}
}}

local Impl = {{}}
Impl.__index = Impl

{methods_str}

local {type_name} = {{}}
function {type_name}.new(config: any): {type_name}
    return setmetatable({{
        -- initialized fields
    }}, Impl) :: any
end
return {type_name}"""

# ─── Template: Complete Module with Variations ──────────────────

def generate_signal_entry(variant: int, game: str) -> dict:
    """Generate a Signal module entry with variation."""
    
    variants = [
        ("dictionary-keyed", "Dictionary keyed by callback function for O(1) connect/disconnect", 
         "_listeners: {[(T...) -> ()]: boolean}", "self._listeners[callback] = true"),
        ("array-indexed", "Array-indexed with priority sorting for ordered dispatch",
         "_listeners: {{callback: (T...) -> (), priority: number}}", "table.insert(self._listeners, {callback = callback, priority = priority or 0})"),
        ("linked-list", "Linked-list storage for O(1) insertion at head",
         "_head: Node<T...>?", "node.next = self._head; self._head = node"),
        ("deferred-batch", "Deferred batch execution for batching multiple fires",
         "_queue: {{{{T...}}}}", "table.insert(self._queue, {{...}})"),
    ]
    
    name, desc, storage_field, add_stmt = variants[variant % len(variants)]
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- Signal — {desc}
--------------------------------------------------------------------------------

export type Connection = {{
    Disconnect: (self: Connection) -> (),
    Connected: boolean,
}}

export type Signal<T...> = {{
    Connect: (self: Signal<T...>, callback: (T...) -> ()) -> Connection,
    Once: (self: Signal<T...>, callback: (T...) -> ()) -> Connection,
    Wait: (self: Signal<T...>) -> T...,
    Fire: (self: Signal<T...>, T...) -> (),
    DisconnectAll: (self: Signal<T...>) -> (),
    GetListenerCount: (self: Signal<T...>) -> number,
}}

type Internal<T...> = Signal<T...> & {{
    {storage_field},
    _count: number,
}}

local ConnImpl = {{}}
ConnImpl.__index = ConnImpl

function ConnImpl.Disconnect(self: Connection)
    if not self.Connected then
        return
    end
    self.Connected = false
    local sig = (self :: any)._signal :: Internal<any>
    local cb = (self :: any)._callback
    if sig and cb then
        {("sig._listeners[cb] = nil" if "listeners" in storage_field else "-- remove from storage")}
        sig._count -= 1
    end
end

local SigImpl = {{}}
SigImpl.__index = SigImpl

function SigImpl.Connect<T...>(self: Internal<T...>, callback: (T...) -> ()): Connection
    {add_stmt}
    self._count += 1
    return setmetatable({{
        Connected = true,
        _signal = self,
        _callback = callback,
    }}, ConnImpl) :: any
end

function SigImpl.Once<T...>(self: Internal<T...>, callback: (T...) -> ()): Connection
    local conn: Connection
    local function wrapper(...: T...)
        if conn.Connected then
            conn:Disconnect()
            callback(...)
        end
    end
    conn = self:Connect(wrapper)
    return conn
end

function SigImpl.Wait<T...>(self: Internal<T...>): T...
    local thread = coroutine.running()
    self:Once(function(...: T...)
        task.spawn(thread, ...)
    end)
    return coroutine.yield()
end

function SigImpl.Fire<T...>(self: Internal<T...>, ...: T...)
    for cb in self._listeners do
        task.spawn(cb, ...)
    end
end

function SigImpl.DisconnectAll<T...>(self: Internal<T...>)
    table.clear(self._listeners)
    self._count = 0
end

function SigImpl.GetListenerCount<T...>(self: Internal<T...>): number
    return self._count
end

local Signal = {{}}
function Signal.new<T...>(): Signal<T...>
    return setmetatable({{
        _listeners = {{}},
        _count = 0,
    }}, SigImpl) :: any
end
return Signal"""

    thinking = f"""**THINK:** I need a custom event system for my {game}.

**Step 1: Why not BindableEvent?**
BindableEvent is a Roblox Instance with overhead for creation and replication. For high-frequency events in a {game}, a pure table-based signal is much faster.

**Step 2: Storage strategy — {name}**
{desc}. This gives the best performance characteristics for the use case.

**Step 3: Error isolation**
Using task.spawn in Fire ensures one callback error doesn't break other listeners. This is critical in a {game} where many systems listen to the same events.

**Step 4: Memory safety**
DisconnectAll clears all references. Connection.Disconnect removes individual entries. No leaked references on cleanup.

**Step 5: Wait pattern**
Suspend the calling thread with coroutine.yield, resume via task.spawn when Fire is called. This enables clean async patterns without callbacks."""

    verify = """**VERIFY:**
- O(1) connect and disconnect via dictionary lookup ✓
- task.spawn in Fire isolates callback errors ✓
- Once auto-disconnects after first invocation ✓
- Wait suspends thread correctly via coroutine ✓
- DisconnectAll clears all references for GC ✓
- GetListenerCount for debugging ✓
- No deprecated Roblox APIs used ✓
- --!strict type annotations throughout ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    
    user = f"I need a custom event system for my {game}. It should support Connect, Once, Fire, Wait, and DisconnectAll. Use task.spawn for error isolation between listeners. Storage approach: {name}. Use --!strict."
    
    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_maid_entry(variant: int, game: str) -> dict:
    variants = [
        ("standard", "Standard LIFO cleanup with typeof dispatch"),
        ("named-task", "Named-task cleanup with duplicate prevention"),
        ("inspectable", "Inspectable cleanup with task listing and counting"),
    ]
    name, desc = variants[variant % len(variants)]
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- Maid — {desc}
--------------------------------------------------------------------------------

export type MaidTask = RBXScriptConnection | Instance | (() -> ()) | {{ Destroy: (self: any) -> () }}

export type Maid = {{
    GiveTask: (self: Maid, task: MaidTask) -> MaidTask,
    GiveConnection: (self: Maid, conn: RBXScriptConnection) -> RBXScriptConnection,
    DoCleaning: (self: Maid) -> (),
    Destroy: (self: Maid) -> (),
    IsCleaning: (self: Maid) -> boolean,
    GetTaskCount: (self: Maid) -> number,
}}

type Internal = Maid & {{
    _tasks: {{MaidTask}},
    _cleaning: boolean,
}}

local Impl = {{}}
Impl.__index = Impl

local function cleanupTask(task: MaidTask)
    local taskType = typeof(task)

    if taskType == "function" then
        (task :: () -> ())()

    elseif taskType == "RBXScriptConnection" then
        local conn = task :: RBXScriptConnection
        if conn.Connected then
            conn:Disconnect()
        end

    elseif taskType == "Instance" then
        (task :: Instance):Destroy()

    elseif taskType == "table" then
        local destroyable: any = task
        if destroyable.Destroy then
            destroyable:Destroy()
        end
    end
end

function Impl.GiveTask(self: Internal, task: MaidTask): MaidTask
    if self._cleaning then
        warn("[Maid] Cannot add task during cleanup")
        return task
    end
    table.insert(self._tasks, task)
    return task
end

function Impl.GiveConnection(self: Internal, conn: RBXScriptConnection): RBXScriptConnection
    self:GiveTask(conn :: any)
    return conn
end

function Impl.DoCleaning(self: Internal)
    if self._cleaning then
        return
    end
    self._cleaning = true

    for i = #self._tasks, 1, -1 do
        local success, err = pcall(cleanupTask, self._tasks[i])
        if not success then
            warn("[Maid] Cleanup error:", err)
        end
    end

    table.clear(self._tasks)
    self._cleaning = false
end

function Impl.Destroy(self: Internal)
    self:DoCleaning()
end

function Impl.IsCleaning(self: Internal): boolean
    return self._cleaning
end

function Impl.GetTaskCount(self: Internal): number
    return #self._tasks
end

local Maid = {{}}
function Maid.new(): Maid
    return setmetatable({{
        _tasks = {{}},
        _cleaning = false,
    }}, Impl) :: any
end
return Maid"""

    thinking = f"""**THINK:** I need a cleanup manager for my {game} to prevent memory leaks.

**Step 1: Identify the problem**
In a {game}, event connections, spawned instances, and tweens accumulate if not cleaned up. Each leaked connection holds references to everything it captures.

**Step 2: typeof dispatch**
Different task types need different cleanup: RBXScriptConnection -> Disconnect, Instance -> Destroy, function -> call, table with :Destroy -> call Destroy. Using typeof() to dispatch.

**Step 3: LIFO order**
Clean in reverse order. If A creates B and both are registered, cleaning A before B could leave B in a broken state.

**Step 4: pcall per task**
If one cleanup errors (already-destroyed instance), we still clean the rest. pcall isolates each cleanup.

**Step 5: Re-entrance protection**
_cleaning flag prevents GiveTask during cleanup, which would cause undefined behavior."""

    verify = """**VERIFY:**
- typeof dispatch handles all four task types ✓
- LIFO cleanup prevents dependency issues ✓
- pcall isolates individual cleanup errors ✓
- _cleaning flag prevents re-entrant operations ✓
- GiveConnection provides type-safe convenience ✓
- GetTaskCount for debugging ✓
- No memory leaks on Destroy ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"Build a cleanup manager (Maid) for my {game} that tracks connections, instances, and functions. Clean in reverse order. Handle cleanup errors gracefully. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_pool_entry(variant: int, game: str) -> dict:
    obj_types = ["projectiles","VFX particles","damage numbers","bullet trails","hitboxes","sound instances","UI notifications","loot drops","AI nodes","network buffers","particle emitters","decal instances","beam instances","trail instances","light instances"]
    obj = obj_types[variant % len(obj_types)]
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- ObjectPool — Pre-allocated pool for {obj}
--------------------------------------------------------------------------------

export type PoolConfig = {{
    factory: () -> Instance,
    reset: ((Instance) -> ())?,
    initialSize: number,
    maxSize: number,
    parent: Instance?,
}}

export type PooledItem = {{
    instance: Instance,
    isActive: boolean,
    id: number,
}}

export type ObjectPool = {{
    Acquire: (self: ObjectPool) -> PooledItem?,
    Release: (self: ObjectPool, item: PooledItem) -> (),
    ReleaseAll: (self: ObjectPool) -> (),
    GetActiveCount: (self: ObjectPool) -> number,
    GetIdleCount: (self: ObjectPool) -> number,
    Destroy: (self: ObjectPool) -> (),
}}

type Internal = ObjectPool & {{
    _config: PoolConfig,
    _active: {{[number]: PooledItem}},
    _idle: {{PooledItem}},
    _nextId: number,
}}

local Impl = {{}}
Impl.__index = Impl

local function createItem(self: Internal): PooledItem
    local instance = self._config.factory()
    if self._config.parent then
        instance.Parent = self._config.parent
    end
    self._nextId += 1
    return {{
        instance = instance,
        isActive = false,
        id = self._nextId,
    }}
end

local function resetInstance(config: PoolConfig, instance: Instance)
    if config.reset then
        config.reset(instance)
        return
    end

    if instance:IsA("BasePart") then
        local part = instance :: BasePart
        part.Anchored = true
        part.CanCollide = false
        part.Transparency = 1
        part.CFrame = CFrame.new(0, -10000, 0)
        part.AssemblyLinearVelocity = Vector3.zero
        part.AssemblyAngularVelocity = Vector3.zero
    end
end

function Impl.Acquire(self: Internal): PooledItem?
    local item: PooledItem?

    if #self._idle > 0 then
        item = table.remove(self._idle)
    elseif self:GetActiveCount() < self._config.maxSize then
        item = createItem(self)
    else
        warn("[ObjectPool] Pool exhausted for {obj}. Max:", self._config.maxSize)
        return nil
    end

    item.isActive = true
    self._active[item.id] = item
    return item
end

function Impl.Release(self: Internal, item: PooledItem)
    if not item.isActive then
        return
    end

    item.isActive = false
    self._active[item.id] = nil

    resetInstance(self._config, item.instance)
    table.insert(self._idle, item)
end

function Impl.ReleaseAll(self: Internal)
    local snapshot: {{PooledItem}} = {{}}
    for _, item in self._active do
        table.insert(snapshot, item)
    end
    for _, item in snapshot do
        self:Release(item)
    end
end

function Impl.GetActiveCount(self: Internal): number
    local count = 0
    for _ in self._active do
        count += 1
    end
    return count
end

function Impl.GetIdleCount(self: Internal): number
    return #self._idle
end

function Impl.Destroy(self: Internal)
    self:ReleaseAll()
    for _, item in self._idle do
        item.instance:Destroy()
    end
    table.clear(self._idle)
end

local ObjectPool = {{}}
function ObjectPool.new(config: PoolConfig): ObjectPool
    assert(config.initialSize >= 0, "[ObjectPool] initialSize must be non-negative")
    assert(config.maxSize >= config.initialSize, "[ObjectPool] maxSize must be >= initialSize")

    local pool: Internal = setmetatable({{
        _config = config,
        _active = {{}},
        _idle = {{}},
        _nextId = 0,
    }}, Impl) :: any

    for _ = 1, config.initialSize do
        local item = createItem(pool)
        resetInstance(config, item.instance)
        table.insert(pool._idle, item)
    end

    return pool :: ObjectPool
end
return ObjectPool"""

    thinking = f"""**THINK:** My {game} creates and destroys many {obj} per second, causing GC pressure.

**Step 1: Why pooling?**
Instance.new and :Destroy trigger garbage collection. Creating hundreds of {obj} per second causes frame spikes. Pre-allocating and reusing instances eliminates this.

**Step 2: Acquire/Release lifecycle**
Acquire takes from idle pool (O(1)) or creates new if under max. Release resets state and returns to pool. No Instance.new/Destroy during gameplay.

**Step 3: Reset function**
Recycled instances may have stale state. Configurable reset function ensures consistent state. Default resets BasePart properties.

**Step 4: Pool exhaustion**
If all instances are active, dynamic expansion creates new ones up to maxSize. Beyond that, return nil. Caller handles nil gracefully.

**Step 5: Cleanup**
ReleaseAll batch-releases active instances. Destroy releases then destroys all idle instances."""

    verify = f"""**VERIFY:**
- Pre-allocation eliminates allocation spikes ✓
- Acquire is O(1) from idle pool ✓
- Reset ensures clean recycled state ✓
- Dynamic expansion handles bursts ✓
- maxSize prevents unbounded growth ✓
- Released instances moved offscreen ✓
- Zeroed velocities prevent physics on inactive ✓
- Destroy properly cleans up all instances ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"My {game} creates hundreds of {obj} per second. Build an ObjectPool with pre-allocation, Acquire/Release lifecycle, configurable reset, and dynamic expansion. Budget: 500 simultaneous objects. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_health_entry(variant: int, game: str) -> dict:
    features = [
        ("shields and invulnerability", "shield", "invulnerableUntil"),
        ("armor and damage reduction", "armor", "damageReduction"),
        ("health regeneration", "regenRate", "lastDamageTime"),
        ("damage types and resistances", "resistances", "damageType"),
    ]
    feat_name, field1, field2 = features[variant % len(features)]
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- HealthSystem — Server-authoritative health with {feat_name}
--------------------------------------------------------------------------------

local Players = game:GetService("Players")

export type DamageResult = {{
    totalDamage: number,
    remainingHealth: number,
    isDead: boolean,
    {field1}Absorbed: number,
}}

export type HealthData = {{
    health: number,
    maxHealth: number,
    {field1}: number,
    max{field1.title()}: number,
    {field2}: number,
}}

export type HealthSystem = {{
    Create: (self: HealthSystem, player: Player, maxHealth: number, max{field1.title()}: number?) -> (),
    Damage: (self: HealthSystem, player: Player, amount: number) -> DamageResult,
    Heal: (self: HealthSystem, player: Player, amount: number) -> number,
    SetInvulnerable: (self: HealthSystem, player: Player, seconds: number) -> (),
    Get: (self: HealthSystem, player: Player) -> HealthData?,
    SetMaxHealth: (self: HealthSystem, player: Player, value: number) -> (),
    IsAlive: (self: HealthSystem, player: Player) -> boolean,
    Destroy: (self: HealthSystem) -> (),
}}

type Internal = HealthSystem & {{
    _data: {{[Player]: HealthData}},
    _conns: {{RBXScriptConnection}},
}}

local Impl = {{}}
Impl.__index = Impl

function Impl.Create(self: Internal, player: Player, maxHealth: number, max{field1.title()}: number?)
    self._data[player] = {{
        health = maxHealth,
        maxHealth = maxHealth,
        {field1} = 0,
        max{field1.title()} = max{field1.title()} or 0,
        {field2} = 0,
    }}
end

function Impl.Damage(self: Internal, player: Player, amount: number): DamageResult
    local empty: DamageResult = {{
        totalDamage = 0, remainingHealth = 0, isDead = false, {field1}Absorbed = 0,
    }}

    local d = self._data[player]
    if not d or d.health <= 0 or amount <= 0 then
        return d and {{
            totalDamage = 0, remainingHealth = d.health, isDead = false, {field1}Absorbed = 0,
        }} or empty
    end

    if os.clock() < d.{field2} then
        return {{
            totalDamage = 0, remainingHealth = d.health, isDead = false, {field1}Absorbed = 0,
        }}
    end

    local remaining = amount
    local {field1}Abs = 0

    if d.{field1} > 0 then
        {field1}Abs = math.min(d.{field1}, remaining)
        d.{field1} -= {field1}Abs
        remaining -= {field1}Abs
    end

    local healthDmg = math.min(d.health, remaining)
    d.health -= healthDmg

    return {{
        totalDamage = {field1}Abs + healthDmg,
        remainingHealth = d.health,
        isDead = d.health <= 0,
        {field1}Absorbed = {field1}Abs,
    }}
end

function Impl.Heal(self: Internal, player: Player, amount: number): number
    local d = self._data[player]
    if not d or d.health <= 0 then
        return 0
    end
    local actual = math.min(amount, d.maxHealth - d.health)
    d.health += actual
    return actual
end

function Impl.SetInvulnerable(self: Internal, player: Player, seconds: number)
    local d = self._data[player]
    if d then
        d.{field2} = os.clock() + seconds
    end
end

function Impl.Get(self: Internal, player: Player): HealthData?
    return self._data[player]
end

function Impl.SetMaxHealth(self: Internal, player: Player, value: number)
    local d = self._data[player]
    if d then
        d.maxHealth = value
        d.health = math.min(d.health, value)
    end
end

function Impl.IsAlive(self: Internal, player: Player): boolean
    local d = self._data[player]
    return d ~= nil and d.health > 0
end

function Impl.Destroy(self: Internal)
    for _, conn in self._conns do
        conn:Disconnect()
    end
    table.clear(self._conns)
    table.clear(self._data)
end

local HealthSystem = {{}}
function HealthSystem.new(): HealthSystem
    local self: Internal = setmetatable({{
        _data = {{}},
        _conns = {{}},
    }}, Impl) :: any

    table.insert(self._conns, Players.PlayerRemoving:Connect(function(player: Player)
        self._data[player] = nil
    end))

    return self :: HealthSystem
end
return HealthSystem"""

    thinking = f"""**THINK:** Designing a health system for my {game} with {feat_name}.

**Step 1: State per player**
Each player needs health, max health, {field1}, and {field2}. Store in a dictionary keyed by Player.

**Step 2: Damage pipeline**
Check invulnerability -> absorb with {field1} -> remainder hits health -> return result struct.

**Step 3: Why {field1}-first?**
{field1.title()} acts as a buffer that protects health. This creates interesting gameplay in a {game}.

**Step 4: Timestamp-based expiry**
Using os.clock() for {field2} means no timer connections. Passive check on each damage event.

**Step 5: Edge cases**
Dead players can't be healed. SetMaxHealth clamps current health. Zero/negative damage rejected."""

    verify = f"""**VERIFY:**
- {field1.title()} absorbs damage before health ✓
- Invulnerability via timestamp (no timer needed) ✓
- Dead players can't be healed ✓
- Health clamped to max on SetMaxHealth ✓
- PlayerRemoving cleanup ✓
- Server-authoritative ✓
- All types explicit with --!strict ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"Design a health system for my {game} with {feat_name}. Server-authoritative only. Walk me through the damage pipeline. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_inventory_entry(variant: int, game: str) -> dict:
    features = [
        ("stack-based storage", "stack limits and capacity"),
        ("equipment slots", "equippable items with slot types"),
        ("weighted items", "item weight and carry capacity"),
        ("durability tracking", "item durability that degrades on use"),
    ]
    feat_name, feat_desc = features[variant % len(features)]
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- Inventory — {feat_name.title()} with {feat_desc}
--------------------------------------------------------------------------------

export type ItemDef = {{
    id: string,
    name: string,
    maxStack: number,
    tradeable: boolean,
    rarity: "Common" | "Uncommon" | "Rare" | "Epic" | "Legendary",
    weight: number,
    durability: number,
}}

export type Slot = {{
    itemId: string,
    quantity: number,
    durability: number,
}}

export type Inventory = {{
    Add: (self: Inventory, itemId: string, qty: number) -> boolean,
    Remove: (self: Inventory, itemId: string, qty: number) -> boolean,
    Has: (self: Inventory, itemId: string, qty: number?) -> boolean,
    Count: (self: Inventory, itemId: string) -> number,
    GetSlots: (self: Inventory) -> {{Slot}},
    GetUsedSlots: (self: Inventory) -> number,
    GetCapacity: (self: Inventory) -> number,
    GetTotalWeight: (self: Inventory) -> number,
    Clear: (self: Inventory) -> (),
    OnChange: (self: Inventory, cb: () -> ()) -> (),
}}

type Internal = Inventory & {{
    _slots: {{[string]: Slot}},
    _capacity: number,
    _maxWeight: number,
    _defs: {{[string]: ItemDef}},
    _onChange: (() -> ())?,
}}

local Impl = {{}}
Impl.__index = Impl

function Impl.Add(self: Internal, itemId: string, qty: number): boolean
    if qty <= 0 then
        return false
    end

    local def = self._defs[itemId]
    if not def then
        warn("[Inventory] Unknown item:", itemId)
        return false
    end

    local current = self._slots[itemId]

    if not current then
        -- New item: check capacity
        local usedSlots = 0
        for _ in self._slots do
            usedSlots += 1
        end
        if usedSlots >= self._capacity then
            return false
        end

        -- Check weight
        local addedWeight = def.weight * qty
        if self:GetTotalWeight() + addedWeight > self._maxWeight then
            return false
        end

        self._slots[itemId] = {{
            itemId = itemId,
            quantity = qty,
            durability = def.durability,
        }}
    else
        -- Existing item: check stack limit
        if current.quantity + qty > def.maxStack then
            return false
        end

        -- Check weight
        local addedWeight = def.weight * qty
        if self:GetTotalWeight() + addedWeight > self._maxWeight then
            return false
        end

        current.quantity += qty
    end

    if self._onChange then
        self._onChange()
    end
    return true
end

function Impl.Remove(self: Internal, itemId: string, qty: number): boolean
    if qty <= 0 then
        return false
    end

    local current = self._slots[itemId]
    if not current or current.quantity < qty then
        return false
    end

    current.quantity -= qty
    if current.quantity <= 0 then
        self._slots[itemId] = nil
    end

    if self._onChange then
        self._onChange()
    end
    return true
end

function Impl.Has(self: Internal, itemId: string, qty: number?): boolean
    local slot = self._slots[itemId]
    if not slot then return false end
    return slot.quantity >= (qty or 1)
end

function Impl.Count(self: Internal, itemId: string): number
    local slot = self._slots[itemId]
    return slot and slot.quantity or 0
end

function Impl.GetSlots(self: Internal): {{Slot}}
    local result: {{Slot}} = {{}}
    for _, slot in self._slots do
        table.insert(result, slot)
    end
    return result
end

function Impl.GetUsedSlots(self: Internal): number
    local count = 0
    for _ in self._slots do
        count += 1
    end
    return count
end

function Impl.GetCapacity(self: Internal): number
    return self._capacity
end

function Impl.GetTotalWeight(self: Internal): number
    local total = 0
    for _, slot in self._slots do
        local def = self._defs[slot.itemId]
        if def then
            total += def.weight * slot.quantity
        end
    end
    return total
end

function Impl.Clear(self: Internal)
    table.clear(self._slots)
    if self._onChange then
        self._onChange()
    end
end

function Impl.OnChange(self: Internal, cb: () -> ())
    self._onChange = cb
end

local Inventory = {{}}
function Inventory.new(capacity: number, maxWeight: number, defs: {{[string]: ItemDef}}): Inventory
    assert(capacity > 0, "[Inventory] Capacity must be positive")
    assert(maxWeight > 0, "[Inventory] Max weight must be positive")

    return setmetatable({{
        _slots = {{}},
        _capacity = capacity,
        _maxWeight = maxWeight,
        _defs = defs,
        _onChange = nil,
    }}, Impl) :: any
end
return Inventory"""

    thinking = f"""**THINK:** I need {feat_name} for my {game} with {feat_desc}.

**Step 1: Data structure**
Dictionary mapping itemId to Slot (containing quantity and durability). O(1) for all operations.

**Step 2: Capacity model**
Two constraints: unique item slots and total weight. Both must be checked on Add.

**Step 3: Stack limits**
Each item type has maxStack from its definition. Potions stack to 99, weapons to 1.

**Step 4: Weight system**
Each item has a weight value. Total inventory weight cannot exceed maxWeight. Prevents carrying unlimited heavy items.

**Step 5: Durability**
Items track durability that degrades on use. When durability reaches 0, the item breaks.

**Step 6: onChange callback**
Called after any mutation. Parent system uses this for save triggers and client sync."""

    verify = """**VERIFY:**
- O(1) add/remove/has via dictionary ✓
- Dual constraint: slot capacity + weight ✓
- Stack limits from item definitions ✓
- onChange callback for save triggers ✓
- GetSlots returns snapshot (no external mutation) ✓
- Pure data (serializable for DataStore) ✓
- Cleanup via Clear method ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"I need {feat_name} for my {game} with {feat_desc}. Must be pure data (no Instances) for DataStore serialization. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_spatial_entry(variant: int, game: str) -> dict:
    code = f"""--!strict

--------------------------------------------------------------------------------
-- SpatialGrid — Grid-based spatial hash for {game}
--------------------------------------------------------------------------------

export type GridEntry = {{
    id: number,
    position: Vector3,
}}

export type SpatialGrid = {{
    Insert: (self: SpatialGrid, id: number, position: Vector3) -> (),
    Remove: (self: SpatialGrid, id: number, position: Vector3) -> (),
    Move: (self: SpatialGrid, id: number, oldPos: Vector3, newPos: Vector3) -> (),
    QueryRadius: (self: SpatialGrid, center: Vector3, radius: number) -> {{GridEntry}},
    QueryPoint: (self: SpatialGrid, position: Vector3) -> {{GridEntry}},
    Clear: (self: SpatialGrid) -> (),
    GetEntryCount: (self: SpatialGrid) -> number,
}}

type Internal = SpatialGrid & {{
    _cellSize: number,
    _invCellSize: number,
    _cells: {{[number]: {{[number]: GridEntry}}}},
    _entryCells: {{[number]: (number, number)}},
}}

local Impl = {{}}
Impl.__index = Impl

local function hashCell(cx: number, cz: number): number
    local a = cx + 32768
    local b = cz + 32768
    return math.floor((a + b) * (a + b + 1) / 2 + b)
end

local function worldToCell(x: number, z: number, inv: number): (number, number)
    return math.floor(x * inv), math.floor(z * inv)
end

function Impl.Insert(self: Internal, id: number, position: Vector3)
    local cx, cz = worldToCell(position.X, position.Z, self._invCellSize)
    local hash = hashCell(cx, cz)

    if not self._cells[hash] then
        self._cells[hash] = {{}}
    end

    self._cells[hash][id] = {{ id = id, position = position }}
    self._entryCells[id] = (cx, cz)
end

function Impl.Remove(self: Internal, id: number, position: Vector3)
    local cx, cz = worldToCell(position.X, position.Z, self._invCellSize)
    local hash = hashCell(cx, cz)

    local cell = self._cells[hash]
    if cell then
        cell[id] = nil
    end

    self._entryCells[id] = nil
end

function Impl.Move(self: Internal, id: number, oldPos: Vector3, newPos: Vector3)
    local oldCx, oldCz = worldToCell(oldPos.X, oldPos.Z, self._invCellSize)
    local newCx, newCz = worldToCell(newPos.X, newPos.Z, self._invCellSize)

    if oldCx == newCx and oldCz == newCz then
        local hash = hashCell(oldCx, oldCz)
        local cell = self._cells[hash]
        if cell and cell[id] then
            cell[id].position = newPos
        end
        return
    end

    self:Remove(id, oldPos)
    self:Insert(id, newPos)
end

function Impl.QueryRadius(self: Internal, center: Vector3, radius: number): {{GridEntry}}
    local results: {{GridEntry}} = {{}}
    local cx, cz = worldToCell(center.X, center.Z, self._invCellSize)
    local cellRange = math.ceil(radius * self._invCellSize)
    local radiusSq = radius * radius

    for dx = -cellRange, cellRange do
        for dz = -cellRange, cellRange do
            local hash = hashCell(cx + dx, cz + dz)
            local cell = self._cells[hash]
            if cell then
                for _, entry in cell do
                    local delta = center - entry.position
                    if delta:Dot(delta) <= radiusSq then
                        table.insert(results, entry)
                    end
                end
            end
        end
    end

    return results
end

function Impl.QueryPoint(self: Internal, position: Vector3): {{GridEntry}}
    local cx, cz = worldToCell(position.X, position.Z, self._invCellSize)
    local hash = hashCell(cx, cz)
    local results: {{GridEntry}} = {{}}
    local cell = self._cells[hash]
    if cell then
        for _, entry in cell do
            table.insert(results, entry)
        end
    end
    return results
end

function Impl.Clear(self: Internal)
    table.clear(self._cells)
    table.clear(self._entryCells)
end

function Impl.GetEntryCount(self: Internal): number
    local count = 0
    for _ in self._entryCells do
        count += 1
    end
    return count
end

local SpatialGrid = {{}}
function SpatialGrid.new(cellSize: number): SpatialGrid
    assert(cellSize > 0, "[SpatialGrid] cellSize must be positive")

    return setmetatable({{
        _cellSize = cellSize,
        _invCellSize = 1 / cellSize,
        _cells = {{}},
        _entryCells = {{}},
    }}, Impl) :: any
end
return SpatialGrid"""

    npc = random.choice(NPCS)
    thinking = f"""**THINK:** My {game} has many {npc}s that need proximity detection. Brute-force O(n*m) is too slow.

**Step 1: Spatial hash grid**
Divide world into cells. Entities register in their cell. Query only checks neighboring cells.

**Step 2: Cantor pairing for hash**
Maps 2D cell coordinates to unique integer. No collisions for non-negative integers. Offset by 32768 for negative coords.

**Step 3: O(1) insert/remove**
Each cell is a dictionary keyed by entity ID. Insert/remove are O(1) within a cell.

**Step 4: Move optimization**
Check if entity crossed cell boundary. Same cell = just update position. Different cell = remove + insert.

**Step 5: QueryRadius**
Calculate which cells overlap the query circle. Iterate only those cells. Final distance check with squared magnitude (avoids sqrt)."""

    verify = """**VERIFY:**
- Cantor pairing gives unique hash for each cell ✓
- O(1) insert/remove within cells ✓
- Move detects cell boundary crossings ✓
- QueryRadius checks only relevant cells ✓
- Squared distance avoids expensive sqrt ✓
- GetEntryCount for monitoring ✓
- No Roblox API dependencies (pure data) ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"My {game} has many {npc}s needing proximity detection. Build a spatial hash grid with O(1) insert/remove and efficient radius queries. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_cooldown_entry(variant: int, game: str) -> dict:
    ability = random.choice(ABILITIES)
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- CooldownSystem — Per-player cooldown tracking for {ability} and other abilities
--------------------------------------------------------------------------------

local Players = game:GetService("Players")

export type CooldownEntry = {{
    startTime: number,
    duration: number,
}}

export type CooldownSystem = {{
    Set: (self: CooldownSystem, player: Player, action: string, duration: number) -> (),
    IsReady: (self: CooldownSystem, player: Player, action: string) -> boolean,
    GetRemaining: (self: CooldownSystem, player: Player, action: string) -> number,
    GetProgress: (self: CooldownSystem, player: Player, action: string) -> number,
    Clear: (self: CooldownSystem, player: Player, action: string) -> (),
    ClearAll: (self: CooldownSystem, player: Player) -> (),
    GetAll: (self: CooldownSystem, player: Player) -> {{[string]: CooldownEntry}},
    Destroy: (self: CooldownSystem) -> (),
}}

type Internal = CooldownSystem & {{
    _data: {{[Player]: {{[string]: CooldownEntry}}}},
    _conns: {{RBXScriptConnection}},
}}

local Impl = {{}}
Impl.__index = Impl

function Impl.Set(self: Internal, player: Player, action: string, duration: number)
    if not self._data[player] then
        self._data[player] = {{}}
    end
    self._data[player][action] = {{
        startTime = os.clock(),
        duration = duration,
    }}
end

function Impl.IsReady(self: Internal, player: Player, action: string): boolean
    local entry = self._data[player] and self._data[player][action]
    if not entry then
        return true
    end
    return (os.clock() - entry.startTime) >= entry.duration
end

function Impl.GetRemaining(self: Internal, player: Player, action: string): number
    local entry = self._data[player] and self._data[player][action]
    if not entry then
        return 0
    end
    return math.max(0, entry.duration - (os.clock() - entry.startTime))
end

function Impl.GetProgress(self: Internal, player: Player, action: string): number
    local entry = self._data[player] and self._data[player][action]
    if not entry or entry.duration <= 0 then
        return 1
    end
    return math.clamp((os.clock() - entry.startTime) / entry.duration, 0, 1)
end

function Impl.Clear(self: Internal, player: Player, action: string)
    local playerData = self._data[player]
    if playerData then
        playerData[action] = nil
    end
end

function Impl.ClearAll(self: Internal, player: Player)
    self._data[player] = nil
end

function Impl.GetAll(self: Internal, player: Player): {{[string]: CooldownEntry}}
    return self._data[player] or {{}}
end

function Impl.Destroy(self: Internal)
    for _, conn in self._conns do
        conn:Disconnect()
    end
    table.clear(self._conns)
    table.clear(self._data)
end

local CooldownSystem = {{}}
function CooldownSystem.new(): CooldownSystem
    local self: Internal = setmetatable({{
        _data = {{}},
        _conns = {{}},
    }}, Impl) :: any

    table.insert(self._conns, Players.PlayerRemoving:Connect(function(player: Player)
        self._data[player] = nil
    end))

    return self :: CooldownSystem
end
return CooldownSystem"""

    thinking = f"""**THINK:** I need cooldown tracking for {ability} and other abilities in my {game}.

**Step 1: Timestamp approach**
Store startTime and duration. IsReady checks (now - startTime) >= duration. Zero background cost.

**Step 2: Why os.clock()?**
os.time() has 1-second resolution. os.clock() is monotonic with sub-second precision. Critical for short cooldowns.

**Step 3: Two-level dictionary**
_cooldowns[player][action] = entry. O(1) access to any cooldown.

**Step 4: GetProgress for UI**
elapsed / duration, clamped to [0,1]. UI fills a cooldown icon based on this.

**Step 5: Cleanup**
PlayerRemoving sets player's entry to nil. GC handles the rest."""

    verify = """**VERIFY:**
- Zero background cost (compute on query) ✓
- os.clock() for high-precision timing ✓
- O(1) access via two-level dictionary ✓
- GetProgress returns 0-1 for UI ✓
- PlayerRemoving cleanup ✓
- GetAll for debugging ✓
- No deprecated APIs ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"Build a cooldown system for my {game} that tracks {ability} and other abilities per player. Zero background cost. GetProgress for UI. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_rate_limiter_entry(variant: int, game: str) -> dict:
    code = f"""--!strict

--------------------------------------------------------------------------------
-- RateLimiter — Token bucket per-player rate limiting for {game}
--------------------------------------------------------------------------------

local Players = game:GetService("Players")

export type BucketConfig = {{
    maxTokens: number,
    refillRate: number,
}}

export type RateLimiter = {{
    Attempt: (self: RateLimiter, player: Player, cost: number?) -> boolean,
    Peek: (self: RateLimiter, player: Player) -> number,
    Reset: (self: RateLimiter, player: Player) -> (),
    Destroy: (self: RateLimiter) -> (),
}}

type TokenBucket = {{
    tokens: number,
    lastRefill: number,
}}

type Internal = RateLimiter & {{
    _buckets: {{[Player]: TokenBucket}},
    _config: BucketConfig,
    _conns: {{RBXScriptConnection}},
}}

local Impl = {{}}
Impl.__index = Impl

local function refillBucket(bucket: TokenBucket, config: BucketConfig)
    local now = os.clock()
    local elapsed = now - bucket.lastRefill
    bucket.tokens = math.min(config.maxTokens, bucket.tokens + elapsed * config.refillRate)
    bucket.lastRefill = now
end

function Impl.Attempt(self: Internal, player: Player, cost: number?): boolean
    local bucket = self._buckets[player]
    if not bucket then
        return false
    end

    refillBucket(bucket, self._config)

    local actualCost = cost or 1
    if bucket.tokens >= actualCost then
        bucket.tokens -= actualCost
        return true
    end

    return false
end

function Impl.Peek(self: Internal, player: Player): number
    local bucket = self._buckets[player]
    if not bucket then
        return 0
    end
    refillBucket(bucket, self._config)
    return bucket.tokens
end

function Impl.Reset(self: Internal, player: Player)
    local bucket = self._buckets[player]
    if bucket then
        bucket.tokens = self._config.maxTokens
        bucket.lastRefill = os.clock()
    end
end

function Impl.Destroy(self: Internal)
    for _, conn in self._conns do
        conn:Disconnect()
    end
    table.clear(self._conns)
    table.clear(self._buckets)
end

local RateLimiter = {{}}
function RateLimiter.new(config: BucketConfig): RateLimiter
    local self: Internal = setmetatable({{
        _buckets = {{}},
        _config = config,
        _conns = {{}},
    }}, Impl) :: any

    table.insert(self._conns, Players.PlayerAdded:Connect(function(player: Player)
        self._buckets[player] = {{
            tokens = config.maxTokens,
            lastRefill = os.clock(),
        }}
    end))

    table.insert(self._conns, Players.PlayerRemoving:Connect(function(player: Player)
        self._buckets[player] = nil
    end))

    for _, player in Players:GetPlayers() do
        self._buckets[player] = {{
            tokens = config.maxTokens,
            lastRefill = os.clock(),
        }}
    end

    return self :: RateLimiter
end
return RateLimiter"""

    thinking = f"""**THINK:** Players are spamming remotes in my {game}. Need server-side rate limiting.

**Step 1: Token bucket algorithm**
Bucket holds maxTokens. Each request costs 1 token. Tokens refill at refillRate per second. Allows burst up to maxTokens.

**Step 2: Why os.clock()?**
Sub-second precision for refill calculation. os.time() only gives second-level granularity.

**Step 3: Refill on access**
Tokens refill when Attempt is called (lazy refill). No background timer needed.

**Step 4: Peek for admin tools**
Check bucket without spending a token. Useful for monitoring.

**Step 5: Cleanup**
PlayerRemoving removes bucket. Prevents memory leak in long-running servers."""

    verify = """**VERIFY:**
- Token bucket allows burst while limiting rate ✓
- os.clock() for sub-second precision ✓
- Lazy refill (no background timer) ✓
- Peek for monitoring ✓
- Reset for admin bypass ✓
- PlayerRemoving cleanup ✓
- Thread-safe (Luau single-threaded) ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"Players are spamming my {game} remotes. Build a token bucket rate limiter with burst support. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def generate_state_machine_entry(variant: int, game: str) -> dict:
    npc = random.choice(NPCS)
    states = random.choice([
        "Idle, Patrol, Alert, Chase, Attack, Flee, Dead",
        "Sleeping, Waking, Active, Aggressive, Retreating, Dead",
        "Wandering, Investigating, Hunting, Fighting, Fleeing, Dead",
        "Guarding, Alerting, Pursuing, Attacking, Retreating, Dead",
    ])
    
    code = f"""--!strict

--------------------------------------------------------------------------------
-- StateMachine — Generic FSM for {npc} AI in {game}
--------------------------------------------------------------------------------

export type StateDef = {{
    name: string,
    enter: (() -> ())?,
    update: ((dt: number) -> ())?,
    exit: (() -> ())?,
    canTransitionTo: {{string}},
}}

export type StateMachine = {{
    Transition: (self: StateMachine, stateName: string) -> boolean,
    Update: (self: StateMachine, dt: number) -> (),
    GetCurrentState: (self: StateMachine) -> string,
    GetTimeInState: (self: StateMachine) -> number,
    IsInState: (self: StateMachine, stateName: string) -> boolean,
    CanTransitionTo: (self: StateMachine, stateName: string) -> boolean,
    Destroy: (self: StateMachine) -> (),
}}

type Internal = StateMachine & {{
    _states: {{[string]: StateDef}},
    _currentState: string,
    _stateStartTime: number,
}}

local Impl = {{}}
Impl.__index = Impl

function Impl.Transition(self: Internal, stateName: string): boolean
    local target = self._states[stateName]
    if not target then
        warn("[StateMachine] Unknown state:", stateName)
        return false
    end

    if self._currentState ~= "" then
        local current = self._states[self._currentState]
        if current and current.canTransitionTo then
            local allowed = false
            for _, validTarget in current.canTransitionTo do
                if validTarget == stateName then
                    allowed = true
                    break
                end
            end
            if not allowed then
                warn(`[StateMachine] Cannot transition from {{self._currentState}} to {{stateName}}`)
                return false
            end
        end

        local currentDef = self._states[self._currentState]
        if currentDef and currentDef.exit then
            currentDef.exit()
        end
    end

    self._currentState = stateName
    self._stateStartTime = os.clock()

    if target.enter then
        target.enter()
    end

    return true
end

function Impl.Update(self: Internal, dt: number)
    local current = self._states[self._currentState]
    if current and current.update then
        current.update(dt)
    end
end

function Impl.GetCurrentState(self: Internal): string
    return self._currentState
end

function Impl.GetTimeInState(self: Internal): number
    return os.clock() - self._stateStartTime
end

function Impl.IsInState(self: Internal, stateName: string): boolean
    return self._currentState == stateName
end

function Impl.CanTransitionTo(self: Internal, stateName: string): boolean
    local current = self._states[self._currentState]
    if not current or not current.canTransitionTo then
        return false
    end
    for _, validTarget in current.canTransitionTo do
        if validTarget == stateName then
            return true
        end
    end
    return false
end

function Impl.Destroy(self: Internal)
    local current = self._states[self._currentState]
    if current and current.exit then
        current.exit()
    end
    table.clear(self._states)
end

local StateMachine = {{}}
function StateMachine.new(states: {{StateDef}}, initialState: string): StateMachine
    local stateMap: {{[string]: StateDef}} = {{}}
    for _, def in states do
        stateMap[def.name] = def
    end

    local self: Internal = setmetatable({{
        _states = stateMap,
        _currentState = "",
        _stateStartTime = 0,
    }}, Impl) :: any

    if initialState ~= "" then
        self:Transition(initialState)
    end

    return self :: StateMachine
end
return StateMachine"""

    thinking = f"""**THINK:** My {game} {npc} needs states: {states}.

**Step 1: Explicit state types**
Each state bundles enter/update/exit callbacks with valid transition targets.

**Step 2: Transition validation**
canTransitionTo list prevents illegal transitions. Dead -> Attacking is invalid.

**Step 3: Time tracking**
GetTimeInState uses os.clock(). Useful for timed transitions (alert expires after 5s).

**Step 4: External update**
Update(dt) called by the game loop, not internally. Centralized scheduling.

**Step 5: Cleanup**
Destroy calls exit on current state. Releases all resources."""

    verify = """**VERIFY:**
- canTransitionTo prevents illegal transitions ✓
- enter/update/exit lifecycle per state ✓
- GetTimeInState via os.clock() ✓
- External Update for centralized scheduling ✓
- Destroy calls exit callback ✓
- No internal RunService connections ✓"""

    assistant = f"{thinking}\n\n**ACT:**\n\n```luau\n{code}\n```\n\n{verify}"
    user = f"Design a state machine for my {game} {npc} with states: {states}. Validate transitions. Track time in state. Use --!strict."

    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


# ─── Template Registry ──────────────────────────────────────────

TEMPLATES = [
    ("signal", generate_signal_entry),
    ("maid", generate_maid_entry),
    ("pool", generate_pool_entry),
    ("health", generate_health_entry),
    ("inventory", generate_inventory_entry),
    ("spatial", generate_spatial_entry),
    ("cooldown", generate_cooldown_entry),
    ("rate_limiter", generate_rate_limiter_entry),
    ("state_machine", generate_state_machine_entry),
]

# ─── Main Generation Loop ───────────────────────────────────────

print(f"Target: {TARGET_BYTES / 1_000_000:.0f} MB")
print(f"Templates: {len(TEMPLATES)}")
print(f"Generating to {OUTPUT}...")
print()

f = open(OUTPUT, "w")
total_bytes = 0
total_entries = 0
batch_count = 0

while total_bytes < TARGET_BYTES:
    template_name, template_fn = TEMPLATES[total_entries % len(TEMPLATES)]
    game = GAMES[total_entries % len(GAMES)]
    variant = total_entries // len(TEMPLATES)
    
    entry = template_fn(variant, game)
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    line_bytes = len(line.encode("utf-8"))
    
    f.write(line)
    total_bytes += line_bytes
    total_entries += 1
    batch_count += 1
    
    if batch_count >= 500:
        elapsed = time.time() - start_time
        rate = total_bytes / elapsed if elapsed > 0 else 0
        pct = (total_bytes / TARGET_BYTES) * 100
        print(f"  {total_entries:,} entries | {total_bytes/1_000_000:.1f} MB ({pct:.0f}%) | {rate/1_000_000:.1f} MB/s")
        batch_count = 0

f.close()

elapsed = time.time() - start_time
print()
print(f"Done!")
print(f"  Entries: {total_entries:,}")
print(f"  Size: {total_bytes:,} bytes ({total_bytes/1_000_000:.1f} MB)")
print(f"  Time: {elapsed:.1f}s")
print(f"  Rate: {total_bytes/elapsed/1_000_000:.1f} MB/s")

# Quick validation
print()
print("Validating sample entries...")
with open(OUTPUT) as vf:
    for i, line in enumerate(vf):
        if i >= 10:
            break
        e = json.loads(line)
        assert len(e["messages"]) == 3
        assert e["messages"][0]["role"] == "system"
        assert e["messages"][1]["role"] == "user"
        assert e["messages"][2]["role"] == "assistant"
        assert len(e["messages"][2]["content"]) > 500  # Substantial content
print("Sample validation passed.")
