# Unity 2D Art Asset Specifications (Resolution, Format, Atlas)

> Source: https://docs.unity3d.com/Manual/Sprites.html, https://docs.unity3d.com/Manual/SpriteAtlas.html, Unity Documentation 2022.3/6000.x
> Fetched: 2026-03-27

---

## Part 1: Sprite Fundamentals

### What Are Sprites?

Sprites are 2D graphic objects that function similarly to standard textures but employ special techniques for combining and managing sprite textures for efficiency and convenience during development. They are used for displaying images as sprites in both 2D and 3D scenes via the **Sprite Renderer** component.

### Key Sprite Features

- **Sprite Editor**: Tools for cutting sprites from textures and cropping
- **Collision Geometry**: Editing Collider 2D component geometry
- **Sprite Renderer**: Component for displaying images as sprites in 2D and 3D scenes
- **9-Slice**: Technique to reuse sprites at various sizes without distortion
- **Sprite Atlas**: Packing multiple sprite textures together for video memory optimization
- **Sprite Masking**: Hiding or revealing sprite portions

---

## Part 2: Sprite Import Settings (Inspector Reference)

### Texture Type

Set to **Sprite (2D and UI)** to format the texture asset for use in 2D features.

Other texture type options for reference:
- Default
- Normal Map
- Cursor
- Cookie
- Sprite (2D/UI) — **Use this for game sprites**
- Lightmap
- Editor GUI

### Texture Shape

- **2D**: Standard texture shape, also used for material albedos, GUI elements, and sprites
- Cube, 2D Array, and 3D also available but not used for sprites

### Sprite Mode

| Mode | Description | Use Case |
|---|---|---|
| **Single** | Treats the whole image as a single texture, generates a single asset | Individual sprite images |
| **Multiple** | Allows defining sprite slicing properties to extract multiple sprites from a single packed tileset or sprite sheet | Sprite sheets, tilesets, animation frames |
| **Polygon** | Clips according to custom outlines defined in the Sprite Editor | Complex shapes, non-rectangular sprites |

### Pixels Per Unit (PPU)

**Definition:** The number of pixels of width and height in the sprite image that correspond to one unit distance in world space.

**Key Considerations:**
- Determines how many Unity units the Sprite is in size
- Typically the same across all Sprites in a project
- Should be decided before production of assets, as it determines Sprites' relative scale to each other, the world, and the orthographic camera
- Common values: 16, 32, 64, 100 (default), 128, 256

**Example:** At PPU = 100, a 200x200 pixel sprite = 2x2 Unity units in world space.

### Mesh Type

| Type | Description | Performance Notes |
|---|---|---|
| **Full Rect** | Creates a quad polygon (rectangle) | Simpler mesh, but renders transparent areas; heavier for mobile devices because all unnecessary parts are rendered transparently |
| **Tight** | Generates mesh based on pixel alpha values | Follows sprite's original contour; recommended for mobile; minimum sprite size: 32x32 pixels |

### Extrude Edges

Controls spacing (in pixels) around the sprite in generated meshes. Helps prevent visual artifacts at sprite edges.

### Pivot

Sets the local coordinate origin point for the sprite:

**Preset Options:** Center, Top Left, Top, Top Right, Left, Right, Bottom Left, Bottom, Bottom Right, Custom

**Custom:** Allows specifying exact X/Y values. Available in Single mode only.

### Generate Physics Shape

Automatically generates a default physics collider shape from the sprite outline if no custom shape has been defined in the Sprite Editor.

---

## Part 3: Texture Properties

### sRGB (Color Texture)

- **Enable**: For standard color textures (diffuse, albedo, sprite art)
- **Disable**: For data textures (smoothness, metalness, normal maps)
- Controls whether texture is stored in gamma or linear color space

### Alpha Source

| Option | Description |
|---|---|
| **None** | No alpha channel |
| **Input Texture Alpha** | Uses the alpha channel from the source image |
| **From Gray Scale** | Generates alpha from image luminance |

### Alpha is Transparency

