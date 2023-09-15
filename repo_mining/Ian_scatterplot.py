#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import json
import requests
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt


# In[29]:


df = pd.read_csv('test.csv')


# In[30]:


dates = df['dates']
files = df['fileNames']


# In[31]:


#print (df)
dates = df['dates']
files = df['fileNames']
authors = df['authorNames']
minDate = min(dates)
maxDate = max(dates)
#print(type(minDate))
#print(type(maxDate))

#print(minDate)
#print(maxDate)

dateFormat =  "%Y-%m-%dT%H:%M:%S%z"
#minDate = datetime.fromisoformat(minDate)
#maxDate = datetime.fromisoformat(maxDate)
minDate = datetime.strptime(minDate,dateFormat)
maxDate = datetime.strptime(maxDate,dateFormat)

#print(type(minDate))
#print(type(maxDate))
#print(minDate)
#print(maxDate)



days = maxDate-minDate
weeksInTotal = days.days / 7
print(weeksInTotal)
print(files)


# In[32]:


plt.scatter(len(files), weeksInTotal, s=400, c=len(files))


# In[ ]:




