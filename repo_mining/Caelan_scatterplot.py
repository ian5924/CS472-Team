import matplotlib.pyplot as plt
from dateutil import parser
import pandas as pd
import numpy as np
import Caelan_config

repo = Caelan_config.repo
file = repo.split('/')[1]

commits = []

f = open(f"{Caelan_config.file_directory}/data_{file}.csv")
csv = pd.read_csv(f)
authors = csv["Author"].unique().tolist()
files = csv["Filename"].unique().tolist()
starttime = parser.parse(min(csv["Time"]))
print(starttime)

# Generate data...
cmap = plt.get_cmap("cool")
colors = cmap(np.linspace(0, 1, len(authors)))
color_map = dict(zip(authors, colors))

for commit in csv.index:
    x = files.index(csv["Filename"][commit])
    y = (parser.parse(csv["Time"][commit]) - starttime).days/7
    plt.scatter(x, y, c=color_map[csv["Author"][commit]])
plt.show()