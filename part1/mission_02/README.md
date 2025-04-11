# 🛰️ MissionComputer Log Analyzer

> `mission_computer_main.log` 파일을 분석하여 시간 역순으로 정렬하고 JSON 포맷으로 저장하며, 보너스로 특정 키워드를 포함한 로그 검색 기능도 제공합니다.  
> Python의 표준 라이브러리만을 사용하여 구현되었습니다.

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
| `README.md` | 프로젝트 소개 및 기능 요약 문서 |

---

## 💌 실행 방법

```bash
python mission_log_analyzer.py
```

실행 시:
- 로그를 리스트로 파싱
- 시간 기준으로 역순 정렬
- JSON 파일로 저장
- 키워드 입력 시 관련 로그만 필터링하여 출력

---

## ✅ 요구사항 체크리스트

| 항목 | 구현 여부 | 설명 |
|------|:--------:|------|
| 로그 파일 읽기 | ✅ | `read_log_file()` 함수 |
| 리스트 변환 및 정렬 | ✅ | `sorted(..., reverse=True)` |
| 딕셔너리 변환 | ✅ | `logs_to_dict()` 함수 |
| JSON 저장 | ✅ | `save_json()` 함수 |
| 키워드 검색 | ✅ | `search_keyword()` 함수 |
| 예외 처리 포함 | ✅ | `try-except` 사용 |
| 외부 라이브러리 미사용 | ✅ | 표준 라이브러리만 사용 |
| UTF-8 인코딩 | ✅ | 로그 파일 및 JSON 저장 모두 utf-8 |

---

## 🧠 개선 제안 (리뷰 기반)

| 항목 | 개선 제안 |
|------|-----------|
| 모듈화 | `main()` 함수로 메인 블록을 분리하면 가독성과 유지보수성이 높아짐 |
| 주석 강화 | 함수에 파라미터/반환 타입을 포함한 Docstring 사용 권장 |
| 정렬 로직 | `datetime.strptime()` 사용으로 정확한 시간 기반 정렬 가능 |
| 파일 존재 경고 | JSON 파일 저장 시 이미 존재하는 경우 덮어쓰기 경고 출력 가능 |
| 테스트 가능성 | 핵심 로직을 별도 모듈로 분리하면 단위 테스트가 용이해짐 |

---

## 💌 개발자 코멘트

> 문제의 핵심 요구사항을 충실히 구현하면서도, 구조적인 개선 여지까지 고려했습니다.  
> 추후 확장성, 재사용성을 고려하여 함수 구조 개선과 모듈화를 고려할 수 있습니다.
>

