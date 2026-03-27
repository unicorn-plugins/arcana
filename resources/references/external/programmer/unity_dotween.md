# DOTween Unity Tween Animation Library Documentation

> Source: https://dotween.demigiant.com/documentation.php
> Fetched: 2026-03-27

## Overview

DOTween (DOTween v2) is a fast, efficient, fully type-safe object-oriented animation engine for Unity, optimized for C#. It is over 400% faster than its predecessor HOTween, avoids unnecessary GC allocations, and provides extensive shortcuts and features for animating any value in Unity.

DOTween can animate these value types: `float`, `double`, `int`, `uint`, `long`, `ulong`, `Vector2`, `Vector3`, `Vector4`, `Quaternion`, `Rect`, `RectOffset`, `Color`, `string`, plus custom types via plugins.

---

## Setup

1. Download DOTween and unzip it anywhere in your Unity Assets folder (not inside Editor or Resources directories).
2. Open the DOTween Utility Panel via **Tools > Demigiant** menu.
3. Select **Setup DOTween...** to configure libraries for your Unity version.
4. Import the namespace in every script that uses DOTween:

```csharp
using DG.Tweening;
```

### Initialization (Optional)

```csharp
// Auto-initializes with defaults if not called
DOTween.Init(autoKillMode, useSafeMode, logBehaviour);

// With custom capacity
DOTween.Init(true, true, LogBehaviour.Verbose)
    .SetCapacity(200, 10);
```

---

## Core Concepts

| Term | Description |
|------|-------------|
| **Tweener** | Animates a single value toward a target |
| **Sequence** | Groups multiple tweens into a unified timeline |
| **Tween** | Generic term for both Tweeners and Sequences |

---

## Creating Tweens

### Method 1: Generic Approach (Most Flexible)

```csharp
// Tween any value with getter/setter
DOTween.To(() => myVector, x => myVector = x, new Vector3(3, 4, 8), 1f);

// Tween only alpha of a Color
DOTween.ToAlpha(() => myColor, x => myColor = x, 1f, duration);

// Tween a single axis
DOTween.ToAxis(() => myVector, x => myVector = x, 5f, 1f, AxisConstraint.X);

// Virtual tween (no target object, just calls a callback)
DOTween.To(x => MyCallback(x), 0f, 100f, 1f);
```

### Method 2: Shortcut Methods (Most Common)

Direct from known Unity objects:

```csharp
transform.DOMove(new Vector3(2, 3, 4), 1f);
rigidbody.DOMove(new Vector3(2, 3, 4), 1f);
material.DOColor(Color.green, 1f);
```

### Method 3: FROM Tweens

Reverses the animation direction — the object starts at the given value and animates to its current value:

```csharp
transform.DOMove(new Vector3(2, 3, 4), 1f).From();
transform.DOMoveX(2, 1f).From(true);  // Relative FROM value
```

**Important:** When you assign a FROM tween, the target immediately jumps to the FROM position.

---

## Shortcut Methods Reference

### Transform Shortcuts

| Method | Description |
|--------|-------------|
| `DOMove(Vector3, float)` | Move to world position |
| `DOLocalMove(Vector3, float)` | Move to local position |
| `DOMoveX/Y/Z(float, float)` | Move single axis |
| `DORotate(Vector3, float)` | Rotate to Euler angles |
| `DOLocalRotate(Vector3, float)` | Rotate in local space |
| `DORotateQuaternion(Quaternion, float)` | Rotate to quaternion |
| `DOScale(Vector3, float)` | Scale to value |
| `DOScaleX/Y/Z(float, float)` | Scale single axis |
| `DOJump(Vector3, float jumpPower, int numJumps, float)` | Jump with Y-axis arc |
| `DOLocalJump(...)` | Jump in local space |
| `DOLookAt(Vector3, float)` | Face toward position |
| `DOPath(Vector3[], float, PathType)` | Animate through waypoints |
| `DOLocalPath(Vector3[], float, PathType)` | Waypoints in local space |

### Special Transform Effects

| Method | Description |
|--------|-------------|
| `DOPunchPosition(Vector3, float, int, float)` | Elastic punch rebound |
| `DOPunchRotation(Vector3, float, int, float)` | Rotation punch |
| `DOPunchScale(Vector3, float, int, float)` | Scale punch |
| `DOShakePosition(float, float, int, float)` | Position vibration |
| `DOShakeRotation(float, Vector3, int, float)` | Rotation vibration |
| `DOShakeScale(float, float, int, float)` | Scale vibration |

