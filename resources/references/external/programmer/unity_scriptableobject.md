# Unity ScriptableObject Pattern Guide for Game Data

> Source: https://docs.unity3d.com/Manual/class-ScriptableObject.html
> Fetched: 2026-03-27

## What is a ScriptableObject?

A ScriptableObject is a serializable Unity class derived from `UnityEngine.Object` that allows you to create data containers that exist as project assets, independent of GameObjects and scenes. Unlike MonoBehaviour, ScriptableObjects are not attached to GameObjects as components but live as standalone `.asset` files in the project.

ScriptableObjects are ideal for:
- Storing shared configuration data used by multiple objects at runtime
- Reducing memory usage by avoiding duplicate copies of data
- Centralizing game data in a way accessible from any scene
- Separating data definition from game logic

---

## Creating a ScriptableObject

### Step 1: Define the Class

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewWeaponData", menuName = "Game Data/Weapon Data", order = 1)]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float attackSpeed;
    public float range;
    public Sprite icon;
    public AudioClip attackSound;
    public GameObject effectPrefab;
}
```

The `[CreateAssetMenu]` attribute adds an entry to the **Assets > Create** menu in the Unity Editor.

### Step 2: Create Asset Instances

Navigate to **Assets > Create > Game Data > Weapon Data** in the Unity Editor. This creates a `.asset` file that can be configured in the Inspector.

### Step 3: Reference in MonoBehaviours

```csharp
using UnityEngine;

public class WeaponController : MonoBehaviour
{
    public WeaponData weaponData;  // Assign in Inspector

    void Attack()
    {
        Debug.Log($"Attacking with {weaponData.weaponName} for {weaponData.damage} damage");
        // All instances referencing this WeaponData share the same data
    }
}
```

---

## Lifecycle Methods

ScriptableObjects support a subset of lifecycle messages:

| Method | Description |
|--------|-------------|
| **Awake()** | Called when the ScriptableObject instance is created (via CreateInstance or asset loading) |
| **OnEnable()** | Called when the object is loaded or enabled |
| **OnDisable()** | Called when the object goes out of scope |
| **OnDestroy()** | Called before the object is destroyed |
| **OnValidate()** | Editor-only; called when the script is loaded or Inspector values change |
| **Reset()** | Called to restore default values |

---

## Static Methods

| Method | Description |
|--------|-------------|
| `ScriptableObject.CreateInstance<T>()` | Creates a new instance at runtime |

```csharp
// Runtime creation
WeaponData runtimeWeapon = ScriptableObject.CreateInstance<WeaponData>();
runtimeWeapon.weaponName = "Magic Sword";
runtimeWeapon.damage = 50;
```

---

## Key Benefits Over MonoBehaviour for Data

### 1. Memory Efficiency

Instead of each prefab instance holding its own copy of data, all instances reference the same ScriptableObject asset. For example, 100 enemies of the same type all point to one `EnemyData` asset rather than duplicating stat values 100 times.

### 2. Data-Logic Separation

ScriptableObjects enforce a clean separation between **what the data is** (ScriptableObject) and **what uses the data** (MonoBehaviour). Non-programmers can tweak values in the Inspector without touching code.

### 3. Scene Independence

ScriptableObjects exist as project assets, not scene objects. They persist across scene loads without requiring `DontDestroyOnLoad`.

### 4. Easy Iteration

Designers can create, duplicate, and modify data assets without programmer involvement, enabling rapid iteration on game balance and content.

---

## Common Patterns

### Pattern 1: Game Configuration Data

```csharp
[CreateAssetMenu(menuName = "Game Data/Game Settings")]
public class GameSettings : ScriptableObject
{
    [Header("Difficulty")]
    public float enemyHealthMultiplier = 1f;
    public float enemyDamageMultiplier = 1f;
    public int maxEnemiesOnScreen = 10;

    [Header("Player")]
    public float playerStartHealth = 100f;
    public int startingLives = 3;

