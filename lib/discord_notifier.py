import requests
import json
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url):
        """
        디스코드 웹훅 URL을 초기화합니다.
        
        Args:
            webhook_url (str): 디스코드 웹훅 URL
        """
        self.webhook_url = webhook_url

    def send_notification_generate(self, title, description, data, success=True):
        """
        디스코드로 알림을 보냅니다.
        
        Args:
            title (str): item title
            description (str): item description
            data (dict) : item data
            success (bool): 성공 여부
        """
        # 임베드 색상 설정 (성공: 초록색, 실패: 빨간색)
        color = 0x00ff00 if success else 0xff0000
        
        embeds = []
        # 1. 기본 임베드(텍스트 정보)
        base_embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": []
        }
        image_urls = []
        for key, value in data.items():
            base_embed["fields"].append({
                "name": str(key),
                "value": str(value),
                "inline": False
            })
            if key.endswith("image_url"):
                if isinstance(value, list):
                    image_urls.extend(value)
                else:
                    image_urls.append(value)
        embeds.append(base_embed)
        # 2. 각 이미지마다 임베드 추가
        for url in image_urls:
            embeds.append({
                "image": {"url": url},
                "color": color
            })
        # 웹훅 데이터 구성
        webhook_data = {
            "embeds": embeds
        }
        try:
            # 디스코드로 알림 전송
            response = requests.post(
                self.webhook_url,
                data=json.dumps(webhook_data),
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 204:
                print("디스코드 알림이 성공적으로 전송되었습니다.")
                return True
            else:
                print(f"디스코드 알림 전송 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"디스코드 알림 전송 중 오류 발생: {str(e)}")
            return False 

    def send_notification_upload(self, title, description, video_url=None, success=True):
        """
        디스코드로 알림을 보냅니다.
        
        Args:
            title (str): 알림 제목
            description (str): 알림 설명
            video_url (str, optional): 업로드된 비디오 URL
            success (bool): 성공 여부
        """
        # 임베드 색상 설정 (성공: 초록색, 실패: 빨간색)
        color = 0x00ff00 if success else 0xff0000
        
        # 임베드 데이터 구성
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": []
        }
        
        # 비디오 URL이 있는 경우 필드에 추가
        if video_url:
            embed["fields"].append({
                "name": "비디오 링크",
                "value": video_url,
                "inline": False
            })
        
        # 웹훅 데이터 구성
        data = {
            "embeds": [embed]
        }
        
        try:
            # 디스코드로 알림 전송
            response = requests.post(
                self.webhook_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 204:
                print("디스코드 알림이 성공적으로 전송되었습니다.")
                return True
            else:
                print(f"디스코드 알림 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"디스코드 알림 전송 중 오류 발생: {str(e)}")
            return False 