### Material Shortcuts

| Method | Description |
|--------|-------------|
| `DOColor(Color, float)` | Animate color |
| `DOFade(float, float)` | Animate alpha |
| `DOFloat(float, string, float)` | Animate shader float property |
| `DOOffset(Vector2, float)` | Animate texture offset |
| `DOTiling(Vector2, float)` | Animate texture scale |

### UI Shortcuts (Canvas / Image / Text)

| Method | Description |
|--------|-------------|
| `DOColor(Color, float)` | Color tween |
| `DOFade(float, float)` | Alpha fade |
| `DOFillAmount(float, float)` | Image fill (Image only) |
| `DOText(string, float)` | Animated text reveal (Text/TMP) |
| `DOValue(float, float)` | Slider value (Slider only) |

### Audio Shortcuts

| Method | Description |
|--------|-------------|
| `DOFade(float, float)` | Volume fade |
| `DOPitch(float, float)` | Pitch change |

### Camera Shortcuts

| Method | Description |
|--------|-------------|
| `DOFieldOfView(float, float)` | FOV animation |
| `DOShakePosition(...)` | Camera shake (position) |
| `DOShakeRotation(...)` | Camera shake (rotation) |

### Rigidbody/Rigidbody2D Shortcuts

| Method | Description |
|--------|-------------|
| `DOMove(Vector3, float)` | Physics-aware position |
| `DOJump(Vector3, float, int, float)` | Physics-aware jump |
| `DORotate(Vector3, float)` | Physics-aware rotation |
| `DOPath(Vector3[], float, PathType)` | Physics-aware path |

---

## Sequences

Sequences group multiple tweens into a single controllable timeline.

```csharp
Sequence mySequence = DOTween.Sequence();
mySequence.Append(transform.DOMoveX(45, 1));
mySequence.Append(transform.DORotate(new Vector3(0, 180, 0), 1));
mySequence.PrependInterval(1);
mySequence.Insert(0, transform.DOScale(new Vector3(3, 3, 3), mySequence.Duration()));
```

### Sequence Methods

| Method | Description |
|--------|-------------|
| `Append(Tween)` | Add tween at the end of the sequence |
| `Prepend(Tween)` | Add tween at the beginning |
| `Insert(float time, Tween)` | Add tween at specific time position |
| `Join(Tween)` | Play simultaneously with the last appended tween |
| `AppendInterval(float)` | Add a pause at the end |
| `PrependInterval(float)` | Add a pause at the beginning |
| `AppendCallback(TweenCallback)` | Execute function at end |
| `InsertCallback(float, TweenCallback)` | Execute function at specific time |

**Important Notes:**
- Tweens inside Sequences cannot loop infinitely.
- You cannot reuse the same tween in multiple Sequences.
- Add all tweens to a Sequence before it starts playing.

---

## Chaining Settings

All settings can be chained using dot notation:

```csharp
transform.DOMoveX(4, 1)
    .SetEase(Ease.InOutQuint)
    .SetLoops(3, LoopType.Yoyo)
    .SetDelay(0.5f)
    .OnComplete(MyCallback);
```

### Timing Settings

| Method | Description |
|--------|-------------|
| `SetDelay(float)` | Delay before the tween starts |
| `SetSpeedBased(bool)` | Treat duration as speed (units/sec) |
| `timeScale` | Playback speed multiplier for this tween |

### Loop Settings

```csharp
.SetLoops(int loops, LoopType type)
```

| LoopType | Description |
|----------|-------------|
| `Restart` | Reset to start each cycle |
| `Yoyo` | Reverse direction each cycle |
| `Incremental` | Add to end value each cycle |

Use `-1` for infinite loops.

### Ease Settings

```csharp
.SetEase(Ease.OutQuint)
.SetEase(animationCurve)       // Custom AnimationCurve
.SetEase(customEaseFunction)   // Custom function
```

