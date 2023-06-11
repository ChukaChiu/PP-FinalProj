#!/usr/bin/env python3

import glob
import os
import random
from tqdm import tqdm

LOG_DIR = './logs'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

LOG_DUPLICATE_DIR = './logs_dup'

REPORT_TEMPLATE = "LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

DUP_COUNT = int(20000)

if __name__ == '__main__':
    fileContents = []
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    for fileName in glob.glob(os.path.join(LOG_DIR, logFileGlob)):
        with open(fileName, 'r') as file:
            fileContents.append(file.read())

    sampleCount = len(fileContents)

    # make duplicate dir 
    if not os.path.isdir(LOG_DUPLICATE_DIR):
        os.makedirs(LOG_DUPLICATE_DIR)

    for count in tqdm(range(1, DUP_COUNT+1)):
        fileName = '{}_{}_LR{:010d}.log'.format(MODEL_NAME, STATION_NAME, count)
        with open(file=os.path.join(LOG_DUPLICATE_DIR, fileName), mode='w') as file:
            file.write(fileContents[random.randrange(sampleCount)])
