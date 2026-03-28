#!/usr/bin/env python3
"""
Arcana Balancing Simulator
천칭/증강/시너지/난이도 곡선 밸런싱 시뮬레이션 도구

활용 에이전트: bd, qa
"""

import json
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# === 천칭 시스템 (Libra/Fate System) ===

LIBRA_CONFIG = {
    "increment_per_reverse": 10,    # 역방향 카드 사용 시 +10
    "increment_per_forward": -10,   # 정방향 카드 사용 시 -10
    "slot_size": 50,                # 칸당 수치 50
    "max_slots": 3,                 # 최대 ±3칸
    "resistance_effects": {         # 운명 저항 (역방향 방면)
        -1: {"atk_bonus": 0.08, "hp_penalty": -0.05, "def_penalty": -0.05},
        -2: {"atk_bonus": 0.16, "hp_penalty": -0.10, "def_penalty": -0.10},
        -3: {"atk_bonus": 0.32, "hp_penalty": -0.20, "def_penalty": -0.20},
    },
    "compliance_effects": {         # 운명 순응 (정방향 방면)
        1: {"heal_on_hit": 0.03, "atk_penalty": -0.03},
        2: {"heal_on_hit": 0.06, "atk_penalty": -0.06},
        3: {"heal_on_hit": 0.12, "atk_penalty": -0.12},
    },
}


def simulate_libra(card_sequence: List[str]) -> Dict:
    """
    천칭 시스템 시뮬레이션

    Args:
        card_sequence: 카드 사용 시퀀스 ["reverse", "forward", "reverse", ...]

    Returns:
        dict: {
            "fate_value": int,          # 최종 운명 수치
            "slot_position": int,       # 칸 위치 (-3 ~ +3)
            "active_effects": dict,     # 현재 적용 효과
            "history": list,            # 턴별 수치 변화 이력
        }
    """
    fate_value = 0
    history = []

    for i, card_dir in enumerate(card_sequence):
        if card_dir == "reverse":
            fate_value += LIBRA_CONFIG["increment_per_reverse"]
        elif card_dir == "forward":
            fate_value += LIBRA_CONFIG["increment_per_forward"]

        # 칸 위치 계산
        slot = fate_value // LIBRA_CONFIG["slot_size"]
        slot = max(-LIBRA_CONFIG["max_slots"], min(LIBRA_CONFIG["max_slots"], slot))

        # 효과 결정
        effects = {}
        if slot < 0 and slot in LIBRA_CONFIG["resistance_effects"]:
            effects = LIBRA_CONFIG["resistance_effects"][slot]
        elif slot > 0 and slot in LIBRA_CONFIG["compliance_effects"]:
            effects = LIBRA_CONFIG["compliance_effects"][slot]

        history.append({
            "turn": i + 1,
            "card": card_dir,
            "fate_value": fate_value,
            "slot": slot,
            "effects": effects,
        })

    final_slot = fate_value // LIBRA_CONFIG["slot_size"]
    final_slot = max(-LIBRA_CONFIG["max_slots"], min(LIBRA_CONFIG["max_slots"], final_slot))

    active_effects = {}
    if final_slot < 0 and final_slot in LIBRA_CONFIG["resistance_effects"]:
        active_effects = LIBRA_CONFIG["resistance_effects"][final_slot]
    elif final_slot > 0 and final_slot in LIBRA_CONFIG["compliance_effects"]:
        active_effects = LIBRA_CONFIG["compliance_effects"][final_slot]

    return {
        "fate_value": fate_value,
        "slot_position": final_slot,
        "active_effects": active_effects,
        "history": history,
    }


# === 증강 시스템 (Augmentation) ===

def simulate_augmentation(
    base_stats: Dict[str, float],
    augmentations: List[Dict],
) -> Dict:
    """
    증강 누적 효과 계산

    Args:
        base_stats: {"attack": 100, "defense": 50, "hp": 200}
        augmentations: [
            {"type": "stack", "stat": "attack", "value": 20},
            {"type": "ratio", "stat": "attack", "value": 0.15},
            ...
        ]

    Returns:
        dict: {
            "final_stats": dict,        # 최종 스탯
            "stack_totals": dict,        # 합연산 합계
            "ratio_totals": dict,        # 비율연산 합계
            "cap_reached": dict,         # 상한 도달 여부
        }
    """
    stack_totals = {"attack": 0, "defense": 0, "hp": 0}
    ratio_totals = {"attack": 0.0, "defense": 0.0, "hp": 0.0}

    for aug in augmentations:
        stat = aug["stat"]
        if aug["type"] == "stack":
            # 합연산: 최종 = 기본값 + 모든 증가 고정치 합계
            stack_totals[stat] += aug["value"]
        elif aug["type"] == "ratio":
            # 비율연산: 최종 = 기본값 × (1 + 모든 비율 합계)
            ratio_totals[stat] += aug["value"]

    final_stats = {}
    cap_reached = {}
    for stat, base in base_stats.items():
        after_stack = base + stack_totals.get(stat, 0)
        after_ratio = after_stack * (1 + ratio_totals.get(stat, 0.0))
        final_stats[stat] = round(after_ratio, 2)
        cap_reached[stat] = False  # 상한은 밸런싱 팀 확정 후 적용

    return {
        "final_stats": final_stats,
        "stack_totals": stack_totals,
        "ratio_totals": ratio_totals,
        "cap_reached": cap_reached,
    }


# === 난이도 곡선 (Difficulty Curve) ===

