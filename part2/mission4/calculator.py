import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton,
    QLineEdit, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase


# 계산 로직을 담당하는 별도 클래스
class CalculatorLogic:
    def __init__(self):
        self.expression = ''

    def input(self, value):
        self.expression += value

    def reset(self):
        self.expression = ''

    def negative_positive(self):
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression

    def percent(self):
        try:
            value = eval(self.expression)
            self.expression = str(value / 100)
        except:
            self.expression = 'Error'

    def equal(self):
        try:
            result = eval(self.expression.replace('×', '*').replace('÷', '/').replace('−', '-'))
            result = round(result, 6)  # 보너스: 소수점 6자리 반올림
            self.expression = str(result)
        except ZeroDivisionError:
            self.expression = '0으로 나눌 수 없음'
        except OverflowError:
            self.expression = '숫자 범위 초과'
        except:
            self.expression = 'Error'
        return self.expression


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pink Blossom Calculator')
        self.setFixedSize(500, 700)
        self.setStyleSheet('background-color: #fff3f4;')
        self.logic = CalculatorLogic()
        self.load_font()
        self.init_ui()

    def load_font(self):
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
        main_layout.setSpacing(25)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont(self.custom_font.family(), 38))
        self.display.setStyleSheet(
            'padding: 30px; font-size: 38px; background-color: #ffdfe5; border: none; border-radius: 12px;'
        )
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '0', '.', '=']
        ]

        self.dot_entered = False

        for row, row_data in enumerate(buttons):
            for col, btn_text in enumerate(row_data):
                if row == 4 and col == 1:
                    continue

                button = QPushButton(btn_text)
                button.setFont(self.custom_font)
                button.setFixedSize(100, 100)
                button.setStyleSheet(self.get_button_style(btn_text))
                button.clicked.connect(self.button_clicked)

                if row == 4 and col == 0:
                    grid.addWidget(button, row, col, 1, 2)
                else:
                    grid.addWidget(button, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def get_button_style(self, text):
        if text in {'+', '−', '×', '÷', '='}:
            return 'background-color: #f67d8d; color: white; border-radius: 20px;'
        elif text in {'C', '±', '%'}:
            return 'background-color: #f5b4bb; color: black; border-radius: 20px;'
        else:
            return 'background-color: #ffdfe5; color: black; border-radius: 20px;'

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.logic.reset()
            self.dot_entered = False
        elif text == '=':
            result = self.logic.equal()
            self.adjust_font_size(result)
        elif text == '±':
            self.logic.negative_positive()
        elif text == '%':
            self.logic.percent()
        elif text == '.':
            if '.' not in self.logic.expression.split()[-1]:
                self.logic.input(text)
        else:
            self.logic.input(text)

        self.display.setText(self.logic.expression)

    def adjust_font_size(self, text):
        length = len(text)
        if length <= 8:
            size = 38
        elif length <= 12:
            size = 30
        else:
            size = 24
        self.display.setFont(QFont(self.custom_font.family(), size))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
    