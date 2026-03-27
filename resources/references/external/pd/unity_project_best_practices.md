# Unity Project Management Best Practices for Small Teams

> Source: https://docs.unity3d.com/6000.3/Documentation/Manual/best-practice-guides.html, https://learn.unity.com/tutorial/project-organization-2019-3, https://github.com/timdhoffmann/unity-project-style-guide
> Fetched: 2026-03-27

## 1. Overview

This document compiles Unity's official best practices and community-proven guidelines for project organization, asset management, coding standards, version control, and team workflows. It is designed for small indie teams (2-5 developers) working with Unity 6 and later versions.

---

## 2. Project Folder Structure

### 2.1 Recommended Directory Layout

```
Assets/
├── __NoVersionControl/        # Temporary files, excluded from version control
├── _Project/                  # All custom production files
│   ├── Core/
│   │   ├── Managers/
│   │   └── ...
│   ├── Characters/
│   │   ├── Enemy/
│   │   ├── Player/
│   │   └── ...
│   ├── Environment/
│   │   ├── Trees/
│   │   └── ...
│   ├── Props/
│   ├── Weapons/
│   ├── Scenes/
│   ├── Scripts/
│   ├── TestScripts/
│   ├── UI/
│   └── Vehicles/
├── Plugins/                   # Reserved for plugins
└── Standard Assets/           # Reserved for Unity standard assets
```

### 2.2 Key Principles

- **Prefix your project folder with underscore** (`_Project`) so it always sorts to the top
- **Prefab everything** - even store assets should be converted to prefabs
- **Preserve asset pack structure** - do not disassemble downloaded asset store packages
- **Tag 3rd party assets** via the inspector for easy identification
- **Keep complex packages in original locations** for easier updates
- **Copy and modify files** in `_Project` folder rather than editing originals from asset packs
- Use `__NoVersionControl/` for temporary files that should not be committed

### 2.3 Asset Store Management

- Keep downloaded packages in their original folder structure
- When modifying third-party assets, copy them into your `_Project` folder first
- Reference modified copies from other project areas
- This approach allows easy updates of the original package without losing your modifications

---

## 3. Scene Hierarchy Organization

### 3.1 Recommended Hierarchy Structure

```
Main
Debug
Managers
Cameras
Lights
UI/
├── Canvas/
│   ├── HUD/
│   ├── PauseMenu/
│   └── ...
World/
├── Terrain/
├── Props/
├── Structures/
└── ...
Gameplay/
├── Actors/
├── Items/
└── ...
_DynamicObjects/              # Parent for runtime-instantiated objects
```

### 3.2 Grouping Objects

Complex scenes often contain extensive object lists. Use **Empty GameObjects** as organizational containers:

1. Right-click in the Hierarchy and select "Create Empty"
2. Rename the GameObject to describe what it will contain
3. Reset transformations to position at (0, 0, 0) or an appropriate pivot point
4. Select all objects to be grouped and parent them under the container
5. Collapse the group to reduce clutter in the Hierarchy

### 3.3 Benefits

- Reduces visual complexity in the Hierarchy panel
- Improves scene navigation and management
- Creates logical object relationships
- Makes multi-developer scene work less conflict-prone

---

## 4. Naming Conventions

### 4.1 General Rules

- **No spaces** in any filenames or folder names
- **PascalCase** for custom files and folders (e.g., `ComplicatedVerySpecificObject`)
- **Most specific descriptor on the left**: `DarkVampire` not `VampireDark`; `PauseButton` not `ButtonPaused`
- **Sequential names use numbers**: `PathNode0`, `PathNode1` (always start at 0)
- **Avoid numbers for non-sequences**: Use `Flamingo`, `Eagle`, `Swallow` instead of `Bird0`, `Bird1`, `Bird2`
- **Prefix temporary objects** with double underscore: `__Player_Backup`

### 4.2 Naming Aspects with Underscores

Use underscores to separate the core name from an aspect descriptor:

- **Button states**: `EnterButton_Active`, `EnterButton_Inactive`
- **Textures**: `DarkVampire_Diffuse`, `DarkVampire_Normalmap`
- **Skybox faces**: `JungleSky_Top`, `JungleSky_North`
- **LOD levels**: `DarkVampire_LOD0`, `DarkVampire_LOD1`

**Important**: Do not use underscores for type distinction. Use `SmallRock`, `LargeRock` instead of `Rock_Small`, `Rock_Large`.

### 4.3 C# Coding Conventions

