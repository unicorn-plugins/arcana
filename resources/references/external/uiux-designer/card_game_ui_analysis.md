# Card Game UI/UX Analysis: Slay the Spire, Balatro, and Hearthstone

> Source: https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/
> Fetched: 2026-03-27

## Overview

This document provides a comprehensive analysis of UI/UX design patterns across three influential card games: Slay the Spire (roguelike deck-builder), Balatro (poker-based roguelike), and Hearthstone (competitive digital CCG). Each game represents a distinct approach to card game interface design, offering valuable lessons for designing Arcana's UI.

---

## 1. Hearthstone: Immersive Physical Design

### Design Philosophy
Hearthstone's senior UI designer Derek Sakamoto stated at GDC 2015 that "our game is UI," highlighting how central interface design is to the gameplay experience. The team designs using **flavor over efficiency**, while maintaining Blizzard's core value of "Gameplay First."

### The Box Metaphor
Hearthstone's interface is structured as a physical box — a game board with little trays for organization and keys to unlock precious goods. Each part of the box is designed to feel like its own distinct place.

### Board Layout
- Sacrifices nearly half the board to fantasy elements ("The Box")
- Uses arc-shaped "Hero Corners" protecting central heroes
- Implements a **7-minion limit** (imposed by UI constraints — the board literally cannot fit more)
- Follows **left-to-right temporal progression**: past (play history) to present (board state) to future (resources/mana)
- Condenses board-placed cards to reduce information overload

### Card Design: Digital Optimization
- **Mana cost, health, and attack values are extremely visible**, popping outside the frame of the cards
- Cards are not bound to their rectangular frame for a generous display
- Eliminates card descriptions on the board (shown via hover tooltips)
- Provides generous spacing between interactive elements
- Hover state replaces the card with a larger, more readable version

### Physical Feel in Digital Design
Making Hearthstone feel physical was an early development goal implemented through:
- Art direction that mimics wooden boards, stone textures, metal elements
- Animation that simulates weight and momentum in card movements
- Sound design (card slam, page turn, coin jingle) that reinforces tactile sensation
- Interactive board elements (clickable objects outside the play area)

### Cross-Platform Adaptation
The phone version required a thorough review of interface interaction mechanisms:
- Optimized touch targets for thumb-based interaction
- Simplified information display while preserving gameplay depth
- Maintained the same UX philosophy across desktop and mobile

### Key Takeaway for Arcana
Hearthstone proves that investing heavily in UI atmosphere and physical feel creates engagement that transcends the card mechanics themselves. The "UI IS the game" philosophy is worth adopting.

---

## 2. Slay the Spire: Functional Clarity for Complex Systems

### Interface Overview
Slay the Spire's interface must communicate complex roguelike systems (deck building, relics, potions, map navigation, combat) while maintaining clarity during fast-paced decision-making.

### UX/UI Analysis: Key Pain Points (from ~50 player reviews)
- Poor UI clarity causing battle confusion
- Excessively small shop interface elements
- Difficulty comprehending character abilities at a glance
- Information hierarchy issues across multiple screens

### Card Interaction Design
- Cards snap to center when hovered (not dragged from position)
- Smoothed card movement follows the cursor with slight lag
- Hand of cards uses a fan arc layout with overlapping
- Drag-to-play mechanic with target selection for targeted cards
- Energy cost prominently displayed in the top-left of each card

### Character Selection Screen Issues & Solutions
1. **Pentagon Ability Visualization**: Geometric pentagon shape displays character abilities simultaneously, helping players quickly grasp strengths and weaknesses without reading extensive text
2. **Navigation Button Repositioning**: Move Back and Embark buttons to the left side, reducing unnecessary user movements and cognitive load
3. **Image-Based Selection with Hover Effects**: Replace text-only buttons with character image representations featuring dynamic hover states

### Battle Screen Design
Two primary organizational improvements for interface clutter:
1. **Bag Icon for Relic Management**: A bag icon simplifies the review process for character relics by creating a cleaner, less cluttered display while maintaining accessibility through hover animations
2. **Vertical Effect Organization**: Organizing buff/debuff effects vertically on both sides of the screen distinguishes player and enemy statuses clearly and reduces combat confusion

### Shop Interface
Three modifications improve item discovery and selection:
1. **Item Categorization**: Organize cards, relics, and potions into logical categories
2. **Simplified Background**: Remove distracting visual elements so item descriptions dominate the visual hierarchy
3. **Enlarged Item Sizes**: Increase selectable area and visual prominence for better accessibility

### Information Architecture
- Top bar: Floor number, gold, potion slots
- Center: Enemy display with intent icons, HP bars
- Bottom: Player hand in arc layout
- Left sidebar: Draw pile count
- Right sidebar: Discard pile count
- Persistent: Relic bar, energy display

### Key Takeaway for Arcana
Slay the Spire demonstrates the critical importance of information hierarchy in complex systems. Buff/debuff clarity, relic visibility, and card readability are constant challenges that must be solved through deliberate layout decisions.

---

## 3. Balatro: Maximum Juice, Minimal Visual Complexity

### Art Direction: Retro CRT Aesthetic
Balatro does not rely on high-fidelity modeling or flashy visual effects. Instead it constructs a highly recognizable "last-century arcade retro" aesthetic:
- **CRT Distortion**: Distortion effect applied to UI edges mimics early Cathode-Ray Tube monitor curvature
- **Scanlines**: Replicates strobe effects and horizontal scanline characteristics of early television screens
- **Pixelation**: UI elements maintain distinct pixelation matching low-resolution equipment characteristics

