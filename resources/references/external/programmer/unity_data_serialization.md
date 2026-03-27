# Unity Data Serialization: JSON/CSV Parsing Best Practices

> Source: https://docs.unity3d.com/6000.3/Documentation/Manual/json-serialization.html
> Fetched: 2026-03-27

## Overview

Data serialization in Unity covers converting game data to and from persistent formats (JSON, CSV, binary) for saving/loading, configuration, localization, and data-driven design. Unity provides built-in JSON support via `JsonUtility`, and the serialization system underpins the Inspector, prefabs, and asset pipeline.

---

## Part 1: Unity JSON Serialization (JsonUtility)

### Core API

The `JsonUtility` class provides three primary methods for converting between Unity objects and JSON format.

#### ToJson — Object to JSON String

```csharp
[Serializable]
public class PlayerSaveData {
    public string playerName;
    public int level;
    public float health;
    public Vector3 position;
    public List<string> inventory;
}

PlayerSaveData data = new PlayerSaveData {
    playerName = "Hero",
    level = 5,
    health = 87.5f,
    position = new Vector3(10, 0, 20),
    inventory = new List<string> { "Sword", "Shield", "Potion" }
};

string json = JsonUtility.ToJson(data);
// {"playerName":"Hero","level":5,"health":87.5,"position":{"x":10.0,"y":0.0,"z":20.0},"inventory":["Sword","Shield","Potion"]}

string prettyJson = JsonUtility.ToJson(data, true);  // Pretty-printed
```

#### FromJson — JSON String to New Object

```csharp
string json = File.ReadAllText(savePath);
PlayerSaveData data = JsonUtility.FromJson<PlayerSaveData>(json);
```

- Ignores JSON fields that have no matching class field.
- Leaves class fields unchanged if the JSON lacks corresponding values.
- Throws an exception if used with MonoBehaviour or ScriptableObject subclasses (use `FromJsonOverwrite` instead).

#### FromJsonOverwrite — JSON String to Existing Object

```csharp
// Required for MonoBehaviour and ScriptableObject
JsonUtility.FromJsonOverwrite(json, existingObject);
```

- Allocates GC memory only as necessary for written fields (strings, arrays).
- No GC allocation at all if all overwritten fields are value types.
- Enables partial "patching" of objects with incomplete JSON.
- Essential for MonoBehaviour and ScriptableObject deserialization.

### Supported Types

JsonUtility accepts:
- MonoBehaviour subclasses
- ScriptableObject subclasses
- Plain classes/structs with `[Serializable]` attribute

JsonUtility serializes these field types:
- Primitive types: `int`, `float`, `double`, `bool`, `string`
- Enum types (32 bits or smaller)
- Unity built-in types: `Vector2`, `Vector3`, `Vector4`, `Quaternion`, `Rect`, `Matrix4x4`, `Color`, `AnimationCurve`
- Custom structs/classes with `[Serializable]` attribute
- Arrays and `List<T>` of the above types
- References to `UnityEngine.Object`-derived objects

### Unsupported Types

- `Dictionary<TKey, TValue>` (use a serializable wrapper)
- Multidimensional arrays and jagged arrays
- Nested container types (e.g., `List<List<int>>`)
- Properties (only fields are serialized)
- `null` for custom classes serialized inline (they become default instances)

### Performance

JsonUtility is **significantly faster** than popular .NET JSON solutions (Newtonsoft.Json, System.Text.Json) with minimal garbage collection overhead.

**Thread Safety:** Background thread usage is permitted, but avoid concurrent access to the same objects being serialized.

### Field Control Attributes

| Attribute | Effect |
|-----------|--------|
| `[SerializeField]` | Forces serialization of private fields |
| `[NonSerialized]` | Excludes a field from serialization |
| `[HideInInspector]` | Hides from Inspector but still serializes |

---

## Part 2: Serialization Rules and Best Practices

### Field Serialization Requirements

A field is serialized when it meets ALL conditions:
1. Is `public`, OR has `[SerializeField]` attribute
2. Is NOT `static`, `const`, or `readonly`
3. Has a serializable field type

### Inline vs. Reference Serialization

**Inline (default):** Custom class data is stored directly. If two fields reference the same object, they become separate copies on deserialization.

```csharp
[Serializable]
public class Stats {
    public int hp;
    public int attack;
}

public class Monster : MonoBehaviour {
    public Stats baseStats;    // Serialized inline
    public Stats currentStats; // Separate copy, even if same reference at runtime
}
```

