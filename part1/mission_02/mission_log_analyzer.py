# mission_log_analyzer.py

import json

def read_log_file(filename):
    """로그 파일을 읽어 리스트로 반환한다. 첫 줄은 헤더라 건너뛴다."""
    logs = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            next(file)  # 첫 줄 건너뜀
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    timestamp, event, message = parts
                    logs.append([timestamp, event, message])
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다.')
    except Exception as e:
        print('파일을 읽는 중 오류 발생:', e)
    return logs


def sort_logs_desc(logs):
    """로그를 시간 기준 역순으로 정렬한다."""
    return sorted(logs, key=lambda x: x[0], reverse=True)


def logs_to_dict(logs):
    """로그 리스트를 딕셔너리로 변환한다."""
    log_dict = {}
    for i, log in enumerate(logs):
        log_dict[str(i)] = {
            'timestamp': log[0],
            'event': log[1],
            'message': log[2]
        }
    return log_dict


def save_json(data, filename):
    """딕셔너리를 JSON 파일로 저장한다."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print('JSON 저장 중 오류:', e)


def search_keyword(logs, keyword):
    """로그 메시지에서 키워드를 포함하는 항목만 출력한다."""
    print(f'"{keyword}"가 포함된 로그:')
    found = False
    for log in logs:
        if keyword.lower() in log[2].lower():
            print(f'{log[0]} - {log[2]}')
            found = True
    if not found:
        print('해당 키워드를 포함한 로그가 없습니다.')


if __name__ == '__main__':
    log_file = 'mission_computer_main.log'
    json_file = 'mission_computer_main.json'
    
    logs = read_log_file(log_file)
    if not logs:
        exit()

    print('\n[1] 읽은 로그 리스트:')
    for log in logs:
        print(log)

    logs = sort_logs_desc(logs)

    print('\n[2] 시간 역순 정렬된 로그:')
    for log in logs:
        print(log)

    log_dict = logs_to_dict(logs)

    print('\n[3] 딕셔너리로 변환된 로그:')
    for k, v in log_dict.items():
        print(k, v)

    save_json(log_dict, json_file)
    print(f'\n[4] JSON 파일로 저장 완료 → {json_file}')

    print('\n[5] 보너스: 키워드 검색')
    keyword = input('검색할 키워드를 입력하세요: ')
    search_keyword(logs, keyword)
