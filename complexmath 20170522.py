# script:   complexmath.py
# author:   Allen H nugent
# date:     2017-05-18
#
# description:  A calculator for complex numbers.

import math

# compensating for Python 2.x/3.x stupidity:
def raw_input(s):
    return input(s)

class Cvector:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
    def modulus(self):
        return math.sqrt(self.a **2 + self.b **2)
    def phase(self):
        if self.b == 0:
            return 0
        else:
            return math.atan2(self.b, self.a)

class Cphasor:
    def __init__(self, r=0, p=0):
        self.r = r
        self.p = p
    def real(self):
        return (self.r * math.cos(self.p))
    def imag(self):
        return (self.r * math.sin(self.p))

def PhasorToVector(p):
    v = Cvector()
    v.a = p.real
    v.b = p.imag
    return v

def VectorToPhasor(v):
    p = Cphasor()
    p.r = v.modulus
    p.p = v.phase
    return p

# this was only used during early dev:
def parseReal(s):
    ic = s.find(',')
    #print "ic = %d" % (ic)
    if ic >= 0:
    #    print "s[0:1] = %s" % (s[0:1])
        sreal = s[0:ic]
    #    print "C: sreal = %s" % (sreal)
    else:
        sreal = s
    #    print "R: sreal = %s" % (sreal)
    return float(s)

def parseComplex(s):
    s = s.strip()
    s = s.strip('(')
    s = s.strip(')')
    ic = s.find(',')
    if ic >= 0:  # a dyad was entered
        ia = s.find('@')
        if ia >= 0:  # using (magnitude, phase) representation
            v = Cphasor()
            smagn = s[0:ic]
            sphase = s[ia + 1:]
            v.r = float(smagn)
            v.p = float(sphase)
            #v = PhasorToPoint(float(smagn), float(sphase))
        else:        # using (real, imaginary) representation
            v = Cvector()
            sreal = s[0:ic]
            simag = s[ic + 1:]
            v.a = float(sreal)
            v.b = float(simag)
    else:  # a monad was entered: assume the number has no imaginary part
        v = Cvector
        sreal = s
        simag = 0
        v.a = float(sreal)
        v.b = float(simag)
    return v

def parseOp(s):
    op = ''
    if s[0] in ops:
        op = s[0]
    return op

def operate(c1, op, c2):
    usephasors = not (type(c1).__name__ == 'Cvector')  # uses different arithmentic methods depending on whether inputs are vectors or phasors
    if usephasors:
        c3 = Cphasor()
    else:
        if op not in ('|', '@'):  # c2 should be a dyad
            if type(c2).__name__ == 'Cphasor':  # default to vector arithmetic when mixed types are entered
                c2 = PhasorToVector(c2)
        c3 = Cvector()

    # unary operations returns a monad ...
    if op == '|':  
        c3.a = c1.modulus()
        c3.b = 'nan'
    elif op == '@':
        c3.a = c1.phase()
        c3.b = 'nan'
    # binary operations return a dyad ...
    elif op in ('+', '-'):  
        if usephasors:   # no simple phasor method for addition, so convert to vector
            c1 = PhasorToVector(c1)
            c2 = PhasorToVector(c2)
        if op == '+': 
            c3.a = c1.a + c2.a
            c3.b = c1.b + c2.b
        else:
            c3.a = c1.a - c2.a
            c3.b = c1.b - c2.b
        if usephasors:  
            c3 = VectorToPhasor(c3)
    elif op == '*':
        if usephasors:
            c3.r = c1.r * c2.r
            c3.p = c1.p + c2.p
        else:
            c3.a = c1.a * c2.a - c1.b * c2.b
            c3.b = c1.a * c2.b - c2.a - c1.b
    elif op == '/':
        if usephasors: 
            if c2.r == 0:
                c3.r = 'nan'
                c3.p = 'nan'
            else:
                c3.r = c1.r / c2.r
                c3.p = c1.p - c2.p
        else:
            if c2.modulus == 0:
                c3.a = 'nan'
                c3.b = 'nan'
            else:
                denom = (c2.a ** 2 + c2.b ** 2)
                c3.a = (c1.a * c2.a + c1.b * c2.b) / denom
                c3.b = (c2.a * c1.b - c1.a * c2.b) / denom
    elif op == '^':
        # TODO: how to encode power into kbd input syntax? parse fractional exponent?
        if not usephasors:
            p1 = VectorToPhasor(c1)
            exp = c2.a
        else:
            exp = c2.r
        c3.r = p1.r ** exp
        c3.p = p1.r / exp
        if not usephasors:
            c3 = PhasorToVector(c3)

    return c3

