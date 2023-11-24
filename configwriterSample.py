import configparser
config = configparser.ConfigParser()
config['SPOTIFY'] = {'client_id': 'yourclientID',
                     'client_secret': 'yourclientSecret',
                     'client_redirect_uri': 'yourAppURI',
                     'track_uri':'yourJam'}
config['ALARM'] = {'time': '07:00',
                     'days': 'S-M-T-W-Th-F-Sa'}

with open('alarmConfig.ini', 'w') as configfile:
  config.write(configfile)