**`[SerializeReference]`:** Preserves reference identity, supports `null`, shared references, cyclical data, and polymorphism.

```csharp
public class Monster : MonoBehaviour {
    [SerializeReference] public IAbility ability;  // Can be any IAbility implementation
}
```

### ISerializationCallbackReceiver

For types that Unity cannot serialize directly (like dictionaries), implement this interface to convert to/from serializable formats:

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class SerializableDictionary<TKey, TValue> : ISerializationCallbackReceiver
{
    [SerializeField] private List<TKey> keys = new List<TKey>();
    [SerializeField] private List<TValue> values = new List<TValue>();

    private Dictionary<TKey, TValue> dictionary = new Dictionary<TKey, TValue>();

    public TValue this[TKey key]
    {
        get => dictionary[key];
        set => dictionary[key] = value;
    }

    public void Add(TKey key, TValue value) => dictionary.Add(key, value);
    public bool TryGetValue(TKey key, out TValue value) => dictionary.TryGetValue(key, out value);
    public bool ContainsKey(TKey key) => dictionary.ContainsKey(key);

    public void OnBeforeSerialize()
    {
        keys.Clear();
        values.Clear();
        foreach (var kvp in dictionary)
        {
            keys.Add(kvp.Key);
            values.Add(kvp.Value);
        }
    }

    public void OnAfterDeserialize()
    {
        dictionary = new Dictionary<TKey, TValue>();
        for (int i = 0; i < Math.Min(keys.Count, values.Count); i++)
        {
            dictionary[keys[i]] = values[i];
        }
    }
}
```

---

## Part 3: JSON Save/Load System

### Complete Save System Implementation

```csharp
using System.IO;
using UnityEngine;

public static class SaveSystem
{
    private static string SaveDirectory => Application.persistentDataPath + "/saves";

    public static void Save<T>(T data, string fileName)
    {
        if (!Directory.Exists(SaveDirectory))
            Directory.CreateDirectory(SaveDirectory);

        string json = JsonUtility.ToJson(data, true);
        string path = Path.Combine(SaveDirectory, fileName + ".json");
        File.WriteAllText(path, json);
        Debug.Log($"Saved to: {path}");
    }

    public static T Load<T>(string fileName) where T : new()
    {
        string path = Path.Combine(SaveDirectory, fileName + ".json");

        if (!File.Exists(path))
        {
            Debug.LogWarning($"Save file not found: {path}");
            return new T();
        }

        string json = File.ReadAllText(path);
        return JsonUtility.FromJson<T>(json);
    }

    public static void LoadOverwrite<T>(string fileName, T target)
    {
        string path = Path.Combine(SaveDirectory, fileName + ".json");

        if (!File.Exists(path))
        {
            Debug.LogWarning($"Save file not found: {path}");
            return;
        }

        string json = File.ReadAllText(path);
        JsonUtility.FromJsonOverwrite(json, target);
    }

    public static bool SaveExists(string fileName)
    {
        return File.Exists(Path.Combine(SaveDirectory, fileName + ".json"));
    }

    public static void DeleteSave(string fileName)
    {
        string path = Path.Combine(SaveDirectory, fileName + ".json");
        if (File.Exists(path))
            File.Delete(path);
    }
}

// Usage
SaveSystem.Save(playerData, "player_save");
PlayerSaveData loaded = SaveSystem.Load<PlayerSaveData>("player_save");
```

### Handling Arrays at Top Level

JsonUtility cannot directly serialize top-level arrays. Wrap them in a container:

```csharp
[Serializable]
public class Wrapper<T>
{
    public List<T> items;
}

// Serialize a list
var wrapper = new Wrapper<ItemData> { items = myItemList };
string json = JsonUtility.ToJson(wrapper);

// Deserialize
var result = JsonUtility.FromJson<Wrapper<ItemData>>(json);
List<ItemData> items = result.items;
```

### Handling Unknown Types

Deserialize into a common structure first, then re-deserialize into the actual type:

```csharp
[Serializable]
public class TypedData {
    public string type;
    // Common fields here
}

string json = File.ReadAllText(path);
TypedData header = JsonUtility.FromJson<TypedData>(json);

switch (header.type) {
    case "weapon":
        return JsonUtility.FromJson<WeaponData>(json);
    case "armor":
        return JsonUtility.FromJson<ArmorData>(json);
    default:
        return JsonUtility.FromJson<ItemData>(json);
}
```

---

## Part 4: CSV Parsing for Game Data

Unity does not have built-in CSV support. Here are practical approaches for parsing CSV data (useful for spreadsheet-based game balance data).

### Simple CSV Parser

```csharp
using System.Collections.Generic;
using UnityEngine;

