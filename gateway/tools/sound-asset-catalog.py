#!/usr/bin/env python3
"""
Arcana Sound Asset Catalog
BGM/SFX 에셋 목록 및 상태 관리 도구

활용 에이전트: sd
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

CATALOG_FILE = "output/design/sound_catalog.json"

DEFAULT_CATALOG = {
    "bgm": {
        "main_menu": {"name": "메인 화면", "mood": "신비롭고 장엄", "style": "오케스트라 + 합창", "status": "planned", "file": None},
        "map_explore": {"name": "맵/노드 탐색", "mood": "긴장감 있는 탐색", "style": "미니멀 앰비언트", "status": "planned", "file": None},
        "battle_normal": {"name": "일반 전투", "mood": "빠른 템포", "style": "퍼커시브 + 현악", "status": "planned", "file": None},
        "battle_boss": {"name": "보스 전투", "mood": "압도적 긴장감", "style": "풀 오케스트라 + 코러스", "status": "planned", "file": None},
        "event_node": {"name": "사건 노드", "mood": "선택의 무게감", "style": "피아노 미니멀", "status": "planned", "file": None},
        "ending": {"name": "엔딩", "mood": "감동과 해방", "style": "서정적 오케스트라", "status": "planned", "file": None},
    },
    "sfx": {
        "card": {
            "draw": {"name": "카드 드로우", "style": "타로카드 넘기는 질감", "status": "planned"},
            "play_forward": {"name": "정방향 스킬", "style": "맑고 정돈된 사운드", "status": "planned"},
            "play_reverse": {"name": "역방향 스킬", "style": "왜곡·리버스 효과", "status": "planned"},
            "synergy": {"name": "시너지 발동", "style": "크리스탈 공명음", "status": "planned"},
        },
        "battle": {
            "hit": {"name": "타격", "style": "임팩트 사운드", "status": "planned"},
            "heal": {"name": "회복", "style": "부드러운 차임", "status": "planned"},
            "buff": {"name": "버프", "style": "상승 톤", "status": "planned"},
            "debuff": {"name": "디버프", "style": "하강 톤", "status": "planned"},
            "ultimate": {"name": "궁극기", "style": "웅장한 임팩트", "status": "planned"},
            "ko": {"name": "전투불능", "style": "무겁게 쓰러지는 소리", "status": "planned"},
        },
        "system": {
            "libra_shift": {"name": "천칭 기울기", "style": "기계적 기어 움직임", "status": "planned"},
            "augment_select": {"name": "증강 선택", "style": "마법 활성 사운드", "status": "planned"},
            "reincarnation": {"name": "윤회", "style": "시간 되돌림 효과", "status": "planned"},
            "totem_create": {"name": "토템 생성", "style": "결정화 사운드", "status": "planned"},
        },
        "environment": {
            "stage_transition": {"name": "스테이지 전환", "style": "문 열림/공간 이동", "status": "planned"},
            "event_appear": {"name": "사건 등장", "style": "신비로운 출현", "status": "planned"},
        },
    },
}

VALID_STATUSES = ["planned", "in_progress", "review", "complete"]


def manage_catalog(action: str, category: str = "", item_id: str = "", **kwargs) -> Dict:
    """
    사운드 에셋 카탈로그 관리

    Actions:
        init: 기본 카탈로그 생성
        list: 전체 카탈로그 조회
        status: 특정 항목 상태 업데이트
        summary: 상태별 요약 통계
    """
    catalog = _load_catalog()

    if action == "init":
        _save_catalog(DEFAULT_CATALOG)
        return {"success": True, "message": "카탈로그 초기화 완료"}

    elif action == "list":
        return {"catalog": catalog}

    elif action == "status":
        new_status = kwargs.get("status", "")
        if new_status not in VALID_STATUSES:
            return {"error": f"Invalid status. Use: {VALID_STATUSES}"}
        # Navigate to item and update
        if category in catalog and item_id in catalog[category]:
            catalog[category][item_id]["status"] = new_status
            _save_catalog(catalog)
            return {"success": True, "updated": f"{category}/{item_id} → {new_status}"}
        return {"error": f"Item not found: {category}/{item_id}"}

    elif action == "summary":
        counts = {s: 0 for s in VALID_STATUSES}
        total = 0
        for cat in catalog.values():
            if isinstance(cat, dict):
                for item in cat.values():
                    if isinstance(item, dict) and "status" in item:
                        counts[item["status"]] = counts.get(item["status"], 0) + 1
                        total += 1
                    elif isinstance(item, dict):
                        for sub in item.values():
                            if isinstance(sub, dict) and "status" in sub:
                                counts[sub["status"]] = counts.get(sub["status"], 0) + 1
                                total += 1
        return {"total": total, "by_status": counts}

    return {"error": f"Unknown action: {action}"}


def _load_catalog() -> Dict:
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CATALOG


def _save_catalog(catalog: Dict):
    os.makedirs(os.path.dirname(CATALOG_FILE), exist_ok=True)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "summary"
    result = manage_catalog(action)
    print(json.dumps(result, indent=2, ensure_ascii=False))
