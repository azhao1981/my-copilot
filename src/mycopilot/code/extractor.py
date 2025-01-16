# -*- coding: utf-8 -*-
import re
from typing import List
from pydantic import BaseModel
import os


class CodeSnippet(BaseModel):
    filename: str
    code: str


class MarkdownParser:
    def parse_markdown(self, markdown_content: str) -> List[CodeSnippet]:
        code_snippets: List[CodeSnippet] = []
        # 匹配以 "** 数字. `文件名`**" 或 "** `文件名`**" 开头的行，后跟代码块
        pattern = r"^\s*\**\s*(?:\d+\.\s*)?`(?P<filename>[^`]+)`\s*\**\s*\n```(?P<language>\w*)\n(?P<code>.*?)\n```"
        matches = re.finditer(pattern, markdown_content, re.MULTILINE | re.DOTALL)
        for match in matches:
            filename = match.group("filename")
            code = match.group("code")
            code_snippets.append(CodeSnippet(filename=filename, code=code.strip()))
        return code_snippets


class FileWriter:
    def write_code_to_file(self, code_snippet: CodeSnippet, output_dir: str):
        filepath = os.path.join(output_dir, code_snippet.filename)
        os.makedirs(output_dir, exist_ok=True)  # 确保目录存在
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_snippet.code)
            print(f"File '{filepath}' created successfully.")
        except Exception as e:
            print(f"Error writing to file '{filepath}': {e}")

# 可以提供一个更高级的接口函数


def extract_and_write_code(markdown_content: str, output_dir: str):
    parser = MarkdownParser()
    writer = FileWriter()
    code_snippets = parser.parse_markdown(markdown_content)
    for snippet in code_snippets:
        writer.write_code_to_file(snippet, output_dir)
