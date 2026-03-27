# Game Design Document (GDD) Writing Guide

> Source: https://gamedevbeginner.com/how-to-write-a-game-design-document-with-examples/, https://document360.com/blog/write-game-design-document/
> Fetched: 2026-03-27

## What is a Game Design Document?

A Game Design Document (GDD) is a detailed plan that outlines how your game will work, look, and feel — covering gameplay mechanics, narrative structure, art direction, monetization strategies, and more. It serves as the central reference for the entire development team.

A GDD is a **living document**, not meant to be carved in stone on day one. Your game will change as you build it, and your GDD should change along with it.

## GDD Structure Template

### 1. Title Page & Overview

```
Game Title: [Name]
Genre: [e.g., 2D Roguelite Turn-based Strategy Card Game]
Platform: [e.g., PC (Steam)]
Target Audience: [e.g., 20-30대 카드/로그라이크 게이머]
Elevator Pitch: [1-2 sentences describing the core experience]
Unique Selling Point (USP): [What makes this game different?]
```

### 2. Game Concept
- Core fantasy: What is the player's power fantasy?
- Core loop: What does the player repeatedly do?
- Meta loop: What keeps the player coming back?
- Tone & mood: Visual and emotional direction
- Reference games: Similar games and what you're borrowing/differentiating

### 3. Gameplay Mechanics

#### Core Mechanics
- **Primary mechanic**: The main action (e.g., card-based combat)
- **Secondary mechanics**: Supporting systems (e.g., deck building, augmentation)
- **Progression**: How the player grows stronger
- **Fail state**: What happens when the player loses

#### System Design Documents
Each major system should have its own sub-document:

| System | Contents |
|--------|----------|
| Combat System | Turn structure, damage formula, targeting |
| Card System | Deck composition, draw mechanics, synergies |
| Economy System | Resources, costs, rewards |
| Progression System | Leveling, upgrades, unlocks |
| AI System | Enemy behavior, difficulty scaling |

### 4. Story & World

- **Setting**: Time period, location, culture
- **Main narrative**: Story synopsis, act structure
- **Characters**: Profiles with motivations and arcs
- **Factions**: Groups and their relationships
- **Lore**: Background world-building

### 5. Art Direction

- **Visual style**: Art references, mood boards
- **Color palette**: Primary and secondary colors
- **Character art specifications**: Proportions, style guide
- **Environment art specifications**: Tile sets, parallax layers
- **UI art specifications**: HUD, menus, icons

### 6. Audio Direction

- **Music style**: Genre, instrumentation, mood per area
- **SFX design**: Categories and quality targets
- **Voice acting**: If applicable, character voice profiles
- **Adaptive audio**: How music responds to gameplay

### 7. Technical Specifications

- **Engine**: Unity, Unreal, Godot, etc.
- **Target specs**: Minimum/recommended hardware
- **Architecture**: Data management, save system
- **Networking**: If applicable, multiplayer architecture
- **Pipeline**: Art-to-engine workflow

### 8. UI/UX Design

- **Screen flow**: Navigation map between all screens
- **HUD layout**: In-game interface elements
- **Menu structure**: Main menu, settings, inventory
- **Tutorial design**: How the player learns
- **Accessibility**: Color blind support, font sizes, controls

### 9. Monetization

- **Business model**: Premium, F2P, DLC
- **Pricing strategy**: Base price, regional pricing
- **DLC plan**: Post-launch content roadmap

### 10. Production Plan

- **Team structure**: Roles and responsibilities
- **Milestones**: Pre-production → Alpha → Beta → Gold
- **Timeline**: Sprint schedule with deliverables
- **Risk register**: Known risks and mitigation

## Best Practices

### Do's
- **Keep it updated**: Review and revise regularly
- **Use visual aids**: Flowcharts, wireframes, mockups
- **Write collaboratively**: Involve the whole team
- **Be specific about mechanics**: Use formulas, not vague descriptions
- **Version control**: Track changes with dates and authors

### Don'ts
- Don't write a novel — be concise
- Don't describe implementation details (that's for TDD)
- Don't lock in every detail before prototyping
- Don't forget the player's perspective

## Document Formats

| Format | Pros | Cons |
|--------|------|------|
| Google Docs | Collaborative, accessible | Limited structure |
| Notion | Database features, linked pages | Learning curve |
| Markdown (Git) | Version control, developer-friendly | Less visual |
| Confluence/Wiki | Structured, searchable | Overhead for small teams |

## Example: System Design Sub-Document

```markdown
# Combat System Design

## Overview
Turn-based card combat with 3-member party vs enemy group.

## Turn Structure
1. Player draws 6 cards from 18-card deck
2. Player plays cards using cost system (max 10, +3/turn)
3. Enemy acts in ID order with random skill selection

## Damage Formula
Final Damage = Base × (1 + ATK%) × Skill Multiplier - Target DEF

## Status Effects
| Effect | Duration | Stacking |
|--------|----------|----------|
| ATK Up | 3 turns | Additive |
| DEF Down | 2 turns | Additive |
```

## Updating the GDD

1. **Weekly reviews**: Check GDD matches current build
2. **Changelog**: Maintain a dated change log at the top
3. **Owner per section**: Assign responsibility for each chapter
4. **Prototype-first**: Update GDD after playtesting, not before
