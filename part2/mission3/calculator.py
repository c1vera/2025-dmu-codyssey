import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton,
    QLineEdit, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pink Blossom Calculator') 
        self.setFixedSize(500, 700)
        self.setStyleSheet('background-color: #fff6f7;')  # 전체 배경을 아주 연한 분홍으로 설정
        self.expression = ''  # 계산식 문자열 저장용
        self.load_font()      # 폰트 불러오기 시도
        self.init_ui()        # UI 구성 시작

    def load_font(self):
        # 프로젝트 내 폰트를 불러와서 적용 (없으면 기본 폰트로 대체)
        font_id = QFontDatabase.addApplicationFont('fonts/calc_font.ttf')
        if font_id == -1:
            print('폰트를 찾을수 없습니다. 기본 폰트를 사용합니다.')
            self.custom_font = QFont('Arial', 24)
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                self.custom_font = QFont(families[0], 24)
            else:
                print('폰트를 찾을수 없습니다. 기본 폰트를 사용합니다.')
                self.custom_font = QFont('Arial', 24)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)  # 디스플레이와 버튼 사이에 여백을 넉넉하게 줌

        # 결과 출력창 설정
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬 (계산기처럼)
        self.display.setReadOnly(True)            # 사용자 입력 막기 (버튼으로만 입력)
        self.display.setFont(QFont(self.custom_font.family(), 38))
        self.display.setStyleSheet(
            'padding: 30px; font-size: 38px; background-color: #ffdfe5; border: none; border-radius: 12px;'
        )
        main_layout.addWidget(self.display)

        # 버튼 그리드 레이아웃 설정
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        # 버튼 텍스트 배열 (아이폰 계산기와 동일한 배치)
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '0', '.', '=']  # 0은 두 칸 차지 (좌우로)
        ]

        # 버튼을 순회하면서 UI에 하나씩 배치
        for row, row_data in enumerate(buttons):
            for col, btn_text in enumerate(row_data):
                if row == 4 and col == 1:
                    continue  # 0을 두 칸 차지하도록 만들기 위해 두 번째 0은 생략

                button = QPushButton(btn_text)
                button.setFont(self.custom_font)
                button.setFixedSize(100, 100)
                button.setStyleSheet(self.get_button_style(btn_text))
                button.clicked.connect(self.button_clicked)  # 버튼 클릭 시 이벤트 연결

                if row == 4 and col == 0:
                    grid.addWidget(button, row, col, 1, 2)  # 0 버튼은 2칸 너비로 설정
                else:
                    grid.addWidget(button, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def get_button_style(self, text):
        # 버튼별 색상 테마를 구분해서 적용
        if text in {'+', '−', '×', '÷', '='}:
            return 'background-color: #f67d8d; color: white; border-radius: 20px;'  # 연산자
        elif text in {'C', '±', '%'}:
            return 'background-color: #f5b4bb; color: black; border-radius: 20px;'  # 기능키
        else:
            return 'background-color: #ffdfe5; color: black; border-radius: 20px;'  # 숫자 등

    def button_clicked(self):
        # 버튼이 눌릴 때마다 처리하는 로직
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.expression = ''  # 전체 지우기
        elif text == '=':
            try:
                # 계산식을 실제 파이썬 식으로 변환 후 계산
                expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                result = str(eval(expr))  # 안전한 계산을 위해선 eval 대신 수식 파서 권장
                self.expression = result
            except Exception:
                self.expression = 'Error'  # 오류 발생 시 에러 메시지 출력
        elif text == '±':
            # 부호 변경 처리 (문자열 앞에 - 붙이거나 떼기)
            try:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
            except Exception:
                pass
        else:
            self.expression += text  # 일반 숫자나 기호는 이어 붙임

        self.display.setText(self.expression)  # 현재 계산식 화면에 출력

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
