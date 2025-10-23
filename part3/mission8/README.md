# 네이버 로그인 크롤링 프로그램

## 개요
네이버 사이트에 로그인하여 로그인 전후 콘텐츠 차이를 확인하고, 로그인 후에만 보이는 콘텐츠를 크롤링하는 프로그램입니다.

## 주요 기능
- 네이버 로그인 전후 콘텐츠 차이 확인
- 자연스러운 입력 방식으로 CAPTCHA 우회 시도
- 셀레니움을 이용한 자동 로그인 (자동화 탐지 방지)
- 로그인 후 전용 콘텐츠 크롤링
- 네이버 메일 제목 크롤링 (보너스 과제)

## 설치 방법

### 1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Chrome 브라우저 설치
Chrome 브라우저가 설치되어 있어야 합니다.

### 3. ChromeDriver 수동 다운로드 및 설정
1. **Chrome 버전 확인**
   - Chrome 브라우저를 열고 주소창에 `chrome://version/` 입력
   - 버전 정보 확인 (예: 131.0.6778.108)

2. **ChromeDriver 다운로드**
   - https://chromedriver.chromium.org/downloads 접속
   - Chrome 버전과 일치하는 드라이버 다운로드
   - 또는 https://googlechromelabs.github.io/chrome-for-testing/ 에서 최신 버전 다운로드

3. **드라이버 배치**
   - 다운로드한 `chromedriver.exe` 파일을 이 프로젝트 폴더에 복사
   - 또는 `drivers` 폴더를 만들어서 그 안에 저장
   - 또는 시스템 PATH 환경변수에 chromedriver 경로 추가

## 사용 방법

### 기본 실행
```bash
python crawling_KBS.py
```

### 실행 과정
1. 프로그램 실행 시 네이버 아이디와 비밀번호를 입력합니다.
2. 자동으로 Chrome 브라우저가 열리고 자연스러운 입력 방식으로 네이버 로그인을 수행합니다.
3. CAPTCHA가 나타나면 브라우저에서 수동으로 인증을 완료합니다.
4. 로그인 성공 시 로그인 후에만 보이는 콘텐츠를 크롤링합니다.
5. 네이버 메일 제목도 함께 크롤링합니다 (보너스 과제).
6. 결과를 화면에 출력합니다.

## 크롤링 대상 콘텐츠
- 개인화된 뉴스 섹션
- 메일 알림
- 개인 설정 메뉴
- 로그아웃 버튼 (로그인 상태 확인)
- 네이버 메일 제목 (보너스 과제)

## CAPTCHA 우회 기능
- **자연스러운 타이핑**: 사람처럼 랜덤한 지연 시간으로 입력
- **자연스러운 마우스 움직임**: 실제 사용자처럼 마우스 이동 시뮬레이션
- **자동화 탐지 방지**: 웹드라이버 탐지를 우회하는 다양한 설정
- **수동 인증 지원**: CAPTCHA 발생 시 사용자가 직접 해결 가능
- **완전한 페이지 로딩**: JavaScript와 이미지가 모두 로드될 때까지 대기
- **자연스러운 브라우저**: 일반 사용자와 동일한 브라우저 환경 제공

## 주의사항
- 네이버의 로그인 정책 변경 시 코드 수정이 필요할 수 있습니다.
- 과도한 요청으로 인한 IP 차단을 방지하기 위해 적절한 딜레이를 두고 있습니다.
- 실제 사용 시에는 환경변수나 설정파일을 통해 인증 정보를 관리하는 것을 권장합니다.
- CAPTCHA가 나타나면 브라우저에서 수동으로 인증을 완료해주세요.

## 코드 구조
- `NaverLoginCrawler`: 메인 크롤링 클래스
- `setup_driver()`: 셀레니움 드라이버 설정 (자동화 탐지 방지, 이미지/JS 활성화)
- `natural_typing()`: 자연스러운 타이핑 시뮬레이션
- `human_like_mouse_move()`: 자연스러운 마우스 움직임
- `wait_for_page_load()`: 페이지 로딩 완료 대기 (JavaScript 및 이미지 포함)
- `check_content_before_login()`: 로그인 전 콘텐츠 확인
- `login_naver()`: 네이버 로그인 수행 (자연스러운 입력 방식)
- `check_login_success()`: 로그인 성공 여부 확인 (CAPTCHA 감지)
- `crawl_login_content()`: 로그인 후 콘텐츠 크롤링
- `crawl_naver_mail_titles()`: 메일 제목 크롤링 (보너스)
- `display_results()`: 결과 출력

## 기술 스택
- Python 3.x
- Selenium 4.15.2
- ChromeDriver (수동 관리)

## 문제 해결

### ChromeDriver 오류 해결
- **"올바른 Win32 응용 프로그램이 아닙니다" 오류**: Chrome 버전과 ChromeDriver 버전이 일치하지 않음
- **"chromedriver를 찾을 수 없습니다" 오류**: 드라이버 파일이 올바른 위치에 없음
- **해결 방법**: Chrome 버전을 확인하고 해당 버전의 ChromeDriver를 다시 다운로드
