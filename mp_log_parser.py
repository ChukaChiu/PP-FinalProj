#!/usr/bin/env python3

import cProfile
import argparse
from datetime import datetime
import numpy as np
import os
import glob
from time import strftime

from tqdm import tqdm

import S4

LOG_DIR = './logs_dup'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--profiling', type=bool, default=False
    )
    return parser

def process_logs():
    firstTime = True
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    for fileName in tqdm(glob.glob(os.path.join(LOG_DIR, logFileGlob))):
        if firstTime:
            dataArray = S4.dataHead
            debugArray = S4.debugHead
        arr, arrDbg = S4.do_parsing(fileName)
        dataArray = np.vstack([dataArray, arr])
        debugArray = np.vstack([debugArray, arrDbg])
        firstTime = False
        
    return dataArray, debugArray 
    

if __name__ == '__main__':
    args = args_parser().parse_args()
    process_start = datetime.now()
    dataArray, debugArray = process_logs()
    process_end = datetime.now()
    print('Process Time Spend: ' + str(process_end - process_start))

    # check report template exists
    if os.path.isfile(REPORT_TEMPLATE):
        write_file_start = datetime.now()
        reportName = PEPORT_PREFIX + write_file_start.strftime("%Y") + write_file_start.strftime("%m") + write_file_start.strftime("%d") + ".xlsx"
        S4.create_report(REPORT_TEMPLATE, reportName, STATION_NAME, [], dataArray, debugArray)
        write_file_end = datetime.now()
        print('Write File Time Spend: ' + str(write_file_end - write_file_start))