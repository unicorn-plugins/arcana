# Game Balancing Theory: Probability, Expected Value & Monte Carlo Methods

> Source: gamebalanceconcepts.wordpress.com, blog.userwise.io, boardsandbarley.com, numberanalytics.com, gamedeveloper.com, redblobgames.com
> Fetched: 2026-03-27

---

## 1. Overview

Game balance is the mathematical foundation underlying all game design. As Will Luton states: "Strip away the audio, the visuals and the story and you're left with only numbers." This document covers the essential mathematical frameworks for game balance: probability theory, expected value calculations, curve design, economic systems, and Monte Carlo simulation methods.

---

## 2. Probability Fundamentals

### 2.1 Basic Probability

**Definition**: Probability measures the likelihood of an event occurring, expressed as a value between 0 (impossible) and 1 (certain), or equivalently 0% to 100%.

**Counting Method** (the fundamental approach):
1. Count total possible outcomes
2. Count successful outcomes
3. Divide successful by total

**Example**: Rolling 4+ on a d6 = 3 successes (4, 5, 6) / 6 total = 50%

**Reality Check**: If you sum all possible outcome probabilities, you should get exactly 100%. This is the first validation for any probability calculation.

### 2.2 Expected Value

The single most important concept for game balance:

```
Expected Value = Sum of (Outcome_i x Probability_i) for all i
```

**Simple Example (d6)**:
- Expected value = (1+2+3+4+5+6) / 6 = 3.5

**Loot Table Example**:
| Drop | Probability | Value | EV Contribution |
|------|------------|-------|-----------------|
| Common (100 gold) | 71% | 100 | 71.0 |
| Uncommon (300 gold) | 21% | 300 | 63.0 |
| Rare (2,000 gold) | 7% | 2,000 | 140.0 |
| Legendary (10,000 gold) | 1.5% | 10,000 | 150.0 |
| **Total** | **100%** | | **424.0 gold/drop** |

### 2.3 Independent vs. Dependent Events

**Independent Events** (dice rolls, random number generators):
- Each event has no effect on subsequent events
- To find P(all events happen): multiply individual probabilities
- Example: Two 6s in a row = 1/6 x 1/6 = 1/36

**Dependent Events** (card draws, deck-based systems):
- Each event changes the probability space for subsequent events
- Once a card is drawn, remaining deck probabilities shift
- Example: Drawing 2 specific cards from a 52-card deck involves changing denominators

**Design Implication**: Deck-based randomness (dependent) feels more "fair" to players than dice-based randomness (independent) because streaks self-correct.

### 2.4 The Negation Strategy

Sometimes calculating the inverse is easier:

```
P(at least one success) = 1 - P(zero successes)
```

**Example**: Probability of at least one 6 when rolling 6d6:
- P(no 6s) = (5/6)^6 = 0.335
- P(at least one 6) = 1 - 0.335 = 0.665 (66.5%)

### 2.5 Variance and Standard Deviation

Expected value alone is insufficient for balance. Two systems can have the same EV but wildly different player experiences:

- **Low variance**: Consistent, predictable outcomes (2d6 averages 7, range 2-12, but clusters around 7)
- **High variance**: Swingy, unpredictable outcomes (1d12 averages 6.5, range 1-12, uniform distribution)

**Standard Deviation** measures spread around the expected value. For game balance:
- Lower std dev = more predictable = safer design
- Higher std dev = more exciting = riskier design
- Neither is inherently better; it depends on design intent

---

## 3. Curves: Defining Relationships Between Values

### 3.1 Linear Curves

```
y = mx + b
```

- Proportional relationships where one value increases steadily with another
- Simple to understand but feel predictable and "grindy" to players
- Use case: Basic resource conversion rates

### 3.2 Exponential Curves

```
y = a * b^x
```

- Constantly accelerating growth
- Creates compelling reward sensations (incremental/idle games)
- Dangerous for balance: small parameter changes cause massive outcome shifts
- Use case: Damage scaling, level progression in power-fantasy games

