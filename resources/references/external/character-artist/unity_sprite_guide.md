# Unity Sprite Technical Guide

> Source: https://docs.unity3d.com/Manual/Sprites.html
> Fetched: 2026-03-27

## Overview

Sprites are the fundamental 2D asset type in Unity. They are 2D graphic objects used for characters, props, projectiles, UI elements, and other visual components in 2D games. While similar to standard textures, sprites employ specialized import and management techniques optimized for 2D game development efficiency.

This guide covers sprite creation, import settings, the Sprite Editor, Sprite Sheets, Pivot Points, Pixels Per Unit (PPU), Sprite Atlas, Sprite Renderer, and best practices for game projects.

---

## 1. Prerequisites

The **2D Sprite package** must be installed to access sprite features in Unity. This package is included automatically when creating a project with the 2D template. For other project types, install it manually through the Unity Package Manager:

1. Open **Window > Package Manager**
2. Search for "2D Sprite"
3. Click **Install**

---

## 2. Sprite Import Settings

When importing an image file (PNG, PSD, TIFF, JPG, BMP, TGA, EXR) as a sprite, configure these settings in the **Texture Import Inspector**.

### Texture Type

Set **Texture Type** to `Sprite (2D and UI)` in the Import Settings panel. This tells Unity to treat the image as a 2D sprite rather than a 3D texture.

### Sprite Mode

| Mode | Description | Use Case |
|------|-------------|----------|
| **Single** | The entire texture is treated as one sprite | Individual character frames, icons, single props |
| **Multiple** | The texture contains multiple sprites that need to be sliced | Sprite sheets, tilesets, animation strip sheets |
| **Polygon** | The sprite shape is defined by a custom polygon outline | Irregular shapes requiring precise collision or rendering bounds |

### Pixels Per Unit (PPU)

**Pixels Per Unit** defines how many pixels in the sprite image correspond to one unit in Unity's world space.

| PPU Value | Effect | Common Use Case |
|-----------|--------|----------------|
| **1** | 1 pixel = 1 world unit | Rarely used; objects would be enormous |
| **16** | 16 pixels = 1 world unit | Low-resolution pixel art (16x16 tiles) |
| **32** | 32 pixels = 1 world unit | Standard pixel art (32x32 tiles) |
| **64** | 64 pixels = 1 world unit | Medium-resolution pixel art |
| **100** | 100 pixels = 1 world unit (Unity default) | HD/vector-style art, UI elements |
| **128** | 128 pixels = 1 world unit | High-resolution 2D art |

**Key considerations:**
- PPU should be consistent across all sprites in a project for uniform scaling
- For tile-based games: set PPU equal to the tile size in pixels (e.g., 32 PPU for 32x32 tiles)
- For character sprites: set PPU so that the character appears at the correct relative scale to the environment
- PPU affects physics calculations -- inconsistent PPU values cause collision mismatches
- Changing PPU after placing sprites in scenes requires repositioning all affected objects

### Pivot Point

The **Pivot** is the point around which the sprite rotates and the position used for placement in the scene. Unity provides preset pivot positions and allows custom coordinates.

| Preset | Position | Common Use |
|--------|----------|-----------|
| **Center** | (0.5, 0.5) | Default; symmetric objects, projectiles, effects |
| **Top Left** | (0, 1) | UI elements, tilemap origins |
| **Top** | (0.5, 1) | Top-aligned elements |
| **Top Right** | (1, 1) | UI corner elements |
| **Left** | (0, 0.5) | Left-aligned elements |
| **Right** | (1, 0.5) | Right-aligned elements |
| **Bottom Left** | (0, 0) | Tilemap tiles, grid-aligned objects |
| **Bottom** | (0.5, 0) | Characters (feet placement), props on ground |
| **Bottom Right** | (1, 0) | Right-aligned ground objects |
| **Custom** | (x, y) | Any specific point; values from 0 to 1 representing normalized position |

