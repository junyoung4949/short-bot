from ai.base import AIClient
import fal_client
import os
from ai.utils import on_queue_update

class FalInpaint(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        os.environ["FAL_KEY"] = api_key

    def execute(self, prompt, **kwargs) -> dict:
        # prompt: [image_url, mask_url, text_prompt]
        image_url = prompt[0]
        mask_url = prompt[1]
        text_prompt = prompt[2]
        result = fal_client.subscribe(
            "fal-ai/inpaint",
            arguments={
                "model_name": "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
                "image_url": image_url,
                "mask_url": mask_url,
                "prompt": text_prompt
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        return result

    def calculate(self, response):
        # 예시: 1초당 $0.00111, 평균 5초 소요라 가정하면 약 $0.0055
        self.calculator.add(0.0055)

    def parse(self, response):
        return response['image']['url']