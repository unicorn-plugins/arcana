# Unity URP Post-Processing Effects

> Source: https://docs.unity3d.com/6000.3/Documentation/Manual/urp/integration-with-post-processing.html
> Fetched: 2026-03-27

## Overview

The Universal Render Pipeline (URP) includes an integrated post-processing implementation that uses the **Volume framework** to manage effects. This is distinct from the Post Processing Stack v2 package, which is incompatible with URP.

Post-processing improves product visuals by applying filters and effects before the image appears on screen. URP provides both a variety of ready-to-use post-processing effects and methods for custom effect creation.

**Important:** URP does not support post-processing on OpenGL ES 2.0.

---

## Setting Up Post-Processing

New scenes in URP do not use post-processing by default. You must manually add post-processing to each new scene.

### Step-by-Step Setup

#### Step 1: Enable Post-Processing on Camera
1. Select your Camera in the scene hierarchy
2. In the Camera Inspector, find the **Rendering** section
3. Enable the **Post Processing** checkbox

#### Step 2: Add a Volume GameObject
1. Go to `GameObject > Volume > Global Volume`
2. This creates a new GameObject with a Volume component attached

#### Step 3: Create a Volume Profile
1. Select the Volume GameObject
2. In the Inspector, locate the Volume component
3. Click **New** to create a fresh Volume Profile asset

#### Step 4: Add Volume Overrides
1. In the Volume component, click **Add Override**
2. Select your desired post-processing effect (e.g., Bloom)
3. Enable and adjust individual settings within the override

#### Step 5: Verify Volume Mask
- Post-processing effects from a Volume apply to a Camera only if the **Volume Mask** property on the Camera contains the layer the Volume belongs to
- Default layer is usually sufficient, but verify if effects are not appearing

---

## Volume Framework

### What is a Volume?

A Volume is a component that defines a region of space where post-processing effects are applied. Volumes use **Volume Profiles** containing one or more **Volume Overrides** to define which effects to apply and their settings.

### Volume Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Global Volume** | Affects the entire scene regardless of camera position | Default post-processing, global color grading |
| **Local Volume** (Box/Sphere) | Affects only cameras within its bounds | Area-specific effects (underwater, fog zones, danger areas) |

### Volume Blending

When a camera is affected by multiple Volumes, URP blends their settings based on:
- **Weight** — The influence of the Volume (0 to 1)
- **Priority** — Higher priority Volumes override lower ones
- **Blend Distance** — How gradually effects transition at Volume boundaries (Local Volumes only)

### Volume Profile

A Volume Profile is a ScriptableObject asset that stores a collection of Volume Overrides. Profiles can be:
- Shared across multiple Volumes
- Swapped at runtime via script
- Created as project assets for reuse

---

## Post-Processing Effects Reference

### Bloom

Creates fringes of light extending from the borders of bright areas in an image, simulating the effect of extremely bright light overwhelming the camera sensor.

#### Properties

| Property | Description | Default |
|----------|-------------|---------|
| **Threshold** | Gamma-space brightness cutoff; only pixels exceeding this value receive bloom | 0.9 |
| **Intensity** | Bloom filter strength (0 disables the effect) | 0 |
| **Scatter** | Bloom radius control (0-1); higher values expand the effect | 0.7 |
| **Tint** | Color applied to the bloom effect | White |
| **Clamp** | Maximum intensity value for bloom calculations | 65472 |
| **High Quality Filtering** | Bilinear sampling for smoother results; increases GPU cost | Off |
| **Downscale** | Initial resolution scale; "Quarter" recommended for performance | Half |
| **Max Iterations** | Maximum processing iterations; reduce for mobile | 6 |

#### Lens Dirt (Sub-feature)

| Property | Description |
|----------|-------------|
| **Texture** | Texture asset simulating lens contamination |
| **Intensity** | Strength of the dirt overlay |

#### Bloom Performance Tips
- Set Downscale to "Quarter" for significant resource reduction
- Disable High Quality Filtering on mobile/lower-end hardware
- Reduce Max Iterations on high-DPI mobile screens
- Use lower-resolution Lens Dirt textures to reduce memory

#### VFX Artist Usage
- Combine with HDR emission on particle materials for glowing effects
- Use bloom to enhance flash effects and explosions
- Set emissive values above 1.0 on materials to trigger bloom
- Pair with additive particle blending for maximum glow

---

### Vignette

Darkens and/or desaturates the edges of the image compared to the center. Replicates a natural photographic effect caused by thick filters, stacked lenses, or improper lens hoods.

