#!/bin/bash

# 사용법: ./push_ecr.sh <ECR_REPOSITORY_NAME> <AWS_REGION>
# 예시: ./push_ecr.sh my-ecr-repo ap-northeast-2

IMAGE_NAME=$1
REGION=$2

if [ -z "$IMAGE_NAME" ] || [ -z "$REGION" ]; then
  echo "사용법: $0 <ECR_REPOSITORY_NAME> <AWS_REGION>"
  exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPOSITORY_URI=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE_NAME}:latest

# ECR 리포지토리 생성 (이미 존재해도 에러 무시)
aws ecr create-repository --repository-name ${IMAGE_NAME} --region ${REGION} > /dev/null 2>&1

# ECR 로그인
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

# Docker 이미지 빌드 (단일 아키텍처, 캐시 무시)
docker buildx build --platform linux/amd64 -t ${IMAGE_NAME}:latest --load .

# 태그 변경
docker tag ${IMAGE_NAME}:latest ${REPOSITORY_URI}

# ECR로 푸시
docker push ${REPOSITORY_URI}

echo "이미지가 성공적으로 ECR에 푸시되었습니다: ${REPOSITORY_URI}" 