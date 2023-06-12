from datetime import datetime
import os
import glob

import S4

LOG_DIR = '../logs_dup'
LOG_EXT = 'log'
MODEL_NAME = 'LWR-X8460A'
STATION_NAME = 'S4'

REPORT_TEMPLATE = "./LWR-X8460_mp_data_empty.xlsx"
PEPORT_PREFIX = "LWR-X8460_mp_data_"

if __name__ == '__main__':
    firstTime = True
    logFileGlob = '{}_{}_*.{}'.format(MODEL_NAME, STATION_NAME, LOG_EXT)
    fileNameList = glob.glob(os.path.join(LOG_DIR, logFileGlob))
    timeStart = datetime.now()

    #np.set_printoptions(linewidth=250)
    for file in fileNameList:
        if firstTime:
            headArray = S4.get_info(file)
            dataArray = S4.dataHead
            debugArray = S4.debugHead
        arr, arrDbg = S4.do_parsing(file)
        dataArray = list(zip(dataArray, arr))
        debugArray = list(zip(debugArray, arrDbg))
        firstTime = False

        # check report template exists
    if os.path.isfile(REPORT_TEMPLATE):
        now = datetime.now()
        reportName = PEPORT_PREFIX + now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + ".xlsx"
        # S4.create_report(REPORT_TEMPLATE, reportName, STATION_NAME, [], dataArray, debugArray)

    timeEnd = datetime.now()
    print('Time Spend: ' + str(timeEnd - timeStart))