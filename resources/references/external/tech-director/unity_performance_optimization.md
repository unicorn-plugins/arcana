# Unity Performance Optimization Guide

> Source: https://docs.unity3d.com/Manual/Profiler.html, https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity.html
> Fetched: 2026-03-27

## Performance Targets for 2D PC Card Game

| Metric | Target | Tool |
|--------|--------|------|
| Frame Rate | 60 FPS stable | Profiler |
| Draw Calls | < 50 per frame | Frame Debugger |
| Memory | < 500 MB | Memory Profiler |
| Load Time | < 3 sec per stage | Profiler |
| GC Alloc | < 1 KB/frame | Profiler |

## Unity Profiler

### Opening
```
Window → Analysis → Profiler (Ctrl+7)
```

### Key Modules

| Module | What to Monitor |
|--------|----------------|
| CPU Usage | Frame time, script execution, physics |
| GPU Usage | Draw calls, shader complexity |
| Rendering | Batches, triangles, set pass calls |
| Memory | Total allocated, GC allocations |
| Audio | Active sources, memory usage |

### Deep Profile
Enable for line-by-line script performance (slower, more detail):
```
Profiler → CPU Usage → Deep Profile toggle
```

## Frame Debugger

```
Window → Analysis → Frame Debugger
```

Shows every draw call in order. Use to identify:
- Un-batched sprites (different materials/textures)
- Overdraw from overlapping transparent sprites
- Unnecessary render passes

## Optimization Techniques

### 1. Sprite Atlas Batching

```
Assets → Create → 2D → Sprite Atlas
```

**Rules:**
- Pack sprites by sorting layer (all background sprites in one atlas)
- Pack sprites used together (all cards in one atlas)
- Max atlas size: 2048x2048 or 4096x4096
- Enable Tight Packing to reduce wasted space

**Impact:** Reduces draw calls from 50+ to <10 for card hand rendering

### 2. Object Pooling

```csharp
public class ObjectPool<T> where T : Component
{
    Queue<T> pool = new Queue<T>();
    T prefab;
    Transform parent;

    public ObjectPool(T prefab, int initialSize, Transform parent)
    {
        this.prefab = prefab;
        this.parent = parent;
        for (int i = 0; i < initialSize; i++)
        {
            T obj = Object.Instantiate(prefab, parent);
            obj.gameObject.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public T Get()
    {
        T obj = pool.Count > 0 ? pool.Dequeue() : Object.Instantiate(prefab, parent);
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

**Use for:** Damage numbers, VFX particles, card instances, enemy spawns

### 3. Garbage Collection Avoidance

**Common GC triggers and solutions:**

| Trigger | Solution |
|---------|----------|
| `string + string` | StringBuilder or string.Format |
| `new List<T>()` in Update | Cache and reuse collections |
| LINQ queries | Use for loops |
| `GetComponent<T>()` in Update | Cache in Start/Awake |
| Boxing (int → object) | Use generic methods |
| Coroutine `new WaitForSeconds` | Cache WaitForSeconds |

```csharp
// BAD - allocates every frame
void Update() {
    var enemies = FindObjectsOfType<Enemy>();  // GC alloc!
}

// GOOD - cache reference
List<Enemy> enemies = new List<Enemy>();
void Start() {
    enemies.AddRange(FindObjectsOfType<Enemy>());
}
```

### 4. Camera Culling
```csharp
// Only render sprites within camera bounds
Camera.main.orthographicSize  // Visible half-height
// Disable renderers outside camera view
```

### 5. Particle System Optimization

| Setting | Recommendation |
|---------|---------------|
| Max Particles | Keep ≤ 100 per system |
| Simulation Space | Local (cheaper than World) |
| Render Mode | Billboard (cheapest) |
| Collision | Disable if not needed |
| Noise | Disable if not needed |
| Trails | Limit length |

### 6. Audio Optimization

| Setting | Recommendation |
|---------|---------------|
| Load Type | Compressed In Memory (SFX), Streaming (BGM) |
| Compression | Vorbis for BGM, ADPCM for SFX |
| Sample Rate | Override to 22050 Hz for SFX |
| Max Voices | Limit simultaneous audio sources |

### 7. Asset Loading

- Use Addressables for on-demand loading
- Preload next stage during current stage play
- Unload previous stage assets on transition
- Use async loading to avoid frame hitches

## Profiling Checklist

- [ ] CPU: Main thread < 16.6ms (60fps target)
- [ ] GPU: Rendering < 16.6ms
- [ ] Draw calls: < 50 per frame
- [ ] GC allocations: < 1KB per frame during gameplay
- [ ] Memory: Total < 500MB
- [ ] No frame spikes > 33ms during combat
- [ ] Stage transition load < 3 seconds
- [ ] Audio: < 32 simultaneous voices
