# Unity Audio System Documentation

> Source: https://docs.unity3d.com/Manual/Audio.html
> Fetched: 2026-03-27

## 1. Overview

Unity's audio system offers full 3D spatial sound, real-time mixing and mastering, hierarchies of mixers, snapshots, and predefined effects. The system enables games to incorporate background music, sound effects, and environmental audio with comprehensive spatial positioning support.

### Basic Theory

In the real world, objects emit sounds that listeners hear. Unity simulates this concept through two key components:

- **Audio Sources**: Components attached to GameObjects that emit sound
- **Audio Listener**: Typically attached to the main camera, receives sound from all sources in the scene

The system calculates spatial audio based on source-listener distance and position. The Doppler Effect is simulated using relative velocities between sources and listeners, creating realistic movement-based pitch shifting.

### Echo and Reverb

Rather than calculating echoes from scene geometry automatically, developers apply Audio Filters to objects. Reverb Zones allow dynamic effects — for example, engine sounds echo when vehicles enter tunnels but diminish upon exit.

---

## 2. Audio File Formats

Unity supports the following audio file formats:

### Uncompressed/Lossless
- `.aif` (Audio Interchange File Format)
- `.wav` (Waveform Audio File Format)

### Compressed
- `.mp3` (MPEG Audio Layer III)
- `.ogg` (Ogg Vorbis)

### Tracker Module Formats
- `.xm` (Extended Module)
- `.mod` (Module)
- `.it` (Impulse Tracker)
- `.s3m` (Scream Tracker 3)

An **Audio Clip** is a container for audio data in Unity. The platform supports mono, stereo, and multichannel audio assets with up to eight channels.

---

## 3. AudioClip Import Settings

### General Properties

| Property | Description |
|----------|-------------|
| **Force To Mono** | Combines multi-channel audio into a single mono track before processing. Useful for reducing file size and memory usage. |
| **Normalize** | Normalizes audio during the Force To Mono mixing down process. Ensures consistent volume levels after downmixing. |
| **Load In Background** | Asynchronously loads audio clips during startup, reducing main thread pressure and improving performance with large files. |
| **Ambisonic** | Supports Ambisonic-encoded audio for spatial soundfield representation, particularly beneficial for 360-degree and XR applications. |

### Load Type Options

| Load Type | Description | Best For |
|-----------|-------------|----------|
| **Decompress On Load** | Decompresses audio immediately upon loading. Vorbis decompression uses approximately 10x more memory than compressed storage. | Small, frequently played clips |
| **Compressed In Memory** | Maintains compression during storage, decompressing during playback on the mixer thread. | Large files where decompression overhead is acceptable |
| **Streaming** | Decodes continuous audio with minimal memory buffering. Overhead approximately 200KB regardless of audio content. | Long music tracks, ambient sounds |

### Compression Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **PCM** | Uncompressed format with highest quality and minimal CPU usage, but largest file sizes. | Short sound effects requiring high quality |
| **ADPCM** | 3.5x compression ratio with low CPU demands. | Noise-heavy sounds played frequently (footsteps, impacts) |
| **Vorbis/MP3** | Smaller files with adjustable quality slider for compression optimization. | Music, longer audio clips |

### Sample Rate Settings

- **Preserve Sample Rate**: Maintains original audio frequency without modification
- **Optimize Sample Rate**: Automatically adjusts based on highest frequency content analysis
- **Override Sample Rate**: Manual control enabling frequency detail reduction for smaller file sizes

### Additional Settings

- **Preload Audio Data**: Default-enabled setting that loads clips when scenes begin, ensuring availability before playback requests
- **Quality Slider**: Controls compression intensity for compressed formats (iterative adjustment recommended)

---

## 4. AudioSource Component

The AudioSource is a component that plays audio clips within a Unity scene and allows customization of playback behavior. It represents audio sources in 3D within Unity's UnityEngine namespace.

### Essential Properties

| Property | Description |
|----------|-------------|
| `volume` | Audio source volume (0.0 to 1.0) |
| `pitch` | Audio playback pitch adjustment |
| `spatialBlend` | 2D/3D blend control (0.0 = fully 2D, 1.0 = fully 3D) |
| `clip` | Default AudioClip for playback |
| `loop` | Enables audio looping |
| `mute` | Mutes/unmutes the source |
| `isPlaying` | Read-only playback status indicator |

### Primary Methods

| Method | Description |
|--------|-------------|
| `Play()` | Starts playback of the assigned clip |
| `Pause()` | Pauses playback at the current position |
| `Stop()` | Stops playback and resets position |
| `PlayDelayed(float delay)` | Plays after a specified delay in seconds |
| `PlayScheduled(double time)` | Plays at a specific DSP time for precise scheduling |
| `PlayOneShot(AudioClip clip)` | Plays a clip once without interrupting the main clip |
| `UnPause()` | Resumes paused playback |

