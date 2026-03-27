#!/usr/bin/env python3
"""
Arcana Image Generation Bridge
Gemini 기반 이미지 생성 API 브릿지

활용 에이전트: art-director, character-artist, background-artist
"""

import json
from typing import Dict, Optional


DOMAIN_PRESETS = {
    "character_concept": {
        "style": "2D game character art, dark fantasy tarot theme, renaissance era, detailed",
        "negative": "3D, photorealistic, modern clothing, gore, childish",
    },
    "card_art": {
        "style": "tarot card illustration, art nouveau border, gold frame, mystical atmosphere",
        "negative": "photorealistic, 3D render, modern, minimalist",
    },
    "background_concept": {
        "style": "2D game background, dark fantasy, medieval architecture, atmospheric lighting",
        "negative": "3D, photorealistic, modern buildings, sci-fi",
    },
    "vfx_reference": {
        "style": "2D game visual effect, particle effect, magical energy, stylized",
        "negative": "photorealistic, 3D render",
    },
}


def generate_image(
    prompt: str,
    preset: str = "character_concept",
    width: int = 1024,
    height: int = 1024,
    output_path: Optional[str] = None,
) -> Dict:
    """
    참고 이미지 생성 (Gemini API 연동)

    Args:
        prompt: 이미지 생성 프롬프트
        preset: 도메인 프리셋 (character_concept, card_art, background_concept, vfx_reference)
        width: 이미지 너비
        height: 이미지 높이
        output_path: 저장 경로 (None이면 임시 경로)

    Returns:
        dict: {"success": bool, "path": str, "prompt_used": str}
    """
    if preset not in DOMAIN_PRESETS:
        return {"error": f"Unknown preset. Available: {list(DOMAIN_PRESETS.keys())}"}

    style = DOMAIN_PRESETS[preset]
    full_prompt = f"{prompt}, {style['style']}"

    # NOTE: 실제 Gemini API 호출은 generate_image 커스텀 앱 (DMAP 마켓플레이스)을 통해 수행
    # 이 브릿지는 프롬프트 조합 및 프리셋 관리 역할

    return {
        "success": True,
        "prompt_used": full_prompt,
        "negative_prompt": style["negative"],
        "dimensions": f"{width}x{height}",
        "output_path": output_path or f"output/design/generated_{preset}.png",
        "note": "Gemini API 호출은 generate_image 커스텀 앱을 통해 수행됩니다.",
    }


if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Fortune character, wheel of fortune tarot"
    preset = sys.argv[2] if len(sys.argv) > 2 else "character_concept"
    result = generate_image(prompt, preset)
    print(json.dumps(result, indent=2, ensure_ascii=False))
