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
    print("Downloading siyuan Appimage...")

# Verify the sha256sum of the appimage file
def verify_file():    
    print("Verifying appimage with sha256")

    with open("SHA256SUMS.txt") as f:
        contents = f.read()    
        match = re.search(rf'siyuan-{version}-linux\.AppImage', contents)
        if match:                
            cmd =["sha256sum", "siyuan-2.7.0-linux.AppImage", "-c", "SHA256SUMS.txt"]
            result = subprocess.run(cmd, capture_output=True, text=True)              
            if f"siyuan-{version}-linux.AppImage: OK" in result.stdout:            
                subprocess.run(["mv", f"siyuan-{version}-linux.AppImage", "siyuan.AppImage"])
                print("SHA256SUMS.txt verified successfully")                
                # Give permission
                subprocess.run(["chmod", "+x", "siyuan.AppImage"])
                
                # Send appimage directory
                pwd = ["pwd"]
                result_pwd = subprocess.run(pwd, capture_output=True) 
                # solve, unknown parameters     
                last = result_pwd.stdout.decode('utf-8')[:-1]                
                subprocess.run(["mv", f"{last}/siyuan.AppImage", os.path.expanduser("~") + "/Documents/appimages/"])
            else:
                print("Error: SHA256SUMS.txt verification failed!")
                exit(1)
        else:
            print("Error: File not found in SHA256SUMS.txt")
            exit(1)

def main():
    get_files()
    verify_file()
    
    print("Siyuan installed successfully.")

if __name__ == "__main__":
    main()
