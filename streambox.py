#!/usr/bin/python3
#
# pip3 install keyboard python-vlc matplotlib
# TypeError: Couldn't find foreign struct converter for 'cairo.Context

# references:
# https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/play_buffer.py;h=23a52f96b5367531838c28079d6263b69cab0ca9;hb=HEAD
# API documentation: https://www.olivieraubert.net/vlc/python-ctypes/doc/
# wiki: https://wiki.videolan.org/Python_bindings
# keyboard: https://github.com/boppreh/keyboard#keyboard.hook

import time
import vlc
import keyboard 
import sys, os
import requests
import shutil
import os.path

source = "https://rk-solutions-streamc.de/hohenackerstreams/66778891-1608455300-Sunday-20-12-20-10-08.mp4"

show_webcam = False

# callback function to handle key presses
def key_pressed(event):
  global show_webcam
  
  show_webcam = False
  print("Released key \"{}\", code {}".format(event.name, event.scan_code))
  
  if event.name == "space" or event.scan_code == 98:
    print("pause")
    media_player.pause() 
    
  elif event.name == "backspace" or event.scan_code == 98:
    print("restart from beginning")
    media_player.set_time(0)
    
  elif event.name == "q":
    print("quit")
    quit()
    sys.exit(0)
  
  elif event.name == "+":
    print("jump forward")
    current_time = media_player.get_time()  # in ms
    media_player.set_time(current_time + 10000) # in ms
  
  elif event.name == "-":
    print("jump backwards")
    current_time = media_player.get_time()  # in ms
    media_player.set_time(current_time - 10000) # in ms
  
  elif event.scan_code == 83:  # ","
    print("load current stream")
    # get all available videos
    livestream_url = ""
    
    # start most recent video
    open_stream(available_streams[-1])
    
  elif event.scan_code == 55:  # "snowflake"
    print("snowflake")
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
    print("load stream")
    # get all available videos
    available_streams = update_available_streams()
    
    number = (int)(event.name)
    
    if len(available_streams) > number:
      open_stream(available_streams[-1-number])
    else:
      print("Error, there are {} streams available, but {} was pressed".
        format(len(available_streams), number))
          
def update_available_streams():
  path = "utils/downloaded"
  downloaded_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
  downloaded_files = sorted(downloaded_files)

  print("available streams: {}".format(downloaded_files))
  downloaded_files = [os.path.join(path,f) for f in downloaded_files]


  return downloaded_files
          
def open_stream(source):
  # load media
  media = vlc_instance.media_new(source)
  media_player.set_media(media) 
          
  # play the video
  media_player.play() 
  media_player.set_fullscreen(True)

  # get information about the video
  duration = media_player.get_length() 
  size = media_player.video_get_size() 
  print("playing {}, duration: {}, size: {}".format(source, duration, size))
          
          
# register callback
keyboard.on_release(key_pressed)

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
  
# main loop
while True:
  if show_webcam:
    
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    img = mpimg.imread("webcam.jpg")
    imgplot = plt.imshow(img)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
  
  time.sleep(1)
  
media_player.set_fullscreen(False)
  
