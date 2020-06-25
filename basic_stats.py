import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MnemosyneDjango.settings")
django.setup()

import pandas as pd
from tqdm import tqdm
import numpy as np
from data_interface.models import Log

# N_USER = 23512
#
# n = N_USER
# users = Log.objects.distinct('user_id').values_list('user_id', flat=True)
# counts = {
#     "user_id": np.zeros(n, dtype=str),
#     "count": np.zeros(n)
# }
# for i, u in tqdm(enumerate(users), total=n):
#     c = Log.objects.filter(user_id=u).count()
#     counts["count"][i] = c
#     counts["user_id"][i] = u
# print("backing up...", flush=True, end=" ")
# df = pd.DataFrame(counts)
# df.to_csv('counts_user.csv')
# print("done!")

v = Log.objects.distinct("user_id", "object_id").values_list("user_id", "object_id")
n = len(v)

counts = {
    "user_id": np.zeros(n, dtype=str),
    "object_id": np.zeros(n, dtype=str),
    "count": np.zeros(n)
}
for i, (u, o) in tqdm(enumerate(v), total=n):
    c = Log.objects.filter(user_id=u, object_id=o).count()
    counts["count"][i] = c
    counts["user_id"][i] = u
    counts["object_id"][i] = o

print("backing up...", flush=True, end=" ")
df = pd.DataFrame(counts)
df.to_csv('counts_user_item_pair.csv')
print("done!")
