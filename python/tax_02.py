#! /usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn-poster")
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.family']='sans-serif'
plt.rcParams['axes.unicode_minus']=False

taxList = [3000, 12000, 25000, 35000, 55000, 80000,180000]
taxDict = {3000: 0.03, 12000: 0.1, 25000: 0.2, 35000: 0.25, 55000: 0.3, 80000: 0.35, 180000: 0.45}

# 新税法速算扣除数
def quick(x):
    money = 0
    salary = x - 5000
    for stage in taxList:
        if salary <= stage:
            for i in range(taxList.index(stage), 0, -1):
                if i == 0:
                    money = money + taxList[i] * (taxDict.get(stage) - taxDict.get(taxList[i]))
                    break
                if i == 1:
                    money = money + taxList[i-1] * (taxDict.get(stage) - taxDict.get(taxList[i-1]))
                    break
                money = money + (taxList[i-1] - taxList[i-2]) * (taxDict.get(stage) - taxDict.get(taxList[i-1]))
            break
    return money

# 新税法纳税金额
def new(x):
    tt = []
    for sal in x:
        tax = 0
        salary = sal - 5000
        for stage in taxList:
            if salary <= stage:
                tax = salary * taxDict.get(stage) - quick(stage)
                tt.append(tax)
                break
    return tt

ztaxList = [1500, 4500, 9000, 35000, 55000, 80000, 150000]
ztaxDict = {1500: 0.03, 4500: 0.1, 9000: 0.2, 35000: 0.25, 55000: 0.3, 80000: 0.35, 150000: 0.45}
#ztaxQuick = {1500: 0, 4500: 105, 9000: 555, 35000: 1005, 55000: 2755,  80000: 5505, 150000: 13505}

# 旧税法速算扣除数
def zquick(x):
   money = 0
   salary = x - 3500
   for stage in ztaxList:
       if salary <= stage:
           for i in range(ztaxList.index(stage), 0, -1):
               if i == 0:
                   money = money + ztaxList[i] * (ztaxDict.get(stage) - ztaxDict.get(ztaxList[i]))
                   break
               if i == 1:
                   money = money + ztaxList[i-1] * (ztaxDict.get(stage) - ztaxDict.get(ztaxList[i-1]))
                   break
               money = money + (ztaxList[i-1] - ztaxList[i-2]) * (ztaxDict.get(stage) - ztaxDict.get(ztaxList[i-1]))
           break
   return money

# 旧税法纳税金额
def old(x):
    zz = []
    for sal in x:
        tax = 0
        salary = sal - 3500
        for stage in ztaxList:
            if salary <= stage:
                tax = salary * ztaxDict.get(stage) - zquick(stage)
                zz.append(tax)
                break
    return zz

# 新旧税法纳税差额
def y(x):
    yy = []
    zz = old(x)
    tt = new(x)
    for i in zz:
        index = zz.index(i)
        yy.append(zz[index] - tt[index])
    return yy

plt.grid(True, linestyle = "-.", color = "grey", linewidth = 1.0)
x = np.arange(5000, 50000, 1000)
plt.xticks(range(5000,50000,3000))
plt.yticks(range(0,10000,500))
plt.plot(x, y(x), color="blue", linewidth=2.0, linestyle="-", label="减少")
plt.plot(x, new(x), color="red", linewidth=1.0, linestyle="--", label="新税法")
plt.plot(x, old(x), color="green", linewidth=1.0, linestyle="--", label="旧税法")
plt.scatter([30000], [2030], s=30, color="red")
plt.annotate("(30000,2030)", xy=(30000,2030), fontsize=10, xycoords='data')
plt.scatter([17000], [1380], s=30, color="red")
plt.annotate("(17000,1380)", xy=(17000,1380), fontsize=10, xycoords='data')
plt.legend(loc="upper left")
plt.xlabel(u"扣除五险一金后工资")
plt.ylabel(u"每月个税")
plt.title(u"算算省了多少钱")
plt.show()
