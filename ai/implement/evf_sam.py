from ai.base import AIClient
import fal_client
import os
from ai.utils import on_queue_update

class EvfSam(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        os.environ["FAL_KEY"] = api_key

    def execute(self, prompt, **kwargs) -> dict:
        image_url = prompt[0]
        text_prompt = prompt[1]
        result = fal_client.subscribe(
            "fal-ai/evf-sam",
            arguments={
                "image_url": image_url,
                "prompt": text_prompt
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        return result

    def calculate(self, response):
        self.calculator.add(0.005)

    def parse(self, response):
        return response['image']['url']