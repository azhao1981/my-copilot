# -*- coding: utf-8 -*-
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from pathlib import Path
import os
import datetime
from typing import Iterator, Union


def load_env():
    load_dotenv(find_dotenv(), override=True)


class LLMConfig(BaseModel):
    api_key: str
    base_url: str
    model: str


def os_getenvs(default: str, *keys: str) -> dict:
    for key in keys:
        value = os.getenv(key, "")
        if value:
            return value
    return default


class Config:
    def __init__(self, api_key: str, base_url: str):
        load_dotenv(find_dotenv(), override=True)
        self.api_key = api_key or os_getenvs(api_key, "API_KEY", "ONEAPI_API_KEY")
        self.base_url = base_url or os_getenvs(base_url, "BASE_URL", "ONEAPI_BASE_URL")

    def get_llm_config(self, model: str) -> LLMConfig:
        return LLMConfig(
            api_key=self.api_key,
            base_url=self.base_url,
            model=model
        )


class LLMFactory:
    @staticmethod
    def create(config: LLMConfig) -> ChatOpenAI:
        return ChatOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            model=config.model
        )


class PromptHandler:
    @staticmethod
    def load_prompt(file_path: str, additional_text: str = "") -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read() + additional_text


class FileManager:
    @staticmethod
    def get_session_path() -> Path:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return Path(current_path(f'sessions/temp-{timestamp}.md'))


class ResponseHandler:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def process_response(self, response: Union[str, Iterator], stream: bool = True):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            if stream:
                for chunk in response:
                    content = chunk.content
                    print(content, end="")
                    file.write(content)
            else:
                print(response.content)
                file.write(response.content)


def process_prompt(
        prompt_file: str, additional_text: str,
        model: str = "claude-3-5-sonnet",
        stream: bool = True,
        api_key: str = "",
        base_url: str = ""
):
    config = Config(api_key, base_url)
    llm_config = config.get_llm_config(model)
    llm = LLMFactory.create(llm_config)

    prompt = PromptHandler.load_prompt(
        current_path(prompt_file), additional_text)
    response = llm.stream(prompt) if stream else llm(prompt)

    file_path = FileManager.get_session_path()
    ResponseHandler(file_path).process_response(response, stream)


def current_path(path: str) -> str:
    """获取相对于当前脚本的路径"""
    if path.startswith('/'):
        return path
    elif path.startswith('./'):
        return str(Path(__file__).parent / path[2:])
    else:
        return str(Path(__file__).parent / path)


if __name__ == "__main__":
    role = """
    You play as a software architect, AI expert, and telecommunications expert to answer questions for me.
    """
    question = """
    使用golang从英文句子中提取出所有的地名，区分国家城市和省份，会使用到哪些库和NLP技术
    从哪里可以得到相关数据或是字典
    请给出代码示例
    """
    process_prompt('./prompt-base.md', role + question)
