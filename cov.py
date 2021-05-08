from random import seed, expovariate
from matrix import *
from pdb import set_trace as xx 

if __name__ == "__main__": 
    seed(0)             # Generate the same random sequences
    Matrix.SigFig = 4   # Print to this number of significant figures

    # Define the correlation matrix
    corr = matrix("1 0.8\n0.8 1")

    n = 8   # Number of observations per variable
    k = 2   # Number of variables

    # Construct F, the matrix of observations
    lambd = 1
    F = matrix([expovariate(lambd) for i in range(n*k)], size=(n, k))
    print("Matrix F:")
    print(F)

    # Get column vector of means
    mu = vector(k, c=True)
    for c in range(k):
        col = F.col(c)
        mu[c] = col.sum/n
    print("\nMeans")
    print(mu)

    # Get column vector of ones
    ones = vector(n, c=True, fill=1)
    print("\nOnes.t")
    print(ones.t)

    # Matrix A
    A = mu*ones.t
    A = ones*mu.t
    print("\nA")
    print(A)

    # Covariance matrix
    # Definition is https://en.wikipedia.org/wiki/Sample_mean_and_covariance#Definition_of_sample_covariance
    d = F - A
    Q = d*d.t/(n - 1)
    print("\nQ")
    print(Q)

    # Transformed random variables
    F1 = Q*F
    print("Transformed matrix F1:")
    print(F1)