### 3.3 Logarithmic Curves (Diminishing Returns)

```
y = a * log(x) + b
```

- Rapid initial growth followed by diminishing returns
- Natural-feeling progression ("easy to learn, hard to master")
- Use case: Skill ratings, rubber-band mechanics, stat scaling after soft caps

### 3.4 Sigmoid (S-Curve)

```
y = 1 / (1 + e^(-x))
```

- Slow start, rapid middle growth, then plateau
- Models adoption curves and difficulty progression
- Use case: Learning curves, matchmaking confidence, unlock pacing

### 3.5 Step Functions

- Discrete jumps at specific thresholds
- Creates clear "tier" boundaries
- Use case: Level-up systems, rank thresholds, gear tiers

### 3.6 Piecewise Functions

- Combine multiple curve types across different ranges
- Most realistic progression systems use piecewise functions
- Use case: MMO leveling (fast early, slow mid, fast pre-cap, slow endgame)

---

## 4. Game Economy Design

### 4.1 Taps, Sinks, and Pinch Points

**Tap**: Any source that creates a resource (quest rewards, loot drops, crafting)
**Sink**: Any system that consumes a resource (shops, upgrades, consumables)
**Pinch Point**: The sweet spot where supply demonstrates resource utility while remaining scarce enough to maintain player motivation

**Balance Rules**:
- When taps >> sinks: Resources become worthless, players disengage
- When sinks >> taps: Players feel frustrated, can't progress
- Healthy economy: Slight scarcity with periodic abundance

### 4.2 Inflation and Anchor Values

**Intentional Inflation**: Increasing both taps and sinks proportionally lets players feel rewarded while maintaining consistent effort requirements.

**Anchor Values**: A foundation for the entire economy. Examples:
- **Time** (Clash of Clans): All resources derive value from time investment
- **Energy** (mobile games): All actions cost energy, which regenerates over time
- **Gold** (traditional RPGs): Universal medium of exchange

All other resources should be traceable back to the anchor through conversion chains.

### 4.3 Conversion Mechanics

When converting between resource types:
- **Avoid linear exchanges** to maintain strategic diversity
- Use diminishing returns on bulk conversions
- Create different optimal conversion paths for different strategies
- Track all conversion chains to prevent exploits (resource loops)

---

## 5. Card Game Balance Specifics

### 5.1 Equivalent Exchange Principle

The most basic principle in card game design: every card's power should be proportional to its cost.

**Creature Value Formula**:
```
Creature Value = Attack Power + Health
Expected Creature Value at Cost N = baseline + (cost_scaling * N)
```

### 5.2 Mana Curve Design

Cards should be distributed across costs to ensure:
- Early game: Sufficient low-cost options for opening plays
- Mid game: Enough mid-cost cards for sustained tempo
- Late game: High-cost finishers as strategic goals

**Practical Template** (for a 30-card deck):
| Cost | Count | Purpose |
|------|-------|---------|
| 0-1 | 6-8 | Opening plays, combo enablers |
| 2-3 | 10-12 | Core gameplay, tempo |
| 4-5 | 6-8 | Power plays, turning points |
| 6+ | 2-4 | Win conditions, finishers |

### 5.3 RPG Damage Formula Foundations

**Basic Damage Formula**:
```
Damage = (Attack - Defense) * Modifier
```

**More Nuanced Formula**:
```
Damage = BaseAttack * (1 + BonusAttack%) * SkillMultiplier - (Defense * DefenseEfficiency)
Damage = max(Damage, MinimumDamage)
```

**Key Considerations**:
- Always have a minimum damage floor (prevents complete nullification)
- Defense should reduce damage, not eliminate it
- Percentage-based vs. flat reduction creates different scaling curves
- Critical hits multiply damage by a factor (typically 1.5x-2.0x)

### 5.4 Stat Weighting for Unit Balance

Assign numerical values to stats, normalize them, and apply weighting factors:

