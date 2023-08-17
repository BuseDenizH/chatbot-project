from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from nlu import NLU

import json


app = FastAPI()

var_NLU = NLU(qa_path="qa.json", nlu_threshold=0.6)


class Text(BaseModel):
    text: str


class EDT(BaseModel):
    text: str


@app.post("/detect_intent")
async def detect_intent(obj: EDT):
    result = var_NLU.extract_intent(obj.text)
    if not result:
        raise HTTPException(status_code=404, detail="Intent not found.")
    return result
