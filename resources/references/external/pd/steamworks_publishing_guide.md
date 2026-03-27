# Steamworks Publishing Guide: Steam PC Publishing Process

> Source: https://partner.steamgames.com/doc/store
> Fetched: 2026-03-27

## 1. Overview

The Steamworks platform provides comprehensive tools for configuring, managing, and operating games on Steam. This guide covers store presence management, publishing workflows, build uploads, and store configuration for PC game publishing.

---

## 2. Application Basics

An **Application (App)** is the main representation of a product on Steam, with its own store page, community hub, and library presence. Each application holds a unique **App ID** referenced throughout Steamworks APIs and tools.

### 2.1 Creating an Application

New applications require:
- Administrator status in the Steamworks partner group
- Purchased Steam Direct Fee ($100 USD) or app credit
- Access to "Create new app..." on the Steamworks landing page

### 2.2 Application Types

| Type | Purpose |
|------|---------|
| **Game** | All games including VR titles |
| **Software** | Audio production, design, photo editing tools |
| **DLC** | Additional content for your game with separate App ID |
| **Video/Series/Episode** | Movies, TV shows, game videos, tutorials |
| **Demo** | Free trial versions with separate App ID, linked to base application |

### 2.3 Core Components Hierarchy

- **Bundles** - Optional groupings allowing multiple packages bundled with discount pricing
- **Packages** - A collection of one or more applications and depots that can be sold via Steam or granted via Steam keys (functions as SKUs or licenses)
- **Depots** - A logical grouping of files which are all delivered to a customer as a single group
- **Builds** - Results from uploading to Steam, containing one or more depots representing a point-in-time snapshot
- **Branches (Betas)** - A specific build made available either publicly or privately. The default branch delivers to customers post-launch. Password-protected branches remain invisible without credentials

---

## 3. Store Page Setup

### 3.1 Store Page Components

Partners must prepare store pages before release and update them post-launch. Key components include:
- Written descriptions (detailed and coherent)
- Graphical assets (capsule images, screenshots, etc.)
- Trailers (required for all products)
- Tags for discovery
- Pricing configuration
- Release date display

### 3.2 Required Graphical Assets

#### Store Assets

| Asset | Dimensions | Required | Notes |
|-------|-----------|----------|-------|
| **Header Capsule** | 920px x 430px | Yes | Game logo and artwork only |
| **Small Capsule** | 462px x 174px | Yes | Compact store listings |
| **Main Capsule** | 1232px x 706px | Yes | Featured/prominent placement |
| **Vertical Capsule** | 748px x 896px | Yes | Vertical layout presentations |
| **Screenshots** | 1920px x 1080px (min) | Yes (min 1) | 16:9 aspect ratio, gameplay only |
| **Page Background** | 1438px x 810px | Optional | Subtle artwork, not too bright |

#### Library Assets

| Asset | Dimensions | Required | Notes |
|-------|-----------|----------|-------|
| **Library Capsule** | 600px x 900px | Yes | Game logo and artwork |
| **Library Hero** | 3840px x 1240px | Yes | Game artwork only (.png) |
| **Library Logo** | 1280px wide and/or 720px tall | Yes | Game logo only (.png), overlays on Hero |
| **Library Header** | 920px x 430px | Yes | Game logo and artwork |

#### Icons

| Asset | Dimensions | Format | Notes |
|-------|-----------|--------|-------|
| **Shortcut Icon** | 256px x 256px | .ico or .png | Steam generates .ico from .png |
| **App Icon** | 184px x 184px | .jpg | Small game logo or icon |

#### Event Assets

| Asset | Dimensions | Required | Notes |
|-------|-----------|----------|-------|
| **Event Cover** | 800px x 450px | Yes | For events or announcements |
| **Event Header** | 1920px x 622px | Optional | Event artwork and logo |

#### Artwork Overrides
- Upload custom capsule images for time-sensitive promotions (major updates, tournaments, limited events)
- Images automatically expire after a specified timespan

**Important**: As of August 2024, Steam accepts larger asset sizes for most capsules. Updated dimensions are mandatory.

### 3.3 Capsule Image Rules

- Must display readable product title or logo
- Game logo and artwork only - no award logos, review quotes, or marketing text
- Must not contain screenshots or gameplay imagery (use the screenshots section instead)

### 3.4 Screenshots Requirements

- Must contain actual gameplay only
- Exclude concept art, pre-rendered cinematics, awards, marketing copy, and product descriptions
- Minimum resolution: 1920x1080 at 16:9 aspect ratio

### 3.5 Trailers

You are required to upload at least one trailer for your product. Trailers are displayed prominently on store pages. Show actual gameplay footage.

### 3.6 Written Descriptions

- Must be "detailed and coherent" so customers understand purchase expectations
- No external website links permitted in the description
- Only launch-ready content should be described
- If discussing future features, clearly mark them as "currently not released"

### 3.7 Tagging System

Tags are terms applied to your game that are visible on your store page. They provide metadata helping Steam recommend products to appropriate audiences. Tags are both developer-set and community-contributed.

