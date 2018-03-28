"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:04

"""
import re


class Parser:
    PROGRAM = 'program:'
    METHOD = 'method:'
    EQUATION = 'equation:'
    LIMITATIONS = 'limitations:'
    BEGIN_CONDITION = 'begin condition:'
    SYMBOL_DIFF = 'dt'

    def __init__(self) -> None:
        super().__init__()
        self.text = ''
        self.current_index = 0

    def init(self):
        self.current_index = 0
        self.text = re.sub(r'[\n\r]', ' ', self.text)

    def error(self, param):
        txt = param + " Символ #" + str(self.current_index)
        raise Exception(txt)

    def passSpace(self):
        while self.current_index < len(self.text):
            if self.text[self.current_index] == ' ':
                self.current_index += 1
                continue
            else:
                break

    def parse(self, text):
        """
        Парсит входящую строку

        :param text:
        :return:
        """
        self.text = text
        self.init()
        try:
            self.program()
            self.equations()
            self.method()
            self.begin_condition()
        except Exception as e:
            print(e.args[0])

    def program(self):
        """
        Блок с названием программы
        :return:
        """
        self.passSpace()
        if self.text[self.current_index:self.current_index + len(self.PROGRAM)] != self.PROGRAM:
            self.error("Ошибка. Ожидалось слово `" + self.PROGRAM + "`, а у вас написано `" +
                       self.text[self.current_index:self.current_index + len(self.PROGRAM)] +
                       "`")
            return
        self.current_index += len(self.PROGRAM)

        if self.text[self.current_index] == ' ':
            self.current_index += 1
        else:
            self.error("Нужен пробел.")
            return

        i = 0
        while self.current_index < len(self.text):
            if not self.readSymbol():
                break
            i += 1
        if i == 0:
            self.error("Ошибка. Ожидалось название программы.")

    def equations(self):
        """
        Блок с уравнениями
        :return:
        """

        self.passSpace()
        if self.text[self.current_index:self.current_index + len(self.EQUATION)] != self.EQUATION:
            self.error("Ошибка. Ожидалось слово `" + self.EQUATION + "`, а у вас написано `" +
                       self.text[self.current_index:self.current_index + len(self.EQUATION)] +
                       "`")
            return
        self.current_index += len(self.EQUATION)
        while (self.current_index < len(self.text) - len(self.METHOD)) and (
                    self.text[self.current_index:self.current_index + len(self.METHOD)] != self.METHOD):
            self.equation()

    def equation(self):
        """
        Считываем отдельное уравнение
        :return:
        """
        self.passSpace()
        self.variable()
        self.passSpace()
        if self.text[self.current_index] == '=':
            self.current_index += 1
        else:
            self.error("Нужен знак `=`.")
            return
        self.right_part()

    def variable(self):
        """
        Считываем переменную
        :return:
        """
        i = 0
        while self.current_index < len(self.text):
            if not self.readSymbol():
                break
            i += 1
        if i < 3:
            self.error("Ошибка (variable). Ожидалась переменная. Длина переменной 3+ символа.")

    def right_part(self):
        pass

    def method(self):
        """
        Блок с описанием метода интегрирования
        :return:
        """
        self.passSpace()

    def begin_condition(self):
        """
        Блок с описанием начальных условий
        :return:
        """
        self.passSpace()

    def readSymbol(self):
        """

        :return:
        """
        if re.match('[\w\d]+', self.text[self.current_index]) != None:
            self.current_index += 1
            return True
        return False
