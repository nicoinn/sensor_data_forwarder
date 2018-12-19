import sys
import os
from Sensor_record import Sparsnas_Sensor_record

API_KEY = os.environ.get('EMONCMS_API_KEY')
NODE_NAME = os.environ.get('EMONCMS_NODE_NAME')
EMONCMS_URL = os.environ.get('EMONCMS_URL')


#Configure reporters
from Reporters import EmonCMS_Reporter,Console_Reporter
reporter1 = EmonCMS_Reporter(EMONCMS_URL,apikey=API_KEY,node=NODE_NAME,only_mapped=False)
reporter2 = Console_Reporter()

reporters = [reporter1,reporter2]

#!/usr/bin/python

import sys

while 1:
    line = sys.stdin.readline()
    if line == '':
        break
    try:
        Sensor_record = Sparsnas_Sensor_record(line)
        for reporter in reporters:
            reporter.report_async(Sensor_record)
            reporter.flush_buffer()         
    except:
        pass