### 3.8 Pricing

- Partners set and manage pricing across all supported currencies
- Tools available for currency configuration
- CSV import/export functionality for bulk pricing
- Recurring subscription options available

---

## 4. Coming Soon Pages

### 4.1 Purpose

A Coming Soon page allows developers to establish a Steam store presence before official release, building audience awareness and collecting wishlists.

### 4.2 Requirements

- Branding images
- Written game description
- Gameplay trailer (ideally)
- **Mandatory**: New products must maintain a Coming Soon page for at least two weeks before launch

### 4.3 When to Publish

Publish when you are confident about:
- Art direction and visual style
- Core gameplay features
- That the game will not undergo major changes before release

There does not appear to be a strong downside to having a store page up for a long time ahead of release. Players who wishlist years before release show comparable purchase likelihood to those wishlisting shortly before launch.

### 4.4 Key Benefits

- **Community Hub Activation**: Enables announcements, artwork sharing, and community discussion
- **Wishlist Collection**: Steam automatically emails wishlisters upon release date activation
- **Audience Building**: Start gathering followers and interest early

### 4.5 Setup Process

1. Create new application via Steamworks dashboard
2. Complete release checklist
3. Finalize all "Store Presence" section requirements
4. Click "Mark As Ready For Review"
5. Submit at least 7 business days before desired visibility date
6. After approval, click green "Post as Coming Soon" button

---

## 5. Publishing & Release Process

### 5.1 Review Process

Before releasing on Steam, both the store presence and product build must be reviewed and approved by Valve.

**Review Timeline:**
- Standard review: 3-5 business days
- Recommended: Submit at least 7 days before desired launch to account for potential revisions
- One-time only: Once approved, subsequent updates bypass review entirely

### 5.2 Store Presence Review Requirements

1. **Content Availability**: Store page must feature only launch-ready content; remove incomplete features or unreleased elements
2. **Visual Assets**: Capsule images must display readable product title or logo; screenshots must contain gameplay only
3. **Description Quality**: Must be detailed and coherent; no external website links

### 5.3 Product Build Review Requirements

1. **Functionality**: Product must launch properly on all listed operating systems
2. **Feature Implementation**: All advertised features in the Basic Info tab must be functional in the submitted build
3. **Payment Systems**: Product must use Steam Wallet for any in-game transactions; cannot redirect to alternative payment platforms

### 5.4 Release Options

Three visibility configurations are available when launching products, depending on product type and release timing.

### 5.5 Early Access

Steam Early Access enables you to sell your game while it is still being developed, with clear communication that products are unfinished. Requirements include:
- Complete all Early Access section questionnaire items
- Provide clear customer expectations regarding current content versus planned additions

### 5.6 Free-to-Play Configuration

Games can launch as free-to-play or transition existing titles. Documentation covers setup procedures, store visibility, and developer best practices.

---

## 6. Build Upload with SteamPipe

### 6.1 Overview

SteamPipe is Valve's content delivery system for pushing game updates to Steam. The system handles chunking, compression, and delta updates automatically.

**Key Features:**
- Efficient binary delta algorithm minimizes update sizes
- Multiple branches for public and private beta versions
- Web-based management for promoting builds
- Games remain playable offline during update downloads
- All content encrypted; inactive versions invisible to users

### 6.2 Build Account Setup

Create a dedicated Steam account with specific permissions:
- "Edit App Metadata"
- "Publish App Changes To Steam"

**Security Requirements for released apps:**
- Phone number attached to account, OR Steam Mobile App configured
- Security changes (email, phone) require a 3-day wait before setting live builds

### 6.3 Initial SteamPipe Configuration

1. Identify your App ID in Steamworks
2. Access General Installation Settings page
3. Define launch options (executable path + arguments) per platform (Windows, macOS, Linux)
4. Configure depots on Depots page
5. Publish changes via Publish page
6. Add depots to appropriate packages

### 6.4 SDK Setup

Download and extract the Steamworks SDK. The ContentBuilder directory structure:

```
ContentBuilder/
├── builder/              (steamcmd.exe)
├── builder_linux/        (Linux version)
├── builder_osx/          (macOS version)
├── content/              (Game files go here)
├── output/               (Build logs, cache, manifests)
└── scripts/              (Build configuration files)
```

### 6.5 Build Configuration Script

Simple build script example (.vdf file):

```
"AppBuild" {
  "AppID" "1000"
  "Desc" "Build description"
  "ContentRoot" "..\content\"
  "BuildOutput" "..\output\"
  "Depots" {
    "1001" {
      "FileMapping" {
        "LocalPath" "*"
        "DepotPath" "."
        "recursive" "1"
      }
    }
  }
}
```

### 6.6 Upload Command

```
steamcmd.exe +login <account> <password> +run_app_build <script.vdf> +quit
```

### 6.7 Build Script Parameters

