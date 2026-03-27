# Game Programming Patterns: State Machine, Observer, and Command

> Source: https://gameprogrammingpatterns.com/contents.html
> Fetched: 2026-03-27

## Overview

This document covers three essential design patterns for game development, based on Robert Nystrom's "Game Programming Patterns." These patterns solve common architectural problems in game code: managing complex object states, decoupling communication between systems, and abstracting actions into reusable objects.

---

## 1. State Machine Pattern

### The Problem

When implementing character behavior with multiple states (standing, jumping, ducking, diving), naive approaches using Boolean flags quickly become unmaintainable:

```cpp
void Heroine::handleInput(Input input) {
    if (input == PRESS_B) {
        if (!isJumping_ && !isDucking_) {
            isJumping_ = true;
            // Jump...
        }
    }
    else if (input == PRESS_DOWN) {
        if (!isJumping_) {
            isDucking_ = true;
            // Duck...
        }
        else {
            // Dive...
        }
    }
}
```

Problems multiply as features are added: invalid state combinations emerge (jumping while ducking), conditional logic scatters across methods, and each new feature requires additional flags with exponential complexity.

### Finite State Machines (FSMs)

An FSM models an entity with:
- A **fixed set of states** (standing, jumping, ducking, diving)
- A **single current state** at any time
- **Input events** that trigger transitions
- **Transitions** defining which state follows from each input in each state

### Enum-Based Implementation

The simplest approach replaces multiple Boolean flags with a single enum:

```cpp
enum State {
    STATE_STANDING,
    STATE_JUMPING,
    STATE_DUCKING,
    STATE_DIVING
};

void Heroine::handleInput(Input input) {
    switch (state_) {
        case STATE_STANDING:
            if (input == PRESS_B) {
                state_ = STATE_JUMPING;
                yVelocity_ = JUMP_VELOCITY;
                setGraphics(IMAGE_JUMP);
            }
            else if (input == PRESS_DOWN) {
                state_ = STATE_DUCKING;
                setGraphics(IMAGE_DUCK);
            }
            break;

        case STATE_JUMPING:
            if (input == PRESS_DOWN) {
                state_ = STATE_DIVING;
                setGraphics(IMAGE_DIVE);
            }
            break;

        case STATE_DUCKING:
            if (input == RELEASE_DOWN) {
                state_ = STATE_STANDING;
                setGraphics(IMAGE_STAND);
            }
            break;
    }
}
```

This prevents invalid states and groups all behavior for one state together, greatly improving clarity.

### The Gang of Four State Pattern

When states need their own data (e.g., `chargeTime_` for a charged attack), the enum approach hits limitations. The State pattern encapsulates each state's behavior and data in separate classes.

**State Interface:**
```cpp
class HeroineState {
public:
    virtual ~HeroineState() {}
    virtual void handleInput(Heroine& heroine, Input input) {}
    virtual void update(Heroine& heroine) {}
    virtual void enter(Heroine& heroine) {}
    virtual void exit(Heroine& heroine) {}
};
```

**Concrete State:**
```cpp
class DuckingState : public HeroineState {
public:
    DuckingState() : chargeTime_(0) {}

    virtual void handleInput(Heroine& heroine, Input input) {
        if (input == RELEASE_DOWN) {
            heroine.setGraphics(IMAGE_STAND);
            // Transition to standing
        }
    }

    virtual void update(Heroine& heroine) {
        chargeTime_++;
        if (chargeTime_ > MAX_CHARGE) {
            heroine.superBomb();
        }
    }

private:
    int chargeTime_;  // State-specific data
};
```

**Delegation from Main Class:**
```cpp
class Heroine {
public:
    void handleInput(Input input) {
        state_->handleInput(*this, input);
    }

    void update() {
        state_->update(*this);
    }

private:
    HeroineState* state_;
};
```

### Enter and Exit Actions

Rather than duplicating setup code at every transition site, each state implements entry and exit actions:

```cpp
class StandingState : public HeroineState {
public:
    virtual void enter(Heroine& heroine) {
        heroine.setGraphics(IMAGE_STAND);
    }
};

// Transition handling
void Heroine::handleInput(Input input) {
    HeroineState* newState = state_->handleInput(*this, input);
    if (newState != NULL) {
        state_->exit(*this);
        delete state_;
        state_ = newState;
        state_->enter(*this);
    }
}
```

