import re
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils.news_cleaner import clean_news
from typing import Dict, List, Tuple

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 전역 변수로 모델과 토크나이저 저장
model = None
tokenizer = None


def load_model():
    """모델과 토크나이저를 로드합니다"""
    global model, tokenizer
    logger.info("🔄 T5 모델 로딩 시작...")
    model = AutoModelForSeq2SeqLM.from_pretrained("paust/pko-t5-base")
    tokenizer = AutoTokenizer.from_pretrained("paust/pko-t5-base")
    logger.info("✅ T5 모델 로딩 완료")


def detect_report_type(text: str) -> Dict[str, any]:
    """제보의 유형과 특징을 정밀하게 감지합니다."""
    logger.info("🔍 제보 유형 감지 시작...")

    accident_types = {
        '교통사고': ['교통사고', '차량사고', '충돌', '추돌', '접촉사고', '차량', '운전', '사고차', '신호위반'],
        '화재': ['화재', '불', '연기', '소방차', '전소', '폭발', '불길', '불꽃'],
        '범죄': ['절도', '강도', '폭행', '사기', '성범죄', '성추행', '도둑', '살인', '총격'],
        '자연재해': ['태풍', '지진', '홍수', '침수', '산사태', '폭우', '폭설', '강풍', '기상이변'],
        '건설사고': ['건설현장', '공사현장', '붕괴', '추락', '크레인', '건물붕괴', '콘크리트'],
        '의료사고': ['병원', '응급', '의료사고', '진료', '의료진', '과실', '수술 중', '의사'],
        '감염병': ['코로나', '독감', '감염병', '전염', '격리', '백신', '질병관리청', '확진자', '집단감염'],
        '실종': ['실종', '행방불명', '아이를 찾습니다', '연락두절', '치매노인', '미아', '행방'],
        '해양사고': ['바다', '선박', '침몰', '표류', '조난', '해경', '구조요청', '어선', '해상', '선창'],
        '산업재해': ['기계', '산업현장', '작업 중', '공장', '기계에 끼임', '절단사고', '산재', '현장사고'],
        '기타': ['소음', '악취', '불편', '민원', '정전', '단수', '환경오염']
    }

    detected_types: List[str] = []
    for cat, keywords in accident_types.items():
        if any(keyword in text for keyword in keywords):
            detected_types.append(cat)

    # 시간 정보
    time_patterns = [
        r'\d{1,2}시\s*\d{1,2}분',
        r'\d{1,2}:\d{2}',
        r'(오늘|어제|내일|금일|당일|주말)',
        r'\d{1,2}일\s*전',
        r'(방금|조금\s*전|곧)'
    ]
    time_info = []
    for pattern in time_patterns:
        time_info += re.findall(pattern, text)

    # 장소 정보
    location_patterns = [
        r'[가-힣]{2,10}시\s*[가-힣]{1,10}(구|군)?\s*[가-힣]{1,10}동',
        r'[가-힣]+로\s*\d+길?',
        r'[가-힣]+동\s*[가-힣]+아파트',
        r'[가-힣]+학교',
        r'[가-힣]+병원',
        r'[가-힣]+역',
        r'[가-힣]+항|[가-힣]+해변|[가-힣]+앞바다|[가-힣]+포구'
    ]
    location_info = []
    for pattern in location_patterns:
        location_info += re.findall(pattern, text)

    # 긴급도
    urgency_keywords = ['긴급', '즉시', '응급', '위험', '사망', '중상', '폭발', '조난', '구조요청']
    is_urgent = any(word in text for word in urgency_keywords)

    # 피해 정보
    damage_patterns = {
        '인명피해': [
            r'\d+\s*명\s*사망', r'\d+\s*명\s*부상',
            r'\d+\s*명\s*중상', r'\d+\s*명\s*경상'
        ],
        '재산피해': [
            r'\d+\s*(만|억)\s*원\s*피해',
            r'차량\s*파손', r'건물\s*파손', r'설비\s*손상'
        ],
        '차량번호': [
            r'[0-9]{2,3}[가-힣][0-9]{4}',
            r'[가-힣]{2,3}\s*[0-9]{2,3}[가-힣][0-9]{4}'
        ]
    }
    damage_info = {}
    for category, patterns in damage_patterns.items():
        damage_info[category] = []
        for pat in patterns:
            damage_info[category] += re.findall(pat, text)

    result = {
        "accident_types": detected_types,
        "time_info": time_info,
        "location_info": location_info,
        "is_urgent": is_urgent,
        "damage_info": damage_info
    }

    logger.info(f"✅ 제보 감지 완료: {result}")
    return result


