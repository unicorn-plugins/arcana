# Spine-Unity Runtime Integration Guide

> Source: http://esotericsoftware.com/spine-unity
> Fetched: 2026-03-27

## Overview

Spine is a 2D skeletal animation tool designed for game development. The Spine-Unity runtime integrates Spine animations into Unity, providing components for rendering, controlling, and interacting with Spine skeletons.

## Installation

### Via Unity Package Manager (UPM)
1. Download spine-unity package from esotericsoftware.com
2. Import via Assets → Import Package → Custom Package
3. Or add via Package Manager from Git URL

### Required Files per Character
```
character.json       (or .skel.bytes for binary)
character.atlas.txt  (atlas descriptor)
character.png        (atlas texture, may be multiple)
```

## Core Components

### SkeletonAnimation
Primary component for Spine animations in Unity.

```csharp
// Basic usage
SkeletonAnimation skeletonAnimation = GetComponent<SkeletonAnimation>();

// Set animation
skeletonAnimation.AnimationState.SetAnimation(0, "idle", true);  // track 0, loop

// Queue animation
skeletonAnimation.AnimationState.AddAnimation(0, "attack", false, 0); // after current

// Set skin
skeletonAnimation.Skeleton.SetSkin("warrior");
skeletonAnimation.Skeleton.SetSlotsToSetupPose();
```

**Properties:**
- Skeleton Data Asset: Reference to imported Spine data
- Initial Skin: Default skin name
- Initial Animation: Default animation name
- Loop: Whether initial animation loops
- Time Scale: Animation playback speed

### SkeletonMecanim
Integrates Spine with Unity's Animator Controller (Mecanim).

**When to use:**
- SkeletonAnimation: Direct API control (recommended for games)
- SkeletonMecanim: When you need Animator state machines

### SkeletonGraphic
For Spine animations in Unity UI (Canvas).

```csharp
// Use for: Card illustrations, UI character portraits
SkeletonGraphic skeletonGraphic = GetComponent<SkeletonGraphic>();
skeletonGraphic.AnimationState.SetAnimation(0, "card_idle", true);
```

## Animation Control

### Tracks
Spine supports layered animation tracks (like animation layers):

```csharp
var state = skeletonAnimation.AnimationState;

// Track 0: Body movement (walk, idle, attack)
state.SetAnimation(0, "walk", true);

// Track 1: Upper body overlay (wave, hold item)
state.SetAnimation(1, "wave", false);

// Track 2: Face expression
state.SetAnimation(2, "happy", true);
```

### Animation Events

```csharp
// Subscribe to events
skeletonAnimation.AnimationState.Event += OnSpineEvent;
skeletonAnimation.AnimationState.Complete += OnAnimationComplete;

void OnSpineEvent(TrackEntry entry, Spine.Event e)
{
    if (e.Data.Name == "hit_impact")
    {
        // Trigger VFX, screen shake, damage number
        SpawnHitEffect(transform.position);
    }
    else if (e.Data.Name == "card_flip")
    {
        // Card animation event
        OnCardFlipped();
    }
}

void OnAnimationComplete(TrackEntry entry)
{
    if (entry.Animation.Name == "attack_forward")
    {
        // Return to idle after attack
        skeletonAnimation.AnimationState.SetAnimation(0, "idle", true);
    }
}
```

### Mixing (Crossfade)

```csharp
// Set default mix duration
var stateData = skeletonAnimation.AnimationState.Data;
stateData.DefaultMix = 0.2f; // 0.2 second crossfade

// Custom mix for specific transitions
stateData.SetMix("idle", "attack", 0.1f);  // Fast transition to attack
stateData.SetMix("attack", "idle", 0.3f);  // Slower return to idle
```

## Skin System

Spine skins allow swapping character appearances:

```csharp
var skeleton = skeletonAnimation.Skeleton;

// Single skin
skeleton.SetSkin("default");

// Combined skins (mix and match)
var combinedSkin = new Skin("combined");
combinedSkin.AddSkin(skeleton.Data.FindSkin("body_base"));
combinedSkin.AddSkin(skeleton.Data.FindSkin("armor_gold"));
combinedSkin.AddSkin(skeleton.Data.FindSkin("weapon_sword"));
skeleton.SetSkin(combinedSkin);
skeleton.SetSlotsToSetupPose();
```

**Use case for Arcana**: Different card states (normal, reversed, ultimate) as skins.

## Rendering

### Materials and Shaders
- Default: `Spine/Skeleton` (unlit)
- For URP 2D Lighting: `Spine/Sprite/Vertex Lit` or `Spine/Sprite/Pixel Lit`
- For normal maps: Use lit shaders with normal map in material

### Draw Order
Spine manages internal draw order of skeleton parts.
Unity sorting is handled via:
- Sorting Layer on SkeletonAnimation
- Order in Layer
- Follow Skeleton Draw Order (default: on)

### Tinting

```csharp
// Tint entire skeleton
skeleton.SetColor(new Color(1, 0.5f, 0.5f, 1)); // Reddish tint (damage flash)

// Tint specific slot
var slot = skeleton.FindSlot("body");
slot.SetColor(Color.red);
```

## Performance Tips

| Tip | Impact |
|-----|--------|
| Use binary format (.skel.bytes) | Faster loading |
| Share atlas textures | Fewer draw calls |
| Limit active skeletons | CPU (pose calculation) |
| Use MeshRenderer batching | Fewer draw calls |
| Disable unused tracks | CPU savings |
| Pool SkeletonAnimation objects | Reduce GC |

## Common Patterns for Card Games

### Card Character Animation
```csharp
public class CardCharacter : MonoBehaviour
{
    SkeletonAnimation spine;

    public void PlayForwardSkill()
    {
        spine.AnimationState.SetAnimation(0, "skill_forward", false);
        spine.AnimationState.AddAnimation(0, "idle", true, 0);
    }

    public void PlayReverseSkill()
    {
        spine.AnimationState.SetAnimation(0, "skill_reverse", false);
        spine.AnimationState.AddAnimation(0, "idle", true, 0);
    }

    public void PlayUltimate()
    {
        spine.AnimationState.SetAnimation(0, "ultimate", false);
        spine.AnimationState.AddAnimation(0, "idle", true, 0);
    }

    public void PlayDefeat()
    {
        spine.AnimationState.SetAnimation(0, "defeat", false);
    }

    public void SetDamageFlash()
    {
        StartCoroutine(DamageFlashCoroutine());
    }

    IEnumerator DamageFlashCoroutine()
    {
        spine.Skeleton.SetColor(Color.red);
        yield return new WaitForSeconds(0.1f);
        spine.Skeleton.SetColor(Color.white);
    }
}
```