| Stat | Weight | Rationale |
|------|--------|-----------|
| HP | 1.0 | Baseline stat |
| Attack | 1.5 | Offensive stats slightly premium |
| Defense | 1.2 | Passive benefit, slightly above baseline |
| Speed | 2.0 | Action economy is very powerful |
| Move Range | 2.0 | Positioning advantage is very powerful |
| Special Ability | Variable | Unique effects need case-by-case evaluation |

**Total Budget Formula**:
```
Unit Power Budget = Sum of (Stat_i * Weight_i)
Units at the same tier should have similar total budgets
```

---

## 6. Monte Carlo Simulation Methods

### 6.1 What Is Monte Carlo Simulation?

A computational technique that uses random sampling to obtain numerical results for systems too complex to solve analytically. Named after the Monte Carlo casino in Monaco.

**Core Principle**: Rather than calculating exact probabilities for complex systems, simulate thousands of random outcomes and analyze the statistical distribution.

### 6.2 Mathematical Foundation

**Expected Value via Simulation**:
```
E(X) ≈ (1/N) * Sum(X_i) for i = 1 to N
```

Where N = number of simulation iterations, X_i = outcome of iteration i.

As N approaches infinity, the simulated expected value converges to the true expected value.

### 6.3 Implementation Steps

**Step 1: Define Parameters**
- List all random elements and their probability distributions
- Define constraints and game rules
- Establish what metrics to measure

**Step 2: Build the Simulation Engine**
- Create functions for each random event
- Implement game rules as deterministic logic
- Track all relevant output metrics

**Step 3: Run Iterations (1,000-10,000+)**
- Each iteration = one complete game/encounter/turn sequence
- Record all output metrics per iteration

**Step 4: Analyze Results**
- Calculate: Mean, Median, Mode, Min, Max, Standard Deviation
- Plot distributions: Histograms, box plots, probability density functions
- Identify outliers: What happens in the worst 5%? Best 5%?

### 6.4 Practical Example: Card Game Monte Carlo in Excel

**Deck Shuffling Engine**:
1. Create a table listing all cards with associated values
2. Generate random values for each card using RAND()
3. Use SMALL and VLOOKUP to programmatically sort cards
4. Verify by pressing F9 multiple times

**Deal and Calculate**:
1. Distribute cards following game rules
2. Use VLOOKUP to pull corresponding values
3. Create a "Key" row containing all player data and totals

**Run 1,000 Iterations**:
1. Number rows 1-1,000 below the Key row
2. Data > What-If Analysis > Data Table
3. Excel automatically recalculates all formulas 1,000 times
4. Analyze results with AVERAGE, MIN, MAX, STDEV

### 6.5 Advanced Techniques

**Importance Sampling** (variance reduction):
```
E(f(x)) ≈ (1/N) * Sum(f(x_i) * p(x_i) / q(x_i))
```
Weight samples toward regions of interest rather than sampling uniformly.

**Stratified Sampling**:
- Divide the probability space into strata
- Sample from each stratum proportionally
- Ensures representative coverage of edge cases

**Monte Carlo Tree Search (MCTS)**:
- Dynamically constructed decision trees using randomized evaluations
- Used in game AI (famously: AlphaGo)
- Applicable to balance testing: simulate AI vs. AI with different parameters

### 6.6 Simulation Process Structure

| Stage | Function | Tools |
|-------|----------|-------|
| Initialization | Define parameters and objectives | Spreadsheet / Python setup |
| Sampling | Extract random values from distributions | RAND(), random.random() |
| Evaluation | Calculate outcomes per sample | Game rule logic |
| Analysis | Compute mean, variance, convergence | Statistical functions |
| Application | Inform design decisions | Visualization, reports |

---

## 7. Matchmaking & Competitive Balance

### 7.1 Elo Rating System

**Predicting Match Outcomes**:
```
Expected Score = 1 / (1 + 10^((OpponentRating - PlayerRating) / 400))
```

