# Unity 2D Game Development Overview

> Source: https://docs.unity3d.com/Manual/Unity2D.html
> Fetched: 2026-03-27

## Unity 2D Overview

Unity provides a comprehensive suite of 2D tools for developing 2D games and 2D elements within 3D projects. Unity's 2D features include dedicated components, rendering pipeline optimizations, and editor workflows designed specifically for 2D content.

## Core 2D Components

### Sprites
- **Sprite Renderer**: Renders 2D images (sprites) in the scene
- **Sprite Editor**: Slice sprite sheets, set pivots, edit meshes
- **Sprite Atlas**: Pack multiple sprites into a single texture for performance
- **Sprite Shape**: Create freeform 2D environments with fill and edge sprites
- **9-Slice Sprites**: Scale UI elements without distorting corners

### 2D Physics
- **Rigidbody 2D**: Physics simulation for 2D objects (Dynamic, Kinematic, Static)
- **Collider 2D**: Box, Circle, Polygon, Edge, Capsule, Composite
- **Physics Material 2D**: Friction and bounciness settings
- **Effectors 2D**: Area, Buoyancy, Platform, Point, Surface effectors
- **Joints 2D**: Distance, Fixed, Friction, Hinge, Relative, Slider, Spring, Target, Wheel

### Tilemap
- **Tilemap Component**: Grid-based tile painting system
- **Tile Palette**: Visual tool for painting tiles
- **Rule Tiles**: Automated tile placement based on neighbor rules
- **Animated Tiles**: Tiles with frame-by-frame animation
- **Tilemap Collider 2D**: Auto-generate colliders from tilemap

## Rendering Pipeline for 2D

### Universal Render Pipeline (URP) 2D
Unity's recommended render pipeline for 2D games.

**Setup:**
1. Install URP package via Package Manager
2. Create URP Asset with 2D Renderer
3. Assign to Project Settings → Graphics → Scriptable Render Pipeline
4. Create 2D Renderer Data asset

**2D Renderer Features:**
- 2D Lights (Global, Point, Spot, Freeform, Sprite)
- Light Blending (multiply, additive, custom)
- Shadow Caster 2D
- Normal Map support for 2D sprites
- Sprite Lit / Sprite Unlit default shaders

### Sorting and Layers

**Sorting Layers** (rendering order):
```
Background (furthest)
  └── Far Parallax
  └── Mid Parallax
  └── Near Parallax
Environment
  └── Ground
  └── Props
Characters
  └── Enemies
  └── Player
Foreground
  └── Weather
  └── Particles
UI (closest)
```

**Order in Layer**: Integer value within a sorting layer (higher = rendered on top)

**Sorting Groups**: Override sorting for a group of renderers

## Animation System for 2D

### Sprite Animation
- **Animation Clips**: Keyframe-based sprite swapping
- **Animator Controller**: State machine for animation transitions
- **Blend Trees**: Blend between animations based on parameters

### Spine Integration
- Spine-Unity runtime for skeletal animation
- SkeletonAnimation, SkeletonMecanim components
- Supports: skins, events, physics, blend modes

### Frame-by-Frame
- Import sprite sheets with multiple frames
- Use Animation window to set frame timing
- Typical rates: 12fps (stylized), 24fps (smooth), 30fps (fluid)

## 2D Project Architecture

### Recommended Folder Structure
```
Assets/
├── Animations/
│   ├── Characters/
│   └── Effects/
├── Audio/
│   ├── BGM/
│   └── SFX/
├── Data/
│   ├── Cards/          (ScriptableObjects)
│   ├── Characters/     (ScriptableObjects)
│   └── Enemies/        (ScriptableObjects)
├── Materials/
├── Prefabs/
│   ├── Characters/
│   ├── Cards/
│   ├── Effects/
│   └── UI/
├── Scenes/
├── Scripts/
│   ├── Combat/
│   ├── Cards/
│   ├── Data/
│   ├── UI/
│   └── Utils/
├── Sprites/
│   ├── Characters/
│   ├── Backgrounds/
│   ├── Cards/
│   ├── Effects/
│   └── UI/
└── Tilemaps/
```

### Key Unity 2D Packages

| Package | Purpose |
|---------|---------|
| 2D Sprite | Core sprite tools |
| 2D SpriteShape | Freeform terrain |
| 2D Tilemap | Grid-based levels |
| 2D Animation | Skeletal 2D animation |
| 2D Pixel Perfect | Pixel art rendering |
| 2D PSD Importer | Import Photoshop files |
| Universal RP | 2D lighting & rendering |
| TextMeshPro | Advanced text rendering |
| Cinemachine | 2D camera system |
| Input System | New input handling |

## Performance Considerations for 2D

- **Sprite Atlases**: Reduce draw calls by batching sprites
- **Object Pooling**: Reuse frequently spawned objects (cards, effects)
- **Camera culling**: Only render visible sprites
- **Minimize overdraw**: Avoid overlapping transparent sprites
- **Profiler**: Use Frame Debugger to check draw call count
- **Target**: 60fps on integrated GPU for PC card game
