import requests
from PIL import Image
import numpy as np
from io import BytesIO
import itertools
import random

class MaskSelector:
    @staticmethod
    def select_smallest_masks(mask_urls, topk=5):
        """
        마스크 url 배열을 받아, 흰색(255) 픽셀 개수가 가장 작은 topk개 url을 반환합니다.
        """
        mask_sizes = []
        for url in mask_urls:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert("L")
                arr = np.array(img)
                white_pixels = np.sum(arr == 255)
                mask_sizes.append((url, white_pixels))
            except Exception as e:
                print(f"마스크 다운로드/분석 실패: {url}, 에러: {e}")
        # 흰색 픽셀 개수 기준 오름차순 정렬 후 상위 topk개 url 반환
        mask_sizes.sort(key=lambda x: x[1])
        return [url for url, _ in mask_sizes[:topk]]

    @staticmethod
    def get_mask_centroid(mask_url):
        """
        마스크 이미지의 중심점(centroid)을 계산합니다.
        """
        try:
            response = requests.get(mask_url)
            img = Image.open(BytesIO(response.content)).convert('L')
            arr = np.array(img)
            ys, xs = np.where(arr > 128)  # 흰색(마스크) 부분
            if len(xs) == 0 or len(ys) == 0:
                return None
            cx = np.mean(xs)
            cy = np.mean(ys)
            return (cx, cy)
        except Exception as e:
            print(f"마스크 중심점 계산 실패: {mask_url}, 에러: {e}")
            return None

    @staticmethod
    def total_distance(centroids):
        """
        여러 중심점들 간의 총 거리를 계산합니다.
        """
        total = 0
        for i, a in enumerate(centroids):
            for j, b in enumerate(centroids):
                if i < j:
                    dist = np.linalg.norm(np.array(a) - np.array(b))
                    total += dist
        return total

    @staticmethod
    def select_farthest_masks(mask_urls, num_select=3):
        """
        마스크 url 배열을 받아, 서로 거리가 가장 먼 num_select개 마스크를 반환합니다.
        """
        centroids = [MaskSelector.get_mask_centroid(url) for url in mask_urls]
        valid = [(url, c) for url, c in zip(mask_urls, centroids) if c is not None]
        
        if len(valid) < num_select:
            raise ValueError(f"마스크 중심 좌표를 구할 수 있는 마스크가 {num_select}개 미만입니다.")
        
        urls, centroids = zip(*valid)
        best = None
        best_score = -1
        
        for comb in itertools.combinations(range(len(urls)), num_select):
            c = [centroids[i] for i in comb]
            score = MaskSelector.total_distance(c)
            if score > best_score:
                best_score = score
                best = comb
        
        return [urls[i] for i in best]

    @staticmethod
    def select_random_far_masks(mask_urls, num_select=3, min_dist=100, max_trials=5):
        """
        마스크 url 배열에서 서로 너무 가까이 붙어있지 않은 마스크 num_select개를 랜덤하게 선택합니다.
        min_dist 픽셀 이상 떨어진 조합만 허용하며, max_trials만큼 시도합니다.
        조건을 만족하는 조합이 없으면 그냥 랜덤하게 반환합니다.
        """
        centroids = [MaskSelector.get_mask_centroid(url) for url in mask_urls]
        valid = [(url, c) for url, c in zip(mask_urls, centroids) if c is not None]
        if len(valid) < num_select:
            raise ValueError(f"마스크 중심 좌표를 구할 수 있는 마스크가 {num_select}개 미만입니다.")
        urls, centroids = zip(*valid)
        indices = list(range(len(urls)))
        for _ in range(max_trials):
            sample = random.sample(indices, num_select)
            coords = [centroids[i] for i in sample]
            ok = True
            for i in range(num_select):
                for j in range(i+1, num_select):
                    if np.linalg.norm(np.array(coords[i]) - np.array(coords[j])) < min_dist:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return [urls[i] for i in sample]
        # 실패 시 그냥 랜덤 반환
        return [urls[i] for i in random.sample(indices, num_select)] 