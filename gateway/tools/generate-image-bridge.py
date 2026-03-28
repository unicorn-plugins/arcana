#!/usr/bin/env python3
"""
Arcana Image Generation Bridge
Gemini 기반 이미지 생성 API 브릿지

지원 모델:
  - flash: gemini-2.5-flash-image (빠른 생성, 일반 컨셉)
  - pro:   nano-banana-pro-preview (고품질, 정교한 아트)

활용 에이전트: ad, ca, ba
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


# gateway/tools/.env 로드
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


# ── 모델 정의 ──────────────────────────────────────────────
MODELS = {
    "flash": {
        "id": "gemini-2.5-flash-image",
        "description": "빠른 생성, 일반 컨셉용 (Gemini 2.5 Flash)",
    },
    "pro": {
        "id": "nano-banana-pro-preview",
        "description": "고품질, 정교한 아트워크용 (Nano Banana Pro)",
    },
}

DEFAULT_MODEL = "flash"


# ── 도메인 프리셋 ──────────────────────────────────────────
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
    "worldview_concept": {
        "style": "2D dark fantasy concept art, epic scale, cinematic composition, atmospheric, mysterious",
        "negative": "3D, photorealistic, modern, cute, childish, anime",
    },
}

SYSTEM_PROMPT = (
    "Always use a clean white background (#FFFFFF) for all generated images. "
    "Do NOT include speech bubbles, thought bubbles, captions, subtitles, narration text, or any floating text overlay in the image. "
    "Scene-appropriate signage that naturally appears in the environment (e.g. traffic signs, store signs, stage banners) is acceptable. "
    "All other text must be omitted entirely."
)


def generate_image(
    prompt: str,
    preset: str = "character_concept",
    model: str = DEFAULT_MODEL,
    width: int = 1024,
    height: int = 1024,
    output_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Gemini API를 사용하여 이미지 생성

    Args:
        prompt: 이미지 생성 프롬프트
        preset: 도메인 프리셋
        model: 모델 선택 ("flash" 또는 "pro")
        width: 이미지 너비
        height: 이미지 높이
        output_path: 저장 경로 (None이면 자동 생성)
        api_key: Gemini API 키 (None이면 .env에서 로드)

    Returns:
        dict: {"success": bool, "path": str, "prompt_used": str, "model_used": str}
    """
    if preset not in DOMAIN_PRESETS:
        return {"success": False, "error": f"Unknown preset. Available: {list(DOMAIN_PRESETS.keys())}"}

    if model not in MODELS:
        return {"success": False, "error": f"Unknown model. Available: {list(MODELS.keys())}"}

    # API 키 확인
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return {"success": False, "error": "GEMINI_API_KEY not found. Set it in gateway/tools/.env"}

    style = DOMAIN_PRESETS[preset]
    full_prompt = f"{prompt}, {style['style']}"
    model_id = MODELS[model]["id"]

    # 출력 경로 설정
    if not output_path:
        output_dir = Path("output/design")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"generated_{preset}.png")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        client = genai.Client(api_key=key)

        response = client.models.generate_content(
            model=model_id,
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                system_instruction=SYSTEM_PROMPT,
            ),
        )

        # 결과 저장
        text_output = None
        image_saved = False

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_output = part.text
            elif part.inline_data is not None:
                with open(out, "wb") as f:
                    f.write(part.inline_data.data)
                image_saved = True

        if image_saved:
            return {
                "success": True,
                "path": str(out),
                "model_used": f"{model} ({model_id})",
                "prompt_used": full_prompt,
                "negative_prompt": style["negative"],
                "dimensions": f"{width}x{height}",
                "text_response": text_output,
            }
        else:
            return {
                "success": False,
                "error": "No image generated in response",
                "model_used": f"{model} ({model_id})",
                "text_response": text_output,
                "prompt_used": full_prompt,
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model_used": f"{model} ({model_id})",
            "prompt_used": full_prompt,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Arcana Image Generation Bridge (Gemini)",
        epilog="""
Models:
  flash  gemini-2.5-flash-image       빠른 생성, 일반 컨셉용
  pro    nano-banana-pro-preview      고품질, 정교한 아트워크용

Examples:
  python generate-image-bridge.py --prompt "운명의 신전" --preset worldview_concept
  python generate-image-bridge.py --prompt "타로 카드 디자인" --preset card_art --model pro
  python generate-image-bridge.py --prompt "반란군 캐릭터" --preset character_concept --model flash --output output/design/rebel.png
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", type=str, required=True, help="Image generation prompt")
    parser.add_argument("--preset", type=str, default="character_concept",
                        choices=list(DOMAIN_PRESETS.keys()), help="Domain preset")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        choices=list(MODELS.keys()),
                        help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--api-key", type=str, default=None, help="Gemini API key (overrides .env)")

    args = parser.parse_args()
    result = generate_image(
        args.prompt, args.preset,
        model=args.model,
        output_path=args.output,
        api_key=args.api_key,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
