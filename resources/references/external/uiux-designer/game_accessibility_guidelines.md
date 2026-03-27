# Game Accessibility Guidelines: WCAG for Games & Color Blind Support

> Source: https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
> Fetched: 2026-03-27

## Overview

This document compiles game accessibility guidelines from the Xbox Accessibility Guidelines (XAGs), Microsoft's Making Games Accessible documentation, and the Game Accessibility Guidelines community resource. It covers visual accessibility, color blind support, auditory accessibility, motor accessibility, cognitive accessibility, and implementation best practices for inclusive game design.

---

## 1. Why Game Accessibility Matters

### Player Base Impact
- 19% of people in the United States have some form of disability
- An estimated 14% of adults in the US have difficulty reading
- An estimated 10% of males have some form of color vision deficiency
- Cataracts (which affect color perception) are even more common than color blindness

### Inclusive Design Principle
Disability is defined as "a mismatch between the needs of the individual and the service, product or environment offered." Anyone can experience a disability, whether it is a long-term medical condition or a short-term situational circumstance (playing in a bright room, holding a baby, noisy environment).

### Business Case
Accessibility features often benefit all players. Subtitles were driven by localization needs but became popular with all gamers. Controller remapping was an accessibility feature that became a standard convenience. Making a game more accessible results in a better game for everyone.

---

## 2. Xbox Accessibility Guidelines (XAGs) Overview

The XAGs are a set of best practices developed in partnership with industry experts and the Gaming & Disability Community (Version 3.2, June 2023).

Each XAG contains:
- **Goal**: Desired impact of proper implementation
- **Overview**: Introduction to affected player groups
- **Scoping Questions**: Help developers identify relevant game elements
- **Implementation Guidelines**: Prescriptive guidance for minimum accessible components
- **Potential Player Impact**: List of affected disability types
- **Resources and Tools**: External articles, videos, and tools

---

## 3. Visual Accessibility

### XAG 101: Text Display
- Select simple, readable fonts
- Provide sufficiently large font sizes (or adjustable font size options)
- Create high contrast between background and font color
- Use strong outlines and shadows for text
- Provide dark background overlays for captions with toggle options
- Maximum 38 characters per line, 2-3 lines at a time for subtitles

### XAG 102: Contrast
- Ensure sufficient contrast ratios between foreground and background elements
- Provide high-contrast mode options
- Test with various display settings and viewing distances
- Apply WCAG contrast ratio guidelines (4.5:1 for normal text, 3:1 for large text) as a baseline

### XAG 103: Additional Channels for Visual and Audio Cues
**Goal**: Express visual and audio cues using multiple sensory methods to ensure key information is perceivable by all players.

**Core Principle**: When cues are provided through multiple sensory methods, relying on sight or hearing alone is no longer a requirement for success.

---

## 4. Color Blind Support (Detailed)

### Types of Color Vision Deficiency
- **Deuteranopia**: Reduced sensitivity to green light (most common)
- **Protanopia**: Reduced sensitivity to red light
- **Tritanopia**: Reduced sensitivity to blue/yellow light
- **Achromatopsia**: Complete inability to perceive color (rare)
- **Cataracts**: Acquired condition affecting color perception and brightness

### Core Principle
**Color alone should never be the sole method of communicating information.** Color must always be supplemented with at least one additional signifier.

### Supplementary Signifiers
- **Text labels**: Provide verbal context for what a symbol represents
- **Symbols and shapes**: Quickly express and reinforce information (e.g., exclamation point for "alert")
- **Patterns**: Distinguish elements beyond color (e.g., striped vs. solid fill)
- **Size/position differences**: Spatial differentiation between element types
- **Icons**: Universal signifiers that transcend color perception

### Implementation Guidelines

#### Color Presets
Offer optimized palette schemes for common types:
- Deuteranopia preset
- Protanopia preset
- Tritanopia preset
- High Contrast Mode
- **Ideally, also offer free choice of color** so players can select specific colors that are most visible and differentiable for them

