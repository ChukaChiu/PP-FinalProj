#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import os
import glob
from typing import Tuple, List

from tqdm import tqdm

from multiprocessing import Pool

import S4

LOG_DIR = './logs_dup'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

def serial_log(fileNames: List[str]):
    dataArray = np.empty((0, len(S4.dataHead)))
    debugArray = np.empty((0, len(S4.debugHead)))
    for fileName in tqdm(fileNames):
        arr, arrDbg = S4.do_parsing(fileName)
        dataArray = np.vstack([dataArray, arr])
        debugArray = np.vstack([debugArray, arrDbg])
    return dataArray, debugArray

def main():
    #np.set_printoptions(linewidth=250)
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    fileNameList = glob.glob(os.path.join(LOG_DIR, logFileGlob))

    with Pool(6) as p:
        dataArray = np.empty((0, len(S4.dataHead)))
        debugArray = np.empty((0, len(S4.debugHead)))
        for arr, arrDbg in tqdm(p.imap_unordered(S4.do_parsing, fileNameList)):
            dataArray = np.vstack([dataArray, arr])
            debugArray = np.vstack([debugArray, arrDbg])

    # # file headers
    # dataArray = S4.dataHead
    # debugArray = S4.debugHead

    # arr, arrDbg = serial_log(fileNameList)
    # dataArray = np.vstack([dataArray, arr])
    # debugArray = np.vstack([debugArray, arrDbg])

    # check report template exists
    if os.path.isfile(REPORT_TEMPLATE):
        now = datetime.now()
        reportName = PEPORT_PREFIX + now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + ".xlsx"
        S4.create_report(REPORT_TEMPLATE, reportName, STATION_NAME, [], dataArray, debugArray)

if __name__ == '__main__':
    timeStart = datetime.now()
    main()
    timeEnd = datetime.now()
    print('Time Spend: ' + str(timeEnd - timeStart))