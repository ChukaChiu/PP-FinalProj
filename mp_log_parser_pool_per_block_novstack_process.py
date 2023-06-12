#!/usr/bin/env python3

import argparse
from datetime import datetime
import numpy as np
import os
import glob

from tqdm import tqdm

from multiprocessing import Manager, Process

import S4

LOG_DIR = './logs_dup'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

def split_task(filenames, section: int):
    total = len(filenames)
    section_size = total//section
    twoDims = []
    r = total % section
    for i in range(0, section):
        add = 0
        if i < r:
            add = 1
        twoDims.append(filenames[i*section_size:(i+1)*section_size+add])
    return twoDims

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--proc', type=int, required=True, default=1
    )
    return parser

def serial_log(fileNames):
    row = len(fileNames)
    dataArray = np.empty((row, len(S4.dataHead)), dtype=object)
    debugArray = np.empty((row, len(S4.debugHead)), dtype=object)
    for idx, fileName in enumerate(tqdm(fileNames)):
        arr, arrDbg = S4.do_parsing(fileName)
        dataArray[idx] = arr
        debugArray[idx] = arrDbg
    return dataArray, debugArray

def worker(fileNames, data_list, debug_list):
    dataArray, debugArray = serial_log(fileNames)
    data_list.append(dataArray)
    debug_list.append(debugArray)

def process_logs(proc_size: int):
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    fileNameList = glob.glob(os.path.join(LOG_DIR, logFileGlob))
    fileNameList2D = split_task(fileNameList, proc_size)

    if proc_size == 1:
        dataArray, debugArray = serial_log(fileNameList)
    else:
        manager = Manager()
        data_list = manager.list()
        debug_list = manager.list()
        jobs = []
        for i in range(0, proc_size):
            proc = Process(target=worker, args=(fileNameList2D[i], data_list, debug_list))
            proc.start()
            jobs.append(proc)

        for proc in jobs:
            proc.join()

        dataArray = np.empty((0, len(S4.dataHead)), dtype=object)
        debugArray = np.empty((0, len(S4.debugHead)), dtype=object)
        for i in range(0, proc_size):
            dataArray = np.vstack([dataArray, data_list[i]])
            debugArray = np.vstack([debugArray, debug_list[i]])
    return dataArray, debugArray

if __name__ == '__main__':
    args = args_parser().parse_args()
    process_start = datetime.now()
    dataArray, debugArray = process_logs(proc_size=args.proc)
    print(dataArray.shape, debugArray.shape)
    process_end = datetime.now()
    print('Process Time Spend: ' + str(process_end - process_start))

    # check report template exists
    
    # if os.path.isfile(REPORT_TEMPLATE):
    #     write_file_start = datetime.now()
    #     reportName = PEPORT_PREFIX + write_file_start.strftime("%Y") + write_file_start.strftime("%m") + write_file_start.strftime("%d") + ".xlsx"
    #     S4.create_report(REPORT_TEMPLATE, reportName, STATION_NAME, [], dataArray, debugArray)
    #     write_file_end = datetime.now()
    #     print('Write File Time Spend: ' + str(write_file_end - write_file_start))