### Advanced Features

- **Spatial audio support** with custom rolloff curves
- **Ambisonic decoder** and spatializer parameters
- **Spectrum and output data analysis** for audio visualization
- **Gamepad audio output routing** for controller speakers
- **Reverb zone mixing** for environmental effects
- **Doppler effect scaling** for movement-based pitch shifting

### Code Example: Basic Audio Toggle

```csharp
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class AudioToggle : MonoBehaviour
{
    private AudioSource audioSource;

    void Start()
    {
        audioSource = GetComponent<AudioSource>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (audioSource.isPlaying)
                audioSource.Pause();
            else
                audioSource.Play();
        }
    }
}
```

---

## 5. AudioListener Component

The AudioListener operates as a microphone-like device that receives input from any given Audio Source in the scene and plays sounds through the computer speakers. It is typically attached to the Main Camera for optimal functionality.

### Key Characteristics

- **No configurable properties** — it simply needs to be present in a scene to function
- Each scene can contain **only one Audio Listener** to work properly
- Handles positional audio by emulating position, velocity, and orientation of sound in the 3D world
- 2D audio sources bypass spatial processing entirely

### Integration Features

- Works with **Reverb Zones** to apply reverberation effects
- Supports **Audio Effects** that apply to all audible sounds in the scene
- Processes audio from Sources within effective range

### Recommended Placement

Attach the AudioListener to either the **Main Camera** or the **player GameObject**, testing both approaches to determine which suits the game best.

---

## 6. Audio Mixer

The Unity Audio Mixer allows you to mix various audio sources, apply effects to them, and perform mastering. It sits between AudioSources and the AudioListener in the signal processing chain.

### Core Components

#### Audio Mixer Groups (Buses)

An Audio Mixer comprises a hierarchical tree structure with groups that function as buses. Each group is a mix of audio signals processed through a signal chain which allows you to control volume attenuation and pitch correction. These groups enable effect insertion and parameter adjustment while supporting send/return mechanisms between buses.

Every Audio Mixer contains a **master group** by default, with additional groups added to build the desired structure. Multiple Audio Mixers can exist and remain active simultaneously within a project.

### Interface Elements

| Element | Description |
|---------|-------------|
| **Asset container** | Holds all AudioGroups and AudioSnapshots |
| **Hierarchy view** | Displays the complete mixing structure |
| **Mixer Views** | Cached visibility settings for subsets of the hierarchy |
| **Snapshots panel** | Lists all AudioSnapshots within the asset |
| **Output routing** | Defines where the mixer's signal routes |
| **AudioGroup Strip** | Shows VU levels, volume, mute/solo controls, and DSP effects |
| **Edit in Play Mode** | Toggle for runtime parameter adjustment |
| **Exposed Parameters** | List of script-accessible controls |

### Signal Routing

Audio routing involves taking a number of input audio signals and outputting one or more output signals. Multiple AudioSources feed into AudioGroups, which then output to a single destination — either the AudioListener or another mixer.

**Important**: This routing operates independently from the scene graph hierarchy, allowing audio organization separate from 3D spatial relationships.

### Typical Sound Category Structure

```
Master
├── Music
├── Menu Sounds
└── Game Sounds
    ├── NPC Dialogue
    ├── Environmental Ambiences
    └── Foley (gunshots, footsteps, etc.)
```

This organizational approach is game-specific and varies between different projects.

### Snapshots

Snapshots capture complete Audio Mixer states, enabling seamless transitions between moods or themes. They record:

- Volume levels
- Pitch settings
- Send levels
- Wet mix amounts
- All effect parameters

**Example**: Applying reverb and music attenuation to create the feeling of being in a cave.

### Ducking

Ducking allows you to alter the effect of one group based on what is happening in another group. This is useful for reducing background ambience during critical audio events like dialogue or cutscenes.

### Views

Customizable views let you toggle group visibility and switch between them as needed, simplifying management of complex mixer hierarchies.

### 3D Spatial Considerations

Distance-based attenuation and environmental reverb effects apply at the AudioSource level, before signals enter the mixer. This separates 3D world-related effects from category-based mixing operations.

---

## 7. Audio Reverb Zones

Reverb Zones are audio components that apply reverb effects to audio clips based on the audio listener's position within defined zones. They enable gradual transitions between areas with and without ambient effects, such as entering a cavern.

### Properties

| Property | Description |
|----------|-------------|
| **Min Distance** | Inner radius where the reverb effect reaches full intensity while transitioning gradually from no effect |
| **Max Distance** | Outer radius marking where the reverb effect begins to fade in gradually from no effect |
| **Reverb Preset** | Selects which reverb effect the zone applies to audio sources within its range |

### Zone Behavior

- **Center to Min Distance**: Gradual reverb application
- **Min Distance to Max Distance**: Full reverb effect zone
- **Beyond Max Distance**: No reverb applied

