# 12 Principles of Animation (Disney Principles for Games)

> Source: https://totter87.medium.com/12-principles-for-game-animation-a9137ef44345
> Additional: https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games
> Fetched: 2026-03-27

## Introduction

The 12 Principles of Animation were developed at Walt Disney Studios and documented by Frank Thomas and Ollie Johnston in their seminal 1981 book "The Illusion of Life: Disney Animation." These principles provide a foundation for creating believable, appealing animation -- but game animation presents unique challenges compared to film and traditional animation.

Game animation must be both artistically interesting and functional within the constraints of games, such as snappy controls and collision systems. While animators train in classical techniques to convey life and expressiveness, games require responsiveness to player input. This guide examines each principle with specific adaptations for interactive media.

---

## Principle 1: Squash and Stretch

**Concept:** Compressing or elongating characters to convey physical reality while maintaining volume. An object appears to compress on impact and stretch during fast movement.

**Purpose:** Creates visual shorthand for physics and can imply material properties (rubber vs. rigid). Maintains the feeling of weight and mass even during extreme deformation.

**Game Challenge:** Extreme deformation creates collision discrepancies between artwork and hitboxes. If a character stretches far beyond its normal bounds, collision detection becomes unreliable.

**Solutions for Games:**
- Keep squash/stretch frames brief to minimize collision issues
- Apply collision only to specific character parts, not the deformed visual
- Use these frames for visual "juice" without affecting core hitbox size
- Consider this a form of player-friendly visual cheating
- In 3D games, extend limbs during fast actions like jumps rather than scaling bones (which is memory-intensive)

**Card Game Application:** Card flip animations can use subtle squash and stretch when cards land on surfaces or when being drawn from a deck, conveying weight and physicality.

---

## Principle 2: Anticipation

**Concept:** A preparatory action that signals an upcoming motion. For example, crouching before jumping, pulling an arm back before throwing, or a brief wind-up before a punch.

**Purpose:** Helps audiences understand and believe character movement. Without anticipation, actions feel sudden and weightless.

**Game Challenge:** Input lag results when anticipation delays player actions. Players expect immediate response to their inputs, and too much wind-up animation feels sluggish.

