import numpy as np
from datetime import datetime
from numpy.typing import NDArray
import argparse
from tqdm import tqdm
from multiprocessing import Pool
import os

import cProfile

WIDTH = 23

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--count', type=int, required=True
    )
    parser.add_argument(
        '-s', '--section', type=int, required=True
    )
    return parser

def make_data_sheet(height: int) -> NDArray:
    ds = np.empty((0, WIDTH))
    for _ in tqdm(range(0, height)):
        ds = np.vstack((ds, np.ones((1, WIDTH))))
    return ds

def main(work_items: int, worker_num: int):
    with Pool(args.section) as p:
        result = np.empty((0, WIDTH))
        for ds in tqdm(p.imap_unordered(func=make_data_sheet, iterable=[work_items]*worker_num)):
            result = np.vstack((result, ds))

if __name__ == '__main__':
    args = args_parser().parse_args()
    start = datetime.now()
    main(args.count//args.section, args.section)
    end = datetime.now()
    print('Time Spend: ' + str(end - start))