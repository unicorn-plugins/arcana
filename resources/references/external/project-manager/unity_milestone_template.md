# Unity Game Project Milestone Planning Guide

> Source: https://learn.unity.com/course/milestones, https://www.projectmanager.com/blog/milestones-project-management
> Fetched: 2026-03-27

## Overview

Any well-run game project needs a scope, specific milestones, appropriate schedules, and time management so that the greater project can be divided into small, achievable tasks for each member of the team. This guide covers milestone planning specifically for Unity-based game development.

## Standard Game Development Milestones

### 1. Concept / Pre-Production

**Duration**: 1-3 months
**Goal**: Define the game's vision and prove it can be fun

| Deliverable | Description | Owner |
|------------|-------------|-------|
| Game Concept Document | 1-page pitch with core loop | Game Director |
| Game Design Document | Full GDD (living document) | Game Designer |
| Art Bible | Visual style guide, color palette | Art Director |
| Technical Prototype | Proof of core mechanic in Unity | Tech Director |
| Project Plan | WBS, timeline, resource allocation | PM |

**Exit Criteria**: Team agrees on vision, prototype demonstrates core fun

### 2. Vertical Slice

**Duration**: 1-2 months
**Goal**: One complete, polished slice of the game

| Deliverable | Description | Owner |
|------------|-------------|-------|
| Playable Build | 1 complete level/loop with final art | All |
| Core Systems | Combat, UI, progression working | Programmer |
| Final Art Sample | Character, background, effects | Art Team |
| Audio Sample | BGM + SFX for the slice | Sound Director |
| Test Cases | QA plan for the slice | QA |

**Exit Criteria**: Vertical slice is fun and represents final quality

### 3. Alpha

**Duration**: 2-4 months
**Goal**: All features implemented, content partially complete

| Deliverable | Description | Owner |
|------------|-------------|-------|
| Feature Complete Build | All systems functional | Programmer |
| All Stages Playable | Full game flow working | Design Team |
| First Balancing Pass | Initial number tuning | Balance Designer |
| Placeholder Assets OK | Temp art/sound acceptable | Art/Sound |
| Integration Tests | All systems working together | QA |

**Exit Criteria**: Game is playable start to finish (quality varies)

### 4. Beta

**Duration**: 2-3 months
**Goal**: All content complete, focus on polish and balance

| Deliverable | Description | Owner |
|------------|-------------|-------|
| Content Complete Build | All art, sound, text finalized | All |
| Balance Pass 2-3 | Difficulty tuning from playtests | Balance Designer |
| Localization Ready | All strings externalized | Programmer |
| Performance Optimized | Target FPS on min spec | Tech Director |
| Full QA Pass | All test cases executed | QA |

**Exit Criteria**: No critical bugs, balance is acceptable

### 5. Gold Master / Release

**Duration**: 1-2 months
**Goal**: Ship-ready build

| Deliverable | Description | Owner |
|------------|-------------|-------|
| Release Candidate | Final build for submission | Tech Director |
| Platform Certification | Steam store page, achievements | PM |
| Marketing Assets | Trailer, screenshots, press kit | PD |
| Day-1 Patch Plan | Known issues and fixes | QA |
| Post-Launch Roadmap | v1.1, v1.2 content plan | PD |

**Exit Criteria**: Build passes platform certification

## Work Breakdown Structure (WBS)

### WBS Template for Unity 2D Card Game

```
1. Pre-Production
   1.1 Game Design
       1.1.1 Core loop design
       1.1.2 Card system design
       1.1.3 Balance framework
       1.1.4 UI/UX wireframes
   1.2 Technical Setup
       1.2.1 Unity project setup (URP 2D)
       1.2.2 Repository & CI/CD
       1.2.3 Coding standards
       1.2.4 Asset pipeline
   1.3 Art Pre-production
       1.3.1 Art style guide
       1.3.2 Character concept art
       1.3.3 Card layout template
       1.3.4 UI kit design

2. Production - Core Systems
   2.1 Combat System
       2.1.1 Turn manager
       2.1.2 Card draw/play
       2.1.3 Damage calculation
       2.1.4 Status effects
   2.2 Card System
       2.2.1 Card data (ScriptableObject)
       2.2.2 Deck management
       2.2.3 Hand UI (drag & drop)
       2.2.4 Synergy detection
   2.3 Meta Systems
       2.3.1 Node map navigation
       2.3.2 Augmentation system
       2.3.3 Save/Load
       2.3.4 Reincarnation loop

3. Production - Content
   3.1 Characters (per character)
       3.1.1 Art (idle, attack, hit, KO)
       3.1.2 Spine animation setup
       3.1.3 Skill implementation
       3.1.4 Balance tuning
   3.2 Stages (per stage)
       3.2.1 Background art (3 parallax layers)
       3.2.2 Enemy design & art
       3.2.3 Boss design & phases
       3.2.4 Event nodes

4. Polish
   4.1 VFX & Juice
   4.2 Sound Integration
   4.3 Tutorial
   4.4 Performance Optimization
   4.5 Localization

5. Release
   5.1 Steam Integration
   5.2 QA Final Pass
   5.3 Marketing
   5.4 Launch
```

## Sprint Planning Template

### 2-Week Sprint Structure

| Day | Activity |
|-----|----------|
| Mon (Day 1) | Sprint Planning: select backlog items |
| Mon-Fri (Day 1-5) | Development: implement features |
| Mon-Thu (Day 8-11) | Development: continue + integration |
| Fri (Day 12) | Code freeze, internal playtest |
| Mon (Day 13) | Bug fixing from playtest |
| Tue (Day 14) | Sprint Review + Retrospective |

### Sprint Backlog Item Template

```
[CARD-042] Implement Synergy Detection
- Priority: High
- Estimate: 5 story points
- Assignee: Programmer
- Dependencies: CARD-038 (Card Data), CARD-040 (Hand Manager)
- Acceptance Criteria:
  □ Detects 3 synergy types (forward, reverse, mixed)
  □ Highlights synergy-eligible cards in hand
  □ Applies synergy bonus on card play
  □ Unit test coverage > 80%
```

## Tools

| Tool | Purpose | Pricing |
|------|---------|---------|
| Jira | Issue tracking, sprint boards | Free (10 users) |
| Notion | GDD, wiki, task management | Free (small teams) |
| GitHub Projects | Code-integrated task boards | Free |
| Trello | Visual kanban boards | Free |
| Unity Cloud Build | CI/CD for Unity | Per-seat |

## Risk Register Template

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Scope creep | High | High | Strict sprint goals, PO approval |
| Key person dependency | High | Medium | Cross-training, documentation |
| Platform rejection | High | Low | Early Steam review, checklist |
| Balance issues | Medium | High | Early playtesting, data-driven tuning |
| Performance on min spec | Medium | Medium | Regular profiling, target budgets |
