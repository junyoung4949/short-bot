from lambda_handler import lambda_handler

if __name__ == "__main__":
    # 테스트용 파라미터 입력
    project_id = "b2c9da57-b9c9-419f-a5ee-b5cc442f621c"

    # GENERATE 테스트
    event_generate = {
        "project_id": project_id,
        "task": "GENERATE"
    }
    print("[GENERATE] 결과:")
    print(lambda_handler(event_generate, None))