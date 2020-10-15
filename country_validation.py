# -*- coding: utf-8 -*-

"""
This code retrieves the calculation of steel stock additions used 
as validation in Table S2 from section 2, Appendix, supporting information.
Assesed countries: Australia,Canada, France, Japan, 
                    United Kingdom, and United States  

Database: EXIOBASE MR-HIOT v.3.3.18.

Software version: Phyton 3.7.3

Created on Wed Oct 23 10:37:04 2019

Updated on Wed Oct 14 14:45 2020

@author: aguilarga
"""

import pandas as pd
from pandas import read_csv
from pandas import ExcelWriter
from datetime import datetime


def main():
    # SETTINGS
    path = 'EXIOBASE_3.3.18_hsut_2011'
    SA = read_csv(path + '\SA_ACT.txt', sep='\t', index_col=[0],
                  header=[0, 1], decimal='.')  # stock additions matrix
    SA_FD = read_csv(path + '\SA_FD.txt', sep='\t', index_col=[0],
                     header=[0, 1], decimal='.')  # add_stocks from FD
    SD = read_csv(path + '\SD.txt', sep='\t', index_col=[0], header=[0, 1],
                   decimal='.')  # stock depletion/removal matrix
    # INDICES AND LABELS
    c_code = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
              'FR', 'GR', 'HU', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT',
              'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'GB', 'NO', 'CH',
              'WE', 'TR', 'US', 'CA', 'CN', 'RU', 'IN', 'AU', 'JP', 'ZA',
              'WF', 'WM', 'BR', 'MX', 'WL', 'KR', 'ID', 'WA']  # country codes
    m_lab = ['Textile', 'Wood', 'Paper',
             'Plastics', 'Glass', 'Steel', 'Precious metals',
             'Aluminium', 'Lead', 'Copper', 'non-ferrous metals',
             'Non-metallic minerals']  # material labels
    # STOCK ADDITTIONS (SA) PER COUNTRY/REGION
    emp = []
    for i in c_code:
        df = stock_add_cal(i, SA, SA_FD)
        emp.append(df)
    sa_all = pd.DataFrame(emp, index=c_code, columns=m_lab)  # calculating SA
    # STOCK DEPLETION/REMOVALS (SD) PER COUNTRY/REGION
    emp2 = []
    for i in c_code:
        df2 = stock_rem_cal(i, SD)
        emp2.append(df2)
    sd_all = pd.DataFrame(emp2)
    sd_all = pd.DataFrame(emp2, index=c_code, columns=m_lab)  # calculating SA
    return sa_all.T, sd_all.T

# FUNCTIONS

# STOCK ADDITIONS CALCULATION OF A SPECIFIC COUNTRY


def stock_add_cal(c_name, SA, SA_FD):
    # INDEX
    m_ind = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]  # material indices
    # CALCULATING STOCK ADDITIONS PER COUNTRY
    SA = SA.iloc[m_ind, :]  # selecting materials in intermediate matrix
    SA_FD = SA_FD.iloc[m_ind, :]  # selecting materials in final demand matrix
    sa = (SA.loc[:, c_name].sum(1) + SA_FD.loc[:, c_name].sum(1)).to_numpy()
    # summing stock additions in country c_name as numpy array
    return sa

def stock_rem_cal(c_name, SD):
    # INDEX
    m_ind = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]  # material indices
    # CALCULATING STOCK ADDITIONS PER COUNTRY
    sd_ = SD.iloc[m_ind, 3::6]  # selecting stock depletion/removal per country
    sd = sd_.loc[:, c_name].sum(1).T.to_numpy()
    return sd


# SAVE RESULTS FUNCTIONS
sa_all, sd_all =main()
writer = ExcelWriter("Data_validation_" + 
                     datetime.now().strftime('%Y%m%d') + ".xlsx")
sa_all.to_excel(writer, 'sa_all')
sd_all.to_excel(writer, 'sd_all')
writer.save()

