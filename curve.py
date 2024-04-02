# -*- coding: utf-8 -*-


"""
Define curve generator functions.
The sample data of curve can be easily replaced with numpy array.
When the generation of a curve depends on other curves, the name of the curve is used as a parameter.
The @reg_node decorator will recognizes and stores the dependencies.

This file can be generated from configuration file or written by customers.
"""


from expander import reg_node
from risk import lerp, sincos
import math
import random


@reg_node
def c1():
    return [1] * 200


@reg_node
def c2():
    return [math.log(x + 1) for x in range(1, 200)]


@reg_node
def c3():
    return [random.random() for x in range(200)]


@reg_node
def c4():
    return [math.cos(x) for x in range(200)]


@reg_node
def c5():
    return [math.sin(x) for x in range(200)]


@reg_node
def c11(c1, c3):
    return [x - sincos(y) for x, y in zip(c1, c3)]


@reg_node
def c12(c2, c4):
    return [2 * x + lerp(x, y, 0.2) for x, y in zip(c2, c4)]


@reg_node
def c13(c11, c12):
    return [1] * 200