### Card Design & Material Feedback
Over 150 Joker cards feature thematic alignment between visuals and mechanics:
- **Thematic Resonance**: Gros Michel banana card has 1/6 destruction chance (reflecting historical Panama disease); Cavendish has 1/1000 odds (referencing disease resistance)
- **Material-Based Feedback**: Cards use distinct textures — Gold (income generation), Glass (fragile high-multiplier), Foil, Negative, Steel, and Stone variants
- **Dynamic Lighting**: Materials display realistic, dynamic lighting changes on hover

### Information Architecture
The interface employs sophisticated spatial strategies:
- **Zone Layout**: Information (left), Interaction area (bottom), Status (top)
- **Dynamic Backgrounds**: Colors shift during Boss Blinds or Booster Pack openings as visual anchors without intrusive UI popups
- **Progressive Disclosure**: Tooltips appear on hover, maintaining an extremely clean interface while preserving flow state
- **Color Psychology**: Dark green casino-table background highlights saturated Joker cards through contrast

### Interactive Feedback & Microinteractions (Juice)
The scoring and settlement phase delivers high-density sensory stimulation:
- **Screen Shake**: Intensifies with scoring magnitude
- **Card Flip Animations**: Satisfying reveal timing
- **Exponentially Jumping Numbers**: Score counters accelerate upward
- **Rising Fire Effects**: Visual escalation for big scores
- **Synchronized Audio**: Jump frequency of numbers matches background audio pitch
- **Physical Inertia**: Card rearrangement simulates push on adjacent cards
- **Magnetic Damping**: Snap-into-place feel when cards settle

### Card Hover Effects
Balatro's hover effect on cards is the exemplary "UI juice" — cards tilt and shimmer with holographic effects, making the simple act of hovering over cards inherently satisfying. Cards drag from where they are clicked (unlike Hearthstone/StS which snap to center).

### Speed Control
The game provides a global speed adjustment function, allowing players to compress waiting animations. This shortens the feedback loop for receiving positive reinforcement while respecting player agency.

### Key Takeaway for Arcana
Balatro proves that "juice" (animation, sound sync, screen shake, particle effects) transforms functional UI into an emotionally engaging experience. Even with minimal art complexity, dense microinteractions create satisfaction.

---

## 4. Cross-Game UI Pattern Analysis

### Card Layout Patterns

| Pattern | Hearthstone | Slay the Spire | Balatro |
|---------|------------|-----------------|---------|
| Hand Layout | Arc fan | Arc fan | Horizontal row |
| Card Hover | Enlarge + center | Snap to center + enlarge | Tilt + holographic |
| Card Play | Drag to board | Drag to target | Click to select |
| Board State | Persistent minions | Temporary (per combat) | N/A (poker hands) |
| Info Density | Medium | High | Low |

### Information Hierarchy Strategies

| Strategy | Hearthstone | Slay the Spire | Balatro |
|----------|------------|-----------------|---------|
| Primary Info | Board state | Card hand + enemies | Current hand + jokers |
| Secondary Info | Hand, mana | Relics, potions, energy | Score, multiplier, chips |
| Tertiary Info | History, opponent hand | Draw/discard piles | Shop, deck stats |
| Disclosure | Hover tooltips | Hover + right-click detail | Hover tooltips |

### Common Design Principles

1. **Progressive Disclosure**: All three games hide detailed information behind hover/click interactions to reduce visual clutter
2. **Spatial Consistency**: Critical gameplay elements maintain fixed screen positions across all states
3. **Visual Feedback Loops**: Every player action produces immediate visual and audio response
4. **Color Coding**: Card rarity/type distinguished through consistent color systems
5. **Readable at a Glance**: Key stats (cost, damage, HP) are always visible without interaction

---

## 5. Design Recommendations for Arcana

### Layout Architecture
- Establish clear zones: hand area (bottom), play field (center), status/info (top and sides)
- Use consistent spatial mapping so players build muscle memory
- Implement progressive disclosure — show summaries by default, details on hover

### Card Component Design
- Make key stats (cost, power, type) visible at all sizes
- Use color coding for card types/elements with secondary indicators (icons, shapes) for accessibility
- Design cards that look good at multiple scales (hand, board, zoomed)

### Interaction Design
- Implement hover-to-preview with smooth transitions
- Add satisfying drag interactions with physics-based feedback
- Provide clear targeting indicators for card effects
- Include undo/cancel affordances for card plays

### Feedback & Juice
- Add screen shake scaled to effect magnitude
- Synchronize visual animations with audio cues
- Implement number counters with satisfying interpolation
- Add card material effects (foil, glow) for rarity distinction
- Include subtle idle animations to make the board feel alive

### Performance Considerations
- Pool card UI objects rather than instantiating/destroying
- Use sprite atlases for card components
- Implement LOD for card detail based on zoom level
- Cache tooltip content to avoid per-frame regeneration

---

## References

- GDKeys: Card Games UI Design of Fairtravel Battle - https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/
- Slay the Spire UX/UI Redesign (Jinyi) - https://medium.com/@n01578837/final-deliverable-632cfc09e673
- Balatro Design Analysis (cccChoice) - https://medium.com/@yyh19971004/balatro-design-analysis-visual-packaging-and-interactive-feedback-cc6fa6a65370
- GDC Vault: Hearthstone Immersive UI - https://gdcvault.com/play/1022036/Hearthstone-How-to-Create-an
- Game Developer: Designing Hearthstone UI - https://www.gamedeveloper.com/design/video-designing-an-immersive-user-interface-for-i-hearthstone-i-
- Interface In Game: Slay the Spire - https://interfaceingame.com/games/slay-the-spire/
- Game UI Database: Balatro - https://www.gameuidatabase.com/gameData.php?id=1935
- UiCard (Unity card game UI framework) - https://github.com/ycarowr/UiCard
