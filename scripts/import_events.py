import json
import sys
import os
from datetime import datetime
from typing import Dict, List

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from models.event import Event
from models.timeline import Timeline

def parse_date(date_str: str) -> datetime:
    """날짜 문자열을 datetime 객체로 변환"""
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return datetime.now()

def import_event_from_json(json_data: Dict) -> Event:
    """JSON 데이터로부터 Event 객체 생성"""
    # ID는 DB에서 자동 생성
    event = Event(
        title=json_data.get('title'),
        summary=json_data.get('summary'),
        description=json_data.get('summary', ''),  # description이 필수이므로 summary를 사용
        event_date=parse_date(json_data.get('eventDate')),
        region_id=json_data.get('region_id'),
        created_at=parse_date(json_data.get('createdAt')),
        updated_at=parse_date(json_data.get('updatedAt')),
        view_count=json_data.get('viewCount', 0),
        category=json_data.get('category'),
        status="new",  # 기본값
        like_count=0,  # 기본값
        tags=[],  # 기본값
        source_type="",  # 기본값
        source_url="",  # 기본값
        source_name="",  # 기본값
        created_by_id=1,  # 임시로 1번 사용자로 설정
        is_verified=False,  # 기본값
        verified_at=None  # 기본값
    )
    return event

def import_timeline_from_json(timeline_data: Dict, event_id: str) -> Timeline:
    """JSON 데이터로부터 Timeline 객체 생성"""
    timeline = Timeline(
        title=timeline_data.get('title'),
        summary=timeline_data.get('description', ''),  # Timeline 모델에는 summary 필드가 있음
        event_date=parse_date(timeline_data.get('eventDate')),
        source_name=timeline_data.get('sourceName', ''),
        source_url=timeline_data.get('sourceUrl', ''),
        source_type=timeline_data.get('sourceType', ''),
        created_by_id=timeline_data.get('createdBy'),
        is_verified=timeline_data.get('isVerified', False),
        verified_at=parse_date(timeline_data.get('verifiedAt')) if timeline_data.get('verifiedAt') else None,
        created_at=parse_date(timeline_data.get('createdAt')),
        is_active=timeline_data.get('isActive', True),
        event_id=event_id
    )
    return timeline

def import_events_from_file(file_path: str):
    """JSON 파일에서 이벤트와 타임라인을 DB에 저장"""
    db = SessionLocal()
    
    try:
        # JSON 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 단일 이벤트인지 리스트인지 확인
        if isinstance(data, dict):
            events_data = [data]
        else:
            events_data = data
        
        for event_data in events_data:
            print(f"📝 이벤트 처리 중: {event_data.get('title', 'Unknown')}")
            
            # Event 저장
            event = import_event_from_json(event_data)
            db.add(event)
            db.flush()  # ID 생성을 위해 flush
            
            print(f"  🆔 생성된 Event ID: {event.id}")
            
            # Timeline 저장
            timelines = event_data.get('timelines', [])
            for i, timeline_data in enumerate(timelines):
                timeline = import_timeline_from_json(timeline_data, event.id)
                db.add(timeline)
                print(f"  📅 타임라인 추가: {timeline.title}")
            
            print(f"✅ 이벤트 저장 완료: {event.title}")
        
        db.commit()
        print(f"🎉 총 {len(events_data)}개 이벤트와 {sum(len(e.get('timelines', [])) for e in events_data)}개 타임라인 저장 완료!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

def import_events_from_directory(directory_path: str):
    """디렉토리 내의 모든 JSON 파일을 처리"""
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            print(f"\n📁 파일 처리 중: {filename}")
            import_events_from_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python import_events.py <file_or_directory_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        import_events_from_file(path)
    elif os.path.isdir(path):
        import_events_from_directory(path)
    else:
        print(f"❌ 경로를 찾을 수 없습니다: {path}")
        sys.exit(1) 