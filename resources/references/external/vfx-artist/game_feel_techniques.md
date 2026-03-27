# Game Feel and Juice Techniques

> Source: https://gamedevacademy.org/game-feel-tutorial/
> Fetched: 2026-03-27

## Overview

Game feel, also called "game juice," refers to the tactile virtual sensation experienced during video game interaction. It encompasses how quickly character animations respond to player input and the quality of audiovisual feedback for actions. Though subtle in design, these elements dramatically impact engagement and create memorable player experiences.

The term "juice" describes the immediate visual and audio feedback that responds to player actions — the "oomph" factor like screen shake when firing a weapon, particle explosions when destroying an enemy, or satisfying sound effects when collecting items. Juicing is about taking a game that works and adding layers of satisfaction.

**Core Principle:** Your game's juice should always echo your core gameplay. All techniques must reinforce existing mechanics rather than be applied arbitrarily.

---

## Fundamental Principles

### 1. Emphasize Player Success
- Use visual celebrations (confetti, screen effects)
- Play encouraging audio feedback
- Implement brief screen pauses (millisecond-level freezes)
- Combine multiple effects for satisfying moments

### 2. Emotional Touch
- Apply slow-motion effects for dramatic moments
- Use cinematic camera angles
- Include ambient soundscapes
- Create dramatic impacts for significant events (deaths, victories)

### 3. Add Randomness
- Vary projectile accuracy slightly
- Randomize AI behaviors
- Use diverse sound effect variations
- Prevent gameplay from feeling repetitive or mechanical

### 4. Create Permanence
- Display explosions and debris that persist
- Leave enemy corpses or destruction marks visible
- Show environmental destruction
- Demonstrate lasting consequences of player actions

### 5. Make Controls Satisfying
- Implement advanced movement mechanics (wall kicks, dashes, triple jumps)
- Create sensitive reactions to input nuances
- Enable player expression through character abilities

---

## Technique: Screen Shake

Screen shake provides immediate visual confirmation that the system acknowledges player input, combating the perception of input delay.

### Types of Screen Shake

| Type | Description | Best For |
|------|-------------|----------|
| **Camera Position Shake** | Moves the camera in random or Perlin noise-driven directions | Impacts, explosions, heavy attacks |
| **View Shake** | Moves the entire view rather than the camera itself | Universal feedback, UI-safe |
| **Post-Processing Shake** | Shakes intensity of lens distortion or chromatic aberration | Subtle, stylized effects |
| **UI Shake** | Shakes only UI elements or portions of them | Damage feedback, alerts |

### Implementation Guidelines

```
Parameters:
- Duration: 0.05s - 0.3s (brief is better)
- Intensity: Start strong, decay over time
- Frequency: Higher = more violent, Lower = more ponderous
- Decay: Use an exponential or ease-out curve
- Direction: Random 2D offset or Perlin noise
```

### Screen Shake Best Practices

1. **Use Perlin noise** instead of random values for smoother, more organic shake
2. **Always decay** — shake should diminish over time, never constant
3. **Scale to impact** — bigger events get stronger/longer shakes
4. **Allow players to reduce or disable** screen shake (accessibility)
5. **Never shake during precision input** — pause shake during aiming or platforming sections
6. **Layer multiple shakes** — use additive blending for simultaneous effects

### Trauma-Based Shake System

A common approach is the "trauma" system:
1. Maintain a `trauma` value (0 to 1)
2. Add trauma on impact events (e.g., +0.3 for a hit, +0.8 for an explosion)
3. Each frame, compute `shake = trauma * trauma` (quadratic for better feel)
4. Apply random offset: `offset = maxOffset * shake * random(-1, 1)`
5. Decay trauma each frame: `trauma = max(0, trauma - decayRate * deltaTime)`

---

## Technique: Hit Stop (Freeze Frame)

Hit stop is a brief pause in the game simulation at the moment of impact. The game freezes for a fraction of a second when you hit, shoot, or knock back an enemy, allowing the player to feel the weight and damage of the attack.

### How It Works

1. On impact, set `Time.timeScale = 0` (or near-zero)
2. Wait for a very short duration (typically 0.03s to 0.15s)
3. Restore `Time.timeScale = 1`

### Duration Guidelines

