#textpyramid
from string import lowercase

def pyramid(n):
    """Prints a n-character tall pyramid of letters, formatted by dashes.
       Lowercase is the list of all lowercase letters, imported from the string library
       and extended to prevent an IndexError (note that this is not memory efficient)."""
    print("\n".join(['-'*(n-i-1) + (lowercase*(n**2))[i**2:(i+1)**2] + '-'*(n-i-1) for i in range(n)]))

def space_efficient_pyramid(n, res=''):
    """A space efficient variation on pyramid"""
    for i in range(n):
        res += '-'*(n-i-1)
        for j in range(i**2, (i+1)**2):
             res += lowercase[j%26]
        res += '-'*(n-i-1)+'\n'
    print res

if __name__ == "__main__":
    pyramid(100)