#### Properties

| Property | Description | Default |
|----------|-------------|---------|
| **Color** | Color of the vignette effect | Black |
| **Center** | Center point of the vignette; screen center is [0.5, 0.5] | [0.5, 0.5] |
| **Intensity** | Strength of the vignette effect | 0 |
| **Smoothness** | Softness of vignette edges (0.01-1); higher = smoother | 0.2 |
| **Rounded** | When enabled, perfectly circular; when disabled, follows aspect ratio | Off |

#### VFX Artist Usage
- Pulse vignette intensity on damage taken
- Use colored vignette (red) for low health warning
- Animate vignette intensity for dramatic moments
- Combine with color shift for environmental mood (underwater = blue tint)

---

### Color Grading

Alters or corrects the color and luminance of the final rendered image. URP supports multiple color grading modes.

#### Tonemapping Modes

| Mode | Description |
|------|-------------|
| **None** | No tonemapping applied |
| **Neutral** | Range-remapping with minimal effect on hue and saturation |
| **ACES** | Industry-standard filmic tonemapping; close to cinematic look |

#### Color Adjustments

| Property | Description |
|----------|-------------|
| **Post Exposure** | Overall exposure adjustment in EV units |
| **Contrast** | Expands or compresses the tonal range |
| **Color Filter** | Tints the entire image |
| **Hue Shift** | Shifts all colors along the hue spectrum |
| **Saturation** | Intensity of colors (-100 = grayscale, 100 = double saturation) |

#### White Balance

| Property | Description |
|----------|-------------|
| **Temperature** | Warm (yellow) to cool (blue) shift |
| **Tint** | Green to magenta shift |

#### Channel Mixer
Adjusts the influence of each input color channel (Red, Green, Blue) on the output channels. Useful for creative color effects.

#### Lift, Gamma, Gain
Three-way color correction for shadows (Lift), midtones (Gamma), and highlights (Gain).

#### Shadows, Midtones, Highlights
Similar to Lift/Gamma/Gain but with adjustable range boundaries for more precise control.

#### Split Toning
Applies different color tints to shadows and highlights with a balance slider.

#### VFX Artist Usage
- Shift saturation briefly on hit for dramatic feedback
- Use post-exposure to create flash-to-dark transitions
- Apply color filter for environmental storytelling (warm = safe, cool = danger)
- Desaturate briefly on death or heavy damage

---

### Chromatic Aberration

Simulates the effect of lens imperfections that cause color channels to separate, creating colored fringes at the edges of objects.

#### Properties

| Property | Description | Default |
|----------|-------------|---------|
| **Intensity** | Strength of the chromatic fringing effect | 0 |
| **Spectral Lut** | Optional texture for custom fringe color pattern | None |

#### VFX Artist Usage
- Spike intensity briefly (0.05-0.2s) on heavy impacts
- Use as a subtle constant effect for a "damaged camera" look
- Layer with screen shake for jarring hit feedback
- Animate from 0 to high and back for teleportation/warp effects

---

### Depth of Field

Simulates the focus behavior of a real camera lens, blurring objects at different distances from the focal point.

#### Gaussian Mode (Mobile-Friendly)

| Property | Description |
|----------|-------------|
| **Start** | Distance where blur begins |
| **End** | Distance where blur reaches maximum |

#### Bokeh Mode (Desktop/Console)

| Property | Description |
|----------|-------------|
| **Focus Distance** | Distance to the sharp focus plane |
| **Focal Length** | Camera lens focal length in mm |
| **Aperture** | F-stop value; lower = more blur |
| **Blade Count** | Number of aperture blades (bokeh shape) |

#### VFX Artist Usage
- Use for cinematic focus during cutscenes or finishing moves
- Blur background during menu/pause overlays
- Create tilt-shift miniature effects
- Animate focus distance for dramatic rack-focus transitions

---

### Film Grain

Overlays a film grain texture to simulate photographic noise, adding a cinematic quality to the image.

#### Properties

| Property | Description |
|----------|-------------|
| **Type** | Thin or Medium grain pattern |
| **Intensity** | Visibility of the grain effect |
| **Response** | How grain reacts to scene brightness |

#### VFX Artist Usage
- Add subtle grain for cinematic or horror atmosphere
- Increase grain during flashback or memory sequences
- Layer with desaturation for old-film effects

---

### Lens Distortion

Simulates the barrel or pincushion distortion of a real camera lens.

#### Properties

