import os
import time
import wmi
import keyboard
import subprocess
# # Initializing the wmi constructor
def closeSpotify():
    os.system("c:\\windows\\system32\\taskkill.exe /f /im Spotify.exe")
def openSpotify():
    subprocess.Popen("Spotify.exe", start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
def playNextSong():
    keyboard.press('ctrl')
    keyboard.press('right')
    keyboard.release('ctrl')
    keyboard.release('right')
def lastWindow():  
    keyboard.press('alt')
    keyboard.press('tab')
    keyboard.release('alt')
    keyboard.release('tab')
def restartSpotify():
    closeSpotify()
    openSpotify()
    time.sleep(1)
    playNextSong()
    time.sleep(1)
    lastWindow()
if __name__ == "__main__":
    restartSpotify()