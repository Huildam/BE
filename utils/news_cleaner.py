import re


def clean_news(text: str) -> str:
    """뉴스 기사나 제보를 전처리하여 요약에 적합한 형태로 정리합니다"""
    # 특수 문자 제거
    text = re.sub(r'\[[^\]]+\]', '', text)  # 괄호 [] 내용 제거
    text = re.sub(r'\([^)]*\)', '', text)  # 괄호 () 내용 제거
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 기자 이름, 이메일 제거
    text = re.sub(r'[가-힣]+ 기자', '', text)
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}', '', text)
    
    # 구어체 표현 정리
    text = re.sub(r'[가-힣]+씨', '', text)  # "~씨" 제거
    text = re.sub(r'[가-힣]+님', '', text)  # "~님" 제거
    text = re.sub(r'[가-힣]+군', '', text)  # "~군" 제거
    
    # 구어체 표현을 문어체로 변경
    text = re.sub(r'했어요', '했습니다', text)
    text = re.sub(r'됐어요', '되었습니다', text)
    text = re.sub(r'있어요', '있습니다', text)
    text = re.sub(r'없어요', '없습니다', text)
    text = re.sub(r'해요', '합니다', text)
    text = re.sub(r'돼요', '됩니다', text)
    
    # 불필요한 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()

    return text 