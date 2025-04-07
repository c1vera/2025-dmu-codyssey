import time
from dummy_sensor import DummySensor
from cross_platform_key_listener import is_q_pressed  # 핵심 추가

ds = DummySensor()


class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.sensor = ds
        self.history = []

    def get_sensor_data(self):
        start_time = time.time()
        print("센서 데이터 수집 시작 (q 키를 누르면 종료)\n")

        while True:
            # 센서 데이터 수집
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            self.history.append(self.env_values.copy())

            print('{')
            for key, value in self.env_values.items():
                print(f"  '{key}': {value},")
            print('}')

            # 5분 평균 출력
            if time.time() - start_time >= 30:
                self.print_5min_average()
                self.history.clear()
                start_time = time.time()

            print("키보드의 'q' 키를 누르면 종료됩니다.")
            
            # 5초 동안 0.1초 단위로 q 키 감지
            for _ in range(50):
                if is_q_pressed():
                    print("\nSystem stopped…")
                    return
                time.sleep(0.1)

    def print_5min_average(self):
        if not self.history:
            print('No data to calculate average.')
            return
# 5분 평균을 내야하지만.. 테스트 용으로 30초마다 평균을 내도록 수정
        print('\n=== 5분 평균 환경 정보 ===')
        for key in self.history[0]:
            total = sum(entry[key] for entry in self.history)
            avg = round(total / len(self.history), 2)
            print(f'{key}: {avg}')
        print('==========================\n')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
