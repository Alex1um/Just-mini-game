import random
from typing import *


def break_number_sum(number: float, length: int) -> Tuple[float]:
    variable = number
    constituents = []
    for i in range(length):
        constituent: float = random.uniform(0, variable)
        constituents.append(constituent)
        variable -= constituent
    return tuple(constituents)