    [Header("Audio")]
    [Range(0f, 1f)] public float masterVolume = 1f;
    [Range(0f, 1f)] public float musicVolume = 0.8f;
    [Range(0f, 1f)] public float sfxVolume = 1f;
}
```

Create separate assets for Easy, Normal, and Hard difficulty settings, then swap them at runtime.

### Pattern 2: Item Database

```csharp
[CreateAssetMenu(menuName = "Game Data/Item Database")]
public class ItemDatabase : ScriptableObject
{
    public List<ItemData> allItems = new List<ItemData>();

    public ItemData GetItemById(string id)
    {
        return allItems.Find(item => item.itemId == id);
    }

    public List<ItemData> GetItemsByType(ItemType type)
    {
        return allItems.FindAll(item => item.type == type);
    }
}

[CreateAssetMenu(menuName = "Game Data/Item")]
public class ItemData : ScriptableObject
{
    public string itemId;
    public string displayName;
    [TextArea] public string description;
    public Sprite icon;
    public ItemType type;
    public int maxStack = 99;
    public int buyPrice;
    public int sellPrice;
    public bool isQuestItem;
}

public enum ItemType { Weapon, Armor, Consumable, Material, QuestItem }
```

### Pattern 3: Enum Replacement

Instead of using enums for card types, element types, or status effects, use ScriptableObjects for extensibility:

```csharp
[CreateAssetMenu(menuName = "Game Data/Element Type")]
public class ElementType : ScriptableObject
{
    public string elementName;
    public Color elementColor;
    public Sprite elementIcon;
    public float damageMultiplierVsFire;
    public float damageMultiplierVsWater;
    public float damageMultiplierVsEarth;
    public float damageMultiplierVsWind;
}
```

New element types can be added by creating new assets without modifying any code.

### Pattern 4: Event Channels (ScriptableObject Events)

Use ScriptableObjects as event buses to decouple systems:

```csharp
[CreateAssetMenu(menuName = "Events/Void Event Channel")]
public class VoidEventChannel : ScriptableObject
{
    private System.Action listeners;

    public void Raise()
    {
        listeners?.Invoke();
    }

    public void Subscribe(System.Action listener)
    {
        listeners += listener;
    }

    public void Unsubscribe(System.Action listener)
    {
        listeners -= listener;
    }
}

[CreateAssetMenu(menuName = "Events/Int Event Channel")]
public class IntEventChannel : ScriptableObject
{
    private System.Action<int> listeners;

    public void Raise(int value)
    {
        listeners?.Invoke(value);
    }

    public void Subscribe(System.Action<int> listener)
    {
        listeners += listener;
    }

    public void Unsubscribe(System.Action<int> listener)
    {
        listeners -= listener;
    }
}
```

**Usage — Publisher (e.g., Player Health):**
```csharp
public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private IntEventChannel onHealthChanged;
    [SerializeField] private VoidEventChannel onPlayerDied;

    private int currentHealth;

    public void TakeDamage(int amount)
    {
        currentHealth -= amount;
        onHealthChanged.Raise(currentHealth);

        if (currentHealth <= 0)
            onPlayerDied.Raise();
    }
}
```

**Usage — Subscriber (e.g., UI):**
```csharp
public class HealthUI : MonoBehaviour
{
    [SerializeField] private IntEventChannel onHealthChanged;

    void OnEnable() => onHealthChanged.Subscribe(UpdateHealthDisplay);
    void OnDisable() => onHealthChanged.Unsubscribe(UpdateHealthDisplay);

    void UpdateHealthDisplay(int health)
    {
        healthText.text = health.ToString();
    }
}
```

### Pattern 5: Runtime Sets

Track active objects without using FindObjectsOfType:

```csharp
[CreateAssetMenu(menuName = "Game Data/Runtime Set")]
public class RuntimeGameObjectSet : ScriptableObject
{
    private List<GameObject> items = new List<GameObject>();

    public IReadOnlyList<GameObject> Items => items;

