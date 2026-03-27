# FMOD for Unity Integration Guide

> Source: https://www.fmod.com/docs/2.03/unity/
> Fetched: 2026-03-27

## 1. Overview

FMOD is a professional audio middleware solution widely used in the game industry for creating adaptive, dynamic audio systems. The FMOD ecosystem consists of two main components:

- **FMOD Studio**: The desktop authoring tool where sound designers create events, mix audio, and design adaptive systems
- **FMOD Engine**: The runtime library that integrates into Unity and plays back authored content efficiently across platforms

FMOD provides capabilities beyond Unity's built-in audio system, including advanced parameter-driven audio behavior, real-time mixing, vertical layering, horizontal re-sequencing, and sophisticated event-based audio architecture.

---

## 2. Installation and Setup

### Prerequisites

- Unity (compatible version)
- FMOD Studio (matching version to the Unity integration)
- Free FMOD account from fmod.com

### Step-by-Step Installation

1. **Download FMOD Studio** from the official FMOD website after creating a free account
2. **Download the FMOD for Unity integration package** (`.unitypackage`) that matches your Unity version and FMOD Studio version
3. **Import the package** into your Unity project via Assets > Import Package > Custom Package
4. **Run the Setup Wizard** that appears automatically after import

### Setup Wizard Configuration

The setup wizard guides through five configuration sections:

#### 1. Updating
- Skip if this is a fresh installation
- For existing projects, the wizard offers tools to reorganize plugin files and refresh event references
- Note: Newer versions replaced the `[FMODUnity.EventRef]` attribute with the `EventReference` type

#### 2. Linking
Choose how the plugin accesses FMOD Studio content:
- **FMOD Studio Project in version control**: Embed the entire `.fspro` project alongside Unity
- **Bank export only**: Export only banks to Unity while keeping the FMOD project locally

Banks must be rebuilt in FMOD Studio (`File > Build`) to sync changes with Unity.

#### 3. Listener
- The wizard automatically locates Unity's default Audio Listener
- Replaces it with FMOD's listener component in active scenes
- FMOD's listener handles 3D audio positioning independently from Unity's system

#### 4. Audio System
- **Recommended**: Disable Unity's native audio system entirely
- This is particularly important for console compatibility (e.g., Xbox)
- Prevents conflicts between Unity audio and FMOD audio processing

#### 5. Audio Sources
- The wizard identifies existing Unity Audio Sources in the project
- Facilitates replacement with FMOD Studio Event Emitter components
- Ensures all audio playback goes through the FMOD pipeline

#### 6. Source Control
- Provides recommendations for `.gitignore` configuration
- Ensures proper repository management of FMOD assets and banks

**Tip**: Check "Do not display this again" to prevent the wizard from reappearing on subsequent project launches.

---

## 3. Core Concepts

### Events

An **event** is the fundamental unit of sound content in FMOD. It is a unit of sound content that can be controlled from game code, and which can contain both audio files and playback logic.

Events can range from simple one-shot sounds to complex multi-layered adaptive compositions. They encapsulate:
- Audio assets (samples, loops)
- Playback logic (randomization, conditions)
- Effects processing (reverb, EQ, compression)
- Parameter automation curves
- Transition rules and regions

### Banks

Banks are containers that package events for runtime loading. To assign an event to a bank:
1. Right-click the event in the Events browser
2. Select **Assign to Bank**
3. Choose the desired bank

Banks must be built in FMOD Studio before they are available in Unity. Use `File > Build` to export banks.

#### Bank Loading Strategies
- **Load on startup**: For essential, always-needed audio (UI sounds, core gameplay)
- **Load on demand**: For level-specific or context-dependent audio
- **Stream from disk**: For large assets like music tracks

### Parameters

Parameters are the primary mechanism for controlling adaptive audio behavior at runtime. They allow game state to influence audio playback dynamically.

#### Creating Parameters
1. Click the `+` next to Timeline in FMOD Studio
2. Choose **Add Parameter Sheet > New Parameter**
3. Configure the parameter:
   - **Name**: e.g., "Intensity", "Health", "Speed"
   - **Type**: User: Continuous (float), User: Discrete (integer), User: Labeled
   - **Range**: e.g., 0 to 1, 0 to 100

#### Parameter Types

| Type | Description | Use Case |
|------|-------------|----------|
| **User: Continuous** | Float value within a range | Intensity, speed, health percentage |
| **User: Discrete** | Integer steps | Weapon type, surface material index |
| **User: Labeled** | Named states | Game state (menu, combat, explore) |
| **Built-in: Distance** | Automatic distance from listener | 3D attenuation |
| **Built-in: Direction** | Automatic angle from listener | Directional audio |
| **Built-in: Elevation** | Automatic vertical angle | Height-based audio |
| **Built-in: Speed** | Automatic object velocity | Movement-based audio |

