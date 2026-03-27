#!/usr/bin/env python3
"""
Arcana Mermaid Diagram Validation Bridge
Mermaid 다이어그램 문법 검증 도구

활용 에이전트: pd, project-manager, uiux-designer
"""

import json
import re
import subprocess
from typing import Dict


MERMAID_KEYWORDS = {
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "erDiagram", "gantt", "pie", "gitgraph",
    "journey", "mindmap", "timeline",
}

COMMON_ERRORS = [
    (r"-->>\s*$", "Missing target after arrow"),
    (r"^\s*-->\s*$", "Arrow without source or target"),
    (r'\["\s*"\]', "Empty label"),
    (r"(participant|actor)\s*$", "Missing participant name"),
    (r"end\s+end", "Duplicate 'end' keyword"),
]


def validate_mermaid(diagram: str) -> Dict:
    """
    Mermaid 다이어그램 문법 검증

    Args:
        diagram: Mermaid 다이어그램 텍스트

    Returns:
        dict: {
            "valid": bool,
            "diagram_type": str,
            "errors": list,
            "warnings": list,
            "line_count": int,
        }
    """
    lines = diagram.strip().split("\n")
    errors = []
    warnings = []
    diagram_type = "unknown"

    if not lines:
        return {"valid": False, "errors": ["Empty diagram"], "diagram_type": "unknown"}

    # Detect diagram type
    first_line = lines[0].strip().lower()
    for kw in MERMAID_KEYWORDS:
        if first_line.startswith(kw.lower()):
            diagram_type = kw
            break

    if diagram_type == "unknown":
        errors.append(f"Line 1: Unknown diagram type. Expected one of: {MERMAID_KEYWORDS}")

    # Basic syntax checks
    bracket_stack = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("%%"):
            continue

        # Check common errors
        for pattern, message in COMMON_ERRORS:
            if re.search(pattern, stripped):
                errors.append(f"Line {i}: {message}")

        # Bracket matching
        for ch in stripped:
            if ch in "({[":
                bracket_stack.append((ch, i))
            elif ch in ")}]":
                if bracket_stack:
                    bracket_stack.pop()
                else:
                    errors.append(f"Line {i}: Unmatched closing bracket '{ch}'")

        # Check for very long lines
        if len(stripped) > 200:
            warnings.append(f"Line {i}: Very long line ({len(stripped)} chars)")

    # Unclosed brackets
    for ch, line_num in bracket_stack:
        errors.append(f"Line {line_num}: Unclosed bracket '{ch}'")

    return {
        "valid": len(errors) == 0,
        "diagram_type": diagram_type,
        "errors": errors,
        "warnings": warnings,
        "line_count": len(lines),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            diagram = f.read()
    else:
        # Example diagram
        diagram = """flowchart TD
    A[윤회 시작] --> B[증강 선택]
    B --> C[맵 노드 화면]
    C --> D{노드 선택}
    D -->|전투| E[전투 노드]
    D -->|사건| F[사건 노드]
    E --> G{클리어?}
    G -->|성공| H[증강 보상]
    G -->|실패| I[게임 오버]
    H --> J{보스?}
    J -->|아니오| C
    J -->|예| K[다음 스테이지]
    I --> L[토템 선택]
    L --> A
    K --> M{최종보스?}
    M -->|아니오| C
    M -->|예| N[엔딩]
"""

    result = validate_mermaid(diagram)
    print(json.dumps(result, indent=2, ensure_ascii=False))
