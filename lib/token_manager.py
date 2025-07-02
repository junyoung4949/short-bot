import pickle
import boto3
from botocore.exceptions import ClientError
from config import BUCKET_NAME

class TokenManager:
    def __init__(self, project_id, user_id):
        self.credentials = None
        self.s3_client = boto3.client('s3')
        self.project_id = project_id
        self.user_id = user_id

    def get_token_key(self):
        """user_id/project_id/token.pickle 경로를 반환합니다."""
        return f"{self.user_id}/{self.project_id}/token.pickle"

    def get_token_from_s3(self):
        """S3에서 토큰을 가져옵니다."""
        try:
            response = self.s3_client.get_object(
                Bucket=BUCKET_NAME,
                Key=self.get_token_key()
            )
            return pickle.loads(response['Body'].read())
        except ClientError as e:
            print(f"S3에서 토큰을 가져오는 중 오류 발생: {str(e)}")
            return None

    def save_token_to_s3(self, credentials):
        """S3에 토큰을 저장합니다."""
        try:
            self.s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=self.get_token_key(),
                Body=pickle.dumps(credentials)
            )
            return True
        except ClientError as e:
            print(f"S3에 토큰을 저장하는 중 오류 발생: {str(e)}")
            return False
