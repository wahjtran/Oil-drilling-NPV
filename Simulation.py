
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
cost = pd.merge(drill_cost, cpi, on='Year')
cost['inflation'] = cost['Avg']/cpi_now

cost['Oil'] = 1000 * cost['Oil'] / cost['inflation']
cost['Nat. Gas'] = 1000 * cost['Nat. Gas'] / cost['inflation']
cost['Dry Well'] = 1000 * cost['Dry Well'] / cost['inflation']

cost90 = cost[ ( cost['Year'] >= 1990 ) ]

# Calculate mean geometric rate of change for each drilling class
def geo_diff(x):
    n = []
    m = []
    o = []
    y = x.shift(1)

    for i in x:
        n.append( ma.log(i) )       
    for i in y:
        m.append( ma.log(i) )
    for i in range( len(x) ):
        o.append( n[i] - m[i] )
    return np.nanmean(o), np.nanstd(o)

d_oil_mean, d_oil_std = geo_diff( cost90['Oil'] )
d_gas_mean, d_gas_std = geo_diff( cost90['Nat. Gas'] )
d_dry_mean, d_dry_std = geo_diff( cost90['Dry Well'] )

# Cholesky decomposoition to correlate initial production and decline rate
corr = np.matrix( [ [1, rho], [rho, 1] ] )
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

# Simulatees drilling cost from end of historic data up to present year
cost_oil = cost[ ( cost['Year']==2006 ) ]['Oil']
cost_gas = cost[ ( cost['Year']==2006 ) ]['Nat. Gas']
cost_dry = cost[ ( cost['Year']==2006 ) ]['Dry Well']
for i in range(2006,year_now):
    cost_oil = ma.exp( rn.normal(d_oil_mean, d_oil_std) + ma.log(cost_oil) )
    cost_gas = ma.exp( rn.normal(d_gas_mean, d_gas_std) + ma.log(cost_gas) )
    cost_dry = ma.exp( rn.normal(d_dry_mean, d_dry_std) + ma.log(cost_dry) )

# Initial costs
cost_acre = rn.normal(12000, 1000) * 960
cost_seis = rn.normal(50, 10) * 43000
cost_0 = cost_acre + cost_seis + cost_oil * oil_well + cost_dry * dry_well
