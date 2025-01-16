# -*- coding: utf-8 -*-
import os


def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def list_code_files(dirpath: str) -> list[str]:
    code_files = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if file.endswith(('.py', '.java', '.js')):  # 可以根据需要添加其他代码文件类型
                code_files.append(os.path.join(root, file))
    return code_files
