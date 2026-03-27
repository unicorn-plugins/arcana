# Unity JSON Serialization Guide

> Source: https://docs.unity3d.com/Manual/JSONSerialization.html
> Fetched: 2026-03-27

## Overview

Unity provides built-in JSON serialization via `JsonUtility`, and the community standard `Newtonsoft.Json` (Json.NET) for more advanced needs. For a data-driven card game, JSON is the primary format for game data (characters, skills, augmentations, monsters, balance tables).

## JsonUtility (Built-in)

### Basic Usage

```csharp
[System.Serializable]
public class CharacterData
{
    public string id;
    public string name;
    public int attack;
    public int defense;
    public int hp;
    public string[] skillIds;
}

// Serialize
CharacterData data = new CharacterData { id = "fortune", name = "Wheel of Fortune", attack = 50, defense = 30, hp = 100 };
string json = JsonUtility.ToJson(data, true); // prettyPrint = true

// Deserialize
CharacterData loaded = JsonUtility.FromJson<CharacterData>(json);

// Overwrite existing object
JsonUtility.FromJsonOverwrite(json, existingData);
```

### Limitations
- No Dictionary support
- No polymorphism (no inheritance deserialization)
- No null support for value types
- Properties not serialized (only fields)
- No custom converters

### Workaround for Dictionaries
```csharp
[System.Serializable]
public class SerializableDictionary<TKey, TValue> : ISerializationCallbackReceiver
{
    [SerializeField] List<TKey> keys = new List<TKey>();
    [SerializeField] List<TValue> values = new List<TValue>();
    Dictionary<TKey, TValue> dict = new Dictionary<TKey, TValue>();

    public void OnBeforeSerialize()
    {
        keys.Clear(); values.Clear();
        foreach (var kvp in dict) { keys.Add(kvp.Key); values.Add(kvp.Value); }
    }

    public void OnAfterDeserialize()
    {
        dict.Clear();
        for (int i = 0; i < keys.Count; i++) dict[keys[i]] = values[i];
    }

    public TValue this[TKey key]
    {
        get => dict[key];
        set => dict[key] = value;
    }
}
```

## Newtonsoft.Json (Json.NET)

### Installation
```
Window → Package Manager → + → Add by name
→ com.unity.nuget.newtonsoft-json
```

### Basic Usage
```csharp
using Newtonsoft.Json;

// Serialize
string json = JsonConvert.SerializeObject(data, Formatting.Indented);

// Deserialize
CharacterData data = JsonConvert.DeserializeObject<CharacterData>(json);

// Dictionary support (native)
var dict = JsonConvert.DeserializeObject<Dictionary<string, int>>(json);
```

### Advanced Features
```csharp
// Polymorphism
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.Auto
};

// Custom converter
public class SkillEffectConverter : JsonConverter<SkillEffect>
{
    public override SkillEffect ReadJson(JsonReader reader, Type type, SkillEffect existing, bool hasExisting, JsonSerializer serializer)
    {
        JObject obj = JObject.Load(reader);
        string effectType = obj["type"].Value<string>();
        return effectType switch
        {
            "damage" => obj.ToObject<DamageEffect>(serializer),
            "heal" => obj.ToObject<HealEffect>(serializer),
            "buff" => obj.ToObject<BuffEffect>(serializer),
            _ => throw new JsonException($"Unknown effect type: {effectType}")
        };
    }
}

// Null handling
var settings = new JsonSerializerSettings
{
    NullValueHandling = NullValueHandling.Ignore
};
```

## Game Data Architecture

### Recommended: JSON → ScriptableObject Pipeline

```
[Game Data JSON files]        (human-editable, version controlled)
        ↓
[JSON Importer Editor Tool]   (custom Unity editor script)
        ↓
[ScriptableObject Assets]     (used at runtime, fast access)
```

### JSON Schema for Arcana

#### character.json
```json
{
  "characters": [
    {
      "id": "fortune",
      "name": "Wheel of Fortune",
      "arcana": "major",
      "role": "support",
      "baseStats": { "attack": 50, "defense": 30, "hp": 100 },
      "growthCurve": { "youth": 0.8, "adult": 1.0, "elder": 0.9 },
      "skills": {
        "forward": { "id": "erase_fate", "cost": 3, "target": "single_enemy" },
        "reverse": { "id": "rewind_fate", "cost": 2, "target": "single_ally" },
        "ultimate": { "id": "new_fate", "cost": 0, "target": "all_allies" }
      },
      "passive": { "id": "fortune_passive", "description": "On heal, increase ally DEF" }
    }
  ]
}
```

#### libra_system.json (천칭 시스템)
```json
{
  "libra": {
    "incrementPerReverse": 10,
    "incrementPerForward": -10,
    "slotSize": 50,
    "maxSlots": 3,
    "effects": {
      "resistance": [
        { "slot": -1, "atkBonus": 0.08, "hpPenalty": -0.05, "defPenalty": -0.05 },
        { "slot": -2, "atkBonus": 0.16, "hpPenalty": -0.10, "defPenalty": -0.10 },
        { "slot": -3, "atkBonus": 0.32, "hpPenalty": -0.20, "defPenalty": -0.20 }
      ],
      "compliance": [
        { "slot": 1, "healOnHit": 0.03, "atkPenalty": -0.03 },
        { "slot": 2, "healOnHit": 0.06, "atkPenalty": -0.06 },
        { "slot": 3, "healOnHit": 0.12, "atkPenalty": -0.12 }
      ]
    }
  }
}
```

## JsonUtility vs Newtonsoft.Json

| Feature | JsonUtility | Newtonsoft.Json |
|---------|------------|----------------|
| Speed | Faster (no reflection) | Slower (reflection) |
| Dictionary | Not supported | Supported |
| Polymorphism | Not supported | Supported |
| Custom converters | Not supported | Supported |
| Null handling | Limited | Full control |
| LINQ to JSON | No | Yes (JObject) |
| Install size | Built-in | +200KB |

**Recommendation for Arcana**: Use Newtonsoft.Json for data import pipeline (editor-time), JsonUtility for runtime save/load (performance).
