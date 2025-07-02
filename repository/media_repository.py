from supabase import create_client, Client
from config import SUPABASE_ANON_KEY, SUPABASE_URL
import requests
import tempfile
import os
import mimetypes
import urllib.parse

class MediaRepository:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self.bucket_name = "media"

    def save_media(self, file_path, file_name=None):
        """
        file_path: 로컬 파일 경로
        file_name: storage에 저장할 파일명(없으면 uuid 자동 생성)
        반환: storage 내 파일의 public url
        """
        import uuid
        if file_name is None:
            ext = os.path.splitext(file_path)[-1]
            file_name = f"{self.user_id}/{self.project_id}/{uuid.uuid4().hex}{ext}"
        with open(file_path, "rb") as f:
            res = self.supabase.storage.from_(self.bucket_name).upload(file_name, f)
        # public url 생성
        url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_name)
        return url
    
    def save_media_by_url(self, url):
        # 1. URL에서 파일 다운로드
        response = requests.get(url)
        # URL에서 파일명 추출
        parsed_url = urllib.parse.urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        ext = os.path.splitext(file_name)[-1]
        # 만약 확장자가 없으면 Content-Type으로 추정
        if not ext:
            content_type = response.headers.get('Content-Type')
            ext = mimetypes.guess_extension(content_type) or ''
        tmp_path = tempfile.mktemp(suffix=ext)
        with open(tmp_path, "wb") as f:
            f.write(response.content)
        # 2. media_repository로 업로드
        media_url = self.save_media(tmp_path)
        # 3. 임시 파일 삭제
        os.remove(tmp_path)
        return media_url

    def read_media(self, file_name):
        """
        file_name: storage 내 파일 경로(예: user_id/project_id/uuid.png)
        반환: 바이너리 데이터
        """
        res = self.supabase.storage.from_(self.bucket_name).download(file_name)
        return res

    def delete_media(self, file_name):
        """
        file_name: storage 내 파일 경로
        반환: 성공 여부
        """
        res = self.supabase.storage.from_(self.bucket_name).remove([file_name])
        return res['error'] is None if isinstance(res, dict) and 'error' in res else True