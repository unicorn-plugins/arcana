# Spine Official Documentation + Spine-Unity Runtime Guide

> Source: http://esotericsoftware.com/spine-unity
> Fetched: 2026-03-27

## Overview

The spine-unity runtime is a Unity plugin supporting playback and manipulation of animations created with Spine. The implementation uses C# and builds upon the spine-csharp runtime, wrapping its structs and functions as Unity components.

**Key Features:**
- Imports files exported from the Spine Editor
- Stores animations in custom Unity asset types
- Based on the generic spine-csharp runtime architecture

> A Spine license is required to integrate the Spine Runtimes into your applications.

---

## Installation

### Prerequisites

- A functional Unity project
- Unity Editor installed from [unity3d.com](http://unity3d.com/get-unity)

### Option 1: Unitypackage Installation

1. Download the latest spine-unity unitypackage from the Spine Unity Download page
2. Import by double-clicking the file or dragging it onto the Project panel in Unity

### Option 2: Git Repository Installation

1. Clone the [spine-runtimes Git repository](https://github.com/esotericsoftware/spine-runtimes)
2. Copy contents from `spine-runtimes/spine-unity/Assets/` to your project's `Assets/` folder
3. Copy the `spine-runtimes/spine-csharp/src` folder to `Assets/Spine/Runtime/spine-csharp`

### Option 3: Unity Package Manager (UPM)

1. Open Package Manager via `Window > Package Manager`
2. Select the `+` icon and choose `Add package from git URL...`
3. Enter one of these URLs:
   - `https://github.com/EsotericSoftware/spine-runtimes.git?path=spine-csharp/src#4.2`
   - `https://github.com/EsotericSoftware/spine-runtimes.git?path=spine-unity/Assets/Spine#4.2`
   - `https://github.com/EsotericSoftware/spine-runtimes.git?path=spine-unity/Assets/Spine Examples#4.2`

The `#4.2` portion specifies the branch; you can alternatively use a specific commit hash for consistency across team members.

### Optional Extension Packages

- Timeline support
- Universal Render Pipeline (URP) shaders
- On-demand loading capabilities

### Updating

> **Critical:** Json and binary skeleton data files exported from Spine 4.1 or earlier will not be readable by the spine-unity 4.2 runtime!

Always re-export skeleton data using the current Spine editor version before updating. Back up your entire Unity project beforehand.

---

## Main Components

### Adding Skeletons to Scenes

**Quick Start Method:**
1. Import skeleton data and texture atlas assets
2. Drag the `_SkeletonData` asset into the Scene view
3. Select `SkeletonAnimation` from the instantiation menu

**Manual Setup:**
1. Create an empty GameObject
2. Add `SkeletonAnimation` component (automatically adds `MeshRenderer` and `MeshFilter`)
3. Assign `_SkeletonData` asset to the Skeleton Data Asset property

> In case you only see bones of a skeleton in Scene view without any images attached, you might want to switch the Initial Skin property to a skin other than default.

---

## Three Implementation Approaches

### 1. SkeletonAnimation Component

The recommended approach offering the most complete feature set with Spine's custom animation system.

**Key Features:**
- Uses Spine's custom animation and event system
- Renders via `MeshRenderer`, compatible with `SpriteMask`
- Highest customization capability
- Smooth transitions and mixing between animations

**Setting Skeleton Data:**

```csharp
using Spine.Unity;

public class YourComponent : MonoBehaviour {
    SkeletonAnimation skeletonAnimation;
    Spine.Skeleton skeleton;

    void Awake() {
        skeletonAnimation = GetComponent<SkeletonAnimation>();
        skeleton = skeletonAnimation.Skeleton;
        animationState = skeletonAnimation.AnimationState;
    }
}
```

**Initial Configuration Parameters:**
- *Initial Skin*: Determines which skin displays at startup
- *Animation Name*: Animation to play on start
- *Loop*: Whether initial animation repeats
- *Time Scale*: Playback speed multiplier
- *Unscaled Time*: Uses `Time.unscaledDeltaTime` for UI independence

**Advanced Parameters:**

| Parameter | Function |
|-----------|----------|
| Initial Flip X/Y | Horizontal/vertical skeleton flipping |
| Animation Update | `Update`, `FixedUpdate`, or manual mode |
| Update When Invisible | Behavior for culled renderers |
| Use Single Submesh | Single material optimization |
| Fix Draw Order | Prevents aggressive batching with 3+ submeshes |
| Immutable Triangles | Optimizes for static attachment visibility |
| Clear State on Disable | Resets state when disabled (useful for pooling) |
| Z-Spacing | Back-to-front rendering offset |
| PMA Vertex Colors | Enables premultiplied alpha blending |
| Tint Black | Adds black tint vertex data |
| Add Normals | Generates vertex normals for lit shaders |
| Solve Tangents | Calculates tangents for normal maps |

### 2. SkeletonMecanim Component

Integrates with Unity's Mecanim animation system for high-level animation control.

**When to Use:**
- Projects already using Mecanim state machines
- Complex layer-based animation blending
- Standard Unity animation workflow preference

**Limitations:**
- Requires additional timeline keys at animation first frames for smooth mixing
- Less flexible animation mixing than `SkeletonAnimation`
- `TrackEntry.MixAttachmentThreshold` unavailable

> To smoothly mix out a timeline state (e.g. bone rotation) from one animation to the next, the second animation requires an additional key at the first frame when in setup pose.

**Animation Blending Control:**

- **Mix Next** (recommended for Base Layer): Previous track applies, next track mixes in using transition weights
- **Always Mix** (recommended for Additive): Fades out previous track, mixes in next track
- **Hard** (previously "Spine Style"): Immediately applies next track
- **Match** (new in 4.2): Calculates Spine animation weights matching Mecanim clip weights

**Event Handling:**

Events in Mecanim are stored within `AnimationClip` objects and work like standard Unity animation events:

```csharp
public class EventHandler : MonoBehaviour {
    // For event "Footstep" outside folders
    void Footstep() {
        Debug.Log("Footstep event received");
    }

    // For event "Footstep" in folder "Foldername"
    void FoldernameFootstep() {
        Debug.Log("Footstep in folder received");
    }
}
```

### 3. SkeletonGraphic Component

Designed for UI rendering within Canvas systems.

**Key Characteristics:**
- Subclasses `UnityEngine.UI.MaskableGraphic`
- Uses `CanvasRenderer` for UI pipeline compatibility
- Compatible with `RectMask2D` and UI masking
- Single-texture limitation by default

> Only use Materials with special CanvasRenderer compatible shaders at SkeletonGraphic components, such as the `Spine/SkeletonGraphic*` shaders which are assigned by default.

**Layout Scale Mode Options:**
- None (default)
- Width Controls Height
- Height Controls Width
- Fit In Parent
- Envelope Parent

**Render Separation:** When enabled, `SkeletonGraphic` automatically creates child `CanvasRenderer` GameObjects for each submesh, allowing flexible draw order control.

---

## Component Lifecycle

### SkeletonAnimation Update Sequence

1. **BeforeApply**: Raised before animations apply; modify skeleton state before animation influence
2. **UpdateLocal**: Raised after animations update local values; read/modify local bone transforms
3. **UpdateComplete**: Raised after world transforms calculate; read bone world values
4. **UpdateWorld**: Raises second world transform calculation; modify local values based on world values

```csharp
void AfterUpdateComplete(ISkeletonAnimation anim) {
    // Called after animation updates complete
}

void Start() {
    skeletonAnimation.UpdateComplete += AfterUpdateComplete;
}
```

### SkeletonRenderer Callbacks

- **OnRebuild**: Raised after skeleton initialization succeeds
- **OnMeshAndMaterialsUpdated**: Raised after mesh and materials update in `LateUpdate()`

```csharp
void AfterMeshAndMaterialsUpdated(SkeletonRenderer renderer) {
    // Called after mesh and materials update
}

void Start() {
    skeletonAnimation.OnMeshAndMaterialsUpdated += AfterMeshAndMaterialsUpdated;
}
```

### Script Execution Order

1. **SkeletonAnimation.Update**: Animations progress, apply to skeleton
2. **SkeletonAnimation.LateUpdate**: Skeleton mesh updates

```csharp
[DefaultExecutionOrder(-1)]
public class SetupPoseComponent : MonoBehaviour {
    void Update() {
        skeleton.SetToSetupPose();
        // Ensures setup pose precedes animation application
    }
}
```

---

## Manual Updates

**Update(deltaTime)** - Full skeleton update without mesh regeneration:

```csharp
skeleton.SetToSetupPose();
skeletonAnimation.Update(0); // Update without advancing time

skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeleton); // Apply without updating state
```

**ApplyAnimation()** - Re-applies current animations without updating `AnimationState`.

**LateUpdateMesh()** - Updates skeleton mesh based on current state:

```csharp
void LateUpdate() {
    skeleton.SetToSetupPose();
    skeletonAnimation.Update(0);
    skeletonAnimation.LateUpdateMesh(); // Regenerate mesh
}
```

---

## Skeleton Control

### Setting Attachments

```csharp
bool success = skeletonAnimation.Skeleton.SetAttachment("slotName", "attachmentName");

// Using property attributes
[SpineSlot] public string slotProperty = "slotName";
[SpineAttachment] public string attachmentProperty = "attachmentName";
bool success = skeletonAnimation.Skeleton.SetAttachment(slotProperty, attachmentProperty);
```

### Setup Pose Reset

```csharp
skeleton.SetToSetupPose();     // Reset bones and slots
skeleton.SetBonesToSetupPose(); // Bones only
skeleton.SetSlotsToSetupPose(); // Slots only
```

### Skin Management

```csharp
bool success = skeletonAnimation.Skeleton.SetSkin("skinName");
skeletonAnimation.Skeleton.SetSlotsToSetupPose();
```

> You likely want to call `Skeleton.SetSlotsToSetupPose` after changing skins if you don't want previously set attachments to affect the visibility of your current attachments.

### Combining Skins

```csharp
var skeleton = skeletonAnimation.Skeleton;
var skeletonData = skeleton.Data;
var mixAndMatchSkin = new Skin("custom-girl");

mixAndMatchSkin.AddSkin(skeletonData.FindSkin("skin-base"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("hair/brown"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("clothes/hoodie-orange"));

skeleton.SetSkin(mixAndMatchSkin);
skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeletonAnimation.Skeleton);
```

### Runtime Repacking

Combine texture regions into a single atlas to reduce draw calls:

```csharp
using Spine.Unity.AttachmentTools;

Skin repackedSkin = collectedSkin.GetRepackedSkin(
    "Repacked skin",
    skeletonAnimation.SkeletonDataAsset.atlasAssets[0].PrimaryMaterial,
    out runtimeMaterial,
    out runtimeAtlas
);

collectedSkin.Clear();
skeletonAnimation.Skeleton.Skin = repackedSkin;
skeletonAnimation.Skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeletonAnimation.Skeleton);
AtlasUtilities.ClearCache();
```

**Troubleshooting Repacking:**
- Read/Write must be enabled on source textures
- Compression must be disabled
- Quality tiers must use full resolution textures
- Source textures should be power-of-two

### Skeleton Scaling and Flipping

```csharp
bool isFlippedX = skeleton.ScaleX < 0;
skeleton.ScaleX = -1;
skeleton.ScaleY = -1;
skeleton.ScaleX = -skeleton.ScaleX; // Toggle flip state
```

### Manual Bone Access

```csharp
Bone bone = skeletonAnimation.Skeleton.FindBone("boneName");
Vector3 worldPosition = bone.GetWorldPosition(skeletonAnimation.transform);

Vector3 position = ...;
bone.SetPositionSkeletonSpace(position);

Quaternion worldRotationQuaternion = bone.GetQuaternion();
```

> Retrieve and apply bone positions during the `UpdateWorld` lifecycle delegate to avoid timing issues.

---

## Animation Control - AnimationState

The system uses tracks (numbered animation channels) supporting simultaneous overlapping animations with automatic mixing.

### Time Scale

```csharp
float timeScale = skeletonAnimation.timeScale;
skeletonAnimation.timeScale = 0.5f; // Half speed
skeletonAnimation.timeScale = 2f;   // Double speed
```

### Setting Animations

```csharp
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(trackIndex, "walk", true);

[SpineAnimation] public string animationProperty = "walk";
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(
    trackIndex, animationProperty, true);

// Using AnimationReferenceAsset
public AnimationReferenceAsset animationReferenceAsset;
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(
    trackIndex, animationReferenceAsset, true);
```

> **Warning:** Don't call `SetAnimation` every frame. It will start the animation anew each frame, freezing at the animation's first frame.

### Queueing Animations

```csharp
TrackEntry entry = skeletonAnimation.AnimationState.AddAnimation(
    trackIndex, "run", true, 2  // 2 second delay
);
```

### Empty Animation and Clearing

```csharp
TrackEntry entry = skeletonAnimation.AnimationState.SetEmptyAnimation(trackIndex, mixDuration);
entry = skeletonAnimation.AnimationState.AddEmptyAnimation(trackIndex, mixDuration, delay);
skeletonAnimation.AnimationState.ClearTrack(trackIndex);
skeletonAnimation.AnimationState.ClearTracks();
```

---

## AnimationState Events

### Event Types

1. **Start**: Animation begins playing
2. **Interrupt**: Animation interrupted by clearing or replacement
3. **Complete**: Animation finishes (fires multiple times if looped)
4. **End**: Animation stops playing
5. **Dispose**: Track entry and animation disposed
6. **Event**: User-defined custom event triggered

### Registering Listeners

```csharp
SkeletonAnimation skeletonAnimation;
Spine.AnimationState animationState;

void Awake() {
    skeletonAnimation = GetComponent<SkeletonAnimation>();
    animationState = skeletonAnimation.AnimationState;

    // Global event listeners
    animationState.Start += OnSpineAnimationStart;
    animationState.Interrupt += OnSpineAnimationInterrupt;
    animationState.End += OnSpineAnimationEnd;
    animationState.Dispose += OnSpineAnimationDispose;
    animationState.Complete += OnSpineAnimationComplete;
    animationState.Event += OnUserDefinedEvent;

    // Track entry event listeners
    Spine.TrackEntry trackEntry = animationState.SetAnimation(trackIndex, "walk", true);
    trackEntry.Start += OnSpineAnimationStart;
    trackEntry.Complete += OnSpineAnimationComplete;
}

public void OnSpineAnimationStart(TrackEntry trackEntry) { }
public void OnSpineAnimationInterrupt(TrackEntry trackEntry) { }
public void OnSpineAnimationEnd(TrackEntry trackEntry) { }
public void OnSpineAnimationDispose(TrackEntry trackEntry) { }
public void OnSpineAnimationComplete(TrackEntry trackEntry) { }

string targetEventName = "targetEvent";

public void OnUserDefinedEvent(Spine.TrackEntry trackEntry, Spine.Event e) {
    if (e.Data.Name == targetEventName) {
        // Handle user event
    }
}
```

### Delaying State Modifications in Callbacks

```csharp
trackEntry.End += e => {
    StartCoroutine(NextFrame(() => {
        YourCode();
    }));
};

IEnumerator NextFrame(System.Action call) {
    yield return 0;
    if (call != null) call();
}
```

### Coroutine Yield Instructions

```csharp
// Wait for specific events
var track = skeletonAnimation.state.SetAnimation(0, "interruptible", false);
var completeOrEnd = WaitForSpineAnimation.AnimationEventTypes.Complete |
                    WaitForSpineAnimation.AnimationEventTypes.End;
yield return new WaitForSpineAnimation(track, completeOrEnd);

// Wait for Complete
yield return new WaitForSpineAnimationComplete(track);

// Wait for End
yield return new WaitForSpineAnimationEnd(track);

// Wait for user-defined event
yield return new WaitForSpineEvent(skeletonAnimation.state, "spawn bullet");
```

---

## Scripting String Property Attributes

Popup fields automatically populate with available skeleton elements:

```csharp
[SpineBone] public string bone;
[SpineSlot] public string slot;
[SpineAttachment] public string attachment;
[SpineSkin] public string skin;
[SpineAnimation] public string animation;
[SpineEvent] public string event;
[SpineIkConstraint] public string ikConstraint;
[SpineTransformConstraint] public string transformConstraint;
[SpinePathConstraint] public string pathConstraint;
```

---

## Runtime Instantiation

```csharp
// From SkeletonDataAsset
SkeletonAnimation instance = SkeletonAnimation.NewSkeletonAnimationGameObject(skeletonDataAsset);

// SkeletonGraphic from SkeletonDataAsset
SkeletonGraphic instance = SkeletonGraphic.NewSkeletonGraphicGameObject(
    skeletonDataAsset, transform, skeletonGraphicMaterial);
```

From exported assets directly:

```csharp
// 1. Create AtlasAsset
SpineAtlasAsset runtimeAtlasAsset = SpineAtlasAsset.CreateRuntimeInstance(
    atlasTxt, textures, materialPropertySource, true);

// 2. Create SkeletonDataAsset
SkeletonDataAsset runtimeSkeletonDataAsset = SkeletonDataAsset.CreateRuntimeInstance(
    skeletonJson, runtimeAtlasAsset, true);

// 3. Create SkeletonAnimation
SkeletonAnimation instance = SkeletonAnimation.NewSkeletonAnimationGameObject(
    runtimeSkeletonDataAsset);
```

---

## Rendering

### Materials and Draw Calls

Each atlas page texture requires its own Material. Material switching between attachments creates draw calls:

- Attachment from Material A
- Attachment from Material A
- Attachment from Material B
- Attachment from Material A
- Result: 3 draw calls (A -> B -> A)

> Every material in the Materials array corresponds to a draw call.

**Optimization:** Pack attachments into fewer atlas pages and group them by draw order.

### Changing Materials Per Instance

```csharp
// Material override
originalMaterial = skeletonAnimation.SkeletonDataAsset.atlasAssets[0].PrimaryMaterial;
skeletonAnimation.CustomMaterialOverride[originalMaterial] = newMaterial;
skeletonAnimation.CustomMaterialOverride.Remove(originalMaterial); // disable

// Slot-specific
skeletonAnimation.CustomSlotMaterials[slot] = newMaterial;
skeletonAnimation.CustomSlotMaterials.Remove(slot);
```

### Tinting (Retains Batching)

```csharp
// Whole skeleton
skeleton.R = color.r;
skeleton.G = color.g;
skeleton.B = color.b;
skeleton.A = color.a;

// Individual slot
slot.R = slotColor.r;
slot.G = slotColor.g;
slot.B = slotColor.b;
slot.A = slotColor.a;
```

### MaterialPropertyBlocks

```csharp
MaterialPropertyBlock mpb = new MaterialPropertyBlock();
mpb.SetColor("_FillColor", Color.red);
mpb.SetFloat("_FillPhase", 1.0f);
GetComponent<MeshRenderer>().SetPropertyBlock(mpb);
```

### Transparency and Draw Order

Between meshes, rendering order follows:
1. Camera depth (multi-camera setups)
2. `Material.renderQueue` (overrides shader Queue tag)
3. Shader `Queue` tag (defaults to `"Transparent"`)
4. `SortingGroup` components on GameObject or parents
5. Renderer's `SortingLayer` and `sortingOrder`
6. Distance from camera

### Fading a Skeleton In or Out

Lowering alpha causes back skeleton parts to show through. Solution: render the skeleton to a temporary `RenderTexture` at normal opacity, then draw the texture at desired fade opacity. Use `SkeletonRenderTexture` and `SkeletonRenderTextureFadeout` utility components.

---

## Built-In Shaders Reference

| Shader | Description |
|--------|-------------|
| `Spine/Skeleton` | Default unlit transparent shader |
| `Spine/Skeleton Graphic` | Default for SkeletonGraphic (UI) |
| `Spine/Skeleton Lit` | Simple lit transparent, no normal maps |
| `Spine/Skeleton Lit ZWrite` | Lit transparent with z-buffer writing |
| `Spine/Skeleton Fill` | Unlit with customizable color overlay |
| `Spine/Skeleton Tint` | Two-color tint (light/dark areas) |
| `Spine/Skeleton Tint Black` | Animated per-slot tint black |
| `Spine/SkeletonGraphic Tint Black` | SkeletonGraphic variant with tint black |
| `Spine/Sprite/Unlit` | Configurable blend, overlay, HSB adjustments |
| `Spine/Sprite/Vertex Lit` | Vertex-lit with normal maps, cel-shading |
| `Spine/Sprite/Pixel Lit` | Per-pixel lit, receives realtime shadows |
| `Spine/Special/Skeleton Grayscale` | Grayscale with customizable intensity |
| `Spine/Blend Modes/*` | Additive, Multiply, Screen blend modes |

### Writing Custom Shaders

Key requirements for custom Spine shaders:
- **Backface culling must be disabled:** `Cull Off`
- **PMA handling:** Either export as Straight alpha or use `Blend One OneMinusSrcAlpha`
- **Vertex colors:** Use PMA blend mode or disable `Advanced - PMA Vertex Colors`
- **UI/non-UI rules:** Don't use UI shaders on SkeletonAnimation; don't use non-UI shaders on SkeletonGraphic

---

## Physics Inheritance

Controls Transform movement application to skeleton PhysicsConstraints:
- **Position**: XY movement with scale factors
- **Rotation**: Rotation movement with scale factor
- **Movement relative to**: Reference Transform for relative calculation

---

## Performance Tips

- Enable `Clear State on Disable` for proper pooling behavior
- Multiple materials on 2+ submeshes may require `Fix Draw Order` enabled
- Pack attachments into fewer atlas pages to minimize draw calls
- Cache `MaterialPropertyBlock` instances for frequent updates
- Use `Shader.PropertyToID()` for efficient property lookups
- Consider `SkeletonRenderSeparator` only when needed for inter-skeleton rendering
