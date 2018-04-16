"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:04

"""
import re


class Parser:
    Program = 'Program:'
    Equations = 'Equations:'
    BeginConditions = 'BeginConditions:'
    IntegrationConfitions = 'BeginConditions:'
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

    def isNextWord(self, word):
        self.passSpace()
        if self.text[self.current_index:self.current_index + len(word)] != word:
            self.error("Ошибка. Ожидалось слово `" + word + "`, а у вас написано `" +
                       self.text[self.current_index:self.current_index + len(word)] +
                       "`")
            raise Exception(self.error())
        self.current_index += len(self.Program)
        return True

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
            self.begin_conditions()
            self.integration_conditions()
        except Exception as e:
            print(e.args[0])

    def program(self):
        """
        Блок с названием программы
        :return:
        """
        self.passSpace()
        self.isNextWord(self.Program)
        self.space()
        self.var()

    def equations(self):
        """
        Блок с уравнениями
        :return:
        """

        self.passSpace()
        self.isNextWord(self.Equations)
        while (self.current_index < len(self.text) - len(self.IntegrationConfitions)) and (
                    self.text[self.current_index:self.current_index + len(self.IntegrationConfitions)]
                    != self.IntegrationConfitions):
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
        if re.match('[\w\d\_\.]+', self.text[self.current_index]) != None:
            self.current_index += 1
            return True
        return False

    def begin_conditions(self):
        pass

    def integration_conditions(self):
        pass

    def space(self):
        if self.text[self.current_index] == ' ':
            self.current_index += 1
            return True

        self.error("Нужен пробел.")
        raise Exception(self.error())

    def var(self):
        i = 0
        while self.current_index < len(self.text):
            if not self.readSymbol():
                break
            i += 1
        if i == 0:
            self.error("Ошибка. Ожидалось название программы.")
            raise Exception(self.error())
        return True
