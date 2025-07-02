from ai.implement.chatgpt_client import ChatGPTClient
from ai.implement.flux1_schnell import Flux1Schnell
from ai.implement.sam2_auto_segment import Sam2AutoSegment
from ai.implement.gpt_edit import GptEdit
from ai.implement.gpt_vision import GptVision
from ai.implement.evf_sam import EvfSam
from ai.implement.fal_inpaint import FalInpaint
from ai.implement.dalle3_client import Dalle3Client
from ai.implement.fal_ideogram import FalIdeogram
from config import OPENAI_API_KEY
from config import FAL_API_KEY
from lib.charge_calculator import ChargeCalculator

class AiClientFactory:
    def __init__(self, calculator: ChargeCalculator):
        self.calculator = calculator

    def get_ai_client(self, name: str):
        if name == "gpt-3.5-turbo":
            return ChatGPTClient(
                calculator=self.calculator,
                api_key=OPENAI_API_KEY,
                model="gpt-3.5-turbo"
            )
        elif name == 'gpt-4':
            return ChatGPTClient(
                calculator=self.calculator,
                api_key=OPENAI_API_KEY,
                model="gpt-4"
            )
        elif name == "flux1_schnell":
            return Flux1Schnell(
                calculator=self.calculator,
                api_key=FAL_API_KEY
            )
        elif name == "sam2_auto_segment":
            return Sam2AutoSegment(
                calculator=self.calculator,
                api_key=FAL_API_KEY
            )
        elif name == "gpt_edit":
            return GptEdit(
                calculator=self.calculator,
                api_key=OPENAI_API_KEY
            )
        elif name == "gpt_vision":
            return GptVision(
                calculator=self.calculator,
                api_key=OPENAI_API_KEY
            )
        elif name == "evf_sam":
            return EvfSam(
                calculator=self.calculator,
                api_key=FAL_API_KEY
            )
        elif name == "fal_inpaint":
            return FalInpaint(
                calculator=self.calculator,
                api_key=FAL_API_KEY
            )
        elif name == "dalle3_client":
            return Dalle3Client(
                calculator=self.calculator,
                api_key=OPENAI_API_KEY
            )
        elif name == "fal_ideogram":
            return FalIdeogram(
                calculator=self.calculator,
                api_key=FAL_API_KEY
            )
        else:
            raise ValueError(f"Unknown AI client: {name}")
