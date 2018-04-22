"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 22:21

"""

import numpy as np

from classes.MathSolver import MathSolver


class Integrator:
    """
    Решает систему линейных уравнений
    """
    integration_methods = (
        "Euler",
        "Modify-Euler",
        "Runge-Kutti-1",
        "Runge-Kutti-2",
        "Runge-Kutti-3",
        "Runge-Kutti-4",
    )

    def __init__(self) -> None:
        super().__init__()
        self.equations = dict()
        self.begin_conditions = dict()
        self.integration_method = None
        self.integration_var_value = 0
        self.integration_var_step_value = 0

    def __str__(self) -> str:
        return "equations: " + str(self.equations) + "\nbegin_conditions: " + str(self.begin_conditions) \
               + "\nintegration_method: " + str(self.integration_method) + "\n" \
               + "\nintegration_var_value: " + str(self.integration_var_value) + "\n" \
               + "\nintegration_var_step_value: " + str(self.integration_var_step_value)

    def euler(self):
        """
        Метод численного интегрирования Эйлера
        :return:dict
        """

        result = dict()
        params = self.begin_conditions
        # TODO поправить метод расчета.
        for t in np.arange(0, float(self.integration_var_value), float(self.integration_var_step_value)):
            result[t] = dict()
            for key, equation in self.equations.items():
                equation_value = MathSolver.solv(equation, params)
                result[t][key] = equation_value
                params[key] = equation_value
        print(result)
        return result

    def modify_euler(self):
        """
        Метод численного интегрирования Эйлера, модифицированный
        :return:dict
        """
        pass

    def runge_kutti(self, n=1):
        """
        Метод численного интегрирования Рунге-Кутты n-го порядка
        :return:dict
        """
        pass
