from abc import ABC, abstractmethod
from lib.charge_calculator import ChargeCalculator

class AIClient(ABC):
    def __init__(self, calculator: ChargeCalculator, api_key):
        self.calculator = calculator
        self.api_key = api_key

    def run(self, prompt):
        response = self.execute(prompt)
        self.calculate(response)
        return self.parse(response)

    @abstractmethod
    def execute(self, prompt, **kwargs) -> dict:
        pass

    @abstractmethod
    def calculate(self, response):
        pass

    @abstractmethod
    def parse(self, response):
        pass