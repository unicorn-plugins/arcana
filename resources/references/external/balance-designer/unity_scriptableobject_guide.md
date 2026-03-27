# Unity ScriptableObject Pattern for Game Data

> Source: https://docs.unity3d.com/Manual/class-ScriptableObject.html
> Fetched: 2026-03-27

---

## 1. Overview

ScriptableObjects are serializable Unity types derived from `UnityEngine.Object`. Unlike MonoBehaviours, they exist in the project as **assets, independent of GameObjects** rather than being attached to game objects as components. They function as data containers and can be referenced through the Inspector.

### Primary Benefits

- **Memory efficiency**: Avoid duplicate data copies across multiple objects at runtime
- **Clean architecture**: Separate data from behavior
- **Editor-friendly**: Editable in the Inspector, versionable in source control
- **Shared references**: Multiple prefabs/objects can reference the same ScriptableObject asset

### Key Use Case

Instead of embedding unchanging data in each prefab instance, create a single ScriptableObject asset and reference it from multiple prefabs. This keeps only **one copy in memory** regardless of how many instances reference it.

---

## 2. Creating ScriptableObject Scripts

### 2.1 Using the Editor Template

The quickest approach:
1. Navigate to **Assets > Create > Scripting > ScriptableObject Script**
2. Alternatively, right-click in the Project window and select **Create > Scripting > ScriptableObject Script**

### 2.2 Manual Class Definition

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "Data",
    menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)]
public class SpawnManagerScriptableObject : ScriptableObject
{
    public string prefabName;
    public int numberOfPrefabsToCreate;
    public Vector3[] spawnPoints;
}
```

**Key elements:**
- Inherit from `ScriptableObject` instead of `MonoBehaviour`
- Use `[CreateAssetMenu]` attribute to enable creation from the Assets menu
- `fileName`: Default name for newly created assets
- `menuName`: Path in the Assets > Create menu
- `order`: Position within the menu

---

## 3. Creating ScriptableObject Instances (Assets)

After defining the class with `[CreateAssetMenu]`:

1. Open the **Assets** menu (or right-click in Project window)
2. Navigate to **Create > ScriptableObjects > [Your Menu Name]**
3. A new `.asset` file is created in the Project
4. Select the asset to edit its values in the Inspector

Each `.asset` file is an independent data instance that can be shared across the project.

---

## 4. Referencing ScriptableObjects at Runtime

### 4.1 Basic Pattern: Data Container + Consumer

**Step 1: Define the Data Container (ScriptableObject)**

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "CardData",
    menuName = "GameData/CardData", order = 1)]
public class CardData : ScriptableObject
{
    public string cardName;
    public string description;
    public int manaCost;
    public int attackPower;
    public int defensePower;
    public Sprite cardArtwork;
    public CardType cardType;
    public CardRarity rarity;
}
```

**Step 2: Create the Consumer (MonoBehaviour)**

```csharp
using UnityEngine;

public class CardDisplay : MonoBehaviour
{
    public CardData cardData;  // Assign via Inspector

    void Start()
    {
        Debug.Log($"Card: {cardData.cardName}");
        Debug.Log($"Cost: {cardData.manaCost}");
        Debug.Log($"Attack: {cardData.attackPower}");
    }
}
```

**Step 3: Wire Up in Editor**
- Create CardData assets for each card
- Drag the CardData asset into the CardDisplay component's `cardData` field

### 4.2 Spawn System Example (from Unity Docs)

```csharp
// Data Container
[CreateAssetMenu(fileName = "Data",
    menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)]
public class SpawnManagerScriptableObject : ScriptableObject
{
    public string prefabName;
    public int numberOfPrefabsToCreate;
    public Vector3[] spawnPoints;
}

// Consumer
public class ScriptableObjectManagedSpawner : MonoBehaviour
{
    public GameObject entityToSpawn;
    public SpawnManagerScriptableObject spawnManagerValues;

    void Start()
    {
        for (int i = 0; i < spawnManagerValues.numberOfPrefabsToCreate; i++)
        {
            Instantiate(entityToSpawn,
                spawnManagerValues.spawnPoints[i],
                Quaternion.identity);
        }
    }
}
```

---

## 5. Saving and Persistence

### 5.1 Edit Mode Script Modifications

Changes made via script in the Editor do **not** auto-save. You must call `EditorUtility.SetDirty()`:

```csharp
#if UNITY_EDITOR
using UnityEditor;
#endif

public void UpdateHighScore(GameSettings settings, int score)
{
    settings.highScore += score;

    #if UNITY_EDITOR
    EditorUtility.SetDirty(settings);
    #endif
}
```

