# -*- coding: utf-8 -*-

"""
This code retrieves the calculation of stock additions in Excel file

The Excel file contains three spreadsheet, as:

    1) sa_all: stock addtions of 43 countries and 5 rest of the world regions
               in tonnes
    2) sa_all_tot: sum of stock addtions (in tonnes), population and
                   stock additions per capita (in tonnes/cap) of 43 countries
                   and 5 rest of the world regions
    3) sa_agg: stock addtions of aggregated regions in tonnes
    4) sa_agg_mat: stock addtions of aggregated regions and
                   material types in tonnes
    5) sa_agg_all: sum of stock addtions (in tonnes), population and
                   stock additions per capita (in tonnes/cap)
                   of aggregated regions
    6) nm_agg: non-metallic minerals stock additions in construction, transport
               and rest of sectors in tonnes
    7) gl_agg: glass stock additions in construction, transport
               and rest of sectors in tonnes
    8) st_agg: steel stock additions in construction, transport
               and rest of sectors in tonnes

Database: EXIOBASE MR-HIOT v.3.3.18.

Software version: Phyton 3.8.3

Created on Wed Oct 23 10:37:04 2019

Updated on Tue Nov 07 19:00 2020

@author: aguilarga
"""

import pandas as pd
import numpy as np
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
    TR = read_csv(path + '\TR_ACT.txt', sep='\t', index_col=[0],
                  header=[0, 1], decimal='.')  # stock for transport matrix
    TR_FD = read_csv(path + '\TR_FD.txt', sep='\t', index_col=[0],
                     header=[0, 1], decimal='.')  # add_stocks for transport FD
    pop = read_csv(path + '\POP.txt', sep='\t', index_col=[0], header=[0],
                   decimal='.')  # population vector
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
    sa_tot = pd.DataFrame(sa_all.sum(1), index=c_code,
                          columns=['Stock additions (tonnes)'])  # summing SA
    sa_all_tot = pd.concat([sa_tot, pop], axis=1, sort=True)  # merging data
    sa_all_tot.insert(2, 'Stock additions per capita (tonnes/cap)',
                      sa_all_tot['Stock additions (tonnes)']/sa_all_tot['Population'], True)  
    # calculating SA per capita and adding new vector

    # STOCK ADDTTIONS (SA) AGGREGATED REGIONS
    sa_agg = region_agg(sa_all)  # aggregating SA per selected country/region
    sa_agg_mat = region_and_mat_agg(sa_all)  # aggregating SA per material type
    sa_agg_tot = region_agg(sa_all_tot)  # aggregating sa_all_tot
    sa_agg_tot['Stock additions per capita (tonnes/cap)'] = (
            sa_agg_tot['Stock additions (tonnes)']/sa_agg_tot['Population'])

    # STOCK ADDITIONS (SA) OF CONSTRUCTION AND TRANSPORT
    # PER COUNTRY AND MATERIAL TYPE

    # NON-METALLIC MINERALS
    emp = []
    for i in c_code:
        df = stock_per_mat_cal('Construction materials and mining waste (excl. unused mining material)',
                               i, SA, SA_FD, TR, TR_FD)
        emp.append(df)
    nm_all = pd.DataFrame(emp, index=c_code,
                          columns=['Construction', 'Transport', 
                                   'hh', 'ngo', 'gov', 'gfc', 'cin', 'civ',
                                   'Rest'])
    # calculating SA of non-metallic minerals per country/region
    nm_agg = region_agg(nm_all)  # aggregating SA non-metallic minerals

    # GLASS
    emp = []
    for i in c_code:
        df = stock_per_mat_cal('Glass', i, SA, SA_FD, TR, TR_FD)
        emp.append(df)
    gl_all = pd.DataFrame(emp, index=c_code,
                          columns=['Construction', 'Transport', 
                                   'hh', 'ngo', 'gov', 'gfc', 'cin', 'civ',
                                   'Rest'])
    # calculating SA of glass per country/region
    gl_agg = region_agg(gl_all)  # aggregating SA of glass
    # STEEL
    emp = []
    for i in c_code:
        df = stock_per_mat_cal('Steel', i, SA, SA_FD, TR, TR_FD)
        emp.append(df)
    st_all = pd.DataFrame(emp, index=c_code,
                          columns=['Construction', 'Transport', 
                                   'hh', 'ngo', 'gov', 'gfc', 'cin', 'civ',
                                   'Rest'])
    # calculating SA of steel per country/region
    st_agg = region_agg(st_all)  # aggregating SA of steel
    return sa_all.T, sa_all_tot.T, sa_agg.T, sa_agg_tot.T, sa_agg_mat.T, nm_agg.T, gl_agg.T, st_agg.T

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

