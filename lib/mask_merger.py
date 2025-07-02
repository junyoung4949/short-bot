from PIL import Image
import numpy as np
import os
import uuid

class MaskMerger:
    @staticmethod
    def merge_masks(mask_paths, output_path=None):
        """
        여러 장의 마스크 이미지를 받아 합성(OR 연산)하여 하나의 마스크로 반환합니다.
        mask_paths: 마스크 이미지 파일 경로 리스트
        output_path: 저장 경로(지정하지 않으면 임시 파일로 저장)
        반환: 합성된 마스크의 PIL.Image 객체와 저장 경로
        """
        if not mask_paths:
            raise ValueError("마스크 경로 리스트가 비어 있습니다.")
        # 첫 번째 마스크를 기준으로 크기 통일
        base = Image.open(mask_paths[0]).convert("L")
        arr = np.array(base)
        for path in mask_paths[1:]:
            mask = Image.open(path).convert("L").resize(base.size)
            arr = np.maximum(arr, np.array(mask))
        merged = Image.fromarray(arr)
        if output_path is None:
            output_path = f"/tmp/merged_mask_{uuid.uuid4().hex}.png"
        merged.save(output_path)
        return output_path 