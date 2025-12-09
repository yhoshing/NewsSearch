#!/bin/bash

# ========================================
# FFmpeg 설치 및 기능 테스트 스크립트
# ========================================

echo "========================================="
echo "FFmpeg 테스트 스크립트"
echo "========================================="
echo ""

# FFmpeg 설치 확인
echo "1. FFmpeg 설치 확인..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg가 설치되어 있습니다."
    ffmpeg -version | head -n 1
else
    echo "✗ FFmpeg가 설치되어 있지 않습니다."
    echo ""
    echo "설치 방법:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: https://ffmpeg.org/download.html"
    exit 1
fi
echo ""

# 출력 디렉토리 확인
echo "2. 출력 디렉토리 확인..."
OUTPUT_DIR="../output"
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "출력 디렉토리가 없습니다. 생성 중..."
    mkdir -p "$OUTPUT_DIR"
    echo "✓ 출력 디렉토리 생성 완료: $OUTPUT_DIR"
else
    echo "✓ 출력 디렉토리 존재: $OUTPUT_DIR"
fi
echo ""

# 테스트 이미지 생성
echo "3. 테스트 이미지 생성..."
TEST_IMAGE="$OUTPUT_DIR/test_image.png"
ffmpeg -f lavfi -i color=c=blue:s=1080x1920:d=1 -frames:v 1 "$TEST_IMAGE" -y 2>/dev/null
if [ -f "$TEST_IMAGE" ]; then
    echo "✓ 테스트 이미지 생성 성공: $TEST_IMAGE"
else
    echo "✗ 테스트 이미지 생성 실패"
    exit 1
fi
echo ""

# 테스트 오디오 생성
echo "4. 테스트 오디오 생성..."
TEST_AUDIO="$OUTPUT_DIR/test_audio.mp3"
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" "$TEST_AUDIO" -y 2>/dev/null
if [ -f "$TEST_AUDIO" ]; then
    echo "✓ 테스트 오디오 생성 성공: $TEST_AUDIO"
else
    echo "✗ 테스트 오디오 생성 실패"
    exit 1
fi
echo ""

# 비디오 합성 테스트
echo "5. 비디오 합성 테스트..."
TEST_VIDEO="$OUTPUT_DIR/test_video.mp4"
ffmpeg -loop 1 -i "$TEST_IMAGE" -i "$TEST_AUDIO" \
    -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
    -pix_fmt yuv420p -shortest \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
    "$TEST_VIDEO" -y 2>/dev/null

if [ -f "$TEST_VIDEO" ]; then
    echo "✓ 비디오 합성 성공: $TEST_VIDEO"

    # 파일 정보 출력
    VIDEO_SIZE=$(ls -lh "$TEST_VIDEO" | awk '{print $5}')
    echo "  파일 크기: $VIDEO_SIZE"

    # 비디오 정보 확인
    echo ""
    echo "비디오 정보:"
    ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of default=noprint_wrappers=1:nokey=1 "$TEST_VIDEO" 2>/dev/null | {
        read width
        read height
        read duration
        echo "  해상도: ${width}x${height}"
        echo "  길이: ${duration}초"
    }
else
    echo "✗ 비디오 합성 실패"
    exit 1
fi
echo ""

# 테스트 파일 정리
echo "6. 테스트 파일 정리..."
read -p "테스트 파일을 삭제하시겠습니까? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$TEST_IMAGE" "$TEST_AUDIO" "$TEST_VIDEO"
    echo "✓ 테스트 파일 삭제 완료"
else
    echo "테스트 파일 유지: $OUTPUT_DIR/"
fi
echo ""

echo "========================================="
echo "✓ 모든 테스트 완료!"
echo "========================================="
echo ""
echo "FFmpeg가 정상적으로 작동합니다."
echo "n8n 워크플로우를 시작할 수 있습니다."
