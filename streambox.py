#!/usr/bin/python3
#
# Installation
# pip3 install keyboard python-vlc matplotlib certifi humanize pyautogui

# References
# https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/play_buffer.py;h=23a52f96b5367531838c28079d6263b69cab0ca9;hb=HEAD
# API documentation: https://www.olivieraubert.net/vlc/python-ctypes/doc/
# wiki: https://wiki.videolan.org/Python_bindings
# keyboard: https://github.com/boppreh/keyboard#keyboard.hook
#
# Notes
# set audio output: right-click on audio icon and select HDMI

import sys, os
import time
import vlc
import keyboard 
import sys, os
import requests
import shutil
import os.path
import threading
import datetime
import traceback
import subprocess
import pyautogui

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.rcParams["figure.facecolor"] = "black"
plt.rcParams["toolbar"] = "None"

# scripts in utils directory
current_dir = os.path.dirname(os.path.realpath(__file__))
utils_dir = os.path.join(current_dir, "utils")
sys.path.append(utils_dir)
import update
import parse
import show_overlay

show_webcam = False
available_files = []

# callback function to handle key presses
def key_pressed(event):
  global show_webcam
  
  show_webcam = False
  print("  (Released key \"{}\", code {})".format(event.name, event.scan_code), flush=True)
  
  try:
    
    if event.name == "space" or event.scan_code == 57:
      print("pause", flush=True)
      
      # determine text depending if the video is currently playing
      text = "Weiter"
      if media_player.is_playing():
        text = "Pause"
        
      # toggle pause
      media_player.pause() 
      
      # show progress bar and the word "Pause" or "Weiter"
      show_overlay.show_video_progress(media_player, text, 3)
      
    elif event.name == "backspace" or event.scan_code == 14:
      print("restart from beginning", flush=True)
      media_player.set_time(0)
      
      # show progress bar 
      show_overlay.show_video_progress(media_player, "zurück gespult", 2)
      
    elif event.name == "tab" or event.scan_code == 69:
      print("toggle fullscreen", flush=True)
      media_player.toggle_fullscreen()
      
      # show progress bar 
      show_overlay.show_video_progress(media_player, "zurück gespult", 2)
      
    elif event.name == "÷" or event.scan_code == 98:
      print("stop", flush=True)
      media_player.stop() 
      
    elif event.name == "q" or event.name == "Q":
      print("quit", flush=True)
      sys.exit(2)
    
    elif event.name == "+":
      print("jump forward", flush=True)
      current_time = media_player.get_time()  # in ms
      new_time = current_time + 10000
      media_player.set_time(new_time) # in ms
      
      # show progress bar 
      show_overlay.show_video_progress(media_player, "+10s", 2)
    
    elif event.name == "-":
      print("jump backwards", flush=True)
      current_time = media_player.get_time()  # in ms
      media_player.set_time(current_time - 10000) # in ms
      
      # show progress bar 
      show_overlay.show_video_progress(media_player, "-10s", 2)
    
    elif event.name == "enter" or event.scan_code == 96:
      print("show info", flush=True)
      
      available_files = parse.get_available_files()
      
      text_list = ""
      fontsize = 100
      print("  n:",len(available_files), flush=True)
      if len(available_files) > 5:
        fontsize = 50
        
      print("  font size: {}".format(fontsize))
        
      for i,filename in reversed(list(enumerate(available_files))):
        
        t = parse.get_date_from_filename(filename)
        text = parse.get_readable_date(t)
        
        key_index = len(available_files)-i-1
        
        if key_index < 10:
          text_list += "{}. {}\n".format(key_index, text)
        
      # show progress bar and the word "Pause" or "Weiter"
      show_overlay.show_overlay_text(text_list, 10, fontsize=fontsize)
    
    elif event.scan_code == 83:  # ","
      print("load current stream", flush=True)
      # get all available videos
      livestream_url = ""
      
      show_livestream()
      show_webcam = False
      
    elif event.scan_code == 55:  # "snowflake"
      print("snowflake", flush=True)
      url = "https://golf-alvaneu.ch/livecam/webcam.jpg"
      
      #open_stream(url)
      
      # download image
      r = requests.get(url, verify=False, stream=True)
      r.raw.decode_content = True

      with open("webcam.jpg", "wb") as f:
        shutil.copyfileobj(r.raw, f)
      
      media_player.stop()
      show_webcam = True
      
    elif event.name in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
      # get all available videos
      available_files = parse.get_available_files()
      
      number = (int)(event.name)
      selected_file = None
      
      print("- Load stream {} of {} available".format(number, len(available_files)), flush=True)
      
      if len(available_files) > number:
        selected_filename = available_files[-1-number]
        
        print("  select file \"{}\"".format(selected_filename), flush=True)
        
        # determine date from filename
        t = parse.get_date_from_filename(selected_filename)
        
        # print datetime object in readable format
        text = parse.get_readable_date(t)
        print("  File \"{}\", date {}".format(selected_filename, text), flush=True)
        
        # show text 
        show_overlay.show_overlay_text(text, 5)
        
        # open the video stream in vlc
        open_stream(selected_filename)
      else:
        print("Error, there are {} streams available, but {} was pressed".
          format(len(available_files), number), flush=True)
        show_overlay.show_overlay_text("{} gedrückt, es sind jedoch nur {} Videos verfügbar.".format(number, len(available_files)), 5)
          
    if not show_webcam:
      plt.close("all")
          
  except Exception as e:
    print(e)
    traceback.print_exc()
          
