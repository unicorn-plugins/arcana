# Unity URP 2D Lighting Documentation

> Source: https://docs.unity3d.com/6000.0/Documentation/Manual/urp/Lights-2D-intro.html , https://gamedevacademy.org/unity-universal-render-pipeline-tutorial/
> Fetched: 2026-03-27

## Overview

The 2D lighting system in Unity's Universal Render Pipeline (URP) provides specialized tools for creating lit 2D scenes. These tools are designed to integrate seamlessly with 2D Renderers such as the Sprite Renderer, Tilemap Renderer, and Sprite Shape Renderer. The system emphasizes optimization for mobile platforms and multi-platform deployment.

---

## Key Differences from 3D Lights

### Dedicated 2D Components

The 2D lighting framework includes its own set of light components, Shader Graph sub-targets, and custom render passes distinct from 3D lighting systems.

### Coplanar Design

Unlike 3D lights, the 2D model was designed specifically to work with 2D worlds that are coplanar and multi-layered, eliminating the need for depth separation between lights and lit objects.

### Non-Physical Rendering

The lighting calculations are not physics-based, differing fundamentally from 3D light implementations. This allows for more artistic control over how light interacts with sprites.

### No Cross-Compatibility

3D and 2D Lights can only affect 3D and 2D Renderers respectively. Combining both systems requires multiple cameras and render textures.

---

## Graphics Pipeline Architecture

The rendering process occurs in two main phases:

**Phase 1: Light Render Texture Generation**
The system draws light shapes onto render textures in screen space, with colors blended additively or via alpha blending based on light configuration.

**Phase 2: Renderer Drawing**
Renderers access the generated light render textures and combine them with sprite colors using specified blend operations.

**Performance Optimization:**
The pipeline includes a pre-phase that batches consecutive sorting layers sharing identical light sets, minimizing render texture operations and improving overall performance.

---

## Project Setup

### Step 1: Install Universal Render Pipeline

**For New Projects:**

1. Open Unity Hub and select "Create > New Unity project"
2. Choose the "Universal RP Template" option

**For Existing Projects:**

1. Navigate to Window > Package Manager
2. Search for "Universal RP" and ensure it is installed and current

### Step 2: Create URP Pipeline Asset

1. Right-click in the Project window
2. Select **Create > Rendering > Universal Render Pipeline > Pipeline Asset**

This automatically generates two files:

- `UniversalRenderPipelineAsset.asset` (main configuration)
- `UniversalRenderPipelineAsset_Renderer.asset` (will be replaced with 2D renderer)

### Step 3: Assign URP in Graphics Settings

1. Go to **Edit > Project Settings > Graphics**
2. Locate "Scriptable Render Pipeline Settings"
3. Drag the `UniversalRenderPipelineAsset` into this field

**Troubleshooting:** If objects appear pink, materials need conversion. Use **Edit > Render Pipeline > Universal Render Pipeline > Upgrade Project Materials to UniversalRP Materials**.

### Step 4: Configure 2D Renderer

1. Right-click in Project folder
2. Select **Create > Rendering > Universal Render Pipeline > 2D Renderer Data**
3. Click your `UniversalRenderPipelineAsset`
4. In the Inspector, drag the 2D Renderer Data into the Renderer List
5. Set it as "Default"

---

## Preparing Sprites for 2D Lighting

The setup workflow involves six key steps:

1. **Sprite Preparation** -- Configure sprites to work with the 2D lighting system by assigning Sprite-Lit-Default or custom lit materials.
2. **Normal Maps and Mask Textures** -- 2D Lights can interact with normal map and mask textures linked to sprites to create advanced lighting effects.
3. **2D Light GameObject Creation** -- Create Light GameObjects within the scene hierarchy.
4. **2D Renderer Data Configuration** -- The 2D Renderer Asset requires specific configuration to support lighting features.
5. **Shadow Caster 2D Component** -- Defines the shape and properties that a light uses to determine the shadows it casts.
6. **Pixel Perfect Camera (Optional)** -- For pixel art games, provides precise scaling and rotation capabilities.

---

## Light Types

Create 2D lights via **GameObject > Light > 2D** or by adding the Light 2D component to any GameObject.

### Global Light

Provides uniform illumination across the entire scene, similar to sunlight. Only one global light can be used per blend style and per sorting layer.

**Use Cases:**