Multiple reverb zones can be mixed to create combined effects, allowing designers to layer multiple reverb environments for complex spatial audio scenarios.

---

## 8. Audio Filters and Effects

Audio effects modify the output of Audio Source and Audio Listener components by filtering frequency ranges or applying reverb and other effects. Effects are applied by adding effect components to the object with the Audio Source or Audio Listener.

### Available Filters

| Filter | Description |
|--------|-------------|
| **Audio Low Pass Filter** | Passes low frequencies while removing frequencies higher than the Cutoff Frequency |
| **Audio High Pass Filter** | Passes high frequencies while removing lower frequencies |
| **Audio Chorus Filter** | Creates a chorus effect by duplicating and slightly detuning the signal |
| **Audio Echo Filter** | Applies echo/delay to the audio signal |
| **Audio Distortion Filter** | Applies distortion to the audio signal |
| **Audio Reverb Filter** | Applies reverb to simulate acoustic environments |

### Important Notes

- **Component ordering matters** — the sequence determines the processing order applied to audio
- Effects can be reordered through inspector context menus
- Individual effects can be enabled or disabled to control application
- CPU usage monitoring is available through the Profiler's Audio Tab

---

## 9. Audio Spatializer SDK

The Audio Spatializer SDK extends Unity's native audio plugin framework to enable sophisticated spatial audio processing. It replaces the standard panning mechanism with advanced three-dimensional sound positioning capabilities.

### HRTF Implementation

The system utilizes Head-Related Transfer Function (HRTF) filtering based on modified KEMAR dataset measurements. This approach simulates how sound reaches human ears from different spatial positions, enhancing immersive audio experiences.

### Technical Architecture

The `UnityAudioSpatializerData` structure provides critical metadata including:

- Listener and source transformation matrices
- Spatial blend parameters
- Spread and stereo panning values
- Distance attenuation callbacks
- Minimum and maximum distance thresholds

The system employs 4x4 transformation matrices to calculate relative positioning. The listener matrix is inverted so that you can multiply the two matrices to get a relative direction-vector.

### Performance Considerations

In an application with many sounds, enable the spatializer only on nearby sounds to reduce CPU overhead, using traditional panning for distant audio sources.

---

## 10. Ambisonic Audio

Ambisonics provide immersive soundfield representation that can completely surround a listener. They work particularly well for 360-degree videos and VR applications.

### Audio Format Requirements

- Multi-channel B-format WAV files
- ACN (Ambisonic Channel Numbering) component ordering
- SN3D normalization

The system stores audio in a multi-channel format rather than mapping channels to specific speakers, enabling flexible soundfield manipulation.

### Configuration

- Designate an ambisonic decoder through Audio settings (Edit > Project Settings > Audio)
- Unity includes no built-in decoders — use custom decoder plug-ins or VR hardware manufacturers' audio SDKs
- Import multi-channel B-format WAV files and enable the "Ambisonic" option in the audio clip inspector

### Playback

- Assign the WAV file as an Audio Clip to an Audio Source
- Disable the "Spatialize" option (automatic decoding handles this)
- The decoder automatically processes spatialization based on audio source and listener orientation
- **Note**: Reverb zones are disabled for ambisonic audio clips

---

## 11. Audio Random Container

The Audio Random Container is a playlist asset you can play back in different ways. It is designed for sound effect use cases including footsteps, impacts, weapons, and props.

### Features

- Organize multiple audio assets into randomized playlists
- Configure playback modes (random, sequential, shuffle)
- Streamline sound design workflows for repetitive game actions
- Prevent repetition fatigue by varying clip selection

---

## 12. Audio Recording

The `Microphone` class API enables developers to:

- Access available microphones connected to the device
- Query microphone capabilities (frequency range, channels)
- Start and stop recording sessions
- Capture audio data into AudioClip objects for runtime use

---

## 13. Platform Considerations

- **Web platform**: Support for Audio Mixers is limited and partial
- **Mobile platforms**: Decompressing compressed audio can consume significant CPU time; choose compression formats carefully
- **Console platforms**: Some features may require platform-specific audio plugins

---

## 14. Best Practices

1. **Use appropriate compression formats**: PCM for short effects, ADPCM for frequently played noise-heavy sounds, Vorbis for music
2. **Stream long audio files**: Use Streaming load type for music and ambient sounds to minimize memory usage
3. **Organize with Audio Mixer groups**: Create a logical hierarchy matching your game's audio categories
4. **Use snapshots for transitions**: Create mixer snapshots for different game states (combat, exploration, menu)
5. **Leverage ducking**: Automatically lower music/ambience during dialogue or important audio events
6. **Profile audio performance**: Use the Audio Profiler module to monitor CPU and memory usage
7. **Test spatial audio**: Verify 3D audio behavior from multiple listener positions and distances
8. **Preload critical audio**: Ensure gameplay-critical sounds are loaded before they are needed
