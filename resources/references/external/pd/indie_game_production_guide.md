# Indie Game Production Pipeline Guide

> Source: https://gdkeys.com/game-development-process/, https://www.gamedeveloper.com/production/goodbye-postmortems-hello-critical-stage-analysis, https://www.glowingeyegames.com/great-post-mortems-for-indie-developers/, https://medium.com/@toxicaliengf/in-search-of-a-better-game-dev-postmortem-process-7b76caae1ff4
> Fetched: 2026-03-27

## 1. Overview

This document compiles production pipeline knowledge, postmortem methodologies, and practical lessons from indie game development. It draws from GDC talks, Gamasutra/Game Developer articles, and real-world indie postmortems to provide a comprehensive production reference for small teams.

---

## 2. Game Development Production Pipeline

### 2.1 Typical Development Timeline

Most studios adopt **2-3 year production cycles** with these phases:

### 2.2 Phase 1: Conception

- **Duration**: Variable (weeks to years)
- **Team Size**: Small, surgical teams
- **Activities**: Explores direction and validates the core promise
- **Ends with**: "Kick-off" meeting
- **Overlap**: Often occurs during previous game's Polish phase

### 2.3 Phase 2: Pre-Production

- **Duration**: Consistent across project scales
- **Focus**: Remains "laser-focused" to avoid becoming early Production

**Three Critical Validations:**
1. **Technical Feasibility** - Team possesses the technical and artistic capabilities required
2. **Fun Factor** - Core gameplay loop proves viable ("Will the game be fun?")
3. **Scope Definition** - Clear scope definition established for Production

### 2.4 Phase 3: Production

- **Duration**: Longest phase (majority of content creation)
- **Primary Challenge**: Scope Creep management
- **Key Rule**: Must continuously trim features to maintain core experience
- **Priority**: Focus on features before content (features carry unknowns and risk)

### 2.5 Phase 4: Polish

- **Duration**: Dedicated 6-month minimum buffer recommended
- **Separation**: Must be separated from Production activities
- **Common Problem**: Often consumed by Production delays
- **Critical for**: Quality launches that meet player expectations

**Common Polish phase mistakes:**
- Treating Polish as a buffer for Production delays
- Cancelling Polish due to unfinished content
- Platform certification conflicts consuming Polish time

---

## 3. Key Deliverables and Milestones

### 3.1 Prototypes / Proof of Concept

Purpose-driven validation tools addressing specific risks:

| Prototype Type | Purpose | Example |
|---------------|---------|---------|
| **Combat system** | Validate core mechanics | In-engine prototype with basic characters and enemies |
| **Progression mechanics** | Test loop engagement | Physical prototypes using cards or board game elements |
| **Art direction** | Validate visual style | Beauty corner - single polished area showcasing final visual direction |
| **Narrative tone** | Test story delivery | Cinematics, visual novels, or dialogue prototypes |

**Key insight**: Match prototype fidelity to validation needs. Physical prototypes (cards, board games) offer fast, cheap iteration. Digital prototypes (Adobe XD, Tabletop Simulator) balance speed with fidelity.

### 3.2 Vertical Slice vs. Horizontal Slice

#### Vertical Slice
- 20 minutes to 1 hour of polished, complete gameplay
- Demonstrates full pipeline from concept to release quality
- Enables investor presentations and public demos
- Proves production feasibility at scale
- **Ideal for 90% of projects**

#### Horizontal Slice
- Entire game represented in rough form
- All systems present but minimal polish
- Tests engagement over extended sessions
- Better for systemic games (deck-builders, engine-builders)
- **Not suitable for external showcase**

### 3.3 Alpha / Feature Complete

- Every feature implemented and testable
- Content remains incomplete or rough
- Occurs approximately 2/3 through Production
- Enables full playthrough testing
- Flags integration issues before Content Complete

### 3.4 Beta / Content Complete

- All features and content finished
- Polish phase begins immediately after
- Supports Beta testing, Friends & Family access
- Identifies engagement failures and balance issues
- Requires aggressive, surgical iteration approach

