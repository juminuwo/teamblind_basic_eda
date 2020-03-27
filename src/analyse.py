import numpy as np
import pandas as pd

threads = pd.read_csv('threads_scores.csv')
companies = np.unique(threads['company'])


def self_company_scores():
    scores = {}
    for company in companies:
        comp_df = threads[threads['company'] == company].drop_duplicates()
        comp_scores = []
        for col_n in comp_df.index:
            comp_scores.append(comp_df.iloc[0, 3 + col_n])
        scores.update({company: comp_scores})
    return scores
