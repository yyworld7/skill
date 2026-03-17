"""NovelAI 核心引擎"""
import json
import requests
from typing import Dict, Any

class NovelCore:
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def generate(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 4096
        }
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json=payload, timeout=120
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"text": content.strip()}
