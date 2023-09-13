#!/usr/bin/python

import json
import requests
import csv
from dateutil import parser as prsr

import os

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


validExtensions = {".java", ".kt", ".cpp", ".h"}

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

lstTokens = [""]
authCommits = dict(dict())
startdate = ""

authorColorCounter = 1
authorColorMap = {}

fileCounter = 1
fileNumberMap = {}


ipage = 1  # url page counter
ct = 0  # token counter

# Get the creation date
startdate = github_auth(
    'https://api.github.com/repos/' + repo,
    lstTokens,
    0
)[0]['created_at']
startdate = prsr.parse(startdate)
try:
    # loop though all the commit pages until the last returned empty page
    while True:
        spage = str(ipage)
        commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
        jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)
        # break out of the while loop if there are no more commits in the pages
        if len(jsonCommits) == 0:
            break
        # iterate through the list of commits in  spage
        for commit in jsonCommits:
            sha = commit['sha']
            # For each commit, use the GitHub commit API to extract the files touched by the commit
            shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
            shaDetails, ct = github_auth(shaUrl, lstTokens, ct)
            filesjson = shaDetails['files']
            author = commit['commit']['author']['name']

            # subtract commit date from start date and convert to weeks.
            commitDate = prsr.parse(commit['commit']['author']['date'])

            for filenameObj in filesjson:
                filename = filenameObj['filename']
                name, extension = os.path.splitext(filename)
                if extension not in validExtensions:
                    continue

                # Author doesnt exist
                if author not in authCommits.keys():
                    authCommits[author] = dict()
                    authCommits[author][filename] = list()
                    authCommits[author][filename].append(commitDate)
                    authorColorMap[author] = authorColorCounter
                    authorColorCounter += 1

                # Author exists but file never seen
                elif filename not in authCommits[author].keys():
                    authCommits[author][filename] = list()
                    authCommits[author][filename].append(commitDate)

                # Author and File exists
                else:
                    authCommits[author][filename].append(commitDate)

                if filename not in fileNumberMap:
                    fileNumberMap[filename] = fileCounter
                    fileCounter += 1

        ipage += 1

except Exception as w:
    print("Error receiving data")
    exit(0)

# Author names -> colors
#Files -> 0,1,2,3,4 ...

rows = ["Author","AuthorID", "File", "FileID", "DateModified"]

file = repo.split('/')[1]
fileOutput = 'data/file_' + file + '.csv'
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
# Startdate for later
writer.writerow([startdate])
writer.writerow(rows)

# author : {fileName : [dates...]}
for author in authCommits:
    commitDict = authCommits[author]
    for fileName in commitDict:
        commitDates = commitDict[fileName]
        for date in commitDates:
            rows = [author, authorColorMap.get(author), fileName, fileNumberMap.get(fileName), date]
            writer.writerow(rows)

fileCSV.close()

#
# author : \
#     {file : (times)}

