import numpy as np

def real_to_cont_frac(x,n):
    if n==0:
        coeff = int(x)
        return np.array([coeff])
    
    else:
        first_coeff = int(x)

        if first_coeff == x:                #ie x is an integer at this step
            other_coeffs = np.zeros(n-1)    #then the following coefficients are null
        else:
            other_coeffs = real_to_cont_frac(1/(x-first_coeff),n-1)

        return np.concatenate((np.array([first_coeff]), other_coeffs))
    
def cont_frac_to_real(coeffs):
    if coeffs.size==1:
        return coeffs[0]
    
    else:
        return coeffs[0] + 1/cont_frac_to_real(coeffs[1:])
    
def minCF(coeff1,coeff2):
    s1 = len(coeff1)
    s2 = len(coeff2)
    r = min(s1,s2)


    for i in range(r):
        if coeff1[i] < coeff2[i]:
            if i%2==0:
                return coeff1
            else:
                return coeff2
        elif coeff1[i] > coeff2[i]:
            if i%2==0:
                return coeff2
            else:
                return coeff1
            
    #if we get out of the for-loop (ie the r first coefficients are all equal)
    #then we must check if adding coefficients will increase or decrease the value of the continued fraction

    if r%2==0:
        if s1 < s2:
            return coeff2
        else:
            return coeff1
        
    if r%2!=0:
        if s1 < s2:
            return coeff1
        else:
            return coeff2


def ordering(B):
    #sorting a list of words with the order specified by minCF and implementing a sort by insertion (most efficient on ~10 elements lists)
    B_sort = B.copy()
    for i in range(1, len(B)):
        key = B_sort[i]
        j = i - 1

        while j >= 0 and minCF(B_sort[j], key)==key:
            B_sort[j + 1] = B_sort[j]
            j -= 1

        B_sort[j + 1] = key
    return B_sort


  