**Key considerations:**
- For **character sprites**: set pivot to **Bottom** (0.5, 0) so the character's feet align with the ground position
- For **tilemap tiles**: set pivot to match the tilemap grid origin (typically Bottom Left or Center)
- For **rotating objects** (wheels, dials): set pivot to **Center**
- For **weapons/tools**: set pivot at the grip/handle point
- Pivot affects rotation behavior, physics anchor, and scene placement coordinates

### Mesh Type

| Type | Description | Performance |
|------|-------------|-------------|
| **Full Rect** | Uses a simple rectangular quad for the sprite mesh | Fastest rendering; wastes fill rate on transparent pixels |
| **Tight** | Generates a mesh that closely follows the sprite's opaque pixels | Reduces overdraw; slightly more vertices; better for sprites with large transparent areas |

**Recommendation**: Use **Tight** for most game sprites to reduce overdraw. Use **Full Rect** for small sprites or sprites that are nearly rectangular.

### Other Import Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Extrude Edges** | Number of pixels to extend the sprite's edge outward to prevent seam artifacts in atlases | 1 |
| **Generate Physics Shape** | Automatically generates a physics collision shape from the sprite outline | Enabled |
| **Wrap Mode** | How the texture behaves when tiled (Repeat, Clamp, Mirror, etc.) | Clamp |
| **Filter Mode** | Texture sampling method (Point, Bilinear, Trilinear) | Bilinear |
| **Max Size** | Maximum texture dimension in pixels (32 to 16384) | 2048 |
| **Compression** | Texture compression format (None, Low Quality, Normal Quality, High Quality) | Normal |
| **sRGB (Color Texture)** | Enable for color textures; disable for data textures (normal maps) | Enabled |

**Filter Mode for Pixel Art:**
- Use **Point (no filter)** for pixel art to maintain crisp, sharp pixels without blurring
- Use **Bilinear** for HD or vector-style art for smooth scaling

---

## 3. Sprite Editor

The Sprite Editor is Unity's built-in tool for editing sprite boundaries, pivots, and outlines within a texture. Open it by clicking **Sprite Editor** in the Texture Import Inspector.

### Core Functions

The Sprite Editor enables developers to:
- Create sprites from a texture
- Edit the meshes Unity uses to render the sprite and detect collisions
- Rig a sprite for skeletal animation

### Sprite Editor Tabs

| Tab | Function |
|-----|----------|
| **Sprite Editor** | Configure sprite properties, define sprite boundaries, set individual pivots; convert textures into multiple sprites via slicing |
| **Custom Outline** | Edit the mesh shape used to render the sprite; reduce overdraw by tightening the mesh to opaque pixels |
| **Custom Physics Shape** | Configure the collision mesh shape for 2D Colliders; optimize physics by matching collision to visible shape |
| **Secondary Textures** | Add supplementary textures (normal maps, mask maps) for enhanced visual effects like lighting |

### Slicing Sprites (Multiple Mode)

When **Sprite Mode** is set to **Multiple**, the Sprite Editor provides slicing tools to divide a sprite sheet into individual sprites:

#### Automatic Slicing

Unity detects individual sprites in the sheet based on transparency:
1. Open Sprite Editor
2. Click **Slice** dropdown
3. Set **Type** to **Automatic**
4. Set **Pivot** for all sliced sprites
5. Click **Slice**
6. Click **Apply**

#### Grid by Cell Size

For uniformly-spaced sprite sheets:
1. Set **Type** to **Grid By Cell Size**
2. Enter pixel dimensions of each cell (e.g., 32x32, 64x64)
3. Set **Offset** if the grid doesn't start at (0,0)
4. Set **Padding** if there's space between cells
5. Click **Slice**

#### Grid by Cell Count

For sheets where you know the number of rows and columns:
1. Set **Type** to **Grid By Cell Count**
2. Enter the number of **Columns** and **Rows**
3. Click **Slice**