### Snapshots

Snapshots in FMOD capture mixer states for different game scenarios. They can:
- Adjust group volumes and effects
- Apply ducking and filtering
- Transition smoothly between audio states
- Be triggered and released from game code

---

## 4. FMOD Studio Event Emitter

The **Studio Event Emitter** is the primary component for playing FMOD events in Unity. It replaces Unity's AudioSource component.

### Configuration

| Property | Description |
|----------|-------------|
| **Event** | Reference to the FMOD Studio event to play |
| **Play Event** | Trigger condition: Object Start, Object Destroy, Trigger Enter, etc. |
| **Stop Event** | Trigger condition for stopping playback |
| **Allow Fadeout** | Whether the event fades out when stopped or cuts immediately |
| **Override Attenuation** | Override the event's 3D attenuation settings |
| **Override Min/Max Distance** | Custom distance values for attenuation |

### Setup Steps

1. Add component: `FMOD Studio > FMOD Studio Event Emitter`
2. Set the **Event Play Trigger** field (e.g., Object Start)
3. Click the search button next to the Event field
4. In the browser popup, double-click the desired event

---

## 5. Scripting API

### Namespaces

```csharp
using FMODUnity;       // Unity-specific FMOD integration
using FMOD.Studio;     // FMOD Studio API
```

### Playing Events

#### One-Shot Playback

```csharp
// Play a one-shot event at a position
FMODUnity.RuntimeManager.PlayOneShot("event:/SFX/Explosion", transform.position);
```

#### Persistent Event Instances

```csharp
// Create and manage a persistent event instance
private FMOD.Studio.EventInstance musicInstance;

void Start()
{
    musicInstance = FMODUnity.RuntimeManager.CreateInstance("event:/Music/Combat");
    musicInstance.start();
}

void OnDestroy()
{
    musicInstance.stop(FMOD.Studio.STOP_MODE.ALLOWFADEOUT);
    musicInstance.release();
}
```

### Controlling Parameters

```csharp
// Set a parameter by name
musicInstance.setParameterByName("Intensity", 0.75f);

// Get a parameter value
float value;
musicInstance.getParameterByName("Intensity", out value);
```

### Example: Adaptive Music Controller

```csharp
using UnityEngine;
using FMODUnity;
using FMOD.Studio;

public class AdaptiveMusicController : MonoBehaviour
{
    [SerializeField] private EventReference musicEvent;
    private EventInstance musicInstance;
    private float currentIntensity = 0f;

    void Start()
    {
        musicInstance = RuntimeManager.CreateInstance(musicEvent);
        musicInstance.start();
    }

    public void UpdateIntensity(float newIntensity)
    {
        currentIntensity = Mathf.Clamp01(newIntensity);
        musicInstance.setParameterByName("Intensity", currentIntensity);
    }

    public void TransitionToExploration()
    {
        musicInstance.setParameterByName("GameState", 0f); // 0 = explore
    }

    public void TransitionToCombat()
    {
        musicInstance.setParameterByName("GameState", 1f); // 1 = combat
    }

    void OnDestroy()
    {
        musicInstance.stop(FMOD.Studio.STOP_MODE.ALLOWFADEOUT);
        musicInstance.release();
    }
}
```

### Bank Management

```csharp
// Load a bank at runtime
FMODUnity.RuntimeManager.LoadBank("Level1", true);

// Unload a bank
FMODUnity.RuntimeManager.UnloadBank("Level1");
```

### 3D Audio Positioning

```csharp
// Attach an event instance to a GameObject for automatic 3D positioning
FMODUnity.RuntimeManager.AttachInstanceToGameObject(
    eventInstance,
    transform,
    GetComponent<Rigidbody>()
);
```

---

## 6. Vertical Layering Technique

Vertical layering (also called vertical orchestration) is a key adaptive audio technique supported by FMOD. Multiple audio tracks play simultaneously, and their volumes are controlled by parameters to create dynamic musical responses.

### Setup in FMOD Studio

1. Create an event and assign it to the main bank
2. Add a timeline sheet with multiple audio tracks (e.g., Bass, Drums, Melody, Strings)
3. Configure tempo markers and loop regions for seamless looping
4. Create a "User: Continuous" parameter named "Intensity" (range 0-1)
5. Add volume automation to each track responding to the Intensity parameter

As the intensity increases, more layers are brought in by adjusting automation curves for each track's volume.

### Example Layer Structure

```
Intensity 0.0 - 0.25:  Ambient pad only
Intensity 0.25 - 0.50: + Light percussion
Intensity 0.50 - 0.75: + Melodic elements
Intensity 0.75 - 1.00: + Full orchestra / heavy drums
```

---

## 7. Event Creation Workflow

### Basic Event Setup

