from Crypto import Random
from Crypto.Util import number

def generate(param):
    q = param[1]
    g = param[2]
    h = param[3]

    return q, g, h

class verifier:
    def setup(self, security):
        p = number.getPrime(2 * security, Random.new().read)
        q = 2*p + 1

        g = number.getRandomRange(1, q-1)
        s = number.getRandomRange(1, q-1)
        print("Secret value:\t",s)
        h = pow(g,s,q)
        
        param = (p,q,g,h)
        print("p=",p)
        print("q=",q)
        print("g=",g)
        print("h=",h)

        return param

    def open(self, param, c, x, *r):
        q,g,h = generate(param)

        sum = 0
        for i in r:
            sum += i

        res = (pow(g,x,q) * pow(h,sum,q)) % q

        return c == res

    def add(self, param, *cm):
        addCM = 1
        for x in cm:
            addCM *= x
        addCM = addCM % param[1]
        return addCM

class prover: 
    def commit(self, param, x):
        q,g,h = generate(param)
        
        r = number.getRandomRange(1, q-1)
        c = (pow(g,x,q) * pow(h,r,q)) % q
        return c, r
 