When enabled, dilates color channels to prevent filtering artifacts at transparent edges. Enable for sprites with transparency.

### Remove PSD Matte

Special processing for transparent Photoshop (.psd) files — removes matte color blending.

---

## Part 4: Advanced Settings

### Read/Write Enabled

- Enables script access via Texture2D methods (GetPixels, SetPixels, etc.)
- **Warning:** Doubles memory usage because a copy is kept in system memory
- **Recommendation:** Disable unless runtime pixel access is required

### Generate Mipmaps

Creates mipmap levels for the texture:

- **Mipmap Filtering**: Box (simple averaging) or Kaiser (sharper results)
- **Preserve Coverage**: Maintains alpha channel coverage across mip levels
- **Alpha Cutoff**: Threshold for alpha coverage preservation
- **Replicate Border**: Prevents edge color bleeding at lower mip levels
- **Fadeout to Gray**: Gradually fades mipmaps to neutral gray at distance

**For 2D games:** Often disabled for pixel art or sprites viewed at consistent distance. Enable for sprites that appear at varying distances from camera.

### Wrap Mode

| Mode | Description |
|---|---|
| **Repeat** | Tiles the texture when UV extends beyond 0-1 range |
| **Clamp** | Stretches edge pixels beyond texture bounds |
| **Mirror** | Mirrors the texture at each boundary |
| **Mirror Once** | Mirrors once, then clamps |
| **Per-axis** | Different mode for U and V axes |

### Filter Mode

| Mode | Description | Best For |
|---|---|---|
| **Point (No Filter)** | Makes the texture appear block pixelated from the closest pixel | **Pixel art** — prevents blurring |
| **Bilinear** | Weighted average of nearby pixels; blurred pixelation | Standard sprites at varying sizes |
| **Trilinear** | Blurs between MIP levels for smooth distance transitions | 3D scenes with sprites at varying depths |

### Aniso Level

Adjusts texture quality at steep viewing angles. Higher values = better quality at angles but more GPU cost. Primarily useful for textures viewed at oblique angles (floor textures, etc.).

---

## Part 5: Compression Settings

### Max Texture Size

Controls the maximum pixel dimensions of the imported texture:

| Available Sizes |
|---|
| 32, 64, 128, 256, 512, 1024, **2048** (common default), 4096, 8192, 16384 |

**Best Practice:** Use the smallest size that maintains acceptable visual quality. Powers of 2 are strongly recommended for compression compatibility.

### Compression Format

| Format | Description | Use Case |
|---|---|---|
| **Automatic** | Unity selects optimal format per platform | General use (default) |
| **None** | No compression, maximum quality | Pixel art, UI elements requiring precision |
| **Low Quality** | Higher compression ratio, smaller file | Background elements, less important sprites |
| **Normal Quality** | Balanced compression | Standard game sprites |
| **High Quality** | Lower compression ratio, better visual | Important character sprites, key art |

### Crunch Compression

- Optional additional compression layer using the Crunch library
- Significantly reduces file size for distribution
- **Compressor Quality**: Higher values = better quality but more memory and longer compression time
- Primarily affects download/storage size, not runtime memory

### Platform-Specific Format Options

| Platform | Common Formats | Notes |
|---|---|---|
| **Standalone (PC/Mac)** | DXT1 (no alpha), DXT5 (with alpha), BC7 | BC7 for highest quality |
| **iOS** | ASTC, PVRTC | ASTC preferred for modern devices |
| **Android** | ASTC, ETC2 | ASTC preferred; ETC2 for wider compatibility |
| **WebGL** | DXT1, DXT5, ASTC | Depends on browser support |

---

## Part 6: Sprite Atlas

### What Is a Sprite Atlas?

A Sprite Atlas packs multiple sprite textures tightly together within a single texture to optimize video memory performance. Unity loads an entire Sprite Atlas into memory when any sprite from that atlas appears in a scene.

### Sprite Atlas Inspector Settings

#### Type Configuration

| Type | Description |
|---|---|
| **Master** | Default; serves as parent for variant atlases |
| **Variant** | Creates a lower-resolution version of a master atlas |

