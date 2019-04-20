import numpy as np
from numpy import linalg as la

A = np.mat([[3, 4, 3, 1], [1, 3, 2, 6], [2, 4, 1, 5], [3, 3, 5, 2]])
U,sigma,VT = la.svd(A)

# sigma是array类型 需要转化成 4*4的类型

Alice = np.mat([[5, 3, 4, 4]])
# 转化成对角阵 https://blog.csdn.net/qq_35277038/article/details/80766746
e = np.diag(sigma)
s = np.mat(e)
#Alice_locayion = Alice*U*sigma#*la.inv(sigma)
Alice_locayion = Alice*U*s.I # 
Alice_locayion = np.multiply(np.multiply(Alice, U), s.I)
print(s)
# print(U)

# print(sigma)

# print(VT)

# print(s.I)
# e = np.diag(sigma)
# print(e)