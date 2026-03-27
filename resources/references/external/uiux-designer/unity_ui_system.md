# Unity UI System: UI Toolkit & uGUI Documentation

> Source: https://docs.unity3d.com/6000.3/Documentation/Manual/UI-system-compare.html
> Fetched: 2026-03-27

## Overview

Unity provides three distinct UI frameworks, each serving different project needs. This document covers the two primary runtime UI systems: **UI Toolkit** (the modern, recommended system) and **uGUI** (the established, production-proven system), along with guidance on when to use each and how to migrate between them.

---

## 1. UI Systems in Unity

### UI Toolkit
UI Toolkit is positioned as the recommended emerging standard for future development, offering a web-like approach with modern design patterns. It uses a document-based architecture similar to web development with UXML (markup), USS (styling), and C# for logic, eliminating GameObject overhead for UI elements.

### uGUI (Unity UI)
uGUI remains the established and production-proven system best suited for runtime applications. It is a GameObject-based UI system where every UI element exists as a GameObject with components like RectTransform, Button, and Text. This approach follows the traditional Unity component pattern.

### IMGUI (Immediate Mode GUI)
IMGUI serves legacy editor extension needs with unrestricted access to editor extensible capabilities. It is not recommended for runtime UI development.

---

## 2. Runtime Recommendations

For runtime UI, uGUI is the recommended solution for most cases, though UI Toolkit serves as an alternative for specific scenarios. Unity is actively investing in UI Toolkit as the future-proof system for Unity 6.0 and beyond.

