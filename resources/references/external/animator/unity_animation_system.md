# Unity Animation System (Animator, AnimationClip)

> Source: https://docs.unity3d.com/Manual/AnimationSection.html
> Fetched: 2026-03-27

## Overview

Unity provides tools and processes to animate the properties of models and assets, such as transform properties for movement and rotation, or light intensity adjustments. Unity offers two animation systems:

### Mecanim Animation System (Recommended)
- Uses the Animator component, Animation window, and Animator window
- Provides better performance for complex character animation with many animation curves and blending
- Recommended for most use cases

### Legacy Animation System
- Uses the Animation component
- Maintained for backward compatibility with older projects
- Better suited for simpler animation scenarios

---

## Core Components

### 1. Animation Clips

Animation Clips are the smallest building blocks of animation in Unity. They represent an isolated piece of motion, such as RunLeft, Jump, or Crawl, and can be manipulated and combined in various ways to produce lively end results.

**Sources for Animation Clips:**

- **Imported from External Sources:**
  - Humanoid animations captured at motion capture studios
  - Artist-created animations from 3D applications (3ds Max, Maya)
  - Third-party animation sets from the Asset Store
  - Multiple clips extracted from single motion files

- **Created Within Unity:**
  - Transform properties (position, rotation, scale) of GameObjects
  - Component attributes (material colors, light intensity, audio volume)
  - Custom script variables (floats, integers, enums, vectors, booleans)
  - Function call timing within scripts

#### Animation Clip Inspector

The Animation tab in the Inspector contains five primary sections:

1. **Asset-specific properties** -- Settings affecting all animation clips in the imported asset
2. **Clip selection list** -- Choose clips to view and preview their animations
3. **Clip-specific properties** -- Settings for individual animation clips
4. **Properties for all clips** -- Shared settings across clips
5. **Animation preview** -- Playback and frame-selection tools

#### Import Compression Options

| Option | Description |
|--------|-------------|
| Off | Preserves all keyframes (highest precision, largest file size) |
| Keyframe Reduction | Reduce redundant keyframes on import |
| Keyframe Reduction and Compression | Combines file-size reduction with runtime optimization |
| Optimal | Unity automatically selects the best compression method |

#### Root Motion Control

Separate configuration available for:
- **Rotation**: Bake into pose or store as root motion
- **Position Y (vertical)**: Control vertical movement extraction
- **Position XZ (horizontal)**: Control horizontal movement extraction

#### Looping Configuration

- **Loop Time**: Restart animation when reaching the end
- **Loop Pose**: Enable seamless motion cycling
- **Cycle Offset**: Adjust looping start points

#### Additional Clip Properties

- **Mirror**: Flip left-right animations (Humanoid only)
- **Additive Reference Pose**: Set frame for additive animation layers
- **Curves**: Manage animation curves for imported clips
- **Events**: Configure animation events triggered during playback
- **Mask**: Apply Avatar masking to specific bones

---

### 2. Animator Controller

An Animator Controller is a core Unity asset that manages animation playback for characters and GameObjects. It arranges and maintains a set of Animation Clips and associated Animation Transitions for a character or an animated GameObject.

The Animator Controller operates as a state machine system that organizes animations and defines how transitions occur between them.

**Key Point:** Even single animation clips require placement within an Animator Controller to function on a GameObject.

#### Creation Methods

- **Automatic**: Unity generates one when you begin animating via the Animation Window or attach a clip to a GameObject
- **Manual**: Right-click in the Project window > **Create** > **Animator Controller**

#### Navigation in the Animator Window

- **Zoom**: Scroll wheel
- **Focus Selected**: Press F to zoom to selected states
- **Fit All**: Press A to display all animation states
- **Play Mode Panning**: View automatically follows the active state

#### Animator Window Components

- **State Machine View**: Central workspace displaying the animation state machine
  - Right-click on the grid to create new state nodes
  - Middle mouse button or Alt+drag to pan
  - Click and drag state nodes to reorganize
- **Parameters Panel**: Variables for scripting-to-Animator communication
  - Float, Int, Bool, Trigger types
- **Layers Panel**: Create and manage independent animation layers
- **Breadcrumb List**: Navigate nested sub-states or blend trees
- **Lock Icon**: Lock focus to prevent unwanted focus shifts

---

### 3. Animator Component

A component on a model that animates that model using the Animation system, with references to both the Animator Controller and Avatar (when needed).

---

### 4. Avatar System

An interface for retargeting animation from one rig to another, specifically designed for humanoid characters. The Avatar maps character skeletons to a common internal format, enabling animation retargeting and muscle definition adjustments.

---

## Animation State Machines

