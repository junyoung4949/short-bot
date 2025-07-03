from ai.base import AIClient
import fal_client
import os
from ai.utils import on_queue_update

class Flux1Schnell(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        os.environ["FAL_KEY"] = api_key
    
    def execute(self, prompt, **kwargs) -> dict:
        return fal_client.subscribe(
            "fal-ai/flux-1/schnell",
            arguments={
                "prompt": prompt[0],
                "image_size": "square_hd",  # 또는 square, portrait_4_3, landscape_4_3 등
                "num_images": 1
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )

    
    def calculate(self, response):
        self.calculator.add(0.003)
    
    def parse(self, response):
        if response and 'images' in response and len(response['images']) > 0:
            return response['images'][0]['url']
        return None