# Game QA Testing Methodology

> Source: https://www.gamedeveloper.com/production/game-qa-best-practices, https://www.istqb.org
> Fetched: 2026-03-27

## Overview

Game QA goes beyond traditional software testing. It must verify fun, balance, fairness, and player experience alongside functional correctness. This guide covers testing methodologies tailored for card-based roguelite games.

## Testing Types

### 1. Functional Testing
Verify that game features work as specified.

| Area | Test Focus |
|------|-----------|
| Combat | Turn order, damage calculation, targeting |
| Cards | Draw, play, discard, synergy detection |
| 천칭 System | Increment/decrement, slot effects, reset per node |
| Augmentation | Stack/ratio application, selection UI |
| Node Map | Navigation, event/combat node appearance |
| Save/Load | Reincarnation data persistence, totem preservation |

### 2. Balance Testing
Verify game difficulty is fair and fun.

**Approaches:**
- **Automated simulation**: Run thousands of battles with random card plays
- **Targeted builds**: Test specific party compositions against each boss
- **Extreme case testing**: Max augmentation stacks, all buffs/debuffs active

### 3. Regression Testing
Verify that bug fixes don't break existing features.

- Run full test suite after each sprint
- Maintain automated regression suite in Unity Test Framework
- Prioritize tests for core systems (combat, cards, 천칭)

### 4. Exploratory Testing
Unscripted testing to discover unexpected bugs.

- **Session-based**: 90-minute focused sessions with a charter
- **Charter examples**:
  - "Explore synergy interactions when party members die mid-combat"
  - "Explore 천칭 extreme values during boss phase transitions"
  - "Explore augmentation stacking across multiple reincarnations"

### 5. Compatibility Testing
Verify game works across PC hardware configurations.

| Config | Specs |
|--------|-------|
| Minimum | Intel i3 / 4GB RAM / Intel HD 4000 |
| Recommended | Intel i5 / 8GB RAM / GTX 1050 |
| High-end | Intel i7 / 16GB RAM / RTX 3060 |

## Testing Techniques

### Boundary Value Analysis (BVA)

Test at the edges of valid input ranges.

**천칭 System:**
| Test | Input | Expected |
|------|-------|----------|
| Just below slot boundary | 운명 수치 = 49 | No effect change |
| Exactly at boundary | 운명 수치 = 50 | Move to slot -1 |
| Just above boundary | 운명 수치 = 51 | Stay at slot -1 |
| Max negative | 운명 수치 = 150 | Slot -3, effects capped |
| Max positive | 운명 수치 = -150 | Slot +3, effects capped |
| Exact zero | 운명 수치 = 0 | Neutral, no effects |

**Cost System:**
| Test | Input | Expected |
|------|-------|----------|
| Cost = 0 | Play card | Cannot play |
| Cost = 1 | Play single-target card (cost 1) | Allowed, cost → 0 |
| Cost = 10 (max) | Recovery +3 | Stay at 10 (capped) |
| Unused cost carryover | End turn with 7 cost | Next turn: 7 + 3 = 10 |

### Combinatorial Testing

Test combinations of game elements systematically.

**Party × Boss Matrix:**
| Party | Chariot | Justice | Hermit | Emperor | World |
|-------|---------|---------|--------|---------|-------|
| Fortune + Justice + Magician | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fortune + Justice + Fool | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fortune + Magician + Fool | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fortune + Justice + Judgment | ✓ | ✓ | ✓ | ✓ | ✓ |
| ... | ... | ... | ... | ... | ... |

**Synergy × 천칭 State:**
- All 3 synergy types × 7 천칭 positions (-3 to +3)
- Total: 21 test combinations

### Pairwise Testing
When full combinatorial testing is too large, use pairwise (2-way) coverage:
- Every pair of parameter values appears in at least one test case
- Reduces test count from thousands to dozens
- Tools: PICT (Microsoft), AllPairs

### Exploratory Testing Charters

**Charter Template:**
```
EXPLORE [feature/area]
WITH [specific tool/technique/scenario]
TO DISCOVER [risks/bugs/issues]
TIME BOX: 90 minutes
```

**Example Charters for Arcana:**
1. "EXPLORE 천칭 system WITH rapid alternating forward/reverse cards TO DISCOVER boundary oscillation bugs — 90min"
2. "EXPLORE augmentation stacking WITH max reincarnation totems active TO DISCOVER stat overflow — 90min"
3. "EXPLORE The World boss 3rd phase WITH instant-death pattern at 3-turn mark TO DISCOVER edge cases — 90min"

## Test Case Template

```
TC-[번호]: [테스트 제목]
Priority: [Critical/High/Medium/Low]
Precondition: [사전 조건]
Steps:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
Expected Result: [기대 결과]
Actual Result: [실제 결과]
Status: [Pass/Fail/Block]
Notes: [비고]
```

### Example Test Cases

```
TC-001: 천칭 시스템 — 역방향 카드 사용 시 운명 수치 +10
Priority: Critical
Precondition: 전투 노드 입장, 천칭 초기화 상태 (운명 수치 = 0)
Steps:
  1. 역방향 스킬 카드 1장 사용
  2. 운명 수치 확인
Expected Result: 운명 수치 = +10
```

```
TC-015: 궁극기 — 3회 연속 사용 시 궁극기 카드 손패 진입
Priority: Critical
Precondition: 전투 중, Fortune 스킬 카드 3장 이상 보유
Steps:
  1. Fortune 스킬 카드 3회 연속 사용
  2. 손 덱 확인
Expected Result: Fortune 궁극기 카드가 손 덱에 추가됨
```

## 5대 테스트 영역 (Arcana 특화)

### 1. 전투 밸런싱
- 모든 보스 패턴별 공략 가능성 (4 + 최종 3페이즈)
- 모든 파티 조합으로 각 보스 클리어 가능 여부
- 전투 시간 목표: 1회 윤회 15~20분 이내

### 2. 천칭 극단값
- -3칸 도달: 공격력 32% 증가 / HP 20% 감소 / 방어 20% 감소
- +3칸 도달: HP 12% 회복 / 공격 12% 감소
- 양쪽 극단 교차 시나리오

### 3. 증강 조합
- 합연산 + 비율연산 중복 소지 시 수치 상한
- 슬롯 귀속 vs 캐릭터 교체 시 증강 유지 확인
- 보스 노드 2회 호출 시 증강 선택 정상 작동

### 4. 윤회/토템
- 토템 다수 누적 (공격 + 방어 + HP 토템) 시 밸런스
- 윤회 시 증강 초기화, 토템 유지 확인
- 토템 삭제 불가 규칙 확인

### 5. 시너지/특수 카드
- 정방향 세트 + 역방향 세트 + 혼합 세트 모든 캐릭터 조합
- 특수 카드 드롭 타이밍 (잡몹 전투 불능 다음 아군 턴)
- 특수 카드 코스트 0 확인, 시너지 연계 가능 여부
