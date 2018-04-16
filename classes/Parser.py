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
        self.isNextWord("=")
        block = self.right_part()

        print(var + " = " + block)

    def right_part(self):
        """
        Правая часть уравнениея
        :return:string
        """
        self.passSpace()
        block = ""
        if self.isNextWord("-", False):
            block += "-"
        while True:
            block += self.additionBlock()
            if self.isEOL():
                self.current_index += 1
                break
            if self.isNextWord(")", False):
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
            if self.isNextWord("+", False):
                add_block += " + " + self.multiplicationBlock()
            elif self.isNextWord("-", False):
                add_block += " - " + self.multiplicationBlock()
            else:
                break
        return add_block

    def multiplicationBlock(self):
        """
        Блок арифмитического умножения/деления
        :return:string
        """
        block = self.varBlock()
        while True:
            if self.isNextWord("*", False):
                block += " * " + self.varBlock()
            elif self.isNextWord("/", False):
                block += " / " + self.varBlock()
            else:
                break

        return block

    def varBlock(self):
        """
        Блок с переменной или числом
        :return:string
        """
        block = ""
        if self.isNextWord("(", False):
            block += "("
            block += str(self.right_part())
            if self.isNextWord(")"):
                block += ")"
        elif self.isDigital():
            block += str(self.Number())
        else:
            block += str(self.var())
        return block

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

    def begin_conditions(self):
        self.isNextWord(self.BeginConditions)
        while (self.current_index < len(self.text) - len(self.IntegrationConfitions)) and (
                    self.text[self.current_index:self.current_index + len(self.IntegrationConfitions)]
                    != self.IntegrationConfitions):
            self.var()
            self.isNextWord("=")
            self.Number()
            if self.isEOL():
                self.current_index += 1
            self.passSpace()

    def integration_conditions(self):
        self.isNextWord(self.IntegrationConfitions)
        self.integration_method()
        self.integration_var()
        self.integration_var_step()

    def integration_method(self):
        self.isNextWord(self.IntegrationMethod)
        self.isNextWord("=")
        self.integration_method_name()
        if self.isEOL():
            self.current_index += 1
        else:
            raise Exception("Ожидалась ';'")

    def integration_method_name(self):
        for method in Integrator.integration_methods:
            if self.isNextWord(method, False):
                return method
        raise Exception("Неизвестный метод интегрирования. Укажите один из следующих:" + str(Integrator.integration_methods))


    def integration_var(self):
        self.isNextWord(self.IntegrationVar)
        self.isNextWord("=")
        self.Number()
        if self.isEOL():
            self.current_index += 1
        else:
            raise Exception("Ожидалась ';'")

    def integration_var_step(self):
        self.isNextWord(self.IntegrationVarStep)
        self.isNextWord("=")
        self.Number()
        if self.isEOL():
            self.current_index += 1
        else:
            raise Exception("Ожидалась ';'")