A state machine is a system diagram consisting of nodes (states) connected by lines (transitions). A state machine is only in one state at a time and remains in the same state until conditions for a transition are met.

### States

Each state contains an animation that plays upon entry. The animation can:
- Play once
- Loop continuously
- Blend multiple animation clips together

### Transitions

Transitions define how long the blend between states should take and the conditions that activate them. Transition criteria include:
- Animation completion
- Specific action completion
- A set of conditions becoming true

### Sub-State Machines

For complex systems, Sub-State Machines allow developers to divide larger state machines into manageable sections.

### Practical Example

A character movement state machine might include:
- **Idle** (standing still)
- **Walking**
- **Running**
- **Jumping**

When a user inputs movement commands, the system transitions from idle to walking based on input conditions.

---

## Blend Trees

Blend Trees enable smooth blending of multiple animations using numeric parameters that control each motion's contribution to the final result.

### Blend Trees vs. Transitions

- **Transitions**: Moving between different animation states over a specified duration with defined activation conditions
- **Blend Trees**: Continuously blend multiple animations using a parameter that controls each motion's contribution

### Animation Requirements for Blending

- Animations must be similar in nature and timing
- Key moments should occur at matching points in normalized time
- Example: walking and running animations should have foot contact points aligned at identical normalized time values

### Creating a Blend Tree

1. Right-click empty space in the Animator Controller view
2. Select **Create State** > **From New Blend Tree**
3. Double-click the Blend Tree to enter the graph editor

### Blend Tree Types

| Type | Description |
|------|-------------|
| 1D Blending | Linear parameter-based blending |
| 2D Blending | Two-parameter blending for complex animations |
| Direct Blending | Direct control over animation contributions |

---

## Animation Layers

Animation Layers enable management of complex state machines across different body parts.

**Common use case:** A lower-body layer for walking-jumping, and an upper-body layer for throwing objects / shooting.

### Blending Modes

- **Override**: Animation on this layer replaces animations from previous layers
- **Additive**: Animation stacks on top of previous layer animations

### Avatar Masks

The Mask property allows you to specify the body parts on which to apply the animation. For example, apply a throwing animation exclusively to the upper body while the character walks.

### Layer Syncing

Enable the **Sync** checkbox to reuse the same state machine structure across layers while using different animation clips. The **Timing** checkbox controls whether the original layer determines animation length or balances between layers based on weight.

---

## Animation Events

Animation events allow you to attach additional data to imported clips which determines when certain actions should occur in time with the animation.

### Creating Animation Events

1. Expand the Events section in the Animation tab
2. Position the playback head to the exact frame
3. Click the **Add Event** button
4. Configure the **Function** property field with the function name

### Event Parameter Types

| Type | Use Case |
|------|----------|
| Float | Volume levels, intensity values |
| Int | Index values, counters |
| String | Text labels, identifiers |
| Object | References to GameObjects or Prefabs |

### Example Use Cases

- Play footstep sounds at specific animation frames
- Instantiate visual effects synchronized with actions
- Trigger gameplay logic at precise animation moments

---

## Root Motion

Root Motion controls how characters move through space based on animation data.

### Body Transform

The Body Transform represents the character's mass center and serves as the foundation for the retargeting engine. It's calculated as an average of the lower and upper body orientation relative to the Avatar's T-Pose.

### Root Transform

The Root Transform is a projection on the Y plane of the Body Transform, computed at runtime. At each frame, changes to the Root Transform are calculated and applied to the GameObject.

### Configuration

#### Root Transform Rotation
- **Bake into Pose**: Keeps orientation on the body transform; GameObject won't rotate
- **Based Upon**: Body Orientation, Original, or manual Offset

#### Root Transform Position (Y)
- **Bake into Pose**: Prevents height changes to the GameObject
- **Based Upon**: Original, Mass Center (Body), or Feet (prevents floating during blends)

#### Root Transform Position (XZ)
- **Bake into Pose**: Used for idle animations to prevent position drift

### Loop Pose

Loop Pose blending occurs within the Root Transform reference frame. Pose differences between start and stop frames are distributed across the clip's 0-100% range.

### Generic Animations

For non-humanoid characters, the system uses the **Root Node** transform instead of the Body Transform.

---

## Inverse Kinematics (IK)

IK enables animation by working backwards from a target position to calculate joint rotations, rather than rotating joints to predetermined angles.

### Setup Requirements

1. **Valid Avatar** - Correctly configured humanoid Avatar
2. **Animator Controller** - At least one animation assigned
3. **IK Pass** - Enable in the Animator window's Base Layer settings
4. **Script Implementation** - Use the `OnAnimatorIK()` callback

### Animator IK Methods

