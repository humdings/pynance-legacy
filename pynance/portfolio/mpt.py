
import numpy as np
import pandas as pd
   
   
def minimum_var(R):
    '''
    Minimum Variance Portfolio weights.
    param:
        R: (Series) portfolio returns
    returns: (Series)
    '''
    cov_inv = np.linalg.inv(R.cov())
    ones = np.ones(len(cov_inv))
    v = cov_inv.dot(ones)
    w = v / ones.T.dot(v)
    return pd.Series({sym: w[i] for i,sym in enumerate(R)}) 

def EF(R, target_func, **kwargs):
    '''
    Efficient Frontier Portfolio weights.
    minimum risk given a target return.
    param:
        R: (Series) portfolio returns
        target_func: (function) takes a series and returns a float.
        kwargs: args passed to the target_func
    returns: 
        (Series)
    '''
    target = target_func(R, **kwargs)
    c_inv = np.linalg.inv(R.cov())
    ones = np.ones(len(c_inv))
    mu0 = np.array([target, 1.0])
    M = np.array([R.mean(), ones]).T
    B = np.dot(M.T, c_inv.dot(M))
    B_inv = np.linalg.inv(B)
    v,u  = np.dot(c_inv, M), np.dot(B_inv, mu0)
    return np.dot(v ,u)