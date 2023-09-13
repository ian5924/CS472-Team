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
  

def get_author_commits(repo, lsttokens, files):
    ct = 0  # token counter
    commits = []
  
    try:
        for file in files:
            print(f"Processing {file}")
            page = 1  # url page counter
            while True:
                commitsUrl = f"https://api.github.com/repos/{repo}/commits?path={file}&page={page}&per_page=100"
                jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)
                
                if not jsonCommits:
                    break
                
                for obj in jsonCommits:
                    commits.append((
                        file,
                        obj["commit"]["author"]["name"],
                        obj["commit"]["author"]["date"]))
                page += 1
    except:
        print("Error receiving data")
        exit(0)
    return commits


repo = Caelan_config.repo
lstTokens = Caelan_config.lstTokens
file = repo.split('/')[1]
fileInput = f"{Caelan_config.file_directory}/file_{file}.csv"
fileOutput = f"{Caelan_config.file_directory}/data_{file}.csv"
commits = None
firstCommit = startdate = github_auth(f"https://api.github.com/repos/{repo}", lstTokens, 0)[0]['created_at']

with open(fileInput) as csvfile:
  csvreader = csv.DictReader(csvfile)
  files = (row["Filename"] for row in csvreader)
  commits = get_author_commits(repo, lstTokens, files)

with open(fileOutput, "w", newline='') as csvfile:
    fieldnames = ["Filename", "Author", "Time"]
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    csvwriter.writeheader()
    for commit in commits:
        csvwriter.writerow({"Filename": commit[0],
                            "Author": commit[1],
                            "Time": commit[2]})