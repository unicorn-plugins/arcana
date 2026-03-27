# Unity Particle System

> Source: https://docs.unity3d.com/6000.3/Documentation/Manual/ParticleSystems.html
> Fetched: 2026-03-27

## Overview

A Particle System in Unity simulates and renders many small images or meshes, called **particles**, to produce a visual effect. Each particle in a system represents an individual graphical element in the effect, and the collective simulation of all particles creates the complete visual impression.

Particle systems are ideal for creating dynamic, fluid-like phenomena such as fire, smoke, clouds, liquids, sparks, dust, and magical effects. These phenomena are difficult to depict using traditional mesh or sprite-based approaches. Solid structures like buildings, characters, or vehicles are better represented through conventional meshes.

Unity provides two particle system solutions:
- **Built-in Particle System** — The legacy, CPU-based system with extensive module support
- **Visual Effect Graph** — A GPU-based, node-graph authoring tool for advanced effects

## Creating a Particle System

There are two ways to add a Particle System to your scene:

1. **As a new GameObject**: Navigate to `GameObject > Effects > Particle System`
2. **As a component on an existing GameObject**: Use `Component > Effects > Particle System`

### Inspector Layout

The Particle System component features a modular Inspector design divided into collapsible sub-sections called **modules**. Each module contains a group of related properties. You can also use a separate Editor window via the **Open Editor** button to edit one or more systems simultaneously.

### Playback Controls

When a Particle System is selected, the Scene view displays a control panel with:
- **Playback Speed** — Adjust simulation speed for previewing effects
- **Playback Time** — Shows elapsed time; drag left/right to scrub through the timeline
- **Particle Count** — Displays current number of active particles
- **Play/Pause/Stop** — Standard playback controls for simulation

### Inspector Properties

| Property | Description |
|----------|-------------|
| **Simulate Layers** | Preview non-selected Particle Systems by matching layer masks |
| **Resimulate** | When enabled, immediately applies property modifications to already-generated particles |
| **Show Bounds** | Displays the bounding volume around selected systems |
| **Show Only Selected** | Hides unselected Particle Systems for focused editing |

## Particle System Modules

### Main Module

The Main module configures the initial state of newly spawned particles. It establishes foundational properties including:
- **Duration** — Length of time the system runs
- **Looping** — Whether the system repeats after completing
- **Start Lifetime** — How long each particle lives
- **Start Speed** — Initial velocity of particles
- **Start Size** — Initial scale of particles
- **Start Rotation** — Initial rotation of particles
- **Start Color** — Initial color of particles
- **Gravity Modifier** — Scales the effect of Physics gravity
- **Simulation Space** — Whether particles move in Local or World space
- **Play On Awake** — Whether the system starts automatically
- **Max Particles** — Maximum number of particles the system can have at once

### Emission Module

Manages the rate and timing of particle emissions, controlling how frequently and when particles are generated.

Key properties:
- **Rate over Time** — Number of particles emitted per second
- **Rate over Distance** — Number of particles emitted per unit of distance moved
- **Bursts** — Timed emission events that spawn a set number of particles at specific times

### Shape Module

Defines the volume or surface that the Particle System uses to emit particles, and the direction of the start velocity. Available shapes include:
- Sphere / Hemisphere
- Cone
- Box
- Circle / Edge
- Mesh / Mesh Renderer / Skinned Mesh Renderer
- Sprite / Sprite Renderer
- Rectangle

### Velocity over Lifetime

Allows particles to change velocity over time, enabling dynamic motion patterns throughout a particle's existence. Supports:
- Linear velocity (X, Y, Z)
- Orbital velocity
- Radial velocity
- Speed modifier curves

### Limit Velocity over Lifetime

Configures particles to reduce in velocity over time, creating drag or friction effects. Useful for simulating air resistance or slowing down debris.

### Inherit Velocity

Ensures the velocity of particles matches or inherits from the parent emitter's velocity. Modes include:
- **Current** — Applies the emitter's current velocity each frame
- **Initial** — Applies the emitter's velocity at the time of particle spawn

### Lifetime by Emitter Speed

Adjusts the initial lifetime of each particle based on the speed of the emitter when the particle spawns. Faster-moving emitters can produce longer or shorter-lived particles.

### Force over Lifetime

Applies simulated physics forces that affect the movement of particles over time. Useful for wind, gravity variations, or directional forces.

### Color over Lifetime

Enables particles to change color over time using a gradient. Common uses:
- Fading out particles as they die (alpha reduction)
- Transitioning fire from yellow to orange to red
- Creating rainbow or color-cycling effects

