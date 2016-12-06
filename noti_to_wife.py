#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Run by crontab 10:00 ~ 18:30

import configparser
from datetime import datetime
import random
import time
import subprocess
import sys

MAX_SEND_CNT = 3

def noti_to_wife(conf_path):
    rv = []
    for i in range(0, MAX_SEND_CNT):
        rv.append(random.randrange(0, 59))
    
    config = configparser.ConfigParser()

    if (conf_path.endswith('/')):
        config.readfp(open(conf_path + 'msg.ini'))
    else:
        config.readfp(open(conf_path + '/msg.ini'))

    number = config.get('MSG', 'number')
    message = config.get('MSG', 'message')
    command = './send_msg.osa %s %s' % (number, message)
    
    snd_cnt = 0
    while True:
        time.sleep(1)
        now = datetime.now()
    
        # 11, 14, 17
        if snd_cnt == 0:
            if (now.hour != 12):
                continue
        elif snd_cnt == 1:
            if (now.hour != 14):
                continue
        elif snd_cnt == 2:
            if (now.hour != 17):
                continue
        else:
            sys.exit(1)
    
        if (rv[snd_cnt] == now.minute):
            subprocess.run(command, shell=True, check=True)
            snd_cnt += 1
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: noti_to_wife.py $CONF_PATH', file=sys.stderr)
        sys.exit(2)

    conf_path = sys.argv[1]
    noti_to_wife(conf_path)

