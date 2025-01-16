# -*- coding: utf-8 -*-
from typing import Dict
from abc import ABC, abstractmethod
import time


class CodeCompressionStrategy(ABC):
    @abstractmethod
    def compress(self, code_snippets: Dict[str, str]) -> Dict[str, str]:
        pass


class OriginalCodeStrategy(CodeCompressionStrategy):
    def compress(self, code_snippets: Dict[str, str]) -> Dict[str, str]:
        return {filename: f"原始代码:\n```\n{content}\n```" for filename, content in code_snippets.items()}


class LLMCompressionStrategy(CodeCompressionStrategy):
    def compress(self, code_snippets: Dict[str, str]) -> Dict[str, str]:
        print("模拟调用大型模型进行代码分析...")
        time.sleep(2)  # 模拟 LLM 处理时间
        descriptions = {}
        for filename, content in code_snippets.items():
            # 这里应该是调用大型模型的 API，并根据模型返回的结果生成描述
            # 为了简化，我们这里生成一个模拟的描述
            function_summaries = "\n".join([f"- 函数 `{func}`: 实现了某功能。" for func in ["func1", "func2"]])
            call_relationships = "- `func1` 调用了 `func2`。"
            descriptions[filename] = f"文件 `{filename}` 包含以下函数：\n{function_summaries}\n调用关系：\n{call_relationships}"
        return descriptions


def compress_code(code_snippets: Dict[str, str], strategy: CodeCompressionStrategy) -> Dict[str, str]:
    return strategy.compress(code_snippets)


def create_compressor(strategy_name: str) -> CodeCompressionStrategy:
    if strategy_name == "original":
        return OriginalCodeStrategy()
    elif strategy_name == "llm":
        return LLMCompressionStrategy()
    else:
        raise ValueError(f"不支持的压缩策略: {strategy_name}")
