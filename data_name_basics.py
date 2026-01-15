import numpy as np
import pandas as pd
from cleanDataMovies import *

url = 'https://datasets.imdbws.com/name.basics.tsv.gz'
df = pd.read_csv(url, sep='\t', compression='gzip', low_memory=False )

clean_movie_dataset(df, verbose = True)

quick_dataset_summary(df, top_n=5, verbose=True)