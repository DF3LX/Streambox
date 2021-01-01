#!/usr/bin/python3

import subprocess
import vlc
import os
import tempfile
import datetime

def show_overlay_text(text, duration_seconds, fontsize=100):
  """ 
  displays an overlay text over fullscreen 
  :param text:         additional text to display
  :param duration_seconds: duration how long the text will be shown
  """
  
  print("- Display overlay for {} seconds, fontsize={}: \"{}\"".format(duration_seconds, fontsize, text), flush=True)
  #temporary_file = tempfile.NamedTemporaryFile()
  #temporary_file.write(text)
  #temporary_filename = temporary_file.name
  
  temporary_filename = "/tmp/a"
  with open(temporary_filename, "w") as f:
    f.write(text)
  
  subprocess.Popen(["osd_cat", "--pos=top", 
    "--offset=100", "--align=left", "--indent=10", "--color=white", 
    "--outline=2", "--outlinecolour=blue", "--delay={}".format(int(duration_seconds)),
    "--lines=15",
    "--font=-bitstream-*-*-*-*-*-{}-*-*-*-*-*-*-*".format(int(fontsize)), temporary_filename])

def show_overlay_bar(fraction, text, duration_seconds):
  """ 
  displays an overlay text over fullscreen and a progress bar
  :param fraction: value between 0 and 1 of the progress bar
  :param text: text to display
  :param duration_seconds: duration how long the text will be shown
  """
  
  fraction = max(0, min(1, fraction))  # clamp fraction to interval [0,1]
  
  print("- Display overlay for {} seconds with bar at {}%: \"{}\"".format(duration_seconds, int(fraction*100), text), flush=True)
  subprocess.Popen(["osd_cat", "--pos=top", 
    "--offset=100", "--align=left", "--indent=10", "--color=white", 
    "--outline=2", "--outlinecolour=blue", "--delay={}".format(int(duration_seconds)),
    "--font=-bitstream-*-*-*-*-*-40-*-*-*-*-*-*-*", 
    "--barmode=percentage", "--text={}".format(text), "--percentage={}".format(int(fraction*100))])

def show_video_progress(media_player, text, duration_seconds):
  """
  displays a progress bar of the current video position and the given text
  :param media_player: the vlc media player instance
  :param text:         additional text to display
  :param duration_seconds: duration how long the text will be shown
  """
  current_time = media_player.get_time()
  total_duration = media_player.get_length() 
  
  if current_time < 0:
    current_time = 0
    
  current_time_str = datetime.datetime.fromtimestamp(int(current_time/1000)).strftime("%M:%S")
  total_time_str = datetime.datetime.fromtimestamp(int(total_duration/1000)).strftime("%M:%S")
       
  text = "{} / {}   {}".format(current_time_str, total_time_str, text)
  
  # only show total duration if it is valid
  if total_duration < 0:
    text = "       {}".format(text)
  
  show_overlay_bar(current_time / total_duration, text, 2)
    
