from lib.token_manager import TokenManager
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

class YouTubeUploader:
    def __init__(self, project_id, user_id):
        self.token_manager = TokenManager(project_id, user_id)
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.credentials = None

    def authenticate(self):
        """S3에서 토큰을 가져와 인증합니다."""
        self.credentials = self.token_manager.get_token_from_s3()
        if not self.credentials:
            print("토큰을 가져오지 못했습니다. 인증 실패.")
            return False
        if self.credentials.expired:
            try:
                request = Request()
                self.credentials.refresh(request)
                self.token_manager.save_token_to_s3(self.credentials)
            except Exception as e:
                print(f"토큰 갱신 실패: {str(e)}")
                return False
        return True

    def upload_video(self, video_path, title, description, tags=None):
        if not self.authenticate():
            print("인증 실패로 업로드 중단")
            return False
        if not os.path.exists(video_path):
            print(f"비디오 파일이 존재하지 않습니다: {video_path}")
            return False
        try:
            youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=self.credentials)
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False,
                    'madeForKids': False
                }
            }
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True
            )
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            print("업로드 시작...")
            response = request.execute()
            print(f"업로드 완료! 비디오 ID: {response['id']}")
            return response['id']
        except Exception as e:
            print(f"업로드 중 오류 발생: {str(e)}")
            return False 