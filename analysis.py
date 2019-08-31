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
import seaborn as sns
from matplotlib import cm
from wordcloud import WordCloud,STOPWORDS

def generate_word_cloud(data, title='wordcloud'):
    wordcloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          scale= 3,
                          random_state = 1
                         ).generate(str(data)) ## generate wordcloud
    plt.figure(1, figsize=(20,10))
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.savefig('{}/{}.jpeg'.format(image_path, title)) ## save wordcloud
    plt.show() ## show image

def drug_usage_analysis(drug_usage_df):
    
    generate_word_cloud(drug_usage_df['COD'].dropna(), 'cod-wordcloud') ## wordcloud for cause of death
    generate_word_cloud(drug_usage_df['DeathCity'].dropna(), 'cities-wordcloud') ## world cloud for cities having drug overdose incidents
        
    drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid'] ## Drugs present in the dataset

    plot_number_of_deaths_in_past_7_years_per_drug(drug_usage_df, drugs)
    plot_number_of_deaths_per_year_per_drug(drug_usage_df, drugs)
    plot_death_count_by_drug_class_per_year(drug_usage_df, drugs)
    plot_number_of_deaths_against_sex(drug_usage_df)
    plot_number_of_deaths_against_race(drug_usage_df)
    plot_death_by_age(drug_usage_df)
    plot_death_by_age_race(drug_usage_df)
    
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
    
def plot_number_of_deaths_against_sex(drug_usage_df):
    #Creating pie chart with male/female proportion

    # sum the instances of males and females
    males = (drug_usage_df['Sex'] == 'Male').sum()
    females = (drug_usage_df['Sex'] == 'Female').sum()
    
    # put them into a list called proportions
    proportions = [males, females]
    
    # Create a pie chart
    plt.pie(
        # using proportions
        proportions,
        # with the labels being officer names
        labels = ['Male', 'Female'],
        # with no shadows
        shadow = False,
        # with colors
        colors = ['green','red'],
        # with one slide exploded out
        explode = (0.15 , 0),
        # with the start angle at 90%
        startangle = 90,
        # with the percent listed as a fraction
        autopct = '%1.1f%%'
    )

    # View the plot drop above
    plt.axis('equal')
    
    # Set labels
    plt.title("Sex Proportion")
    
    # View the plot
    plt.tight_layout()
    plt.savefig('{}/death-count-against-sex.jpeg'.format(image_path))
    plt.show()
    
def plot_number_of_deaths_against_race(drug_usage_df):
    race_count = drug_usage_df['Race'].value_counts() ## extract number of deaths by race
    
    ## create bar plot 
    plt.figure(figsize=(20,10))
    sns.barplot(y=race_count.index, x=race_count.values)
    plt.savefig('{}/death-count-race-wise.jpeg'.format(image_path))
    plt.show()
    
def plot_death_by_age(drug_usage_df):
    df_new = drug_usage_df.drop([2195]) ## remove row with no age
    plt.figure(figsize=(20,10))
    bins = [0, 18, 25, 45, 65, 100] ## age group bins
    
    df_new['AgeGroup'] = pd.cut(df_new['Age'], bins) ## add AgeGroup col
    
    ## create bar chart age group wise
    sns.set_style("whitegrid")
    plt.title('Death Count Associtated with Age Groups', fontsize=30, fontweight='bold', y=1.05,)
    plt.xlabel('AgeGroup', fontsize=25)
    plt.ylabel('Count', fontsize=25)
    ax = sns.countplot(x="AgeGroup", data=df_new, palette="hls")
    for p in ax.patches:
        ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.35, p.get_height()+10))
    plt.savefig('{}/death-by-age.jpeg'.format(image_path))
    plt.show()
    
def plot_death_by_age_race(drug_usage_df):
    df_new = drug_usage_df.drop([2195]) ## remove row with no age
    df_new = df_new.rename(index={'Unknown':'Other'})
    
    ## create violin plot for number of deaths based on gender and race
    plt.figure(figsize=(20,10))
    sns.violinplot(x="Race", y="Age", hue="Sex", data=df_new, palette="Set2", split=True, scale="count", inner="stick")
    plt.savefig('{}/death-by-age-race.jpeg'.format(image_path))
    plt.show()
    
def plot_age_race(drug_usage_df):
    df_new = drug_usage_df.drop([2195]) ## remove row with no age
    df_new = df_new.rename(index={'Unknown':'Other'})
    ordered_days = df_new.Race.value_counts().index
    g = sns.FacetGrid(df_new, row="Race", row_order=ordered_days,
                      height=2, aspect=5,)
    g.map(sns.distplot, "Age", hist=False, rug=True)
    plt.savefig('{}/plot-age-race.jpeg'.format(image_path))
    plt.show()

filename = 'dataset-revised.csv'
image_path = 'static/images'
drug_usage_df = pd.read_csv(filename, parse_dates = ['Date', 'DateReported', 'DateOfDeath']) ## Load the dataset
drug_usage_analysis(drug_usage_df)