# symbols defined operations:
ops = ('+', '-', '*', '/', '|', '@', '^')
opnames = ('plus', 'minus', 'multiplied by', 'divided by', 'modulus', 'phase', 'exponent')
# TODO: create a lookup incl. words 'addition',... 'modulus', 'phase'
#X: opsdict = zip(ops, names)

print ("Supported complex operators:")
#for op in ops:
    #compiler error in Python3.x: print "(s%: s%)" % (op, names[op])
#    print (op)
#    print (op + ': ' + names[op])
#for keys, values in opsdict.items():
#    print(keys)
#    print(values)
for i in range(len(ops)):
    print(ops[i] + '  ' + opnames[i])
    
print ("")
print ("Complex numbers should be entered as dyads; if a monad is entered, it is assumed to represent a real number.")
print ("After the first entry, a second entry comprised of an operator and optional argument will be prompted.")
print ("If the operator is unary, a second dyad should not be entered.")
print ("If the operator requires an argument (e.g. an exponent), it should be entered immediately following the operator, on the same line.")
print ("If the argument is fractional, it can be entered as a ratio (a/b).")
print ("If the operator is binary, the argument should be a second complex number.")
print ("")

#formatV = "(%d, %d)"  # only useful in Python 2.x
prompt = 'Enter a complex number as (a,b) or (r,@p), where parentheses are optional: \n'
#print("Enter a complex number as (a, b) or (r, @p):")
s1 = raw_input(prompt)
while len(s1) != 0:
    v1 = parseComplex(s1)
    s2 = raw_input('Enter an operation and (optionally) another complex (or real) number in the same format: ')
    op = parseOp(s2)
    if op in ops:
        if op in ('|', '@'):
            v2 = Cvector()   # (0,0)
        else:
            v2 = parseComplex(s2[1:])  # what happens if no v2?

        v3 = operate(v1, op, v2)
        
        usephasors = not (type(v3).__name__ == 'Cvector')
        if op in ('|', '@'):
            if usephasors:
                print ('(' + str(v1.r) + ',@' + str(v1.p) + ') ' + op + ' = ' + str(v3.r))
            else:
                #compiler error in Python3.x: print formatV % (v1.a, v1.b)
                print ('(' + str(v1.a) + ',' + str(v1.b) + ') ' + op + ' = ' + str(v3.a))
        elif op == '^':
            if usephasors:
                print ('(' + str(v1.r) + ',' + str(v1.p) + ')' + op + v2.a + ' = (' + str(v3.r) + ',@' + str(v3.p) + ')')
            else:
                print ('(' + str(v1.a) + ',' + str(v1.b) + ')' + op + v2.a + ' = (' + str(v3.a) + ',' + str(v3.b) + ')')
        else:
            if usephasors:
                print ('(' + str(v1.r) + ',' + str(v1.p) + ')' + op + '(' + str(v2.r) + ',@' + str(v2.p) + ') = (' + str(v3.r) + ',' + str(v3.p) + ')')
            else:
                print ('(' + str(v1.a) + ',' + str(v1.b) + ')' + op + '(' + str(v2.a) + ',' + str(v2.b) + ') = (' + str(v3.a) + ',' + str(v3.b) + ')')

    s1 = raw_input(prompt)

exit(0)
