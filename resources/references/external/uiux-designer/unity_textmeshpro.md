# Unity TextMeshPro Documentation: Font Rendering Guide

> Source: https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/index.html
> Fetched: 2026-03-27

## Overview

TextMeshPro (TMP) is Unity's advanced text rendering solution, providing a set of tools for 2D and 3D text that offers superior control compared to Unity's built-in text components. It leverages Signed Distance Field (SDF) rendering technology to produce crisp, scalable text with support for rich effects like outlines, drop shadows, bevels, and glow — all without losing quality at any scale or distance.

---

## 1. Getting Started

### Installation
TextMeshPro is bundled with the Unity Editor and requires no separate installation. Different versions can be accessed through the Packages Window.

### Required Setup
To use TextMeshPro, import the essential resources:
**Window > TextMeshPro > Import TMP Essential Resources**

### Optional Resources
Import examples and extras for learning:
**Window > TextMeshPro > Import TMP Examples & Extras**
(Strongly recommended for new users)

---

## 2. Core Features

- **Text Formatting**: Character, word, line, and paragraph spacing controls
- **Typography**: Kerning support, justified text formatting
- **Interactive Elements**: Hyperlink functionality
- **Rich Text**: More than 30 rich text tags
- **Multi-font Support**: Use multiple fonts in a single text element
- **Sprite Integration**: Inline sprite/emoji rendering
- **Custom Styles**: Reusable text style definitions
- **Advanced Rendering**: Custom SDF shaders for high-quality output

---

## 3. SDF Font Rendering Technology

### What is SDF?
Signed Distance Field (SDF) is the modern standard for text rendering in games. Unlike traditional bitmap fonts that store pixel data, SDF font assets contain **contour distance information** — grayscale gradients running from the middle of each glyph to a point past its edge.

### How It Works
In SDF font atlases, the **gradient's mid-point corresponds to the edge of the glyph**. This allows the renderer to precisely determine character boundaries at any scale. The distance data encodes how far each pixel is from the nearest edge of the character, with values above the midpoint being inside the glyph and values below being outside.

### Advantages Over Bitmap Fonts
| Aspect | Bitmap Fonts | SDF Fonts |
|--------|-------------|-----------|
| Scaling | Jagged/blurry at non-native sizes | Crisp at any scale |
| Camera Distance | Quality degrades | Consistent quality |
| Transformation | Artifacts on rotation/skew | Clean edges always |
| Effects Support | Limited | Outlines, shadows, bevels, glow |
| Memory Efficiency | Need multiple sizes | Single atlas for all sizes |
| Runtime Cost | Low | Slightly higher shader cost |

### Visual Quality
SDF fonts produce text with **completely smooth edges regardless of camera distance**, contrasting sharply with bitmap fonts that exhibit jagged or blurry edges. The technology handles magnification and distortion exceptionally well.

### When to Use Bitmap Instead
Use rasterized bitmap rendering only when displaying a small font at a **1:1 ratio** (e.g., 10pt font rendered at exactly 10px on screen). For all other cases, SDF is superior.

---

## 4. Font Asset Creation

### Accessing the Creator
**Window > TextMeshPro > Font Asset Creator**

### Step-by-Step Process
1. Create an Assets folder for custom fonts and add font files (.ttf or .otf)
2. Open the Font Asset Creator
3. Configure settings (detailed below)
4. Select **Generate Font Asset**
5. Save the generated asset

### Critical Settings

#### Sampling Point Size / Font Size
- Controls SDF accuracy for font reproduction
- **Auto Size**: Attempts to populate the full character set automatically
- **Custom Mode**: 50-70 points is generally optimal
- Higher values = better reproduction but larger atlas
- Excessive sampling prevents some characters from rendering (atlas overflow)

#### Font Padding
- Dictates the size of visual effects (outlines, glow, bevels)
- Creates room for the SDF gradient — larger padding = smoother transitions
- **Ideal ratio: 1:10** relative to sampling size
  - 60pt sampling = 6pt padding
  - 50pt sampling = 5pt padding
