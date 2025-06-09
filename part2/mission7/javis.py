#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import wave
import datetime
import threading
import pyaudio


def ensure_records_folder_exists():
    """
    records 폴더가 현재 스크립트가 실행되는 경로에 존재하는지 확인하고,
    없으면 새로 생성해 줍니다.
    """
    records_dir = os.path.join(os.getcwd(), 'records')
    if not os.path.isdir(records_dir):
        os.makedirs(records_dir)
    return records_dir


def get_timestamped_filename():
    """
    현재 날짜와 시간을 기준으로 '년월일-시분초.wav' 형식의 파일명을 만들어 반환합니다.
    예) 20250602-091530.wav
    """
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return filename


def record_audio(stop_event, output_path, channels=1, rate=44100, chunk=1024):
    """
    마이크로부터 음성을 녹음해서 WAV 파일로 저장하는 함수입니다.
    stop_event가 set될 때까지 계속 녹음하며, 녹음된 데이터를 output_path에 쓰고 종료합니다.
    """
    # PyAudio 인스턴스 생성
    audio_interface = pyaudio.PyAudio()

    try:
        # 입력 스트림 열기
        stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )
    except Exception as e:
        print('마이크를 여는 중에 오류가 발생했습니다:', str(e))
        audio_interface.terminate()
        return

    print('녹음을 시작합니다. 중지하려면 Enter 키를 누르세요.')

    frames = []

    # 백그라운드에서 키 입력을 감지해 녹음을 중지하기 위한 쓰레드
    def wait_for_enter():
        input()
        stop_event.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()

    # 녹음 루프: stop_event가 set될 때까지 계속 읽어들임
    while not stop_event.is_set():
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print('스트림에서 데이터를 읽는 중 오류:', str(e))
            break

    # 스트림과 PyAudio 객체 정리
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    # WAV 파일로 저장
    try:
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio_interface.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        print(f'녹음이 완료되었습니다: {output_path}')
    except Exception as e:
        print('파일 저장 중 오류가 발생했습니다:', str(e))


def list_recorded_files(start_date=None, end_date=None):
    """
    bonus 과제로 구현한 기능:
    records 폴더 내에 있는 WAV 파일을 확인해서, 
    (선택적으로) 특정 날짜 범위(start_date ~ end_date)에 속하는 리스트를 반환합니다.

    - start_date, end_date 모두 None일 경우, 전체 파일 목록 반환
    - start_date, end_date 문자열은 'YYYYMMDD' 형식이어야 합니다.
    """
    records_dir = ensure_records_folder_exists()
    all_files = [f for f in os.listdir(records_dir) if f.lower().endswith('.wav')]

    # 날짜 필터가 없으면 전체 반환
    if not start_date and not end_date:
        return sorted(all_files)

    filtered = []
    for fname in all_files:
        # 파일명에서 날짜 부분 추출 (예: '20250602-091530.wav' -> '20250602')
        try:
            date_str = fname.split('-')[0]
            # 날짜 범위를 숫자로 비교할 수 있도록 변환
            file_date = int(date_str)
        except ValueError:
            continue

        if start_date:
            try:
                sd = int(start_date)
            except ValueError:
                sd = None
        else:
            sd = None

        if end_date:
            try:
                ed = int(end_date)
            except ValueError:
                ed = None
        else:
            ed = None

        # start_date, end_date 조건에 맞게 필터링
        if ((sd is None or file_date >= sd) and
                (ed is None or file_date <= ed)):
            filtered.append(fname)

    return sorted(filtered)


def main():
    """
    프로그램 진입점(main 함수).
    1) records 폴더를 준비하고,
    2) 파일명을 생성한 뒤,
    3) 음성 녹음(record_audio) 기능을 호출합니다.
    """
    records_dir = ensure_records_folder_exists()
    filename = get_timestamped_filename()
    output_path = os.path.join(records_dir, filename)

    stop_event = threading.Event()
    record_audio(stop_event, output_path)

    # bonus: 녹음된 파일 목록을 보여주고 싶다면 아래 주석을 해제해서 사용
    # print('\n=== 녹음 파일 목록 ===')
    # for f in list_recorded_files():
    #     print(f)


if __name__ == '__main__':
    main()
