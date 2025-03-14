# main.py

import os

def check_python():
    # 파이썬이 정상적으로 실행되는지 확인하는 코드
    print('Hello Mars~')

def get_log_filepath():
    # 현재 main.py가 위치한 디렉토리를 기준으로 로그 파일 경로를 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'mission_computer_main.log')

def get_report_filepath():
    # 분석 결과 파일을 main.py가 있는 폴더에 저장하도록 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'log_analysis.md')

def read_log_file(filename):
    # 로그 파일을 읽어오는 함수
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"오류: 파일 '{filename}'을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

def write_analysis_report(filename, content):
    # 분석 결과를 Markdown 파일로 저장하는 함수
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"보고서 저장 중 오류 발생: {e}")

def analyze_logs(lines):
    # 로그 파일에서 'ERROR' 또는 'explosion'이 포함된 중요한 로그만 추출하는 함수
    error_logs = [line for line in lines if 'ERROR' in line or 'explosion' in line.lower()]
    return error_logs

def main():
    check_python()
    
    log_filepath = get_log_filepath()  # 올바른 로그 파일 경로 가져오기
    report_filepath = get_report_filepath()  # 올바른 보고서 파일 경로 가져오기
    
    logs = read_log_file(log_filepath)
    if not logs:
        return  # 로그 파일이 없으면 프로그램 종료
    
    print("--- 로그 내용 (시간의 역순, 최신 순서) ---")
    for log in logs[::-1]:  # 최신 로그가 먼저 출력되도록 역순 정렬
        print(log.strip())
    
    error_logs = analyze_logs(logs)
    if error_logs:
        print("\n--- 주요 오류 로그 ---")
        for error in error_logs:
            print(error.strip())
        
        write_analysis_report(report_filepath, "\n".join(error_logs))
        print(f"분석 보고서가 [{report_filepath}]에 저장되었습니다.")
    else:
        print("로그에서 중요한 오류를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