```csharp
// Position and rotation weights (0 = disabled, 1 = full influence)
animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1);
animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1);

// Set target position and rotation
animator.SetIKPosition(AvatarIKGoal.RightHand, targetPosition);
animator.SetIKRotation(AvatarIKGoal.RightHand, targetRotation);

// Look At
animator.SetLookAtWeight(1);
animator.SetLookAtPosition(lookTarget.position);
```

### Implementation Example

```csharp
using UnityEngine;

public class IKControl : MonoBehaviour {
    Animator animator;
    public bool ikActive = false;
    public Transform rightHandObj = null;
    public Transform lookObj = null;

    void Start() {
        animator = GetComponent<Animator>();
    }

    void OnAnimatorIK() {
        if (ikActive) {
            if (lookObj != null) {
                animator.SetLookAtWeight(1);
                animator.SetLookAtPosition(lookObj.position);
            }

            if (rightHandObj != null) {
                animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1);
                animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1);
                animator.SetIKPosition(AvatarIKGoal.RightHand, rightHandObj.position);
                animator.SetIKRotation(AvatarIKGoal.RightHand, rightHandObj.rotation);
            }
        }
    }
}
```

---

## Animator Class API Reference

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `applyRootMotion` | bool | Apply root motion displacement to GameObject |
| `avatar` | Avatar | Current Avatar for humanoid animation |
| `cullingMode` | AnimatorCullingMode | Visibility-based culling behavior |
| `speed` | float | Playback speed multiplier (1.0 = normal) |
| `updateMode` | AnimatorUpdateMode | Update timing (normal, animated physics, unscaled) |
| `runtimeAnimatorController` | RuntimeAnimatorController | Active controller driving states |
| `isHuman` | bool | True if rig is humanoid |
| `layerCount` | int | Number of animation layers |
| `parameterCount` | int | Number of parameters |

### State Control Methods

```csharp
// Force transition to specified state
void Play(string stateName, int layer = -1, float normalizedTime = float.NegativeInfinity)

// Play state using fixed time
void PlayInFixedTime(string stateName, int layer = -1, float fixedTime = 0f)

// Smooth blend from current to target state
void CrossFade(string stateName, float transitionDuration, int layer = -1)

// Crossfade using fixed time values
void CrossFadeInFixedTime(string stateName, float transitionDuration, int layer = -1)
```

### Parameter Management

```csharp
// Set parameters
void SetFloat(string name, float value, float dampTime = 0f, float deltaTime = Time.deltaTime)
void SetInteger(string name, int value)
void SetBool(string name, bool value)
void SetTrigger(string name)

// Get parameters
float GetFloat(string name)
bool GetBool(string name)
int GetInteger(string name)
```

### State Queries

```csharp
AnimatorStateInfo GetCurrentAnimatorStateInfo(int layerIndex)
AnimatorStateInfo GetNextAnimatorStateInfo(int layerIndex)
bool IsInTransition(int layerIndex)
AnimatorClipInfo[] GetCurrentAnimatorClipInfo(int layerIndex)
```

### Layer Management

```csharp
void SetLayerWeight(int layerIndex, float weight)   // 0 = inactive, 1 = full
int GetLayerIndex(string layerName)
string GetLayerName(int layerIndex)
float GetLayerWeight(int layerIndex)
```

### Target Matching

```csharp
void MatchTarget(Vector3 matchPosition, Quaternion matchRotation,
    AvatarTarget target, MatchTargetWeightMask weightMask,
    float startNormalizedTime, float targetNormalizedTime)
```

### Utility Methods

```csharp
void Rebind()                          // Rebuild internal bindings
void WriteDefaultValues()              // Write default property values
void ResetControllerState()            // Return to default initial state
static int StringToHash(string name)   // Convert name to hash ID for performance
```

### StateMachineBehaviour Callbacks

```csharp
void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
```

---

## Performance Considerations

- **Rebinding cost**: Occurs on initialization, controller changes, or GameObject enabling. Minimize through prebuilt controllers.
- **Humanoid overhead**: Generic animations perform better; humanoid clips incur 15-20% CPU overhead but enable clip reuse across characters.
- **Parallelization**: The system uses multi-threading, but grouping multiple Animators under one root prevents parallel Transform updates.
- **StateMachineBehaviour overhead**: Introduces synchronization points that can block parallel evaluation.

---

## Workflow Summary

1. Import or create animation clips
2. Organize clips in an Animator Controller
3. Configure Avatar mapping for humanoid characters
4. Attach Animator component to the model
5. Reference Controller and Avatar in the Inspector
6. Set up state machines, transitions, blend trees, and layers
7. Script parameter changes and state queries for gameplay integration