1. Open FMOD Studio
2. Right-click in the Events browser > New Event
3. Drag audio assets onto the timeline
4. Set loop regions if needed
5. Add effects (reverb, EQ, compression, etc.)
6. Assign to a bank
7. Build banks (`File > Build`)

### Multi-Instrument Events

FMOD supports creating events with multiple instruments that can be:
- **Randomized**: Select from a pool of clips randomly
- **Sequential**: Play clips in order
- **Shuffled**: Randomized without immediate repetition

This is ideal for footstep sounds, impact effects, and other repetitive game audio.

### Transition Regions

For horizontal re-sequencing, FMOD supports transition regions that define:
- Where a transition can occur (transition markers)
- What happens during the transition (crossfade, immediate cut)
- Destination regions based on parameter values

---

## 8. Mixer and Routing

### FMOD Mixer Architecture

FMOD Studio includes a full mixing console with:
- **Groups (Buses)**: Hierarchical routing for audio categories
- **Returns**: Shared effect processing (reverb sends, delay sends)
- **VCAs**: Volume Control Amplifiers for grouping volume control without routing
- **Master Bus**: Final output stage

### Typical Bus Structure

```
Master Bus
├── Music
│   ├── Exploration Music
│   └── Combat Music
├── SFX
│   ├── Player
│   ├── Enemies
│   ├── Environment
│   └── UI
├── Dialogue
│   ├── NPC
│   └── Narration
└── Ambience
    ├── Indoor
    └── Outdoor
```

### Sidechain and Ducking

FMOD supports sidechaining between buses, allowing:
- Dialogue to automatically duck music and SFX
- Combat sounds to reduce ambient volume
- UI sounds to briefly lower game audio

---

## 9. Advanced Features

### Programmer Sounds

Programmer sounds allow loading and playing audio assets at runtime from code, useful for:
- Localized dialogue systems
- User-generated content
- Dynamic audio that cannot be predetermined

### Beat and Marker Synchronization

FMOD events can contain tempo and beat markers that Unity scripts can listen for:
- Synchronize visual effects with music beats
- Trigger gameplay events on specific musical markers
- Create rhythm-based gameplay mechanics

### RMS Level Monitoring

Monitor the volume levels of event instances in real-time for:
- Audio-reactive visual effects
- Lip-sync approximation
- Dynamic UI audio meters

### Occlusion and Obstruction

FMOD supports audio occlusion (sound passing through walls) and obstruction (sound blocked by objects) through:
- Manual parameter control from raycasts
- Integration with physics systems
- Custom occlusion algorithms

---

## 10. Platform Deployment

### Supported Platforms

FMOD supports deployment across all major Unity target platforms:
- Windows, macOS, Linux
- iOS, Android
- PlayStation, Xbox, Nintendo Switch
- WebGL (with limitations)

### Performance Optimization

- **Bank loading**: Load only necessary banks per scene/level
- **Instance limits**: Set maximum simultaneous instances per event
- **Virtual voices**: FMOD automatically virtualizes inaudible sounds
- **Compression**: Configure per-platform compression settings in FMOD Studio
- **Profiling**: Use FMOD Studio's live profiling to monitor CPU and memory usage

### Build Configuration

- Ensure banks are included in the build output directory
- Configure platform-specific audio settings in FMOD Studio
- Test audio on target hardware for performance validation

---

## 11. FMOD Tutorial Collection Reference

The following tutorial topics are available for deeper learning (based on Alessandro Fama's tutorial series):

### Core Integration
- Plugin installation and setup
- Event playback and triggering
- Parameter modulation systems
- Mixer control and management

### Advanced Features
- ScriptableObject organization for events
- Beat and marker synchronization systems
- Playback state management
- Programmer sounds implementation

### Practical Applications
- Footstep audio systems
- RMS level monitoring for event instances
- Third-person listener implementation
- Music playlist shuffling functionality
- Dynamic object collision responses
- PlayOneShot with parameter integration

---

## 12. Best Practices

1. **Version matching**: Always ensure FMOD Studio and Unity integration versions match
2. **Disable Unity audio**: When using FMOD, disable Unity's built-in audio system to avoid conflicts
3. **Use events, not raw clips**: Let sound designers control audio behavior through FMOD Studio events
4. **Parameter-driven design**: Design audio systems around parameters that map to game states
5. **Bank organization**: Group events into logical banks that match your loading strategy
6. **Release instances**: Always stop and release event instances when no longer needed to prevent memory leaks
7. **Profile regularly**: Use FMOD Studio's profiling tools to monitor audio performance
8. **Collaborate with sound designers**: FMOD enables non-programmers to iterate on audio independently
9. **Use snapshots for state changes**: Create mixer snapshots for different game states (paused, underwater, indoors)
10. **Test on target platforms**: Audio performance varies significantly across platforms
