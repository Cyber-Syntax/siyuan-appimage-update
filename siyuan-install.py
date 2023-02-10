#!/bin/python3

import requests
import json
import subprocess
import re, os
# Written by Cyber-Syntax.
# 18 January 2023

# Get the version of the latest release
response = requests.get("https://api.github.com/repos/siyuan-note/siyuan/releases/latest")
data = json.loads(response.text)

# Solve, missing "v" problem on the sha256 file.
version = data["tag_name"].replace("v", "")

# Directorys
appimages_dir = os.path.expanduser("~") + "/Documents/appimages/"
backup_dir = os.path.expanduser("~") + "/Documents/appimages/backup_siyuan/"
appimages_path = os.path.join(appimages_dir, "siyuan.AppImage")

# Download sha256 and appimage
def get_files():
    
    print("Siyuan installation started...")        
    
    # sha256
    url = [asset["browser_download_url"] for asset in data["assets"] if asset["name"] == "SHA256SUMS.txt"][0]
    subprocess.run(["wget", "-q", "-O", "SHA256SUMS.txt", url])
    print("Downloading SHA256SUMS.txt...")
    
    # appimage
    url = [asset["browser_download_url"] for asset in data["assets"] if asset["name"].endswith(".AppImage")][0]
    
    subprocess.run(["wget", "-q", "-O", f"siyuan-{version}-linux.AppImage", url])
    print("Downloading Siyuan-Note Appimage...")

# Verify the sha256sum of the appimage file
def verify_file():    
    print("Verifying appimage with sha256")

    with open("SHA256SUMS.txt") as f:
        contents = f.read()    
        match = re.search(rf'siyuan-{version}-linux\.AppImage', contents)
        
        if match:                          
            cmd =["sha256sum", f"siyuan-{version}-linux.AppImage", "-c", "SHA256SUMS.txt"]
            result = subprocess.run(cmd, capture_output=True, text=True)              
            
            if f"siyuan-{version}-linux.AppImage: OK" in result.stdout:
                print("SHA256SUMS.txt verified successfully")   
                # Delete sha file                                  
                subprocess.run(["rm", "SHA256SUMS.txt"])

                subprocess.run(["mv", f"siyuan-{version}-linux.AppImage", "siyuan.AppImage"])                            
                # Give permission
                subprocess.run(["chmod", "+x", "siyuan.AppImage"])                                                                                     
            else:
                print("Error: SHA256SUMS.txt verification failed!")
                exit(1)
        else:
            print("Error: File not found in SHA256SUMS.txt")
            exit(1)

def log_version(): 
    # Create file for logging siyuan version       
    f = open("siyuan-version", "a")
    f.write(f"{version}\n")
    f.close()

    f = open("siyuan-version", "r")
    print(f.read(), "The version is logged.")
    
    # Move to appimage directory
    try:
        pwd = ["pwd"]
        result_pwd = subprocess.run(pwd, capture_output=True) 
        
        # solve, unknown parameters     
        last = result_pwd.stdout.decode('utf-8')[:-1]                     
        
        subprocess.run(["mv", f"{last}/siyuan-version", appimages_dir])    
        print("Appimage version successfully logged.")            
    
    except subprocess.CalledProcessError:
        print("Error: while moving files to appimages directory")
        return

def save_old():
    # Find current directory
    pwd = ["pwd"]
    result_pwd = subprocess.run(pwd, capture_output=True) 
    
    # Solve, unknown parameters     
    last = result_pwd.stdout.decode('utf-8')[:-1] 
    
    # Check if the file already exists in the folder
    if os.path.exists(appimages_path):
        print(f"siyuan.AppImage found at {appimages_path}")
        confirm = input(f"If you want to overwritten (y), want to backup old (n)?")

        # The file is overwritten or backed up      
        if confirm.lower() == 'y':                                                              
            subprocess.run(["mv", f"{appimages_path}", appimages_dir])                                                              
        else:
            # backup old version
            subprocess.run(["mv", f"{appimages_path}", "siyuan.old.AppImage"])
            subprocess.run(["mv", "siyuan.old.AppImage", backup_dir])

            # Move new version to appimages directory
            subprocess.run(["mv", f"{appimages_path}", appimages_dir])            


def main():
    get_files()
    verify_file()
    save_old()
    log_version()    
    print("Siyuan installed successfully.")

if __name__ == "__main__":
    main()