### Editing Individual Sprites

After slicing, select any sprite in the editor to modify:
- **Name**: Rename the sprite (affects access in code and animation)
- **Position**: X, Y pixel position of the sprite's top-left corner in the texture
- **Size**: Width and Height in pixels
- **Pivot**: Individual pivot point (overrides the global setting)
- **Border**: Left, Right, Top, Bottom border values for 9-slice scaling

---

## 4. Sprite Sheets

A sprite sheet is a single texture containing multiple sprites arranged in a grid or packed layout. Sprite sheets are essential for 2D game development.

### Types of Sprite Sheets

| Type | Description | Use Case |
|------|-------------|----------|
| **Animation Strip** | Single row of animation frames | Walk cycles, attack animations |
| **Grid Sheet** | Regular grid of equal-sized cells | Tilesets, character animation sets |
| **Packed Sheet** | Irregularly arranged sprites optimized for space | Atlas-style asset management |

### Sprite Sheet Best Practices

1. **Power-of-two dimensions**: Use texture sizes that are powers of 2 (256x256, 512x512, 1024x1024, 2048x2048) for optimal GPU memory usage and compression
2. **Consistent cell sizes**: Keep all frames for a single animation the same pixel dimensions
3. **Padding between sprites**: Add 1-2 pixels of transparent padding between sprites to prevent bleed artifacts
4. **Extrude edges**: Set Extrude Edges to 1 in import settings to prevent seam artifacts
5. **Group related sprites**: Keep all frames of an animation on the same sheet for efficient batching
6. **Leave no wasted space**: Pack sprites efficiently to minimize texture memory
7. **File format**: Use PNG for sprites with transparency; PSD for layered source files

### Animation Frame Layout

For character animation sprite sheets:

```
+-------+-------+-------+-------+
| Idle  | Idle  | Idle  | Idle  |
| Fr. 1 | Fr. 2 | Fr. 3 | Fr. 4 |
+-------+-------+-------+-------+
| Walk  | Walk  | Walk  | Walk  |
| Fr. 1 | Fr. 2 | Fr. 3 | Fr. 4 |
+-------+-------+-------+-------+
| Run   | Run   | Run   | Run   |
| Fr. 1 | Fr. 2 | Fr. 3 | Fr. 4 |
+-------+-------+-------+-------+
| Atk   | Atk   | Atk   | Atk   |
| Fr. 1 | Fr. 2 | Fr. 3 | Fr. 4 |
+-------+-------+-------+-------+
```

Each row represents one animation, each column represents one frame. All cells are the same pixel dimensions.

---

## 5. Sprite Renderer Component

The **Sprite Renderer** is the component that displays a sprite in the scene. Attach it to a GameObject to render a 2D sprite.

### Key Properties

| Property | Description |
|----------|-------------|
| **Sprite** | The sprite asset to render |
| **Color** | Tint color applied to the sprite (white = no tint) |
| **Flip** | Mirror the sprite horizontally (X) or vertically (Y) without changing the Transform |
| **Material** | The material used for rendering (default: Sprites-Default) |
| **Draw Mode** | Simple (default), Sliced (for 9-slice), or Tiled |
| **Sorting Layer** | The layer used for draw order sorting |
| **Order in Layer** | The render order within the sorting layer (higher = drawn on top) |
| **Mask Interaction** | How the sprite interacts with Sprite Masks (None, Visible Inside Mask, Visible Outside Mask) |

### Sorting and Layering

Unity renders sprites based on:
1. **Sorting Layer**: Named layers defined in Project Settings (e.g., Background, Default, Foreground, UI)
2. **Order in Layer**: Integer value within a sorting layer; higher values render on top
3. **Distance to Camera**: For sprites on the same layer and order, distance to the camera determines draw order

### Sprite Renderer Draw Modes