def create_report_summary_prompt(text: str, report_features: Dict) -> str:
    """제보 특징에 맞는 요약 프롬프트를 생성합니다"""
    logger.info("📝 제보 요약 프롬프트 생성...")
    
    # 기본 프롬프트
    base_prompt = "다음 제보를 요약해주세요. "
    
    # 사고 유형별 특화 프롬프트
    if '교통사고' in report_features['accident_types']:
        base_prompt += "교통사고의 경우 시간, 장소, 차량정보, 피해상황을 포함하여 요약해주세요. "
    elif '화재' in report_features['accident_types']:
        base_prompt += "화재의 경우 발생시간, 장소, 피해규모, 소방대 대응상황을 포함하여 요약해주세요. "
    elif '범죄' in report_features['accident_types']:
        base_prompt += "범죄의 경우 발생시간, 장소, 범죄유형, 피해상황을 포함하여 요약해주세요. "
    
    # 긴급도에 따른 프롬프트
    if report_features['is_urgent']:
        base_prompt += "긴급한 상황이므로 즉시 대응이 필요한 내용을 강조하여 요약해주세요. "
    
    # 시간 정보가 있는 경우
    if report_features['time_info']:
        base_prompt += f"발생시간({', '.join(report_features['time_info'])})을 포함하여 요약해주세요. "
    
    # 장소 정보가 있는 경우
    if report_features['location_info']:
        base_prompt += f"발생장소({', '.join(report_features['location_info'])})를 포함하여 요약해주세요. "
    
    # 피해 정보가 있는 경우
    if any(report_features['damage_info'].values()):
        damage_text = []
        for damage_type, info in report_features['damage_info'].items():
            if info:
                damage_text.append(f"{damage_type}: {', '.join(info)}")
        if damage_text:
            base_prompt += f"피해정보({'; '.join(damage_text)})를 포함하여 요약해주세요. "
    
    final_prompt = base_prompt + f"\n\n제보 내용: {text}"
    logger.info(f"✅ 생성된 프롬프트: {final_prompt[:200]}...")
    
    return final_prompt