| Action | Duration | Notes |
|--------|----------|-------|
| Light attack | 0.02s - 0.05s | Barely noticeable but adds weight |
| Heavy attack | 0.05s - 0.10s | Clear pause, satisfying impact |
| Critical hit | 0.08s - 0.15s | Dramatic, emphasizes power |
| Kill / Death | 0.10s - 0.20s | Maximum dramatic effect |
| Boss death | 0.15s - 0.30s | Can be longer for cinematic effect |

### Implementation Approaches

**Approach 1: TimeScale Manipulation**
- Set `Time.timeScale` to 0 or near-zero
- Use `WaitForSecondsRealtime` for the delay (unaffected by timeScale)
- Simple but affects ALL game systems

**Approach 2: Selective Freeze**
- Pause only specific entities (attacker and target)
- Disable their Update logic temporarily
- More control, does not affect unrelated systems

**Approach 3: Animation Speed**
- Set animator speed to 0 at the impact frame
- Resume after the freeze duration
- Only affects visual animation, not game logic

### Critical Warnings

- Durations exceeding 0.15 seconds drastically decrease player satisfaction
- Hit stop must feel instantaneous — it enhances impact, not interrupts flow
- Never apply hit stop to rapid-fire attacks (machine guns, rapid combos)
- Scale hit stop duration to attack significance

---

## Technique: Flash Effects

Visual flashes on hit provide instant feedback that an attack has connected.

### Types of Flash Effects

#### White Flash (Damage Flash)
- Briefly tint the hit entity white/bright for 1-3 frames
- Implementation: Swap material to a white/emissive material, then swap back
- Alternative: Use a shader with a `_FlashAmount` parameter (0 to 1)

#### Color Flash
- Flash red for damage, green for healing, blue for shield hits
- Use color to communicate damage types
- Overlay or multiply blend mode

#### Impact Flash (VFX Sprite)
- Spawn a bright flash sprite at the point of impact
- Scale up quickly, fade out rapidly (0.05s - 0.15s)
- Use additive blending for glow effect

#### Screen Flash
- Brief full-screen white or colored overlay
- Very short duration (1-3 frames)
- Use for massive impacts, explosions, lightning

#### Invincibility Flash
- Rapidly toggle sprite visibility or alpha
- Common pattern: visible for 2 frames, invisible for 2 frames
- Communicates invincibility frames (i-frames) to the player

### Flash Implementation Tips

1. Keep flashes extremely brief (1-5 frames at 60fps)
2. Layer with other effects (shake + flash + particles)
3. Use emission/HDR colors with bloom for glow effect
4. Ensure flashes are visible against any background
5. Provide options to reduce flash intensity (photosensitivity accessibility)

---

## Technique: Camera Effects

### Camera Zoom / Punch

- Brief zoom-in on impact, then return to normal
- Emphasizes the moment of contact
- Can combine with slow-motion for cinematic kills

### Camera Kick / Recoil

- Camera briefly moves in the direction opposite to the attack
- Returns smoothly to original position
- Simulates physical recoil from force

### Camera Follow with Lag

- Camera follows the player with slight delay using Lerp/SmoothDamp
- Creates a sense of speed and momentum
- Tighten follow during precision moments, loosen during action

### Dynamic FOV

- Increase FOV when moving fast (dash, sprint)
- Decrease FOV when aiming or focusing
- Creates a visceral sense of speed changes

### Cinematic Camera

- Slow-motion with dramatic angle on critical kills
- Zoom into finishing blows
- Brief letterboxing for dramatic moments

---

## Technique: Particle Effects

### Impact Particles
- Spawn particles at the collision point
- Direction should radiate outward from impact
- Scale particle count and size to damage/force

### Environment Particles
- Dust on landing
- Sparks on metal collision
- Water splashes
- Wood splinters / debris
- Blood or hit fluid (stylized)

### Trail Particles
- Attach particle trails to fast-moving projectiles and weapons
- Use stretched billboard or trail renderer
- Match color to the attack element (fire, ice, lightning)

### Persistent Particles
- Leave scorch marks, scratches, or residue
- Slowly fade over time
- Creates a sense of permanence and impact history

---

## Technique: Slow Motion (Bullet Time)

### When to Use
- Critical hits or kills
- Dodge/parry moments
- Boss phase transitions
- Near-death moments

### Implementation

