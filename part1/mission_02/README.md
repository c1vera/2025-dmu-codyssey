# 🛰️ MissionComputer Log Analyzer

> `mission_computer_main.log` 파일을 기반으로 로그를 읽고, 정렬 및 JSON 변환까지 처리하는 파이썬 기반 로그 분석 도구입니다.  
> 외부 라이브러리 없이 Python 표준 기능만으로 CSV → List → Dict → JSON 변환을 수행하며, 보너스로 특정 키워드 검색 기능도 제공합니다.

---

## 💌 주요 기능

- 로그 파일(.log)을 읽어 리스트로 변환
- 날짜/시간 기준으로 시간 역순 정렬
- 리스트를 딕셔너리로 변환 후 JSON으로 저장
- 메시지 내용에서 특정 키워드를 포함한 로그만 필터링 (보너스)

---

## 💌 파일 구성

| 파일명 | 설명 |
|--------|------|
| `mission_computer_main.log` | 로그 원본 데이터 (CSV 포맷) |
| `mission_computer_main.json` | 정렬 후 저장되는 JSON 파일 |
| `mission_log_analyzer.py` | 전체 로직을 수행하는 실행 파일 |

---

## 💌 실행 방법

### ▶️ 1. 실행 전 준비

- Python 3.x 이상 설치
- 외부 라이브러리 불필요 (✅ 표준 라이브러리만 사용)

### ▶️ 2. 실행 명령어

```bash
python mission_log_analyzer.py
```

실행 시 로그 전체를 읽고 정렬하며, JSON으로 저장한 뒤 키워드 검색까지 수행합니다.

---

## 💌 작동 예시

```plaintext
[1] 읽은 로그 리스트:
['2023-08-27 10:00:00', 'INFO', 'Rocket initialization process started.']
...

[2] 시간 역순 정렬된 로그:
['2023-08-27 12:00:00', 'INFO', 'Center and mission control systems powered down.']
...

[4] JSON 파일로 저장 완료 → mission_computer_main.json

[5] 보너스: 키워드 검색
검색할 키워드를 입력하세요: Oxygen
2023-08-27 11:35:00 - Oxygen tank unstable.
2023-08-27 11:40:00 - Oxygen tank explosion.
```

---

## 💌 개발자 코멘트

> 로그 파일을 처리할 때 예외 상황이 자주 발생할 수 있어 `FileNotFoundError`, `Exception` 등을 명시적으로 처리했습니다.  
> 시간 형식을 기준으로 정렬할 때는 문자열 비교로도 충분하다는 점을 활용했습니다 (YYYY-MM-DD HH:MM:SS).  
> JSON 저장 시 `ensure_ascii=False`를 활용해 한글이 깨지지 않도록 처리했습니다.

---

## ✅ 요구사항 체크리스트

### 📌 수행 과제

| 항목 | 구현 여부 | 설명 |
|------|:--------:|------|
| 로그 파일 읽기 | ✅ | `read_log_file()` 함수 사용 |
| 리스트로 변환 | ✅ | 각 행을 `[timestamp, event, message]` 형태로 처리 |
| 시간 역순 정렬 | ✅ | `sorted(..., reverse=True)` |
| 딕셔너리로 변환 | ✅ | `logs_to_dict()` 함수 사용 |
| JSON으로 저장 | ✅ | `save_json()` 함수 사용 |
| 키워드 검색 기능 | ✅ | `search_keyword()` 함수 구현 |
| 예외처리 포함 | ✅ | 파일 처리 및 변환 과정 전반에 `try-except` 사용 |

---

### 📌 제약사항

| 항목 | 충족 여부 | 설명 |
|------|:--------:|------|
| Python 3.x 사용 | ✅ | 최신 문법 기반으로 작성 |
| 외부 라이브러리 미사용 | ✅ | `json` 외에는 모두 기본 문법 사용 |
| UTF-8 인코딩 사용 | ✅ | 로그 파일과 JSON 저장 모두 `encoding='utf-8'` |
| PEP8 스타일 준수 | ✅ | 코드 간결하게 작성, 공백 및 들여쓰기 포함 |
| 파일명 명시적 지정 | ✅ | log와 json 파일명을 과제명 그대로 사용 |

---

### 🌟 보너스 과제

| 항목 | 구현 여부 | 설명 |
|------|:--------:|------|
| 시간 역순 정렬 출력 | ✅ | 정렬 결과 리스트 출력 포함 |
| 특정 키워드 포함 로그 추출 | ✅ | 입력값 기반으로 메시지 필터링 |