# Bug Tracking & Reporting Guide

> Source: https://www.gamedeveloper.com/programming/bug-tracking-best-practices
> Fetched: 2026-03-27

## Bug Report Template

```
Bug ID: [BUG-XXXX]
Title: [간결한 버그 제목]
Reporter: [보고자]
Date: [YYYY-MM-DD]
Build: [빌드 버전]

Severity: [Critical / Major / Minor / Trivial]
Priority: [P1 / P2 / P3 / P4]
Status: [New / Confirmed / In Progress / Fixed / Verified / Closed / Won't Fix]
Assignee: [담당자]

Category: [Combat / Cards / UI / 천칭 / Augmentation / Audio / Visual / Performance / Crash]

Precondition: [버그 발생 전 상태]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Result: [기대 결과]
Actual Result: [실제 결과]
Frequency: [Always / Often / Sometimes / Rare]

Attachments:
- [Screenshot / Video / Log file]

Environment:
- OS: [Windows 10/11]
- Resolution: [1920x1080]
- Quality: [Low/Medium/High]
- Unity Version: [6000.x]
```

## Severity Classification

| Severity | Definition | Example | Response Time |
|----------|-----------|---------|---------------|
| **Critical** | Game-breaking, crash, data loss | 전투 중 크래시, 세이브 파일 손상, 무한 루프 | Fix immediately |
| **Major** | Feature broken, no workaround | 천칭 시스템 수치 미적용, 궁극기 미발동, 카드 드로우 실패 | Fix this sprint |
| **Minor** | Feature partially broken, workaround exists | 시너지 하이라이트 표시 안됨, 잘못된 사운드 재생 | Fix before milestone |
| **Trivial** | Cosmetic, no gameplay impact | 오타, 미세한 정렬 오차, 아이콘 해상도 | Fix when available |

## Priority Classification

| Priority | Definition | Criteria |
|----------|-----------|----------|
| **P1** | Must fix before next build | Critical severity OR affects core loop |
| **P2** | Must fix before milestone | Major severity OR affects user experience |
| **P3** | Should fix before release | Minor severity, non-blocking |
| **P4** | Nice to fix | Trivial, cosmetic only |

### Severity × Priority Matrix

| | Critical | Major | Minor | Trivial |
|---|---------|-------|-------|---------|
| **Core Loop** (전투/카드) | P1 | P1 | P2 | P3 |
| **Sub System** (천칭/증강) | P1 | P2 | P3 | P4 |
| **UI/UX** | P2 | P2 | P3 | P4 |
| **Audio/Visual** | P2 | P3 | P3 | P4 |
| **Performance** | P1 | P2 | P3 | P4 |

## Bug Categories for Arcana

### Combat Bugs
- Turn order incorrect
- Damage calculation wrong
- Targeting error (single vs multi)
- Death/KO not triggering
- Cost calculation error

### Card Bugs
- Draw count incorrect (should be 6)
- Synergy not detected
- Card stuck in hand (can't play/discard)
- Card effect not applied
- Ultimate gauge incorrect

### 천칭 System Bugs
- Increment/decrement not applied
- Slot effect not triggered at boundary
- Visual not matching actual value
- Not resetting on new combat node
- Overflow beyond ±3 slots

### Augmentation Bugs
- Wrong augmentation offered
- Duplicate identical augmentation in same selection
- Stack/ratio calculation error
- Augmentation lost on party change
- Slot binding incorrect

### Performance Bugs
- FPS drop below target (60fps)
- Memory leak (increasing usage over time)
- Load time exceeds target (3 seconds)
- GC spike causing frame hitch
- Audio cutting out

## Bug Lifecycle

```
New → Confirmed → In Progress → Fixed → Verified → Closed
  ↓                    ↓           ↓
  Won't Fix        Reopened    Failed Verification
  Duplicate                      → In Progress
  Cannot Reproduce
```

### Status Definitions

| Status | Who Sets | Meaning |
|--------|---------|---------|
| New | QA | Bug reported, not yet reviewed |
| Confirmed | QA Lead | Bug reproduced, assigned to developer |
| In Progress | Developer | Fix is being worked on |
| Fixed | Developer | Fix committed, awaiting verification |
| Verified | QA | Fix confirmed working |
| Closed | QA Lead | Bug resolved, no further action |
| Won't Fix | PD/PM | Decision not to fix (by design, out of scope) |
| Duplicate | QA | Same as existing bug report |
| Cannot Reproduce | QA | Unable to reproduce after multiple attempts |

## Regression Testing After Fix

When a bug is marked "Fixed":

1. **Verify the fix**: Reproduce exact steps — bug should not occur
2. **Test related features**: Ensure fix didn't break related functionality
3. **Edge cases**: Test boundary values near the fixed area
4. **Different configurations**: Test on different quality settings / resolutions
5. **Mark as Verified** or **Reopen** with additional information

## Metrics to Track

| Metric | Target | Measured |
|--------|--------|---------|
| Open Critical bugs | 0 at release | Per build |
| Open Major bugs | < 5 at release | Per build |
| Bug find rate | Decreasing trend | Per sprint |
| Bug fix rate | > bug find rate | Per sprint |
| Fix verification turnaround | < 2 days | Average |
| Regression bugs | < 5% of total fixes | Per milestone |

## Tools

| Tool | Purpose | Cost |
|------|---------|------|
| GitHub Issues | Bug tracking (code-integrated) | Free |
| Jira | Full-featured issue tracking | Free (10 users) |
| Linear | Modern issue tracking | Free (small teams) |
| Unity Bug Reporter | In-engine crash reporting | Built-in |
| OBS Studio | Bug video recording | Free |
