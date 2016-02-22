
import pandas as pd
import math as ma
import numpy as np

drill_cost = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Drilling_cost.csv")
prices = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Price.csv")
cpi = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Inflation.csv")

cpi_now = 237.945

p = pd.merge(drill_cost, cpi, on='Year')
p['inflation'] = p['Avg']/cpi_now

p['Oil'] = p['Oil']/p['inflation']
p['Nat. Gas'] = p['Nat. Gas']/p['inflation']
p['Dry Well'] = p['Dry Well']/p['inflation']

p10 = p[(p['Year'] >= 1996)]


def geo_diff(x):
    n = []
    m = []
    o = []
    y = x.shift(1)

    for i in x:
        n.append(ma.log(i))       
    for i in y:
        m.append(ma.log(i))
    for i in range(len(x)):
        o.append(n[i] - m[i])
    return np.nanmean(o), np.nanstd(o)

d_oil = geo_diff(p10['Oil'])
d_gas = geo_diff(p10['Nat. Gas'])
d_dry = geo_diff(p10['Dry Well'])

