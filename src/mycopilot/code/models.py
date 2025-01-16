# -*- coding: utf-8 -*-
from pydantic import BaseModel


class CodeFileContent(BaseModel):
    filename: str
    content: str


class CodeDescription(BaseModel):
    filename: str
    description: str
