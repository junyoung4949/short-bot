import os
from ai.factory import AiClientFactory
from lib.charge_calculator import ChargeCalculator
from repository.project_repository import ProjectRepository
from repository.media_repository import MediaRepository
from repository.item_repository import ItemRepository
from lib.impl_loader import ImplLoader
from lib.youtube_uploader import YouTubeUploader
from lib.discord_notifier import DiscordNotifier

def lambda_handler(event, context):
    # project_id, user_id, webhook_url, task 가져오기
    project_id = event.get('project_id')
    task = event.get('task')
    if not project_id or not task:
        return {'statusCode': 400, 'body': 'project_id, task는 필수입니다.'}
    
    project_repository = ProjectRepository(project_id)
    project_info = project_repository.get_project_info()

    if not hasattr(project_info, 'data') or not project_info.data:
        return {'statusCode': 404, 'body': f'project_id {project_id}에 해당하는 프로젝트가 존재하지 않습니다.'}
    if 'user_id' not in project_info.data or 'webhook_url' not in project_info.data:
        return {'statusCode': 404, 'body': f'project_id {project_id}의 프로젝트 정보에 user_id 또는 webhook_url이 없습니다.'}

    user_id = project_info.data['user_id']
    webhook_url = project_info.data['webhook_url']

    chargeCalculator = ChargeCalculator(project_repository)
    ai_client_factory = AiClientFactory(chargeCalculator)
    media_repository = MediaRepository(user_id, project_id)
    item_repository = ItemRepository(user_id, project_id)
    discord_notifier = DiscordNotifier(webhook_url)
    youtube_uploader = YouTubeUploader(project_id, user_id)

    loader = ImplLoader(user_id, project_id)
    AssetImpl = loader.get_asset_impl()
    VideoImpl = loader.get_video_impl()

    asset_impl = AssetImpl(ai_client_factory, media_repository)
    video_impl = VideoImpl()

    if task == 'GENERATE':
        try:
            item = asset_impl.run()
            item['status'] = 'PENDING'
            item_repository.save_item(item)
            discord_notifier.send_notification_generate(title=item['title'], description=item['description'], data=item['data'])
            return {
                        'statusCode': 200,
                        'body': {
                            'message': '에셋 생성 성공'
                        }
                    }
        except Exception as e:
            # 예외 발생 시 디스코드로 에러 알림
            discord_notifier.send_notification_generate(title='에셋 생성 실패', description=str(e), data={}, success=False)
            return {'statusCode': 500, 'body': f'에러 발생: {str(e)}'}
        finally:
            chargeCalculator.execute()
    elif task == 'UPLOAD':
        try:
            item = item_repository.read_item_random()
            video_path = video_impl.run(item['data'])
            short_id = youtube_uploader.upload_video(video_path, item['title'], item['description'])
            item_repository.update_status_uploaded(item['id'])
            video_url = f"https://youtube.com/watch?v={short_id}"
            discord_notifier.send_notification_upload(title=item['title'], description=item['description'], video_url=video_url, success=True)
            return {
                        'statusCode': 200,
                        'body': {
                            'message': '업로드 성공'
                        }
                    }
        except Exception as e:
            # 예외 발생 시 디스코드로 에러 알림
            discord_notifier.send_notification_generate(title='동영상 업로드중 에러 발생', description=str(e), data={}, success=False)
            return {'statusCode': 500, 'body': f'에러 발생: {str(e)}'}
    elif task == 'GENERATE_UPLOAD':
            try:
                item = asset_impl.run()
                video_path = video_impl.run(item['data'])
                short_id = youtube_uploader.upload_video(video_path, item['title'], item['description'])
                video_url = f"https://youtube.com/watch?v={short_id}"
                item['status'] = 'UPLOADED'
                item_repository.save_item(item)
                discord_notifier.send_notification_upload(title=item['title'], description=item['description'], video_url=video_url, success=True)
                return {
                        'statusCode': 200,
                        'body': {
                            'message': '에셋 생성 후 업로드 성공'
                        }
                    }
            except Exception as e:
                # 예외 발생 시 디스코드로 에러 알림
                discord_notifier.send_notification_generate(title='동영상 업로드중 에러 발생', description=str(e), data={}, success=False)
                return {'statusCode': 500, 'body': f'에러 발생: {str(e)}'}
    else:
        return {'statusCode': 400, 'body': 'task는 GENERATE, UPLOAD, GENERATE_UPLOAD 만 허용합니다.'}