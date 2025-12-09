#!/bin/bash

# ========================================
# API 연결 테스트 스크립트
# ========================================

echo "========================================="
echo "API 연결 테스트 스크립트"
echo "========================================="
echo ""

# .env 파일 확인
if [ ! -f "../.env" ]; then
    echo "✗ .env 파일이 없습니다."
    echo ""
    echo ".env.example 파일을 복사하여 .env 파일을 생성하고"
    echo "API 키를 입력해주세요:"
    echo ""
    echo "  cp .env.example .env"
    echo "  # .env 파일을 편집하여 API 키 입력"
    echo ""
    exit 1
fi

# .env 파일 로드
echo "환경 변수 로드 중..."
export $(cat ../.env | grep -v '^#' | xargs)
echo ""

# NewsAPI 테스트
echo "1. NewsAPI 연결 테스트..."
if [ -z "$NEWSAPI_KEY" ]; then
    echo "✗ NEWSAPI_KEY가 설정되지 않았습니다."
else
    RESPONSE=$(curl -s "https://newsapi.org/v2/top-headlines?country=kr&pageSize=1&apiKey=$NEWSAPI_KEY")
    STATUS=$(echo $RESPONSE | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    if [ "$STATUS" == "ok" ]; then
        echo "✓ NewsAPI 연결 성공"
        TOTAL=$(echo $RESPONSE | grep -o '"totalResults":[0-9]*' | cut -d':' -f2)
        echo "  사용 가능한 뉴스: $TOTAL개"
    else
        echo "✗ NewsAPI 연결 실패"
        ERROR=$(echo $RESPONSE | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        echo "  오류: $ERROR"
    fi
fi
echo ""

# OpenAI API 테스트
echo "2. OpenAI API 연결 테스트..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "✗ OPENAI_API_KEY가 설정되지 않았습니다."
else
    RESPONSE=$(curl -s https://api.openai.com/v1/models \
        -H "Authorization: Bearer $OPENAI_API_KEY" 2>&1)

    if echo "$RESPONSE" | grep -q '"object": "list"'; then
        echo "✓ OpenAI API 연결 성공"

        # GPT-4 사용 가능 여부 확인
        if echo "$RESPONSE" | grep -q '"id": "gpt-4"'; then
            echo "  ✓ GPT-4 사용 가능"
        else
            echo "  ✗ GPT-4 사용 불가 (권한 확인 필요)"
        fi

        # DALL-E 3 사용 가능 여부 확인
        if echo "$RESPONSE" | grep -q '"id": "dall-e-3"'; then
            echo "  ✓ DALL-E 3 사용 가능"
        else
            echo "  ! DALL-E 3 사용 가능 여부 미확인"
        fi
    else
        echo "✗ OpenAI API 연결 실패"
        ERROR=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        if [ ! -z "$ERROR" ]; then
            echo "  오류: $ERROR"
        fi
    fi
fi
echo ""

# ElevenLabs API 테스트
echo "3. ElevenLabs API 연결 테스트..."
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "✗ ELEVENLABS_API_KEY가 설정되지 않았습니다."
else
    RESPONSE=$(curl -s https://api.elevenlabs.io/v1/voices \
        -H "xi-api-key: $ELEVENLABS_API_KEY" 2>&1)

    if echo "$RESPONSE" | grep -q '"voices"'; then
        echo "✓ ElevenLabs API 연결 성공"

        # 사용 가능한 음성 목록
        VOICE_COUNT=$(echo "$RESPONSE" | grep -o '"voice_id"' | wc -l)
        echo "  사용 가능한 음성: $VOICE_COUNT개"

        # Voice ID 확인
        if [ -z "$ELEVENLABS_VOICE_ID" ]; then
            echo "  ! ELEVENLABS_VOICE_ID가 설정되지 않았습니다."
            echo ""
            echo "  사용 가능한 음성 목록:"
            echo "$RESPONSE" | grep -o '"voice_id":"[^"]*"' | cut -d'"' -f4 | head -5 | while read voice; do
                echo "    - $voice"
            done
        else
            if echo "$RESPONSE" | grep -q "\"voice_id\":\"$ELEVENLABS_VOICE_ID\""; then
                echo "  ✓ 설정된 Voice ID 사용 가능"
            else
                echo "  ✗ 설정된 Voice ID를 찾을 수 없습니다."
            fi
        fi
    else
        echo "✗ ElevenLabs API 연결 실패"
        ERROR=$(echo "$RESPONSE" | grep -o '"detail":"[^"]*"' | cut -d'"' -f4)
        if [ ! -z "$ERROR" ]; then
            echo "  오류: $ERROR"
        fi
    fi
fi
echo ""

echo "========================================="
echo "테스트 완료"
echo "========================================="
echo ""
echo "모든 API가 정상적으로 작동하면 워크플로우를 시작할 수 있습니다."
