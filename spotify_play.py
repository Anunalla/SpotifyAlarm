import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import configparser
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def volume_fading(sp,device_id,start_pcnt,interval, coeff, max_vol=80):
    last_pcnt = start_pcnt
    while last_pcnt < max_vol:
        time.sleep(interval)
        new_pcnt = math.ceil(last_pcnt + last_pcnt* coeff)
        if new_pcnt>max_vol:
            new_pcnt = max_vol
        sp.volume(new_pcnt,device_id)
        last_pcnt = new_pcnt

def play_my_jam():
    config = configparser.ConfigParser()
    config.read('alarmConfig.ini')
    client_id = config['SPOTIFY']['client_id']
    client_secret = config['SPOTIFY']['client_secret']
    client_redirect_uri = config['SPOTIFY']['client_redirect_uri']
    target_uri = config['SPOTIFY']['track_uri']
    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    os.environ['SPOTIPY_REDIRECT_URI'] = client_redirect_uri

    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    # Shows playing devices
    res = sp.devices()
    print("Found Players: \n", res)

    found_desktop_app = False
    desktop_app_index = 0
    if (len(res["devices"]) > 0):
        for i in range(0, len(res["devices"])):
            if (res["devices"][i]["type"] == "Computer"):
                res["devices"][i]["is_active"] = True
                found_desktop_app = True
                desktop_app_index = i
    print("Found desktop app? ", found_desktop_app)
    start_volume_pcnt = 100
    device_id = res['devices'][desktop_app_index]['id']
    interval = 5
    coeff = 0.1

    # adjust system volume level
    audio_devices = AudioUtilities.GetSpeakers()
    interface = audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-5.5, None) # range: -65.0 to 0 : 0-> 100, -65.0 : 0, for every 6 point increase, volume doubles (-5.5 = 69)
    
    try:
        sp.volume(start_volume_pcnt,device_id)
        sp.start_playback(device_id=device_id,uris=[target_uri])
    except Exception as e:
        print("Play failed")
        print(e)
    # volume_fading(sp, device_id, start_volume_pcnt, interval, coeff, max_vol=70)

if __name__ == "__main__":
    play_my_jam()