| Mode | Description |
|------|-------------|
| **Simple** | Renders the sprite as-is; scaling stretches the entire image |
| **Sliced** | Uses 9-slice borders; corners stay fixed, edges stretch, center tiles or stretches |
| **Tiled** | Tiles the sprite within the defined size; useful for repeating patterns |

---

## 6. Sprite Atlas

A **Sprite Atlas** combines multiple sprite textures into a single optimized texture, reducing draw calls and improving rendering performance.

### Why Use Sprite Atlases?

"A sprite atlas combines multiple textures into a single texture. Unity only needs to create one draw call for all the sprites in a sprite atlas." This significantly reduces GPU overhead, especially for games with many on-screen sprites.

### Creating a Sprite Atlas

1. In the Project window, right-click and select **Create > 2D > Sprite Atlas**
2. Select the new Sprite Atlas asset
3. In the Inspector, click **+** under **Objects for Packing** to add sprites or folders
4. Configure packing settings
5. Click **Pack Preview** to see the result

### Sprite Atlas Settings

| Setting | Description |
|---------|-------------|
| **Type** | Master (primary atlas) or Variant (resolution variant of a master) |
| **Include in Build** | Whether the atlas is included in the built game |
| **Allow Rotation** | Allows sprites to be rotated for tighter packing |
| **Tight Packing** | Packs sprites based on their mesh outline rather than bounding rectangle |
| **Padding** | Pixels between packed sprites to prevent bleed (default: 4) |
| **Max Texture Size** | Maximum atlas texture dimension (default: 2048) |
| **Filter Mode** | Point, Bilinear, or Trilinear |
| **Compression** | Texture compression format |

### Sprite Atlas Best Practices

1. **Group by scene/level**: Put sprites that appear together in the same atlas to maximize batching
2. **Don't exceed 2048x2048** unless necessary: Larger atlases waste memory if only a few sprites are used
3. **Use Tight Packing** for sprites with large transparent areas
4. **Enable Allow Rotation** for better space utilization (unless sprites must maintain orientation)
5. **Create resolution variants** for different platforms (e.g., half resolution for mobile)
6. **Late binding** (runtime loading): Load atlases manually at runtime for memory-critical scenarios

---

## 7. 9-Slice Sprites

9-slicing allows a sprite to be scaled while preserving its border proportions. This is essential for UI panels, dialogue boxes, health bars, and any scalable frame-like elements.

### How 9-Slicing Works

The sprite is divided into 9 regions using border values:

```
+--------+------------------+--------+
| Corner |      Edge        | Corner |
| (fixed)|  (stretch horiz) | (fixed)|
+--------+------------------+--------+
|  Edge  |      Center      |  Edge  |
|(stretch|  (stretch both)  |(stretch|
|  vert) |                  |  vert) |
+--------+------------------+--------+
| Corner |      Edge        | Corner |
| (fixed)|  (stretch horiz) | (fixed)|
+--------+------------------+--------+
```

- **Corners**: Never stretch; maintain original size
- **Edges**: Stretch in one direction only
- **Center**: Stretches in both directions (or tiles)

### Setting Up 9-Slice Borders

1. Open the **Sprite Editor**
2. Select the sprite
3. Set **Border** values: L (Left), R (Right), T (Top), B (Bottom) in pixels
4. Click **Apply**
5. On the Sprite Renderer, set **Draw Mode** to **Sliced** or **Tiled**

---

## 8. Sprite Masking

**Sprite Masks** reveal or hide portions of sprites. The mask sprite defines the visible area.

### Setup

1. Create a GameObject with a **Sprite Mask** component
2. Assign a mask sprite (the alpha channel defines the mask shape)
3. On the sprites to be masked, set **Mask Interaction**:
   - **Visible Inside Mask**: Only renders where the mask exists
   - **Visible Outside Mask**: Only renders where the mask does not exist

### Use Cases

