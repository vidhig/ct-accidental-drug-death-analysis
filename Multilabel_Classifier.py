#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%matplotlib notebook
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler    
    
#===== Data Modelling =====

class DataModelling: 
        
    def data_for_model(self,df):
        
        #This section will merge drug columns containing Opioid
        
        drug_opioid_lst = ['Heroin', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Hydrocodone', 'Benzodiazepine', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS', 'AnyOpioid'] # List of drugs which contain opioids

        sum_opioid = df[drug_opioid_lst].sum(axis = 1)            
        df['Opioids'] = [1 if x > 0 else 0 for x in sum_opioid]
        
        # Creating a new column named 'year' from Date of death column  
        df['Date'] = pd.to_datetime(df['Date'])
        df['year'] = df['Date'].dt.year
        df = df[~df['year'].isnull()]
        df['year'] = df['year'].apply(np.int64)
        
        # Creating a new category in 'Race' named Mixed when the number of types of Race for a given person is more than 1. Example, Hispanic & Black
        df['Race'] = df['Race'].astype(str).replace('nan', '')
        df_new_race = []
        for i in df['Race']:
            i = i.split(',')
            if(len(i)>1):
                df_new_race.append('Mixed')
            else:
                df_new_race.append(i[0])
                
        df['new_race'] = df_new_race
        df.drop(['Race'], inplace= True, axis =1)
        df.info()
        
        # Dropping off columns which are not in form of Interger or of type Object, to refine the dataset which goes into the model
        df_model = df.drop(['Unnamed: 0','ID','Date','DateType','DateReported','DateOfDeath','ResidenceCity','ResidenceCounty','ResidenceState','DeathCity','DeathCounty','LocationifOther','DescriptionofInjury','InjuryPlace','InjuryCity','InjuryCounty','InjuryState','COD','OtherSignifican','Other','ResidenceCityGeo','InjuryCityGeo','DeathCityGeo'],axis =1)
    
        numeric_columns = ['DeathCounty_Latitude','DeathCounty_Longitude','DeathCity_Latitude','DeathCity_Longitude','ResidenceCity_Latitude','ResidenceCity_Longitude','InjuryCity_Latitude','InjuryCity_Longitude']
        for col in numeric_columns:
            df_model[col] = df_model[col].apply(pd.to_numeric)
        
        df_model = df_model.dropna() # Dropping of rows which contain NA values
        df_model.head()
        df_model.info()
        
        
        # Creating Dummy variables for categorical variables 
        categorical_feature_mask = df_model.dtypes==object
        # filter categorical columns using mask and turn it into a list
        categorical_cols = df_model.columns[categorical_feature_mask].tolist()
        
        df_model_dummies = pd.get_dummies(df_model[categorical_cols],drop_first=True)
        
        df_model.info()
        
        df_model = pd.concat([df_model, df_model_dummies], axis=1)
        df_model.info()
        
        for col in categorical_cols:
            df_model.drop([col], axis = 1, inplace=True)
        df_model.info()
        df_cols = df_model.columns.tolist()
        df_cols.remove('Age')
        df_cols.append('Age')
        df_model = df_model[df_cols]
        df_model.info()
        #df_model.to_csv('final_model.csv')
        return df_model  # Returning refined Dataset which can be readily applied to the model

#==== Creating Training and Testing dataset

    def training(self,df_model):
        
        # Configuring Input and Output Variables of the model 
        X = df_model.iloc[:,17:]
        X.drop(['Opioids'], inplace= True, axis =1)
        X.info()
        y = df_model[['Opioids','Cocaine','Ethanol']] 
        y.info()
    
        ss = StandardScaler()
        x = ss.fit_transform(X)
    
        X_new = pd.DataFrame(data = x)
        X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.2, random_state = 10)
    
        X_train.info()
        y_train.info()
    
        train_x = X_train
        test_x = X_test
        training_accuracy =[]
        testing_accuracy = []
        # Initiating Random forest classifier for modelling
        clf = RandomForestClassifier(n_estimators = 200, max_depth= 13)
        clf.fit(train_x, y_train)  
        
        print("Training Accuracy is "+ str(clf.score(train_x, y_train)))
        print("Testing Accuracy is "+str(clf.score(test_x, y_test)))
            
        feature = list(map(lambda x:round (x,3), clf.feature_importances_))
        list_columns = X.columns.tolist()
        feature_score = list(zip(list_columns, feature))
        feature_score = sorted(feature_score, key = lambda x: (x[1]))
        return training_accuracy, testing_accuracy, feature_score
    

df = pd.read_csv('dataset-revised.csv',parse_dates=True)
df.info()
data_modelling = DataModelling()
new_df = data_modelling.data_for_model(df)
Train_acc, Test_acc, feature_imp = data_modelling.training(new_df)