### When to Choose UI Toolkit (Runtime)
- Multi-resolution menus in intensive UI projects
- World-space and VR interfaces
- Custom shader and material requirements
- Textureless UI rendering needs
- Advanced flexible layout systems (CSS-like flexbox)
- Dynamic texture atlas functionality
- Right-to-left language support and emoji rendering
- Data-intensive interfaces like crafting systems or inventory screens
- Building editor tools (shares Unity's own system)
- Desktop/console projects prioritizing performance
- Starting fresh projects with longer development timelines

### When to Choose uGUI (Runtime)
- Easy referencing from MonoBehaviours
- Keyframed animation requirements (full Animator and Timeline integration)
- In-scene authoring workflows
- Integration with Animation Clips and Timeline
- Sprite and Sprite Atlas support
- Shipping within 3 months with existing team expertise
- Complex animations with particles and state machines
- VR/AR projects needing world space UI
- Heavy reliance on Timeline integration

---

## 3. Feature Comparison

| Feature | UI Toolkit | uGUI | IMGUI |
|---------|-----------|------|-------|
| WYSIWYG Authoring | Yes | Yes | No |
| Data Binding | Yes | No | No |
| Serialized Events | No | Yes | No |
| Animation Integration | No | Yes | Yes |
| Textureless Elements | Yes | No | No |
| SVG Support | Yes | No | No |

---

## 4. Architecture Differences

### Visual Editing
- **uGUI**: Scene View editing with direct GameObject manipulation
- **UI Toolkit**: UI Builder tool providing a Figma-like design interface

### Styling & Layout
**uGUI** uses LayoutGroups and nested hierarchies for responsive design, making complex layouts challenging.

**UI Toolkit** employs CSS-like flexbox through USS stylesheets:
```css
.menu-container {
    flex-grow: 1;
    background-color: #1a1a1a;
    justify-content: center;
    align-items: center;
}

.button-primary {
    padding: 10px 20px;
    background-color: #4a90d9;
    color: white;
    border-radius: 5px;
}
```

### Event Handling
- **uGUI**: `button.onClick.AddListener(HandleClick);`
- **UI Toolkit**: `button.clicked += HandleClick;` (requires manual unsubscription)

### Data Binding
**uGUI** requires manual updates for each element:
```csharp
foreach (var item in items) {
    Instantiate(itemPrefab, itemContainer);
}
```

**UI Toolkit** provides built-in data binding with ListView virtualization, handling thousands of items efficiently and automatically.

---

## 5. Performance Comparison

Benchmark results testing 1000 interactive UI elements:

| Metric | uGUI | UI Toolkit | Improvement |
|--------|------|-----------|-------------|
| Draw Calls | 45 | 5 | 9x fewer |
| CPU Frame Time | 12.5ms | 4.2ms | 3x faster |
| Memory Usage | 125MB | 48MB | 2.6x reduction |
| Item Instantiation (100 items) | 85ms | 15ms | 5.7x faster |

UI Toolkit excels with smooth performance at 10,000+ scrolling items while uGUI stutters at 500+.

---

## 6. uGUI Core Components

### Canvas
The Canvas component is the root of all UI elements in uGUI. All UI elements must be children of a Canvas GameObject. The Canvas determines how UI is rendered:
- **Screen Space - Overlay**: UI rendered on top of everything
- **Screen Space - Camera**: UI rendered at a specific distance from a camera
- **World Space**: UI elements behave as regular GameObjects in the scene

### RectTransform
Every UI element uses a RectTransform (instead of a regular Transform) for positioning and sizing within the Canvas. It supports anchors and pivot points for responsive layouts.

### Core Visual Components
- **Image**: Displays sprite textures
- **Raw Image**: Displays raw textures (non-sprite)
- **Text / TextMeshPro**: Renders text content
- **Mask / RectMask2D**: Clips child content to parent bounds

### Core Interaction Components
- **Button**: Clickable element with onClick event
- **Toggle**: On/off checkbox element
- **Slider**: Draggable value selection
- **Scrollbar**: Scroll position indicator
- **Dropdown**: Selection menu
- **Input Field**: Text input element
- **Scroll Rect**: Scrollable content container

### Layout Components
- **Horizontal Layout Group**: Arranges children horizontally
- **Vertical Layout Group**: Arranges children vertically
- **Grid Layout Group**: Arranges children in a grid
- **Layout Element**: Controls child sizing within groups
- **Content Size Fitter**: Resizes based on content
- **Aspect Ratio Fitter**: Maintains aspect ratios

### Event System
The Event System manages input and raycasting for UI interaction. It uses:
- **Graphic Raycaster**: Detects UI element interactions
- **EventTrigger**: Handles various pointer events (enter, exit, click, drag)
- **IPointerClickHandler, IDragHandler**: Interface-based event handling

---

## 7. UI Toolkit Core Concepts

### UXML (UI Markup)
UI Toolkit uses UXML files to define UI structure, similar to HTML:
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="container">
        <ui:Label text="Hello World" class="title" />
        <ui:Button text="Click Me" name="my-button" />
    </ui:VisualElement>
</ui:UXML>
```

### USS (Unity Style Sheets)
Styling is done through USS files, similar to CSS:
```css
.container {
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.title {
    font-size: 24px;
    color: #ffffff;
    -unity-font-style: bold;
}
```

### VisualElement
The base class for all UI Toolkit elements. Unlike uGUI where every element is a GameObject, VisualElements are lightweight managed objects.

### Key UI Toolkit Controls
- **Label**: Text display
- **Button**: Clickable element
- **TextField**: Text input
- **Toggle**: Checkbox
- **Slider / SliderInt**: Value selection
- **DropdownField**: Selection menu
- **ListView**: Virtualized list for large datasets
- **ScrollView**: Scrollable container
- **Foldout**: Collapsible section

---

## 8. Animation Capabilities

### uGUI Animation (Stronger)
- Full Animator and Timeline integration
- Complex curves and blend trees
- State machine driven UI transitions
- Keyframe animation on any property
- Particle system integration

### UI Toolkit Animation (Limited)
- CSS transitions only (no Timeline or Animator support)
- Property-based transitions via USS:
```css
.button {
    transition-property: background-color, scale;
    transition-duration: 0.3s;
    transition-timing-function: ease-in-out;
}
```
- C# schedule-based animations via `VisualElement.schedule`

---

## 9. Migration from uGUI to UI Toolkit

### Component Mapping
| uGUI Component | UI Toolkit Equivalent |
|----------------|----------------------|
| Text / TextMeshPro | Label |
| Image | VisualElement (with background-image) |
| Button | Button |
| Toggle | Toggle |
| Slider | Slider |
| Dropdown | DropdownField |
| Input Field | TextField |
| Scroll Rect | ScrollView |
| Layout Groups | Flex layout (USS) |

### Migration Strategy
The recommended approach is to build new features with UI Toolkit while maintaining existing uGUI screens. Projects can use both systems simultaneously — uGUI for game HUD and UI Toolkit for menus — in the same codebase without conflicts.

### Key Considerations
- **Maturity**: uGUI remains in maintenance mode receiving bug fixes while UI Toolkit receives new features exclusively, signaling Unity's future direction.
- **Learning Curve**: uGUI feels natural to Unity developers; UI Toolkit requires adopting web-like patterns and CSS-based thinking.
- **Mobile Performance**: UI Toolkit generally performs better, especially with many UI elements, though simple uGUI interfaces work fine on mobile.

---

## 10. Best Practices for Card Game UI

### For a Card Game Project (like Arcana)
1. **Hybrid Approach**: Use uGUI for in-game card interactions (drag, hover, animations) and UI Toolkit for menus, settings, and data-heavy screens (deck builder, collection)
2. **Canvas Setup**: Use Screen Space - Camera for the main game board to allow depth-based card layering
3. **Card Rendering**: Leverage TextMeshPro for card text (supports rich text, outlines, and SDF rendering)
4. **Responsive Layout**: Plan for multiple aspect ratios using anchors (uGUI) or flex layouts (UI Toolkit)
5. **Animation**: Use DOTween or the Animator for card flip, draw, play, and discard animations
6. **Performance**: Pool card UI objects rather than instantiating/destroying them

---

## References

- Unity Manual: UI Systems Comparison - https://docs.unity3d.com/6000.3/Documentation/Manual/UI-system-compare.html
- Unity Manual: UI Toolkit - https://unity.com/features/ui-toolkit
- Unity Manual: uGUI - https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/index.html
- Unity Manual: Migrate from uGUI to UI Toolkit - https://docs.unity3d.com/6000.2/Documentation/Manual/UIE-Transitioning-From-UGUI.html
- Angry Shark Studio: UI Toolkit vs UGUI 2025 Guide - https://www.angry-shark-studio.com/blog/unity-ui-toolkit-vs-ugui-2025-guide/
