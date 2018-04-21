"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 23:13

"""


class MathSolver:
    """
    Класс занимается решением арифметического выражения
    """

    @staticmethod
    def solv(equation, params):
        """
        Решает уравние
        :param equation:string - уравнение
        :param params:dict - переменные
        :return:float - результат решения
        """
        for key, value in params.items():
            equation = equation.replace(key, str(value))
        try:
            value = eval(equation)
            return value
        except Exception as e:
            raise Exception("Не удалось решить уравнение. " + e.args[0])