**Common Ease Types:**
- `Linear` — Constant speed
- `InQuad`, `OutQuad`, `InOutQuad` — Quadratic
- `InCubic`, `OutCubic`, `InOutCubic` — Cubic
- `InQuart`, `OutQuart`, `InOutQuart` — Quartic
- `InQuint`, `OutQuint`, `InOutQuint` — Quintic
- `InSine`, `OutSine`, `InOutSine` — Sinusoidal
- `InExpo`, `OutExpo`, `InOutExpo` — Exponential
- `InCirc`, `OutCirc`, `InOutCirc` — Circular
- `InBack`, `OutBack`, `InOutBack` — Overshoot
- `InElastic`, `OutElastic`, `InOutElastic` — Spring
- `InBounce`, `OutBounce`, `InOutBounce` — Bounce
- `Flash` — Flashing effect

### Behavior Settings

| Method | Description |
|--------|-------------|
| `SetAutoKill(bool)` | Kill automatically when complete (default: true) |
| `SetRelative(bool)` | Values are relative to start (additive) |
| `SetId(object)` | Assign an identifier for filtering |
| `SetTarget(object)` | Assign a target for filtering |
| `SetLink(GameObject)` | Link tween lifecycle to a GameObject |
| `SetRecyclable(bool)` | Reuse tween after kill instead of destroying |

### Update Type

```csharp
.SetUpdate(UpdateType.Normal, bool isIndependent)
```

| UpdateType | Description |
|------------|-------------|
| `Normal` | Update() |
| `Late` | LateUpdate() |
| `Fixed` | FixedUpdate() |
| `Manual` | Manual via DOTween.ManualUpdate() |

Set `isIndependent = true` to ignore `Time.timeScale` (useful for pause menus).

---

## Callbacks

```csharp
myTween
    .OnStart(StartFunction)
    .OnUpdate(UpdateFunction)
    .OnComplete(CompleteFunction)
    .OnKill(KillFunction)
    .OnPlay(PlayFunction)
    .OnPause(PauseFunction)
    .OnRewind(RewindFunction)
    .OnStepComplete(StepCompleteFunction);
```

| Callback | When It Fires |
|----------|---------------|
| `OnStart` | When tween begins playing for the first time |
| `OnUpdate` | Every frame while tween is active |
| `OnComplete` | When tween finishes (all loops complete) |
| `OnKill` | When tween is killed/destroyed |
| `OnPlay` | When tween starts or resumes playing |
| `OnPause` | When tween is paused |
| `OnRewind` | When tween is rewound |
| `OnStepComplete` | After each loop cycle completes |

---

## Controlling Tweens

### Instance Control

```csharp
myTween.Play();
myTween.Pause();
myTween.PlayBackwards();
myTween.PlayForward();
myTween.Restart();
myTween.Rewind();
myTween.Complete();
myTween.Kill();
myTween.Kill(true);    // Complete before killing
```

### Query State

```csharp
myTween.IsActive();
myTween.IsPlaying();
myTween.IsComplete();
myTween.Duration();
myTween.Elapsed();
```

### Static / Global Control

```csharp
DOTween.Kill("myId");                // Kill all tweens with ID
DOTween.Kill(myTransform);           // Kill all tweens on target
DOTween.KillAll();                   // Kill everything
DOTween.Complete();                  // Complete all
DOTween.Pause();                     // Pause all
DOTween.Play("myId");               // Play all with ID
DOTween.Restart("myId");            // Restart all with ID
DOTween.RewindAll();                 // Rewind all
```

### Shortcut Control (on target)

```csharp
transform.DOKill();                  // Kill tweens on this transform
transform.DOPause();                 // Pause tweens on this transform
transform.DOPlay();                  // Play tweens on this transform
transform.DORestart();               // Restart tweens on this transform
transform.DORewind();                // Rewind tweens on this transform
transform.DOComplete();              // Complete tweens on this transform
```

---

## Global Settings

```csharp
// Capacity
DOTween.SetTweensCapacity(2000, 100);   // Tweeners, Sequences

// Global time scale
DOTween.timeScale = 0.5f;
DOTween.unscaledTimeScale = 1f;

// Defaults for new tweens
DOTween.defaultEaseType = Ease.OutQuad;
DOTween.defaultLoopType = LoopType.Restart;
DOTween.defaultAutoKill = true;
DOTween.defaultAutoPlay = AutoPlay.All;
DOTween.defaultRecyclable = false;
DOTween.defaultTimeScaleIndependent = false;
DOTween.defaultUpdateType = UpdateType.Normal;

// Safety
DOTween.useSafeMode = true;             // Handle destroyed targets gracefully
DOTween.useSmoothDeltaTime = false;
DOTween.logBehaviour = LogBehaviour.ErrorsOnly;
```