## 💌 터미널 출력 메세지
```plaintext
PS C:\Users\vera\Desktop\4-1\2025-dmu-codyssey\part1\mission_02> python .\mission_log_analyzer.py   

[1] 읽은 로그:
['2023-08-27 10:00:00', 'INFO', 'Rocket initialization process started.']
['2023-08-27 10:02:00', 'INFO', 'Power systems online. Batteries at optimal charge.']
['2023-08-27 10:05:00', 'INFO', 'Communication established with mission control.']
['2023-08-27 10:08:00', 'INFO', 'Pre-launch checklist initiated.']
['2023-08-27 10:10:00', 'INFO', 'Avionics check: All systems functional.']
['2023-08-27 10:12:00', 'INFO', 'Propulsion check: Thrusters responding as expected.']
['2023-08-27 10:15:00', 'INFO', 'Life support systems nominal.']
['2023-08-27 10:18:00', 'INFO', 'Cargo bay secured and sealed properly.']
['2023-08-27 10:20:00', 'INFO', 'Final system checks complete. Rocket is ready for launch.']
['2023-08-27 10:23:00', 'INFO', 'Countdown sequence initiated.']
['2023-08-27 10:25:00', 'INFO', 'Engine ignition sequence started.']
['2023-08-27 10:27:00', 'INFO', 'Engines at maximum thrust. Liftoff imminent.']
['2023-08-27 10:30:00', 'INFO', 'Liftoff! Rocket has left the launchpad.']
['2023-08-27 10:32:00', 'INFO', 'Initial telemetry received. Rocket is on its trajectory.']
['2023-08-27 10:35:00', 'INFO', 'Approaching max-Q. Aerodynamic pressure increasing.']
['2023-08-27 10:37:00', 'INFO', 'Max-Q passed. Vehicle is stable.']
['2023-08-27 10:40:00', 'INFO', 'First stage engines throttled down as planned.']
['2023-08-27 10:42:00', 'INFO', 'Main engine cutoff confirmed. Stage separation initiated.']
['2023-08-27 10:45:00', 'INFO', 'Second stage ignition. Rocket continues its ascent.']
['2023-08-27 10:48:00', 'INFO', 'Payload fairing jettisoned. Satellite now exposed.']
['2023-08-27 10:50:00', 'INFO', 'Orbital insertion calculations initiated.']
['2023-08-27 10:52:00', 'INFO', 'Navigation systems show nominal performance.']
['2023-08-27 10:55:00', 'INFO', 'Second stage burn nominal. Rocket velocity increasing.']
['2023-08-27 10:57:00', 'INFO', 'Entering planned orbit around Earth.']
['2023-08-27 11:00:00', 'INFO', 'Orbital operations initiated. Satellite deployment upcoming.']
['2023-08-27 11:05:00', 'INFO', 'Satellite deployment successful. Mission objectives achieved.']
['2023-08-27 11:10:00', 'INFO', "Initiating deorbit maneuvers for rocket's reentry."]
['2023-08-27 11:15:00', 'INFO', 'Reentry sequence started. Atmospheric drag noticeable.']
['2023-08-27 11:20:00', 'INFO', 'Heat shield performing as expected during reentry.']
['2023-08-27 11:25:00', 'INFO', 'Main parachutes deployed. Rocket descent rate reducing.']
['2023-08-27 11:28:00', 'INFO', 'Touchdown confirmed. Rocket safely landed.']
['2023-08-27 11:30:00', 'INFO', 'Mission completed successfully. Recovery team dispatched.']
['2023-08-27 11:35:00', 'INFO', 'Oxygen tank unstable.']
['2023-08-27 11:40:00', 'INFO', 'Oxygen tank explosion.']
['2023-08-27 12:00:00', 'INFO', 'Center and mission control systems powered down.']

[2] 정렬된 로그:
['2023-08-27 12:00:00', 'INFO', 'Center and mission control systems powered down.']
['2023-08-27 11:40:00', 'INFO', 'Oxygen tank explosion.']
['2023-08-27 11:35:00', 'INFO', 'Oxygen tank unstable.']
['2023-08-27 11:30:00', 'INFO', 'Mission completed successfully. Recovery team dispatched.']
['2023-08-27 11:28:00', 'INFO', 'Touchdown confirmed. Rocket safely landed.']
['2023-08-27 11:25:00', 'INFO', 'Main parachutes deployed. Rocket descent rate reducing.']
['2023-08-27 11:20:00', 'INFO', 'Heat shield performing as expected during reentry.']
['2023-08-27 11:15:00', 'INFO', 'Reentry sequence started. Atmospheric drag noticeable.']
['2023-08-27 11:10:00', 'INFO', "Initiating deorbit maneuvers for rocket's reentry."]
['2023-08-27 11:05:00', 'INFO', 'Satellite deployment successful. Mission objectives achieved.']
['2023-08-27 11:00:00', 'INFO', 'Orbital operations initiated. Satellite deployment upcoming.']
['2023-08-27 10:57:00', 'INFO', 'Entering planned orbit around Earth.']
['2023-08-27 10:55:00', 'INFO', 'Second stage burn nominal. Rocket velocity increasing.']
['2023-08-27 10:52:00', 'INFO', 'Navigation systems show nominal performance.']
['2023-08-27 10:50:00', 'INFO', 'Orbital insertion calculations initiated.']
['2023-08-27 10:48:00', 'INFO', 'Payload fairing jettisoned. Satellite now exposed.']
['2023-08-27 10:45:00', 'INFO', 'Second stage ignition. Rocket continues its ascent.']
['2023-08-27 10:42:00', 'INFO', 'Main engine cutoff confirmed. Stage separation initiated.']
['2023-08-27 10:40:00', 'INFO', 'First stage engines throttled down as planned.']
['2023-08-27 10:37:00', 'INFO', 'Max-Q passed. Vehicle is stable.']
['2023-08-27 10:35:00', 'INFO', 'Approaching max-Q. Aerodynamic pressure increasing.']
['2023-08-27 10:32:00', 'INFO', 'Initial telemetry received. Rocket is on its trajectory.']
['2023-08-27 10:30:00', 'INFO', 'Liftoff! Rocket has left the launchpad.']
['2023-08-27 10:27:00', 'INFO', 'Engines at maximum thrust. Liftoff imminent.']
['2023-08-27 10:25:00', 'INFO', 'Engine ignition sequence started.']
['2023-08-27 10:23:00', 'INFO', 'Countdown sequence initiated.']
['2023-08-27 10:20:00', 'INFO', 'Final system checks complete. Rocket is ready for launch.']
['2023-08-27 10:18:00', 'INFO', 'Cargo bay secured and sealed properly.']
['2023-08-27 10:15:00', 'INFO', 'Life support systems nominal.']
['2023-08-27 10:12:00', 'INFO', 'Propulsion check: Thrusters responding as expected.']
['2023-08-27 10:10:00', 'INFO', 'Avionics check: All systems functional.']
['2023-08-27 10:08:00', 'INFO', 'Pre-launch checklist initiated.']
['2023-08-27 10:05:00', 'INFO', 'Communication established with mission control.']
['2023-08-27 10:02:00', 'INFO', 'Power systems online. Batteries at optimal charge.']
['2023-08-27 10:00:00', 'INFO', 'Rocket initialization process started.']

[3] JSON 파일로 저장 완료 → mission_computer_main.json

[4] 검색할 키워드를 입력하세요: max

🔍 "max" 포함 로그:
2023-08-27 10:37:00 - Max-Q passed. Vehicle is stable.
2023-08-27 10:35:00 - Approaching max-Q. Aerodynamic pressure increasing.
2023-08-27 10:27:00 - Engines at maximum thrust. Liftoff imminent.
```
