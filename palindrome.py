#palindrome.py
from itertools import combinations

def palindrome(text):
    #Check for equality with reversed string
    return str(text)[::-1] == str(text)

def n_palindromes(n):
    #Return list of palindromes under n
    return [str(i) for i in range(1, n+1) if palindrome(i)]

def nth_palindrome(n, count=0, i=0):
    #Brute force search for palindromes
    while count!=n: 
        i+=1
        if palindrome(i): count +=1
    return i 

def ryandromes(n):
    #Convert to integer and return sums of each pair if 
    #the value is in the list of palindromes
    ps = [int(n) for n in n_palindromes(n)]
    #return [(p[i] + p[i+1]) for i in range(len(p)-1) if (p[i] + p[i+1]) in p]
    res = []
    for i in range(len(ps)):
        for j in range(2, len(ps[i:])): 
            if sum(ps[i:i+j]) in ps and sum(ps[i:i+j]) not in res:
                res.append(sum(ps[i:i+j]))
    return sorted(res)



def nth_ryandrome(n, current = 10):
    #Use the ryandrome list generate in ryandromes(n) to find the nth ryandrome
    try: return ryandromes(current)[n-1]
    except IndexError: return nth_ryandrome(n, 2*current) 

if __name__ == "__main__":
    print len(n_palindromes(2**24))
    print n_palindromes(2**24)[-1]
    print nth_palindrome(22222)
    print len(ryandromes(10000))
    print nth_ryandrome(200)




