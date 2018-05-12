# script:       complexmath.py
# author:       Allen H nugent
# date:         2017-05-18
# last edit:    2018-05-12
#
# description:  A calculator for complex numbers based on OOP-architecture.
#
# TODO: support 'a + i b' notation   <<< hasn't this been done???!!!
# a+ib, (a,b), or (r,@p)

# Test Cases
#
# 2+i3 - 1+i1
# 0+i0 + 1+i1
# 0+i0 + 0+i0
# 2,3 - 1,1
# 0,0 + 1,1
# 0,0 + 0,0
# 2@

#import pypreprocessor
import math

#define python3

def Csign(x):
    # assigns sign char for imaginary part
    if x >= 0:
        s = "+"
    elif x < 0:
        s = "-"
    return(s)

class Cvector:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
    def real(self):
        return self.a
    def imag(self):
        return self.b
    def modulus(self):
        return math.sqrt(self.a **2 + self.b **2)
    def phase(self):
        if self.b == 0:
            return 0
        else:
            return math.atan2(self.b, self.a)
    def Cformat(self, complexformat = "i", sep = ""):
        # Returns a string representation of a complex number as...
        #    a + ib  if complexformat = "i"
        #    a, b    if complexformat = ""
        #    (a, b)  if complexformat = "("
        
        if (complexformat == "i"):
            return("{0}{1}{2}{3}i{4}".format(self.a, sep, Csign(self.b), sep, abs(self.b)))
        else:
            #comma = "," if "," in complexformat else ""
            #paren = ("(", ")") if "(" in complexformat else ("", "")
            comma = ","
            paren = ("(", ")") if (complexformat == "(") else ("", "")
            #return("{0},{1}{2}".format(self.a, sep, self.b))
            #  complexformat == "," or undefined
            #       ( a , _  b )
            return("{0}{1}{2}{3}{4}{5}".format(paren[0], self.a, comma, sep, self.b, paren[1]))
    def type(self):
        return 'vector'

class Cphasor:
    def __init__(self, r=0, p=0):
        self.r = r
        self.p = p
    def real(self):
        return (self.r * math.cos(self.p))
    def imag(self):
        return (self.r * math.sin(self.p))
    def modulus(self):
        return self.r
    def phase(self):
        return self.p
    def Cformat(self, complexformat = "", sep = ""):
        # Returns a string representation of a complex number as...
        #    a, @b    if complexformat = ""
        #    (a, @b)  if complexformat = "("

        #comma = "," if "," in complexformat else ""
        #paren = ("(", ")") if "(" in complexformat else ("", "")
        comma = ","
        paren = ("(", ")") if (complexformat == "(") else ("", "")
        return ("{0}{1}{2}{3}{4}{5}{6}".format(paren[0], self.r, comma, sep, "@", self.p, paren[1]))
#        return ("{0},{1}@{2}".format(self.r, sep, self.p))
#        elif (complexformat == "("):
#            return ("({0},{1}@{2})".format(self.r, sep, self.p))
#        else:
#            return ("{0},{1}@{2}".format(self.r, sep, self.p))
    def type(self):
        return 'phasor'

def getComplexFormat(s):
    # Encodes a flag to determine whetehr to use a + ib notation 
    # or (a, b) notation (with or without parentheses).
    
    if (s.find('i') >= 0):
        complexformat = "i"
    else:
        # OUT: always use comma!
#        complexformat = ()
#        if(s.find("(") >= 0):
#            complexformat = complexformat + ("(",)
#        if(s.find(",") >= 0):
#            complexformat = complexformat + (",",)
        complexformat = "(" if(s.find("(") >= 0) else ""
    return complexformat

def PhasorToVector(p):
    v = Cvector()
    v.a = p.real()     # p.a = real part
    v.b = p.imag()     # p.b = imaginary part
    return v

def VectorToPhasor(v):
    p = Cphasor()
    p.r = v.modulus()
    p.p = v.phase()
    return p

def parseComplex(s):
    s = s.replace(" ", "")
    s = s.replace("(", "")
    s = s.replace(")", "")

    ii = s.find('i')
    if ii >= 0:  # using standard 'a + iB' notation
        sign2 = s[ii - 1]
        imult2 = signToNum(sign2)
        # TODO: if imult2 == 0 PROBLEM
        sign1 = s[0]
        imult1 = signToNum(sign1)
        if (imult1 == 0):
            imult1 = 1
            sreal = s[0:(ii - 1)]
        else:
            sreal = s[1:(ii - 1)]
        simag = s[(ii + 1):]
        v = Cvector(float(sreal) * imult1, float(simag) * imult2)
    else:
        ic = s.find(',')
        if ic >= 0:  # a dyad was entered
            ia = s.find('@')
            if ia >= 0:  # using (magnitude, phase) representation
                smagn = s[0:ic]
                sphase = s[ia + 1:]
                v = Cphasor(float(smagn), float(sphase))
            else:        # using (real, imaginary) representation
                sreal = s[0:ic]
                simag = s[ic + 1:]
                v = Cvector(float(sreal), float(simag))
        else:  # a monad was entered: assume the number has no imaginary part
            sreal = s
            simag = 0
            v = Cvector(float(sreal), float(simag))
    return v

