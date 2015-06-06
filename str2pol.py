# String interpreter, returns a MultiPol object after parsing the input string

# Accepted operators:
# +, -, *, ^
# Multiplication must ALWAYS be EXPLICIT

from multipol import MultiPol


def str2pol(strpol, var):
    varnum = len(var)

    toadd = strpol.split('+')
    if len(toadd) > 1:
        poly = MultiPol([0])
        for elem in toadd:
            poly = poly + str2pol(elem, var)
        return poly
    else:
        tosub = strpol.split('-')
        if len(tosub) > 1:
            if tosub[0] == '':
                poly = MultiPol([0])
            else:
                poly = str2pol(tosub[0], var)
            for i in range(1, len(tosub)):
                poly = poly - str2pol(tosub[i], var)
            return poly
        else:
            tomult = strpol.split('*')
            if len(tomult) > 1:
                poly = MultiPol([1])
                for elem in tomult:
                    poly = poly * str2pol(elem, var)
                return poly
            else:
                topow = strpol.split('^')
                if len(topow) > 2:
                    raise SyntaxError('Invalid string')
                elif len(topow) == 2:
                    try:
                        x = float(topow[1])
                        d = int(x)
                    except:
                        raise SyntaxError('Invalid string')
                    else:
                        if x != d:
                            raise SyntaxError('Invalid string')
                    return str2pol(topow[0], var) ** d
                else:
                    if isfloat(strpol):
                        if int(strpol) == float(strpol):
                            return MultiPol([int(strpol)])
                        else:
                            return MultiPol([float(strpol)])

                    for i in range(0, varnum):
                        if strpol == var[i]:
                            v = [0, 1]
                            for j in reversed(range(i, varnum - 1)):
                                v = [v]
                            return MultiPol(v, varnum)
                    raise SyntaxError('Invalid string')


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
