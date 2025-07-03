import openai
from ai.base import AIClient
from lib.charge_calculator import ChargeCalculator

class ChatGPTClient(AIClient):
    def __init__(self, calculator: ChargeCalculator, api_key, model: str = "gpt-3.5-turbo"):
        super().__init__(calculator, api_key)
        self.model = model
        openai.api_key = api_key  # api_key를 전역으로 설정

    def execute(self, prompt, **kwargs):
        response = openai.chat.completions.create(
            model=self.model,
            messages=prompt,
        )
        return response

    def calculate(self, response):
        price_per_1k = {
            "gpt-3.5-turbo": 0.0015,
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            # 필요시 추가
        }
        total_tokens = response.usage.total_tokens
        for key in price_per_1k:
            if response.model.startswith(key):
                price = price_per_1k[key]
                break
        else:
            raise ValueError(f"지원하지 않는 모델명입니다: {response.model}")
        total_1k_units = total_tokens / 1000
        cost = price * total_1k_units
        self.calculator.add(cost)
        return cost
    
    def parse(self, response):
        return response.choices[0].message.content