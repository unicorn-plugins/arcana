# Unity Tilemap and 2D Parallax Background Techniques

> Source: https://pixelnest.io/tutorials/2d-game-unity/parallax-scrolling/ , https://medium.com/@Code_With_K/parallax-background-in-unity-fd8766d5a9bd , https://gamedevacademy.org/mastering-unitys-new-tilemap-editor-building-2d-levels/
> Fetched: 2026-03-27

## Overview

This document covers two essential systems for 2D game background artists working in Unity: the Tilemap system for efficient level construction, and parallax scrolling techniques for creating depth in 2D environments.

---

## Part 1: Unity Tilemap System

### What Is a Tilemap?

Unity's Tilemap Editor enables developers to paint levels directly in the Unity editor for rapid 2D level creation. The system eliminates the need for external level design tools and integrates tightly with Unity's 2D rendering and physics pipelines.

### Project Setup

**Folder Structure:**

```
Assets/
  Scenes/
  Tiles/
    Tile Palettes/
    Tile Images/
  Sprites/
    Backgrounds/
    Characters/
```

**Required Packages:**

- 2D Tilemap Editor (included by default in 2D projects)
- 2D Tilemap Extras (for Rule Tiles, Animated Tiles, etc.)

### Creating a Tilemap

1. Right-click in Hierarchy
2. Select **2D Object > Tilemap > Rectangular**
3. This generates a Grid parent object and Tilemap child
4. The Grid defines cell size and layout; the Tilemap holds painted tiles

**Other Tilemap Types:**

- **Rectangular** -- Standard grid layout (most common)
- **Hexagonal** -- Hex-based grids for strategy games
- **Isometric** -- Diamond-shaped tiles for isometric perspective

### Tile Palettes

A Tile Palette is a collection of sprites used for painting levels.

**Creating a Palette:**

1. Navigate to **Window > 2D > Tile Palette**
2. Click "Create New Palette"
3. Assign a descriptive name (e.g., "Dungeon_Walls", "Forest_Ground")
4. Save in the Tile Palettes folder
5. Drag sprite assets into the palette window

**Tip:** Create separate palettes for different tile categories -- solid objects, decorative elements, hazards, interactive tiles, etc.

### Painting Tools

The Tile Palette provides several tools:

| Tool | Function |
|------|----------|
| **Brush** | Paint tiles in the Scene view with selected tile |
| **Box Fill** | Fill rectangular areas with a tile |
| **Fill Selection** | Flood fill an enclosed area |
| **Tile Sampler** | Pick tiles from the Scene (eyedropper) |
| **Eraser** | Remove painted tiles |
| **Move** | Reposition painted tiles |

### Tilemap Layers

Organize complexity through multiple Tilemap layers under a single Grid:

| Layer | Sorting Order | Purpose |
|-------|---------------|---------|
| Background | -10 | Sky, distant scenery, decorative backdrops |
| Terrain | 0 | Solid platforms, walls, ground |
| Detail | 5 | Non-collision decorations (grass, vines, cracks) |
| Foreground | 10 | Elements rendered in front of the player |

**How to Add Layers:**

1. Right-click the Grid object in Hierarchy
2. Select **2D Object > Tilemap > Rectangular**
3. Rename the new Tilemap (e.g., "Background", "Foreground")
4. Set the **Sorting Order** in the Tilemap Renderer component

### Tilemap Collision

**Adding Colliders to Tiles:**

1. Select your Tilemap GameObject
2. Add component: **Tilemap Collider 2D**
3. (Optional) Add **Composite Collider 2D** for optimized physics
4. Enable "Used by Composite" on the Tilemap Collider 2D

The Tilemap Collider 2D automatically generates collision shapes matching your tile layout. Using Composite Collider merges adjacent tile colliders into larger shapes, significantly improving physics performance.

### Rule Tiles

Rule Tiles automatically adjust their appearance based on neighboring tiles, creating natural-looking terrain transitions without manual placement.

**Setup:**

1. Right-click in Project > **Create > 2D > Tiles > Rule Tile**
2. Add tiling rules: define which sprite appears based on neighbor conditions
3. Each rule specifies neighboring tile requirements (present, absent, or any)
4. Drag the Rule Tile into a Tile Palette for painting

**Common Rules:**

