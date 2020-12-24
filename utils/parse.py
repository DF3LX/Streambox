#!/usr/bin/python3

import requests
import shutil
import os
import os.path
from datetime import datetime
import time

def parse_online_list(html_text):
  filenames = []

  pos = html_text.find("<tr><td>")
  
  while pos > 0:
    # find next filename
    pos = html_text.find("filename=", pos)
    if pos < 0:
      break
    pos += len("filename=")
     #print("pos: {}, string: [{}...]".format(pos, html_text[pos:pos+10]))

    # extract filename
    pos_end = html_text.find("\"", pos)
    filename_online = html_text[pos:pos_end]

    # advance to next filename
    filenames.append(filename_online)
    pos = html_text.find("</tr>", pos)

  return filenames
  
# print current date
print(datetime.today().strftime('%d.%m.%Y %H:%M:%S'))

# load index-nopw.php page
url = "https://rk-solutions-streamc.de/hohenacker/index-nopw.php"
r = requests.get(url, verify=False, stream=True)
r.raw.decode_content = True

with open("index-nopw.php", "wb") as f:
  shutil.copyfileobj(r.raw, f)

with open("index-nopw.php", "rb") as f:
  html_text = str(f.read())

# determine files that are available online
filenames = parse_online_list(html_text)

# determine files that have already been downloaded
path = "downloaded"

# create directory if it does not exist
if not os.path.exists(path):
  os.makedirs(path)
downloaded_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# iterate over all filenames that were found online
for filename in filenames:
 
  # check if file has already been downloaded
  if filename not in downloaded_files:
    print("Download file \"{}\".".format(filename))
    
    # download file
    t_start = time.time()
    url = "https://rk-solutions-streamc.de/hohenackerstreams/{}".format(filename)
    r = requests.get(url, verify=False, stream=True)
    r.raw.decode_content = True
    with open(os.path.join(path,filename), "wb") as f:
      shutil.copyfileobj(r.raw, f)

    t_end = time.time()
    print("Download finished in {} s.".format(t_end-t_start))

  else:
    print("File \"{}\" has already been downloaded earlier, do not download again.".format(filename))

