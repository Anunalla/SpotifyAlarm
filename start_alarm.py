import os
import time
from datetime import datetime
import spotify_play
import configparser

daysOfTheWeek = {6:"S",
                 0:"M",
                 1:"T",
                 2:"W",
                 3:"Th",
                 4:"F",
                 5:"Sa"}

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('alarmConfig.ini')
    alarm_time= config['ALARM']['time']
    alarm_time = datetime.strptime(alarm_time,"%H:%M")
    alarm_days = config['ALARM']['days'].split("-")
    played=False
    while(1):
        time.sleep(1)
        nowtime = datetime.now()
        check_obj = nowtime
        nowday = nowtime.weekday()
        day = daysOfTheWeek[nowday]
        # print(alarm_time,alarm_days,nowday, day)
        if (day in alarm_days):
            # print("Day recognized :" , alarm_time.hour,nowtime.hour,alarm_time.minute,nowtime.minute,played )
            if ((alarm_time.hour == nowtime.hour) & (alarm_time.minute == nowtime.minute)):
                if(played==False):
                    print("I am playing")
                    spotify_play.play_my_jam()
                    played = True
            else:
                played= False

