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

import folium
import json
#from dataprocessing import *

def county_wise_drug_death_count_connecticut(df_per_county):
    state_coordinates = [41.60, -73.0877]
    
    ## Load geojson on the counties of connecticut
    with open('ct-counties-json.geojson') as f:
        geodata = json.load(f)

    ## load connecticut map
    map_county = folium.Map(location=state_coordinates, zoom_start = 9)
    
    ## 0%, 25%, 50%, 75%, 100% => quantile ranges representing the bin for the graph color coding
    bins = list(df_per_county['TotalCount'].quantile([0, 0.25, 0.5, 0.75, 1]))
    
    for index, row in df_per_county.iterrows():
        ## extract location coordinates
        location = [str(row['DeathCounty_Latitude']), str(row['DeathCounty_Longitude'])]
        ## add county-name: number-of-deaths-in-county popup
        tooltip = (str(row['DeathCounty']) + ': ' + str(row['TotalCount']))
        icon = folium.Icon(color = 'black', icon = 'remove-circle') ## update location marker icon
        marker = folium.Marker(location = location, tooltip = tooltip, icon = icon) ## create location marker
        marker.add_to(map_county) ## add location marker to map
        
    ## create choropleth map using the dataset and add to map
    folium.Choropleth(
        name='choropleth',
        geo_data=geodata,
        data=df_per_county,
        columns=['DeathCounty', 'TotalCount'],
        key_on='feature.properties.name',
        fill_color='OrRd',
        fill_opacity=0.3,
        line_weight=2,
        bins=bins,
        legend_name='Accidental Drug Death Count in the past 7 years',
        reset = True,
        highlight=True
    ).add_to(map_county)
    
    
    folium.LayerControl().add_to(map_county)
    return map_county
    
#drug_usage_df = pd.read_csv('dataset-revised.csv') ## Load the dataset
#drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid']
#df_per_county = extract_df_per_county_per_drug(drug_usage_df, drugs)
#map_county = county_wise_drug_death_count_connecticut(df_per_county)