# STOCK ADDITIONS CALCULATION OF A SPECIFIC COUNTRY AND MATERIAL
# IN CONSTRUCTION AND TRANSPORT


def stock_per_mat_cal(m_name, c_name, SA, SA_FD, TR, TR_FD):
    idx = pd.IndexSlice
    tot = (SA.loc[m_name, c_name].sum().sum() +
           SA_FD.loc[m_name, c_name].sum().sum())  # summing all stock_adds
    con = (SA.loc[m_name, idx[c_name, 'Construction (45)']].sum())  # construction stock_adds
    tra = (TR.loc[m_name, c_name].sum().sum() +
           TR_FD.loc[m_name, c_name].sum().sum())  # transport stock_adds
    hh = (SA_FD.loc[m_name, 
                    idx[c_name, 'Final consumption expenditure by households']].sum())
    ngo = (SA_FD.loc[m_name, 
                    idx[c_name, 'Final consumption expenditure by non-profit organisations serving households (NPISH)']].sum())
    gov = (SA_FD.loc[m_name, 
                    idx[c_name, 'Final consumption expenditure by government']].sum())
    gfc = (SA_FD.loc[m_name, 
                    idx[c_name, 'Gross fixed capital formation']].sum())
    cin = (SA_FD.loc[m_name, 
                    idx[c_name, 'Changes in inventories']].sum())
    civ = (SA_FD.loc[m_name, 
                    idx[c_name, 'Changes in valuables']].sum())
    rest = tot - con - tra - (hh + ngo + gov + gfc + cin + civ)
    r = np.array([con, tra, hh, ngo, gov, gfc, cin, civ, rest])
    return r

# AGGREGATION OF SELECTED COUNTRIES/REGIONS


def region_agg(df):
    # CHINA
    cn = pd.DataFrame(df.loc['CN', :])
    cn.columns = ['China']
    # NORTH AMERICA
    na_index = ['US', 'CA']
    na = pd.DataFrame(df.loc[na_index, :].sum(0), columns=['North America'])
    # EUROPEAN REGION
    eu_index = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
                'FR', 'GR', 'HU', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT',
                'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'GB', 'NO', 'CH',
                'WE', 'TR']  # Europe
    eu = pd.DataFrame(df.loc[eu_index, :].sum(0), columns=['Europe'])
    # AUSTRALIA
    au = pd.DataFrame(df.loc['AU', :])
    au.columns = ['Australia']
    # JAPAN
    jp = pd.DataFrame(df.loc['JP', :])
    jp.columns = ['Japan']
    # MIDDLE EAST
    me_index = ['WM']  # Middle East
    me = pd.DataFrame(df.loc[me_index, :].sum(0), columns=['Middle East'])
    # RUSSIA
    ru = pd.DataFrame(df.loc['RU', :])
    ru.columns = ['Russia']
    # LATIN AMERICA
    la_index = ['BR', 'MX', 'WL']  # Latin America
    la = pd.DataFrame(df.loc[la_index, :].sum(0), columns=['Latin America'])
    # ASIA AND PACIFIC
    ap_index = ['KR', 'ID', 'WA']  # Asia and Pacific
    ap = pd.DataFrame(df.loc[ap_index, :].sum(0), columns=['Asia and Pacific'])
    # INDIA
    ind = pd.DataFrame(df.loc['IN', :])
    ind.columns = ['India']
    # AFRICA
    af_index = ['ZA', 'WF']
    af = pd.DataFrame(df.loc[af_index, :].sum(0), columns=['Africa'])
    # DATAFRAME PER REGION
    df_agg = pd.concat([cn, na, eu, au, jp, me, ru, la, ap, ind, af], axis=1)
    df_agg = df_agg.T
    return df_agg

