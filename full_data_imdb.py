import numpy as np
import pandas as pd
from cleanDataMovies import *

#title_akas
url1 = 'https://datasets.imdbws.com/title.akas.tsv.gz'
df1 = pd.read_csv(url1, sep='\t', compression='gzip', low_memory=False, na_values='\\N')
df1.rename(columns={"titleId": "tconst"}, inplace=True)
df1=df1[['tconst','region','region','types','isOriginalTitle']]
df1=df1[df1['isOriginalTitle'] == 1]

#title_episode
# url2 = 'https://datasets.imdbws.com/title.episode.tsv.gz'
# df2 = pd.read_csv(url2, sep='\t', compression='gzip', low_memory=False, na_values='\\N')

#title_principals
url3 = 'https://datasets.imdbws.com/title.principals.tsv.gz'
df3 = pd.read_csv(url3, sep='\t', compression='gzip', low_memory=False, na_values='\\N')
df3 = df3[['tconst','nconst','category']]
df3 = df3[df3['category'] == 'director']
#title_ratings
url4 = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
df4 = pd.read_csv(url4, sep='\t', compression='gzip', low_memory=False, na_values='\\N')

#title_crew
#url5 = 'https://datasets.imdbws.com/title.crew.tsv.gz'
#df5 = pd.read_csv(url5, sep='\t', compression='gzip', low_memory=False, na_values='\\N')

#title-basics
url6 = 'https://datasets.imdbws.com/title.basics.tsv.gz'
df6 = pd.read_csv(url6, sep='\t', compression='gzip', low_memory=False, na_values='\\N')
df6 = df6[['tconst','titleType','originalTitle','isAdult','startYear','runtimeMinutes','genres']]
df6 = df6[df6['isAdult'] == 0]
df6 = df6[df6['titleType'] == 'movie']
for df in [df1, df3, df4, df6]:
    df['tconst'] = df['tconst'].astype(str).str.strip()

dfull = df1.merge(df3, on='tconst', how='inner') \
            .merge(df4, on='tconst', how='inner') \
            .merge(df6, on='tconst', how='inner')

#clean_movie_dataset(dfull, verbose=True)

#quick_dataset_summary(dfull, top_n=5, verbose=True)

dfull.to_csv('fulldata_imdb.csv', index = False)