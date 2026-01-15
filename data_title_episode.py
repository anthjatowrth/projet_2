import numpy as np
import pandas as pd
from cleanDataMovies import *

# DATA SET : SERIE, SEASON NUMBER / EPISODE NUMBER

url = 'https://datasets.imdbws.com/title.episode.tsv.gz'
df = pd.read_csv(url, sep='\t', compression='gzip', low_memory=False, nrows = 1000 )

clean_movie_dataset(df, verbose = True)

quick_dataset_summary(df, top_n=10, verbose=True)