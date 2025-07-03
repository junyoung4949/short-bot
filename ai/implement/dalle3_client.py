from ai.base import AIClient
import openai
import os

class Dalle3Client(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        self.api_key = api_key
        openai.api_key = api_key

    def execute(self, prompt, **kwargs) -> dict:
        # prompt: [text_prompt]
        text_prompt = prompt[0]
        image_size = kwargs.get("image_size", "1024x1024")
        n = kwargs.get("n", 1)
        response = openai.images.generate(
            model="dall-e-3",
            prompt=text_prompt,
            n=n,
            size=image_size,
            response_format="url"
        )
        return response

    def calculate(self, response):
        # DALL·E 3 가격은 1장당 약 $0.04 (2024년 기준)
        n = len(response.data) if hasattr(response, "data") else 1
        self.calculator.add(0.04 * n)

    def parse(self, response):
        # 첫 번째 이미지 URL 반환
        if hasattr(response, "data") and len(response.data) > 0:
            return response.data[0].url
        return None 