- Rule is flexible for aesthetic variations
- Larger padding = higher-quality rendering and support for thicker effects

#### Packing Method
- **Fast**: Quick preview testing during development
- **Optimum**: Production-quality atlases (use for final builds)

#### Atlas Resolution
- Determined by sampling size and padding values
- **Mobile targets**: Cap at 2048x2048 maximum
- Desktop: Up to 4096x4096 for large character sets
- Larger atlases = more characters but more memory

#### Character Set Options
- **ASCII**: Default, covers basic Latin characters
- **Extended ASCII**: Includes accented characters
- **Custom Characters**: Input specific characters or reference another Font Asset
- **Custom Range**: Hexadecimal ranges for specific Unicode blocks
- **Unicode Range**: Direct Unicode character inclusion
- **Characters from File**: Batch import from text file (ideal for localization)

#### Render Mode
- **SDF / SDFAA / SDF16 / SDF32**: Signed Distance Field variants (recommended)
- **Raster / Raster Hinted / Smooth / Smooth Hinted**: Bitmap fallbacks
- Use SDF modes unless rendering at exact 1:1 pixel ratio

---

## 5. Font Asset Types

### Static Font Assets
- Contain predetermined characters (menus, dialogue, known text)
- Do not reference original font source file
- Smaller build size
- Best for: Known, fixed content (UI labels, card names, predefined text)

### Dynamic Font Assets
- Populate at runtime with specific characters as needed
- **Require source font file (.ttf/.otf) inclusion in build**
- Ideal for: Input fields, player names, variable/user-generated content
- Can generate any character from the source font on demand

### Multi-Atlas Textures
- Auto-generate additional atlas textures when characters exceed current atlas size
- Larger memory footprint but enables runtime flexibility
- Essential for localization support (CJK character sets)

---

## 6. Font Weights and Styles

### Font Weight Variations
TextMeshPro supports multiple font weights (thin, light, regular, medium, bold, black). Each weight can be:
- **Loaded from a separate Font Asset**: Best quality, requires separate font files
- **Simulated through settings**: Applies algorithmic bold/italic (lower quality)

### Bold and Italic
- Use dedicated font files for best results
- Simulated bold adds outline weight to characters
- Simulated italic applies a shear transformation

---

## 7. Font Fallbacks

### Purpose
When the primary font asset lacks a requested character, fallback assets are checked in sequence. This is essential for:
- Multi-language support
- Special character coverage
- Emoji/symbol rendering

### Configuration Levels
- **Global fallbacks**: Set in TMP Settings asset (apply to all text)
- **Per-asset fallbacks**: Set on individual Font Assets (asset-specific)
- Fallback chain is searched in order until the character is found

---

## 8. Shader System

### Shader Types

#### Distance Field (SDF) — Recommended
- The standard shader for SDF font assets
- Supports outlines, underlays (drop shadows), bevels, glow
- **Unlit**: Not affected by scene lighting
- Best for: Most 2D and 3D UI text

#### Distance Field (Surface)
- SDF variant that **interacts with scene lighting**
- Uses Unity's surface shader framework
- Best for: In-world text that should respond to light/shadow
- **Not a physically-based shader**

#### Distance Field Overlay
- SDF variant rendered on top of everything
- **Unaffected by scene lighting**
- Best for: HUD elements, always-visible labels

#### Bitmap Shader
- For non-SDF bitmap font assets
- Simpler rendering, no SDF effects
- Best for: Pixel-perfect small text at fixed sizes

#### Sprite Shader
- Conforms sprite graphics to character shapes from the font atlas
- Best for: Inline sprites and emoji

### Mobile Variants
Each shader has a **mobile variant** optimized for lower-spec devices:
- Reduced feature set (fewer effects)
- Better performance on tablets and phones
- Does not support surface shader variants
- Not affected by scene lighting

### Performance Note
SDF shaders are slightly more expensive than bitmap shaders but the visual quality improvement is substantial. Mobile variants trade features for performance.

---

## 9. Material Properties

### Best Practice
**Always create a new Material Preset for each Font Atlas** to enable per-atlas customization while preserving the default material.

