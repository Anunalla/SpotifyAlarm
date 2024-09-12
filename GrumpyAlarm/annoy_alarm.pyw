import winsound
import configparser
import os
import time
import datetime as dt
from datetime import datetime as dtm
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

daysOfTheWeek = {6:"S",
                 0:"M",
                 1:"T",
                 2:"W",
                 3:"Th",
                 4:"F",
                 5:"Sa"}

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('grumpyAlarmConfig.ini')

    alarm_time= config['ALARM']['time']
    alarm_time = dtm.strptime(alarm_time,"%H:%M")
    alarm_days = config['ALARM']['days'].split("-")

    played=False
    num_snoozes = 6
    snooze_interval = 15 # min
    current_time = dtm.now()
    snooze_count = 0
    audio_devices = AudioUtilities.GetSpeakers()
    interface = audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    while(1):
        time.sleep(1)
        nowtime = dtm.now()
        check_obj = nowtime
        nowday = nowtime.weekday()
        day = daysOfTheWeek[nowday]
        # print(alarm_time,alarm_days,nowday, day)
        if (day in alarm_days):
            # print("Day recognized :" , alarm_time.hour,nowtime.hour,alarm_time.minute,nowtime.minute,played )
            if ((alarm_time.hour == nowtime.hour) & (alarm_time.minute == nowtime.minute)):
                    # adjust system volume level
                    volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(-5.5, None)
                    
                    for i in range(5):
                        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
                        time.sleep(7)
                    current_time = dtm.now()
                    played = True  
                    snooze_count = 0          
            else:
                if(played):
                    if(snooze_count<num_snoozes):
                        if((dtm.now()-current_time) >= dt.timedelta(minutes=15)):
                            volume.SetMute(0, None)
                            volume.SetMasterVolumeLevel(-5.5, None)
                            for i in range(5):
                                winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
                                time.sleep(7)
                            snooze_count+=1
                            current_time = dtm.now()
                            played = True
                        else:
                            pass
                    else:
                        played = False
                        snooze_count = 0
                else:
                    played= False
                    snooze_count = 0

