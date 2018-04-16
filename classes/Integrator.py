"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 22:21

"""

class Integrator:
    """
    Решает систему линейных уравнений
    """
    integration_methods = (
        "Euler",
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


