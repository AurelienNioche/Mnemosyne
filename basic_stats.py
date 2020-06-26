import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MnemosyneDjango.settings")
django.setup()

from django.utils import timezone

import pandas as pd
from tqdm import tqdm
import numpy as np
from data_interface.models import Log, Info

LIMIT_BULK = 1000

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

# print("Querying...")
# t = timezone.now()
# entries = Log.objects.distinct("user_id", "object_id").iterator()
# print(f"Done! [{timezone.now()-t}]")

# print("Counting...")
# t = timezone.now()
n = 21249531   # entries.count()
# print(f"Done! [{timezone.now()-t}]")

info_entries = []
i_entry = 0
i = 0
for e in Log.objects.distinct("user_id", "object_id").iterator():
    print(f"Get user_id and object id for entry {i}", end='\r')
    u, o = e.user_id, e.object_id
    c = Log.objects.filter(user_id=u, object_id=o).count()
    info_entries.append(
        Info(user_id=u, object_id=o, user_object_pair_id=u+'-'+o, count=c)
    )
    i_entry += 1
    i += 1
    if i_entry == LIMIT_BULK:
        Info.objects.bulk_create(info_entries)
        info_entries = []
        i_entry = 0

