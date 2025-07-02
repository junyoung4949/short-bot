import importlib.util
import tempfile
import boto3
from config import BUCKET_NAME

class ImplLoader:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
        self.bucket = BUCKET_NAME

    def _download_from_s3(self, key):
        s3 = boto3.client('s3')
        tmp_path = tempfile.mktemp(suffix='.py')
        s3.download_file(self.bucket, key, tmp_path)
        return tmp_path

    def _load_module_from_path(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_asset_impl(self):
        key = f"{self.user_id}/{self.project_id}/asset_impl.py"
        file_path = self._download_from_s3(key)
        module = self._load_module_from_path("asset_impl", file_path)
        return module.AssetImpl

    def get_video_impl(self):
        key = f"{self.user_id}/{self.project_id}/video_impl.py"
        file_path = self._download_from_s3(key)
        module = self._load_module_from_path("video_impl", file_path)
        return module.VideoImpl

    def get_asset_and_video_impl(self):
        asset_key = f"{self.user_id}/{self.project_id}/asset_impl.py"
        video_key = f"{self.user_id}/{self.project_id}/video_impl.py"
        asset_path = self._download_from_s3(asset_key)
        video_path = self._download_from_s3(video_key)
        asset_module = self._load_module_from_path("asset_impl", asset_path)
        video_module = self._load_module_from_path("video_impl", video_path)
        return asset_module.AssetImpl, video_module.VideoImpl 