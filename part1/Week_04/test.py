from cross_platform_key_listener import is_q_pressed
import time

print("출력 중입니다. 'q' 키를 누르면 종료됩니다.")

while True:
    # (여기에 센서 출력이든 뭐든 넣어도 됨)
    print("센서 작동 중...")
    
    for _ in range(50):  # 약 5초 동안 키 감지
        if is_q_pressed():
            print("\nSystem stopped…")
            exit()
        time.sleep(0.1)
