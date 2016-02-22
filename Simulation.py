
import pandas as pd
import math as ma
import numpy as np
from numpy import random as rn

drill_cost = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Drilling_cost.csv")
prices = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Price.csv")
cpi = pd.read_csv("C:\Users\Wah Tran\OneDrive\Documents\School\Codes\Simulation\Inflation.csv")

# SIMULATION PARAMETERS #

# CPI for present day (October 2015)
cpi_now = 237.945
# Correlation between initial productionand decline rate
rho = 0.64
# Current year
year_now = 2015
# Number of years to simulate
sim_yrs = 15
# Value at risk level to evaluate
risk = 5
# Number of simulations
sim = 10000

# Adjust historic drilling prices for inflation
p = pd.merge(drill_cost, cpi, on='Year')
p['inflation'] = p['Avg']/cpi_now

p['Oil'] = 1000*p['Oil']/p['inflation']
p['Nat. Gas'] = 1000*p['Nat. Gas']/p['inflation']
p['Dry Well'] = 1000*p['Dry Well']/p['inflation']

p10 = p[(p['Year'] >= 1990)]

# Calculate mean geometric rate of change for each drilling class
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

d_oil_mean, d_oil_std = geo_diff(p10['Oil'])
d_gas_mean, d_gas_std = geo_diff(p10['Nat. Gas'])
d_dry_mean, d_dry_std = geo_diff(p10['Dry Well'])

# Cholesky decomposoition to correlate initial production and decline rate
corr = np.matrix( [[1, rho], [rho, 1]] )
cholesky = np.transpose( np.linalg.cholesky(corr) )

# Generate 'mean' and 'std' for uniform decline rate
dec = rn.uniform(0.15, 0.32, 1000000)
dec_mean = np.mean(dec)
dec_std = np.std(dec)




# For each universe, simulates number of wells
well_num = int( rn.uniform(10, 30) )

# Simulates probability of oil in each well individually using
# truncated normal distributions.  Bernoulli distribution determines
# if oil is ultimately found.
oil_well = 0
for i in range(well_num):
    while True:
        pCH3 = rn.normal(0.99, 0.05)
        pRes = rn.normal(0.75, 0.10)
        if pCH3 <= 1 and pRes <=1:
            pOil = pCH3*pRes
            oil_well += rn.binomial(1, pOil)
            break

dry_well = well_num - oil_well



