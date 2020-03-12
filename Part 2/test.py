from scipy.stats import expon
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(1, 1)

mean, var, skew, kurt = expon.stats(moments='mvsk')
x = np.linspace(expon.ppf(0.01),
                expon.ppf(0.99), 100)
ax.plot(x, expon.pdf(x),
       'r-', lw=5, alpha=0.6, label='expon pdf')
rv = expon()
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
vals = expon.ppf([0.001, 0.5, 0.999])
bol = np.allclose([0.001, 0.5, 0.999], expon.cdf(vals))
print(bol)
r = expon.rvs(size=1000)

ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
ax.legend(loc='best', frameon=False)
plt.show()