- Center tile (surrounded on all sides)
- Edge tiles (one side exposed)
- Corner tiles (two adjacent sides exposed)
- Single tile (fully isolated)
- End caps (one connection only)

### Animated Tiles

Animated Tiles cycle through a sequence of sprites at a defined speed:

1. Create via **Create > 2D > Tiles > Animated Tile**
2. Assign sprite frames in order
3. Set animation speed
4. Paint like any other tile

**Use Cases:** Water surfaces, lava flows, flickering torches, swaying vegetation.

### Scripting Tilemap Access

Access Tilemaps programmatically through the `Tilemap` component:

```csharp
using UnityEngine;
using UnityEngine.Tilemaps;

public class TilemapController : MonoBehaviour
{
    private Tilemap tilemap;

    void Start()
    {
        tilemap = GetComponent<Tilemap>();
    }

    // Get a tile at a specific cell position
    public TileBase GetTileAt(Vector3Int cellPosition)
    {
        return tilemap.GetTile(cellPosition);
    }

    // Set a tile at a specific cell position
    public void SetTileAt(Vector3Int cellPosition, TileBase tile)
    {
        tilemap.SetTile(cellPosition, tile);
    }

    // Convert world position to cell position
    public Vector3Int WorldToCell(Vector3 worldPosition)
    {
        return tilemap.WorldToCell(worldPosition);
    }

    // Clear all tiles
    public void ClearAll()
    {
        tilemap.ClearAllTiles();
    }
}
```

### Tilemap Best Practices

| Practice | Benefit |
|----------|---------|
| Consistent tile sizes | Simplifies alignment and scaling |
| Layer organization | Reduces rendering overhead and keeps scenes manageable |
| Rule Tile usage | Accelerates terrain painting dramatically |
| Palette categorization | Improves workflow efficiency for large tilesets |
| Composite colliders | Optimizes physics calculations |
| Naming conventions | Use clear names like "Ground_Tilemap", "Deco_Tilemap" |

---

## Part 2: 2D Parallax Scrolling

### Theory

Parallax scrolling is a 2D art technique that gives an illusion of depth by making background images move slower than those in the foreground. The idea is to move the background layers at different speeds -- the farther the layer is, the slower it moves. If done correctly, this gives a convincing illusion of depth.

### Design Decisions

**Two primary approaches exist:**

1. **Player and camera move; backgrounds scroll** -- Works naturally with depth-based parallax. The camera follows the player, and background layers move proportionally.
2. **Player and camera static; level is a treadmill** -- The world moves past the camera. Common in endless runners and shmups.

**Recommended hybrid for most 2D games:**

- Player moves forward with the camera
- Background elements move at varying speeds relative to camera movement
- This creates the parallax illusion with an orthographic camera

### Layer Organization

Standard parallax layer structure:

| Layer | Parallax Factor | Loop | Example Content |
|-------|----------------|------|-----------------|
| Far Background | 0.1 - 0.2 | Yes | Sky, distant mountains, clouds |
| Mid Background | 0.3 - 0.5 | Yes | Hills, tree lines, distant buildings |
| Near Background | 0.6 - 0.8 | Optional | Closer trees, structures |
| Gameplay Layer | 1.0 | No | Player, enemies, platforms |
| Near Foreground | 1.2 - 1.5 | Optional | Close foliage, dust particles |
| Far Foreground | 1.5 - 2.0 | Optional | Closest decorative elements |

### Scene Hierarchy Setup

```
ParallaxBackground (Empty GameObject)
  |- Sky_Layer (SpriteRenderer, z=10)
  |- Mountains_Layer (SpriteRenderer, z=8)
  |- Trees_Layer (SpriteRenderer, z=5)
  |- Clouds_Layer (SpriteRenderer, z=9)
Gameplay
  |- Player
  |- Enemies
  |- Tilemap_Ground
Foreground (Empty GameObject)
  |- FG_Foliage (SpriteRenderer, z=-2)
```

### Basic Parallax Controller Script

Attach this script to each background layer:

```csharp
using UnityEngine;

public class ParallaxController : MonoBehaviour
{
    private float length, startpos;
    public GameObject cam;
    public float parallaxEffect;

    void Start()
    {
        startpos = transform.position.x;
        length = GetComponent<SpriteRenderer>().bounds.size.x;
    }

    void Update()
    {
        float temp = (cam.transform.position.x * (1 - parallaxEffect));
        float dist = (cam.transform.position.x * parallaxEffect);

        transform.position = new Vector3(
            startpos + dist,
            transform.position.y,
            transform.position.z
        );

        // Infinite scrolling loop
        if (temp > startpos + length) startpos += length;
        else if (temp < startpos - length) startpos -= length;
    }
}
```