Entry actions consolidate code that would otherwise be duplicated across multiple transitions into the same state.

### Static vs. Instantiated States

**Static States (Flyweight):** If a state has no instance variables, create one shared instance:
```cpp
if (input == PRESS_B) {
    heroine.state_ = &HeroineState::jumping;  // Shared static instance
}
```

**Instantiated States:** For states with their own data, allocate new instances:
```cpp
HeroineState* StandingState::handleInput(Heroine& heroine, Input input) {
    if (input == PRESS_DOWN) {
        return new DuckingState();  // Fresh instance with own chargeTime_
    }
    return NULL;
}
```

### Concurrent State Machines

When behavior has multiple independent dimensions (what the character does vs. what weapon they carry), maintain separate machines:

```cpp
class Heroine {
private:
    HeroineState* state_;      // Movement: standing, jumping, ducking...
    HeroineState* equipment_;  // Weapon: unarmed, sword, bow...
};

void Heroine::handleInput(Input input) {
    state_->handleInput(*this, input);
    equipment_->handleInput(*this, input);
}
```

This avoids the combinatorial explosion of creating states like "JumpingWithSword", "DuckingWithBow", etc.

### Hierarchical State Machines

When multiple states share behavior (standing, walking, running all respond to "jump" the same way), use inheritance:

```cpp
class OnGroundState : public HeroineState {
public:
    virtual void handleInput(Heroine& heroine, Input input) {
        if (input == PRESS_B) {
            // Jump — shared by standing, walking, running
        }
        else if (input == PRESS_DOWN) {
            // Duck — shared by standing, walking, running
        }
    }
};

class StandingState : public OnGroundState {
    // Inherits jump and duck behavior, adds its own
};
```

### Pushdown Automata

Standard FSMs have no memory of previous states. A pushdown automaton uses a **stack**:

- **Push:** Enter a new state while preserving the current state below.
- **Pop:** Remove the top state, automatically returning to the previous one.

Example: Firing a weapon pushes the FiringState. When firing completes, it pops and the character automatically resumes their previous activity (standing, running, jumping) without explicit transition rules.

### When to Use FSMs

State machines excel when:
- An entity's behavior depends on internal state
- States divide into a small number of distinct options
- The entity responds to events over time

Best for: character controllers, menu navigation, network protocols, simple AI, turn-based systems. For complex AI, consider behavior trees or planning systems.

---

## 2. Observer Pattern

### The Problem

Game systems need to communicate without becoming tightly coupled. An achievement system must respond to events from physics, combat, UI, and many other unrelated systems. Embedding achievement checks throughout the codebase creates a maintenance nightmare.

### Core Architecture

**Observer Interface:**
```cpp
class Observer {
public:
    virtual ~Observer() {}
    virtual void onNotify(const Entity& entity, Event event) = 0;
};
```

**Subject (the thing being observed):**
```cpp
class Subject {
public:
    void addObserver(Observer* observer) {
        observers_[numObservers_++] = observer;
    }

    void removeObserver(Observer* observer) {
        for (int i = 0; i < numObservers_; i++) {
            if (observers_[i] == observer) {
                observers_[i] = observers_[numObservers_ - 1];
                numObservers_--;
                return;
            }
        }
    }

protected:
    void notify(const Entity& entity, Event event) {
        for (int i = 0; i < numObservers_; i++) {
            observers_[i]->onNotify(entity, event);
        }
    }

private:
    Observer* observers_[MAX_OBSERVERS];
    int numObservers_ = 0;
};
```

### Implementation Example: Achievements

```cpp
class Achievements : public Observer {
public:
    virtual void onNotify(const Entity& entity, Event event) {
        switch (event) {
            case EVENT_ENTITY_FELL:
                if (entity.isHero() && heroIsOnBridge_) {
                    unlock(ACHIEVEMENT_FELL_OFF_BRIDGE);
                }
                break;
            case EVENT_ENEMY_KILLED:
                enemiesKilled_++;
                if (enemiesKilled_ >= 100) {
                    unlock(ACHIEVEMENT_SLAYER);
                }
                break;
        }
    }
};
```