def signToNum(sign):
    if sign == '+':
        mult = 1
    else:
        if sign == '-':
            mult = -1
        else:
            mult = 0  # no sign; caller must handle default to +1
    return mult

def parseOp(s):
    op = ''
    if s[0] in dops.keys():
        op = s[0]
    return op

def operate(c1, op, c2):

    if op in ('|', '@'):
        # output of monadic operations is a phasor:
        usephasors = True
    else:
        # default to vector arithmetic if mixed types were entered (ignore for monadic operations):
        usephasors = (c1.type() == 'phasor')
        #X: if type(c2).__name__ == 'Cphasor':
        if c1.type() == 'vector' and c2.type() == 'phasor':
            c2 = PhasorToVector(c2)
            usephasors = False
        #TODO: support a+ib in mixed formats

    if usephasors:
        c3 = Cphasor()
    else:
        c3 = Cvector()

    # unary operations are already covered by the Cphasor methods, so just return the input as a phasor ...
    if op in ('|', '@'):
        c3 = VectorToPhasor(c1)
    # binary operations return a dyad ...
    elif op in ('+', '-'):  
        if usephasors:   # no simple phasor method for addition, so convert to vector
            c1 = PhasorToVector(c1)
            c2 = PhasorToVector(c2)
            c3 = Cvector()
        if op == '+': 
            c3.a = c1.a + c2.a
            c3.b = c1.b + c2.b
        else:
            c3.a = c1.a - c2.a
            c3.b = c1.b - c2.b
        if usephasors:    # convert back
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
            p1 = c1
            exp = c2.r
        c3.r = p1.r ** exp
        c3.p = p1.p * exp
        #c3 = Cvector(p1.r ** exp * math.cos(exp * p1.p), p1.r ** exp * math.sin(exp * p1.p))
        if not usephasors:
            c3 = PhasorToVector(c3)

    return c3, usephasors


# symbols for defined operations:
#ops = ('+', '-', '*', '/', '^',  '|', '@')
dops = {'+': 'addition', '-': 'subtaction', '*': 'multiplication', 
        '/': 'division', '^': 'exponent', '|': 'modulus', '@': 'phase'}

doStackOutput = False;

for i in dops:
    print("{0} : {1}".format(i, dops[i]))

#print("Enter a complex number as (a, b) or (r, @p):")
prompt0 = ('Data entry, display formats: \n'
            + 'a = real part, b = imaginary part; r = modulus, p = phase (radians); \n'
            + 'parentheses and spaces are optional. \n\n'
            + 'Enter a complex number as a+ib, (a,b), or (r,@p): ')
prompt1 = 'Enter a complex number as a+ib, (a,b), or (r,@p), or ? for help: '
prompt2 = 'Enter an operation and (optionally) another complex number in the same format: '

print('Data entry, display formats: \n'
            + '   a = real part, b = imaginary part; r = modulus, p = phase (radians); \n'
            + '      a+ib, (a,b), or (r,@p) \n'
            + '   parentheses and spaces are optional. \n\n')

# python2 s1 = raw_input(prompt0)
s1 = input(prompt0)
sep = " " if (s1.strip().find(" ") >= 0) else "" # does the user prefer spaces between components and terms?

# if s1 == '?':
#     prompt = ('a = real part, b = imaginary part; r = modulus, p = phase (radians); \n'
#             + 'parentheses and spaces are optional.')
#     s1 = raw_input(prompt)

while len(s1) != 0:
    v1 = parseComplex(s1)
    complexformat = getComplexFormat(s1)  #: discover which format has been entered
    sep = " " if (s1.strip().find(" ") >= 0) else ""
    # python2 s2 = raw_input(prompt2)
    s2 = input(prompt2)

    op = parseOp(s2)  # extract operator
    if op in dops.keys():
        if op in ('|', '@'):
            v2 = Cvector()   # not needed, so set dummy = (0,0)
        else:
            v2 = parseComplex(s2[1:])  # what happens if no v2?

        v3, usephasors = operate(v1, op, v2)

        if op in ('|', '@'):   # modulus or phase
            if (op == '|'):
                f3 = v3.modulus()
            elif (op == '@'):
                f3 = v3.phase()
            #ifdef python3
            if doStackOutput:
                print("{0}".format(v1.Cformat(complexformat, sep)))
                print("{0}".format(op))
                #print(' = ')
                print("{0}={1}".format(sep))
                print("{0}".format(f3))
            else:
                print("{0}{1} {2}{3} = {4}{5}".format(v1.Cformat(complexformat, sep), sep, op, sep, sep, f3))
        else:
            if doStackOutput:
                print("{0}".format(v1.Cformat(complexformat, sep)))
                print("{0}".format(op))
                print("{0}".format(v2.Cformat(complexformat, sep)))
                print("{0}={1}".format(sep))
                print("{0}".format(v3.Cformat(complexformat, sep)))
            else:
                print("{0}{1} {2} {3}{4}{5} = {6}{7}".format(v1.Cformat(complexformat, sep), sep, 
                      op, sep, v2.Cformat(complexformat, sep), sep, sep, v3.Cformat(complexformat, sep)))
                
    s1 = input(prompt1)

exit(0)