1. Reduce `Time.timeScale` to 0.1 - 0.3
2. Duration: 0.2s - 1.0s (real time)
3. Ease in and ease out of slow motion (never snap)
4. Keep audio pitch-shifted or use dedicated slow-mo sound effects
5. Apply post-processing (slight desaturation, vignette)

---

## Technique: Knockback and Recoil

### Knockback
- Push the hit entity away from the attacker
- Distance and speed proportional to attack power
- Apply easing (fast start, slow stop) for weight
- Can interact with physics or be animation-driven

### Squash and Stretch
- Borrowed from animation principles
- On impact: briefly squash the hit entity (compress)
- On launch: stretch in the direction of movement
- On landing: squash on contact, then return to normal
- Example: Celeste — Madeline stretches vertically when jumping, squashes on landing, hair follows with delay, dust forms on the ground

### Recoil Animation
- Attacker briefly recoils backward on heavy attacks
- Weapon kick animation on firing
- Adds weight to the attack action

---

## Technique: Sound Design for Game Feel

### Layered Audio Feedback
- **Impact sounds** — Meaty, full-bodied audio for hits
- **Whoosh sounds** — Movement/swing audio before impact
- **Reaction sounds** — Enemy pain/death vocalizations
- **Environmental sounds** — Surface-dependent impact sounds

### Sound Variation
- Always have 3-5 variations of each sound effect
- Randomize pitch slightly (plus/minus 10-20%)
- Prevents repetitive audio fatigue

### Audio Priority
- Louder and more prominent for significant events
- Subtle for minor feedback
- Layer multiple sounds for complex moments

### Soundscapes
- Background ambient audio loops that ground the player in the game world
- Should not demand conscious attention
- Support the mood and setting

---

## Technique: UI Feedback and Juice

### Damage Numbers
- Pop out from hit position
- Animate: scale up, float upward, fade out
- Color-code by damage type
- Larger font for critical hits

### Health Bar Effects
- Delayed health bar (white bar chases red bar)
- Shake the health bar on damage
- Flash the bar briefly
- Color change at low health (red pulse)

### Hit Marker / Crosshair Feedback
- Crosshair briefly expands or flashes on hit
- Kill confirmed indicator
- Directional damage indicators

### Screen Overlay Effects
- Blood splatter or vignette at low health
- Directional damage indicators at screen edges
- Brief chromatic aberration on damage

---

## Technique: Post-Processing for Impact

### Chromatic Aberration
- Brief spike on heavy impacts
- Separates RGB channels for a jarring effect
- Duration: 0.05s - 0.2s, then fade back to 0

### Bloom Spike
- Increase bloom intensity briefly on explosions/flashes
- Enhances the brightness of flash effects
- Combine with HDR emission on VFX

### Vignette Pulse
- Darken screen edges on damage taken
- Red-tinted vignette for low health
- Subtle pulse on heartbeat at critical health

### Color Grading Shift
- Brief desaturation on taking damage
- Warm shift for fire, cool shift for ice
- Full desaturation on death/game over

### Radial Blur
- Brief radial blur on explosions or dashes
- Creates a sense of force radiating from a point

---

## Layering Effects: The Complete Hit

A satisfying hit in a game typically layers multiple techniques simultaneously:

1. **Frame 0 (Impact):** Hit stop begins, white flash on enemy, impact particles spawn, screen shake starts, hit sound plays, damage number appears
2. **Frames 1-3:** Flash fades, particles expand, shake continues, knockback begins
3. **Frames 4-8:** Hit stop ends, time resumes, knockback in progress, particles dissipate, shake decays
4. **Frames 9-15:** Enemy recovery animation, shake ends, particles finish, any post-processing effects fade

### Effect Layering Priority (from most to least important)

1. Sound effects (most immediately felt)
2. Animation response (character reaction)
3. Screen shake (camera feedback)
4. Particles (visual flair)
5. Flash effects (emphasis)
6. Post-processing (atmosphere)
7. UI feedback (information)

---

## Accessibility Considerations

Always provide options for players to control game feel intensity:

- **Screen shake intensity slider** (0% to 100%)
- **Flash effect toggle** (for photosensitive players)
- **Screen effects intensity** (reduce post-processing effects)
- **Haptic/rumble toggle** and intensity
- **Hit stop toggle** (some players find it disorienting)
- **Reduce motion** global setting
