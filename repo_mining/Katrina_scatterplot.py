import matplotlib.pyplot as plt		# to make plot
import pandas				# parse csv file

result = pandas.read_csv('data/file_rootbeer.csv')

startYear = result['Year'].values[-1:]
startMonth = result['Month'].values[-1:]

plt.scatter(result['Filename Number'], ((result['Year'] - startYear) * 52) + (result['Month'] - startMonth), c = result['Author Color'], cmap="hsv")

# label scatter plot
plt.xlabel("file")
plt.ylabel("weeks")

plt.show()