| Parameter | Purpose |
|-----------|---------|
| `AppID` | Game identifier; account needs Edit App Metadata permission |
| `Desc` | Internal description visible only in admin panel |
| `ContentRoot` | Root folder for game files (absolute or relative path) |
| `BuildOutput` | Location for logs, manifests, cache |
| `Preview` | Output only; no upload - for verifying configuration |
| `SetLive` | Beta branch to auto-promote after build; cannot be "default" |

### 6.8 Depot Configuration

- **DepotID**: Identifies the depot
- **ContentRoot**: Override app-level root path
- **FileMapping**: Specify source files to depot location with wildcards
- **FileExclusion**: Exclude files with wildcard support
- **InstallScript**: Mark and sign installation scripts
- **FileProperties**:
  - `userconfig`: User-modifiable files not overwritten by updates
  - `versionedconfig`: Updated with depot changes

### 6.9 Pack File Best Practices

SteamPipe chunks files into ~1MB segments. For pack files (common in game engines):

- Keep asset changes concentrated within pack files to minimize patch sizes
- Group assets by level/feature into separate files
- Add new pack files for updates instead of modifying existing ones
- Do not shuffle asset ordering (causes whole-file redownload)
- Limit individual pack file size (~1-2 GB recommended)
- General compression is unnecessary (Steam compresses for delivery)

### 6.10 CI/CD Integration

For continuous integration environments:
1. Initial login: `steamcmd.exe +login <username>`
2. Enter password and SteamGuard token
3. Verify: type `info` to confirm connection
4. Preserve `<Steam>\config\config.vdf` between runs
5. Future runs: `steamcmd.exe +login <username>` (no password needed)

### 6.11 Build Promotion and Testing

Access `https://partner.steamgames.com/apps/builds/<AppID>` to:
- Set builds live on default or beta branches
- Preview update sizes for customers
- Rollback to previous builds with a few clicks

Deploy builds to beta branches before public release for testing.

---

## 7. Store Discovery & Marketing

### 7.1 Pre-Purchasing

Pre-purchases tend to be ineffective unless heavily anticipated and marketed. Recommended to use short pre-purchase windows if at all.

### 7.2 Franchise Pages

Related products can be linked through franchise definitions and homepage configuration.

### 7.3 Developer & Publisher Homepages

Tools for developers and publishers to create customized homepage pages for their organization and display all their games.

### 7.4 Livestreaming

Broadcast setup tools allowing game streaming to product pages or developer homepages.

### 7.5 User Reviews

Community-generated reviews calculate aggregate scores displayed on store pages, reflecting customer sentiment over 30-day and lifetime periods.

---

## 8. Content Management & Compliance

### 8.1 Localization

Over 60% of Steam users use it in a language other than English. Multi-language support is needed across:
- Store presentation text
- Pricing and currency localization
- Age rating requirements (varies by region, e.g., Germany, Indonesia)

### 8.2 Content Survey

Mandatory content questionnaires supporting regional compliance and age rating assignment. Must be completed as part of the release checklist.

### 8.3 Product Retirement

Procedures exist for discontinuing product sales including cancellation, retirement, or rights expiration scenarios.

---

## 9. Preloading

For large games (>20GB) or retail key distribution before release:
- Content downloads encrypted and unplayable until release
- Decryption occurs automatically at official release time
- Submit preload request to Steam Publishing if required

---

## 10. Retail Disk Creation

### Gold Master Build

Create SKU configuration file:
```
"sku" {
  "name" "Game Title Installer"
  "appid" "202930"
  "disk_size_mb" "640"
  "included_depots" {
    "1" "202931"
    "2" "202932"
  }
}
```

Build command: `build_installer sku_goldmaster.txt "D:\retail_disks"`

---

## 11. Troubleshooting

### Common Build Issues

| Error | Likely Cause | Resolution |
|-------|-------------|------------|
| Login Denied | SteamGuard code needed | Check email, use `set_steam_guard_code <code>` |
| DepotBuild status = 6 | Permission or path issue | Verify App ID, account permissions, content paths |
| Failed to get app info | Configuration not published | Publish Installation + Depots config |
| Invalid content configuration | No build set live | Set live via builds page; verify launch options |
| Mac/Linux files missing | Depot not in package | Add depots to package via admin page |

### Debug Commands

| Command | Purpose |
|---------|---------|
| `app_status [appid]` | Current app state |
| `app_info_print [appid]` | Steamworks configuration |
| `app_config_print [appid]` | User configuration |
| `file "logs\content_log.txt"` | SteamPipe operations log |

---

## 12. Quick Reference: Publishing Checklist

1. Create application on Steamworks (pay Steam Direct fee)
2. Configure depots and packages
3. Prepare all graphical assets (capsules, screenshots, icons, hero images)
4. Write detailed store description
5. Upload gameplay trailer
6. Set tags and categories
7. Configure pricing across currencies
8. Upload game build via SteamPipe
9. Set up Coming Soon page (minimum 2 weeks before launch)
10. Complete Content Survey for age ratings
11. Submit store presence and build for review ("Mark as Ready for Review")
12. Wait 3-5 business days for approval
13. Set release date
14. Launch game (set build live on default branch)
15. Monitor user reviews and update as needed