#### Best Practices
1. Use color combinations that can be differentiated by red/green color blind users:
   - **Colors that appear similar**: All shades of red and green, including brown and orange
   - **Colors that stand out**: Blue and yellow
2. Do not rely solely on color to communicate or distinguish game objects — use shapes and patterns as well
3. Combine presets with free color selection for maximum flexibility
4. Use a color blind simulator to test designs (e.g., Color Oracle)

#### What NOT to Do
- **Avoid full palette filters**: Applying a complete game recoloring is unpopular with colorblind gamers, alters unrelated elements, damages aesthetics, and only addresses pre-designed conditions
- **Avoid relying on "colorblind mode" as an afterthought**: Design with accessibility from the start

#### Examples of Proper Implementation
- **Grounded (Obsidian)**: Uses color + shape + iconography + text labels together. Missing ingredients are shown with red color, a warning triangle symbol, AND "Missing ingredients" text
- **Call of Duty: Black Ops Cold War**: Allows players to choose the color of each map icon category (allies, enemies, party, self) independently
- **Forza Horizon 4**: Provides Deuteranopia, Protanopia, Tritanopia presets plus High Contrast Mode
- **Sea of Thieves**: Locked items are grayed out AND have a lock symbol
- **Forza Horizon**: Unavailable menu elements are grayed out with "Not available" text label and lock symbol

#### Testing Tools
- **Color Oracle**: Free color blind simulator (deuteranopia, protanopia, tritanopia)
- **Colour Contrast Analyser (CCA)**: Tests contrast ratios
- **Unreal Engine**: Built-in color blindness simulation tools
- **Important**: Simulation tools should NOT replace testing with actual colorblind players

---

## 5. Multisensory Communication

### Visual Options
1. **Text**: Labels that provide verbal context for symbols or elements
2. **Symbols and shapes**: Combined with text labels for quick recognition
3. **Color**: As reinforcement (never as sole indicator)
4. **On-screen elements**: Damage indicators, directional markers, health bars

