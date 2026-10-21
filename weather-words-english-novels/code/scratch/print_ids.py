import pandas as pd
s = pd.read_csv("data/sample_ids.csv")
for c in sorted(s.cohort.unique()):
    print(c, ",".join(map(str, s[(s.cohort == c) & (s.draw_rank <= 20)].id)))
