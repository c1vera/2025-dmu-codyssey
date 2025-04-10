import time
import platform
import os
import psutil
from dummy_sensor import DummySensor
from cross_platform_key_listener import is_q_pressed

ds = DummySensor()


class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.sensor = ds
        # 처음에 센서 데이터 키를 기준으로 빈 리스트를 가진 딕셔너리 생성
        self.history = {key: [] for key in self.sensor.get_env()}
        self.settings = self.load_settings()

    def load_settings(self):
        settings = []
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    key = line.strip()
                    if key:
                        settings.append(key)
        except FileNotFoundError:
            print('설정 파일(setting.txt)이 없어 전체 항목을 출력합니다.')
        return settings

    def format_json_like(self, data):
        print('{')
        keys = list(data.keys())
        for i, key in enumerate(keys):
            value = data[key]
            if isinstance(value, str):
                value = f"'{value}'"
            comma = ',' if i < len(keys) - 1 else ''
            print(f"  '{key}': {value}{comma}")
        print('}')

    def get_mission_computer_info(self):
        try:
            info = {
                'os_name': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_core_count': os.cpu_count(),
                'memory_total': round(psutil.virtual_memory().total / (1024 ** 3), 2)  # GB
            }

            filtered_info = {
                key: info[key] for key in self.settings if key in info
            } if self.settings else info

            print('\n=== 시스템 정보 ===')
            self.format_json_like(filtered_info)
            print()
        except Exception as e:
            print(f'시스템 정보 수집 중 오류 발생: {e}')

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }

            filtered_load = {
                key: load[key] for key in self.settings if key in load
            } if self.settings else load

            print('\n=== 시스템 부하 정보 ===')
            self.format_json_like(filtered_load)
            print()
        except Exception as e:
            print(f'시스템 부하 수집 중 오류 발생: {e}')

    def get_sensor_data(self):
        start_time = time.time()
        print("센서 데이터 수집 시작 (q 키를 누르면 종료)\n")

        while True:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()

            # 각 키에 대해 값을 나눠서 저장함 (평균 계산 쉽게 하려고 이렇게 함)
            for key in self.env_values:
                self.history[key].append(self.env_values[key])

            self.format_json_like(self.env_values)

            if time.time() - start_time >= 30:  # 테스트용: 30초
                self.print_5min_average()
                # 평균 출력 후 기록 초기화
                self.history = {key: [] for key in self.env_values}
                start_time = time.time()

            print("키보드의 'q' 키를 누르면 종료됩니다.")

            for _ in range(50):  # 5초 동안 0.1초 간격
                if is_q_pressed():
                    print("\nSystem stopped…")
                    return
                time.sleep(0.1)

    def print_5min_average(self):
        print('\n=== 5분 평균 환경 정보 ===')
        for key, values in self.history.items():
            if values:
                avg = round(sum(values) / len(values), 2)
                # 평균은 소수점 둘째 자리까지 반올림
                print(f'{key}: {avg}')
        print('==========================\n')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_mission_computer_info()
    RunComputer.get_mission_computer_load()
    RunComputer.get_sensor_data()
