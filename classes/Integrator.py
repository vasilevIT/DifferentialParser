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