def clean_summary(summary: str) -> str:
    """요약 결과를 정리합니다"""
    logger.info("🧹 요약 정리 시작...")
    logger.info(f"📝 원본 요약: {summary}")
    
    # 대괄호 안의 메타 정보 제거: [시간], [유형] 등
    summary = re.sub(r'\[[^\[\]]+\]', '', summary)
    
    # "사건 개요:", "요약:" 등의 헤더 제거
    summary = re.sub(r'(사건\s*개요\s*:?|요약\s*:?|내용\s*:?)', '', summary)
    
    # 프롬프트 관련 텍스트 제거
    prompt_patterns = [
        r'다음 제보를 요약해주세요\.?\s*',
        r'교통사고의 경우.*?요약해주세요\.?\s*',
        r'화재의 경우.*?요약해주세요\.?\s*',
        r'범죄의 경우.*?요약해주세요\.?\s*',
        r'긴급한 상황이므로.*?요약해주세요\.?\s*',
        r'발생시간\([^)]*\)을 포함하여 요약해주세요\.?\s*',
        r'발생장소\([^)]*\)를 포함하여 요약해주세요\.?\s*',
        r'피해정보\([^)]*\)를 포함하여 요약해주세요\.?\s*',
        r'제보 내용:\s*',
        r'요약해주세요\.?\s*',
        r'포함하여 요약해주세요\.?\s*',
        r'강조하여 요약해주세요\.?\s*',
        r'발생시간\([^)]*\)을 포함하여\.?\s*',
        r'발생장소\([^)]*\)를 포함하여\.?\s*',
        r'피해정보\([^)]*\)를 포함하여\.?\s*'
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
    
    logger.info(f"✅ 정리된 요약: {result}")
    return result


def extract_numbers(text: str) -> list:
    """텍스트에서 숫자들을 추출합니다"""
    numbers = re.findall(r'\d+', text)
    logger.info(f"📊 추출된 숫자: {numbers}")
    return numbers


def find_sentences_with_numbers(text: str, numbers: list) -> list:
    """숫자가 포함된 문장들을 찾습니다"""
    sentences = re.split(r'[.!?]\s*', text)
    sentences_with_numbers = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(num in sentence for num in numbers):
            sentences_with_numbers.append(sentence)
    
    logger.info(f"🔢 숫자가 포함된 문장 수: {len(sentences_with_numbers)}")
    return sentences_with_numbers


def fix_incomplete_sentences(summary: str) -> str:
    """불완전한 문장을 수정합니다"""
    logger.info("🔧 불완전한 문장 수정 시작...")
    
    sentences = summary.split('\n')
    fixed_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # 문장이 완전하지 않으면 수정
            if not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            fixed_sentences.append(sentence)
    
    result = '\n'.join(fixed_sentences)
    logger.info(f"✅ 수정된 문장: {result}")
    return result


def fix_korean_grammar(sentence: str) -> str:
    """한국어 문법을 수정합니다"""
    # 조사 수정
    sentence = re.sub(r'([가-힣]+)에서\s+([가-힣]+)가', r'\1에서 \2이', sentence)
    sentence = re.sub(r'([가-힣]+)에서\s+([가-힣]+)를', r'\1에서 \2을', sentence)
    
    # 주어-목적어-동사 순서 개선
    # "~에서 ~가 ~했다" → "~에서 ~이 ~했습니다"
    sentence = re.sub(r'([가-힣]+)에서\s+([가-힣]+)가\s+([가-힣]+)했다', r'\1에서 \2이 \3했습니다', sentence)
    
    # 불완전한 문장 구조 수정
    if sentence.endswith('되는.'):
        sentence = sentence.replace('되는.', '되는 사고가 발생했습니다.')
    elif sentence.endswith('되는'):
        sentence = sentence.replace('되는', '되는 사고가 발생했습니다.')
    elif sentence.endswith('하는.'):
        sentence = sentence.replace('하는.', '하는 상황이 발생했습니다.')
    elif sentence.endswith('하는'):
        sentence = sentence.replace('하는', '하는 상황이 발생했습니다.')
    elif sentence.endswith('있는.'):
        sentence = sentence.replace('있는.', '있는 상태입니다.')
    elif sentence.endswith('있는'):
        sentence = sentence.replace('있는', '있는 상태입니다.')
    
    # 구어체를 문어체로 변경
    sentence = re.sub(r'됐어요', '되었습니다', sentence)
    sentence = re.sub(r'있어요', '있습니다', sentence)
    sentence = re.sub(r'없어요', '없습니다', sentence)
    sentence = re.sub(r'해요', '합니다', sentence)
    sentence = re.sub(r'돼요', '됩니다', sentence)
    sentence = re.sub(r'봐요', '봅니다', sentence)
    sentence = re.sub(r'줘요', '줍니다', sentence)
    sentence = re.sub(r'나요', '납니다', sentence)
    sentence = re.sub(r'어요', '습니다', sentence)
    sentence = re.sub(r'아요', '습니다', sentence)
    
    # 불완전한 동사 수정
    sentence = re.sub(r'(\w+)돼서', r'\1되어서', sentence)
    sentence = re.sub(r'(\w+)됐어요', r'\1되었습니다', sentence)
    sentence = re.sub(r'(\w+)됐습니다', r'\1되었습니다', sentence)
    
    # 조사 수정 (이/가, 을/를)
    sentence = re.sub(r'([가-힣]+)가\s+([가-힣]+)를', r'\1이 \2을', sentence)
    sentence = re.sub(r'([가-힣]+)가\s+([가-힣]+)에', r'\1이 \2에', sentence)
    
    return sentence


def improve_grammar_structure(summary: str) -> str:
    """문법 구조를 개선합니다"""
    logger.info("📝 문법 구조 개선 시작...")
    logger.info(f"📝 개선 전: {summary}")
    
    sentences = summary.split('\n')
    improved_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # 한국어 문법 수정
            sentence = fix_korean_grammar(sentence)
            
            # 문장 끝 정리
            if not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            
            improved_sentences.append(sentence)
    
    result = '\n'.join(improved_sentences)
    logger.info(f"✅ 개선 후: {result}")
    return result


def improve_summary_tone(summary: str) -> str:
    """요약의 말투를 개선합니다"""
    logger.info("🎯 말투 개선 시작...")
    logger.info(f"📝 개선 전: {summary}")
    
    # 반복되는 내용 제거
    summary = re.sub(r'제주칼호텔\s*', '', summary)
    summary = re.sub(r'제주 서귀포칼호텔\s*', '제주 서귀포칼호텔', summary)
    
    # 불필요한 정보 제거
    summary = re.sub(r'인명피해:\s*없음\.?', '', summary)
    summary = re.sub(r'사고\s*인명피해:\s*없음\.?', '', summary)
    
    # 말투 개선
    summary = re.sub(r'됐어요', '되었습니다', summary)
    summary = re.sub(r'있어요', '있습니다', summary)
    summary = re.sub(r'없어요', '없습니다', summary)
    summary = re.sub(r'해요', '합니다', summary)
    summary = re.sub(r'돼요', '됩니다', summary)
    
    # 문장 정리
    sentences = summary.split('\n')
    cleaned_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 5:  # 너무 짧은 문장 제거
            # 중복된 내용이 있는지 확인
            if not any(existing in sentence for existing in cleaned_sentences):
                cleaned_sentences.append(sentence)
    
    result = '\n'.join(cleaned_sentences)
    logger.info(f"✅ 개선 후: {result}")
    return result


def preserve_numbers_in_summary(original_text: str, summary: str) -> str:
    """요약에서 누락된 중요한 숫자들을 원본에서 복원합니다"""
    logger.info("🔢 숫자 보존 처리 시작...")
    
    original_numbers = extract_numbers(original_text)
    summary_numbers = extract_numbers(summary)
    
    # 요약에 없는 숫자들을 찾아서 추가
    missing_numbers = [num for num in original_numbers if num not in summary_numbers]
    logger.info(f"📊 누락된 숫자: {missing_numbers}")
    
    if missing_numbers:
        # 누락된 숫자가 포함된 문장들을 찾기
        sentences_with_missing_numbers = find_sentences_with_numbers(original_text, missing_numbers)
        
        # 요약에 추가할 문장들
        additional_sentences = []
        for sentence in sentences_with_missing_numbers:
            if sentence not in summary and len(sentence) > 10:  # 중복 제거 및 최소 길이
                additional_sentences.append(sentence)
        
        # 추가 문장이 있으면 요약에 추가
        if additional_sentences:
            summary += '\n' + '\n'.join(additional_sentences[:2])  # 최대 2개 문장만 추가
            logger.info(f"➕ 추가된 문장: {additional_sentences[:2]}")
    
    logger.info(f"✅ 최종 요약: {summary}")
    return summary


def summarize_text(text: str) -> str:
    """T5 모델을 사용하여 텍스트를 요약합니다"""
    global model, tokenizer
    
    logger.info("🚀 요약 프로세스 시작...")
    logger.info(f"📄 입력 텍스트: {text[:100]}...")
    
    try:
        # 제보 특징 감지
        logger.info("🔍 제보 특징 감지 시작...")
        report_features = detect_report_type(text)
        
        # 텍스트 전처리
        logger.info("🧹 텍스트 전처리 시작...")
        cleaned_text = clean_news(text)
        logger.info(f"✅ 전처리된 텍스트: {cleaned_text[:100]}...")
        
        if not cleaned_text.strip():
            logger.warning("⚠️ 유효한 텍스트가 없습니다")
            return text
        
        # 제보 특징에 맞는 프롬프트 생성
        logger.info("📝 제보 특화 프롬프트 생성...")
        input_text = create_report_summary_prompt(cleaned_text, report_features)
        logger.info(f"🔤 T5 입력: {input_text[:200]}...")
        
        # 토크나이징
        logger.info("🔤 토크나이징 시작...")
        input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).input_ids
        logger.info(f"✅ 토크나이징 완료 (길이: {input_ids.shape[1]})")
        
        # 제보 유형에 따른 생성 파라미터 조정
        generation_params = get_generation_params_by_type(report_features)
        
        # 요약 생성
        logger.info("🤖 T5 모델 요약 생성 시작...")
        output_ids = model.generate(
            input_ids, 
            **generation_params
        )
        logger.info(f"✅ 모델 생성 완료 (출력 길이: {output_ids.shape[1]})")
        
        # 디코딩
        logger.info("🔤 디코딩 시작...")
        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        logger.info(f"✅ 원본 요약: {summary}")
        
        # 프롬프트 제거 (T5가 프롬프트를 포함한 경우)
        summary = clean_summary(summary)
        
        # 제보 특화 후처리
        summary = post_process_report_summary(summary, report_features, text)
        
        logger.info("🎉 요약 프로세스 완료!")
        return summary
        
    except Exception as e:
        logger.error(f"❌ T5 요약 서비스 오류: {e}")
        return text