**Configuration per Layer:**

- Assign Main Camera to the `cam` field
- Set `parallaxEffect` value (0 = no movement, 1 = moves with camera):
  - Sky: 0.1
  - Far mountains: 0.2
  - Mid mountains: 0.5
  - Near trees: 0.7
  - Foreground: 1.0 (or greater for foreground parallax)

### Advanced Parallax with Looping

For seamless infinite backgrounds with proper object recycling:

```csharp
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class ScrollingScript : MonoBehaviour
{
    /// <summary>
    /// Scrolling speed
    /// </summary>
    public Vector2 speed = new Vector2(10, 10);

    /// <summary>
    /// Moving direction
    /// </summary>
    public Vector2 direction = new Vector2(-1, 0);

    /// <summary>
    /// Movement should be applied to camera
    /// </summary>
    public bool isLinkedToCamera = false;

    /// <summary>
    /// Background is infinite
    /// </summary>
    public bool isLooping = false;

    private List<SpriteRenderer> backgroundPart;

    void Start()
    {
        if (isLooping)
        {
            backgroundPart = new List<SpriteRenderer>();

            for (int i = 0; i < transform.childCount; i++)
            {
                Transform child = transform.GetChild(i);
                SpriteRenderer r = child.GetComponent<SpriteRenderer>();
                if (r != null)
                {
                    backgroundPart.Add(r);
                }
            }

            // Sort by position (left to right)
            backgroundPart = backgroundPart.OrderBy(
                t => t.transform.position.x
            ).ToList();
        }
    }

    void Update()
    {
        Vector3 movement = new Vector3(
            speed.x * direction.x,
            speed.y * direction.y,
            0);

        movement *= Time.deltaTime;
        transform.Translate(movement);

        if (isLinkedToCamera)
        {
            Camera.main.transform.Translate(movement);
        }

        if (isLooping)
        {
            SpriteRenderer firstChild = backgroundPart.FirstOrDefault();

            if (firstChild != null)
            {
                if (firstChild.transform.position.x < Camera.main.transform.position.x)
                {
                    if (firstChild.IsVisibleFrom(Camera.main) == false)
                    {
                        SpriteRenderer lastChild = backgroundPart.LastOrDefault();
                        Vector3 lastPosition = lastChild.transform.position;
                        Vector3 lastSize = (lastChild.bounds.max - lastChild.bounds.min);

                        firstChild.transform.position = new Vector3(
                            lastPosition.x + lastSize.x,
                            firstChild.transform.position.y,
                            firstChild.transform.position.z
                        );

                        backgroundPart.Remove(firstChild);
                        backgroundPart.Add(firstChild);
                    }
                }
            }
        }
    }
}
```

### Visibility Extension Helper

Required utility for the advanced looping script:

```csharp
using UnityEngine;

public static class RendererExtensions
{
    public static bool IsVisibleFrom(this Renderer renderer, Camera camera)
    {
        Plane[] planes = GeometryUtility.CalculateFrustumPlanes(camera);
        return GeometryUtility.TestPlanesAABB(planes, renderer.bounds);
    }
}
```

This extension checks whether a renderer is within the camera's viewing frustum.

### Layer Speed Configuration Table

For the advanced ScrollingScript approach:

| Layer | Speed | Direction | Linked to Camera | Looping |
|-------|-------|-----------|-------------------|---------|
| Far Background | (1, 1) | (-1, 0) | No | Yes |
| Mid Background | (1.5, 1.5) | (-1, 0) | No | Yes |
| Near Background | (2.5, 2.5) | (-1, 0) | No | No |
| Foreground (player) | (1, 1) | (1, 0) | Yes | No |

Faster speeds create the illusion of closer distance, building depth perception.

### Vertical Parallax

For games with vertical scrolling, extend the parallax system to the Y axis:

```csharp
void Update()
{
    float distX = cam.transform.position.x * parallaxEffectX;
    float distY = cam.transform.position.y * parallaxEffectY;

    transform.position = new Vector3(
        startPosX + distX,
        startPosY + distY,
        transform.position.z
    );
}
```

