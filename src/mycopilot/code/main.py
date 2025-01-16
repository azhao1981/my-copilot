# -*- coding: utf-8 -*-
from config import Settings
from code_loader import load_code
from code_compressor import create_compressor, compress_code
from prompt_generator import merge_code_descriptions, merge_code, create_prompt
from extractor import extract_and_write_code


def main():
    settings = Settings(code_path=".")  # 默认加载当前目录，可以修改为指定文件

    code_snippets = load_code(settings.code_path)

    compressor = create_compressor(settings.compression_strategy)
    compressed_descriptions = compress_code(code_snippets, compressor)

    if settings.compression_strategy == "original":
        merged_content = merge_code(code_snippets)
    else:
        merged_content = merge_code_descriptions(compressed_descriptions)

    prompt = create_prompt(merged_content, prefix=settings.prompt_prefix, suffix=settings.prompt_suffix)

    print("生成的 Prompt:\n")
    print(prompt)


def extract(prompt: str):
    settings = Settings(output_dir="./sessions/.code")
    extract_and_write_code(prompt, settings.output_dir)


if __name__ == "__main__":
    with open("./src/mycopilot/code/temp-20250116121254.md", "r", encoding="utf-8") as f:
        prompt = f.read()
    extract(prompt)
