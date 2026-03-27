# Unity Shader Graph and VFX Graph

> Source: https://docs.unity3d.com/Manual/shader-graph.html
> Fetched: 2026-03-27

## Part 1: Shader Graph

### Overview

Shader Graph is a visual shader development tool that enables you to build shaders by creating and connecting nodes in a graph framework, rather than writing shader code manually. It offers instant feedback that reflects your changes, making it accessible to both experienced developers and those new to shader creation.

Shader Graph comes automatically included when you install either the Universal Render Pipeline (URP) or High Definition Render Pipeline (HDRP).

### Render Pipeline Compatibility

| Pipeline | Shader Graph Support |
|----------|---------------------|
| Universal Render Pipeline (URP) | Yes |
| High Definition Render Pipeline (HDRP) | Yes |
| Built-in Render Pipeline | Yes |
| Custom Scriptable Render Pipeline | No |

### Key Concepts

#### Nodes

Nodes are the fundamental building blocks of a Shader Graph. Each node performs a specific operation — from simple math to complex texture sampling. Nodes have input and output ports that connect via edges to form a processing pipeline.

Common node categories include:
- **Math** — Add, Multiply, Lerp, Clamp, Step, Smoothstep, Remap
- **UV** — Tiling and Offset, Rotate, Polar Coordinates, Twirl, Spherize
- **Procedural** — Noise (Simple, Gradient, Voronoi), Checkerboard, Shape
- **Channel** — Split, Combine, Swizzle, Flip
- **Input** — Texture 2D, Color, Vector, Time, Position, Normal, UV
- **Artistic** — Blend, Contrast, Saturation, Hue, White Balance, Channel Mixer

#### Edges

Edges are the connections between node ports. They define the flow of data through the graph. Edges carry typed data (float, Vector2, Vector3, Vector4, Color, Texture, etc.) and support implicit type conversions.

#### Master Stack

The Master Stack is the endpoint of a Shader Graph. It defines the final surface properties of the shader:

**Vertex Stage:**
- Position
- Normal
- Tangent

**Fragment Stage:**
- Base Color
- Normal (Tangent/Object/World)
- Metallic
- Smoothness
- Emission
- Ambient Occlusion
- Alpha
- Alpha Clip Threshold

#### Graph Inspector

The Graph Inspector allows you to view and modify properties of the graph, nodes, and graph settings. It contains:
- **Node Settings** — Properties specific to the selected node
- **Graph Settings** — Global settings like Surface Type (Opaque/Transparent), Alpha Clipping, Render Face, etc.

#### Sub Graphs

Sub Graphs are reusable shader graph assets that can be nested inside other Shader Graphs. They help:
- Reduce duplication of common node patterns
- Organize complex shaders into manageable pieces
- Share functionality across multiple shaders

#### Custom Function Node

The Custom Function Node allows you to write custom HLSL code within a Shader Graph. It supports:
- **String mode** — Write HLSL directly in the node
- **File mode** — Reference an external HLSL file

This is essential for accessing features not available through built-in nodes.

#### Blackboard Properties

The Blackboard is where you define exposed properties that can be modified from the Material Inspector or via script:
- Float, Integer, Boolean
- Vector2, Vector3, Vector4
- Color, Texture2D, Texture3D, Cubemap
- Gradient, Matrix
- Keywords (Boolean, Enum, Built-in)

#### Keywords

Keywords enable shader variants — different compilation paths within the same shader:
- **Boolean Keyword** — On/Off toggle
- **Enum Keyword** — Multiple named options
- **Built-in Keyword** — Unity-defined keywords (e.g., quality levels)

### Common VFX Shader Techniques in Shader Graph

#### Dissolve Effect
Use a noise texture with a Step or Smoothstep node compared against a threshold property to create dissolve effects with optional edge emission.

#### Fresnel / Rim Lighting
Use the Fresnel Effect node to create glowing edges on objects — useful for shields, magic auras, and selection highlights.

#### Scrolling Textures
Combine Time node with Tiling and Offset to create scrolling UV effects for fire, water, energy fields.

#### Distortion / Heat Haze
Sample a noise texture to offset screen-space UVs for refraction and distortion effects.

#### Color Gradient Mapping
Remap grayscale textures through a gradient to create stylized color effects.

---

## Part 2: Visual Effect Graph (VFX Graph)

### Overview

The Visual Effect Graph (VFX Graph) is a node-based visual authoring tool for creating GPU-accelerated particle effects and visual simulations. It enables you to author visual effects using node-based visual logic. Effects are stored as Visual Effect Assets that integrate with the Visual Effect Component and can be reused multiple times throughout a scene.

### Key Differences from Built-in Particle System