public static class CSVParser
{
    /// <summary>
    /// Parse a CSV TextAsset into a list of dictionaries.
    /// First row is treated as headers (column names).
    /// </summary>
    public static List<Dictionary<string, string>> Parse(TextAsset csvFile)
    {
        var result = new List<Dictionary<string, string>>();
        string[] lines = csvFile.text.Split('\n');

        if (lines.Length < 2) return result;

        // Parse header row
        string[] headers = ParseLine(lines[0]);

        // Parse data rows
        for (int i = 1; i < lines.Length; i++)
        {
            string line = lines[i].Trim();
            if (string.IsNullOrEmpty(line)) continue;

            string[] values = ParseLine(line);
            var entry = new Dictionary<string, string>();

            for (int j = 0; j < headers.Length && j < values.Length; j++)
            {
                entry[headers[j].Trim()] = values[j].Trim();
            }

            result.Add(entry);
        }

        return result;
    }

    /// <summary>
    /// Parse a single CSV line, handling quoted fields with commas.
    /// </summary>
    private static string[] ParseLine(string line)
    {
        var fields = new List<string>();
        bool inQuotes = false;
        string current = "";

        for (int i = 0; i < line.Length; i++)
        {
            char c = line[i];

            if (c == '"')
            {
                inQuotes = !inQuotes;
            }
            else if (c == ',' && !inQuotes)
            {
                fields.Add(current);
                current = "";
            }
            else
            {
                current += c;
            }
        }
        fields.Add(current);

        return fields.ToArray();
    }
}
```

### CSV to ScriptableObject Pipeline

```csharp
using System.Collections.Generic;
using UnityEngine;

// Data class
[CreateAssetMenu(menuName = "Game Data/Card Database")]
public class CardDatabase : ScriptableObject
{
    public List<CardEntry> cards = new List<CardEntry>();

    [System.Serializable]
    public class CardEntry
    {
        public string cardId;
        public string cardName;
        public int manaCost;
        public int attack;
        public int defense;
        public string description;
        public string rarity;
        public string cardType;
    }

    /// <summary>
    /// Import cards from a CSV TextAsset.
    /// CSV format: id,name,mana_cost,attack,defense,description,rarity,type
    /// </summary>
    public void ImportFromCSV(TextAsset csvFile)
    {
        cards.Clear();
        var rows = CSVParser.Parse(csvFile);

        foreach (var row in rows)
        {
            var card = new CardEntry
            {
                cardId = row.GetValueOrDefault("id", ""),
                cardName = row.GetValueOrDefault("name", ""),
                manaCost = int.TryParse(row.GetValueOrDefault("mana_cost", "0"), out int mana) ? mana : 0,
                attack = int.TryParse(row.GetValueOrDefault("attack", "0"), out int atk) ? atk : 0,
                defense = int.TryParse(row.GetValueOrDefault("defense", "0"), out int def) ? def : 0,
                description = row.GetValueOrDefault("description", ""),
                rarity = row.GetValueOrDefault("rarity", "Common"),
                cardType = row.GetValueOrDefault("type", "Creature")
            };

            cards.Add(card);
        }

        Debug.Log($"Imported {cards.Count} cards from CSV");
    }
}

// Extension method for Dictionary
public static class DictionaryExtensions
{
    public static TValue GetValueOrDefault<TKey, TValue>(
        this Dictionary<TKey, TValue> dict, TKey key, TValue defaultValue)
    {
        return dict.TryGetValue(key, out TValue value) ? value : defaultValue;
    }
}
```

### Editor Script for CSV Import

```csharp
#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(CardDatabase))]
public class CardDatabaseEditor : Editor
{
    private TextAsset csvFile;

    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        EditorGUILayout.Space();
        EditorGUILayout.LabelField("CSV Import", EditorStyles.boldLabel);

        csvFile = (TextAsset)EditorGUILayout.ObjectField(
            "CSV File", csvFile, typeof(TextAsset), false);

        if (csvFile != null && GUILayout.Button("Import from CSV"))
        {
            var database = (CardDatabase)target;
            database.ImportFromCSV(csvFile);
            EditorUtility.SetDirty(database);
            AssetDatabase.SaveAssets();
        }
    }
}
#endif
```

---

## Part 5: Serialization Best Practices

### 1. Minimize Serialized Data

Serialize only the essential information needed to reconstruct state. This ensures backwards compatibility as the project evolves.

```csharp
// GOOD: Save only essential data
[Serializable]
public class GameSave
{
    public int currentLevel;
    public float playTime;
    public List<string> unlockedCards;
    public int currency;
}

