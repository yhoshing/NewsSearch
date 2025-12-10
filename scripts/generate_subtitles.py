#!/usr/bin/env python3
"""
자막 SRT 파일 생성 스크립트

스크립트 텍스트를 입력받아 타이밍이 포함된 SRT 자막 파일을 생성합니다.
"""

import sys
import json
import re
from datetime import timedelta
from typing import List, Dict, Tuple


def time_to_srt_format(seconds: float) -> str:
    """
    초를 SRT 타임 포맷으로 변환

    Args:
        seconds: 초 단위 시간

    Returns:
        SRT 형식의 시간 문자열 (HH:MM:SS,mmm)
    """
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60
    milliseconds = td.microseconds // 1000

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def split_text_into_segments(text: str, max_chars: int = 60) -> List[str]:
    """
    긴 텍스트를 자막용 세그먼트로 분할

    Args:
        text: 원본 텍스트
        max_chars: 세그먼트당 최대 글자 수

    Returns:
        분할된 텍스트 리스트
    """
    # 문장 단위로 분할 (한국어 문장부호 포함)
    sentences = re.split(r'([.!?。！？])', text)

    segments = []
    current_segment = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
        full_sentence = (sentence + punctuation).strip()

        if not full_sentence:
            continue

        # 현재 세그먼트에 추가했을 때 max_chars를 초과하면
        if len(current_segment) + len(full_sentence) > max_chars:
            if current_segment:
                segments.append(current_segment.strip())
            current_segment = full_sentence
        else:
            current_segment += " " + full_sentence if current_segment else full_sentence

    if current_segment:
        segments.append(current_segment.strip())

    return segments


def calculate_segment_timing(
    segments: List[str],
    total_duration: float
) -> List[Tuple[float, float, str]]:
    """
    각 세그먼트의 타이밍 계산

    Args:
        segments: 텍스트 세그먼트 리스트
        total_duration: 총 영상 길이 (초)

    Returns:
        (시작시간, 종료시간, 텍스트) 튜플의 리스트
    """
    if not segments:
        return []

    # 각 세그먼트의 길이에 비례하여 시간 할당
    total_chars = sum(len(seg) for seg in segments)

    timings = []
    current_time = 0.0

    for segment in segments:
        segment_duration = (len(segment) / total_chars) * total_duration
        start_time = current_time
        end_time = current_time + segment_duration

        timings.append((start_time, end_time, segment))
        current_time = end_time

    return timings


def generate_srt_from_segments(
    segments: List[Dict[str, str]]
) -> str:
    """
    세그먼트 딕셔너리로부터 SRT 생성

    Args:
        segments: 타임라인과 텍스트가 포함된 세그먼트 리스트
                 [{"time": "0-5", "text": "텍스트"}, ...]

    Returns:
        SRT 형식의 자막 문자열
    """
    srt_content = ""

    for i, segment in enumerate(segments, start=1):
        time_range = segment.get("time", "0-5")
        text = segment.get("text", "")

        # 시간 범위 파싱
        time_parts = time_range.split("-")
        start_time = float(time_parts[0]) if time_parts else 0.0
        end_time = float(time_parts[1]) if len(time_parts) > 1 else start_time + 5.0

        # SRT 엔트리 생성
        srt_content += f"{i}\n"
        srt_content += f"{time_to_srt_format(start_time)} --> {time_to_srt_format(end_time)}\n"
        srt_content += f"{text}\n\n"

    return srt_content


def generate_srt_from_script(
    script: str,
    total_duration: float = 60.0,
    max_chars_per_segment: int = 60
) -> str:
    """
    스크립트 텍스트로부터 SRT 생성

    Args:
        script: 전체 스크립트 텍스트
        total_duration: 총 영상 길이 (초)
        max_chars_per_segment: 세그먼트당 최대 글자 수

    Returns:
        SRT 형식의 자막 문자열
    """
    # 텍스트를 세그먼트로 분할
    segments = split_text_into_segments(script, max_chars_per_segment)

    # 타이밍 계산
    timings = calculate_segment_timing(segments, total_duration)

    # SRT 생성
    srt_content = ""
    for i, (start_time, end_time, text) in enumerate(timings, start=1):
        srt_content += f"{i}\n"
        srt_content += f"{time_to_srt_format(start_time)} --> {time_to_srt_format(end_time)}\n"
        srt_content += f"{text}\n\n"

    return srt_content


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법:")
        print("  1. 스크립트로부터 생성:")
        print("     python generate_subtitles.py --script \"텍스트\" --duration 60 --output subtitle.srt")
        print("  2. JSON 세그먼트로부터 생성:")
        print("     python generate_subtitles.py --json segments.json --output subtitle.srt")
        print("  3. 표준 입력으로부터 생성:")
        print("     echo '스크립트' | python generate_subtitles.py --output subtitle.srt")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="SRT 자막 파일 생성")
    parser.add_argument("--script", help="스크립트 텍스트")
    parser.add_argument("--json", help="세그먼트 JSON 파일 경로")
    parser.add_argument("--duration", type=float, default=60.0, help="총 영상 길이 (초)")
    parser.add_argument("--max-chars", type=int, default=60, help="세그먼트당 최대 글자 수")
    parser.add_argument("--output", "-o", required=True, help="출력 SRT 파일 경로")

    args = parser.parse_args()

    srt_content = ""

    # JSON 파일로부터 생성
    if args.json:
        with open(args.json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # segments 키가 있는 경우
        if isinstance(data, dict) and "segments" in data:
            segments = data["segments"]
            srt_content = generate_srt_from_segments(segments)
        # 리스트인 경우
        elif isinstance(data, list):
            srt_content = generate_srt_from_segments(data)
        else:
            print("오류: JSON 형식이 올바르지 않습니다.", file=sys.stderr)
            sys.exit(1)

    # 스크립트 텍스트로부터 생성
    elif args.script:
        srt_content = generate_srt_from_script(
            args.script,
            args.duration,
            args.max_chars
        )

    # 표준 입력으로부터 생성
    else:
        script = sys.stdin.read().strip()
        if script:
            srt_content = generate_srt_from_script(
                script,
                args.duration,
                args.max_chars
            )
        else:
            print("오류: 입력이 없습니다.", file=sys.stderr)
            sys.exit(1)

    # 파일로 저장
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f"자막 파일이 생성되었습니다: {args.output}")


if __name__ == "__main__":
    main()
