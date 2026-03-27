# Unity Test Framework Guide

> Source: https://docs.unity3d.com/Packages/com.unity.test-framework@latest
> Fetched: 2026-03-27

## Overview

Unity Test Framework (UTF) provides a testing environment based on NUnit, the .NET unit testing library. It supports two test modes for comprehensive game testing.

## Test Modes

### EditMode Tests
- Run in Unity Editor without entering Play mode
- Fast execution, no scene loading
- Test pure logic: damage formulas, deck shuffling, stat calculations
- Location: `Assets/Tests/EditMode/`

### PlayMode Tests
- Run in a scene with full Unity lifecycle (Start, Update, etc.)
- Test MonoBehaviour interactions, UI, coroutines
- Can run in Editor or standalone builds
- Location: `Assets/Tests/PlayMode/`

## Setup

### Assembly Definitions
```
Assets/Tests/
├── EditMode/
│   ├── EditModeTests.asmdef    (Test references: UnityEngine.TestRunner, UnityEditor.TestRunner)
│   └── CombatTests.cs
└── PlayMode/
    ├── PlayModeTests.asmdef    (Test references: UnityEngine.TestRunner)
    └── UITests.cs
```

### asmdef Settings
- Platform: Editor only (EditMode) or Any (PlayMode)
- References: Add your game's assembly definition
- Check "Test Assemblies" in Inspector

## EditMode Test Examples

### Testing Damage Formula
```csharp
using NUnit.Framework;

[TestFixture]
public class DamageCalculationTests
{
    [Test]
    public void BasicDamage_AttackMinusDefense()
    {
        float damage = CombatFormula.Calculate(attack: 100, defense: 30, multiplier: 1.0f);
        Assert.AreEqual(70f, damage);
    }

    [Test]
    public void DamageNeverNegative()
    {
        float damage = CombatFormula.Calculate(attack: 10, defense: 100, multiplier: 1.0f);
        Assert.GreaterOrEqual(damage, 0f);
    }

    [TestCase(-1, ExpectedResult = 0.08f)]
    [TestCase(-2, ExpectedResult = 0.16f)]
    [TestCase(-3, ExpectedResult = 0.32f)]
    public float LibraResistance_AttackBonus(int slot)
    {
        return LibraSystem.GetAttackBonus(slot);
    }

    [TestCase(1, ExpectedResult = 0.03f)]
    [TestCase(2, ExpectedResult = 0.06f)]
    [TestCase(3, ExpectedResult = 0.12f)]
    public float LibraCompliance_HealRate(int slot)
    {
        return LibraSystem.GetHealOnHitRate(slot);
    }
}

[TestFixture]
public class DeckTests
{
    [Test]
    public void DeckSize_ThreeCharacters_18Cards()
    {
        var party = new Party(3);
        var deck = new Deck(party);
        Assert.AreEqual(18, deck.TotalCards);
    }

    [Test]
    public void Draw_Returns6Cards()
    {
        var deck = CreateTestDeck(18);
        var hand = deck.Draw(6);
        Assert.AreEqual(6, hand.Count);
    }

    [Test]
    public void DeadCharacter_CardsRemovedFromDeck()
    {
        var deck = CreateTestDeck(18);
        deck.RemoveCharacterCards("fortune");
        Assert.AreEqual(12, deck.TotalCards); // 18 - 6
    }
}

[TestFixture]
public class AugmentationTests
{
    [Test]
    public void StackAugment_AddsToBase()
    {
        // 합연산: 최종 = 기본값 + 모든 증가치 합계
        int baseStat = 100;
        int augment1 = 20;
        int augment2 = 30;
        int result = AugmentCalculator.ApplyStack(baseStat, augment1, augment2);
        Assert.AreEqual(150, result);
    }

    [Test]
    public void RatioAugment_MultipliesBase()
    {
        // 비율연산: 최종 = 기본값 × (1 + 모든 비율 합계)
        float baseStat = 100f;
        float ratio1 = 0.1f;  // +10%
        float ratio2 = 0.2f;  // +20%
        float result = AugmentCalculator.ApplyRatio(baseStat, ratio1, ratio2);
        Assert.AreEqual(130f, result, 0.01f);
    }
}
```

### Testing Synergy Detection
```csharp
[TestFixture]
public class SynergyTests
{
    [Test]
    public void ForwardSet_SameCharacterForwardForward()
    {
        var card1 = new Card("fortune", Direction.Forward);
        var card2 = new Card("fortune", Direction.Forward);
        Assert.IsTrue(SynergyDetector.IsForwardSet(card1, card2));
    }

    [Test]
    public void ReverseSet_SameCharacterReverseReverse()
    {
        var card1 = new Card("justice", Direction.Reverse);
        var card2 = new Card("justice", Direction.Reverse);
        Assert.IsTrue(SynergyDetector.IsReverseSet(card1, card2));
    }

    [Test]
    public void MixedSet_SameSkillDifferentDirection()
    {
        var card1 = new Card("magician", Direction.Forward);
        var card2 = new Card("magician", Direction.Reverse);
        Assert.IsTrue(SynergyDetector.IsMixedSet(card1, card2));
    }

    [Test]
    public void NoSynergy_DifferentCharacters()
    {
        var card1 = new Card("fortune", Direction.Forward);
        var card2 = new Card("justice", Direction.Forward);
        Assert.IsFalse(SynergyDetector.HasAnySynergy(card1, card2));
    }
}
```

## PlayMode Test Examples

### Testing Turn Flow
```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine.TestTools;

public class TurnSystemTests
{
    [UnityTest]
    public IEnumerator PlayerTurn_DrawsCards_WaitsForInput()
    {
        var battleScene = SceneManager.LoadSceneAsync("BattleScene");
        yield return battleScene;

        var turnManager = Object.FindObjectOfType<TurnManager>();
        turnManager.StartBattle();
        yield return null;

        Assert.AreEqual(TurnPhase.PlayerTurn, turnManager.CurrentPhase);
        Assert.AreEqual(6, turnManager.PlayerHand.Count);
    }

    [UnityTest]
    public IEnumerator CostSystem_StartsAt10_Recovers3PerTurn()
    {
        yield return SetupBattle();
        var costSystem = Object.FindObjectOfType<CostSystem>();

        Assert.AreEqual(10, costSystem.CurrentCost);  // Full at start

        costSystem.SpendCost(5);
        Assert.AreEqual(5, costSystem.CurrentCost);

        yield return EndPlayerTurn();
        yield return EndEnemyTurn();  // Back to player turn

        Assert.AreEqual(8, costSystem.CurrentCost);  // 5 + 3 recovery
    }
}
```

## Running Tests

### Test Runner Window
```
Window → General → Test Runner
```
- EditMode tab: Run all edit mode tests
- PlayMode tab: Run all play mode tests
- Filter by name, category, or assembly
- Run All / Run Selected / Rerun Failed

### Command Line
```bash
# Run EditMode tests
Unity.exe -runTests -testPlatform EditMode -projectPath ./arcana

# Run PlayMode tests
Unity.exe -runTests -testPlatform PlayMode -projectPath ./arcana

# Output results
-testResults ./results.xml
```

## Best Practices

1. **Test pure logic in EditMode** (faster): damage, synergy, augmentation math
2. **Test interactions in PlayMode**: UI flow, coroutines, scene transitions
3. **Use [TestCase] for parametric tests**: boundary values, multiple inputs
4. **Name tests clearly**: `Method_Scenario_ExpectedResult`
5. **Test edge cases first**: empty deck, 0 HP, max augmentation stack
6. **Run tests before every commit**
