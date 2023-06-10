#!/usr/bin/env python3

import argparse
from datetime import datetime
import numpy as np
import os
import glob
from time import strftime

import S4

LOG_DIR = './logs'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

if __name__ == '__main__':
    firstTime = True
    fileList = os.listdir(LOG_DIR)
    parser = argparse.ArgumentParser()
    parser.add_argument('--station', '-s', choices = ['S4'])
    args = parser.parse_args()
    timeStart = datetime.now()

    #np.set_printoptions(linewidth=250)
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, args.station, LOG_EXT)
    for fileName in glob.glob(os.path.join(LOG_DIR, logFileGlob)):
        if firstTime:
            headArray = S4.get_info(fileName)
            dataArray = S4.dataHead
            debugArray = S4.debugHead
        arr, arrDbg = S4.do_parsing(fileName)
        dataArray = np.vstack([dataArray, arr])
        debugArray = np.vstack([debugArray, arrDbg])
        firstTime = False
        
    # check report template exists
    if os.path.isfile(REPORT_TEMPLATE):
        reportWritable = True
        now = datetime.now()
        reportName = PEPORT_PREFIX + now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + ".xlsx"
        if args.station in ['s4', 'S4']:
            S4.create_report(REPORT_TEMPLATE, reportName, args.station.upper(), headArray, dataArray, debugArray)
    
    timeEnd = datetime.now()
    print('Time Spend: ' + str(timeEnd - timeStart))