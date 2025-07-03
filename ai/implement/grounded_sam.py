from ai.base import AIClient
import requests

class GroundedSAM(AIClient):
    def __init__(self, calculator, api_key=None, api_url=None):
        self.calculator = calculator
        self.api_key = api_key
        self.api_url = api_url or "http://localhost:8000/segment"  # 예시 URL

    def execute(self, prompt, **kwargs) -> dict:
        """
        prompt: [image_url, text_prompt]
        """
        image_url = prompt[0]
        text_prompt = prompt[1]
        payload = {
            "image_url": image_url,
            "text_prompt": text_prompt
        }
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def calculate(self, response):
        pass

    def parse(self, response):
        # response는 {"mask_url": ...} 형태라고 가정
        return response["mask_url"] 