- **camelCase** for variables and fields
- **PascalCase** for class names, method names, and public properties
- **Leading underscore** on private fields to distinguish from local variables: `private RigidBody _rigidBody;`
- Use meaningful, descriptive names
- Avoid abbreviations unless universally recognized

---

## 5. Version Control

### 5.1 System Comparison

| System | Strengths | Best For |
|--------|-----------|----------|
| **Git** | Free, widely adopted, excellent branching | Small teams, open source, distributed teams |
| **Perforce** | Handles large binaries well, file locking | Studios with large art assets |
| **PlasticSCM (Unity DevOps)** | Unity-integrated, visual interface | Teams wanting native Unity integration |

### 5.2 Git Best Practices for Unity

**Essential .gitignore entries:**
```
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Uu]ser[Ss]ettings/
*.csproj
*.unityproj
*.sln
*.suo
*.tmp
*.user
*.userprefs
*.pidb
*.booproj
*.svd
*.pdb
*.mdb
*.opendb
*.VC.db
*.pidb.meta
*.pdb.meta
*.mdb.meta
```

**Project Settings for Version Control:**
- Editor > Project Settings > Editor: Set **Version Control Mode** to "Visible Meta Files"
- Editor > Project Settings > Editor: Set **Asset Serialization Mode** to "Force Text"
- These settings ensure .meta files are tracked and scene/prefab files are mergeable

### 5.3 Branching Strategy for Small Teams

- **main**: Stable, always-buildable branch
- **develop**: Integration branch for features in progress
- **feature/xxx**: Individual feature branches
- Keep branches short-lived (merge within 1-2 weeks)
- Communicate before editing shared scenes to avoid merge conflicts

### 5.4 Unity-Specific Version Control Tips

- Unity assets are not file-path specific - you can reorganize folders freely without losing references
- Always commit `.meta` files alongside their corresponding assets
- Scene and prefab merges can be complex - coordinate who edits which scenes
- Use Unity's Smart Merge tool (`UnityYAMLMerge`) for better YAML merge results
- Consider splitting large scenes into multiple smaller scenes using additive scene loading

---

## 6. Unity Official Best Practice Guides (Reference Library)

Unity provides 21 comprehensive best practice guides organized into five categories:

### 6.1 Art and Design (6 Guides)

| Guide | Key Topics |
|-------|-----------|
| Create Virtual and Mixed Reality Experiences | VR template, XR Interaction Toolkit, Apple Vision Pro |
| The Definitive Guide to Animation | Import/export, humanoid animations, UI animation |
| 2D Game Art, Animation, and Lighting | Professional 2D dev including art, design, lighting, VFX |
| The Unity Game Designer Playbook | Visual scripting, input systems, level design, prototyping |
| UI Toolkit for Advanced Developers | Feature-focused sections by professional role |
| Introduction to Game Level Design | ProBuilder, Terrain system, worldbuilding workflows |

### 6.2 DevOps (1 Guide)

| Guide | Key Topics |
|-------|-----------|
| Project Organization and Version Control | VCS concepts, Perforce/Git/PlasticSCM comparison, Unity Asset Manager, Build Automation |

### 6.3 Graphics and Rendering (4 Guides)

| Guide | Key Topics |
|-------|-----------|
| Shaders and VFX with URP | Toon/outline shaders via Shader Graph, stencil operations |
| Introduction to URP | Project setup, Quality Settings, Adaptive Probe Volumes, custom shaders |
| Lighting and Environments in HDRP | Lighting systems, environment effects, performance optimization |
| Advanced Visual Effects | VFX Graph integration, real-time effects |

### 6.4 Performance Optimization (5 Guides)

| Guide | Key Topics |
|-------|-----------|
| Optimize for Mobile, XR, and Web | Cross-platform performance for Unity 6 |
| Optimize for Consoles and PCs | Platform-specific performance tuning |
| Ultimate Guide to Profiling | Advanced profiling, memory management, power consumption |
| The Unity Game Dev Field Guide | Editor navigation, dev environment, physics, input systems |
| Tips to Increase Productivity | 100+ pages covering editor, 2D, debugging, URP/HDRP, UI Toolkit |

### 6.5 Scripting (5 Guides)

| Guide | Key Topics |
|-------|-----------|
| C# Style Guide for Clean Code | Naming conventions, formatting, code documentation |
| Multiplayer Networking | Core multiplayer principles, Netcode for GameObjects |
| DOTS Concepts and Samples | Data-Oriented Technology Stack primer |
| Modular Architecture with ScriptableObjects | Design patterns, production techniques |
| Design Patterns and SOLID | SOLID principles, eleven practical code examples |

