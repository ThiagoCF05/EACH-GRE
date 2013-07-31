'''
Created on 31/07/2013

@author: thiagocastroferreira
'''
def parse(A):
    result = []
    for target in A.keys():
        for property in A[target].keys():
            for value in A[target][property]:
                element = target + '.' + '.' + property + '.' + value
                result.append(element)
    return set(result)

def dice(A, B):
    A = parse(A)
    B = parse(B)
    
    lenA = len(A)
    lenB = len(B)
    
    return (2. * len(A.intersection(B))) / (lenA + lenB)

def masi(A, B):
    A = parse(A)
    B = parse(B)
    
    division = (len(A.intersection(B))) / (len(A.union(B)))
    
    weight = 0.0
    
    if len(A.intersection(B)) == 0:
        weight = 0.
    elif A == B:
        weight = 1.
    elif A.issubset(B) or B.issubset(A):
        weight = 2. / 3
    else:
        weight = 1. / 3
        
    return weight * division
    