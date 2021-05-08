#!/usr/bin/python3

import tkinter as tk
import random
from string import ascii_letters

random.seed(42)

colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
def do_stuff():
  s = ''.join([random.choice(ascii_letters) for i in range(10)])
  color = random.choice(colors)
  label.config(text=s, fg=color)
  tk_instance.after(100, do_stuff)

tk_instance = tk.Tk()
tk_instance.wm_overrideredirect(True)
screen_width = tk_instance.winfo_screenwidth()
screen_height = tk_instance.winfo_screenheight()
print("screen dimensions: {} x {}".format(screen_width, screen_height))
tk_instance.geometry("{}x{}+0+0".format(screen_width, screen_height))
tk_instance.bind("<Button-1>", lambda evt: tk_instance.destroy())

label = tk.Label(text='', font=("Helvetica", 60))
label.pack(expand=True)

do_stuff()
tk_instance.mainloop()
