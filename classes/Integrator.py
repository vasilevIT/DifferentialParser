"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 22:21

"""

import numpy as np
import copy

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

    def run(self):
        if self.integration_method == 'Euler':
            return self.euler()
        elif self.integration_method == 'Modify-Euler':
            return self.modify_euler()
        elif self.integration_method == 'Runge-Kutti-1':
            return self.runge_kutti(1)
        elif self.integration_method == 'Runge-Kutti-2':
            return self.runge_kutti(2)
        elif self.integration_method == 'Runge-Kutti-3':
            return self.runge_kutti(3)
        elif self.integration_method == 'Runge-Kutti-4':
            return self.runge_kutti(4)

    def euler(self):
        """
        Метод численного интегрирования Эйлера
        :return:dict
        """

        result = dict()
        params = self.begin_conditions
        result[0] = dict()
        for key, equation in self.equations.items():
            integration_var = key.replace("/dt", "")
            init_value = params[integration_var]
            result[0][key] = float(init_value)

        for t in np.arange(1, float(self.integration_var_value) + float(self.integration_var_step_value),
                           float(self.integration_var_step_value)):
            result[t] = dict()
            for key, equation in self.equations.items():
                equation_value = MathSolver.solv(equation, params)
                integration_var = key.replace("/dt", "")
                equation_value = float(params[integration_var]) + (
                    float(self.integration_var_step_value) * equation_value)
                result[t][key] = equation_value
                params[integration_var] = equation_value
            print(result)
            print(params)
        return result

    def modify_euler(self):
        """
        Метод численного интегрирования Эйлера, модифицированный
        :return:dict
        """

        result = dict()
        params = self.begin_conditions
        result[0] = dict()
        for key, equation in self.equations.items():
            integration_var = key.replace("/dt", "")
            init_value = params[integration_var]
            result[0][key] = float(init_value)

        for t in np.arange(1, float(self.integration_var_value) + float(self.integration_var_step_value),
                           float(self.integration_var_step_value)):
            result[t] = dict()
            for key, equation in self.equations.items():
                params_temp = copy.deepcopy(params)
                # 1
                equation_value_1 = MathSolver.solv(equation, params_temp)
                integration_var = key.replace("/dt", "")
                equation_value = float(params_temp[integration_var]) + equation_value_1
                params_temp[integration_var] = equation_value
                # 2
                equation_value_2 = MathSolver.solv(equation, params_temp)
                # result value
                equation_value = float(params[integration_var]) + 0.5 * float(self.integration_var_step_value) * (
                    equation_value_1 + equation_value_2)
                result[t][key] = equation_value
                params[integration_var] = equation_value

        return result

    def runge_kutti(self, n=1):
        """
        Метод численного интегрирования Рунге-Кутты n-го порядка
        :return:dict
        """

        # raise Exception("Метода Рунге-Кутта еще не реализован")
        result = dict()
        params = self.begin_conditions
        result[0] = dict()
        for key, equation in self.equations.items():
            integration_var = key.replace("/dt", "")
            init_value = params[integration_var]
            result[0][key] = float(init_value)

        if n == 1:
            return self.euler()
        elif n == 2:
            return self.modify_euler()
        elif n == 3:
            pass
        elif n == 4:
            return self.runge_kutti_4()
        raise Exception("Неизвестная степень метода Рунге-Кутта")

    def runge_kutti_4(self):
        """
        Метод Рунге-Кутты 4-го порядка
        :return:
        """
        result = dict()
        params = self.begin_conditions
        result[0] = dict()
        for key, equation in self.equations.items():
            integration_var = key.replace("/dt", "")
            init_value = params[integration_var]
            result[0][key] = float(init_value)

        for t in np.arange(1, float(self.integration_var_value) + float(self.integration_var_step_value),
                           float(self.integration_var_step_value)):
            result[t] = dict()
            for key, equation in self.equations.items():
                params_temp = copy.deepcopy(params)
                integration_var = key.replace("/dt", "")
                # 1
                equation_value_1 = MathSolver.solv(equation, params_temp)
                equation_value = float(params_temp[integration_var]) + 0.5 * float(
                    self.integration_var_step_value) * equation_value_1
                params_temp[integration_var] = equation_value
                # 2
                equation_value_2 = MathSolver.solv(equation, params_temp)
                equation_value = float(params_temp[integration_var]) + 0.5 * float(
                    self.integration_var_step_value) * equation_value_2
                params_temp[integration_var] = equation_value
                # 3
                equation_value_3 = MathSolver.solv(equation, params_temp)
                equation_value = float(params_temp[integration_var]) + equation_value_3
                params_temp[integration_var] = equation_value
                # 4
                equation_value_4 = MathSolver.solv(equation, params_temp)
                equation_value_4 = float(self.integration_var_step_value) * equation_value_4
                # result value
                y_val = (1 / 6) * float(self.integration_var_step_value) \
                                   * (equation_value_1 + 2 * equation_value_2 + 2 * equation_value_3 + equation_value_4)
                equation_value = float(params[integration_var]) + y_val
                result[t][key] = equation_value
                params[integration_var] = equation_value

        return result