### Audio Options
1. **Spatial audio**: Direction and distance information (e.g., Killer Instinct's stereo-panned attack cues)
2. **Audio cues**: Pings, bells, notifications for events (e.g., new objectives)
3. **Distinct sound design**: Unique sounds for different objects and events

### Haptic Options
1. **Haptic rumbling patterns**: Alert players of visual/audio information
2. **Important**: Always use haptics in conjunction with at least one other cue type (not all devices support haptics)

---

## 6. Auditory Accessibility

### Subtitles and Closed Captions
- Select simple, readable fonts
- Provide sufficiently large and adjustable font sizes
- Create high contrast between text and background
- Use dark background overlays with toggle options
- Maximum 38 characters per line, 2-3 lines displayed at a time
- Differentiate who is speaking (e.g., "Daniel: Hi!")
- Provide options for how much sound information is displayed

### Sound Design
- Use 3D/spatial audio cues for directional information
- Separate volume controls for music, speech, and sound effects
- Design speech that provides meaningful information
- Ensure speech is spoken at reasonable rate with rate control
- Provide visual representations of important audio cues

### Game Chat Transcription
- Text-to-Speech and Speech-to-Text functionalities as options
- Allow non-microphone users to type and have messages converted to voice
- Allow hearing-impaired users to read transcribed voice messages

---

## 7. Motor Accessibility

### Fully Mappable Controls
- Allow complete remapping of all controls to any input
- Support custom controllers (e.g., Xbox Adaptive Controller)
- Include remapping directly in the game (don't rely on platform-level remapping alone)
- Support alternative input methods

### Input Flexibility
- Support single-hand play when possible
- Provide options to replace rapid/repeated button presses with holds or toggles
- Allow adjustable timing for time-sensitive inputs
- Support multiple input device types simultaneously

### Difficulty Options
- Provide wider selection of difficulty levels
- Consider accessibility-specific difficulty modifiers (separate from game difficulty)
- Allow granular adjustments (combat difficulty, puzzle timing, etc.)

---

## 8. Cognitive Accessibility

### Clarity and Simplicity
- Provide clear, consistent navigation patterns
- Use familiar icons and symbols
- Minimize cognitive load in menus and interfaces
- Offer tutorials and practice modes

### Memory Support
- Provide objective reminders and quest logs
- Include "last played" summaries when resuming saved games
- Display clear status indicators for current progress
- Use consistent information placement across screens

### Reading and Comprehension
- Support adjustable text size
- Use plain language where possible
- Provide audio narration options for menus
- Offer visual/icon-based alternatives to text

---

## 9. Photosensitivity and Epilepsy

### Avoid
- Flashing lights with frequency of 5-30 flashes per second (Hz)
- Flashing image sequences lasting more than 5 seconds
- More than 3 flashes in a single second covering 25%+ of screen
- Moving repeated patterns covering 25%+ of screen
- Static repeated patterns covering 40%+ of screen
- Instantaneous high brightness/contrast changes (including fast cuts) or to/from red
- More than 5 evenly spaced high-contrast repeated stripes

### Best Practices
- Include Flashing On/Off as a setting (default: Off)
- Test with automated tools (e.g., Harding Test, Harding FPA G2)
- Design for breaks between game levels
- Encourage players to take breaks from non-stop play

---

## 10. Accessibility Review Checklist

| Area | Accessibility Features |
|------|----------------------|
| In-game cinematics | Subtitles, captions, photosensitivity tested |
| Artwork (2D/3D) | Color blind friendly, not color-dependent, uses shapes/patterns |
| Start/settings menus | Read-aloud options, remember settings, alt input methods, adjustable font |
| Gameplay | Adjustable difficulty, subtitles/captions, good visual + audio feedback |
| HUD display | Adjustable position, adjustable font size, color blind options |
| Control input | Mappable controls, custom controller support, simplified input option |

---

## 11. Implementation Priority for Card Games

### High Priority (Must Have)
1. **Color + Shape/Icon**: Never use color alone to distinguish card types, rarity, or effects
2. **Text Size Options**: Adjustable font sizes for card text and UI elements
3. **Contrast**: High contrast between card text and backgrounds
4. **Subtitles**: For any voice-over or narrative audio
5. **Remappable Controls**: Full keyboard/controller customization

### Medium Priority (Should Have)
1. **Color Blind Presets**: Deuteranopia, Protanopia, Tritanopia presets
2. **Custom Color Selection**: Free choice for key UI element colors
3. **Screen Reader Support**: Menu narration for visually impaired players
4. **Difficulty Modifiers**: Separate accessibility options from game difficulty
5. **Animation Speed Control**: Let players adjust or skip animations

### Lower Priority (Nice to Have)
1. **Full haptic feedback**: Controller vibration patterns for events
2. **Audio Description**: Narrated descriptions of visual events
3. **One-handed play mode**: Alternative control schemes
4. **Photosensitivity mode**: Reduced flash/shake effects

---

## References

- Xbox Accessibility Guidelines (XAGs) v3.2 - https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
- XAG 103: Additional Channels for Visual and Audio Cues - https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103
- Making Games Accessible (Microsoft) - https://learn.microsoft.com/en-us/windows/uwp/gaming/accessibility-for-games
- Game Accessibility Guidelines (Community) - https://gameaccessibilityguidelines.com/
- Color Usage in Games - https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/
- Color Blindness Accessibility in Video Games (Filament Games) - https://www.filamentgames.com/blog/color-blindness-accessibility-in-video-games/
- Color Oracle (Simulator) - https://colororacle.org/
- Colour Contrast Analyser (CCA) - https://developer.paciellogroup.com/resources/contrastanalyser/