**Updating Ratings**:
```
New Rating = Old Rating + K * (Actual Score - Expected Score)
```

Where K-factor (typically 32) sets maximum adjustment per match.

**Properties**:
- Self-correcting: Lower-rated players gain more from upsets
- Zero-sum: Total rating in the system remains constant
- Converges: After sufficient games, ratings stabilize

### 7.2 Elo Limitations

- Confusing mathematics reduces player trust
- Ranking losses create disincentives to play
- Poor initial rankings for new players (cold start problem)
- Cannot reward individual performance in team games
- Assumes all games are equally important

---

## 8. Practical Balance Workflow

### 8.1 The Balance Pipeline

```
1. [Theory] Design on paper using expected value calculations
2. [Spreadsheet] Build cost/power budget spreadsheets
3. [Simulation] Run Monte Carlo for edge cases
4. [Prototype] Implement and playtest
5. [Data Collection] Track key metrics from playtests
6. [Analysis] Compare actual vs. predicted outcomes
7. [Iteration] Adjust parameters, repeat from step 2
```

### 8.2 Common Balance Heuristics

1. **The 40/40/20 Rule**: In a balanced game, players should win ~40% of the time, lose ~40%, and have ~20% close/uncertain outcomes
2. **Three Standard Deviations**: If an outcome is more than 3 SD from expected, the system likely has a bug or exploit
3. **Pareto Check**: If 20% of options account for 80% of wins, diversity is insufficient
4. **Minimum Viable Difference**: The smallest change that has a statistically significant effect (prevents over-tuning)

### 8.3 Important Limitations

Monte Carlo and mathematical approaches:
- **Cannot tell you if your game is fun**
- Cannot simulate strategy or human decision-making
- Cannot replace human playtesting
- Identify mechanical imbalances but not experiential problems
- Are tools, not solutions

"Humans are not naturally good at thinking in probability" - this makes mathematical literacy particularly powerful for designers, but also means player perception of fairness often differs from mathematical fairness.

---

## 9. Key Formulas Reference Sheet

### Probability
```
P(A) = favorable outcomes / total outcomes
P(A and B) = P(A) * P(B)                    [independent events]
P(A or B) = P(A) + P(B) - P(A and B)
P(at least one) = 1 - P(none)
```

### Expected Value
```
EV = Sum(outcome_i * probability_i)
EV(multiple events) = Sum(EV(single events))
```

### Variance & Standard Deviation
```
Variance = Sum((outcome_i - EV)^2 * probability_i)
StdDev = sqrt(Variance)
```

### Damage Formulas
```
Basic: Damage = Attack - Defense
Multiplicative: Damage = Attack * (1 - DefenseReduction%)
Hybrid: Damage = (Attack * Multiplier) - FlatDefense
Critical: CritDamage = Damage * CritMultiplier
Expected DPS = BaseDamage * (1 + CritChance * (CritMultiplier - 1)) * AttackSpeed
```

### Economy
```
Inflation Rate = (NewPrice - OldPrice) / OldPrice
Resource Half-Life = time for resource to lose 50% value
Pinch Ratio = TotalSinks / TotalTaps (target: slightly > 1.0)
```

### Elo
```
Expected = 1 / (1 + 10^((Rb - Ra) / 400))
NewRating = OldRating + K * (Score - Expected)
```

---

## 10. Relevance to Arcana Project

For a tarot-themed card game requiring balance:

- **Expected Value calculations** are essential for pricing card effects (each Arcana card should have a balanced EV relative to its cost)
- **Monte Carlo simulation** can test thousands of deck compositions before playtesting
- **Curve design** (exponential, logarithmic, sigmoid) informs how card power scales with game progression
- **Mana curve principles** apply directly to deck construction rules
- **The equivalent exchange principle** ensures Major Arcana (high power) have proportional costs
- **Stat weighting** provides a framework for balancing different card attributes (damage, healing, utility)
- **Variance management**: High-variance effects (tarot reading randomness) need careful EV calibration
