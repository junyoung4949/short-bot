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
        except Exception as e:
            # 예외 발생 시 디스코드로 에러 알림
            discord_notifier.send_notification_generate(title='에셋 생성 실패', description=str(e), data={})
            return {'statusCode': 500, 'body': f'에러 발생: {str(e)}'}
        finally:
            chargeCalculator.execute()
    elif task == 'UPLOAD':
        pass
    elif task == 'GENERATE_UPLOAD':
        pass
    else:
        return {'statusCode': 400, 'body': 'task는 GENERATE, UPLOAD, GENERATE_UPLOAD 만 허용합니다.'}
    
    # return {
    #     'statusCode': 200,
    #     'body': {
    #         'youtube_url': youtube_url,
    #         'asset_result': asset_result
    #     }
    # }