**Physics system acts as Subject:**
```cpp
class Physics : public Subject {
    void updateBody(Entity& entity) {
        // ... physics calculations ...
        if (entity.position().y < 0) {
            notify(entity, EVENT_ENTITY_FELL);
        }
    }
};
```

### Linked List Optimization

To avoid dynamic memory allocation during registration, observers can form an intrusive linked list:

```cpp
class Subject {
private:
    Observer* head_;  // First observer in the list
};

class Observer {
    friend class Subject;
    Observer* next_;  // Next observer in the list
};

void Subject::addObserver(Observer* observer) {
    observer->next_ = head_;
    head_ = observer;
}

void Subject::notify(const Entity& entity, Event event) {
    Observer* observer = head_;
    while (observer != NULL) {
        observer->onNotify(entity, event);
        observer = observer->next_;
    }
}
```

### Key Characteristics

- **Synchronous:** The subject directly invokes observers and does not resume until all have returned. Slow observers block the subject.
- **Decoupled:** The subject knows nothing about what observers do with notifications.
- **Performance:** Walking a list and calling virtual methods is negligible overhead.
- **No memory allocation** with the linked list approach.

### The Destruction Problem

The Gang of Four pattern does not address object lifetimes. Solutions:

1. **Observers unregister in destructors** — requires discipline but works.
2. **Subjects notify before destruction** — observers can clean up references.
3. **Bidirectional tracking** — observers know which subjects they watch, enabling automatic unregistration.

**Lapsed Listener Problem** (garbage-collected languages): If a UI observer is not explicitly unregistered when the screen is dismissed, it continues receiving notifications invisibly, wasting resources. Always unregister in `OnDisable()` or equivalent.

### Modern Adaptations

Contemporary implementations often use **functions/delegates** rather than class hierarchies:

```csharp
// C# delegate approach (Unity-friendly)
public event System.Action<Entity, Event> OnNotify;

// Registration
physics.OnNotify += achievements.HandleEvent;

// Notification
OnNotify?.Invoke(entity, eventType);
```

### When to Use Observers

- Communication between **loosely coupled systems** (UI reacting to gameplay events)
- Broadcasting events to **unknown numbers of listeners** (achievement, analytics, audio)
- Within cohesive modules, prefer **direct method calls** for clarity

---

## 3. Command Pattern

### Core Concept

A command is a **reified method call** — an object that encapsulates an action. This turns function calls into first-class objects that can be stored, passed around, queued, serialized, and undone.

### Configuring Input

**Before (hardcoded):**
```cpp
void InputHandler::handleInput() {
    if (isPressed(BUTTON_X)) jump();
    else if (isPressed(BUTTON_Y)) fireGun();
    else if (isPressed(BUTTON_A)) swapWeapon();
    else if (isPressed(BUTTON_B)) lurchIneffectively();
}
```

**After (command pattern):**
```cpp
class Command {
public:
    virtual ~Command() {}
    virtual void execute() = 0;
};

class JumpCommand : public Command {
public:
    virtual void execute() { jump(); }
};

class FireCommand : public Command {
public:
    virtual void execute() { fireGun(); }
};

class InputHandler {
public:
    void handleInput() {
        if (isPressed(BUTTON_X)) buttonX_->execute();
        else if (isPressed(BUTTON_Y)) buttonY_->execute();
        else if (isPressed(BUTTON_A)) buttonA_->execute();
        else if (isPressed(BUTTON_B)) buttonB_->execute();
    }

private:
    Command* buttonX_;  // Can be reassigned at runtime
    Command* buttonY_;
    Command* buttonA_;
    Command* buttonB_;
};
```

Now button bindings can be swapped at runtime without modifying core logic, enabling key remapping.

### Directing Actors

Pass the target actor as a parameter to decouple commands from specific objects:

```cpp
class Command {
public:
    virtual void execute(GameActor& actor) = 0;
};

class JumpCommand : public Command {
public:
    virtual void execute(GameActor& actor) {
        actor.jump();
    }
};
```

The input handler returns commands instead of executing them:

```cpp
Command* InputHandler::handleInput() {
    if (isPressed(BUTTON_X)) return buttonX_;
    if (isPressed(BUTTON_Y)) return buttonY_;
    return NULL;
}

// Game loop
Command* command = inputHandler.handleInput();
if (command) {
    command->execute(playerActor);  // Or any actor
}
```

