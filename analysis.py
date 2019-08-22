#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################
##  Activity: CS5010 - Project
##  Name:
##      Dibyendu Roy Chowdhury - drc2qw
##      Saad Saleem - ss3vy
##      Sneha Choudhary - sc4xc
##      Vidhi Gupta - vg5vc
###############################################

import maprenderer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def drug_usage_analysis(drug_usage_df):
        
    drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid'] ## Drugs present in the dataset

    plot_number_of_deaths_in_past_7_years_per_drug(drug_usage_df, drugs)
    plot_number_of_deaths_per_year_per_drug(drug_usage_df, drugs)
    plot_death_count_by_drug_class_per_year(drug_usage_df, drugs)
    
    
    county_columns = ['DeathCounty', 'DeathCounty_Latitude', 'DeathCounty_Longitude']
    df_per_county = drug_usage_df[county_columns + drugs].groupby(county_columns).sum() ## frame dataframe of deaths per county per drug
    df_per_county['TotalCount'] = df_per_county[drugs].sum(axis = 1) ## add new col to sum up total number of deaths per county
    df_per_county.reset_index(inplace=True)
    
    county_map = maprenderer.county_wise_drug_death_count_connecticut(df_per_county) ## create map for deaths per county
    county_map.save('{}/photo-counties.html'.format(image_path)) ## save html map
    return county_map

def plot_death_count_by_drug_class_per_year(drug_usage_df, drugs):
    drug_opioid_lst = ['Heroin', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Hydrocodone', 'Methadone', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid'] ## type of opioids
    drug_stimulant_list = ['Cocaine', 'Amphet'] ## type of stmiulants
    sum_opioid = drug_usage_df[drug_opioid_lst].sum(axis = 1)
    sum_stimulant = drug_usage_df[drug_stimulant_list].sum(axis = 1)
    
    drug_usage_df['Opioids'] = [1 if x > 0 else 0 for x in sum_opioid]
    drug_usage_df['Stimulants'] = [1 if x > 0 else 0 for x in sum_stimulant]
    drug_usage_df['Year'] = drug_usage_df['Date'].dt.year.astype('Int64')
    
    ## Benzodiazepine and Ethanol represent a class of drugs in itself
    drug_usage_df_new = drug_usage_df[['Year', 'Opioids', 'Stimulants', 'Benzodiazepine', 'Ethanol']].groupby(['Year']).sum()
    drug_usage_df_new.rename(columns={'Benzodiazepine':'Benzodiazepines', 'Ethanol': 'Alcohol'}, inplace=True) ## rename columns
    
    A = drug_usage_df_new['Opioids']
    B = drug_usage_df_new['Stimulants']
    C = drug_usage_df_new['Benzodiazepines']
    D = drug_usage_df_new['Alcohol']
    
    ## create stacked barchart
    plt.title('Number of deaths year wise based on Drug Class')
    plt.bar(drug_usage_df_new.index.tolist(), A, color = 'maroon', edgecolor='black', width = 0.5)
    plt.bar(drug_usage_df_new.index.tolist(), B, color = 'indianred', edgecolor='black', bottom = A, width = 0.5)
    plt.bar(drug_usage_df_new.index.tolist(), C, color = 'coral', edgecolor='black', bottom = A + B, width = 0.5)
    plt.bar(drug_usage_df_new.index.tolist(), D, color = 'sandybrown', edgecolor='black', bottom = A + B + C, width = 0.5)
    plt.legend(['Opioids', 'Stimulants', 'Benzodiazepines', 'Alcohol'],loc=2, prop={'size': 8})
    plt.savefig('{}/death-count-by-drug-class.jpeg'.format(image_path))
    plt.show()      
    
def plot_number_of_deaths_in_past_7_years_per_drug(drug_usage_df, drugs):
    accidents_per_drug = drug_usage_df[drugs].sum()
    accidents_per_drug = accidents_per_drug.sort_values()
    ax = accidents_per_drug.plot(kind='barh', title ="Accidental Death Count in the past 7 years per drug", fontsize=14, figsize = (20,10), stacked=True, color = cm.inferno_r(np.linspace(0.3, 0.6, 30)))
    ax.set_xlabel("Drugs", fontsize=14)
    ax.set_ylabel("Number of Accidental Deaths", fontsize=14)
    for index, value in enumerate(accidents_per_drug):
        x_index = value+2
        y_index = index-0.08
        ax.text(x_index, y_index, str(value), fontweight='bold', fontsize=14)
    ax.get_figure().savefig('{}/death-count-per-drug-over-seven-years.jpeg'.format(image_path))
    plt.show()
    
def plot_number_of_deaths_per_year_per_drug(drug_usage_df, drugs):
    drug_usage_df['Year'] = drug_usage_df['Date'].dt.year.astype('Int64') ## extract year
    drug_usage_per_year = drug_usage_df[drugs + ['Year']].groupby(['Year']).sum() ## sum of number of deaths per year
    
    ## create bar chart
    ax = drug_usage_per_year.plot(kind = 'bar', legend = True, figsize = (20,10), width = 1, fontsize=14)
    ax.set_xlabel("Years", fontsize=14)
    ax.set_ylabel("Number of Accidental Deaths", fontsize=14)
    plt.grid(True)
    ax.get_figure().savefig('{}/death-count-per-drug-per-year.jpeg'.format(image_path))
    plt.show()

filename = 'dataset-revised.csv'
image_path = 'static/images'
drug_usage_df = pd.read_csv(filename, parse_dates = ['Date', 'DateReported', 'DateOfDeath']) ## Load the dataset
drug_usage_analysis(drug_usage_df)