| Feature | Built-in Particle System | VFX Graph |
|---------|------------------------|-----------|
| Processing | CPU-based | GPU-based (Compute Shaders) |
| Authoring | Inspector modules | Node graph |
| Particle Count | Thousands | Millions |
| Mesh Output | Limited | Full mesh support |
| Scripting Access | Extensive API | Limited API |
| Platform Support | All platforms | Compute shader capable |
| Learning Curve | Lower | Higher |

### Core Concepts

#### Systems

A System is the fundamental unit of a VFX Graph. It represents a complete particle effect pipeline containing multiple Contexts arranged vertically.

#### Contexts

Contexts define the stages of a particle effect's lifecycle:

- **Spawn** — Controls when and how many particles are created
  - Rate (constant emission)
  - Burst (periodic bursts)
  - Custom spawn logic via blocks

- **Initialize** — Sets the initial state of each particle at birth
  - Position (shapes: sphere, box, circle, line, mesh surface)
  - Velocity (direction and speed)
  - Lifetime
  - Size, Color, Rotation
  - Custom attributes

- **Update** — Modifies particle properties each frame
  - Forces (gravity, drag, wind)
  - Turbulence / Noise
  - Collision
  - Conform to Sphere/SDF
  - Age and lifetime management

- **Output** — Defines how particles are rendered
  - Particle Quad / Triangle / Octagon
  - Particle Mesh
  - Particle Strip (trails / ribbons)
  - Particle Point (point cloud)
  - Lit / Unlit variants

#### Blocks

Blocks are the operations within Contexts. They are stacked vertically and execute in order. Examples:
- Set Position (Random: Sphere)
- Set Velocity (Random)
- Set Size over Lifetime (Curve)
- Turbulence (Perlin)
- Collision with Plane

#### Operators

Operators are nodes that perform calculations outside of contexts. They process values and feed results into Blocks or other Operators:
- Math operations
- Noise generators
- Sampling (curves, gradients, textures)
- Logic and comparison
- Transform operations

#### Properties (Blackboard)

Exposed properties that can be set per-instance from the Inspector or via script:
- Float, Int, Bool
- Vector2/3/4, Color
- Texture, Mesh
- Gradient, Curve
- AnimationCurve

#### Subgraphs

Reusable graph fragments that encapsulate common patterns. Types:
- **Subgraph Block** — Reusable block logic
- **Subgraph Operator** — Reusable operator logic
- **Subgraph Context** — Reusable context logic (limited)

### VFX Graph + Shader Graph Integration

Visual Effect Graphs can use compatible Shader Graphs to render particles, enabling visually authored custom shaders for particle output.

#### Setup Steps

1. Open a Shader Graph in the Shader Graph window
2. In Graph Settings, select a render pipeline Target (HDRP or Universal)
3. Enable **Support VFX Graph** in the Graph Settings
4. Save the Shader Graph

#### Using in VFX Graph

1. Open your Visual Effect Graph (or create via `Create > Visual Effects > Visual Effect Graph`)
2. Assign your compatible Shader Graph to the **Shader Graph** property on the output context
3. Click the output Context to view and modify Inspector options

**Important:** Edits made to a Shader Graph's exposed properties via the VFX Graph Inspector are local to that VFX Graph instance and do not affect the original Shader Graph asset.

#### Supported Output Contexts

- Particle Shader Graph Mesh
- Particle Shader Graph Primitive (Quad, Triangle, Octagon)
- ParticleStrip Shader Graph Quad

#### Performance Note

VFX Graph support does not impact runtime performance, but Shader Graphs with **Support VFX Graph** enabled take longer to compile.

#### Limitations

**Unsupported Blackboard Properties:**
- Diffusion Profile
- Virtual Texture
- Gradient

**Target-Specific Restrictions:**
- HDRP: No Decal or Fog Volume support; limited vertex animation motion vectors
- URP: No Decal support

### Common VFX Graph Techniques

#### Fire and Flames
- Spawn with rate, initialize on cone shape
- Velocity upward with turbulence in Update
- Color over Lifetime gradient (white > yellow > orange > red > black)
- Size decreasing over lifetime
- Additive blend mode output

#### Smoke and Fog
- Low velocity, high lifetime
- Noise-based movement for organic drift
- Opacity fading over lifetime
- Large particle sizes with soft blending

#### Sparks and Debris
- Burst spawn on event
- High initial velocity with random spread
- Gravity force in Update
- Small size, bright color, short lifetime
- Optional collision and bounce

#### Magic / Energy Effects
- Orbital velocity around a center point
- Fresnel-based Shader Graph output
- Color cycling via noise or gradient
- Strip output for trail/ribbon effects

#### Impact / Hit Effects
- Event-triggered burst spawning
- Radial velocity from impact point
- Rapid size reduction
- Multiple systems layered (flash, sparks, smoke, debris)
