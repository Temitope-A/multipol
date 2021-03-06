from numbers import Number, Integral
import re
import json


class MultiPol(object):
# Constructor method
# Lowest degrees first
    def __init__(self, pol_list, var=None):

        MultiPol.clean(pol_list)
        self.pol = MultiPol.normalize(pol_list)
        #TO DO: Check that the lists ultimately contain
        #Numbers

        self.poldegree = len(self.pol) - 1
        self.degree = MultiPol.caldegree(self.pol)

        if var is None:
            self.var = MultiPol.calcvar(self.pol)
        else:
            try:
                d = int(var)
            except TypeError:
                print('number of variable specification not valid')
            else:
                if d < MultiPol.calcvar(self.pol):
                    raise ArithmeticError('You are using more variables than '
                                          'specified')
                else:
                    self.var = d

#Evaluation by call
    def __call__(self, value):
        return self.evaluate(value)

###### Operator methods #######################################################

#Equality checking.

    def __eq__(self, other):
        if isinstance(other, Number):
            return self == MultiPol([other])
        else:
            d = other.poldegree
            if self.poldegree != d:
                return False
            else:
                for i in range(0, d + 1):
                    a = self.pol[i]
                    b = other.pol[i]

                    if isinstance(a, Number):
                        if isinstance(b, Number):
                            if a != b:
                                return False
                        else:
                            return a == MultiPol(b)
                    else:
                        if isinstance(b, Number):
                            return MultiPol(a) == b
                        else:
                            return MultiPol(a) == MultiPol(b)
            return True

#Addition and subtraction (addition needs amending)

    def __add__(self, other):
        try:
            d = other.poldegree
        except AttributeError:
            if isinstance(other, Number):
                return self + MultiPol([other])
            else:
                raise TypeError(other)
        else:
            if self.var == other.var:
                pol_list = []
                k = min(self.poldegree, d) + 1
                for i in range(0, k):
                    a = self.pol[i]
                    b = other.pol[i]
                    if isinstance(a, Number):
                        if isinstance(b, Number):
                            pol_list.append(a + b)
                        else:
                            pol_list.append((MultiPol([a]) + MultiPol(b)).pol)
                    elif isinstance(b, Number):
                        pol_list.append((MultiPol(a) + MultiPol([b])).pol)
                    else:
                        pol_list.append((MultiPol(a) + MultiPol(b)).pol)

                pol_list.extend(self.pol[k:])
                pol_list.extend(other.pol[k:])

                return MultiPol(pol_list, max(self.var, other.var))

            elif self.var > other.var:
                pol_list = other.pol
                for i in range(other.var, self.var):
                    pol_list = [pol_list]
                return self + MultiPol(pol_list, self.var)
            else:
                return other + self

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        pol_list = []
        for i in range(0, self.poldegree + 1):
            if isinstance(self.pol[i], Number):
                pol_list.append(-self.pol[i])
            else:
                pol_list.append((-MultiPol(self.pol[i])).pol)

        return MultiPol(pol_list, self.var)

    def __sub__(self, other):
        return self + (-other)

