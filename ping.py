import winsound
import datetime
import json
import os
import configparser
import codecs

from time import gmtime, strftime

# FILES
logs = 'log.txt'
work = 'oneping.txt'
config = 'config.ini'

log_file = open(logs, 'w')
log_file.close()

# INI FILE 
ini = configparser.ConfigParser()

with codecs.open(config, 'r', encoding='utf-8') as f:
    ini.read_file(f)

# INI VALUES
REPEAT = int(ini.get('ping_config', 'repeat'))
LIMIT = int(ini.get('ping_config', 'limit'))
MAX_LIMIT = int(ini.get('ping_config', 'max_limit'))
WARNING = int(ini.get('ping_config', 'warning'))
B_DURATION = int(ini.get('ping_config', 'b_duration'))
IP = ini.get('ping_config', 'ip')
BEEP = ini.get('ping_config', 'beep')

if REPEAT == 0:
    REPEAT = True

# BEEP
sound_f = 2500 # frequency of the sound
sound_d = B_DURATION # duration of the sound, change it on config file
if BEEP == 'on':
    beep = lambda beep: winsound.Beep(sound_f, sound_d + 1000)
else:
    beep = False
    
# TEXT COLORS
GREEN = '\033[1;32;40m'
RED = '\033[1;31;40m'
BLACK = '\033[1;30;40m'
YELLOW = '\033[1;33;40m'

type = [] # store the type of the ping, if =< 1 then store 0, else 1
x = 0

while x is not REPEAT:
    
    host = os.system('ping.exe -n 1 {0} | FIND "TTL=" > {1}'.format(IP, work))

    work_file = open(work)
    log_file = open(logs, 'a')
    
    line = work_file.read()
    
    if len(line) == 0:
        print(RED + 'Sem resposta, verifique se o host informado está correto\n' + BLACK)
        winsound.Beep(sound_f, sound_d + 1000)
    else:
    
        split = line.split('=')
        
        ms = split[2]
        
        ms = ms.replace(' TTL', '')
        ms = ms.replace('ms', '')
        ms = int(ms)

        if len(split) < 4:
            ms = split[1]
            ms = ms.replace('32 tempo<', '')
            ms = ms.replace('ms TTL', '')
        else:
            ms = split[2]
            ms = ms.replace('ms TTL', '')
        
        ms = int(ms)

        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        to_log = '{0} ms {1} \n'.format(ms, time)
        log_file.write(to_log)
        
        if ms >= LIMIT and ms < MAX_LIMIT:
            type.append(1)
            print(YELLOW + '{0} ms {1} {2}'.format(ms, BLACK, time))
        elif ms >= MAX_LIMIT:
            type.append(1)
            print(RED + '{0} ms {1} {2}'.format(ms, BLACK, time))
            winsound.Beep(sound_f, sound_d + 500)
        elif ms < LIMIT:
            type.append(0)
            print(GREEN + '{0} ms {1} {2}'.format(ms, BLACK, time))

        if len(type[-WARNING:]) == 3 and 0 not in type[-WARNING:]:
            winsound.Beep(sound_f, sound_d)
        
        if len(type) > 50:
            type = []
        
    log_file.close()
    work_file.close()
    
    x += 1

input(' ')