Without this call, in-memory changes **revert when closing the editor**.

### 5.2 Runtime Limitations

- **Standalone builds can only READ** from ScriptableObject assets
- **Cannot write to ScriptableObject assets** at runtime in builds
- For runtime-writable data, use JSON serialization, PlayerPrefs, or a save system
- In the Editor, runtime changes persist until you exit Play mode (then revert)

---

## 6. Common Patterns for Game Data

### 6.1 Pattern: Game Configuration Database

```csharp
[CreateAssetMenu(menuName = "GameData/GameConfig")]
public class GameConfig : ScriptableObject
{
    [Header("Player Settings")]
    public int startingHP = 100;
    public int startingMana = 50;
    public float moveSpeed = 5.0f;

    [Header("Difficulty Scaling")]
    public AnimationCurve enemyHealthCurve;
    public AnimationCurve enemyDamageCurve;
    public float difficultyMultiplier = 1.0f;

    [Header("Economy")]
    public int goldPerEnemy = 10;
    public float goldMultiplier = 1.0f;
}
```

### 6.2 Pattern: Card Collection / Database

```csharp
[CreateAssetMenu(menuName = "GameData/CardDatabase")]
public class CardDatabase : ScriptableObject
{
    public List<CardData> allCards;

    public CardData GetCardByName(string name)
    {
        return allCards.Find(card => card.cardName == name);
    }

    public List<CardData> GetCardsByType(CardType type)
    {
        return allCards.FindAll(card => card.cardType == type);
    }

    public List<CardData> GetCardsByRarity(CardRarity rarity)
    {
        return allCards.FindAll(card => card.rarity == rarity);
    }
}
```

### 6.3 Pattern: Enum-like Constants

```csharp
[CreateAssetMenu(menuName = "GameData/ElementType")]
public class ElementType : ScriptableObject
{
    public string elementName;
    public Color elementColor;
    public Sprite elementIcon;
    public float damageMultiplierVsFire;
    public float damageMultiplierVsWater;
    public float damageMultiplierVsEarth;
    public float damageMultiplierVsAir;
}
```

This is more flexible than C# enums because:
- Designers can add new elements without code changes
- Each element carries its own data (color, icon, multipliers)
- Relationships between elements are data-driven

### 6.4 Pattern: Event System (Scriptable Event Architecture)

```csharp
// Event definition
[CreateAssetMenu(menuName = "Events/GameEvent")]
public class GameEvent : ScriptableObject
{
    private List<GameEventListener> listeners = new List<GameEventListener>();

    public void Raise()
    {
        for (int i = listeners.Count - 1; i >= 0; i--)
        {
            listeners[i].OnEventRaised();
        }
    }

    public void RegisterListener(GameEventListener listener)
    {
        listeners.Add(listener);
    }

    public void UnregisterListener(GameEventListener listener)
    {
        listeners.Remove(listener);
    }
}

// Listener component
public class GameEventListener : MonoBehaviour
{
    public GameEvent gameEvent;
    public UnityEvent response;

    void OnEnable() => gameEvent.RegisterListener(this);
    void OnDisable() => gameEvent.UnregisterListener(this);

    public void OnEventRaised() => response.Invoke();
}
```

### 6.5 Pattern: Runtime Sets

```csharp
[CreateAssetMenu(menuName = "GameData/RuntimeSet")]
public class RuntimeSet<T> : ScriptableObject
{
    public List<T> items = new List<T>();

    public void Add(T item)
    {
        if (!items.Contains(item))
            items.Add(item);
    }

    public void Remove(T item)
    {
        if (items.Contains(item))
            items.Remove(item);
    }
}

// Concrete implementation for enemies
[CreateAssetMenu(menuName = "GameData/EnemyRuntimeSet")]
public class EnemyRuntimeSet : RuntimeSet<Enemy> { }
```

---

## 7. Best Practices

### 7.1 Architecture Guidelines

1. **Separate data from logic**: ScriptableObjects hold data; MonoBehaviours execute behavior
2. **Use ScriptableObjects for shared configuration**: Any data referenced by multiple objects
3. **Leverage the Inspector**: Design ScriptableObjects to be designer-friendly with headers, tooltips, and ranges
4. **Version control friendly**: `.asset` files are YAML-serialized, making diffs readable
5. **File names must match class names**: Unity requirement for proper serialization

### 7.2 Inspector Enhancement

