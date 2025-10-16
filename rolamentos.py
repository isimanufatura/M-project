import numpy as np
import matplotlib.pyplot as plt

# Fatores de confiabilidade R da distribuição de weibull
weibull = {
#   R% : K_R
    50 : 5.00,
    90 : 1.00,
    95 : 0.62,
    96 : 0.53,
    97 : 0.44,
    98 : 0.33,
    99 : 0.21,
}

R = 99 # porcentual de confiabilidade
L10 = 10 # vida em fadiga expressa em milhões de revoluções
K_R = weibull[R]

Lp = K_R*L10

Fa_Co = {
    0.014 : 0.19,
    0.021 : 0.21,
    0.028 : 0.22,
    0.042 : 0.24,
    0.056 : 0.26,
    0.070 : 0.27,
    0.084 : 0.28,
    0.110 : 0.30,
    0.170 : 0.34,
    0.280 : 0.38,
    0.420 : 0.42,
    0.560 : 0.44,
}

ratio = [0.014, 0.021, 0.028, 0.042, 0.056, 0.070,
         0.084, 0.110, 0.170, 0.280, 0.420, 0.560]

e = [0.19, 0.21, 0.22, 0.24, 0.26, 0.27,
     0.28, 0.30, 0.34, 0.38, 0.42, 0.44]

ratio_interp = np.linspace(0.014,0.560, num=100)
e_interp = np.interp(ratio_interp, ratio, e)

plt.figure()
plt.plot(ratio, e, label='original')
plt.plot(ratio_interp, e_interp, label='interpolated')
plt.legend()
plt.show()