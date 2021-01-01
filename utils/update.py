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

  # determine installation directory of Streambox, regardless of current working directory
  current_dir = os.path.dirname(os.path.realpath(__file__))
  install_dir = os.path.join(current_dir, "..")

  # parse file current_stable_version.txt
  stable_version_hash = ""
  filename = os.path.join(install_dir, "current_stable_version.txt")
  with open(filename, "r") as f:
    stable_version_hash = f.read()
    stable_version_hash = str(stable_version_hash).strip()   # remove whitespace
    
  # determine hash of checked out version
  current_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=install_dir)
  current_hash = current_hash.strip()   # remove whitespace
  current_hash = current_hash.decode("utf-8")
  
  print("  Current stable version hash={}".format(stable_version_hash))
  print("  Checked out version    hash={}".format(current_hash), flush=True)
  
  if current_hash != stable_version_hash:
    
    # checkout main
    output_checkout_main = subprocess.check_output(["git", "checkout", "main"], cwd=install_dir)
    
    # pull
    output_pull = subprocess.check_output(["git", "pull", "origin", "main"], cwd=install_dir)
    
    # checkout version
    checkout_successfull = True
    output_checkout = ""
    try:
      output_checkout = str(subprocess.check_output(["git", "checkout", stable_version_hash], cwd=install_dir))
    except:
      checkout_successfull = False
    
    print("--------------------------\n\033[92mgit checkout main\033[0m")
    print(str(output_checkout_main))
    print("\033[92mgit pull origin main\033[0m")
    print(str(output_pull))
    print("\033[92mgit checkout {}\033[0m".format(stable_version_hash))
    print(str(output_checkout))
    print("\n--------------------------\n")
    
    if checkout_successfull:
      print("Now exiting script such that it can be restarted.", flush=True)
      sys.exit(0)
    else:
      print("Checkout was not successful")
  
  else:
    print("  Version is up to date.", flush=True)