def get_generation_params_by_type(report_features: Dict) -> Dict:
    """제보 유형에 따른 생성 파라미터를 반환합니다"""
    base_params = {
        'max_length': 100,
        'min_length': 20,
        'num_beams': 4,
        'early_stopping': True,
        'do_sample': True,
        'no_repeat_ngram_size': 3,
        'repetition_penalty': 1.1,
        'length_penalty': 0.8,
        'temperature': 0.8,
        'top_k': 50,
        'top_p': 0.9
    }
    
    # 긴급한 경우 더 상세한 요약
    if report_features['is_urgent']:
        base_params['max_length'] = 150
        base_params['min_length'] = 30
        base_params['temperature'] = 0.7  # 더 일관된 출력
    
    # 교통사고의 경우 차량정보 포함
    if '교통사고' in report_features['accident_types']:
        base_params['max_length'] = 120
        base_params['min_length'] = 25
    
    # 화재의 경우 더 상세한 정보
    if '화재' in report_features['accident_types']:
        base_params['max_length'] = 140
        base_params['min_length'] = 30
    
    return base_params


def post_process_report_summary(summary: str, report_features: Dict, original_text: str) -> str:
    """제보 요약을 후처리합니다"""
    logger.info("🔧 제보 특화 후처리 시작...")
    
    # 불완전한 문장 수정
    summary = fix_incomplete_sentences(summary)
    
    # 문법 구조 개선
    summary = improve_grammar_structure(summary)
    
    # 말투 개선
    summary = improve_summary_tone(summary)
    
    # 숫자 보존
    summary = preserve_numbers_in_summary(original_text, summary)
    
    # 제보 특화 정리
    summary = format_report_summary(summary, report_features)
    
    logger.info(f"✅ 후처리 완료: {summary}")
    return summary


def format_report_summary(summary: str, report_features: Dict) -> str:
    """제보 요약을 형식에 맞게 정리합니다"""
    logger.info("📋 제보 형식 정리 시작...")
    
    # 긴급한 경우 표시
    if report_features['is_urgent']:
        summary = "[긴급] " + summary
    
    # 사고 유형 표시
    if report_features['accident_types']:
        accident_type = report_features['accident_types'][0]
        summary = f"[{accident_type}] " + summary
    
    # 시간 정보가 있으면 앞에 배치
    if report_features['time_info']:
        time_info = report_features['time_info'][0]
        if not summary.startswith(f"[{time_info}]"):
            summary = f"[{time_info}] " + summary
    
    # 장소 정보가 있으면 포함
    if report_features['location_info'] and not any(loc in summary for loc in report_features['location_info']):
        location_info = report_features['location_info'][0]
        summary = summary.replace(".", f" ({location_info}).", 1)
    
    logger.info(f"✅ 형식 정리 완료: {summary}")
    return summary 