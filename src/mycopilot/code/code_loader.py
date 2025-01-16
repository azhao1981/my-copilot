# -*- coding: utf-8 -*-
from typing import Dict
from utils import read_file, is_directory, list_code_files


def load_file_content(filepath: str) -> Dict[str, str]:
    return {filepath: read_file(filepath)}


def load_directory_content(dirpath: str) -> Dict[str, str]:
    code_files = list_code_files(dirpath)
    return {filepath: read_file(filepath) for filepath in code_files}


def load_code(path: str) -> Dict[str, str]:
    if is_directory(path):
        return load_directory_content(path)
    else:
        return load_file_content(path)