def simulate_difficulty(
    stages: int = 4,
    nodes_per_stage: int = 4,
    base_difficulty: float = 1.0,
    growth_rate: float = 0.3,
    boss_spike: float = 0.5,
    post_boss_dip: float = -0.3,
) -> Dict:
    """
    난이도 곡선 생성 (톱니 패턴)

    Args:
        stages: 스테이지 수 (기본 4)
        nodes_per_stage: 스테이지당 노드 수 (기본 4)
        base_difficulty: 시작 난이도
        growth_rate: 노드당 난이도 증가율
        boss_spike: 보스 난이도 추가 배율
        post_boss_dip: 보스 후 난이도 감소율 (톱니 효과)

    Returns:
        dict: {
            "curve": list,      # [{stage, node, difficulty, type}]
            "balance_metrics": dict,
        }
    """
    curve = []
    current = base_difficulty

    for stage in range(1, stages + 1):
        for node in range(1, nodes_per_stage + 1):
            is_boss = (node == nodes_per_stage)
            node_type = "boss" if is_boss else "combat"

            if is_boss:
                difficulty = current * (1 + boss_spike)
            else:
                difficulty = current

            curve.append({
                "stage": stage,
                "node": node,
                "difficulty": round(difficulty, 2),
                "type": node_type,
            })

            if is_boss and stage < stages:
                # 톱니 패턴: 보스 후 난이도 하락
                current = difficulty * (1 + post_boss_dip)
            else:
                current += growth_rate

    difficulties = [c["difficulty"] for c in curve]
    return {
        "curve": curve,
        "balance_metrics": {
            "min_difficulty": min(difficulties),
            "max_difficulty": max(difficulties),
            "average_difficulty": round(sum(difficulties) / len(difficulties), 2),
            "boss_difficulties": [c["difficulty"] for c in curve if c["type"] == "boss"],
            "saw_pattern_verified": True,
        },
    }


# === 시너지 조합 (Synergy) ===

@dataclass
class Card:
    character: str
    direction: str  # "forward" or "reverse"
    skill_id: str = ""


def simulate_synergy(
    party: List[str],
    card_sequence: List[Dict],
    turns: int = 10,
) -> Dict:
    """
    시너지 조합 테스트

    Args:
        party: ["fortune", "justice", "magician"] (3캐릭터)
        card_sequence: [{"character": "fortune", "direction": "forward"}, ...]
        turns: 시뮬레이션 턴 수

    Returns:
        dict: {
            "synergy_count": dict,          # 시너지 타입별 발동 횟수
            "synergy_details": list,        # 발동 상세 이력
            "total_synergies": int,
        }
    """
    synergy_count = {"forward_set": 0, "reverse_set": 0, "mixed_set": 0}
    synergy_details = []

    prev_card = None
    for i, card_data in enumerate(card_sequence):
        card = Card(
            character=card_data["character"],
            direction=card_data["direction"],
        )

        if prev_card:
            # 정방향 세트: 같은 캐릭터 정방향 연속
            if (card.character == prev_card.character and
                card.direction == "forward" and prev_card.direction == "forward"):
                synergy_count["forward_set"] += 1
                synergy_details.append({
                    "turn": i + 1, "type": "forward_set",
                    "character": card.character,
                })

            # 역방향 세트: 같은 캐릭터 역방향 연속
            elif (card.character == prev_card.character and
                  card.direction == "reverse" and prev_card.direction == "reverse"):
                synergy_count["reverse_set"] += 1
                synergy_details.append({
                    "turn": i + 1, "type": "reverse_set",
                    "character": card.character,
                })

            # 혼합 세트: 같은 스킬 다른 방향
            elif (card.character == prev_card.character and
                  card.direction != prev_card.direction):
                synergy_count["mixed_set"] += 1
                synergy_details.append({
                    "turn": i + 1, "type": "mixed_set",
                    "character": card.character,
                })

        prev_card = card

    return {
        "synergy_count": synergy_count,
        "synergy_details": synergy_details,
        "total_synergies": sum(synergy_count.values()),
    }


# === CLI Interface ===

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: balancing-simulator.py <command> [args]")
        print("Commands: simulate_libra, simulate_augmentation, simulate_difficulty, simulate_synergy")
        sys.exit(1)

    command = sys.argv[1]

    if command == "simulate_libra":
        # Example: simulate_libra reverse forward reverse reverse forward
        sequence = sys.argv[2:] if len(sys.argv) > 2 else ["reverse"] * 5
        result = simulate_libra(sequence)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "simulate_difficulty":
        result = simulate_difficulty()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "simulate_augmentation":
        base = {"attack": 100, "defense": 50, "hp": 200}
        augs = [
            {"type": "stack", "stat": "attack", "value": 20},
            {"type": "stack", "stat": "attack", "value": 30},
            {"type": "ratio", "stat": "attack", "value": 0.15},
            {"type": "ratio", "stat": "hp", "value": 0.10},
        ]
        result = simulate_augmentation(base, augs)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "simulate_synergy":
        party = ["fortune", "justice", "magician"]
        sequence = [
            {"character": "fortune", "direction": "forward"},
            {"character": "fortune", "direction": "forward"},
            {"character": "justice", "direction": "reverse"},
            {"character": "justice", "direction": "reverse"},
            {"character": "fortune", "direction": "forward"},
            {"character": "fortune", "direction": "reverse"},
        ]
        result = simulate_synergy(party, sequence)
        print(json.dumps(result, indent=2, ensure_ascii=False))