// BAD: Saving derived/cached data
[Serializable]
public class BadGameSave
{
    public int currentLevel;
    public string currentLevelName;  // Derivable from currentLevel
    public float playTime;
    public string formattedPlayTime; // Derivable from playTime
    public List<string> unlockedCards;
    public int unlockedCardCount;    // Derivable from list length
}
```

### 2. Avoid Deep Nesting

Keep serialized structures flat and simple. Complex nested custom classes become difficult to migrate and maintain.

```csharp
// GOOD: Flat structure with references
[Serializable]
public class CardSaveData
{
    public string cardId;
    public int upgradeLevel;
    public int experience;
}

// BAD: Deep nesting
[Serializable]
public class DeepCardData
{
    public string cardId;
    public CardUpgradeData upgradeData;  // Nested custom class
    // If CardUpgradeData changes structure, migration is painful
}
```

### 3. Use ScriptableObjects for Shared Data

Reference ScriptableObject assets instead of embedding entire object graphs. This ensures data is serialized once and prevents unintentional duplication.

### 4. Thread Safety

- Unity APIs can only be called from the main thread.
- Do NOT call Unity APIs from constructors or field initializers of serializable types (they run on a loading thread).
- Safe to use: `Debug.Log`, math functions (`Vector3` operations, `Mathf`).
- Do NOT initiate serialization from finalizer methods.

### 5. Version Your Save Data

```csharp
[Serializable]
public class VersionedSaveData
{
    public int saveVersion = 2;
    public string playerName;
    public int level;
    public float health;
    // Version 2 additions:
    public int currency;
    public List<string> achievements;
}

// Migration
public static VersionedSaveData LoadWithMigration(string json)
{
    var data = JsonUtility.FromJson<VersionedSaveData>(json);

    if (data.saveVersion < 2)
    {
        // Migrate v1 -> v2
        data.currency = 100;  // Default starting currency
        data.achievements = new List<string>();
        data.saveVersion = 2;
    }

    return data;
}
```

### 6. Use Newtonsoft.Json for Advanced Scenarios

When JsonUtility's limitations are too restrictive (need Dictionary support, polymorphism, LINQ-to-JSON), use Newtonsoft.Json via the Unity package `com.unity.nuget.newtonsoft-json`:

```csharp
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// Dictionary serialization
var config = new Dictionary<string, object> {
    { "volume", 0.8f },
    { "difficulty", "hard" },
    { "controls", new Dictionary<string, string> {
        { "jump", "space" },
        { "attack", "mouse0" }
    }}
};

string json = JsonConvert.SerializeObject(config, Formatting.Indented);
var loaded = JsonConvert.DeserializeObject<Dictionary<string, object>>(json);

// Dynamic JSON parsing
JObject obj = JObject.Parse(json);
float volume = obj["volume"].Value<float>();
```

**Trade-off:** Newtonsoft.Json is more flexible but slower than JsonUtility and generates more garbage collection allocations.

---

## Part 6: Data Pipeline Summary

| Data Type | Recommended Format | Unity Tool |
|-----------|-------------------|------------|
| Game balance (spreadsheet-managed) | CSV | Custom parser + ScriptableObject |
| Save/load game state | JSON | JsonUtility |
| Configuration files | JSON | JsonUtility or Newtonsoft.Json |
| Localization strings | CSV or JSON | Custom parser |
| Complex nested data | JSON | Newtonsoft.Json |
| Large binary data (textures, audio) | Binary/AssetBundle | Unity AssetBundle system |
| Editor-configurable data | ScriptableObject | Unity Inspector |
| Network API responses | JSON | Newtonsoft.Json or JsonUtility |

### Recommended Workflow for Card Game Data

1. **Design Phase:** Designers maintain card data in Google Sheets / Excel.
2. **Export:** Export as CSV files.
3. **Import:** Use Editor scripts to import CSV into ScriptableObject databases.
4. **Runtime:** Game systems reference ScriptableObject data directly.
5. **Saves:** Use JsonUtility to serialize player progress (unlocked cards, deck configurations, etc.) to `Application.persistentDataPath`.
6. **Loading:** On startup, load ScriptableObject assets for game data and JSON files for player state.
