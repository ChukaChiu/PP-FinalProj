#!/usr/bin/env python3

import cProfile
import argparse
from datetime import datetime
import numpy as np
from numpy.typing import NDArray
import os
import glob
from typing import Tuple, List, Any

from tqdm import tqdm

from multiprocessing import Pool

import S4

LOG_DIR = './logs_dup'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

def split_task(filenames: List[str], section: int) -> List[List[str]]:
    total = len(filenames)
    section_size = total//section
    twoDims: List[List[str]] = []
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
        '-p', '--pool', type=int, required=True, default=1
    )
    return parser

def serial_log(fileNames: List[str]) -> Tuple[NDArray, NDArray]:
    # prof = cProfile.Profile()
    # prof.enable()
    row = len(fileNames)
    dataArray = np.empty((row, len(S4.dataHead)), dtype=Any)
    debugArray = np.empty((row, len(S4.debugHead)), dtype=Any)
    for idx, fileName in enumerate(tqdm(fileNames)):
        arr, arrDbg = S4.do_parsing(fileName)
        # dataArray[idx] = arr
        # debugArray[idx] = arrDbg
    # prof.disable()
    # prof.dump_stats('{}.pstats'.format(os.getpid()))
    return dataArray, debugArray

def process_logs(pool_size: int):    #np.set_printoptions(linewidth=250)
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    fileNameList = glob.glob(os.path.join(LOG_DIR, logFileGlob))
    fileNameList2D = split_task(fileNameList, pool_size)

    with Pool(pool_size) as p:
        row = len(fileNameList)
        worker_row = len(fileNameList) // pool_size
        dataArray = np.empty((row, len(S4.dataHead)), dtype=Any)
        debugArray = np.empty((row, len(S4.debugHead)), dtype=Any)
        for i, (arr, arrDbg) in enumerate(tqdm(p.imap_unordered(serial_log, fileNameList2D))):
            # dataArray[i*worker_row:(i+1)*worker_row,:] = arr
            # debugArray[i*worker_row:(i+1)*worker_row,:] = arrDbg
            pass
    return dataArray, debugArray

if __name__ == '__main__':
    args = args_parser().parse_args()
    prof = cProfile.Profile()
    prof.enable()
    process_start = datetime.now()
    dataArray, debugArray = process_logs(pool_size=args.pool)
    process_end = datetime.now()
    prof.disable()
    prof.dump_stats('1.pstats')
    print('Process Time Spend: ' + str(process_end - process_start))

    # check report template exists
    
    # if os.path.isfile(REPORT_TEMPLATE):
    #     write_file_start = datetime.now()
    #     reportName = PEPORT_PREFIX + write_file_start.strftime("%Y") + write_file_start.strftime("%m") + write_file_start.strftime("%d") + ".xlsx"
    #     S4.create_report(REPORT_TEMPLATE, reportName, STATION_NAME, [], dataArray, debugArray)
    #     write_file_end = datetime.now()
    #     print('Write File Time Spend: ' + str(write_file_end - write_file_start))
