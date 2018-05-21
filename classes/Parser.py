"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:04

"""
import sys, traceback

from classes.Integrator import Integrator
from classes.ParserBase import ParserBase


class Parser(ParserBase):
    def __init__(self) -> None:
        super().__init__()
        self.integrator = Integrator()

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
            print(self.not_init_vars)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise Exception(e.args[0], self.current_index, 2)

    def program(self):
        """
        Блок с названием программы
        :return:
        """
        self.passSpace()
        self.isNextWord(self.Program)
        self.space()
        self.programName()

    def equations(self):
        """
        Блок с уравнениями
        :return:
        """

        self.passSpace()
        self.isNextWord(self.Equations)
        while (self.current_index < len(self.text) - len(self.BeginConditions)) and (
                    self.text[self.current_index:self.current_index + len(self.BeginConditions)]
                    != self.BeginConditions):
            self.equation()
            self.passSpace()

    def equation(self):
        """
        Считываем отдельное уравнение
        :return:
        """
        self.passSpace()
        var = self.integrationVariable()
        self.isNextWordWithoutLineBreak("=")
        block = self.right_part()
        self.integrator.equations[var] = block
        self.isNextWordWithoutLineBreak(';')

    def right_part(self):
        """
        Правая часть уравнениея
        :return:string
        """
        self.passSpace(True)
        block = ""
        if self.isNextWordWithoutLineBreak("-", False):
            block += "-"
        while True:
            block += self.additionBlock()
            if self.isEOL():
                break
            if self.isNextWordWithoutLineBreak(")", False):
                self.current_index -= 1
                break
        return block

    def additionBlock(self):
        """
        Блок арифметического суммирования/вычитания
        :return:string
        """
        add_block = self.multiplicationBlock()
        while True:
            if self.isNextWordWithoutLineBreak("+", False):
                add_block += " + " + self.multiplicationBlock()
            elif self.isNextWordWithoutLineBreak("-", False):
                add_block += " - " + self.multiplicationBlock()
            else:
                break
        return add_block

    def multiplicationBlock(self):
        """
        Блок арифметического умножения/деления
        :return:string
        """
        block = self.degreeBlock()
        while True:
            if self.isNextWordWithoutLineBreak("*", False):
                block += " * " + self.degreeBlock()
            elif self.isNextWordWithoutLineBreak("/", False):
                block += " / " + self.degreeBlock()
            else:
                break

        return block

    def degreeBlock(self):
        """
        Блок арифметической степени
        :return:string
        """
        block = self.varBlock()
        while True:
            if self.isNextWordWithoutLineBreak("^", False):
                block += " ** " + self.varBlock()
            else:
                break

        return block

    def varBlock(self):
        """
        Блок с переменной или числом
        :return:string
        """
        block = ""
        if self.isNextWordWithoutLineBreak("(", False):
            block += "("
            block += str(self.right_part())
            if self.isNextWordWithoutLineBreak(")"):
                block += ")"
        elif self.isDigital():
            block += str(self.Number())
        else:
            var = str(self.var())
            self.add_not_init_var(var)
            block += var
        return block

    def method(self):
        """
        Блок с описанием метода интегрирования
        :return:
        """
        self.passSpace()

    def begin_conditions(self):
        """
        Блок с начальными условиями
        :return:
        """
        self.passSpace()
        self.isNextWord(self.BeginConditions)
        self.passSpace()
        while (self.current_index < len(self.text) - len(self.IntegrationConfitions)) and (
                    self.text[self.current_index:self.current_index + len(self.IntegrationConfitions)]
                    != self.IntegrationConfitions):
            self.begin_condition()
            if self.isEOL():
                self.current_index += 1
            self.passSpace()
        if len(self.not_init_vars) > 0:
            self.goToStartWord()
            self.error("Ошибка. Не проинициализированны следующие переменные: " + self.not_init_vars.__str__())

    def begin_condition(self):
        """
        Блок с описанием начальных условий
        :return:
        """
        var = self.var()
        self.free_not_init_var(var)
        self.isNextWord("=")
        value = self.Number()
        self.integrator.begin_conditions[var] = value
        self.isNextWordWithoutLineBreak(';')
        self.passSpace()

    def integration_conditions(self):
        """
        Условия интегрирования
        :return:
        """
        self.isNextWord(self.IntegrationConfitions)
        self.integration_method()
        self.integration_var()
        self.integration_var_step()

    def integration_method(self):
        """
        Метод интегрирования
        :return:
        """
        self.passSpace()
        self.isNextWord(self.IntegrationMethod)
        self.isNextWord("=")
        self.integration_method_name()
        self.isNextWordWithoutLineBreak(';')

    def integration_method_name(self):
        """
        Название метода интегрирования
        :return:
        """
        self.passSpace(True)
        for method in Integrator.integration_methods:
            if self.isNextWordWithoutLineBreak(method, False):
                self.integrator.integration_method = method
                return method
        raise Exception(
            "Неизвестный метод интегрирования. Укажите один из следующих:" + str(Integrator.integration_methods))

    def integration_var(self):
        """
        Переменная интегрирования
        :return:
        """
        self.isNextWord(self.IntegrationVar)
        self.isNextWordWithoutLineBreak("=")
        value = self.Number()
        self.integrator.integration_var_value = value
        self.isNextWordWithoutLineBreak(';')

    def integration_var_step(self):
        """
        Шаг интегрирования
        :return:
        """
        self.isNextWord(self.IntegrationVarStep)
        self.isNextWordWithoutLineBreak("=")
        value = self.Number()
        self.integrator.integration_var_step_value = value
        self.isNextWordWithoutLineBreak(';')
