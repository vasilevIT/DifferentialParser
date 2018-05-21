"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 20:18

"""
import re


class ParserBase:
    Program = 'Program:'
    Equations = 'Equations:'
    BeginConditions = 'BeginConditions:'
    IntegrationConfitions = 'IntegrationConditions:'
    IntegrationMethod = 'method'
    IntegrationVar = 't'
    IntegrationVarStep = 'd' + IntegrationVar
    SYMBOL_DIFF = IntegrationVarStep

    def __init__(self) -> None:
        super().__init__()
        self.text = ''
        self.current_index = 0
        self.not_init_vars = list()

    def init(self):
        """
        Инициализация
        :return:
        """
        self.current_index = 0
        # self.text = re.sub(r'[\n\r]', ' ', self.text)

    def error(self, param):
        """
        Генерация текста ошибки
        :param param:
        :return:
        """
        txt = param + " Символ #" + str(self.current_index)
        raise Exception(txt)

    def passSpace(self, only_spaces = False):
        """
        Пропускает пустые символы
        :param only_spaces: Пропускать только пробелы (без переносов строки)
        :return:
        """
        while self.current_index < len(self.text):
            if (self.text[self.current_index] == ' ') or (not only_spaces and ((self.text[self.current_index] == '\r') or (self.text[self.current_index] == '\n'))):
                self.current_index += 1
                continue
            else:
                break

    def isNextWord(self, word, force=True):
        """
        Ищет слово с пропуском пустых символов
        :param word: Слово, которое мы ищем
        :param force: Генерировать ли текст ошибки
        :return:
        """
        self.passSpace()
        return self._isNextWord(word, force)

    def isNextWordWithoutLineBreak(self, word, force=True):
        """
        Ищет слово с пропуском только пробелов (поиск происходит только в пределах одной строки)
        :param word: Слово, которое мы ищем
        :param force: Генерировать ли текст ошибки
        :return:
        """
        self.passSpace(True)
        return self._isNextWord(word, force)

    def _isNextWord(self,word, force):
        """
        Если word является следующим словом в строке, то возвращает True, иначе генерирует ошибку
        :param word: Слово, которое мы ищем
        :param force: Генерировать ли текст ошибки
        :return:
        """
        find_word = self.text[self.current_index:self.current_index + len(word)]
        if find_word != word:
            if force:
                self.error("Ошибка. Ожидалось слово `" + word + "`, а у вас написано `" +
                           find_word +
                           "`")
            return False
        self.current_index += len(word)
        return True

    def space(self):
        if self.isSpace():
            self.current_index += 1
            return True

        self.error("Нужен пробел.")
        raise Exception(self.error)

    def isSpace(self):
        """
        Определяет, что текущий симвл пробел
        :return:
        """
        if self.text[self.current_index] == ' ':
            return True
        return False

    def programName(self):
        """
        Считывает название программы
        :return:
        """
        self.passSpace()
        i = 0
        while self.current_index < len(self.text):
            if not self.readSymbol():
                break
            i += 1
        if i == 0:
            self.error("Ошибка. Ожидалось название программы.")
            raise Exception(self.error)
        return True

    def var(self):
        """
        Считываем переменную
        :return:
        """
        var_name = ""
        self.passSpace(True)
        i = 0
        while self.current_index < len(self.text):
            if not self.readVarSymbol():
                break
            var_name += self.text[self.current_index - 1: self.current_index]
            i += 1
        if i < 1:
            self.error("Ошибка (var). Ожидалась переменная. Длина переменной 3+ символа. Получено: "
                       + self.text[self.current_index - 5: self.current_index]
                       + " длина " + str(i)
                       )
        return var_name

    def integrationVariable(self):
        var_name = self.var()
        self.add_not_init_var(var_name)
        self.isNextWord("/")
        self.isNextWord(self.IntegrationVarStep)
        return var_name + "/" + self.IntegrationVarStep

    def readSymbol(self):
        """
        Читает символ
        :return:boolean
        """
        if self.isDigital() or self.isChar() or re.match('[\_\.]+', self.text[self.current_index]):
            self.current_index += 1
            return True
        return False

    def readVarSymbol(self):
        """
        Читает символ из переменной
        :return:boolean
        """
        if self.isDigital() or self.isChar() or re.match('[\_]+', self.text[self.current_index]):
            self.current_index += 1
            return True
        return False

    def isDigital(self):
        """
        Проверяет, является ли текущий символ цифрой
        :return:boolean
        """
        if re.match('[0-9]+', self.text[self.current_index]) is not None:
            return True
        return False

    def isChar(self):
        """
        Проверяет, является ли текущий символ буквой
        :return:boolean
        """
        if re.match('[a-zA-Z]+', self.text[self.current_index]) is not None:
            return True
        return False

    def Number(self):
        """
        Считывает число (целое или дробное)
        :return:
        """
        # self.passSpace()
        number = self.IntNumber()
        if self.isNextWordWithoutLineBreak(".", False):
            number += "."
            number += self.IntNumber()
        if len(number) < 1:
            raise Exception("Ожидалось число")
        return number

    def IntNumber(self):
        """
        Считывает целое число
        :return:
        """
        self.passSpace(True)
        number = ""
        while True:
            if self.isDigital():
                number += self.text[self.current_index:self.current_index + 1]
                self.current_index += 1
            else:
                break
        return number

    def goToStartWord(self):
        """
        Возвращает указать в начало текущего слова
        :return:
        """
        while not self.isSpace():
            self.current_index -= 1

    def isEOL(self):
        """
        Определяет, что достигнут конец строки
        :return:
        """
        self.passSpace(True)
        if (self.text[self.current_index] == ";") or (self.text[self.current_index] == "\r") or (self.text[self.current_index] == "\n"):
            return True
        return False


    def add_not_init_var(self, var):
        """
        Добавляет переменную в список не инициализированных переменных
        :param var:
        :return:
        """
        if not (var in self.not_init_vars):
            self.not_init_vars.append(var)

    def free_not_init_var(self,var):
        """
        Удаляет переменную из списка после ее инициализации
        :param var:
        :return:
        """
        if var in self.not_init_vars:
            self.not_init_vars.remove(var)
