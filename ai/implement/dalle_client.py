import openai
from ai.base import AIClient

class DalleClient(AIClient):
    def __init__(self, calculator, api_key, model: str = "dall-e-3"):
        super.__init__(calculator, api_key)
        self.model = model

    def execute(self, description: str, size: str = "1024x1024", **kwargs) -> dict:
        response = openai.Image.create(
            model=self.model,
            prompt=description,
            size=size,
            n=1
        )
        image_url = response["data"][0]["url"]
        return {"image_url": image_url}
    
    def calculate(self):
        return super().calculate()