### 3.5 Release Milestones

| Milestone | Definition |
|-----------|-----------|
| **Content Lock** | All game content finalized; no new content added |
| **Design Lock** | All design systems finalized; no new mechanics |
| **Audio Lock** | All audio finalized |
| **Candidate Build** | Release candidate awaiting platform certification |
| **Gold Master** | Final approved version for manufacturing/distribution |
| **Day-One Patch** | Updates deployed at launch using pre-release window |

---

## 4. Production Pipeline Glossary

| Term | Definition |
|------|-----------|
| **Beauty Corner** | Single polished area showcasing final visual direction (non-playable) |
| **Gym/Test Room** | In-engine spaces for prototyping specific mechanics |
| **FPP** | First Playable Prototype - aggregated prototypes entering Pre-Production |
| **Content/Design/Audio Locks** | Freezing departments to stabilize pre-launch development |
| **Candidate Build** | Release candidate awaiting platform certification |
| **Gold Master** | Final approved version for manufacturing/distribution |
| **Day-One Patch** | Updates deployed at launch using pre-release manufacturing window |
| **Scope Creep** | Uncontrolled expansion of project features beyond original plan |
| **Crunch** | Extended overtime work periods, typically near milestones |

---

## 5. Team Scaling and Workflow

### 5.1 Team Size by Phase

| Phase | Team Size | Focus |
|-------|-----------|-------|
| **Conception** | Minimal surgical team (1-3) | Direction and core promise |
| **Pre-Production** | Small, focused group (3-5) | Constant size regardless of final team |
| **Production** | Gradual growth to full "cruising size" | Content creation at scale |
| **Polish** | Full team, highly agile | Bug fixing, optimization, final quality |

### 5.2 Feature vs. Content Priority

**Critical Rule**: Focus on shipping all Features before shipping all Content. Features carry unknowns and risk; content is more predictable once the pipeline is established.

- Features first: core mechanics, systems, tools, pipeline
- Content second: levels, art assets, audio, narrative content
- This ordering de-risks the project and prevents late-stage redesigns

---

## 6. Risk Management

### 6.1 Primary Production Risks

1. **Scope creep** consuming development time
2. **Feature integration failures** discovered too late
3. **Insufficient polish** creating launch quality issues
4. **Player engagement failures** requiring redesigns
5. **Platform certification** blocking delays
6. **Marketing gaps** - building a game nobody knows about
7. **Monetization misalignment** - wrong business model for the game

### 6.2 Risk Mitigation Strategies

- **Prototype early**: Validate risky assumptions before full production
- **Feature-first development**: Complete all systems before filling in content
- **Protected polish time**: Never borrow from polish phase for production
- **Regular playtesting**: External feedback every 2-4 weeks
- **Scope management**: Maintain a "cut list" of features ranked by importance
- **Pipeline validation**: Vertical slice proves the full pipeline works end-to-end

---

## 7. Postmortem Methodologies

### 7.1 Traditional Postmortem: The "5 Wrongs, 5 Rights" Framework

The classic format from Game Developer Magazine:
- Identify 5 things that went well
- Identify 5 things that went poorly
- Be specific and avoid sugar-coating the negative sections
- Conduct after project completion

**Problems with traditional postmortems:**
- **Memory degradation**: Developers struggle to recall details after months of development
- **Team dispersal**: Key personnel have already moved to other projects
- **Low motivation**: Exhausted team members show minimal enthusiasm for documentation
- **No immediate impact**: Analysis cannot improve the current game
- **Hierarchical intimidation**: Junior team members avoid critiquing senior staff
- **Less than 2%** of developers review postmortems from previous projects

### 7.2 Critical Stage Analysis (CSA)

An alternative to traditional postmortems that provides "a quick, relatively painless process to find out what went right, what went wrong, what needs to be done to fix it, who will do it and by when."

**Advantages over postmortems:**
- **Real-time intervention**: Analysis occurs during development, enabling course correction
- **Accountability**: Explicit assignment of responsibility with defined timelines
- **Contextual accuracy**: Problems documented while details remain fresh
- **Continuous improvement**: Systematic feedback loop prevents repeated mistakes

