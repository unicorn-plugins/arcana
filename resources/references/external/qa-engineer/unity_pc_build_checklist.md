# Unity PC Build & Steam Deployment Checklist

> Source: https://docs.unity3d.com/Manual/BuildSettings.html, https://partner.steamgames.com/doc/sdk/uploading
> Fetched: 2026-03-27

## Unity Build Settings

### Platform: PC, Mac & Linux Standalone

```
File → Build Settings → PC, Mac & Linux Standalone
```

| Setting | Recommended Value |
|---------|------------------|
| Target Platform | Windows |
| Architecture | x86_64 |
| Compression Method | LZ4HC (best ratio) |
| IL2CPP Backend | Recommended for release (vs Mono) |
| Strip Engine Code | On (reduces build size) |
| API Compatibility | .NET Standard 2.1 |

### Player Settings

```
Edit → Project Settings → Player
```

| Setting | Value |
|---------|-------|
| Company Name | Team Light Life |
| Product Name | Arcana |
| Default Icon | Game icon (256x256) |
| Default Cursor | Custom cursor if applicable |
| Resolution & Presentation | Fullscreen Window (default) |
| Supported Aspect Ratios | 16:9, 16:10 |
| Default Resolution | 1920 x 1080 |
| Allow Fullscreen Switch | On |
| Resizable Window | On |
| Color Space | Linear (URP requirement) |

### Quality Settings

```
Edit → Project Settings → Quality
```

| Level | Resolution | VSync | Anti-Aliasing | Shadows |
|-------|-----------|-------|--------------|---------|
| Low | 1280x720 | Off | None | Off |
| Medium | 1920x1080 | On | 2x MSAA | Basic |
| High | 2560x1440+ | On | 4x MSAA | Full |

## Pre-Build Checklist

### Code
- [ ] No compiler errors or warnings
- [ ] All Debug.Log statements removed or wrapped in #if DEBUG
- [ ] No hardcoded file paths
- [ ] Save system tested (new game, load game, continue)
- [ ] All scenes added to Build Settings scene list
- [ ] Input system works with keyboard + mouse (no controller-only paths)

### Assets
- [ ] No missing references in prefabs/scenes
- [ ] Sprite Atlases built and assigned
- [ ] Audio compression settings optimized
- [ ] No uncompressed textures in build
- [ ] Addressable groups built (if using Addressables)

### Performance
- [ ] 60 FPS on minimum spec hardware
- [ ] No frame spikes > 33ms in combat
- [ ] Memory usage < 500MB
- [ ] Stage transition < 3 seconds
- [ ] No GC spikes during gameplay

### Functionality
- [ ] Tutorial completes without errors
- [ ] All 4 stages + final boss playable
- [ ] All characters' skills functional
- [ ] 천칭 system displays and calculates correctly
- [ ] Augmentation selection and application works
- [ ] Reincarnation/totem system preserves data
- [ ] Settings (volume, resolution, fullscreen) persist

## Steam Integration

### Steamworks SDK Setup
1. Download Steamworks SDK
2. Import `Steamworks.NET` or `Facepunch.Steamworks` Unity package
3. Create `steam_appid.txt` in project root with your App ID
4. Initialize Steam in game startup:

```csharp
void Awake()
{
    if (!SteamAPI.Init())
    {
        Debug.LogError("Steam initialization failed");
        // Handle gracefully (allow offline play or show error)
    }
}

void OnApplicationQuit()
{
    SteamAPI.Shutdown();
}
```

### Steam Features Checklist

| Feature | Implementation |
|---------|---------------|
| Achievements | Unlock via Steamworks API |
| Cloud Save | Save files to Steam Cloud path |
| Rich Presence | Show current stage/boss in friend list |
| Screenshots | F12 support (automatic with Steam overlay) |
| Stats | Track: reincarnation count, bosses defeated, cards played |

### SteamPipe Build Upload

```bash
# Install SteamCMD
# Create app_build.vdf configuration

steamcmd +login [username] +run_app_build app_build.vdf +quit
```

**app_build.vdf:**
```
"AppBuild"
{
    "AppID" "[your_app_id]"
    "Desc" "Arcana v1.0 build"
    "ContentRoot" "./build/"
    "BuildOutput" "./output/"
    "Depots"
    {
        "[depot_id]"
        {
            "FileMapping"
            {
                "LocalPath" "*"
                "DepotPath" "."
                "recursive" "1"
            }
        }
    }
}
```

### Store Page Checklist

| Asset | Spec |
|-------|------|
| Header Capsule | 460 x 215 px |
| Small Capsule | 231 x 87 px |
| Main Capsule | 616 x 353 px |
| Hero Graphic | 3840 x 1240 px |
| Logo | 940 x 422 px (transparent BG) |
| Screenshots | 1920 x 1080 px (min 5) |
| Trailer | 1080p, ≤ 2 min |
| Description | Short + Long description |
| System Requirements | Minimum + Recommended |
| Tags/Categories | Roguelite, Card Game, Strategy, Turn-Based |

## Release Process

1. **Internal QA Pass** — Full regression test
2. **Steam Build Upload** — Upload via SteamPipe
3. **Steam Review** — Submit for Valve review (2-5 business days)
4. **Coming Soon Page** — Live at least 2 weeks before launch
5. **Release Day** — Click "Release" in Steamworks partner dashboard
6. **Day-1 Monitoring** — Watch for crash reports, reviews, community feedback
7. **Day-1 Patch** — Address critical issues within 24 hours
