from xeger import Xeger
from random import randint,choice


operatorNoPat = "[+-]\\ {0,1}"
operatorPat = "\\ {0,1}[+-]\\ {0,1}"
multPat = "\\ {0,1}\\*\\ {0,1}"
consPat = "[+-]?[1-9][0-9]{0,1}"
monoPat = "x( {0,1}\\*\\* {0,1}[+-]?[1-9])?"
leftPat = "\\ {0,1}\\(\\ {0,1}"
rightPat = "\\ {0,1}\\)\\ {0,1}"

MAXmonoPat="x\\*\\*9999\\*x\\*\\*2"
ZEROconsPat = "[+-]?0"
ZEROmonoPat = "x( {0,1}\\*\\* {0,1}[+-]?0)?"


pat = Xeger(limit=20)
nest = 0


def generator(times):
    s = generate_poly(times)
    while len(s) > 100:
        s = generate_poly(times)
    return s

def generate_poly(times):
    poly = ""
    operator = randint(0, 1)
    if operator:
        poly += pat.xeger(operatorPat)
    poly += generate_term()
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
        times = randint(0, 5)  ###
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
        factor = pat.xeger(choice([consPat,consPat,consPat,consPat,consPat,consPat,consPat,consPat,consPat,ZEROconsPat]))
    elif factor_type == 2:
        factor = pat.xeger(choice([monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,MAXmonoPat,ZEROmonoPat]))
    elif factor_type == 3:
        nest += 1
        factor = "sin(x)**"+str(randint(-5,5))
        nest -= 1
    elif factor_type == 4:
        nest += 1
        factor = "cos(x)**"+str(randint(-5,5))
        nest -= 1
    elif factor_type == 5:
        nest += 1
        factor = choice(["sin(x)","cos(x)"])
        nest -= 1
    return factor

if __name__=='__main__':
    for i in range(10):
        print(generator(5)+"\n")