#Multiplication

    def __mul__(self, other):
        try:
            m = self.poldegree + other.poldegree
        except AttributeError:
            if isinstance(other, Number):
                return self * MultiPol([other])
            else:
                raise TypeError('{} Is not a polynomial '
                                'or number'.format(other))
        else:
            if self.var == other.var:
                d = self.var
                pol_list = [0 for i in range(0, m + 1)]
                for i in range(0, self.poldegree + 1):
                    for j in range(0, other.poldegree + 1):
                        a = self.pol[i]
                        b = other.pol[j]
                        if (isinstance(a, Number) and isinstance(b, Number)
                        and isinstance(pol_list[i + j], Number)):
                            pol_list[i + j] += a * b
                        else:
                            if isinstance(a, Number):
                                a = [a]
                            if isinstance(b, Number):
                                b = [b]
                            if isinstance(pol_list[i + j], Number):
                                pol_list[i + j] = [pol_list[i + j]]

                            x = (MultiPol(a, d) * MultiPol(b, d)
                                 + MultiPol(pol_list[i + j], d))
                            pol_list[i + j] = x.pol

                return MultiPol(pol_list, d)

            elif self.var > other.var:
                pol_list = other.pol
                for i in range(other.var, self.var):
                    pol_list = [pol_list]
                return self * MultiPol(pol_list, self.var)
            else:
                return other * self

    def __rmul__(self, other):
        return self * other

    def __pow__(self, exp):
        if exp == 0:
            return 1
        elif exp == 1:
            return self
        elif not(isinstance(exp, Integral) and (exp > 0)):
            raise TypeError(exp)
        else:
            return self * self ** (exp - 1)

# Division
#    def __truediv__(self, other):
#        m = self.degree
#        try:
#            n = other.degree
#        except AttributeError:
#            if isinstance(other, Number):
#                return self/Polynomial([other])
#            else:

# Evaluation via Horner's method ##############################################

    def evaluate(self, x):

        if isinstance(x, Number):
            x = [x]

        if self.var == 0:
            return self.pol[0]

        else:
            if len(x) < self.var:
                raise IndexError('Variables and points of evaluation'
                                 ' not compatible')
            else:
                return MultiPol.__evaluate(self.pol, x)

    def __evaluate(pol_list, x):

        if isinstance(pol_list, Number):
            return pol_list
        else:
            res = MultiPol.__evaluate(pol_list[-1], x[:-1])
            for i in reversed(range(0, len(pol_list) - 1)):
                res = x[-1] * res + MultiPol.__evaluate(pol_list[i], x[:-1])

            return res

# Constructors helpers#########################################################

# This class method deletes trailing zeroes recursively, see __eq__ for identity
# checking

    def clean(pol_list):
        try:
            n = len(pol_list)
        except TypeError as Err:
            if isinstance(pol_list, Number):
                pass
            else:
                print(Err)
        else:
            while n > 1:
                try:
                    pol_list[-1][0]
                except TypeError:
                    if pol_list[-1] == 0:
                        pol_list.pop()
                    else:
                        break
                else:
                    if MultiPol(pol_list[-1]) == 0:  # This eliminates
                        pol_list.pop()               # trailing zeroes
                    else:
                        break
                finally:
                    n -= 1

            for element in pol_list:
                MultiPol.clean(element)

    def normalize(pol_list):
        s = str(pol_list)
        match = re.search('\[\[.\]\]', s)
        while match is not None:
            s = re.sub('\[\[.\]\]', MultiPol.change, s)
            match = re.search('\[\[.\]\]', s)

        return json.loads(s)

    def change(matchobj):

        x = matchobj.group(0).replace('[[', '[')
        return x.replace(']]', ']')

# This method computes the degree of a multivariable Polynomial as max degree of
# the monomials.
    def caldegree(pol_list):
        try:
            pol_list[0]
        except TypeError as Err:
            if isinstance(pol_list, Number):
                return 0
            else:
                print(Err(pol_list))
        else:
            return max([MultiPol.caldegree(x) + pol_list.index(x)
                       for x in pol_list])

# This method computes the number of variables
    def calcvar(pol_list):
        try:
            d = len(pol_list)
        except TypeError as Err:
            if isinstance(pol_list, Number):
                return 0
            else:
                raise Err
        else:
            if d == 1:
                if isinstance(pol_list[0], Number):
                    return 0
                else:
                    return 1 + MultiPol.calcvar(pol_list[0])
            else:
                return 1 + max([MultiPol.calcvar(x) for x in pol_list])

#Representation methods #######################################################
#__repr__ returns the formal representation,

    def __repr__(self):
        return repr(self.pol)

#_str_ the informal presentation of the polynomial
