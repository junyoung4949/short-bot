from ai.base import AIClient
import fal_client
from ai.utils import on_queue_update
import os

class FalIdeogram(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        os.environ["FAL_KEY"] = api_key

    def execute(self, prompt, **kwargs) -> dict:
        image_url = prompt[0]
        mask_url = prompt[1]
        text_prompt = prompt[2]

        result = fal_client.subscribe(
        "fal-ai/ideogram/v3/edit",
        arguments={
            "prompt": text_prompt,
            "image_url": image_url,
            "mask_url": mask_url
        },
        with_logs=True,
        on_queue_update=on_queue_update,
        )
        return result

    def calculate(self, response):
        self.calculator.add(0.06)

    def parse(self, response):
        return response['images'][0]['url']