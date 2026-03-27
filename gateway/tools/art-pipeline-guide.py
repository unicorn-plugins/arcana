#!/usr/bin/env python3
"""
Arcana Art Asset Pipeline Guide
Spine 애니메이션-게임엔진 연동, 카드 이미지 규격 관리 도구

활용 에이전트: tech-director, animator
"""

import json
from typing import Dict

# 카드 이미지 규격
CARD_SPECS = {
    "card_full": {"width": 512, "height": 768, "format": "PNG", "color": "RGBA", "dpi": 72},
    "card_thumbnail": {"width": 128, "height": 192, "format": "PNG", "color": "RGBA", "dpi": 72},
    "card_frame_major": {"color": "gold (#FFD700)", "border_width": 4},
    "card_frame_minor": {"color": "silver (#C0C0C0)", "border_width": 3},
    "card_background": {
        "style": "단색 or 그라데이션, 아르누보 요소 가능",
        "character_colors": {
            "fortune": "#2E7D32",
            "justice": "#C62828",
            "magician": "#1565C0",
            "fool": "TBD",
            "judgment": "#F9A825",
        },
    },
    "card_layout": {
        "layers": ["background", "character", "frame", "name_plate"],
        "rules": [
            "캐릭터는 프레임 위로 그려질 수 있음",
            "캐릭터는 이름표에 가려짐",
            "프레임 바깥은 배경보다 어두운 같은 계열 단색",
        ],
    },
}

# Spine 애니메이션 규격
SPINE_SPECS = {
    "version": "4.1+",
    "export_format": "JSON (개발) / Binary (릴리즈)",
    "runtime": "spine-unity 4.1+",
    "atlas": {"max_size": 2048, "format": "PNG", "filter": "Linear"},
    "character_animations": {
        "required": ["idle", "move", "hit", "ko"],
        "combat": ["skill_forward", "skill_reverse", "ultimate"],
        "optional": ["victory", "special"],
    },
    "frame_rate": 24,
    "naming_convention": {
        "skeleton": "{character_id}_skeleton.json",
        "atlas": "{character_id}_atlas.atlas",
        "texture": "{character_id}_atlas.png",
    },
}

# 스프라이트 규격
SPRITE_SPECS = {
    "character": {"ppu": 100, "pivot": "bottom_center", "mesh_type": "tight", "filter": "bilinear"},
    "background": {"ppu": 100, "pivot": "center", "mesh_type": "full_rect", "filter": "bilinear"},
    "ui": {"ppu": 100, "pivot": "center", "mesh_type": "full_rect", "filter": "point"},
    "vfx": {"ppu": 100, "pivot": "center", "mesh_type": "tight", "filter": "bilinear"},
}

# 에셋 네이밍 컨벤션
NAMING_CONVENTION = {
    "character_sprite": "chr_{character_id}_{state}.png",
    "background": "bg_{stage_id}_{layer}_{variant}.png",
    "card_art": "card_{character_id}_{direction}.png",
    "vfx": "vfx_{effect_name}_{frame:03d}.png",
    "ui_element": "ui_{category}_{element_name}.png",
    "icon": "ico_{category}_{name}.png",
}


def check_spec(asset_type: str) -> Dict:
    """에셋 유형별 규격 조회"""
    specs = {
        "card": CARD_SPECS,
        "spine": SPINE_SPECS,
        "sprite": SPRITE_SPECS,
        "naming": NAMING_CONVENTION,
    }
    if asset_type in specs:
        return {"asset_type": asset_type, "spec": specs[asset_type]}
    return {"error": f"Unknown type. Available: {list(specs.keys())}"}


def generate_guide(guide_type: str = "full") -> Dict:
    """아트 파이프라인 가이드 생성"""
    if guide_type == "card":
        return {"guide": "Card Art Pipeline", "spec": CARD_SPECS}
    elif guide_type == "spine":
        return {"guide": "Spine Animation Pipeline", "spec": SPINE_SPECS}
    elif guide_type == "sprite":
        return {"guide": "Sprite Import Pipeline", "spec": SPRITE_SPECS}
    elif guide_type == "naming":
        return {"guide": "Asset Naming Convention", "spec": NAMING_CONVENTION}
    else:
        return {
            "guide": "Full Art Pipeline Guide",
            "card_spec": CARD_SPECS,
            "spine_spec": SPINE_SPECS,
            "sprite_spec": SPRITE_SPECS,
            "naming": NAMING_CONVENTION,
            "engine_checklist": [
                "Unity URP 2D Renderer 설정 확인",
                "Sprite Atlas 그룹 설정 (sorting layer별)",
                "Spine-Unity 런타임 패키지 설치",
                "2D Lighting 설정 (Light2D 컴포넌트)",
                "TextMeshPro 폰트 에셋 생성",
                "Addressables 그룹 구성 (스테이지별)",
            ],
        }


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate_guide"
    if cmd == "check_spec":
        asset_type = sys.argv[2] if len(sys.argv) > 2 else "card"
        print(json.dumps(check_spec(asset_type), indent=2, ensure_ascii=False))
    else:
        guide_type = sys.argv[2] if len(sys.argv) > 2 else "full"
        print(json.dumps(generate_guide(guide_type), indent=2, ensure_ascii=False))
