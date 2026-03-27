# Unity URP 2D Renderer Setup & Configuration

> Source: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest
> Fetched: 2026-03-27

## Overview

The Universal Render Pipeline (URP) 2D Renderer is Unity's optimized rendering solution for 2D games. It provides a dedicated 2D lighting system, shadow casting, and normal map support while maintaining excellent performance.

## Initial Setup

### Step 1: Install URP
```
Window → Package Manager → Universal RP → Install
```

### Step 2: Create Pipeline Asset
```
Assets → Create → Rendering → URP Asset (with 2D Renderer)
```
This creates two assets:
- `URP-Asset.asset` (Pipeline settings)
- `URP-Asset_Renderer.asset` (2D Renderer Data)

### Step 3: Assign Pipeline
```
Edit → Project Settings → Graphics → Scriptable Render Pipeline Settings → [Assign URP Asset]
Edit → Project Settings → Quality → Rendering → [Assign URP Asset per quality level]
```

### Step 4: Verify Shaders
All sprites should use URP-compatible shaders:
- `Sprite-Lit-Default` (receives 2D lighting)
- `Sprite-Unlit-Default` (no lighting, flat rendering)

## 2D Light Types

### Global Light
- Illuminates everything in the scene
- Used for ambient/base lighting
- Properties: Color, Intensity, Blend Style
- Typical use: Day/night cycle base light

### Point Light
- Circular light radiating from a point
- Properties: Color, Intensity, Inner/Outer Radius, Falloff
- Typical use: Torches, magical glow, character aura

### Spot Light (Freeform)
- Directional cone of light
- Properties: Color, Intensity, Inner/Outer Angle, Falloff
- Typical use: Spotlights, focused beams

### Freeform Light
- Custom shape defined by editable spline
- Properties: Color, Intensity, Falloff Offset, Falloff Strength
- Typical use: Window light shapes, irregular areas

### Sprite Light
- Light shape defined by a sprite texture
- Properties: Color, Intensity, Sprite reference
- Typical use: Patterned light (stained glass, foliage shadows)

## Blend Styles

Define how lights combine with sprite colors:

| Blend Style | Operation | Use Case |
|------------|-----------|----------|
| Multiply | Light × Sprite | Realistic lighting, shadows |
| Additive | Light + Sprite | Glowing effects, fire |
| Custom | User-defined | Special effects |

Configure in: URP 2D Renderer Data → Light Blend Styles (up to 4)

## Shadow System

### Shadow Caster 2D
- Attach to GameObjects to cast shadows
- Properties: Cast Shadows (on/off), Self Shadows, Caster Group
- Use Composite Shadow Caster for complex shapes

### Shadow Settings
- In 2D Renderer Data: Shadow settings
- Shadow Intensity: 0 (no shadow) to 1 (full black)
- Shadow Volume Intensity: Controls shadow edge softness

## Normal Maps for 2D

Normal maps add depth to 2D sprites under dynamic lighting.

### Workflow:
1. Create normal map for sprite (e.g., in Sprite Illuminator, Laigter)
2. Import as Normal Map (Texture Type: Normal Map)
3. Assign to sprite's material Secondary Textures
4. Use `Sprite-Lit-Default` shader
5. 2D lights will now create depth effect on the sprite

### Sprite Editor → Secondary Textures
```
Name: _NormalMap
Texture: [your normal map texture]
```

## Layer & Sorting Configuration

### Target Sorting Layers for 2D Card Game
```
Layer 0: Background_Far       (sky, distant landscape)
Layer 1: Background_Mid       (buildings, mountains)
Layer 2: Background_Near      (foreground objects)
Layer 3: Battlefield          (combat area)
Layer 4: Characters_Back      (back row enemies)
Layer 5: Characters_Front     (front row, player party)
Layer 6: Cards                (card hand, played cards)
Layer 7: Effects              (VFX, particles)
Layer 8: UI_World             (health bars, damage numbers)
Layer 9: UI_Overlay           (HUD, menus)
```

### Light Target Sorting Layers
Each 2D Light can target specific sorting layers:
- Ambient light → All layers
- Torch light → Characters + Battlefield only
- UI light → UI layers only (or none, keep UI unlit)

## Camera Setup

### Cinemachine 2D
```
1. Add CinemachineVirtualCamera to scene
2. Set Body: Framing Transposer
3. Set Lens: Orthographic
4. Set Follow target: Player/Battle area
5. Configure Dead Zone, Soft Zone for camera movement
```

### Pixel Perfect Camera (Optional)
```
Add PixelPerfectCamera component for pixel art:
- Assets PPU: Match sprite PPU (e.g., 100)
- Reference Resolution: Target resolution (e.g., 1920x1080)
- Upscale Render Texture: On (for crisp scaling)
```

## Performance Optimization

| Setting | Recommendation | Impact |
|---------|---------------|--------|
| Light count | < 20 per scene | Draw calls |
| Shadow casters | Minimize | GPU cost |
| Blend styles | Use ≤ 2 | Render passes |
| Normal maps | Only for key sprites | Texture memory |
| Sprite Atlas | Pack per sorting layer | Batching |

## Scripting Examples

### Dynamic Light Control (C#)
```csharp
using UnityEngine.Rendering.Universal;

public class DynamicLight : MonoBehaviour
{
    Light2D light2D;

    void Start()
    {
        light2D = GetComponent<Light2D>();
    }

    // Flickering torch effect
    void Update()
    {
        light2D.intensity = 0.8f + Mathf.PerlinNoise(Time.time * 3f, 0) * 0.4f;
    }

    // Fate system visual: shift light color based on balance
    public void SetFateLight(float fateValue)
    {
        // fateValue: -3 (resistance) to +3 (compliance)
        float t = Mathf.InverseLerp(-3f, 3f, fateValue);
        light2D.color = Color.Lerp(Color.red, Color.blue, t);
    }
}
```
