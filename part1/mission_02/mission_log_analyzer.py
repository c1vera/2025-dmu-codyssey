import json

def read_log_file(filename):
    """로그 파일을 읽어 리스트로 반환합니다.
    
    Args:
        filename (str): 읽을 파일 경로

    Returns:
        list: [["timestamp", "event", "message"], ...] 형태의 리스트
    """
    logs = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            next(file)  # 헤더 무시
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    logs.append(parts)
    except FileNotFoundError:
        print('[오류] 파일이 존재하지 않습니다.')
    except Exception as e:
        print('[오류] 파일 읽기 중 예외 발생:', e)
    return logs


def sort_logs_desc(logs):
    """로그 리스트를 시간 기준으로 역순 정렬합니다."""
    return sorted(logs, key=lambda x: x[0], reverse=True)


def logs_to_dict(logs):
    """로그 리스트를 딕셔너리로 변환합니다."""
    return {
        str(i): {
            'timestamp': log[0],
            'event': log[1],
            'message': log[2]
        }
        for i, log in enumerate(logs)
    }


def save_json(data, filename):
    """딕셔너리를 JSON 파일로 저장합니다."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print('[오류] JSON 저장 실패:', e)


def search_keyword(logs, keyword):
    """키워드를 포함한 로그 메시지를 출력합니다."""
    print(f'\n🔍 "{keyword}" 포함 로그:')
    found = False
    for log in logs:
        if keyword.lower() in log[2].lower():
            print(f'{log[0]} - {log[2]}')
            found = True
    if not found:
        print('→ 해당 키워드를 포함한 로그가 없습니다.')


def main():
    log_file = 'mission_computer_main.log'
    json_file = 'mission_computer_main.json'

    logs = read_log_file(log_file)
    if not logs:
        return

    print('\n[1] 읽은 로그:')
    for log in logs:
        print(log)

    logs = sort_logs_desc(logs)

    print('\n[2] 정렬된 로그:')
    for log in logs:
        print(log)

    log_dict = logs_to_dict(logs)

    save_json(log_dict, json_file)
    print(f'\n[3] JSON 파일로 저장 완료 → {json_file}')

    keyword = input('\n[4] 검색할 키워드를 입력하세요: ')
    search_keyword(logs, keyword)


if __name__ == '__main__':
    main()
