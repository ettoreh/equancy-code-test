# test.py

import pandas as pd
import numpy as np



# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------

def observation_number(df: pd.DataFrame) -> str:
    return "Il y a %d observations dans ce dataset." %df.shape[0]


def missing_values(df:pd.DataFrame) -> str:
    if df.isnull().sum().sum()==0:
        phrase = "Il n'y a pas de valeur manquantes dans ce dataset."
    else:
        phrase = "Il y a:\n"        
        for value in pd.DataFrame(df.isnull().sum()).itertuples():
            if value._1!=0:
                phrase += "%d valeur manquantes" %value._1
                phrase += "dans la colonne '%s'\n" %value.Index
    return phrase


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def experience_missing_value_imputation(df: pd.DataFrame) -> pd.DataFrame:
    values = df.groupby('Metier').agg(['mean', 'median'])['Experience']
    df.loc[
        (df.Experience.isna()) & (df.Metier=='Data scientist'), 'Experience'
    ] = values.loc['Data scientist', 'median']
    df.loc[
        (df.Experience.isna()) & (df.Metier=='Data engineer'), 'Experience'
    ] = values.loc['Data engineer', 'mean']
    return df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

def experience_average_per_job(df: pd.DataFrame) -> str:
    phrase = "La moyenne d'experience\n"
    for value in df.groupby('Metier').mean().itertuples():
        phrase += "pour un %s est %f années\n" % (value.Index, value.Experience)
    return phrase


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def experience_labellizer(df: pd.DataFrame) -> pd.DataFrame:
    firstQuartile = np.percentile(df.Experience.dropna(), q=25)
    median = np.percentile(df.Experience.dropna(), q=50)
    secondQuartile = np.percentile(df.Experience.dropna(), q=75)
    
    def helper_function(x: float) -> str:
        if x < firstQuartile:
            return "débutant"
        elif x < median:
            return "confirmé"
        elif x < secondQuartile:
            return "avancé"
        else:
            return "expert"
    new = df.copy()
    new.Experience = df.Experience.apply(helper_function)
    return new


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

