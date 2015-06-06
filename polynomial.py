from multipol import MultiPol


class Polynomial(MultiPol):

# Instances are polynomials, implemented operations are additions
# (subtractions), multiplications. Numbers and be added or multiplied
# seamlessly.
# Pol([1,0,-1,3]) is 1-x^2+3x^3
# Evaluation can be done by calling the polynomial on the value
# For interactive use, import variable x from var.py

    def __init__(self, pol_list):

        MultiPol.__init__(self, pol_list, 1)

#Addition and subtraction

    def __str__(self):
        if self.pol[0] != 0:
            pol_str = str(abs(self.pol[0]))
            if self.pol[0] > 0:
                nextsign = '+'
            else:
                nextsign = '-'
        else:
            pol_str = ''
            nextsign = ''

        for i in range(1, self.degree + 1):
            if self.pol[i] != 0:
                a = abs(self.pol[i])
                if a != 1:
                    pol_str = (str(a) + 'x^{}'.format(i) + nextsign + pol_str)
                else:
                    pol_str = ('x^{}'.format(i) + nextsign + pol_str)
                if self.pol[i] > 0:
                    nextsign = '+'
                else:
                    nextsign = '-'
        if nextsign == '-':
            pol_str = '-' + pol_str

        return pol_str


