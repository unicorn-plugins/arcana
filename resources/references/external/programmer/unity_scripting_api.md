# Unity Scripting API (C#) Overview and Key Classes

> Source: https://docs.unity3d.com/ScriptReference/index.html
> Fetched: 2026-03-27

## Overview

The Unity Scripting API provides the complete set of classes, methods, properties, and events available to C# scripts within the Unity engine. It is organized by namespaces, with **UnityEngine** being the primary namespace for most game developers. The scripting reference covers everything from basic object manipulation to physics, rendering, audio, networking, and editor extensions.

## Key Namespaces

| Namespace | Description |
|-----------|-------------|
| **UnityEngine** | Core runtime classes (GameObjects, Components, Physics, Rendering, etc.) |
| **UnityEngine.UI** | Legacy UI system (Canvas, Button, Text, Image, etc.) |
| **UnityEngine.UIElements** | UI Toolkit (modern UI system) |
| **UnityEngine.SceneManagement** | Scene loading, unloading, and management |
| **UnityEngine.AI** | Navigation and pathfinding (NavMesh) |
| **UnityEngine.Audio** | Audio mixing and effects |
| **UnityEngine.Animations** | Animation system utilities |
| **UnityEngine.Events** | UnityEvent system for Inspector-configurable callbacks |
| **UnityEngine.InputSystem** | New Input System package |
| **UnityEngine.Rendering** | Scriptable Render Pipeline utilities |
| **UnityEditor** | Editor-only classes for custom tools (not available at runtime) |

---

## Core Classes

### MonoBehaviour

MonoBehaviour is the base class that most Unity scripts derive from. It provides lifecycle functions and must always exist as a Component of a GameObject.

#### Lifecycle Methods (Execution Order)

```
Initialization Phase:
  Awake() → OnEnable() → Start()

Update Phase (per frame):
  FixedUpdate() → Update() → LateUpdate()

Cleanup Phase:
  OnDisable() → OnDestroy()
```

**Initialization:**
- **Awake()** — Called when the script instance is loaded, before any Start calls. Use for initializing references between scripts.
- **OnEnable()** — Called each time the component or GameObject becomes active.
- **Start()** — Called before the first frame update, only once, after all Awake calls complete.

**Per-Frame Updates:**
- **FixedUpdate()** — Called at fixed time intervals (default 0.02s). Use for physics calculations and Rigidbody manipulation.
- **Update()** — Called once per frame. Use for most game logic, input polling, and non-physics movement.
- **LateUpdate()** — Called after all Update methods. Use for camera follow logic and post-processing of frame data.

**Cleanup:**
- **OnDisable()** — Called when the component or GameObject becomes inactive.
- **OnDestroy()** — Called when the component or GameObject is destroyed. Use for cleanup (unsubscribing events, releasing resources).

#### Physics Callbacks

**3D Collisions:**
- `OnCollisionEnter(Collision)` — When a collision with another collider begins.
- `OnCollisionStay(Collision)` — Each frame a collision persists.
- `OnCollisionExit(Collision)` — When a collision ends.

**3D Triggers:**
- `OnTriggerEnter(Collider)` — When another collider enters a trigger zone.
- `OnTriggerStay(Collider)` — Each frame a collider stays in the trigger.
- `OnTriggerExit(Collider)` — When a collider exits the trigger zone.

**2D Equivalents:**
- `OnCollisionEnter2D`, `OnCollisionStay2D`, `OnCollisionExit2D`
- `OnTriggerEnter2D`, `OnTriggerStay2D`, `OnTriggerExit2D`

#### Coroutine Methods

- **StartCoroutine(IEnumerator)** — Starts an asynchronous coroutine.
- **StopCoroutine(Coroutine)** — Stops a specific coroutine.
- **StopAllCoroutines()** — Stops all coroutines on this MonoBehaviour.

#### Invocation Methods

- **Invoke(string methodName, float time)** — Calls a method after a delay.
- **InvokeRepeating(string methodName, float time, float repeatRate)** — Calls a method repeatedly.
- **CancelInvoke()** — Cancels all pending Invoke calls.
- **IsInvoking()** — Returns true if any Invoke is pending.

#### Key Properties

- `enabled` — Whether the component receives Update calls.
- `isActiveAndEnabled` — Whether the component is active in the hierarchy.
- `gameObject` — The GameObject this component is attached to.
- `transform` — The Transform component on the same GameObject.
- `destroyCancellationToken` — A CancellationToken raised when the object is destroyed (useful for async/await).

---

### GameObject

The fundamental object in Unity scenes. Every entity in a scene is a GameObject.

