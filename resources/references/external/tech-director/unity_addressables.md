# Unity Addressables Asset Management Guide

> Source: https://docs.unity3d.com/Packages/com.unity.addressables@latest
> Fetched: 2026-03-27

## Overview

Unity Addressables is an asset management system that allows loading assets by address (string key) instead of direct references. It simplifies asset loading, memory management, and content updates — critical for games with many art assets like card games.

## Why Addressables for Card Games

| Problem | Addressables Solution |
|---------|----------------------|
| Loading 78+ card art assets at startup | Load on demand by card ID |
| Memory spikes during stage transitions | Unload previous stage assets |
| DLC card packs post-launch | Remote content catalogs |
| Long build times with all assets | Separate asset bundles |

## Setup

### Installation
```
Window → Package Manager → Addressables → Install
Window → Asset Management → Addressables → Groups
→ Create Addressables Settings
```

### Making Assets Addressable
1. Select asset in Project window
2. Check "Addressable" in Inspector
3. Assign address (default = asset path, can customize)
4. Assign to Group

### Group Organization for Card Game
```
Groups:
├── Core (Local)           → Always loaded: UI, fonts, common VFX
├── Characters (Local)     → Character sprites, spine data
├── Cards (Local)          → Card art, frames, backgrounds
├── Stages_1 (Local)       → Stage 1 backgrounds, enemies
├── Stages_2 (Local)       → Stage 2 backgrounds, enemies
├── Stages_3 (Local)       → Stage 3 backgrounds, enemies
├── Stages_4 (Local)       → Stage 4 backgrounds, enemies, final boss
├── Audio_BGM (Local)      → Background music per stage
├── Audio_SFX (Local)      → Sound effects
└── DLC_Pack1 (Remote)     → Future DLC content
```

## Loading Assets

### Basic Load
```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

// Load sprite by address
AsyncOperationHandle<Sprite> handle = Addressables.LoadAssetAsync<Sprite>("card_fortune_forward");
handle.Completed += (op) => {
    if (op.Status == AsyncOperationStatus.Succeeded)
        cardImage.sprite = op.Result;
};

// Async/Await pattern (Unity 2023+)
Sprite sprite = await Addressables.LoadAssetAsync<Sprite>("card_fortune_forward").Task;
```

### Load by Label
```csharp
// Load all stage 1 assets
AsyncOperationHandle<IList<GameObject>> handle =
    Addressables.LoadAssetsAsync<GameObject>("stage_1", null);
```

### Instantiate
```csharp
// Instantiate prefab by address
AsyncOperationHandle<GameObject> handle =
    Addressables.InstantiateAsync("prefab_enemy_swords");
```

## Memory Management

### Release Assets
```csharp
// Release loaded asset
Addressables.Release(handle);

// Release instantiated object
Addressables.ReleaseInstance(gameObject);
```

### Stage Transition Pattern
```csharp
public class StageLoader : MonoBehaviour
{
    AsyncOperationHandle currentStageHandle;

    public async Task LoadStage(int stageNumber)
    {
        // Unload previous stage
        if (currentStageHandle.IsValid())
            Addressables.Release(currentStageHandle);

        // Force garbage collection
        await Resources.UnloadUnusedAssets();

        // Load new stage
        currentStageHandle = Addressables.LoadAssetsAsync<Object>(
            $"stage_{stageNumber}", null);
        await currentStageHandle.Task;
    }
}
```

## Build & Profile

### Build
```
Window → Asset Management → Addressables → Groups
→ Build → New Build → Default Build Script
```

### Analyze
```
Window → Asset Management → Addressables → Analyze
→ Check Duplicate Bundle Dependencies
→ Bundle Layout Preview
```

### Event Viewer (Profiling)
```
Window → Asset Management → Addressables → Event Viewer
→ Monitor asset load/unload in real time
```

## Best Practices

1. **Group by loading pattern**: Assets loaded together should be in the same group
2. **Address naming**: Use consistent naming (`character_{name}_{state}`)
3. **Release promptly**: Release assets when leaving a stage
4. **Preload critical assets**: Load Core group during splash screen
5. **Use labels**: Tag assets for batch loading (`"stage_1"`, `"boss"`, `"vfx"`)
6. **Profile regularly**: Use Event Viewer to catch memory leaks
