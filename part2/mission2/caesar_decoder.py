def caesar_cipher_decode(target_text):
    decoded_list = []

    for shift in range(1, 26):
        result = ''
        for char in target_text:
            if 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += char
        decoded_list.append((shift, result))

    return decoded_list


def read_password_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print('[에러] password.txt 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'[에러] 파일을 읽는 중 문제가 발생했습니다: {e}')
    return None


def save_result(decoded_text):
    try:
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(decoded_text)
        print(f'[알림] result.txt에 저장되었습니다.')
    except Exception as e:
        print(f'[에러] 결과 저장 중 문제가 발생했습니다: {e}')


def contains_dictionary_word(text, dictionary):
    words = text.lower().split()
    return any(word in dictionary for word in words)


def main():
    dictionary = {'love', 'mars', 'emergency', 'key', 'base', 'mission'}  # 필요한 키워드 추가 가능
    encrypted = read_password_file('password.txt')
    if not encrypted:
        return

    decoded_list = caesar_cipher_decode(encrypted)

    print('\n[카이사르 복호화 결과]')
    selected_auto = None
    for shift, decoded in decoded_list:
        marker = ''
        if contains_dictionary_word(decoded, dictionary) and selected_auto is None:
            marker = ' ← 사전 단어 포함!'
            selected_auto = (shift, decoded)
        print(f'{shift:2}번 이동: {decoded}{marker}')

    if selected_auto:
        shift, result = selected_auto
        print(f'\n[자동 탐지] {shift}번 이동된 "{result}" 문장이 사전 단어를 포함하고 있어 result.txt에 저장합니다.')
        save_result(result)
    else:
        try:
            selected = int(input('\n자동 해석이 실패했습니다. 사람이 보기엔 몇 번 이동된 결과가 올바른가요? (1~25): '))
            if 1 <= selected <= 25:
                final_result = decoded_list[selected - 1][1]
                save_result(final_result)
            else:
                print('[경고] 유효하지 않은 번호입니다.')
        except ValueError:
            print('[경고] 숫자만 입력해주세요.')


if __name__ == '__main__':
    main()