```csharp
[CreateAssetMenu(menuName = "GameData/CardData")]
public class CardData : ScriptableObject
{
    [Header("Identity")]
    public string cardName;
    [TextArea(3, 5)]
    public string description;

    [Header("Stats")]
    [Range(0, 10)]
    public int manaCost;
    [Range(0, 100)]
    public int attackPower;
    [Range(0, 100)]
    public int defensePower;

    [Header("Visuals")]
    public Sprite artwork;
    public Color cardColor = Color.white;

    [Header("Classification")]
    public CardType cardType;
    public CardRarity rarity;
    [Tooltip("Tags used for filtering and synergy matching")]
    public string[] tags;
}
```

### 7.3 Performance Considerations

- ScriptableObjects are loaded into memory when first referenced
- Use `Resources.UnloadUnusedAssets()` to free unreferenced assets
- For large datasets, consider Addressables for lazy loading
- ScriptableObject references are cheap (just a pointer to the asset in memory)

### 7.4 Common Mistakes to Avoid

1. **Modifying ScriptableObject data at runtime**: Changes persist in Editor but not in builds
2. **Forgetting `SetDirty()` in Editor scripts**: Changes silently lost on editor close
3. **Storing scene-specific references**: ScriptableObjects are project-level assets; they cannot reference scene objects directly
4. **Not using `[CreateAssetMenu]`**: Forces manual asset creation, error-prone
5. **Bloated ScriptableObjects**: Keep them focused; split large data sets into multiple SO types

---

## 8. ScriptableObject vs. Alternatives

| Feature | ScriptableObject | MonoBehaviour | JSON/XML | Scriptable DOTS |
|---------|-----------------|---------------|----------|----------------|
| Lives in scene | No | Yes | No | No |
| Inspector editing | Yes | Yes | No (without tools) | Limited |
| Memory sharing | Yes (by reference) | No (per instance) | No | Yes |
| Runtime writable | Editor only | Yes | Yes | Yes |
| Version control | Good (YAML) | Good (YAML) | Excellent (text) | Varies |
| Hot reload | Yes | Partial | Manual | No |
| Designer friendly | Very | Moderate | Low | Low |

---

## 9. Advanced: Custom Editor for ScriptableObjects

```csharp
#if UNITY_EDITOR
using UnityEditor;

[CustomEditor(typeof(CardData))]
public class CardDataEditor : Editor
{
    public override void OnInspectorGUI()
    {
        CardData card = (CardData)target;

        // Draw default inspector
        DrawDefaultInspector();

        // Add custom preview
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("Preview", EditorStyles.boldLabel);

        if (card.artwork != null)
        {
            GUILayout.Label(AssetPreview.GetAssetPreview(card.artwork),
                GUILayout.Width(128), GUILayout.Height(128));
        }

        // Add calculated fields
        EditorGUILayout.LabelField("Power Rating",
            (card.attackPower + card.defensePower).ToString());

        // Add validation
        if (string.IsNullOrEmpty(card.cardName))
        {
            EditorGUILayout.HelpBox("Card name is required!",
                MessageType.Warning);
        }
    }
}
#endif
```

---

## 10. Relevance to Arcana Project

For a tarot-themed card game built in Unity:

### Recommended ScriptableObject Structure

```
Assets/
  GameData/
    Cards/
      MajorArcana/
        TheFool.asset
        TheMagician.asset
        ... (22 cards)
      MinorArcana/
        Wands/
          AceOfWands.asset
          ... (14 cards)
        Cups/
          AceOfCups.asset
          ... (14 cards)
        Swords/
          AceOfSwords.asset
          ... (14 cards)
        Pentacles/
          AceOfPentacles.asset
          ... (14 cards)
    Config/
      GameConfig.asset
      DifficultySettings.asset
      BalanceConfig.asset
    Elements/
      Fire.asset
      Water.asset
      Air.asset
      Earth.asset
    Enemies/
      EnemyDatabase.asset
    Events/
      OnCardPlayed.asset
      OnStressChanged.asset
      OnBattleEnd.asset
```

### Key Design Decisions

1. **Each tarot card = one CardData ScriptableObject**: 78 assets total, each editable by designers
2. **Element types as ScriptableObjects**: Data-driven elemental interaction system (Fire/Water/Air/Earth)
3. **Balance tuning via ScriptableObjects**: Damage formulas, stress rates, and economy values all live in SO assets
4. **Event architecture**: Decouple game systems using ScriptableObject events
5. **Card Database**: Central index SO referencing all 78 card SOs for runtime lookup
6. **Difficulty presets**: Multiple GameConfig SOs for different difficulty levels

### Balance Designer Workflow

1. Open CardData asset in Inspector
2. Adjust stats (mana cost, attack, defense, special effects)
3. Run Monte Carlo test (separate tool) against card database
4. Playtest in Unity (ScriptableObject changes take effect immediately)
5. Iterate without touching any code
