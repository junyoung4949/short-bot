from abc import ABC, abstractmethod

class AssetTemplate(ABC):
    def __init__(self, ai_factory, media_repository):
        self.ai_factory = ai_factory
        self.media_repository = media_repository

    def run(self) -> dict:
        return self.build()
    
    @abstractmethod
    def build(self) -> dict:
        raise NotImplementedError