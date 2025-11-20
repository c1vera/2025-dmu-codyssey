미션: FastAPI 기반 TO-DO API (venv + uvicorn + CSV 저장)

개발 환경
- Python 3.x
- FastAPI, Uvicorn (런타임)
- 표준 라이브러리만 사용해 CSV로 데이터 영속화

가상환경 생성 및 의존성 설치 (Windows PowerShell)
1) 프로젝트 루트로 이동
   cd C:\Users\vera\Desktop\4-1\2025-dmu-codyssey\part4\mission1
2) 가상환경 생성
   python -m venv .venv
3) 가상환경 활성화
   .\.venv\Scripts\Activate.ps1
4) 업그레이드 및 설치
   python -m pip install --upgrade pip
   pip install fastapi uvicorn

실행
- 앱 엔트리: todo.py (FastAPI 앱 객체 이름: app)
- 개발 서버 실행:
  uvicorn todo:app --reload --host 127.0.0.1 --port 8000

엔드포인트
- POST /todos/add
  - 요청 본문: Dict (예: {'task': '할 일', 'done': False})
  - 응답: Dict {'status': 'ok', 'item': <추가된 항목>, 'count': <전체 개수>}
- GET /todos/list
  - 응답: Dict {'todo_list': [ ... ], 'count': <전체 개수>}

데이터 저장
- 파일: todo_list.csv (현재 디렉터리)
- 컬럼: item (요청 Dict를 JSON 문자열로 저장)
- 서버 시작 시 CSV에서 읽어 메모리의 todo_list를 초기화

curl로 동작 확인 예시
1) 추가 (POST)
   curl -s -X POST "http://127.0.0.1:8000/todos/add" ^
        -H "Content-Type: application/json" ^
        -d "{\"task\":\"첫 번째 할 일\",\"done\":false}"

2) 조회 (GET)
   curl -s "http://127.0.0.1:8000/todos/list"

코딩 규약
- 문자열은 기본적으로 ' ' 사용
- = 양옆 공백 유지 (예: foo = (0,))
- 들여쓰기는 공백 사용, PEP 8 준수
- 함수 이름은 소문자 + snake_case
- APIRouter 사용 필수