- Base scene brightness
- Day/night cycle systems
- Ambient lighting for entire levels

### Point Light

Emits light in all directions from a single point with configurable inner and outer radius.

**Properties:**

- **Radius Inner** -- Maximum intensity radius
- **Radius Outer** -- Falloff boundary where intensity reaches zero

**Use Cases:**

- Torches, lanterns, campfires
- Magical orbs and spell effects
- Localized environmental lighting

### Spot Light

Directional light with a cone shape, providing angular control over illumination.

**Properties:**

- **Radius Inner / Radius Outer** -- Control falloff distance
- **Inner / Outer Spot Angle** -- Define angular light spread

**Use Cases:**

- Flashlights and focused beams
- Spotlights in performance halls
- Directional magical effects

### Freeform Light

Uses an editable polygon with a spline editor for custom light shapes. Add control points by clicking along the polygon outline; remove them via the Delete key.

**Properties:**

- **Falloff** -- Adjusts the light's falloff area extent
- **Falloff Strength** -- Controls edge softness of the light effect

**Warning:** Avoid self-intersecting outlines as they cause unintended lighting artifacts.

**Use Cases:**

- Window light projections
- Irregular shaped light sources
- Custom atmospheric effects

### Sprite Light

Creates a light based on a selected sprite texture, allowing for highly stylized lighting shapes.

**Properties:**

- **Sprite** -- Assign a sprite image as the light source

**Use Cases:**

- Patterned light through stained glass
- Complex decorative lighting
- Cookie-cutter light effects

**Note:** Parametric lights are deprecated from URP 11 onward; use the Render Pipeline Converter to upgrade existing assets.

---

## Common Light Properties

All Light 2D types share these properties:

| Property | Description |
|----------|-------------|
| **Light Type** | Freeform, Sprite, Spot, or Global |
| **Color** | Color of the emitted light (via color picker) |
| **Intensity** | Brightness level (default: 1) |
| **Target Sorting Layers** | Which sorting layers the light affects |
| **Blend Style** | How the light blends with sprites (customizable in 2D Renderer Asset) |
| **Light Order** | Rendering sequence relative to other lights (supports negative values; unavailable for Global) |
| **Overlap Operation** | Additive or Alpha Blend overlap modes |
| **Shadow Strength** | How much light Shadow Caster 2Ds block (0-1 range) |
| **Volumetric Intensity** | Volumetric lighting opacity (0-1 range) |
| **Volumetric Shadow Strength** | Volumetric light blockage by Shadow Caster 2Ds (0-1 range) |
| **Normal Map Quality** | Disabled, Accurate, or Fast for lighting calculation precision |
| **Normal Map Distance** | Distance in Unity units between light and sprite (when enabled) |

---

## Blend Styles

URP 2D supports multiple blend modes for controlling how light interacts with sprites:

- **Additive** -- Light adds to scene brightness. Good for bright, warm light sources.
- **Multiply** -- Darkens based on light presence. Useful for shadow effects.
- **Screen** -- Mimics film photography light behavior.
- **Overlay** -- Combines additive and multiply effects for rich results.

Blend styles are configured in the 2D Renderer Data asset. Select the blend style in the Light 2D component inspector for each individual light.

---

## Shadow System

### Shadow Caster 2D Component

To enable shadows, sprites must have the Shadow Caster 2D component:

1. Select a sprite GameObject
2. Add Component > Search "Shadow Caster 2D"
3. Configure shadow properties in the component

The Shadow Caster 2D defines the shape and properties that a light uses to determine the shadows it casts. Only essential sprites should have this component for performance.

### Shadow Properties

- **Shadow Strength** -- Controls how dark shadows appear (0 = transparent, 1 = fully opaque)
- **Casts Shadows** -- Enable or disable shadow casting per object
- **Self Shadows** -- Whether the object casts shadows on itself

---

## Normal Maps Integration

Normal maps add surface detail that reacts to 2D lighting without additional geometry:

1. Import a normal map texture
2. In the sprite's material, assign the normal map to the appropriate slot
3. 2D lights will respond to surface detail information
4. Adjust Normal Map Quality to Accurate or Fast in light properties
5. Set Normal Map Distance to control perceived depth

**Use Cases:**

- Stone wall textures with visible depth
- Metallic surfaces with reflective properties
- Organic textures like bark, scales, or fabric folds

---

## C# Scripting Examples

