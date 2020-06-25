import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv("counts.csv")
a = np.argsort(df["count"])[::-1]
print(df["count"][a][:30])
plt.hist(df["count"], log=10)
plt.xlabel("N entries")
plt.ylabel("Freq")
plt.show()