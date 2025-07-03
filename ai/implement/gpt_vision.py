from ai.base import AIClient
import openai

class GptVision(AIClient):
    def __init__(self, calculator, api_key, model="gpt-4o"):
        self.calculator = calculator
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def execute(self, prompt, **kwargs) -> dict:
        """
        prompt: [image_url, text_prompt]
        """
        image_url = prompt[0]
        text_prompt = prompt[1]
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512
        )
        return response

    def calculate(self, response):
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        input_cost = (input_tokens / 1000) * 0.005
        output_cost = (output_tokens / 1000) * 0.015
        total_cost = round(input_cost + output_cost, 6)
        self.calculator.add(total_cost)

    def parse(self, response):
        # 첫 번째 응답 메시지의 텍스트만 반환
        return response.choices[0].message.content
