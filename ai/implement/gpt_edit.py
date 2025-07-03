from ai.base import AIClient
import openai
import requests
import uuid
import os
import tempfile

class GptEdit(AIClient):
    def __init__(self, calculator, api_key):
        self.calculator = calculator
        self.api_key = api_key

    def execute(self, prompt, **kwargs) -> dict:
        image_url = prompt[0]
        mask_url = prompt[1]
        original_image = requests.get(image_url).content
        mask_image = requests.get(mask_url).content

        # tmp 디렉토리에 uuid로 파일 저장
        tmp_dir = tempfile.gettempdir()
        original_path = os.path.join(tmp_dir, f"original_{uuid.uuid4()}.png")
        mask_path = os.path.join(tmp_dir, f"mask_{uuid.uuid4()}.png")
        with open(original_path, "wb") as f:
            f.write(original_image)
        with open(mask_path, "wb") as f:
            f.write(mask_image)

        # change_prompt = (
        #     "Create exactly 3 small and hard-to-notice differences in this teddy bear image. "
        #     "For example, adjust one paw pad, add a stripe to the hat, or slightly change the bowtie shape. "
        #     "Keep the overall style and layout the same."
        # )

        change_prompt = prompt[2]

        # 4. DALL·E API (images/edits) 호출
        response = openai.images.edit(
            image=open(original_path, "rb"),
            mask=open(mask_path, "rb"),
            prompt=change_prompt,
            n=1,
            size="1024x1024",
            response_format="url"  # 또는 "b64_json" 사용 가능
        )
        return response

    def calculate(self, response):
        self.calculator.add(0.04)

    def parse(self, response):
        return response.data[0].url
        # result = requests.get(image_url)
        # with open("teddy_edited.png", "wb") as f:
        #     f.write(result.content)
        # print("✅ 이미지가 성공적으로 생성되었습니다: teddy_edited.png")