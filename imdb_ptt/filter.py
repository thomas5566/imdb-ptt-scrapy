import pandas as ps
import numpy as np

df = ps.read_csv("text2.csv")
title = df.iloc[:, 0]

chicago = ps.read_csv("text.csv").dropna(how="all")
chicago["title"] = chicago["title"].astype("category")


ss = []

for x in title:
    ss.append(x)

# for s in ss:
#     print(chicago["title"][chicago["title"].str.contains(s)])


def matcher(x):
    for i in ss:
        if i in x:
            return i
    else:
        return np.nan


chicago["Match"] = chicago["title"].apply(matcher)

print(chicago["Match"])

# whatIwant = [chicago["title"].str.contains(s, case=False, regex=True) for s in ss]

# chicago["New_Column"] = np.where(whatIwant, chicago["title"])
