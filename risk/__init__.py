# -*- coding: utf-8 -*-

"""This package consist of common function."""

import math


def lerp(x: float, y: float, t: float) -> float:
    return (1 - t) * x + t * y


def sincos(x: float) -> float:
    return math.cos(math.sin(x))
