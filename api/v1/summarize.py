from fastapi import APIRouter, HTTPException, status
import re

from schemas.summarize import (
    ArticleRequest, 
    SummarizeResponse,
)
from services.summarize_service import summarize_text, detect_report_type

router = APIRouter()


def clean_summary_output(summary: str) -> str:
    """요약 결과에서 프롬프트와 불필요한 내용을 제거합니다"""
    # 대괄호 안의 메타 정보 제거: [시간], [유형] 등
    summary = re.sub(r'\[[^\[\]]+\]', '', summary)
    
    # "사건 개요:", "요약:", "내용:", "제목:" 등의 헤더 제거
    summary = re.sub(r'(사건\s*개요\s*:?|요약\s*:?|내용\s*:?|제목\s*:?)', '', summary)
    
    # 프롬프트 관련 텍스트 제거
    prompt_patterns = [
        r'다음 제보를 요약해주세요\.?\s*',
        r'다음 내용을 요약해주세요:?\s*',
        r'교통사고의 경우.*?요약해주세요\.?\s*',
        r'화재의 경우.*?요약해주세요\.?\s*',
        r'범죄의 경우.*?요약해주세요\.?\s*',
        r'긴급한 상황이므로.*?요약해주세요\.?\s*',
        r'발생시간\([^)]*\)을 포함하여 요약해주세요\.?\s*',
        r'발생장소\([^)]*\)를 포함하여 요약해주세요\.?\s*',
        r'피해정보\([^)]*\)를 포함하여 요약해주세요\.?\s*',
        r'제보 내용:?\s*',
        r'요약해주세요\.?\s*',
        r'포함하여 요약해주세요\.?\s*',
        r'강조하여 요약해주세요\.?\s*',
        r'발생시간\([^)]*\)을 포함하여\.?\s*',
        r'발생장소\([^)]*\)를 포함하여\.?\s*',
        r'피해정보\([^)]*\)를 포함하여\.?\s*',
        r'해주세요\.?\s*',
        r'제보\s*',
        r'^\d{1,2}일\.\s*',  # "30일." 등 날짜로 시작하는 문장 제거
        r'^\d{1,2}일\s*',   # "30일 " 등 날짜로 시작하는 문장 제거
        r'다음\s*',          # "다음"으로 시작하는 문장 제거
        r'내용\s*',          # "내용" 단어 제거
        r'제목\s*',          # "제목" 단어 제거
    ]
    
    for pattern in prompt_patterns:
        summary = re.sub(pattern, '', summary, flags=re.IGNORECASE | re.DOTALL)
    
    # 공백 정리
    lines = summary.strip().split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    
    # 줄바꿈으로 다시 연결
    result = '\n'.join(cleaned_lines)
    
    # 최종 공백 정리
    result = re.sub(r'\s+', ' ', result).strip()
    
    # 문장 시작 부분의 불필요한 점(.) 제거
    result = re.sub(r'^\.\s*', '', result)
    
    # 번호 매기기 제거: (1), (2), (3) 등
    result = re.sub(r'\(\d+\)\s*', '', result)
    
    # 문장 시작 부분의 날짜 패턴 제거: "29일.", "30일." 등
    result = re.sub(r'^\d{1,2}일\.\s*', '', result)
    
    return result


@router.post("/", response_model=SummarizeResponse)
def summarize_article(req: ArticleRequest):
    """뉴스 기사나 제보를 요약합니다"""
    try:
        # 서비스 레이어에서 요약 수행
        summary = summarize_text(req.text)
        
        # 프롬프트 제거
        cleaned_summary = clean_summary_output(summary)
        
        return SummarizeResponse(summary=cleaned_summary)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"요약 처리 중 오류가 발생했습니다: {str(e)}"
        ) 