# 🌌 MissionComputer: 크로스 플랫폼 키 감지 기반 화성 기지 시스템/센서 시뮬레이터

> 화성 기지의 생존 환경 정보를 5초마다 출력하고, 시스템 정보와 부하 상태까지 확인할 수 있는 Python 기반 시뮬레이터입니다.  
> `q` 키를 누르면 실시간으로 종료되며, 운영체제/플랫폼에 관계없이 정상 작동합니다.

---

## 💌 주요 기능

- 🌡️ 더미 센서(DummySensor)를 통해 환경 데이터 무작위 생성
- 🧠 `MissionComputer` 클래스에서 센서 데이터를 5초마다 출력
- 📈 5분마다 평균 센서 데이터를 계산 및 출력 (테스트 시 30초로 설정 가능)
- 💻 시스템 정보(OS, CPU, 메모리) 및 부하 상태 출력 기능 추가
- ⚙️ 출력 항목을 `setting.txt` 파일을 통해 커스터마이징 가능
- ⌨️ `q` 키를 누르면 실시간으로 프로그램 종료

---

## 💌 파일 구성

| 파일명 | 설명 |
|--------|------|
| `dummy_sensor.py` | 더미 센서 데이터 생성 클래스 |
| `cross_platform_key_listener.py` | 운영체제별 실시간 키 입력 감지 유틸리티 |
| `mars_mission_computer.py` | 메인 실행 파일. 센서 출력, 시스템 정보 출력, 키 감지 처리 |
| `setting.txt` | 시스템 정보 출력 항목 설정 파일 (선택 사항) |

---

## 💌 실행 방법

### ▶️ 1. 실행 전 확인

- Python 3.x 이상 설치
- 외부 라이브러리 `psutil`만 설치되어 있으면 됨 (시스템 정보용)
  ```bash
  pip install psutil
  ```

### ▶️ 2. 실행 명령어

```bash
python mars_mission_computer.py
```

---

## 💌 작동 예시

```plaintext
=== 시스템 정보 ===
{
  'os_name': 'Windows',
  'cpu_core_count': 8,
  'memory_total': 15.92
}

=== 시스템 부하 정보 ===
{
  'cpu_usage_percent': 12.5,
  'memory_usage_percent': 48.2
}

센서 데이터 수집 시작 (q 키를 누르면 종료)

{
  'mars_base_internal_temperature': 23.4,
  'mars_base_external_temperature': 11.2,
  ...
}
'q' 키를 누르면 종료됩니다.
```

사용자가 `q` 키를 누르면:

```plaintext
System stopped…
```

---

## 💌 setting.txt 예시

출력할 항목만 골라서 아래처럼 작성할 수 있습니다:

```
os_name
cpu_core_count
memory_total
cpu_usage_percent
```

→ 시스템 정보 및 부하 항목에서 지정한 것만 출력됩니다.

---

## 💌 개발자 코멘트

> 기존의 `input()` 방식은 Enter를 눌러야 인식되기 때문에 실시간 처리에 부적합합니다.  
> 외부 라이브러리를 사용할 수 없는 조건에서 실시간 키 입력을 구현하기 위해 운영체제별 방식으로 직접 처리하였습니다.  
> 또한 시스템 정보 필터링 기능은 `setting.txt`를 통해 사용자가 원하는 항목만 출력할 수 있게 유연성을 고려했습니다.

---

## 💌 의존성

| 모듈 | 설명 |
|------|------|
| `platform`, `os`, `time` | Python 표준 라이브러리 |
| `psutil` | 시스템 정보/부하 수집용. 과제에서 사용 허용됨 |
| `cross_platform_key_listener.py` | 키 입력 감지용 직접 구현 모듈 |
| `dummy_sensor.py` | 테스트용 센서 클래스 |

---

## 💡 참고 사항

- macOS/Linux에서는 터미널에서 실행하세요 (더블 클릭 실행 시 키 감지 안 됨)
- 일부 Linux 배포판에서는 루트 권한이 필요할 수 있음 (`sudo python mars_mission_computer.py`)
- Windows 환경에서 가장 안정적으로 동작 테스트 완료됨

---

## ✅ 요구사항 체크리스트

### 📌 수행 과제

| 항목 | 구현 여부 | 설명 |
|------|:--------:|------|
| `MissionComputer` 클래스 생성 | ✅ | 환경 및 시스템 정보 처리 담당 |
| `env_values` 속성 포함 | ✅ | 센서 데이터 저장용 딕셔너리 |
| 6가지 환경 정보 포함 | ✅ | 온도, 습도, 광량, CO₂, 산소 등 |
| `DummySensor` 클래스 사용 | ✅ | 무작위 테스트용 센서 |
| `ds`로 인스턴스화 | ✅ | `ds = DummySensor()` 사용 |
| `get_sensor_data()` 구현 | ✅ | 센서 값 수집 및 출력 |
| JSON 유사 형식으로 출력 | ✅ | 딕셔너리 구조로 직접 출력 |
| 5초 간격 반복 출력 | ✅ | 0.1초 간격 q 키 감지 루프 포함 |
| `RunComputer` 인스턴스 생성 및 실행 | ✅ | `__main__`에서 호출 |
| 시스템 정보 출력 기능 구현 | ✅ | `platform`, `os`, `psutil` 사용 |
| 시스템 부하 출력 기능 구현 | ✅ | CPU/메모리 실시간 상태 출력 |
| setting.txt 필터 기능 구현 | ✅ | 사용자 지정 항목만 출력 가능 |

---

### 📌 제약사항

| 항목 | 충족 여부 | 설명 |
|------|:--------:|------|
| Python 3.x 사용 | ✅ | 최신 문법 사용 |
| 외부 라이브러리 최소화 | ✅ | `psutil`만 허용 |
| 시간 관련 모듈 사용 가능 | ✅ | `time` 사용 |
| PEP8 스타일 가이드 준수 | ✅ | 들여쓰기, 공백 등 정리됨 |
| 예외 처리 포함 | ✅ | 시스템 정보 조회 시 try-except 포함 |
| 경고/에러 없이 실행 | ✅ | 모든 OS에서 정상 작동 확인 |

---

### 🌟 보너스 과제

| 항목 | 구현 여부 | 설명 |
|------|:--------:|------|
| 특정 키(`q`)로 출력 종료 | ✅ | `cross_platform_key_listener`로 실시간 감지 |
| 5분 평균값 출력 | ✅ | `print_5min_average()` 구현 완료 |
| setting.txt로 필터링 | ✅ | 선택된 항목만 출력 가능 |

