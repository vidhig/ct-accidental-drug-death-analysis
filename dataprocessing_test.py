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

import unittest
import pandas as pd
from dataprocessing import PreProcess

class TestPreProcess(unittest.TestCase):
    
    def test_is_date_col_converted_to_date_type(self):
        pre_process = PreProcess() ## create object
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_date_columns(dataframe) ## method call to get actual value
        
        expected_date_col_type = 'datetime64[ns]'
        
        ## assertion
        self.assertEqual(expected_date_col_type, str(processed_df.Date.dtypes), msg = 'Date column did not convert to Date type')
        
    def test_is_date_reported_col_inserted_into_dataframe(self):
        pre_process = PreProcess() ## create object
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_date_columns(dataframe) ## method call to get actual value

        expected_col = 'DateReported'
        
        ## assertion
        self.assertIn(expected_col, processed_df.columns.tolist(), msg = '{} column did not get inserted into the dataframe'.format(expected_col))
        
    def test_is_date_of_death_col_inserted_into_dataframe(self):
        pre_process = PreProcess() ## create object
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_date_columns(dataframe) ## method call to get actual value

        expected_col = 'DateOfDeath'
        
        ## assertion
        self.assertIn(expected_col, processed_df.columns.tolist(), msg = '{} column did not get inserted into the dataframe'.format(expected_col))
        
    def test_remove_na_from_drug_cols(self):
        pre_process = PreProcess() ## create object
        drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid']
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_all_drug_columns(dataframe, drugs) ## method call to get actual value

        expected_count_of_na_values = 0
        
        ## assertion
        self.assertEqual(expected_count_of_na_values, processed_df[drugs].isna().any().sum(), msg = 'Drug columns still have NA values')
        
    def test_is_latitude_longitude_extracted_to_separate_cols(self):
        pre_process = PreProcess() ## create object
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_geographic_data(dataframe) ## method call to get actual value
        
        expected_cols = ['DeathCity_Latitude', 'DeathCity_Longitude', 'ResidenceCity_Latitude', 'ResidenceCity_Longitude', 'InjuryCity_Latitude', 'InjuryCity_Longitude', 'DeathCounty_Latitude', 'DeathCounty_Longitude']
        
        ## assertion
        self.assertTrue(all(col in processed_df.columns.tolist() for col in expected_cols), msg = 'Not all latitude and longitude columns have been extracted')
        
    def test_remove_na_from_death_county(self):
        pre_process = PreProcess() ## create object
        dataframe = pd.read_csv('test-dataset.csv') ## load test-dataset (contains only 20 rows)
        
        processed_df = pre_process.clean_geographic_data(dataframe) ## method call to get actual value
        
        expected_count_of_na_values = 0

        ## assertion
        self.assertEqual(expected_count_of_na_values, processed_df['DeathCounty'].isna().any().sum(), msg = 'DeathCounty column still has NA values')

if __name__ == '__main__':
    unittest.main()