# AGGREGATION OF SELECTED COUNTRIES/REGIONS AND MATERIAL TYPES


def region_and_mat_agg(df):
    df_ = df.T.T
    df_.insert(0, 'Textile/Wood/Paper',
               df_['Textile'] + df_['Wood'] + df_['Paper'], True)
    # grouping textile+wood+paper
    df_.insert(4, 'Aluminium/Lead/Copper and other metals',
               df_['Aluminium'] + df_['Lead'] + df_['Copper'] +
               df_['non-ferrous metals'] + df_['Precious metals'], True)
    # grouping metals
    df_ = df_.drop(['Textile', 'Wood', 'Paper', 'Aluminium', 'Lead', 'Copper',
                   'non-ferrous metals', 'Precious metals'], axis=1)
    # droping groups

    # CHINA
    cn = pd.DataFrame(df_.loc['CN', :])
    cn.columns = ['China']
    # NORTH AMERICA
    na_index = ['US', 'CA']
    na = pd.DataFrame(df_.loc[na_index, :].sum(0), columns=['North America'])
    # EUROPEAN REGION
    eu_index = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
                'FR', 'GR', 'HU', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT',
                'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'GB', 'NO', 'CH',
                'WE', 'TR']  # Europe
    eu = pd.DataFrame(df_.loc[eu_index, :].sum(0), columns=['Europe'])
    # AUSTRALIA
    au = pd.DataFrame(df_.loc['AU', :])
    au.columns = ['Australia']
    # JAPAN
    jp = pd.DataFrame(df_.loc['JP', :])
    jp.columns = ['Japan']
    # MIDDLE EAST
    me_index = ['WM']  # Middle East
    me = pd.DataFrame(df_.loc[me_index, :].sum(0), columns=['Middle East'])
    # RUSSIA
    ru = pd.DataFrame(df_.loc['RU', :])
    ru.columns = ['Russia']
    # LATIN AMERICA
    la_index = ['BR', 'MX', 'WL']  # Latin America
    la = pd.DataFrame(df_.loc[la_index, :].sum(0), columns=['Latin America'])
    # ASIA AND PACIFIC
    ap_index = ['KR', 'ID', 'WA']  # Asia and Pacific
    ap = pd.DataFrame(df_.loc[ap_index, :].sum(0),
                      columns=['Asia and Pacific'])
    # INDIA
    ind = pd.DataFrame(df_.loc['IN', :])
    ind.columns = ['India']
    # AFRICA
    af_index = ['ZA', 'WF']
    af = pd.DataFrame(df_.loc[af_index, :].sum(0), columns=['Africa'])
    # DATAFRAME PER REGION
    df_agg = pd.concat([cn, na, eu, au, jp, me, ru, la, ap, ind, af], axis=1)
    df_agg = df_agg.T
    return df_agg

# SAVE RESULTS FUNCTIONS


def save_result():
    sa_all, sa_all_tot, sa_agg, sa_agg_tot, sa_agg_mat, nm_agg, gl_agg, st_agg  = main()
    writer = ExcelWriter("Data_S1_" +
                         datetime.now().strftime('%Y%m%d') + "all_fd"+ ".xlsx")
    sa_all.to_excel(writer, 'sa_all')
    sa_all_tot.to_excel(writer, 'sa_all_tot')
    sa_agg.to_excel(writer, 'sa_agg')
    sa_agg_tot.to_excel(writer, 'sa_agg_tot')
    sa_agg_mat.to_excel(writer, 'sa_agg_mat')
    nm_agg.to_excel(writer, 'non-metallic')
    gl_agg.to_excel(writer, 'glass')
    st_agg.to_excel(writer, 'steel')
    writer.save()
    return

