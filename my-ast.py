# -*- coding: utf-8 -*-
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from pathlib import Path
import os
import datetime
from typing import Iterator, Union


class LLMConfig(BaseModel):
    api_key: str
    base_url: str
    model_name: str


class Config:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        self.api_key = os.getenv("ONEAPI_API_KEY", "")
        self.base_url = os.getenv("ONEAPI_BASE_URL", "")

    def get_llm_config(self, model_name: str) -> LLMConfig:
        return LLMConfig(api_key=self.api_key, base_url=self.base_url, model_name=model_name)


class LLMFactory:
    @staticmethod
    def create(config: LLMConfig) -> ChatOpenAI:
        return ChatOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            model=config.model_name
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
                print(response)
                file.write(response)


def process_prompt(
        prompt_file: str, additional_text: str,
        model_name: str = "claude-3-5-sonnet",
        stream: bool = True
):
    config = Config()
    llm_config = config.get_llm_config(model_name)
    llm = LLMFactory.create(llm_config)

    prompt = PromptHandler.load_prompt(current_path(prompt_file), additional_text)
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
    process_prompt('./prompt-base.md', "1.8 和 1.11 谁大")