The same command objects can now drive:
- **Player input** — execute on the player actor
- **AI behavior** — AI generates commands for its own actor
- **Replay systems** — recorded commands replayed on any actor
- **Demo mode** — scripted command sequences

### Undo and Redo

Commands capture state before execution, enabling reversal:

```cpp
class MoveUnitCommand : public Command {
public:
    MoveUnitCommand(Unit* unit, int x, int y)
        : unit_(unit), x_(x), y_(y),
          xBefore_(0), yBefore_(0) {}

    virtual void execute() {
        xBefore_ = unit_->x();
        yBefore_ = unit_->y();
        unit_->moveTo(x_, y_);
    }

    virtual void undo() {
        unit_->moveTo(xBefore_, yBefore_);
    }

private:
    Unit* unit_;
    int xBefore_, yBefore_;
    int x_, y_;
};
```

### Command History for Multi-Level Undo

Maintain a list of executed commands with a pointer to the current position:

```
[Move A] → [Attack B] → [Move C] ← current
                                     ↑ undo pointer
```

- **Undo:** Move pointer backward, call `undo()` on the command.
- **Redo:** Move pointer forward, call `execute()` on the command.
- **New command after undo:** Discard all commands ahead of the pointer, add new command.

### Functional Approach (for languages with closures)

```javascript
function makeMoveUnitCommand(unit, x, y) {
    var xBefore, yBefore;
    return {
        execute: function() {
            xBefore = unit.x();
            yBefore = unit.y();
            unit.moveTo(x, y);
        },
        undo: function() {
            unit.moveTo(xBefore, yBefore);
        }
    };
}
```

### Key Advantages

| Benefit | Description |
|---------|-------------|
| **Decoupling** | Separates input/AI from the actions they trigger |
| **Remapping** | Button bindings changeable at runtime |
| **Undo/Redo** | Reversible operations with command history |
| **Replay** | Record and replay sequences of commands |
| **Networking** | Serialize commands and send over network for multiplayer |
| **AI** | AI systems generate the same command objects as player input |
| **Queueing** | Commands can be stored and executed later |
| **Macros** | Combine multiple commands into composite commands |

### When to Use Commands

- **Input handling** with remappable controls
- **Strategy/tactics games** with undo capability
- **Turn-based games** where actions are queued
- **Multiplayer** where input must be serialized and transmitted
- **Replay systems** that record gameplay
- **Editor tools** requiring undo/redo stacks

---

## Combining Patterns in Unity

These three patterns work together powerfully in Unity game development:

### Example: Card Game Architecture

```csharp
// STATE: Card game phases
public abstract class GamePhase {
    public virtual void Enter(GameManager gm) {}
    public virtual void Exit(GameManager gm) {}
    public virtual void Update(GameManager gm) {}
    public virtual GamePhase HandleInput(GameManager gm, PlayerAction action) {
        return null; // No transition
    }
}

public class DrawPhase : GamePhase {
    public override void Enter(GameManager gm) {
        gm.DrawCards(gm.CurrentPlayer, gm.CardsPerDraw);
        // OBSERVER: Notify UI and effects
        gm.OnPhaseChanged?.Invoke(this);
    }

    public override GamePhase HandleInput(GameManager gm, PlayerAction action) {
        if (action == PlayerAction.EndDraw)
            return new PlayPhase();
        return null;
    }
}

// COMMAND: Player actions are undoable
public class PlayCardCommand : ICommand {
    private Card card;
    private int previousMana;

    public void Execute(GameState state) {
        previousMana = state.CurrentMana;
        state.CurrentMana -= card.ManaCost;
        card.ApplyEffect(state);
    }

    public void Undo(GameState state) {
        card.RemoveEffect(state);
        state.CurrentMana = previousMana;
    }
}

// OBSERVER: Decoupled system communication
public class CardPlayedEvent : ScriptableObject {
    public event System.Action<Card> OnCardPlayed;
    public void Raise(Card card) => OnCardPlayed?.Invoke(card);
}
```

This combination provides:
- **State** manages game flow (draw, play, combat, end phases)
- **Observer** decouples UI updates, sound effects, and analytics from game logic
- **Command** enables undo/redo of player actions and replay of game history