---

## Path Tweening

Animate objects along multi-point paths:

```csharp
Vector3[] waypoints = {
    new Vector3(0, 0, 0),
    new Vector3(5, 5, 5),
    new Vector3(10, 0, 0)
};

transform.DOPath(waypoints, 3f, PathType.CatmullRom)
    .SetOptions(true)      // Snap to integers
    .SetLookAt(0.1f);      // Look forward along path
```

**Path Types:** `Linear`, `CatmullRom` (smooth curves), `CubicBezier`

**Note:** Path tweens do not support Back or Elastic eases.

---

## TextMesh Pro Animation

Per-character animation with DOTween Pro:

```csharp
DOTweenTMPAnimator animator = new DOTweenTMPAnimator(tmpText);

// Animate individual characters
animator.DOFadeChar(0, 1, 1f);
animator.DOColorChar(0, Color.red, 1f);
animator.DOScaleChar(0, 1.5f, 1f);
animator.DOOffsetChar(0, new Vector3(0, 10, 0), 1f);

// Animate all characters in sequence
Sequence seq = DOTween.Sequence();
for (int i = 0; i < animator.textInfo.characterCount; i++) {
    if (!animator.textInfo.characterInfo[i].isVisible) continue;
    seq.Join(animator.DOFadeChar(i, 1, 0.5f).SetDelay(i * 0.05f));
}
```

---

## Common Recipes

### Fade In UI Panel

```csharp
CanvasGroup panel;

void ShowPanel() {
    panel.alpha = 0;
    panel.gameObject.SetActive(true);
    panel.DOFade(1, 0.3f).SetEase(Ease.OutQuad);
}

void HidePanel() {
    panel.DOFade(0, 0.3f).SetEase(Ease.InQuad)
        .OnComplete(() => panel.gameObject.SetActive(false));
}
```

### Card Flip Animation

```csharp
Sequence flipSequence = DOTween.Sequence();
flipSequence.Append(transform.DOScaleX(0, 0.15f).SetEase(Ease.InQuad));
flipSequence.AppendCallback(() => {
    // Swap card face sprite here
    cardImage.sprite = isRevealed ? cardFrontSprite : cardBackSprite;
});
flipSequence.Append(transform.DOScaleX(1, 0.15f).SetEase(Ease.OutQuad));
```

### Screen Shake

```csharp
Camera.main.DOShakePosition(0.5f, 0.3f, 15, 90f)
    .SetUpdate(UpdateType.Normal, true);  // Ignore timeScale
```

### Button Press Feedback

```csharp
void OnButtonClicked() {
    transform.DOPunchScale(Vector3.one * 0.1f, 0.3f, 5, 0.5f);
}
```

### Floating/Bobbing Animation

```csharp
transform.DOMoveY(transform.position.y + 0.5f, 1f)
    .SetEase(Ease.InOutSine)
    .SetLoops(-1, LoopType.Yoyo);
```

### Delayed Sequence of Actions

```csharp
Sequence battleSequence = DOTween.Sequence();
battleSequence.Append(attacker.DOMove(targetPos, 0.3f).SetEase(Ease.OutQuad));
battleSequence.AppendCallback(() => PlayAttackEffect());
battleSequence.AppendInterval(0.2f);
battleSequence.Append(attacker.DOMove(originalPos, 0.3f).SetEase(Ease.InQuad));
battleSequence.AppendCallback(() => ShowDamageNumber());
```

---

## Performance Tips

1. **Set capacity** early: `DOTween.SetTweensCapacity(expectedTweeners, expectedSequences);`
2. **Enable recycling** for frequently created/destroyed tweens: `.SetRecyclable(true)` or `DOTween.Init(recycleAllByDefault: true)`.
3. **Use Safe Mode** in development, consider disabling in production for slight performance gain.
4. **Kill tweens** when objects are destroyed: call `transform.DOKill()` in `OnDestroy()`.
5. **Null tween references** in `OnKill()` callback when using recycling to avoid stale references.
6. Default capacity is 200 Tweeners and 50 Sequences — increase if you use more.