---

## 7. Project Management for Small Teams

### 7.1 Production Phases (Unity Learn Framework)

1. **Pre-production**: Concept development, prototyping, team formation, scope definition
2. **Production**: Asset creation, feature implementation, integration, iteration
3. **Post-production**: Testing, polishing, bug fixing, optimization, release preparation

### 7.2 Task Management Best Practices

- Break work into small, testable increments (1-3 day tasks)
- Use a project management tool (Trello, Jira, Monday.com, Notion)
- Hold brief daily standups (15 minutes maximum)
- Review progress weekly against milestones
- Track actual time spent versus estimates to improve future planning

### 7.3 Team Communication

- Establish clear ownership of scenes and systems to avoid conflicts
- Use a shared communication platform (Slack, Discord)
- Document decisions and technical designs
- Schedule regular playtesting sessions with the full team

### 7.4 Build and Integration Practices

- Set up automated builds using Unity Build Automation or custom CI/CD
- Build frequently (at minimum daily) to catch integration issues early
- Maintain a "green" main branch that always compiles and runs
- Test on target platforms regularly, not just in the editor

---

## 8. Asset Pipeline Best Practices

### 8.1 Texture Guidelines

- Use power-of-two dimensions (256, 512, 1024, 2048, 4096)
- Set appropriate max resolution per platform (mobile: 1024, PC: 2048-4096)
- Use texture atlases for UI and small environmental details
- Enable compression appropriate to platform (ASTC for mobile, BC7 for PC)
- Use mipmaps for 3D scene textures; disable for UI textures

### 8.2 Audio Guidelines

- Import source audio as WAV or AIFF (lossless)
- Let Unity handle compression settings per platform
- Use Vorbis compression for music and ambient loops
- Use ADPCM for short sound effects
- Stream long audio clips; decompress short clips on load

### 8.3 Model Import Guidelines

- Export from DCC tools as FBX
- Keep polygon counts appropriate for target platform
- Use LOD groups for complex models
- Configure import settings consistently across similar assets
- Separate animations from mesh files where possible

### 8.4 Script Organization

- One MonoBehaviour per file, file name matching class name
- Use namespaces to avoid naming collisions
- Separate game logic from MonoBehaviour where possible (testability)
- Use assembly definitions to speed up compilation in large projects
- Organize scripts by feature/system rather than by type

---

## 9. Performance Optimization Quick Reference

### 9.1 Common Performance Pitfalls

- **Avoid `Find()` in Update loops**: Cache references in `Start()` or `Awake()`
- **Object pooling**: Reuse objects instead of Instantiate/Destroy cycles
- **Batching**: Use static batching for non-moving objects, dynamic batching for small meshes
- **Overdraw**: Minimize transparent/overlapping materials
- **Physics**: Use simple colliders; limit Rigidbody count; adjust Fixed Timestep

### 9.2 Profiling Workflow

1. Profile on the target device, not just in the editor
2. Use Unity Profiler to identify CPU and GPU bottlenecks
3. Use Frame Debugger for rendering analysis
4. Use Memory Profiler for memory leak detection
5. Profile regularly throughout development, not just at the end

### 9.3 Mobile-Specific Tips

- Target 30fps or 60fps consistently (avoid variable frame rates)
- Minimize draw calls (aim for under 100 on mobile)
- Use baked lighting where possible
- Reduce shader complexity (avoid realtime shadows on low-end devices)
- Test on the lowest-spec target device

---

## 10. Recommended Workflow for a Small Indie Team

### 10.1 Initial Project Setup Checklist

1. Create a new Unity project using the appropriate template (2D, 3D, URP, HDRP)
2. Set up version control (Git + .gitignore + Force Text serialization + Visible Meta Files)
3. Create the `_Project/` folder structure with all subfolders
4. Configure Quality Settings for target platforms
5. Set up assembly definitions for script organization
6. Import essential packages and configure project settings
7. Create a "Bootstrap" or "Main" scene for initialization
8. Document the project setup in a README for team members

### 10.2 Daily Workflow

1. Pull latest changes from the repository
2. Check the build to ensure it compiles
3. Work on assigned tasks in feature branches
4. Test changes locally before committing
5. Commit with descriptive messages
6. Push and create pull requests for review
7. Merge approved changes to develop branch

### 10.3 Weekly Workflow

1. Sprint review: Demo completed features
2. Sprint planning: Assign next week's tasks
3. Integration testing: Test full build on target platforms
4. Playtest: Have team members play through recent changes
5. Address critical bugs before starting new features
