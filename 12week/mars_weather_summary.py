import csv
import mysql.connector

def read_csv_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 건너뛰기
        return [row for row in reader]

def insert_weather_data(cursor, data):
    for row in data:
        mars_date, temp, storm = row
        query = (
            "INSERT INTO mars_weather (mars_date, temp, storm) "
            f"VALUES ('{mars_date}', {int(temp)}, {int(storm)});"
        )
        cursor.execute(query)

def main():
    # MySQL 연결
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='비밀번호',
        database='codyssey'
    )
    cursor = conn.cursor()

    # CSV 데이터 로드
    data = read_csv_data('mars_weathers_data.csv')

    # 테이블 생성 (존재하지 않을 경우)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mars_weather (
            weather_id INT AUTO_INCREMENT PRIMARY KEY,
            mars_date DATETIME NOT NULL,
            temp INT,
            storm INT
        );
    """)

    # INSERT 실행
    insert_weather_data(cursor, data)

    # 커밋 및 종료
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
