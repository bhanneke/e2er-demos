import glob
import pandas as pd
bins = [(1770, 1799), (1800, 1819), (1820, 1839), (1840, 1859), (1860, 1879), (1880, 1899)]
files = sorted(glob.glob('data/*.csv'))
print(files)
a = pd.concat([pd.read_csv(f) for f in files]).drop_duplicates('id')
print(len(a))
for i, (s, e) in enumerate(bins, 1):
    m = (a.author_birth_year >= s) & (a.author_birth_year <= e)
    print(i, m.sum(), a[m].authors.nunique())
print(a[a.authors.str.contains(';')].authors.head(8).tolist())
print(a.subjects.str.contains('ranslat', na=False).sum())
