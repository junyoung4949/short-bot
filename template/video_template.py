from abc import ABC, abstractmethod
import moviepy.editor as mpy

class VideoTemplate(ABC):
    def __init__(self):
        self.moviepy = mpy
        pass

    def run(self, json):
        self.render(json)
        return self.save_video()

    @abstractmethod
    def render(self, json):
        raise NotImplementedError
    
    @abstractmethod
    def save_video(self) -> str:
        """youtube에 업로드할 동영상의 경로를 반환합니다."""
        raise NotImplementedError