**Implementation:**
1. Conduct brief analysis at the end of each major milestone
2. Document issues while development continues
3. Assign clear ownership and resolution timelines
4. Enable mid-project corrections
5. Create accountability across all organizational levels
6. Prioritize issues by measurable impact on project outcomes

### 7.3 Structured Team Postmortem Process (Moon Candy Method)

A comprehensive 3-step postmortem methodology proven by a 4-person indie studio:

#### Step 1: Rebuild Project Timeline

- Each team member individually reconstructs the development history
- Review project management tools, Slack histories, documentation, old builds, repository commits
- Organize work into approximately 2-week chunks
- Output: bullet-point timeline document

**Future improvement**: Spend more time during development tracking this info via weekly or semi-weekly surveys so reconstruction is not needed at the end.

#### Step 2: Create Survey Form

**Part 1 (Timeline-Based)** - Repeated for each 2-week period:
- Stress level assessment (numerical rating)
- Roadblock identification and navigation strategies
- Team accomplishments and strengths during the period
- Individual task assignments

**Part 2 (Topic-Based):**
- Goal achievement evaluation (against original project goals)
- Communication tools and methods effectiveness
- Project management and scheduling assessment
- Personal obstacles overcome
- Individual role reflection
- Future-focused goals

**Practical Tip**: Craft all questions beforehand in a separate document. The interface for making a form gets cumbersome on longer forms.

#### Step 3: Group Review Meeting

- Single day-long session (5 hours)
- Question-by-question progression
- Individual response sharing followed by group discussion
- Detailed note-taking throughout

### 7.4 Supporting Tools for Postmortems

- **Project management tool** (Monday.com, Trello, Jira) with time tracking
- **Personal development journal** (simple text file, started early in the project)
- **Communication archive** (Slack/Discord history for reconstructing decisions)
- **Build archive** (saved builds at milestone points for comparison)

### 7.5 Emotional Safety in Postmortems

**Core requirements for productive retrospectives:**
- Quality listening skills across team
- Individual accountability and mutual support
- Blame-free reflection culture
- Psychological safety for honest sharing

**Risks to watch for:**
- Power dynamics inhibiting candid feedback
- Toxicity derailing productive reflection
- Pre-existing team dysfunction (must be addressed before postmortem)

---

## 8. Lessons from Indie Game Postmortems

### 8.1 Case Studies Summary

| Game | Team Size | Platform | Key Lesson |
|------|-----------|----------|------------|
| **Drunk Shotgun** | Solo | Mobile | Marketing and monetization gaps kill good games |
| **Starcom Nexus** | Solo | Steam | Early Access provides a valuable "second launch" sales bounce |
| **Bass Money** | Solo | Steam (free) | Complete journey documentation is invaluable for first-timers |
| **Core Defense** | Solo | Steam | $20K+ week 1, $70K+ year 1 is achievable for solo devs with the right niche |

### 8.2 Common Development Challenges

**Game Design Issues:**
- **Finding the Fun**: Requires iterative testing and player feedback; you cannot design fun in a document
- **Unrealistic Schedules**: Plans frequently change; hope-based estimates fail consistently
- **Testing Gaps**: Bug detection is different from gameplay enjoyment testing; both are needed
- **Balancing Problems**: Developer familiarity creates difficulty calibration errors; fresh eyes are essential
- **Scope Creep**: Endless development without defined finish lines leads to burnout and failure
- **Art Pipeline**: Integration and workflow require serious planning even for small teams

**Marketing and Business Challenges:**
- Building and releasing a game does not mean players will ever find it
- Advertising and PR require budget and expertise separate from development
- Finding publishers or distribution partners presents additional obstacles
- Monetization decisions (sales model, IAP, ads) must be made during early design phases
- Marketing is a fundamentally different skillset from game development

### 8.3 Statistical Reality