### Color by Speed

Makes particles change color based on their current speed. Fast-moving particles can appear differently from slow-moving ones.

### Size over Lifetime

Allows particles to change size over time using a curve. Common uses:
- Growing particles that expand outward (explosions)
- Shrinking particles that fade away (dissipating smoke)
- Pulsing effects using oscillating curves

### Size by Speed

Makes particles change size based on their speed. Useful for stretch-like effects on fast particles.

### Rotation over Lifetime

Configures particles to spin or rotate over time. Supports:
- Angular velocity curves
- Separate X, Y, Z rotation (3D mode)

### Rotation by Speed

Makes particles change their rotation speed based on how fast they are moving.

### External Forces

Configures the effect of external physics forces such as Wind Zones and Force Fields on particles. Properties include:
- **Multiplier** — Scales the effect of external forces
- **Influence Filter** — Controls which force fields affect the system

### Noise Module

Controls the turbulence of particles as they move, adding organic variation to particle motion. Properties include:
- **Strength** — Intensity of the noise effect
- **Frequency** — How rapidly the noise pattern changes
- **Scroll Speed** — How fast the noise field moves
- **Damping** — Whether strength is proportional to frequency
- **Octaves** — Layers of noise for more complex patterns
- **Quality** — Low (1D), Medium (2D), or High (3D) noise

### Collision Module

Manages particle collisions with scene geometry. Two modes:
- **Planes** — Collisions with defined planes
- **World** — Collisions with scene colliders

Properties include:
- **Bounce** — How much velocity is retained after collision
- **Lifetime Loss** — Fraction of lifetime lost on collision
- **Min Kill Speed** — Minimum speed below which particles are destroyed

### Triggers Module

Configures particles that act as triggers for gameplay interactions. Can detect when particles enter, exit, or exist inside specified colliders and respond with actions like:
- Kill the particle
- Send a callback
- Ignore the trigger

### Sub Emitters Module

Enables particles that emit other particles, creating hierarchical emission systems. Sub-emitters can trigger on:
- **Birth** — When a particle is born
- **Collision** — When a particle collides
- **Death** — When a particle dies
- **Trigger** — When a particle enters a trigger
- **Manual** — Via scripting

### Texture Sheet Animation

Uses a texture grid to create animation frames for particle sprites. Supports:
- Grid mode (rows and columns on a single texture)
- Sprites mode (individual sprite assets)
- Frame over Time curves
- Start Frame randomization
- Animation cycling modes

### Lights Module

Configures real-time lights attached to particles for dynamic lighting effects. Properties:
- **Light** — Reference to a Light prefab
- **Ratio** — Fraction of particles that receive lights
- **Random Distribution** — Randomize which particles get lights
- **Use Particle Color** — Match light color to particle color
- **Size Affects Range** — Particle size influences light range
- **Alpha Affects Intensity** — Particle alpha influences light brightness

### Trails Module

Creates trails behind particles for motion visualization. Useful for:
- Sparkler effects
- Meteor trails
- Magic projectile paths
- Speed lines

Properties include trail lifetime, minimum vertex distance, texture mode, color over trail, and width over trail.

### Custom Data Module

Allows attachment of custom data formats in the Editor to particles. This data can be read in scripts or shaders for specialized behaviors.

### Renderer Module

Controls how a particle's image or mesh is transformed, shaded, and overdrawn by other particles. Key settings:
- **Render Mode** — Billboard, Stretched Billboard, Horizontal/Vertical Billboard, Mesh
- **Material** — The material used to render particles
- **Sort Mode** — How particles are sorted for rendering
- **Min/Max Particle Size** — Screen-space size limits
- **Render Alignment** — View, World, Local, or Facing alignment
- **Pivot** — Offset for the particle's pivot point

## Performance Best Practices

1. **Limit Max Particles** — Keep the particle count as low as possible while maintaining visual quality
2. **Use Simple Materials** — Avoid complex shaders on particle materials
3. **Minimize Overdraw** — Reduce particle overlap, especially with transparent particles
4. **Use LOD** — Reduce particle counts at distance
5. **Disable Unnecessary Modules** — Only enable modules you actually need
6. **Avoid Collision on Mobile** — World collision is expensive; use planes when possible
7. **Texture Atlasing** — Combine particle textures to reduce draw calls
8. **Simulation Space** — Use Local space when possible for better performance
9. **GPU Instancing** — Enable GPU instancing on particle materials when supported
10. **Culling** — Use bounding volume culling to skip off-screen systems
