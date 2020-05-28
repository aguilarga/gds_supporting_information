# -*- coding: utf-8 -*-

"""
This code retrieves the calculation of steel stock additions used 
as validation in Table S2 from section 2, Appendix, supporting information.
Assesed countries: Australia,Canada, France, Japan, 
                    United Kingdom, and United States  

Database: EXIOBASE MR-HIOT v.3.3.17.

Software version: Phyton 3.7.3

Created on Wed Oct 23 10:37:04 2019

Updated on Wed May 27 14:45 2020

@author: aguilarga
"""

import pandas as pd
import numpy as np
from pandas import read_csv
from pandas import ExcelWriter
from datetime import datetime


# FUNCTIONS

# STOCK ADDITIONS CALCULATION OF A SPECIFIC COUNTRY AND MATERIAL
# IN CONSTRUCTION AND TRANSPORT


def stock_per_mat_cal(m_name, c_name, SA, SA_FD, TR, TR_FD):
    idx = pd.IndexSlice
    tot = (SA.loc[m_name, c_name].sum().sum() +
           SA_FD.loc[m_name, c_name].sum().sum())
    con = (SA.loc[m_name, idx[c_name, 'Construction (45)']].sum())
    tra = (TR.loc[m_name, c_name].sum().sum() +
           TR_FD.loc[m_name, c_name].sum().sum())
    fd = SA_FD.loc[m_name, c_name].sum().sum()
    rest = tot - con - tra - fd
    r = np.array([con, tra, fd, rest])
    return r

# AGGREGATION OF SELECTED COUNTRIES/REGIONS

def reg_agg(df):  
    # AUSTRALIA
    au = pd.DataFrame(df.loc['AU', :])
    au.columns = ['Australia']
    # CANADA
    ca = pd.DataFrame(df.loc['CA', :])
    ca.columns = ['Canada']
    # FRANCE
    fr = pd.DataFrame(df.loc['FR', :])
    fr.columns = ['France']
    # JAPAN
    jp = pd.DataFrame(df.loc['JP', :])
    jp.columns = ['Japan']
    # UNITED KINGDOM
    uk = pd.DataFrame(df.loc['GB', :])
    uk.columns = ['United Kingdom']
    # UNITED STATES
    us = pd.DataFrame(df.loc['US', :])
    us.columns = ['United States']
    # DATAFRAME PER REGION
    df_agg = pd.concat([au, ca, fr, jp, uk, us], axis=1)
    df_agg = df_agg.T
    return df_agg

# CALCULATION

path = 'EXIOBASE_3.3.17_hsut_2011'
SA = read_csv(path + '\SA_ACT.txt', sep='\t', index_col=[0, 1],
              header=[0, 1], decimal=',')  # stock additions matrix
SA_FD = read_csv(path + '\SA_FD.txt', sep='\t', index_col=[0, 1],
                 header=[0, 1], decimal=',')  # add_stocks from FD
TR = read_csv(path + '\TR_ACT.txt', sep='\t', index_col=[0, 1],
              header=[0, 1], decimal='.')  # stock for transport matrix
TR_FD = read_csv(path + '\TR_FD.txt', sep='\t', index_col=[0, 1],
                 header=[0, 1], decimal='.')  # add_stocks for transport FD
# INDICES AND LABELS
c_code = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
          'FR', 'GR', 'HU', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT',
          'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'GB', 'NO', 'CH',
          'WE', 'TR', 'US', 'CA', 'CN', 'RU', 'IN', 'AU', 'JP', 'ZA',
          'WF', 'WM', 'BR', 'MX', 'WL', 'KR', 'ID', 'WA']  # country codes
    
# STOCK ADDITIONS (SA) OF CONSTRUCTION AND TRANSPORT
# STEEL
emp = []
for i in c_code:
    df = stock_per_mat_cal('Steel', i, SA, SA_FD, TR, TR_FD)
    emp.append(df)
st_all = pd.DataFrame(emp, index=c_code,
                      columns=['Construction', 'Transport', 'Final Demand',
                               'Rest'])
# calculating SA of steel per country/region
st_agg = reg_agg(st_all)  # aggregating SA of steel

# SAVE RESULTS FUNCTIONS

writer = ExcelWriter("country_validation_" + 
                     datetime.now().strftime('%Y%m%d') + ".xlsx")
st_agg.to_excel(writer, 'steel')
writer.save()