- **Success rate**: Approximately 20-25% of indie games achieve financial viability
- **Revenue distribution**: Top 20% of games generate approximately 80% of revenue
- **Success-to-failure ratios**: Range from 1:7 to 1:25 depending on definition of success

**Implication**: Small improvements in process significantly impact sustainability. Systematic postmortem analysis separates sustainable careers from unsustainable ventures.

---

## 9. The Crunch Problem

### 9.1 Industry Context

Chronic overtime is normalized in game development despite clear evidence of its harm:

- **Law of Diminishing Returns** reduces effectiveness after sustained overtime
- **Creativity deteriorates** under extended crunch conditions
- **Health impacts** result from persistent night-shift and overtime schedules
- **High turnover**: Most developers endure 1-2 crunch projects before seeking other employment
- **Innovation deficit**: Exhausted teams resort to feature parity rather than creative problem-solving

### 9.2 Sustainable Alternatives for Indie Teams

- Plan realistic scope from the start (scope down, then scope down again)
- Build in buffer time at every milestone (minimum 20% buffer)
- Practice iterative development: ship the smallest viable version first
- Set hard working hour limits and respect them
- Use crunch only as a last resort, with defined end dates and recovery time
- Track overtime hours to identify systemic scheduling problems

---

## 10. Production Pipeline Quick Reference

### 10.1 Complete Pipeline at a Glance

```
Conception (weeks-months)
  └── Core idea validation
  └── Team formation
  └── Kick-off meeting
       │
Pre-Production (3-6 months)
  └── Prototype core mechanics
  └── Validate fun factor
  └── Define scope
  └── Create vertical slice
  └── Establish art/tech pipeline
       │
Production (12-24 months)
  └── Feature implementation (features first)
  └── Content creation (content second)
  └── Alpha / Feature Complete (at ~2/3 mark)
  └── Beta / Content Complete
       │
Polish (3-6 months)
  └── Bug fixing
  └── Optimization
  └── Platform certification
  └── Balancing and tuning
  └── Final QA pass
       │
Release
  └── Gold Master
  └── Day-One Patch
  └── Launch marketing push
       │
Post-Launch
  └── Monitor player feedback
  └── Critical bug patches
  └── Content updates / DLC
  └── Postmortem / CSA review
```

### 10.2 Milestone Checklist for Small Teams

**Pre-Production Exit Criteria:**
- [ ] Core gameplay loop is fun (validated by external playtesters)
- [ ] Art style is defined and achievable by the team
- [ ] Technical risks are identified and prototyped
- [ ] Scope is documented and agreed upon
- [ ] Production schedule with milestones exists
- [ ] Version control and build pipeline are set up

**Alpha Checklist:**
- [ ] All gameplay features are implemented
- [ ] Full game is playable start to finish (even if rough)
- [ ] No major systems remain unbuilt
- [ ] Performance is acceptable on target platform
- [ ] External playtesting feedback has been incorporated

**Beta Checklist:**
- [ ] All content is in the game
- [ ] All art is at final quality
- [ ] All audio is implemented
- [ ] No known crash bugs
- [ ] Game is ready for extended testing

**Release Checklist:**
- [ ] All critical and major bugs are fixed
- [ ] Performance targets are met on all target platforms
- [ ] Platform-specific requirements are met (Steam, console cert, etc.)
- [ ] Store page and marketing materials are ready
- [ ] Launch marketing plan is in place
- [ ] Day-one patch is prepared if needed

---

## 11. Recommended Reading and Resources

### GDC Talks
- "The Business of Being Indie: A Production Survival Guide" (GDC Vault)
- "Best Practices for Small Studios: Outmaneuver Your Competition" (GDC Vault)

### Articles
- Game Developer Magazine postmortem archives (gamedeveloper.com)
- "Goodbye Postmortems, Hello Critical Stage Analysis" (Game Developer)
- Indie game postmortem compilations (glowingeyegames.com)

### Books
- "Blood, Sweat, and Pixels" by Jason Schreier
- "The Art of Game Design" by Jesse Schell
- "Agile Game Development with Scrum" by Clinton Keith
