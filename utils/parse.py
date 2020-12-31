#!/usr/bin/python3

import requests
import shutil
import os
import os.path
import datetime
import time
import certifi
import urllib3
import humanize
import vlc
import subprocess

# determine installation directory of Streambox, regardless of current working directory
current_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = os.path.join(current_dir, "..")

downloaded_files_path = os.path.join(install_dir,"downloaded")
currently_downloading_files_path = os.path.join(install_dir,"currently_downloading")

def get_available_files():
  """
  return full paths of video files that are currently available locally
  """
  
  # get all files in directory "downloaded"
  downloaded_files = [os.path.join(downloaded_files_path, f) for f in os.listdir(downloaded_files_path) if os.path.isfile(os.path.join(downloaded_files_path, f))]
  return downloaded_files

def parse_online_list():
  """ 
  Helper function that parses the online streaming page and 
  determines all video files that are currently available online 
  :return: list with filenames
  """
  filenames = []

  # get index-nopw.php page from web server
  url = "https://rk-solutions-streamc.de/hohenacker/index-nopw.php"
  
  https = urllib3.PoolManager(
      cert_reqs='CERT_REQUIRED',
      ca_certs=certifi.where()
  )
  request = https.request('GET', url)
  html_text = request.data.decode('utf-8')

  # jump to start of list
  pos = html_text.find("<tr><td>")
  
  # iterate over "filename=" entries in html text
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
  
def download_new_videos():
  """
  Check which videos are available online and which have already been downloaded.
  Then download new videos. They are stored under directory "currently_downloading" during the download
  and then moved to the directory "downloaded". The locally available video files are all in "downloaded".
  """

  # print current date
  print("- download_new_videos started at {}".format(datetime.datetime.today().strftime('%d.%m.%Y %H:%M:%S')), flush=True)

  # determine files that are available locally

  # create directories if they do not exist
  if not os.path.exists(downloaded_files_path):
    os.makedirs(downloaded_files_path)
    
  if not os.path.exists(currently_downloading_files_path):
    os.makedirs(currently_downloading_files_path)
    
  # get all files in directory "downloaded"
  downloaded_files = [f for f in os.listdir(downloaded_files_path) if os.path.isfile(os.path.join(downloaded_files_path, f))]

  # check if the downloaded files under "downloaded" are all valid  
  vlc_instance = vlc.Instance()   # create a vlc instance 
  media_player = vlc_instance.media_player_new() # create a media player 
  
  # iterate over files
  for filename in downloaded_files:
      
    path = os.path.join(downloaded_files_path, filename)
    video_is_valid = True
      
    try:
      output = subprocess.check_output(["ffmpeg", "-i", path, "-t", "1", "-f", "null", "-"], stderr=subprocess.STDOUT)
      if "Invalid data found" in str(output):
        video_is_valid = False
    except Exception as e:
      #print("exception: {}".format(str(e)))
      video_is_valid = False
      
    if video_is_valid:
      print("  File {} under \"downloaded\" is valid.".format(filename), flush=True)
    else:
      print("  File {} under \"downloaded\" is invalid, removing it.".format(filename), flush=True)
      
      # remove this file
      os.remove(path)
      
  # relist all files in directory "downloaded", some have potentially been deleted
  downloaded_files = [f for f in os.listdir(downloaded_files_path) if os.path.isfile(os.path.join(downloaded_files_path, f))]

  # --------------------------------------------
  # determine files that are available online
  filenames_online = parse_online_list()

  print("  {} videos found online.".format(len(filenames_online)), flush=True)

  # iterate over all filenames that were found online
  for filename in filenames_online:
   
    # check if file has already been downloaded
    if filename not in downloaded_files:
      print("  Download file \"{}\" ".format(filename), end="", flush=True)
      
      # download file
      t_start = time.time()
      url = "https://rk-solutions-streamc.de/hohenackerstreams/{}".format(filename)
          
      https = urllib3.PoolManager(
          cert_reqs='CERT_REQUIRED',
          ca_certs=certifi.where()
      )
      # stream data in chunks
      request = https.request('GET', url, preload_content=False)
      
      # parse filesize from sent header
      headers = dict(request.headers)
      print("({}).".format(humanize.naturalsize(headers["Content-Length"])), flush=True)
      
      # store incoming data stream to file
      temporary_filename = os.path.join(currently_downloading_files_path, filename)
      resulting_filename = os.path.join(downloaded_files_path, filename)
      with open(temporary_filename, "wb") as f:
        shutil.copyfileobj(request, f)

      # move file from "currently_downloading" to "downloaded"
      os.rename(temporary_filename, resulting_filename)

      # measure runtime
      t_end = time.time()
      print("  Download finished in {:.2f} s.".format(t_end-t_start))

    else:
      print("  File \"{}\" has already been downloaded earlier, do not download again.".format(filename))