**Key Methods:**
- `AddComponent<T>()` — Adds a component of type T.
- `GetComponent<T>()` — Retrieves a component of type T.
- `GetComponentInChildren<T>()` — Searches children for a component.
- `GetComponentInParent<T>()` — Searches parents for a component.
- `SetActive(bool)` — Activates or deactivates the GameObject.
- `Find(string name)` — Finds a GameObject by name (static, slow).
- `FindWithTag(string tag)` — Finds a GameObject by tag (static).
- `Instantiate(Object)` — Creates a clone (inherited from Object).
- `Destroy(Object)` — Destroys a GameObject or component (inherited from Object).

**Key Properties:**
- `activeSelf` — Whether this specific GameObject is active.
- `activeInHierarchy` — Whether this GameObject is active considering parent state.
- `tag` — The tag string assigned to this GameObject.
- `layer` — The layer index (used for physics, rendering masks).
- `scene` — The scene this GameObject belongs to.

---

### Transform

Represents position, rotation, and scale of a GameObject. Every GameObject has a Transform.

**Key Properties:**
- `position` / `localPosition` — World/local position (Vector3).
- `rotation` / `localRotation` — World/local rotation (Quaternion).
- `eulerAngles` / `localEulerAngles` — Rotation in Euler angles.
- `localScale` — Local scale.
- `forward`, `right`, `up` — Direction vectors in world space.
- `parent` — Parent Transform.
- `childCount` — Number of direct children.

**Key Methods:**
- `Translate(Vector3)` — Moves the transform.
- `Rotate(Vector3)` — Rotates the transform.
- `LookAt(Transform target)` — Faces toward a target.
- `SetParent(Transform parent)` — Sets the parent transform.
- `GetChild(int index)` — Gets child by index.
- `Find(string name)` — Finds a child by name.
- `TransformPoint(Vector3)` — Converts local to world position.
- `InverseTransformPoint(Vector3)` — Converts world to local position.

---

### Rigidbody / Rigidbody2D

Provides physics simulation to a GameObject.

**Key Properties:**
- `velocity` — Linear velocity vector.
- `angularVelocity` — Angular velocity.
- `mass` — Mass of the rigidbody.
- `drag` / `angularDrag` — Damping values.
- `useGravity` — Whether gravity applies.
- `isKinematic` — If true, not driven by physics engine.
- `constraints` — Freeze specific axes of movement/rotation.

**Key Methods:**
- `AddForce(Vector3, ForceMode)` — Applies a force.
- `AddTorque(Vector3, ForceMode)` — Applies rotational force.
- `MovePosition(Vector3)` — Moves to position respecting physics.
- `MoveRotation(Quaternion)` — Rotates respecting physics.

---

### Physics / Physics2D

Static classes for raycasting and physics queries.

**Key Static Methods:**
- `Raycast(Ray, out RaycastHit, float maxDistance)` — Casts a ray and returns hit info.
- `OverlapSphere(Vector3, float radius)` — Returns all colliders within a sphere.
- `SphereCast`, `BoxCast`, `CapsuleCast` — Various shape casts.
- `OverlapBox`, `OverlapCapsule` — Overlap queries.

---

### Camera

Represents a rendering viewpoint.

**Key Properties:**
- `main` — Returns the first enabled Camera tagged "MainCamera" (static).
- `fieldOfView` — Vertical field of view in degrees.
- `orthographic` — Whether the camera is orthographic.
- `orthographicSize` — Half-size of the orthographic view.
- `depth` — Rendering order among cameras.
- `cullingMask` — Layer mask for selective rendering.

**Key Methods:**
- `ScreenToWorldPoint(Vector3)` — Converts screen position to world position.
- `WorldToScreenPoint(Vector3)` — Converts world position to screen position.
- `ScreenPointToRay(Vector3)` — Creates a ray from screen position.
- `ViewportToWorldPoint(Vector3)` — Converts viewport position to world.

---

### Other Important Classes

