import os

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

lstTokens = []
file_directory = "data"

if not os.path.exists(file_directory):
 os.makedirs(file_directory)