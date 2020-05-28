from xeger import Xeger
from random import *

operatorNoPat = "[+-]\\ {0,1}"
operatorPat = "\\ {0,1}[+-]\\ {0,1}"
multPat = "\\ {0,1}\\*\\ {0,1}"
consPat = "[+-]?[1-9][0-9]{0,1}"
monoPat = "x( {0,1}\*\* {0,1}[+]?[1-4][0-9]?)?"
#monoPat = "x( {0,1}\*\* {0,1}[+-]?0)?"
leftPat = "\\ {0,1}\\(\\ {0,1}"
rightPat = "\\ {0,1}\\)\\ {0,1}"
indexPat = "(\*\* {0,1}[+]?[1-4][0-9]?)?"
#indexPat = "(\*\* {0,1}[+-]?0)?"
pat = Xeger(limit=20)
nest = 0


def generator(length):
    s = generate_poly()
    while len(s) > length:
        s = generate_poly()
    return s


def generate_poly():
    poly = ""
    operator = randint(0, 1)
    if operator:
        poly += pat.xeger(operatorPat)
    poly += generate_term()
    if nest:
        times = randint(0, 1)
    else:
        times = randint(0, 2)
    for i in range(0, times):
        poly += pat.xeger(operatorPat) + generate_term()
    return poly


def generate_term():
    term = ""
    operator = randint(0, 1)
    if operator:
        term += pat.xeger(operatorNoPat)
    term += generate_factor()
    if nest:
        times = randint(0, 2)
    else:
        times = randint(0, 4)
    for i in range(0, times):
        term += pat.xeger(multPat) + generate_factor()
    return term


def generate_factor():
    global nest
    if nest < 3:
        factor_type = randint(1, 5)
    else:
        factor_type = randint(1, 2)
    factor = ""
    if factor_type == 1:
        factor = pat.xeger(consPat)
    elif factor_type == 2:
        factor = pat.xeger(monoPat)
    elif factor_type == 3:
        nest += 1
        factor = "sin" + pat.xeger(leftPat) + generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 4:
        nest += 1
        factor = "cos" + pat.xeger(leftPat) + generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 5:
        nest += 1
        factor = "(" + generate_poly() + ")"
        nest -= 1
    #elif factor_type == 6:
    #    factor = choice(["sin","cos"]) + " ( 0 )"
    return factor


if __name__ == "__main__":
    print(generator(10))