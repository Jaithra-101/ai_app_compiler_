import json, os
from openai import OpenAI

USE_LLM = os.getenv('USE_LLM', 'false').lower() == 'true'
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

class LLMClient:
    def __init__(self):
        self.client = OpenAI() if USE_LLM else None

    def json_call(self, system: str, user: str) -> dict:
        if not USE_LLM:
            raise RuntimeError('LLM disabled. Deterministic compiler mode is active.')
        res = self.client.chat.completions.create(
            model=MODEL,
            temperature=0,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': user},
            ],
        )
        return json.loads(res.choices[0].message.content)
