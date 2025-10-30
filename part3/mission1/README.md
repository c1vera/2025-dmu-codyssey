<<<<<<< HEAD
# 문제2 감동의 메시지 - HTML 메일 전송 프로그램

## 개요
화성에서 지구로 HTML 형식의 메일을 전송하는 프로그램입니다. CSV 파일을 통해 다중 수신자에게 메일을 보낼 수 있습니다.

## 주요 기능

### 1. HTML 형식 메일 전송
- HTML 태그를 사용한 서식 있는 메일 전송
- CSS 스타일 적용 가능
- 텍스트와 HTML 모두 지원

### 2. CSV 파일을 통한 다중 수신자 관리
- `mail_target_list.csv` 파일에서 수신자 목록 읽기
- 이름과 이메일 주소를 CSV 형식으로 관리
- 개별 전송과 일괄 전송 방식 모두 지원

### 3. 전송 방식 선택
- **개별 전송**: 한 명씩 순차적으로 전송 (안정적)
- **일괄 전송**: 여러 명에게 한 번에 전송 (빠름)

### 4. 보너스 기능
- 네이버 메일을 통한 전송 지원
- 첨부파일 포함 메일 전송

## 파일 구조

```
part3/mission1/
├── sendmail.py              # 메인 프로그램
├── mail_target_list.csv     # 수신자 목록 파일
├── sample_html_email.html   # HTML 메일 예시
└── README.md               # 사용법 설명서
```

## 사용 방법

### 1. 프로그램 실행
```bash
python sendmail.py
```

### 2. 이메일 설정
- Gmail 계정 정보 입력
- 앱 비밀번호 사용 (2단계 인증 필요)
- 수신자 이메일 주소 입력

### 3. 메일 전송 옵션 선택
1. **간단한 텍스트 메일**: 기본 텍스트 메일
2. **HTML 형식 메일**: HTML 태그 사용 가능
3. **CSV 파일을 통한 다중 수신자 HTML 메일**: 주요 기능
4. **첨부파일이 있는 메일**: 파일 첨부 가능
5. **네이버 메일을 통한 전송**: 네이버 메일 사용

### 4. CSV 파일 형식
```csv
이름,이메일
김철수,kimcs@example.com
이영희,leeyh@example.com
박민수,parkms@example.com
```

## HTML 메일 예시

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>화성에서 온 메시지</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #ff6b6b; color: white; padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 화성에서 온 메시지</h1>
    </div>
    <div class="content">
        <p>한송희 박사가 화성에서 생존하고 있습니다!</p>
        <p><strong>빠른 구조가 필요합니다!</strong></p>
    </div>
</body>
</html>
```

## 전송 방식 비교

### 개별 전송 (Individual)
- **장점**: 안정적, 개별 오류 처리 가능
- **단점**: 시간이 오래 걸림
- **사용 시기**: 중요한 메일, 소수 수신자

### 일괄 전송 (Bulk)
- **장점**: 빠른 전송 속도
- **단점**: 한 명 실패 시 전체 실패 가능
- **사용 시기**: 일반 공지, 다수 수신자

## 네이버 메일 설정 (보너스)

네이버 메일을 사용하려면:
1. 네이버 메일 계정에서 SMTP 설정 활성화
2. 프로그램에서 옵션 5 선택
3. 네이버 계정 정보 입력

## 주의사항

1. **Gmail 사용 시**:
   - 2단계 인증 활성화 필수
   - 앱 비밀번호 생성 필요
   - 일반 비밀번호 사용 불가

2. **네이버 메일 사용 시**:
   - SMTP 설정에서 보안 설정 확인
   - 앱 비밀번호 또는 일반 비밀번호 사용 가능

3. **CSV 파일**:
   - UTF-8 인코딩 사용
   - 첫 번째 줄은 헤더 (이름,이메일)
   - 쉼표로 구분

## 오류 해결

### 인증 오류
- 이메일 주소와 비밀번호 확인
- 2단계 인증 설정 확인
- 앱 비밀번호 사용 확인

### 수신자 오류
- 이메일 주소 형식 확인
- CSV 파일 형식 확인
- 파일 경로 확인

### 서버 연결 오류
- 인터넷 연결 확인
- 방화벽 설정 확인
- SMTP 서버 상태 확인

## 개발 환경

- **Python**: 3.x 버전
- **라이브러리**: Python 기본 라이브러리만 사용
- **코딩 스타일**: PEP 8 준수
- **문자열**: 작은따옴표(') 기본 사용

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

=======
<img width="492" height="446" alt="image" src="https://github.com/user-attachments/assets/ecbb9f5c-115c-45bf-bb39-9488d73b7ae0" />
<img width="885" height="681" alt="image" src="https://github.com/user-attachments/assets/9286783a-3f32-4da9-be33-f2b8cda87ce5" />
<img width="1329" height="110" alt="image" src="https://github.com/user-attachments/assets/aab82851-b0c2-4dbb-92d9-451d0b8cc3d9" />
>>>>>>> 8a16c1ccf1a0ed517ae0239975d995e347621d18