**Solutions for Games:**
- Combine anticipation with immediate action (squash frame as character leaves ground on jump)
- Design game pacing around windup animations when it serves gameplay (Castlevania's deliberate whip attack)
- Make anticipation part of risk/reward gameplay mechanics
- Reserve full anticipation for NPCs and bosses where it aids readability of incoming attacks
- Use it as a warning signal before enemy attacks (Dark Souls, Metroid Dread model)
- For player characters, use shorter anticipation frames (1-3 frames) or skip them entirely for responsiveness

**Card Game Application:** Cards can have a brief "lift" or glow anticipation before being played, and enemies can telegraph their attacks with visual wind-up cues.

---

## Principle 3: Staging

**Concept:** Using composition and silhouettes to direct audience attention and communicate narrative clearly. Presenting any idea so that it is completely and unmistakably clear.

**Components:**
- **Composition:** Scene framing and camera positioning that convey mood and relationships
- **Silhouettes:** Pose clarity where a blackened character shape remains readable

**Game Challenge:** Players often control the camera, so traditional cinematic staging must adapt to interactive viewpoints.

**Solutions for Games:**
- Design level approaches to important locations with careful environmental composition
- Ensure 2D sprite keyframes have readable silhouettes
- For 3D characters, animate from multiple camera angles to verify pose clarity
- Create visual "weenies" (landmarks) that naturally guide player attention
- Use lighting, color, and scale to establish visual hierarchy
- In UI-heavy games, use staging principles for card layouts and combat readability

**Card Game Application:** Card layouts should clearly communicate game state. Combat staging ensures players can read the battlefield at a glance -- which cards are in play, what's in hand, and what effects are active.

---

## Principle 4: Straight Ahead and Pose-to-Pose

These describe two different animation creation workflows:

**Straight Ahead Animation:** Drawing frames sequentially from first to last without predetermined keyframes. Creates fluid, spontaneous motion. Best for effects, loose cloth, fire, water, and organic reactions.

**Pose-to-Pose Animation:** Establishing keyframes (major poses) first, then filling in breakdowns and in-betweens. Better for structured movements like walks, runs, and planned action sequences.

**Key Terms:**
- **Keyframes:** Major poses containing primary acting and storytelling
- **Breakdowns:** Intermediate poses between keyframes showing the path of action
- **In-betweens:** Frames smoothing the transition between breakdowns

**Game Advantage:** No inherent conflict with games -- this is purely a workflow choice. Game production favors pose-to-pose due to frequent iteration and animation cuts during development.

**Card Game Application:** Card animations (draw, play, discard) benefit from pose-to-pose workflow -- define the key positions (in deck, in hand, on field, in discard) then create smooth transitions between them.

---

## Principle 5: Follow-Through and Overlapping Action

**Concept:** Loosely attached elements (hair, clothing, limbs, accessories) continue moving after the primary motion stops, creating layered rhythms of movement.

**Purpose:** Conveys inertia and physical realism. Prevents characters from looking stilted by ensuring that not everything stops at the same time.

**Game Considerations:** Few limitations, but additional follow-through frames increase file size and may affect gameplay pacing.

**Techniques for Games:**
- **Economic use:** Minimize follow-through frames but maximize their visual impact
- **Entire motion as follow-through:** First frame shows motion's end; remaining frames show the settling/recovery
- **Separate objects:** Effect continues on a distinct visual element while the character regains control faster (similar to Hollow Knight's cape trailing behind)
- **Procedural physics:** Use engine-driven cloth and hair simulation for follow-through without extra animation frames

**Card Game Application:** When a card is played, particle effects and impact visuals can continue after the card reaches its destination. Card hand rearrangement should have overlapping timing -- cards don't all shift simultaneously but ripple into position.

---

## Principle 6: Slow-In and Slow-Out (Ease In / Ease Out)

**Concept:** Animating more frames near keyframes (start and end of movement) to show easing, with fewer frames through the middle of the action.

**Purpose:** Focuses attention on keyframes and creates more natural, less robotic motion. Mimics how real objects accelerate and decelerate.

**Game Adaptation:** Game engines handle tweening and easing curves automatically. Animators must use custom animation curves to control acceleration and deceleration profiles.

**Common Easing Functions:**
- **Ease In:** Slow start, fast finish (acceleration)
- **Ease Out:** Fast start, slow finish (deceleration)
- **Ease In-Out:** Slow start, fast middle, slow finish
- **Linear:** Constant speed (feels mechanical, useful for some effects)

**Constraint:** Limited frame budgets in pixel art may require different timing solutions -- use fewer total frames but place them strategically.

**Card Game Application:** Card movement from hand to play area should ease out (decelerate as it arrives). Card draw should ease in (accelerate away from the deck). UI elements sliding in should use ease-out for a satisfying landing feel.

---

## Principle 7: Arcs

**Concept:** Animating body parts and objects in curved rather than straight-line motions. Nearly all natural movement follows arced paths.

**Purpose:** Mirrors natural joint movement and gravitational physics. Objects thrown follow parabolic arcs. Limbs swing in curves because they rotate around joints.

**Game Status:** No inherent conflict with games -- always apply this principle.

**Application:** Even subtle details benefit when following arced paths rather than linear ones. Projectiles, swinging weapons, jumping characters, and turning heads should all travel in curves.

**Card Game Application:** Cards drawn from a deck should arc upward before settling into the hand. Cards played should follow a curved path to the battlefield, not a rigid straight line. Attack animations should swing in arcs toward targets.

---

## Principle 8: Secondary Action

**Concept:** Additional movements occurring alongside the primary action to add life and personality. These support and enhance the main action without distracting from it.

**Examples:**
- Arm and leg swing during walk cycles
- Fidgeting, breathing, and blinking in idle animations
- Moving gears, wagging tails, flowing hair
- Facial expressions during body movement

**Purpose:** Increases visual interest and communicates character personality. A character who taps their foot while idle feels more alive than one who stands perfectly still.

**Game Application:** No inherent limitations. Incorporate whenever possible within performance budgets. Idle animations are prime opportunities for secondary action.

**Card Game Application:** Cards in hand can have subtle hover animations (floating, pulsing glow). The battlefield can have ambient secondary motion (flickering candles, shifting shadows). Enemy creatures can have breathing or idle fidget animations.

---

## Principle 9: Timing

**Concept:** The number of frames allocated to an action determines its speed and feel. More drawings = slower action; fewer drawings = faster action.

**Game Advantage:** Unlike film locked at 24fps, games can adjust playback speed programmatically without re-animating. Time scale modifications allow a single animation to serve multiple speed contexts.

**Key Techniques:**
- **Animation Smears:** Stretched, rough frames showing motion blur that appear for a single frame. They create strong visual impact despite rough appearance and allow smooth-looking motion with fewer individual drawings.
- **Frame Holds:** Holding a single frame for emphasis or dramatic effect
- **Speed Curves:** Non-linear playback speed within a single animation

**File Size Consideration:** More frames increase game size. Efficiency matters especially in 2D sprite-based games where each frame is a separate image.

**Card Game Application:** Card play timing communicates power -- a powerful spell card might have slower, more dramatic timing, while a quick attack card snaps to the field instantly. Damage numbers should appear with precise timing relative to impact animations.

---

## Principle 10: Exaggeration

**Concept:** Amplifying the other principles themselves rather than functioning as a standalone technique. Exaggeration is about how much to push poses, timing, and expressions beyond strict realism.

**Purpose:** Helps audiences accept animated motion that would look flat if rendered realistically. Animation needs to be "larger than life" to read clearly on screen.

**Game Application:**
- Build "game feel" and "juice" through exaggerated timing, effects, and screen shake
- Different exaggeration levels create different game tones (cartoony vs. grounded)
- Not just about being "visceral" -- subtle exaggeration works for elegant or whimsical games too

**Balance:** Maintain responsiveness and collision safety while pushing poses for visual impact. The game should feel good to play, not just look dramatic.

**Card Game Application:** Card impacts can produce exaggerated screen shake, particle bursts, and damage numbers that scale with power. A high-damage attack should feel dramatically different from a weak one through exaggerated visual feedback.

---

## Principle 11: Solid Drawing (and Design)

**Concept:** Mastery of fundamentals: anatomy, proportion, perspective, and skilled character drawing. Understanding characters as three-dimensional forms even when rendered in 2D.

**Importance:** Foundation for believable, appealing characters. Prevents stiff or disconnected-looking animation.

**Key Considerations:**
- **Avoid twinning:** Over-reliance on symmetrical poses makes characters look robotic
- **Asymmetrical poses:** Suggest three-dimensional presence and natural stance
- **Volume consistency:** Characters should maintain consistent mass and proportion across frames
- **Construction:** Build characters from basic 3D shapes (spheres, cylinders, boxes) before adding detail

**Game Relevance:** Strong foundational drawing skill prevents characters from feeling flat or disconnected from their environment. Even in pixel art, understanding form and volume creates better animations.

**Card Game Application:** Card art should demonstrate solid drawing principles. Character designs on cards need clear silhouettes and appealing proportions. Combat sprites should read well at small sizes with strong construction.

---

## Principle 12: Appeal

**Concept:** Character design that creates connection and conveys personality at a glance. The animated equivalent of "charisma" -- making characters that audiences want to watch.

**Factors:**
- **Predominant shapes:** Circles feel friendly, triangles feel dangerous, squares feel stable
- **Color palettes:** Communicate character alignment and personality
- **Expressive faces:** Even simple expressions create emotional connection
- **Clear emotional communication:** Audiences should understand a character's mood instantly
- **Distinctive silhouettes:** Characters should be recognizable from their outline alone

**Game Advantage:** No restrictions. Appeal comes through character design and animation quality.

**Impact:** Characters with strong appeal generate fan engagement and player attachment, driving community building and franchise loyalty.

**Card Game Application:** Card art and creature designs should have immediate visual appeal. Each card should feel unique and memorable. The overall visual style of the game should be cohesive and inviting.

---

## Historical Context

The principles trace from Winsor McCay's pioneering animation work (1908-1914) through the "rubber hose" era of the 1920s -- characterized by characters with flexible, boneless limbs -- to Disney's rebellion against that style in the 1930s. McCay criticized the industry for making animation "a trade" rather than art.

The Disney studio's systematic development of these principles elevated animation from simple movement to believable performance. Modern works like Cuphead have successfully reclaimed the rubber hose aesthetic while properly implementing all 12 Principles, proving that any style can benefit from these foundational techniques.

---

## Summary: Principles and Game Constraints

| Principle | Game Constraint | Severity |
|-----------|----------------|----------|
| Squash and Stretch | Collision/hitbox mismatch | Medium |
| Anticipation | Input lag / responsiveness | High |
| Staging | Player-controlled camera | Medium |
| Straight Ahead / Pose-to-Pose | None (workflow choice) | None |
| Follow-Through / Overlapping | Frame count / file size | Low |
| Slow-In / Slow-Out | Frame budget in pixel art | Low |
| Arcs | None | None |
| Secondary Action | Performance budget | Low |
| Timing | Frame count / file size | Low |
| Exaggeration | Collision safety | Low |
| Solid Drawing | None (skill-based) | None |
| Appeal | None (design-based) | None |

**Key Takeaway:** Most principles have no inherent conflict with game development. The challenge lies in balancing artistic expression with technical constraints (collision, input responsiveness, file size). Solutions involve collaborating between animators and programmers -- using shorter frame counts, clever timing adjustments, and smart visual tricks rather than abandoning these foundational techniques.
