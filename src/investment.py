import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker 
from matplotlib.ticker import MultipleLocator, FuncFormatter

months=list()
moneys=list()
salarys=list()
_003s=list()
money=0
_003=0


for month in range(0,12*20):
	months.append(month)
	money = money + 1*np.power(1.01,month)
	moneys.append(money)

	_003 = _003 + 1*np.power(1.0083,month)
	_003s.append(_003)
	salarys.append(1*month)

plt.plot(months,moneys,months,salarys)
plt.xlabel('时间(月)')
plt.ylabel('现金(万元)')
plt.plot(months,moneys,label="$y=∑(1*1.01^x)$",color="red",linewidth=2)
plt.plot(months,salarys,label="$y=1*x$",color="blue",linewidth=2)
plt.plot(months,_003s,label="$y=∑(1*1.003^x)$",color="green",linewidth=2)


ax = plt.gca()
ax.xaxis.set_major_locator( MultipleLocator(12))#1年为一个刻度
ax.yaxis.set_major_locator(MultipleLocator(50))#50万为一个刻度
plt.grid(True)
plt.title('投资收入VS纯工资')
plt.legend()
plt.show()

## 现金（工资+投资收入):
##第一个月:10000,
##第二个月:10000+10000*(1+0.01),
##第三个月:10000+10000(1+0.01)+10000(1+0.01)^2,
##....
##第x个月:10000+10000(1+0.01)+10000(1+0.01)^2+10000(1+0.01)^3+....+10000(1+0.01)^x
## 公式:∑(10000*1.01^x)  x∈[0,12]
