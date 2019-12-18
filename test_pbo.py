from pypbo import pbo
from util.metrics import sharpe_iid
import numpy as np
N = 100
T = 200
mu, sigma = 0, 0.01
M = np.random.normal(mu, sigma, size=(T, N))

print(M.shape)

S = 12


result = pbo(M, S, sharpe_iid, threshold=0.0, n_jobs=1, verbose=False)
print(result.pbo)

