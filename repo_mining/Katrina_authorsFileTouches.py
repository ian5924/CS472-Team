import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

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
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # keep track of all authors for colors and file numbers
    authors = []
    files = []

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

                # get author name for commit
                commitAuthor = shaDetails['commit']['author']['name']

                # get date commited
                date = shaDetails['commit']['author']['date']
                
                # get the month
                month = date [5:7]
                year = date [0:4]

                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # check if a source file
                    if filename.endswith(".java"):      # i think this is how you check file extension
                        # if first time checking file, initalize empty array
                        if filename not in dictfiles:
                            dictfiles[filename] = []
                            files.append(filename)
                        dictfiles[filename].append([commitAuthor, date])

                        if commitAuthor not in authors:
                            authors.append(commitAuthor)

                        # write info to file
                        # very neat :)
                        # rows = ["Filename", "Filename Number", "Author", "Date", "Month", "Year", "Author Color"]
                        rows = [filename, files.index(filename), commitAuthor, date, month, year, authors.index(commitAuthor)]
                        writer.writerow(rows)

                        # debugging
                        # print("filename: ", filename)
                        # print("commit author: ", commitAuthor)
                        # print("date: ", date, "\n")
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
lstTokens = [""]

# open the file before calling the function
file = repo.split('/')[1]

# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Filename Number", "Author", "Date", "Month", "Year", "Author Color"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

# print total # of files for debugging
print('Total number of files: ' + str(len(dictfiles)))

# close the file
fileCSV.close()