### Adjusting Light Intensity at Runtime

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class LightController : MonoBehaviour
{
    private Light2D light2D;

    void Start()
    {
        light2D = GetComponent<Light2D>();
    }

    public void SetIntensity(float newIntensity)
    {
        light2D.intensity = newIntensity;
    }

    public void SetLightColor(Color newColor)
    {
        light2D.color = newColor;
    }
}
```

### Creating a Flickering Torch Effect

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class FlickeringLight : MonoBehaviour
{
    private Light2D light2D;
    public float minIntensity = 0.7f;
    public float maxIntensity = 1.2f;
    public float flickerSpeed = 5f;

    void Start()
    {
        light2D = GetComponent<Light2D>();
    }

    void Update()
    {
        light2D.intensity = Mathf.Lerp(
            minIntensity,
            maxIntensity,
            Mathf.PerlinNoise(Time.time * flickerSpeed, 0f)
        );
    }
}
```

### Dynamic Day/Night Cycle

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class DayNightCycle : MonoBehaviour
{
    private Light2D globalLight;
    public float cycleDuration = 120f; // seconds for full cycle
    public Color dayColor = Color.white;
    public Color nightColor = new Color(0.1f, 0.1f, 0.3f);
    public float dayIntensity = 1.0f;
    public float nightIntensity = 0.2f;
    public AnimationCurve intensityCurve;

    void Start()
    {
        globalLight = GetComponent<Light2D>();
    }

    void Update()
    {
        float timeInCycle = Mathf.Repeat(Time.time, cycleDuration) / cycleDuration;
        globalLight.intensity = intensityCurve.Evaluate(timeInCycle);
        globalLight.color = Color.Lerp(nightColor, dayColor, intensityCurve.Evaluate(timeInCycle));
    }
}
```

---

## Performance Optimization Tips

### General Recommendations

1. **Limit active lights** -- Each light impacts performance; disable distant or off-screen lights.
2. **Use global lights for base illumination** -- More efficient than multiple point lights.
3. **Optimize shadow casters** -- Only essential sprites need Shadow Caster 2D.
4. **Batch similar light types** -- URP handles uniform light types more efficiently.
5. **Test on target devices** -- Mobile platforms benefit greatly from optimization.
6. **Profile regularly** -- Use Frame Debugger (Window > Frame Debugger) to identify bottlenecks.

### Sorting Layer Optimization

The 2D lighting pipeline batches consecutive sorting layers sharing identical light sets. Organize sorting layers so that layers lit by the same lights are adjacent to minimize render texture operations.

### Light Count Guidelines

| Platform | Recommended Max Lights per Scene |
|----------|----------------------------------|
| Mobile | 4-8 active lights |
| Desktop | 16-32 active lights |
| Console | 16-32 active lights |

These are guidelines -- actual limits depend on light complexity, shadow casters, and target framerate.

---

## Common Issues and Solutions

### Scene Appears Completely Dark

- Verify 2D Renderer Data is assigned to URP asset
- Check that at least one 2D light exists in the scene (typically a Global light)
- Ensure sprites have lit materials (Sprite-Lit-Default)

### Lights Do Not Affect Sprites

- Ensure sprites have the appropriate material supporting 2D lights
- Verify Light 2D component is actually added to the GameObject
- Check Target Sorting Layers include the layer the sprite is on

### Performance Degradation

- Reduce number of active lights
- Increase light range conservatively rather than using many small lights
- Reduce shadow caster count
- Profile using Frame Debugger (Window > Frame Debugger)

### Pink/Magenta Materials

- Materials need conversion to URP-compatible shaders
- Use **Edit > Render Pipeline > Universal Render Pipeline > Upgrade Project Materials**

---

## Recommended Workflow for 2D Game Lighting

1. **Start with a Global Light** at low intensity (0.3-0.5) to establish ambient brightness
2. **Place primary light sources** (Point lights for torches, Freeform for windows)
3. **Adjust colors** to match the scene's mood and time of day
4. **Add Shadow Caster 2D** to key objects that should cast shadows
5. **Assign normal maps** to sprites that benefit from surface detail
6. **Configure blend styles** in the 2D Renderer Data for desired look
7. **Test and iterate** -- adjust intensities, colors, and positions
8. **Optimize** -- remove unnecessary lights and shadow casters
9. **Profile on target platform** to ensure performance targets are met
