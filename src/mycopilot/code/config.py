# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Union


class Settings(BaseModel):
    code_path: str = "./"  # 代码文件或目录路径
    compression_strategy: str = "llm"  # 压缩策略，可选 "original" 或 "llm"
    prompt_prefix: str = "以下是代码的描述："
    prompt_suffix: str = "请根据以上代码描述进行分析。"
    output_dir: str = "./.output"
