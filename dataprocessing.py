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

import numpy as np
import pandas as pd
import json

## Represents the collection of methods that clean data
class PreProcess:
    ## Pre process the Date and DateType column to extract 2 new columns
    ## one for DateReported date type and another for DateOfDeath date type
    def clean_date_columns(self, dataframe):
        columns = dataframe.columns.tolist() ## Extract all column names
        
        ## Convert date column to type datetime
        dataframe['Date'] = pd.to_datetime(dataframe['Date'], format = '%m/%d/%y %H:%M') 
        
        if 'DateReported' not in columns:
            ## Add the DateReported column based on DateType field
            dataframe['DateReported'] = np.where(dataframe['DateType'] == 'DateReported', dataframe['Date'], np.datetime64('NaT'))
            ## Insert the column after DateType column
            columns.insert(columns.index('DateType')+1, 'DateReported')
            
        if 'DateOfDeath' not in columns:
            ## Add the DateOfDeath column based on DateType field
            dataframe['DateOfDeath'] = np.where(dataframe['DateType'] == 'DateofDeath', dataframe['Date'], np.datetime64('NaT')) 
            ## Insert the column after DateReported column
            columns.insert(columns.index('DateType')+2, 'DateOfDeath')
            
        dataframe = dataframe[columns] ## Update columns in dataframe
        return dataframe
    
    ## Data preprocessing function to fill in NaN values with zeros for drugs not involved
    ## and replace the Y marker with 1 to indicate true
    def clean_all_drug_columns(self, dataframe, drugs):
        ## Iterate through the list of drug columns
        for drug in drugs:
            non_null = dataframe[drug].notnull() 
            dataframe.loc[non_null, drug] = 1
            dataframe[drug].fillna(0, inplace = True) ## replace NA with 0
            dataframe[drug] = dataframe[drug].replace( 'Y', 1) ## replace Y with 1
        return dataframe
    
    ## Pre process the DeathCityGeo, ResidenceCityGeo and InjuryCityGeo columns to extract latitude and longitude info
    ## and update DeathCounty NA values based on the DeathCity
    def clean_geographic_data(self, dataframe):
        ## Load JSON file that contains a mapping of counties to their latitude, longitude and cities in the county
        ## {'county-name': {'latitude': <>, 'longitude': <>, 'cities': []}}
        with open('counties-town-mapping.json') as f:
            counties = json.load(f)
    
        ## Iterate through the rows
        for index, row in dataframe.iterrows():
            ## continue if DeathCounty is already populated
            if str(row['DeathCounty']).upper() != 'NAN':
                continue
            city = str(row['DeathCity']).upper() ## extract city name
            for county, details in counties.items():
                if city in details['cities']:
                    dataframe.at[index, 'DeathCounty'] = county ## update DeathCounty when city found
                    break
                
        ## Populate DeathCounty latitude and longitude using the JSON data from counties
        dataframe['DeathCounty_Latitude'] = dataframe['DeathCounty'].map(lambda county: counties[county]['latitude'])
        dataframe['DeathCounty_Longitude'] = dataframe['DeathCounty'].map(lambda county: counties[county]['longitude'])
        
        ## Extract the latitude and longitude values from DeathCityGeo, ResidenceCityGeo and InjuryCityGeo
        dataframe['DeathCity_Latitude'], dataframe['DeathCity_Longitude'] = self.__extract_coordinates(dataframe['DeathCityGeo'])
        dataframe['ResidenceCity_Latitude'], dataframe['ResidenceCity_Longitude'] = self.__extract_coordinates(dataframe['ResidenceCityGeo'])
        dataframe['InjuryCity_Latitude'], dataframe['InjuryCity_Longitude'] = self.__extract_coordinates(dataframe['InjuryCityGeo'])
        
        return dataframe

    ## Extract coordinates from the column and frame the list
    def __extract_coordinates(self, geo_location_col):
        latitudes = []
        longitudes = []
        geo_location_col = geo_location_col.fillna("")
        for geo_loc in geo_location_col:
            if geo_loc == "":
                latitudes.append("")
                longitudes.append("")
            else:
                latitudes.append(geo_loc.split('\n')[1].replace('(','').split(',')[0])
                longitudes.append(geo_loc.split('\n')[1].replace(')','').split(',')[1])
        
        return latitudes, longitudes


filename = 'dataset.csv'
drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid']
drug_usage_df = pd.read_csv(filename) ## Load the dataset
pre_process = PreProcess()
drug_usage_df = pre_process.clean_date_columns(drug_usage_df) 
drug_usage_df = pre_process.clean_all_drug_columns(drug_usage_df, drugs)
drug_usage_df = pre_process.clean_geographic_data(drug_usage_df)
drug_usage_df.to_csv('dataset-revised.csv')