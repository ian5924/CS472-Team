#!/usr/bin/python
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser as prsr

# rows for the CSV file
rows = ["Author", "AuthorID", "File", "FileID", "DateModified"]
f = open("data/file_rootbeer.csv", 'r')   # open file in read

# first line was transferred as the start date
startdate = prsr.parse(f.readline())
csvfile = pd.read_csv(f)

#Get authors only unique because the commits are simply listed.
authors = csvfile['Author'].unique()


# create the color map based on the length of my authors, so that each one is a different color.
clr = plt.get_cmap("tab20")
colors = [clr(i) for i in numpy.linspace(0, 1, len(authors))]
colorMap = dict(zip(authors, colors))

uniquePoints = []
uPointLabels = []
plottedAuthors = []


fig = plt.figure()
fig.set_figwidth(fig.get_figwidth() * 1.7)
fig.set_figheight(fig.get_figheight() * 1.5)
plt.xlabel("File ID")
plt.ylabel("Weeks since start")
plt.title("Author Contributions by file since project start")
# go through each row in the CSV and plot it.
for idx, row in csvfile.iterrows():
    x = row['FileID']
    # (commit date - start date) -> # of days /7 = # of weeks activity
    y = (prsr.parse(row['DateModified']) - startdate).days/7
    author = row['Author']
    color = colorMap[author]
    point = plt.scatter(x, y, label=author, c=color)  #
    if author not in plottedAuthors:
        plottedAuthors.append(author)
        uniquePoints.append(point)
        uPointLabels.append(point.get_label())

plt.legend(uniquePoints, uPointLabels, title="Legend")
plt.show()




