import json
import requests
import csv
import Caelan_config
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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    
    language_gist_url = "https://gist.githubusercontent.com/ppisarczyk/43962d06686722d26d176fad46879d41/raw/211547723b4621a622fc56978d74aa416cbd1729/Programming_Languages_Extensions.json"
    language_json = requests.get(language_gist_url).json()

    language_url = f"https://api.github.com/repos/{repo}/languages"
    languages, ct = github_auth(language_url, lsttokens, ct)
    languages = languages.keys()
    extensions = {extension
                  for l in language_json
                  if l['name'] in languages
                  for extension in l['extensions']}

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = f"https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100"
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = f"https://api.github.com/repos/{repo}/commits/{sha}"
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if os.path.splitext(filename)[1] in extensions:
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

repo = Caelan_config.repo
lstTokens = Caelan_config.lstTokens

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print(f'Total number of files: {len(dictfiles)}')
 
file = repo.split('/')[1]
fileOutput = f"{Caelan_config.file_directory}/file_{file}.csv"
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w', newline='')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print(f'The file {bigfilename} has been touched {bigcount} times.')