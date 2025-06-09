import os
import wave
import datetime
import threading
import pyaudio
import csv
import speech_recognition as sr


def ensure_records_folder_exists():
    records_dir = os.path.join(os.getcwd(), 'records')
    if not os.path.isdir(records_dir):
        os.makedirs(records_dir)
    return records_dir


def get_timestamped_filename():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return filename


def record_audio(stop_event, output_path, channels=1, rate=44100, chunk=1024):
    audio_interface = pyaudio.PyAudio()

    try:
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

    def wait_for_enter():
        input()
        stop_event.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()

    while not stop_event.is_set():
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print('스트림에서 데이터를 읽는 중 오류:', str(e))
            break

    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    try:
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio_interface.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        print(f'녹음이 완료되었습니다: {output_path}')
    except Exception as e:
        print('파일 저장 중 오류가 발생했습니다:', str(e))


def perform_stt_and_save_csv(wav_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ko-KR')
            print('📝 인식된 텍스트:', text)
            csv_path = wav_path.replace('.wav', '.csv')
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['time', 'text'])
                writer.writerow(['0.0', text])
            print(f'📄 CSV 파일로 저장되었습니다: {csv_path}')
    except sr.UnknownValueError:
        print('⚠️ 음성을 인식하지 못했습니다.')
    except sr.RequestError as e:
        print(f'❌ STT 서비스 요청 실패: {e}')


def list_recorded_files(start_date=None, end_date=None):
    records_dir = ensure_records_folder_exists()
    all_files = [f for f in os.listdir(records_dir) if f.lower().endswith('.wav')]

    if not start_date and not end_date:
        return sorted(all_files)

    filtered = []
    for fname in all_files:
        try:
            date_str = fname.split('-')[0]
            file_date = int(date_str)
        except ValueError:
            continue

        sd = int(start_date) if start_date else None
        ed = int(end_date) if end_date else None

        if ((sd is None or file_date >= sd) and
                (ed is None or file_date <= ed)):
            filtered.append(fname)

    return sorted(filtered)


def search_csv_keyword(records_dir, keyword):
    print(f'\n🔍 "{keyword}" 키워드 검색 결과:')
    for fname in os.listdir(records_dir):
        if fname.endswith('.csv'):
            path = os.path.join(records_dir, fname)
            with open(path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if keyword in row['text']:
                        print(f'[{fname}] {row["time"]}초 - {row["text"]}')


def main():
    records_dir = ensure_records_folder_exists()
    filename = get_timestamped_filename()
    wav_path = os.path.join(records_dir, filename)

    stop_event = threading.Event()
    record_audio(stop_event, wav_path)

    # STT 수행 후 CSV 저장
    perform_stt_and_save_csv(wav_path)

    # 보너스: 키워드로 텍스트 검색
    keyword = input('\n검색할 키워드를 입력하세요 (스킵하려면 엔터): ').strip()
    if keyword:
        search_csv_keyword(records_dir, keyword)


if __name__ == '__main__':
    main()
