import boto3
from botocore.exceptions import ClientError
from config import BUCKET_NAME

class S3Repository:
    def __init__(self, project_id, user_id):
        self.s3_client = boto3.client('s3')
        self.project_id = project_id
        self.user_id = user_id

    def get_music(self, music_name = 'background.mp3'):
        directory = f"{self.user_id}/{self.project_id}/"
        try:
            response = self.s3_client.get_object(
                Bucket=BUCKET_NAME,
                Key=directory + "music/" + music_name
            )
            return response['Body'].read()  # mp3 파일의 바이너리 데이터를 반환
        except ClientError as e:
            print(f"mp3를 가져오는 과정에서 오류 발생: {str(e)}")
            return None
