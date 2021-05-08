# update

import sys
import os
import subprocess
import datetime

# determine installation directory of Streambox, regardless of current working directory
current_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = os.path.join(current_dir, "..")

def apply_updates():
  """ This functions checks if there is a newer versions of this program
  in the git repo and if so, checks out the latest version.
  The current version is indicated by the commit hash in current_stable_version.txt
  """
  print("- apply_updates() started at {}".format(datetime.datetime.today().strftime('%d.%m.%Y %H:%M:%S')), flush=True)

  if os.path.exists("NO_UPDATE"):
    print("No update file exists!")
    return

  # determine installation directory of Streambox, regardless of current working directory
  current_dir = os.path.dirname(os.path.realpath(__file__))
  install_dir = os.path.join(current_dir, "..")

  # determine hash of currently checked out version
  current_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=install_dir)
  current_hash = current_hash.strip()   # remove whitespace
  current_hash = current_hash.decode("utf-8")
  

  # checkout main
  output_checkout_main = subprocess.check_output(["git", "checkout", "main"], cwd=install_dir)
  
  # pull
  output_pull = subprocess.check_output(["git", "pull", "origin", "main"], cwd=install_dir)
    
  # determine hash of currently checked out version
  new_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=install_dir)
  new_hash = new_hash.strip()   # remove whitespace
  new_hash = new_hash.decode("utf-8")
  
  print("  old version hash={}".format(current_hash), flush=True)
  print("  new version hash={}".format(new_hash), flush=True)
  
  
  print("--------------------------\n\033[92mgit checkout main\033[0m")
  print(str(output_checkout_main))
  print("\033[92mgit pull origin main\033[0m")
  print(str(output_pull))
  print("\n--------------------------\n")
     
  if current_hash != new_hash:
    print("Now exiting script such that it can be restarted.", flush=True)
    sys.exit(0)
  else:
    print("  Version is up to date.", flush=True)

def revert(s):
  
  # checkout v0
  output1 = subprocess.check_output(["git", "checkout", "v0"], cwd=install_dir)
  output2 = subprocess.check_output(["git", "reset", "--hard"], cwd=install_dir)
  
  with open("NO_UPDATE", "w") as f:
    f.write("revert to v0 at {}\n".format(str(datetime.datetime.now())))
    f.write(s)
  
  
