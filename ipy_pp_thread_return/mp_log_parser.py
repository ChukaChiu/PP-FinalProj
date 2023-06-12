import argparse
from datetime import datetime
##import numpy as np
import sys
import os
import sys
from time import strftime
import threading

import S4

LOG_PATH = '.'
LOG_TYPE = '.log'
MODEL_NAME = 'LWR-X8460'

REPORT_EMPTY = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

if __name__ == '__main__':
    firstTime = True
    fileList = os.listdir(LOG_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument('--station', '-s', choices = ['s2', 'S2', 's4', 'S4'])
    args = parser.parse_args()
    timeStart = datetime.now()

    threads = []
    dataArray = S4.dataHead
    debugArray = S4.debugHead

    #np.set_printoptions(linewidth=250)
    for file in fileList:
        if file.startswith(MODEL_NAME) and file.endswith(LOG_TYPE) and file.find(args.station.upper()) != -1:
            if args.station in ['s4', 'S4']:
                if firstTime:
                    headArray = S4.get_info(file)
                    dataArray = S4.dataHead
                    debugArray = S4.debugHead
                arr, arrDbg = S4.do_parsing(file)
                dataArray = list(zip(dataArray, arr))
                debugArray = list(zip(debugArray, arrDbg))
                firstTime = False
                
                thread = threading.Thread(target=S4.do_parsing, args=(file))
                thread.start()
                threads.append(thread)
                
        elif file == REPORT_EMPTY:
            now = datetime.now()
            reportName = PEPORT_PREFIX + now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + ".xlsx"
            reportWritable = True
            
    #if reportWritable:
    #    if args.station in ['s4', 'S4']:
    #        S4.create_report(REPORT_EMPTY, reportName, args.station.upper(), headArray, dataArray, debugArray)
    
    timeEnd = datetime.now()
    print('Time Spend: ' + str(timeEnd - timeStart))