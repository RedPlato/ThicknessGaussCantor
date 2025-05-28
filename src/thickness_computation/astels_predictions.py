import numpy as np

def theoretical_thickness(N):
    r"""Compute the thickness predicted by Astels formula for Bernoulli-Cantor set with alphabet {1, ... , N}"""
    delta = (-N + np.sqrt(N**2 + 4*N))/2

    thickness = np.infty
    for i in range(1,N):
        bound_A = delta*(N-1)*((i+1)*N + N + delta)/((N - delta*(N-1))*(i*N + N + delta))
        bound_B = ((N-(i+1))*N + delta*(N-1))*(i+delta)/((N - delta*(N-1))*(N+delta))
        bound_min = min(bound_A,bound_B)
        if thickness > bound_min:
            thickness = bound_min

    return thickness
