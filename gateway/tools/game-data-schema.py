#!/usr/bin/env python3
"""
Arcana Game Data Schema Generator
캐릭터/스킬/증강/몬스터/보스 JSON 스키마 생성 도구

활용 에이전트: programmer, bd
"""

import json
import os
from typing import Dict


SCHEMAS = {
    "character": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Character Data",
        "type": "object",
        "required": ["id", "name", "arcana", "role", "baseStats", "skills"],
        "properties": {
            "id": {"type": "string", "description": "캐릭터 고유 ID (예: fortune, justice)"},
            "name": {"type": "string", "description": "캐릭터 표시 이름"},
            "arcana": {"type": "string", "enum": ["major", "minor"], "description": "메이저/마이너 아르카나"},
            "role": {"type": "string", "enum": ["support", "tank", "dps", "hybrid"], "description": "전투 역할"},
            "baseStats": {
                "type": "object",
                "required": ["attack", "defense", "hp"],
                "properties": {
                    "attack": {"type": "number", "minimum": 0},
                    "defense": {"type": "number", "minimum": 0},
                    "hp": {"type": "number", "minimum": 1},
                },
            },
            "growthCurve": {
                "type": "object",
                "properties": {
                    "youth": {"type": "number"},
                    "adult": {"type": "number"},
                    "elder": {"type": "number"},
                },
            },
            "skills": {
                "type": "object",
                "required": ["forward", "reverse", "ultimate"],
                "properties": {
                    "forward": {"$ref": "#/definitions/skillRef"},
                    "reverse": {"$ref": "#/definitions/skillRef"},
                    "ultimate": {"$ref": "#/definitions/skillRef"},
                },
            },
            "passive": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        },
        "definitions": {
            "skillRef": {
                "type": "object",
                "required": ["id", "cost", "target"],
                "properties": {
                    "id": {"type": "string"},
                    "cost": {"type": "integer", "minimum": 0, "maximum": 10},
                    "target": {"type": "string", "enum": ["single_enemy", "all_enemies", "single_ally", "all_allies", "self"]},
                },
            },
        },
    },

    "skill": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Skill Data",
        "type": "object",
        "required": ["id", "name", "direction", "cost", "target", "effects"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "direction": {"type": "string", "enum": ["forward", "reverse", "ultimate"]},
            "cost": {"type": "integer", "minimum": 0, "maximum": 10},
            "target": {"type": "string", "enum": ["single_enemy", "all_enemies", "single_ally", "all_allies", "self"]},
            "effects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["type", "value"],
                    "properties": {
                        "type": {"type": "string", "enum": ["damage", "heal", "buff", "debuff", "remove_debuff", "remove_skill", "shield", "counter"]},
                        "value": {"type": "number"},
                        "stat": {"type": "string", "enum": ["attack", "defense", "hp"]},
                        "duration": {"type": "integer"},
                        "scaling": {"type": "string"},
                    },
                },
            },
        },
    },

    "augmentation": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Augmentation Data",
        "type": "object",
        "required": ["id", "name", "type", "target", "stat", "value"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "type": {"type": "string", "enum": ["stack", "ratio"], "description": "stack=합연산, ratio=비율연산"},
            "target": {"type": "string", "enum": ["slot", "all"], "description": "슬롯 귀속 or 전체"},
            "stat": {"type": "string", "enum": ["attack", "defense", "hp"]},
            "value": {"type": "number"},
            "nodeType": {"type": "string", "enum": ["combat", "boss"]},
        },
    },

    "monster": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Monster Data",
        "type": "object",
        "required": ["id", "name", "minorArcana", "stats", "skills"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "minorArcana": {"type": "string", "enum": ["pentacles", "swords", "cups", "wands"]},
            "stats": {
                "type": "object",
                "required": ["attack", "defense", "hp"],
                "properties": {
                    "attack": {"type": "number"},
                    "defense": {"type": "number"},
                    "hp": {"type": "number"},
                },
            },
            "skills": {
                "type": "array",
                "maxItems": 2,
                "items": {"type": "string"},
            },
            "patterns": {
                "type": "array",
                "maxItems": 6,
                "items": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "specialCardDrop": {"type": "string"},
        },
    },

    "boss": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Boss Data",
        "type": "object",
        "required": ["id", "name", "stage", "phases"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "stage": {"type": "integer", "minimum": 1, "maximum": 4},
            "phases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["phase", "skills"],
                    "properties": {
                        "phase": {"type": "integer"},
                        "hpThreshold": {"type": "number"},
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "ultimateCondition": {"type": "string"},
                    },
                },
            },
        },
    },

    "synergy": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Synergy Data",
        "type": "object",
        "required": ["id", "type", "condition", "effect"],
        "properties": {
            "id": {"type": "string"},
            "type": {"type": "string", "enum": ["forward_set", "reverse_set", "mixed_set"]},
            "condition": {"type": "string"},
            "effect": {"type": "object"},
        },
    },

    "event": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Arcana Event Node Data",
        "type": "object",
        "required": ["id", "name", "description", "choices"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "choices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["text", "effects"],
                    "properties": {
                        "text": {"type": "string"},
                        "effects": {"type": "array", "items": {"type": "object"}},
                    },
                },
            },
        },
    },
}


def generate_schema(schema_name: str, output_dir: str = ".") -> str:
    """JSON 스키마 파일 생성"""
    if schema_name not in SCHEMAS:
        return f"Error: Unknown schema '{schema_name}'. Available: {list(SCHEMAS.keys())}"

    filename = f"{schema_name}.schema.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(SCHEMAS[schema_name], f, indent=2, ensure_ascii=False)

    return f"Generated: {filepath}"


def validate_data(data_file: str, schema_name: str) -> Dict:
    """데이터 파일을 스키마로 검증 (기본 검증)"""
    if schema_name not in SCHEMAS:
        return {"valid": False, "error": f"Unknown schema: {schema_name}"}

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"valid": False, "error": str(e)}

    schema = SCHEMAS[schema_name]
    required = schema.get("required", [])
    missing = [r for r in required if r not in data]

    if missing:
        return {"valid": False, "missing_fields": missing}

    return {"valid": True, "fields_count": len(data)}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: game-data-schema.py <command> [args]")
        print("Commands: generate_schema <name> [output_dir], validate_data <file> <schema>")
        print(f"Available schemas: {list(SCHEMAS.keys())}")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "generate_schema":
        name = sys.argv[2] if len(sys.argv) > 2 else "character"
        out_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        print(generate_schema(name, out_dir))

    elif cmd == "validate_data":
        data_file = sys.argv[2]
        schema_name = sys.argv[3]
        result = validate_data(data_file, schema_name)
        print(json.dumps(result, indent=2))

    elif cmd == "generate_all":
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        os.makedirs(out_dir, exist_ok=True)
        for name in SCHEMAS:
            print(generate_schema(name, out_dir))
