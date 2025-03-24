CSV_INPUT_PATH = 'C:/Users/yahwa/Desktop/project/2025-dmu-codyssey/part1/mission2/Mars_Base_Inventory_List.csv'
CSV_OUTPUT_PATH = 'C:/Users/yahwa/Desktop/project/2025-dmu-codyssey/part1/mission2/Mars_Base_Inventory_danger.csv'
BIN_OUTPUT_PATH = 'C:/Users/yahwa/Desktop/project/2025-dmu-codyssey/part1/mission2/Mars_Base_Inventory_List.bin'

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_csv_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다:', filename)
        return []
    except Exception as e:
        print('파일 읽기 중 오류 발생:', e)
        return []

def parse_inventory(csv_lines):
    header = csv_lines[0].split(',')
    inventory = []
    for line in csv_lines[1:]:
        parts = line.split(',')
        try:
            flammability = float(parts[4])
        except ValueError:
            continue  # 인화성이 숫자가 아니면 제외
        inventory.append({
            'Substance': parts[0],
            'Weight': parts[1],
            'Specific Gravity': parts[2],
            'Strength': parts[3],
            'Flammability': flammability
        })
    return inventory

def save_csv_file(filename, inventory):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('Substance,Weight,Specific Gravity,Strength,Flammability\n')
            for item in inventory:
                file.write('{},{},{},{},{}\n'.format(
                    item['Substance'], item['Weight'], item['Specific Gravity'],
                    item['Strength'], item['Flammability']))
    except Exception as e:
        print('CSV 저장 중 오류 발생:', e)

def save_binary_file(filename, inventory):
    try:
        with open(filename, 'wb') as file:
            for item in inventory:
                line = '{},{},{},{},{}\n'.format(
                    item['Substance'], item['Weight'], item['Specific Gravity'],
                    item['Strength'], item['Flammability'])
                file.write(line.encode('utf-8'))
    except Exception as e:
        print('이진 파일 저장 중 오류:', e)

def load_binary_file(filename):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            print('=== 이진 파일 내용 ===')
            print(content.decode('utf-8'))
    except Exception as e:
        print('이진 파일 읽기 중 오류:', e)

def main():
    lines = read_csv_file(CSV_INPUT_PATH)
    if not lines:
        return

    inventory = parse_inventory(lines)
    inventory.sort(key=lambda x: x['Flammability'], reverse=True)

    print('=== 전체 정렬 목록 ===')
    for item in inventory:
        print(item)

    danger_items = [item for item in inventory if item['Flammability'] >= 0.7]

    print('\n=== 인화성 0.7 이상 위험 물질 목록 ===')
    for item in danger_items:
        print(item)

    save_csv_file(CSV_OUTPUT_PATH, danger_items)

    save_binary_file(BIN_OUTPUT_PATH, inventory)
    load_binary_file(BIN_OUTPUT_PATH)


if __name__ == '__main__':
    main()