- Revealing portions of a map as the player explores (fog of war)
- Health bar fill effects
- Portal or window effects
- Character silhouettes behind obstacles

---

## 9. Sorting Groups

**Sorting Groups** enable complex layering hierarchies by grouping GameObjects with Sprite Renderers.

### How It Works

A Sorting Group component on a parent GameObject causes all child Sprite Renderers to sort among themselves first, then the group is sorted as a single unit against other renderers in the scene.

### Use Cases

- Multi-part characters (body, clothing, weapons) that should sort together as one unit
- Parallax background layers
- Buildings with interior sprites that sort independently from exterior sprites

---

## 10. Pixel Art Specific Settings

For pixel art game projects, use these recommended import settings:

| Setting | Value | Reason |
|---------|-------|--------|
| **Filter Mode** | Point (no filter) | Preserves sharp pixel edges without anti-aliasing blur |
| **Compression** | None | Prevents compression artifacts on pixel art |
| **Max Size** | Match source size or nearest power of 2 | Prevents unwanted scaling |
| **Mesh Type** | Full Rect | Pixel art sprites are typically rectangular with minimal transparency |
| **PPU** | Match tile/cell size (e.g., 16, 32) | Ensures 1 tile = 1 world unit |
| **Pivot** | Bottom (for characters), Center (for tiles) | Consistent placement |
| **sRGB** | Enabled | Correct color display |

### Camera Settings for Pixel Art

- Set camera to **Orthographic** projection
- Set **Orthographic Size** to `Screen Height / (2 * PPU)` for 1:1 pixel mapping
- Example: 1080p screen with 32 PPU: `1080 / (2 * 32) = 16.875`

---

## 11. Performance Optimization Checklist

1. **Use Sprite Atlases** to batch draw calls for sprites that appear together
2. **Set appropriate Max Size** -- do not use 4096x4096 for a 64x64 sprite
3. **Enable compression** for non-pixel-art sprites to reduce memory
4. **Use Tight mesh type** for sprites with large transparent regions to reduce overdraw
5. **Minimize Sorting Layers** -- each unique layer can break batching
6. **Avoid runtime sprite creation** when possible; pre-bake sprite assets
7. **Use Sprite Masks** instead of alpha-blended overlays for masking effects
8. **Profile with Frame Debugger** (Window > Analysis > Frame Debugger) to identify excessive draw calls
9. **Disable Read/Write Enabled** on sprites that don't need runtime pixel access
10. **Use mipmaps sparingly** -- typically disabled for 2D sprites to save memory

---

## 12. Common Sprite Specifications for Game Projects

### Recommended Sprite Sizes by Asset Type

| Asset Type | Recommended Size | Notes |
|------------|-----------------|-------|
| Character (pixel art) | 32x32 to 64x64 | Per frame; consistent across all frames |
| Character (HD) | 256x256 to 512x512 | Per frame; may vary by character importance |
| Tile (pixel art) | 16x16 or 32x32 | Must be uniform across tileset |
| Tile (HD) | 64x64 to 128x128 | Must be uniform across tileset |
| UI Icons | 32x32 to 128x128 | Provide multiple sizes for different UI contexts |
| Projectile | 8x8 to 32x32 | Small; frequently instantiated |
| VFX Sprite | 64x64 to 256x256 | May use sprite sheet for animation |
| Background | 1920x1080 or tiled | Full-screen or repeating pattern |

### File Format Recommendations

| Format | Use Case | Transparency | Compression |
|--------|----------|-------------|-------------|
| **PNG** | Primary sprite format | Full alpha channel | Lossless |
| **PSD** | Source files with layers | Full alpha channel | None (source only) |
| **TGA** | Legacy format | Full alpha channel | Lossless or RLE |
| **EXR** | HDR sprites, lightmaps | Full alpha channel | Lossy or lossless |
| **JPG** | Backgrounds without transparency | No alpha | Lossy (avoid for sprites) |
