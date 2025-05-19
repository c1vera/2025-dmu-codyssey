# door_hacking.py
import zipfile
import string
import time
import itertools
import threading
import os
import zlib

# 설정
ZIP_FILE_NAME = 'emergency_storage_key.zip'
PASSWORD_FILE_NAME = 'password.txt'
PASSWORD_LENGTH = 6
NUM_THREADS = 8
CHARSET = string.digits + string.ascii_lowercase  # 숫자 + 소문자

# 상태 공유
found_flag = False
lock = threading.Lock()


def try_passwords(start_chars):
    global found_flag
    trial_count = 0
    start_time = time.time()

    try:
        with zipfile.ZipFile(ZIP_FILE_NAME) as zf:
            for first in start_chars:
                if found_flag:
                    return

                for combo in itertools.product(CHARSET, repeat=PASSWORD_LENGTH - 1):
                    if found_flag:
                        return

                    password = first + ''.join(combo)
                    trial_count += 1
                                            
                    try:
                        zf.extractall(pwd=password.encode('utf-8'))
                        # 비밀번호가 맞았지만 압축 에러가 나면 여기서 zlib.error 발생
                        with lock:
                            if not found_flag:
                                found_flag = True
                                elapsed = time.time() - start_time
                                print(f'\n✅ 성공! 비밀번호: {password}')
                                print(f'🔁 시도 횟수 (스레드 {threading.current_thread().name}): {trial_count}')
                                print(f'⏱️ 소요 시간: {elapsed:.2f}초')
                                with open(PASSWORD_FILE_NAME, 'w') as f:
                                    f.write(password)
                        return
                    except (RuntimeError, zipfile.BadZipFile, zlib.error):
                        if trial_count % 50000 == 0:
                            elapsed = time.time() - start_time
                            print(f'[스레드 {threading.current_thread().name}] {trial_count}회 시도 중... 경과: {elapsed:.1f}s')
                        continue
                    except Exception as e:
                        print(f'[치명적 에러] 스레드 {threading.current_thread().name}: {e}')
                        return
                    except RuntimeError:
                        if trial_count % 50000 == 0:
                            elapsed = time.time() - start_time
                            print(f'[스레드 {threading.current_thread().name}] {trial_count}회 시도 중... 경과: {elapsed:.1f}s')
                        continue
                    except Exception as e:
                        print(f'[에러] 스레드 {threading.current_thread().name}: {e}')
                        return
    except zipfile.BadZipFile:
        print('에러: 손상된 ZIP 파일입니다.')
    except FileNotFoundError:
        print(f'에러: {ZIP_FILE_NAME} 파일을 찾을 수 없습니다.')


def unlock_zip():
    print('🔐 멀티스레드 비밀번호 해제 시작')
    print('⌛ 시작 시간:', time.strftime('%Y-%m-%d %H:%M:%S'))

    # 첫 자리 기준으로 스레드 나눔
    chunk_size = len(CHARSET) // NUM_THREADS
    threads = []

    for i in range(NUM_THREADS):
        start = i * chunk_size
        end = None if i == NUM_THREADS - 1 else (i + 1) * chunk_size
        chunk = CHARSET[start:end]
        t = threading.Thread(target=try_passwords, args=(chunk,), name=f'T{i+1}')
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not found_flag:
        print('❌ 모든 시도에도 비밀번호를 찾지 못했습니다.')


if __name__ == '__main__':
    unlock_zip()