### Face Properties
- **Color**: Base text color (supports HDR)
- **Softness**: Edge softness of characters
- **Dilate**: Expands or contracts character outlines
- **Texture**: Optional face texture overlay
- **Speed**: Scrolling speed for face texture

### Outline Properties
- **Color**: Outline color (supports transparency)
- **Thickness**: Outline width
- **Texture**: Optional outline texture
- Outlines are generated from SDF data (no extra geometry)

### Underlay (Drop Shadow)
- **Color**: Shadow color
- **Offset X/Y**: Shadow displacement
- **Dilate**: Shadow spread
- **Softness**: Shadow blur amount
- Can simulate drop shadows, emboss, or engraving effects

### Glow
- **Color**: Glow color
- **Offset**: Distance from character edge
- **Inner**: Inner glow intensity
- **Outer**: Outer glow extent
- **Power**: Glow falloff curve

### Bevel
- **Type**: Inner or outer bevel
- **Amount**: Bevel depth
- **Offset**: Bevel edge position
- **Width**: Bevel gradient width
- Available only in Surface shader variants

### Lighting (Surface Shader Only)
- **Specular Color**: Highlight color
- **Specular Power**: Highlight sharpness
- **Reflectivity**: Fresnel reflection
- **Diffuse/Shadow**: Light/shadow response
- **Ambient**: Ambient light contribution

### Bump Map (Surface Shader Only)
- **Texture**: Normal map for surface detail
- **Face/Outline**: Separate bump intensity controls

### Environment Map (Surface Shader Only)
- **Cubemap**: Reflection cubemap texture
- **Rotation**: Environment map orientation

---

## 10. Rich Text Tags

TextMeshPro supports over 30 rich text tags for inline formatting. Key tags include:

### Text Formatting
- `<b>Bold</b>` — Bold text
- `<i>Italic</i>` — Italic text
- `<u>Underline</u>` — Underlined text
- `<s>Strikethrough</s>` — Strikethrough text
- `<sup>Superscript</sup>` — Superscript
- `<sub>Subscript</sub>` — Subscript

### Color and Appearance
- `<color=#FF0000>Red</color>` — Text color (hex)
- `<color="red">Red</color>` — Text color (named)
- `<alpha=#80>Semi-transparent</alpha>` — Alpha/opacity
- `<mark=#FFFF0044>Highlighted</mark>` — Text highlight/background

### Size and Spacing
- `<size=24>Large</size>` — Font size
- `<size=+4>Relative</size>` — Relative size change
- `<cspace=2>Spaced</cspace>` — Character spacing
- `<mspace=1em>Monospace</mspace>` — Monospace width
- `<line-height=120%>Tall lines</line-height>` — Line height
- `<indent=2em>Indented</indent>` — Text indentation
- `<margin=5>Margined</margin>` — Text margins

### Alignment
- `<align="left">Left</align>` — Text alignment
- `<align="center">Center</align>`
- `<align="right">Right</align>`
- `<align="justified">Justified</align>`

### Font and Style
- `<font="FontName">Custom Font</font>` — Switch font
- `<font-weight="700">Bold Weight</font-weight>` — Font weight
- `<style="H1">Heading</style>` — Apply custom style

### Special Elements
- `<sprite name="emoji">` — Inline sprite/emoji
- `<link="id">Clickable</link>` — Hyperlink
- `<page>` — Page break
- `<br>` — Line break
- `<nobr>No Break Here</nobr>` — Prevent line break
- `<lowercase>`, `<uppercase>`, `<smallcaps>` — Case transformation

### Positioning
- `<voffset=5>Raised</voffset>` — Vertical offset
- `<pos=50%>Positioned</pos>` — Horizontal position
- `<rotate=15>Tilted</rotate>` — Character rotation (individual characters)

---

## 11. Custom Styles

### Creating Styles
Custom styles allow reusable formatting combinations defined in a TMP Style Sheet:
```
<style="damage">
  <color=#FF4444><b>{0}</b></color>
</style>

<style="healing">
  <color=#44FF44><b>+{0}</b></color>
</style>
```

