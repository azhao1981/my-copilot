# -*- coding: utf-8 -*-
from typing import Dict


def merge_code_descriptions(descriptions: Dict[str, str]) -> str:
    return "\n\n".join(descriptions.values())


def merge_code(code_snippets: Dict[str, str]) -> str:
    parts = [f"文件名: {filename}\n```\n{content}\n```" for filename, content in code_snippets.items()]
    return "\n\n".join(parts)


def create_prompt(main_content: str, prefix: str = "", suffix: str = "") -> str:
    return f"{prefix}\n{main_content}\n{suffix}"
