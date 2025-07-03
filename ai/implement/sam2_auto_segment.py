from ai.base import AIClient
import fal_client
import os
from ai.utils import on_queue_update

class Sam2AutoSegment(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        os.environ["FAL_KEY"] = api_key

    def execute(self, prompt, **kwargs) -> dict:
        result = fal_client.subscribe(
            "fal-ai/sam2/auto-segment",
            arguments={
                "image_url": prompt[0]
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        return result

    def calculate(self, response):
        self.calculator.add(0.007)

    def parse(self, response):
        return response