import numpy as np
import pandas as pd
from cleanDataMovies import *

# DATA SET : ID MOVIE, MOVIE NAME, REGION, ORDERING, ORIGINAL TITLE

url = 'https://datasets.imdbws.com/title.basics.tsv.gz'
df = pd.read_csv(url, sep='\t', compression='gzip', low_memory=False, nrows = 1000 )

clean_movie_dataset(df, verbose = True)

quick_dataset_summary(df, top_n=5, verbose=True)