    public void Add(GameObject item)
    {
        if (!items.Contains(item))
            items.Add(item);
    }

    public void Remove(GameObject item)
    {
        items.Remove(item);
    }
}
```

```csharp
public class RegisterToSet : MonoBehaviour
{
    [SerializeField] private RuntimeGameObjectSet runtimeSet;

    void OnEnable() => runtimeSet.Add(gameObject);
    void OnDisable() => runtimeSet.Remove(gameObject);
}
```

### Pattern 6: Stat Modifiers and Status Effects

```csharp
[CreateAssetMenu(menuName = "Game Data/Status Effect")]
public class StatusEffect : ScriptableObject
{
    public string effectName;
    public Sprite icon;
    public float duration;
    public bool isStackable;
    public bool isPermanent;

    [Header("Stat Modifications")]
    public float healthPerSecond;    // Positive = heal, Negative = damage
    public float moveSpeedMultiplier = 1f;
    public float attackDamageMultiplier = 1f;
    public float defenseMultiplier = 1f;

    [Header("Visual")]
    public Color tintColor = Color.white;
    public GameObject vfxPrefab;
}
```

---

## Data Persistence and Saving

### Editor Behavior

- Inspector modifications to ScriptableObject assets are automatically saved by the Editor.
- Programmatic changes in Edit mode require `EditorUtility.SetDirty()` followed by optional `AssetDatabase.SaveAssets()`.

### Runtime Behavior

- In standalone builds, ScriptableObject data is **read-only**. Changes exist only in memory and are lost when the application closes.
- In the Editor, runtime changes persist if saved — which can cause unintended data modification during Play mode testing.

### Saving Runtime Data

For persistent save data, serialize to JSON/binary and write to `Application.persistentDataPath`:

```csharp
// Save
string json = JsonUtility.ToJson(myScriptableObject);
File.WriteAllText(savePath, json);

// Load
string json = File.ReadAllText(savePath);
JsonUtility.FromJsonOverwrite(json, myScriptableObject);
```

---

## Best Practices

1. **Use `[CreateAssetMenu]`** on every ScriptableObject class to make asset creation easy for designers.
2. **Keep ScriptableObjects focused** — one type of data per class (Single Responsibility).
3. **Use ScriptableObjects for read-only config data** and separate systems for runtime mutable state.
4. **Reference ScriptableObjects via Inspector fields**, not hardcoded paths or `Resources.Load`.
5. **Be careful in Play mode** — changes to ScriptableObjects in the Editor during Play mode persist after stopping.
6. **Use `[PreferBinarySerialization]`** for ScriptableObjects with large arrays (textures, meshes, vertex data) to reduce file size and improve load times.
7. **Avoid storing runtime mutable state** in ScriptableObjects in builds unless you have a serialization strategy.
8. **Script filename must match the class name** for proper serialization.
9. **Unsaved runtime-created instances** get serialized into scene files if referenced by scene objects — use `HideFlags.DontSave` to prevent this.

---

## Architecture Example: Card Game Data

```
Assets/
  GameData/
    Cards/
      FireBolt.asset          (CardData)
      IceShield.asset         (CardData)
      HealingLight.asset      (CardData)
    Elements/
      Fire.asset              (ElementType)
      Water.asset             (ElementType)
      Earth.asset             (ElementType)
    StatusEffects/
      Burn.asset              (StatusEffect)
      Freeze.asset            (StatusEffect)
    Settings/
      EasyDifficulty.asset    (GameSettings)
      NormalDifficulty.asset  (GameSettings)
      HardDifficulty.asset    (GameSettings)
    Databases/
      CardDatabase.asset      (CardDatabase)
      ItemDatabase.asset      (ItemDatabase)
    Events/
      OnCardPlayed.asset      (CardEventChannel)
      OnTurnEnded.asset       (VoidEventChannel)
      OnHealthChanged.asset   (IntEventChannel)
```

This architecture allows designers to create and balance game content entirely through the Unity Editor, while programmers build systems that consume these data assets through serialized references.