| Class | Purpose |
|-------|---------|
| **Component** | Base class for all things attached to GameObjects |
| **Object** | Base class for all Unity objects; provides `Instantiate()`, `Destroy()`, `DontDestroyOnLoad()` |
| **Time** | `deltaTime`, `fixedDeltaTime`, `timeScale`, `time`, `unscaledDeltaTime` |
| **Debug** | `Log()`, `LogWarning()`, `LogError()`, `DrawRay()`, `DrawLine()` |
| **Input** | Legacy input: `GetKey()`, `GetAxis()`, `mousePosition` |
| **Application** | `dataPath`, `persistentDataPath`, `Quit()`, `isPlaying`, `platform` |
| **SceneManager** | `LoadScene()`, `LoadSceneAsync()`, `GetActiveScene()`, `sceneLoaded` event |
| **Resources** | `Load<T>()`, `LoadAll<T>()`, `UnloadUnusedAssets()` |
| **PlayerPrefs** | Simple key-value persistence: `SetInt()`, `GetInt()`, `SetString()`, etc. |
| **AudioSource** | `Play()`, `Pause()`, `Stop()`, `PlayOneShot()`, `volume`, `clip` |
| **Animator** | `SetTrigger()`, `SetBool()`, `SetFloat()`, `SetInteger()`, `Play()` |
| **Material** | `color`, `mainTexture`, `SetFloat()`, `SetColor()`, `SetTexture()` |
| **Mathf** | `Lerp()`, `Clamp()`, `Abs()`, `Sin()`, `Cos()`, `PI`, `Infinity` |
| **Vector3** | `Distance()`, `Lerp()`, `Normalize()`, `Dot()`, `Cross()`, `MoveTowards()` |
| **Quaternion** | `Euler()`, `LookRotation()`, `Slerp()`, `Lerp()`, `identity` |
| **Color** | `Lerp()`, `red`, `green`, `blue`, `white`, `black`, `clear` |
| **Random** | `Range()`, `insideUnitSphere`, `insideUnitCircle`, `rotation` |
| **Coroutine Yields** | `WaitForSeconds`, `WaitForFixedUpdate`, `WaitForEndOfFrame`, `WaitUntil` |

---

## Important Attributes

| Attribute | Purpose |
|-----------|---------|
| `[SerializeField]` | Exposes private fields in the Inspector |
| `[HideInInspector]` | Hides a public field from the Inspector |
| `[Header("text")]` | Adds a header label in the Inspector |
| `[Tooltip("text")]` | Adds hover tooltip in the Inspector |
| `[Space]` | Adds vertical spacing in the Inspector |
| `[Range(min, max)]` | Clamps a numeric field with a slider |
| `[RequireComponent(typeof(T))]` | Auto-adds component T when this script is added |
| `[DisallowMultipleComponent]` | Prevents multiple instances on one GameObject |
| `[ExecuteInEditMode]` | Runs lifecycle methods in the Editor |
| `[CreateAssetMenu]` | Creates a menu item for ScriptableObject assets |
| `[Serializable]` | Marks a class/struct as serializable |
| `[System.NonSerialized]` | Prevents a field from being serialized |
| `[AddComponentMenu("path")]` | Customizes the Add Component menu location |

---

## Common Usage Patterns

### Getting References

```csharp
// In Inspector (preferred)
[SerializeField] private Rigidbody rb;

// In Awake (runtime)
private Rigidbody rb;
void Awake() {
    rb = GetComponent<Rigidbody>();
}

// Finding objects
GameObject player = GameObject.FindWithTag("Player");
Camera cam = Camera.main;
```

### Coroutine Pattern

```csharp
IEnumerator FadeOut(float duration) {
    float elapsed = 0f;
    while (elapsed < duration) {
        float alpha = Mathf.Lerp(1f, 0f, elapsed / duration);
        spriteRenderer.color = new Color(1, 1, 1, alpha);
        elapsed += Time.deltaTime;
        yield return null; // Wait one frame
    }
}

// Start it
StartCoroutine(FadeOut(2f));
```

### Async/Await Pattern (Modern)

```csharp
async void LoadSceneAsync() {
    AsyncOperation op = SceneManager.LoadSceneAsync("GameScene");
    while (!op.isDone) {
        float progress = Mathf.Clamp01(op.progress / 0.9f);
        loadingBar.fillAmount = progress;
        await Task.Yield();
    }
}
```

### Singleton Pattern

```csharp
public class GameManager : MonoBehaviour {
    public static GameManager Instance { get; private set; }

    void Awake() {
        if (Instance != null && Instance != this) {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

### Object Pooling

```csharp
Queue<GameObject> pool = new Queue<GameObject>();

GameObject GetFromPool() {
    if (pool.Count > 0) {
        GameObject obj = pool.Dequeue();
        obj.SetActive(true);
        return obj;
    }
    return Instantiate(prefab);
}

void ReturnToPool(GameObject obj) {
    obj.SetActive(false);
    pool.Enqueue(obj);
}
```

---

## Performance Tips

1. **Cache component references** in `Awake()` instead of calling `GetComponent()` repeatedly.
2. **Avoid `Find()` methods** in Update loops; use serialized references or tags.
3. **Use object pooling** instead of frequent Instantiate/Destroy calls.
4. **Prefer `CompareTag("Tag")`** over `== "Tag"` to avoid garbage allocation.
5. **Use `FixedUpdate()`** for physics, `Update()` for input and logic, `LateUpdate()` for camera.
6. **Minimize `SendMessage()`** calls; use direct references or events instead.
7. **Use the new Input System** package instead of legacy `Input` class for better performance and flexibility.