def open_stream(source):
  print("- Play \"{}\"".format(source), flush=True)
  try:
    # load media
    media = vlc_instance.media_new(source)
    media_player.set_media(media) 
            
    # play the video
    media_player.play() 
    media_player.set_fullscreen(True)
    #media_player.set_fullscreen(False)
    media_player.video_set_scale(0)   # 0 means adjust to fit

    # get information about the video
    duration = media_player.get_length() 
    size = media_player.video_get_size() 
    print("- Play \"{}\", duration: {}s, size: {}".format(source, duration, size), flush=True)

  except Exception as e:
    print(e, flush=True)
        
def show_livestream():
  print("- Show livestream", flush=True)
  media_player.stop()
  subprocess.Popen("sudo -u pi chromium-browser --no-sandbox --noerrdialogs --disable-infobars --incognito --kiosk --start-fullscreen https://rk-solutions-streamc.de/hohenacker/livestream.html", shell=True)
  
  # wait for chrome to load
  time.sleep(20)
  
  # get screen resolution
  screen_width, screen_height = pyautogui.size()
    
  print("  Screen dimensions: {} x {} ".format(screen_width, screen_height), flush=True)
  print("  Now move to {},{} ".format(int(screen_width/2), int(screen_height/2)), flush=True)
    
  # click at center of screen to start the stream
  pyautogui.moveTo(int(screen_width/2), int(screen_height/2))
  print("  Click")
  pyautogui.click()
  
          
# start of the script
print("streambox.py started", flush=True)

# download a new version of this script if available, then quit the program
# or do nothing if there is no newer version
update.apply_updates()
          
# start extra thread that downloads new videos
try:
  thread = threading.Thread(target = parse.download_new_videos)
  thread.start()
  time.sleep(2)  # wait two seconds for the checks being run
except:
  print("Could not start thread to download new videos.", flush=True)
          
# register callback
keyboard.on_press(key_pressed)
#keyboard.on_release(key_released)

# create a vlc instance 
vlc_instance = vlc.Instance() 
  
# create a media player 
media_player = vlc_instance.media_player_new() 
  
# creating the media 
#media = vlc_instance.media_new(source)
  
# assign media to the player
#media_player.set_media(media) 
  
# play the video
#media_player.play() 
#media_player.set_fullscreen(True)
  
try:
  
  # main loop
  while True:
    if show_webcam:
      
      # load webcam picture
      img = mpimg.imread("webcam.jpg")
      imgplot = plt.imshow(img)
      
      # set background color to black and remove axis
      plt.gcf().set_facecolor("black")
      plt.axis("off")
      
      # set fullscreen
      mng = plt.get_current_fig_manager()
      mng.full_screen_toggle()
      
      # display window
      plt.show()
    
    time.sleep(1)

except Exception as e:
  print(e)
  traceback.print_exc()
  
media_player.set_fullscreen(False)
  