| Property | Description |
|----------|-------------|
| **Intensity** | Strength and direction of distortion (-1 to 1) |
| **X Multiplier** | Distortion intensity on horizontal axis |
| **Y Multiplier** | Distortion intensity on vertical axis |
| **Center** | Center point of the distortion |
| **Scale** | Global screen scaling to hide distortion artifacts at edges |

#### VFX Artist Usage
- Brief pulse on heavy impacts (fish-eye punch)
- Subtle constant distortion for underwater or dream sequences
- Animate for warp/portal entrance effects
- Combine with chromatic aberration for disorientation

---

### Motion Blur

Blurs the image in the direction of camera movement, simulating the blur captured by a real camera during exposure.

#### Properties

| Property | Description |
|----------|-------------|
| **Quality** | Low, Medium, or High |
| **Intensity** | Strength of the blur (0-1) |
| **Clamp** | Maximum length of blur streaks (0-0.2) |

#### VFX Artist Usage
- Enable during high-speed movement (dash, boost)
- Increase intensity during speed-up abilities
- Disable during precision gameplay (aiming, platforming)

**Warning:** Motion blur can cause nausea; always provide a toggle option.

---

### Panini Projection

Reduces perspective distortion at the edges of the screen, particularly useful at wide FOV settings.

#### Properties

| Property | Description |
|----------|-------------|
| **Distance** | Strength of the Panini projection (0-1) |
| **Crop to Fit** | Crops the image to remove empty areas caused by projection |

---

## Mobile Optimization Guide

### Recommended Effects for Mobile

These effects are efficient on mobile hardware:
- **Bloom** (with High Quality Filtering disabled)
- **Chromatic Aberration**
- **Color Grading**
- **Lens Distortion**
- **Vignette**

### Moderate Cost Effects
- **Depth of Field** (Gaussian mode only on mobile)
- **Film Grain**

### Expensive Effects (Desktop/Console Only)
- **Depth of Field** (Bokeh mode)
- **Motion Blur**

### Mobile Performance Tips

1. Keep active Volume Overrides to a minimum
2. Prefer Gaussian DoF over Bokeh on mobile
3. Disable High Quality Filtering on Bloom
4. Set Bloom Downscale to "Quarter"
5. Reduce Bloom Max Iterations
6. Avoid Motion Blur on mobile
7. Use lower-resolution Lens Dirt textures

---

## VR Considerations

Certain post-processing effects can cause nausea and disorientation in VR:

| Effect | VR Recommendation |
|--------|-------------------|
| **Vignette** | Recommended (reduces motion sickness) |
| **Color Grading** | Safe to use |
| **Bloom** | Safe with moderate settings |
| **Chromatic Aberration** | Avoid (causes discomfort) |
| **Lens Distortion** | Avoid (conflicts with HMD optics) |
| **Motion Blur** | Avoid (causes nausea) |
| **Depth of Field** | Use cautiously |
| **Film Grain** | Use cautiously |

---

## Scripting Post-Processing at Runtime

### Accessing Volume Overrides via Script

```
// Common pattern for runtime post-processing control
// 1. Get reference to the Volume component
// 2. Access the Volume Profile
// 3. Get the specific Override (e.g., Bloom, Vignette)
// 4. Modify properties and set .overrideState = true

// Example use cases for VFX:
// - Spike chromatic aberration on damage
// - Pulse vignette on hit
// - Flash bloom intensity on explosions
// - Desaturate on death
// - Animate DOF focus for cutscenes
```

### Common Runtime Patterns

1. **Damage Feedback:** Spike vignette intensity + chromatic aberration, ease back to normal over 0.2s
2. **Explosion Flash:** Spike bloom intensity + post-exposure, ease back over 0.1s
3. **Death Sequence:** Animate saturation to -100, increase vignette, reduce post-exposure
4. **Speed Boost:** Increase motion blur intensity, widen bloom scatter
5. **Underwater Transition:** Shift color filter to blue-green, add chromatic aberration, increase vignette

---

## Custom Post-Processing Effects

URP supports creating custom full-screen post-processing effects through:

1. **Custom Renderer Features** — Add custom render passes to the URP rendering pipeline
2. **Full-Screen Shader Graph** — Create full-screen effects using Shader Graph with the Fullscreen target
3. **Scriptable Render Passes** — Write custom C# render passes for maximum control

### When to Use Custom Effects
- Outline / edge detection
- Pixelation
- Custom blur patterns (radial, directional)
- Scanlines or CRT effects
- Color palette restriction
- Custom distortion patterns
- Toon/cel-shading post-process
