import numpy as np
import pandas as pd
from cleanDataMovies import *

df = pd.read_csv('full_data_imdb.csv', sep = ";", nrows = 1000)

clean_movie_dataset(df, verbose=True)
quick_dataset_summary(df, top_n =20, verbose = True)

#df2 = pd.read_csv('DS_TICM_EQUIPEMENT_data.csv', sep = ";", nrows = 1000)

#quick_dataset_summary(df2, top_n =20, verbose = True)