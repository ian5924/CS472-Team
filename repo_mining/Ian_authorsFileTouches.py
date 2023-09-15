import pandas as pd
import json
import requests
import csv
from datetime import datetime
import os
#import matplotlib.pyplot as plt


if not os.path.exists("data"):
 os.makedirs("data")
fileNameVec = []
authorNameVec = []
dateVec = []
# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, dictfiles2, dictfiles3, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    #3 vectors for file name, author name and date
    
     
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
               
                
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
               
                filesjson = shaDetails['files']
    
                for filenameObj in filesjson:
                    
                    filename = filenameObj['filename']
                    
                    if  filename.endswith(".java"):
                       # for storedFile in fileNameVec:
                            #if fileNameVec[storedFile] == filename:
                               # continue
                        
                        #print("dropped first java file")
                        author = shaObject['commit']['author']['name']#find the author/date
                        #print("author:", author)
                        date = shaObject['commit']['author']['date']
                        
                        
                        
                        
                        
                        fileNameVec.append(filename)
                        authorNameVec.append(author)
                        dateVec.append(date)
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        dictfiles2[author] = dictfiles2.get(author, 0) + 1
                        dictfiles3[date] = dictfiles3.get(date, 0) + 1
                        #print("date: ", date)
                        #print("dictfiles3[date]: ",dictfiles3[date])
                        
                    else:
                        #print("deafult")
                        continue 
                   
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["554516516"]

dictfiles = dict()
dictfiles2= dict()
dictfiles3= dict()


countfiles(dictfiles, dictfiles2, dictfiles3, lstTokens, repo)

df = pd.DataFrame({'fileNames': fileNameVec, 'authorNames': authorNameVec, 'dates': dateVec})
print (df)
dates = df['dates']
files = df['fileNames']
minDate = min(dates)
maxDate = max(dates)
print(type(minDate))
print(type(maxDate))

print(minDate)
print(maxDate)

dateFormat = "%Y/%m/%d/%H/%M/%S"
minDate = datetime.fromisoformat(minDate)
maxDate = datetime.fromisoformat(maxDate)


print(type(minDate))
print(type(maxDate))
print(minDate)
print(maxDate)



days = maxDate-minDate
weeksInTotal = days.days / 7
print(weeksInTotal)

df.to_csv('/test.csv')

#plt.scatter(files, weeksInTotal, c=weeksInTotal, s=400)

#print('Total number of files: ' + str(len(dictfiles)))
#print('Total number of authors: ' + str(len(dictfiles2)))
#print('Total number of dates: ' + str(len(dictfiles3)))
#print("dict files: ", dictfiles.items())
#print("\n \n \n dict AU : ", dictfiles2.items())
#print("\n \n \n dict DA : ", dictfiles3.items())
'''
file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

#bigcount = None #stat for max touch
#bigfilename = None#name of file with max touches
#print("This is dict files BEfore loop: ",dictfiles)
for author, count in dictfiles.items(): 
    rows = [author, count]
    print ("author: ", author, "count: ", count)
    writer.writerow(rows)
    print("Found bigcount: ", bigcount) # tracks file with most touches
    if bigcount is None or count > bigcount:
       
        bigcount = count
        bigfilename = filename
    

fileCSV.close()
'''
#print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
#print("This is dict files after loop: ",dictfiles)
#print("Size of fileName vec:", len(fileNameVec))
#print("Size of authorName vec:", len(authorNameVec))
#print("Size of dateName vec:", len(dateVec))


#for loop for 3 var