#### Build Configuration

**Include in Build**: When enabled, Unity loads the sprite atlas at startup. When disabled, manual runtime loading is required via `SpriteAtlasManager`.

#### Variant Settings

**Scale**: Multiplier for resolution relative to parent master atlas (maximum 1.0). Example: 0.5 = half resolution.

**Warning:** Avoid scale values below 0.25, as this may produce visual artifacts depending on compression format and original resolution.

### Packing Options (Master Type Only)

| Setting | Description | Default | Notes |
|---|---|---|---|
| **Allow Rotation** | Rotates sprites for optimal packing fit | Varies | **Disable for Canvas UI** elements |
| **Tight Packing** | Uses custom mesh outlines instead of rectangles | Varies | Better space efficiency |
| **Alpha Dilation** | Expands edge colors into transparent pixels | Enabled | Prevents visible seams |
| **Padding** | Pixel spacing between packed sprites | **4 pixels** | Minimum 2 recommended to avoid neighbor pixel bleeding with OpenGL |

### Texture Properties

| Setting | Description | Notes |
|---|---|---|
| **Read/Write** | Enables C# script access via Texture2D methods | Duplicates data; disable unless needed |
| **Generate Mip Maps** | Creates mipmap levels | Usually disabled for 2D games |
| **sRGB** | Stores colors in gamma space | Enable for color art |
| **Filter Mode** | Point, Bilinear, or Trilinear | Point for pixel art |
| **Aniso Level** | Viewing angle quality (when mipmaps + Bilinear/Trilinear) | Usually 1 for 2D |

### Compression Settings (Default Tab)

| Setting | Options | Notes |
|---|---|---|
| **Max Texture Size** | 32 to 16384 | Default atlas size: **2048x2048** |
| **Format** | Automatic (default) or specific format | Platform-dependent |
| **Compression** | None, Low, Normal, High Quality | None for pixel art |
| **Crunch Compression** | Toggle | Reduces distribution size |
| **Compressor Quality** | Slider | Higher = better quality, more memory |

### Platform-Specific Overrides

Allow per-platform customization of:
- Max Texture Size
- Format
- Compressor Quality

Access via Platform-specific overrides panel at bottom of Inspector window.

### Objects for Packing

**Packables list**: Sprites, textures, and folders to include in the atlas. Add via drag-and-drop or the Add button.

**Pack Preview**: Generates a preview of the combined atlas for inspection.

---

## Part 7: Sprite Atlas Optimization Best Practices

### Organization Strategy

1. **Group by scene usage**: Ideally all or most sprites that are active in a Scene should belong to the same Atlas
2. **Split by common usage**: Divide sprite textures into multiple smaller Atlases according to their common usage rather than creating one massive atlas
3. **Minimize unused textures**: Since Unity loads entire atlases, avoid mixing frequently and rarely used sprites in one atlas

### Size Optimization

1. **Reduce Max Texture Size**: Use Platform-specific overrides to set appropriate sizes per platform
2. **How resizing works**: When Max Texture Size is lower than current dimensions, Unity reduces packed texture dimensions and automatically trims empty space
3. **Size constraint**: If any individual sprite exceeds the Max Texture Size, the atlas ignores that constraint and remains at minimum required size to contain sprites at original dimensions

### Variant Atlas Guidelines

- Use high padding values and better compression formats when using Variant Atlases
- Avoid scale values less than 0.25 to prevent visual artifacts
- Useful for supporting multiple device resolutions (HD, SD)

### Memory Management

- Unity loads the complete atlas texture into memory when any sprite from it is referenced
- Unused sprites within a loaded atlas still consume memory
- Organization by scene/feature helps minimize wasted memory

---

## Part 8: Recommended Settings by Art Style

### Pixel Art Games

| Setting | Recommended Value | Reason |
|---|---|---|
| Filter Mode | **Point (No Filter)** | Prevents blurring, maintains crisp pixels |
| Compression | **None** | Preserves exact pixel colors |
| Generate Mipmaps | **Disabled** | Not needed at fixed camera distance |
| Mesh Type | **Full Rect** | Simpler for uniform pixel grids |
| PPU | Match to tile size (e.g., 16, 32) | 1 tile = 1 Unity unit |
| Sprite Mode | Multiple (for sheets) | Efficient sprite sheet workflow |

### HD / Hand-Painted Art Games

| Setting | Recommended Value | Reason |
|---|---|---|
| Filter Mode | **Bilinear** | Smooth scaling at various sizes |
| Compression | **Normal or High Quality** | Balance of quality and size |
| Generate Mipmaps | **Consider enabling** | If sprites appear at varying distances |
| Mesh Type | **Tight** | Better performance, especially mobile |
| PPU | 100 (default) or project-specific | Consistent world-space sizing |
| Max Texture Size | 2048 or 4096 | Based on source art resolution |

### Mobile-Optimized Settings

| Setting | Recommended Value | Reason |
|---|---|---|
| Compression | **ASTC** (modern) or **ETC2** (wide compat) | GPU-native compression |
| Max Texture Size | 1024-2048 | Balance quality and memory |
| Mesh Type | **Tight** | Reduces overdraw on fill-limited GPUs |
| Atlas Padding | 2-4 pixels | Prevents bleeding without waste |
| Crunch Compression | **Enable** | Reduces download size |
| Read/Write | **Disable** | Halves runtime memory usage |

---

## Part 9: File Format Recommendations

### Source Art Formats

| Format | Pros | Cons | Best For |
|---|---|---|---|
| **PNG** | Lossless, alpha support, widely compatible | Larger file size | Sprites with transparency, pixel art |
| **PSD** | Layers preserved, direct Photoshop workflow | Large files, Unity flattens on import | Layered art with transparency |
| **TGA** | Lossless, alpha support | Less common in web workflows | Legacy pipelines |
| **EXR** | HDR support, high precision | Very large, overkill for 2D | HDR effects, light maps |

**General Rule:** Use PNG for most 2D sprite work. Unity re-compresses on import regardless of source format, so lossless source preserves maximum quality.

### Resolution Guidelines

| Asset Type | Recommended Resolution | Notes |
|---|---|---|
| Character sprites | 256x256 to 1024x1024 | Depends on screen prominence |
| Background tiles | 64x64 to 256x256 | Repetition makes large sizes wasteful |
| UI icons | 64x64 to 256x256 | Consider multiple DPI targets |
| Full-screen backgrounds | 1920x1080 to 2560x1440 | Match target display resolution |
| Effect sprites | 128x128 to 512x512 | Balance quality with particle count |
| Card game assets | 512x768 to 1024x1536 | Vertical format, readable text |

### Power of Two (POT) Considerations

- Textures with dimensions that are powers of 2 (256, 512, 1024, 2048...) compress most efficiently
- Many compression formats (PVRTC, ETC) require POT dimensions
- ASTC and DXT can handle non-POT (NPOT) textures
- **Recommendation:** Use POT dimensions for atlas textures; individual sprites can be any size since they are packed into POT atlases

---

## Part 10: Workflow Summary

### Asset Pipeline Checklist

1. **Create art** in source format (PNG recommended) at desired resolution
2. **Import into Unity** — automatically detected as Default texture type
3. **Set Texture Type** to Sprite (2D and UI)
4. **Configure Sprite Mode**: Single for individual sprites, Multiple for sprite sheets
5. **Set Pixels Per Unit** consistently across all project sprites
6. **Choose Mesh Type**: Tight for mobile, Full Rect for pixel art
7. **Configure Filter Mode**: Point for pixel art, Bilinear for HD art
8. **Set Compression**: None for pixel art, Normal/High for HD art
9. **Create Sprite Atlases** grouping sprites by scene/feature usage
10. **Configure Atlas settings**: Padding, packing options, platform overrides
11. **Test with Pack Preview** to verify atlas efficiency
12. **Set Platform Overrides** for each target platform (PC, iOS, Android)
