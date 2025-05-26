import numpy as np
from continued_fractions_toolbox.continued_fractions_basics import cont_frac_to_real

def C(N,n):
    r"""Generating the n first coefficients of words of the Bernoulli-Cantor set with aphabet {1, ... , N}
        PARAMETERS
            N: integer, size of the alphabet
            n: integer, size of the words
        RETURNS
            list of list of integers"""
    base = np.array([[i] for i in range(1,N+1)])
    list_if_even = range(1,N+1)
    list_if_odd  = range(N,0,-1)
    if n==0:
        return base
    
    else: #recursive algorithm
        C_prev = C(N,n-1)
        C_next = np.zeros((N**(n+1),n+1))
        incr = 0
        for j in range(N**n):
            element = C_prev[j]
            for i in range(N):
                if n%2==0:    #we are separating cases so that we generate the numbers in an increasing order
                    new_element = np.append(element,list_if_even[i])
                else:
                    new_element = np.append(element,list_if_odd[i])
                    
                C_next[N*incr + i] = new_element
            incr = incr+1

        return list(C_next)
    

    
def segments_cantor(N,n,k):
    r"""Computing the bounds of the segments of the Bernoulli-Cantor set with alphabet {1, ..., N} associated to words of length n
        PARAMETERS
            N: integer, size of the alphabet
            n: integer, size of the words
            k: integer, size of the suffixes
        RETURNS
            list of list of floats"""

    cantor_step = C(N,n)
    segments_list = list(np.zeros((N**(n+1),2)))

    #creating suffixes to have more precisions

    suffix1 = int(k/2)*[1,N]
    suffixN = int(k/2)*[N,1]
    if k%2!=0:
        suffix1.append(1)
        suffixN.append(N)

    if n%2!=0:
        suffix_begin = suffix1
        suffix_final = suffixN
    else:
        suffix_begin = suffixN
        suffix_final = suffix1
        
    for i in range(N**(n+1)):
        element = cantor_step[i]

        coeff_begin = element + suffix_begin
        coeff_final = element + suffix_final

        segment_begin = cont_frac_to_real(coeff_begin)
        segment_final = cont_frac_to_real(coeff_final)

        segments_list[i] = [segment_begin,segment_final]

    return segments_list