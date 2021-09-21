#####################################################################################################
###################################### FOOTBALL PLAYER RECOMMENDER ##################################
#####################################################################################################

#####################################################################################################
# Libraries
#####################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#####################################################################################################
# Getting Data
#####################################################################################################

data = pd.read_excel("Ders Notları/Career Mode player datasets - FIFA 15-21.xlsx")
df = data.copy()

#####################################################################################################
# Analyze the Dataset
#####################################################################################################

def df_summary(df):
    print("############### OBSERVATIONS-COLUMNS COUNTS ###############")
    print("\n")
    print(df.shape)
    print("############### INDEX ###############")
    print("\n")
    print(df.index)
    print("############### COLUMNS ###############")
    print("\n")
    print(df.columns)
    print("############### DATAFRAME INFORMATIONS ###############")
    print("\n")
    print(df.info())
    print("############### DATAFRAME INFORMATIONS ###############")
    print("\n")
    print(df.describe().T)

df_summary(df)

def missing_value_analysis(df):
    print("Is there any missing value on the dataset?")
    print(df.isnull().values.any())
    missing = df.isnull().values.any()

    if (missing == True):
        print("############### MISSING VALUE COUNTS BY VARIABLES ###############")
        print(df.isnull().sum())
        print("############### TOTAL MISSING VALUE COUNTS ###############")
        print(df.isnull().sum().sum())
    else:
        pass

missing_value_analysis(df)

#####################################################################################################
# Preprocessing
#####################################################################################################

def preprocessor(df):
  new_df = df.copy()
  drop_df = ["ls", "st", "rs","lw", "lf", "cf", "rf", "rw", "lam", "cam", "ram", "lm", "lcm", "cm", "rcm", "rm",
            "lwb", "ldm", "cdm","rdm","rwb","lb","lcb","cb","rcb","rb","team_jersey_number","loaned_from","joined",
            "contract_valid_until","nation_position","nation_jersey_number","player_tags","real_face","body_type",
            "wage_eur", "player_positions","league_name", "nationality","dob","player_url", "sofifa_id","long_name",
            "club_name", "value_eur", "work_rate", "release_clause_eur","team_position"]

  new_df.drop(drop_df, axis = 1, inplace = True)

  new_df["player_traits"] = new_df["player_traits"].apply(lambda x: str(x).count(",") + 1 if len(str(x)) != 0 else 0)
  new_df["player_traits"].head(30)

  new_df["preferred_foot"] = [2 if i == "Left" else 1 for i in new_df["preferred_foot"]]

  scaler = MinMaxScaler(feature_range=(0, 1))
  scaler.fit(new_df[["age", "height_cm", "weight_kg"]])
  new_df[["age", "height_cm", "weight_kg"]] = scaler.transform(new_df[["age", "height_cm", "weight_kg"]])
  return new_df

new_df = preprocessor(df)

#####################################################################################################
# Creating the Correlation Matrix
#####################################################################################################

new_df.index = new_df["short_name"]
new_df.drop("short_name", axis = 1, inplace = True)
new_df = new_df.T
new_df.head(2) # For controlling whether the process works or not

#####################################################################################################
# Setting Recommender System
#####################################################################################################

## For easy to make searching, there is a function you can benefit

def player_search(df, name = "Messi"):
  print(df.columns[df.columns.str.contains(name)])

player_search(new_df, name = "Potuk")

def player_recommender(new_df, df, budget = 10000000000000, rec_count = 6):
  player_name = input("Please enter a player name who is matching the skillset you are searching for = ")
  player_name = new_df[player_name]


  corr_df = new_df.corrwith(player_name).sort_values(ascending = False)
  corr_df = corr_df.reset_index()
  corr_df.rename(columns = {0: "corr_value"}, inplace = True)
  final_df = corr_df.merge(df[["short_name", "value_eur"]], on = "short_name", how = "inner")
  return final_df[final_df["value_eur"] < budget].sort_values(by = "corr_value", ascending = False).iloc[1:rec_count]


player_recommender(new_df, df, budget = 400000, rec_count = 10)