### Usage
```
You deal <style="damage">25</style> damage and heal <style="healing">10</style> HP.
```

### Style Sheets
- Define in a TMP StyleSheet asset
- Assign globally via TMP Settings or per-component
- Support nested tags within style definitions

---

## 12. Sprite Assets (Inline Icons/Emoji)

### Creating Sprite Assets
1. Create a sprite sheet texture with icons
2. Create a TMP Sprite Asset referencing the texture
3. Define sprite entries with names and Unicode mappings

### Usage in Text
```
Attack: 5 <sprite name="sword">
Health: 10 <sprite name="heart">
Mana: 3 <sprite name="crystal">
```

### Application for Card Games
Sprite assets are invaluable for card games:
- Inline element/type icons in card descriptions
- Mana/resource cost symbols
- Status effect icons in tooltips
- Keyword indicators

---

## 13. Best Practices for Card Game Text Rendering

### Card Text
1. Use SDF fonts for all card text — ensures readability at any zoom level
2. Set font padding to at least 5-6pt for outline/shadow effects
3. Use outline + underlay for text readability over varied card art backgrounds
4. Create separate Material Presets for different card zones (title, description, stats)

### Dynamic Content
1. Use Dynamic Font Assets for player-generated text (deck names, notes)
2. Use Static Font Assets for predefined UI text (menus, tooltips, card names)
3. Set up font fallbacks for localization support (especially CJK)

### Performance
1. Use the mobile shader variant on mobile platforms
2. Avoid excessive rich text tags per frame (batch static text)
3. Cache TMP_Text component references
4. Use `SetText()` instead of modifying `.text` property for frequently updated values
5. Pool text objects in scrolling lists (deck builder, collection browser)

### Accessibility
1. Support adjustable font sizes (minimum 12pt on mobile, 16pt on desktop)
2. Ensure minimum contrast ratio of 4.5:1 between text and background
3. Use font outlines/underlays to maintain readability over complex backgrounds
4. Test with color blind simulation to verify color-coded text is also distinguishable by shape/icon
5. Provide font size scaling option in settings menu

---

## 14. Troubleshooting Common Issues

### Blurry Text
- Increase Sampling Point Size in Font Asset Creator
- Increase Font Padding
- Ensure Canvas Scaler is properly configured
- Check that Pixel Perfect option is appropriate for your resolution

### Missing Characters
- Verify character is included in the Font Asset's character set
- Check font fallback chain
- For dynamic fonts, ensure source font file supports the character
- For CJK, consider multi-atlas textures

### Outline/Effect Artifacts
- Artifacts appear when effects bleed into adjacent characters in the atlas
- **Fix**: Increase padding during font asset creation
- **Fix**: Scale down effect values
- **Fix**: Use larger atlas resolution

### Performance Issues
- Reduce number of TMP objects updating per frame
- Use TextMeshProUGUI for Canvas-based UI (not TextMeshPro 3D for UI)
- Batch static text that doesn't change
- Profile with Unity Profiler to identify text-related bottlenecks

---

## References

- TextMeshPro 4.0 Documentation - https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/index.html
- TextMeshPro 3.2 Documentation - https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/index.html
- About SDF Fonts - https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/FontAssetsSDF.html
- TMP Shaders - https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/Shaders.html
- Font Asset Creation (Unity Learn) - https://learn.unity.com/tutorial/textmesh-pro-font-asset-creation-1
- Shaders and Material Properties (Unity Learn) - https://learn.unity.com/tutorial/textmesh-pro-shaders-and-material-properties
- QuickStart to TextMesh Pro (Unity Learn) - https://learn.unity.com/tutorial/working-with-textmesh-pro
- Pixel Font Rendering with TMP - https://discussions.unity.com/t/how-to-set-up-crisp-ttf-otf-pixel-font-rendering-with-textmesh-pro/947258
- Font Import Guide (Wayline) - https://www.wayline.io/blog/text-mesh-pro-in-unity-font-import-guide
