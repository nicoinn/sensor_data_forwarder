import time

from tellcore.telldus import TelldusCore
core = TelldusCore()


#Configure reporters
from Reporters import EmonCMS_Reporter,Console_Reporter
reporter1 = EmonCMS_Reporter("https://emoncms.org",apikey="YOUR_API_KEY",node="MY_NODE_NAME",only_mapped=True)
#reporter2 = EmonCMS_Reporter("http://yourserver.me:8080",apikey="YOUR_API_KEY2",node="MY_NODE_NAME2",only_mapped=True)
reporter3 = Console_Reporter(only_mapped=False)

reporters = [reporter1,reporter3]


#How frequently to pull sensor data from Telldus Core (in seconds)
reporting_interval = 60

from Sensor_record import Sensor_record

stop_time = time.time()
while True:
    start_time = stop_time
    Sensor_records = map(Sensor_record,core.sensors())
    for reporter in reporters:

        #By first buffering all the sensors and flushing at the end, we will only get one timeout in case the server
        #is not available.
        map(reporter.report_async,Sensor_records)
        reporter.flush_buffer()

    stop_time = time.time()
    time_left_next_report = reporting_interval - (stop_time-start_time)

    if (time_left_next_report>0):
        time.sleep(time_left_next_report)