Assign separate parallax factors for X and Y axes per layer for full 2D depth control.

---

## Part 3: Combining Tilemap and Parallax

### Architecture

Tilemaps work best for gameplay layers where collision and interaction matter. Parallax backgrounds typically use regular Sprite Renderers for non-interactive scenic layers.

**Recommended Structure:**

```
Scene
  |- ParallaxBackground/
  |    |- Sky (SpriteRenderer, parallax=0.1)
  |    |- Mountains (SpriteRenderer, parallax=0.3)
  |    |- DistantTrees (SpriteRenderer, parallax=0.5)
  |
  |- Grid/
  |    |- Background_Tilemap (decorative, no collider)
  |    |- Ground_Tilemap (TilemapCollider2D + CompositeCollider2D)
  |    |- Detail_Tilemap (decorative overlays, no collider)
  |
  |- Player
  |- Enemies
  |
  |- Foreground/
       |- FG_Foliage (SpriteRenderer, parallax=1.3)
```

### Tilemap with 2D Lighting (URP)

When using URP 2D Lighting with Tilemaps:

1. Ensure the Tilemap Renderer component's material is set to a Sprite-Lit material
2. The 2D Renderer Data must be assigned in the URP Pipeline Asset
3. Lights will affect tilemap tiles the same way they affect regular sprites
4. Shadow Caster 2D can be added to tilemap GameObjects for shadow effects

### Camera Setup for Parallax

**Cinemachine Integration (Recommended):**

1. Install Cinemachine via Package Manager
2. Create a Virtual Camera targeting the player
3. Configure damping for smooth following
4. Parallax scripts reference the Main Camera (which Cinemachine controls)

**Manual Camera Follow:**

```csharp
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;
    public float smoothSpeed = 0.125f;
    public Vector3 offset;

    void LateUpdate()
    {
        Vector3 desiredPosition = target.position + offset;
        Vector3 smoothedPosition = Vector3.Lerp(
            transform.position,
            desiredPosition,
            smoothSpeed
        );
        transform.position = new Vector3(
            smoothedPosition.x,
            smoothedPosition.y,
            transform.position.z
        );
    }
}
```

### Constraining Player to Camera Bounds

Prevent the player from leaving the visible area:

```csharp
// Add to PlayerScript Update()
var dist = (transform.position - Camera.main.transform.position).z;

var leftBorder = Camera.main.ViewportToWorldPoint(
    new Vector3(0, 0, dist)).x;
var rightBorder = Camera.main.ViewportToWorldPoint(
    new Vector3(1, 0, dist)).x;
var topBorder = Camera.main.ViewportToWorldPoint(
    new Vector3(0, 0, dist)).y;
var bottomBorder = Camera.main.ViewportToWorldPoint(
    new Vector3(0, 1, dist)).y;

transform.position = new Vector3(
    Mathf.Clamp(transform.position.x, leftBorder, rightBorder),
    Mathf.Clamp(transform.position.y, topBorder, bottomBorder),
    transform.position.z
);
```

---

## Best Practices and Warnings

### Parallax

- **Avoid `OnBecameVisible()` and `OnBecameInvisible()`** -- These methods execute differently in the Scene view versus builds, creating unpredictable behavior.
- Use consistent sprite dimensions for predictable looping behavior.
- Test parallax effects across various camera speeds.
- Layer backgrounds from slowest (back) to fastest (front) movement.
- Monitor performance with multiple layers.
- Document your parallax factor values for consistency across similar scenes.
- For pixel-perfect games, ensure parallax movement aligns with pixel grid to avoid sub-pixel jitter.

### Tilemap

- Use consistent tile sizes (16x16, 32x32, or 64x64 are common).
- Keep Tilemap layers organized with clear naming conventions.
- Use Rule Tiles extensively to accelerate terrain creation.
- Apply Composite Colliders for any tilemap with physics interaction.
- Separate collision tiles from decorative tiles on different layers.

### Performance

- Minimize the total number of parallax layers (4-6 is typically sufficient).
- Use texture atlases for tilemap sprites to reduce draw calls.
- Profile on target hardware, especially mobile devices.
- Consider disabling distant parallax layers on lower-end devices.
- Use object pooling for any dynamically spawned background elements.
