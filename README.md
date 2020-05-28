[![DOI](https://zenodo.org/badge/252446314.svg)](https://zenodo.org/badge/latestdoi/252446314)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# gds_supporting_information
This repository corresponds to supplemetary information of the paper 'Global distribution of material inflows to capital formation and its implications for a circularity transition'

## EXIOBASE_3.3.17_hsut_2011 folder.
It includes:	
* Materials accumulated at the end of the period by activities ('SA_ACT.txt')	
* Materials accumulated at the end of the period by final demand categories	('SA_FD.txt')
* Materials accumulated for transport equiment at the end of the period by activities ('TR_ACT.txt')	
* Materials accumulated for transport equiment at the end of the period by final demand categories ('TR_FD.txt')	
* Population per country/region from World Bank database ('POP.txt')
* Classfications used in EXIOBASE v3.3.17	('Classifications.xlsx')

***Note on the approach***: by-product technology assumption (Stone's method) is applied. Inputs of products to activities/final consumers includes only products that are produced as principal productions.

## main.py
It includes all functions for calculating results of 'Global distribution of material inflows to capital formation 
and its implications for a circularity transition' 

## country_validation.py
It retrieves results for country validation in Table S2, Section 2, ***Appendix.docx***

## Data_S1.xls 
Results from ***main.py*** by running ***save_result()*** function

## Data_S2.xls
Results from ***main.py*** grouped by income category. This Excel file was created from ***Data_S1.xls***, and imported to Tableau for creating global map   

## Data_S3.xls  
It includes countries, regions and income classification of EXIOBASE matching World Bank groups

## Appendix.docx
It includes procedure for importing data from EXIOBASE website (http://www.exiobase.eu/), constructing the figures, and a comparison between the paper's results and previous studies.
