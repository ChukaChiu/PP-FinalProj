from pstats import SortKey, Stats
import argparse

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', type=str, required=True, default=None
    )
    return parser

if __name__ == '__main__':
    args = args_parser().parse_args()
    ps = Stats(args.file).sort_stats(SortKey.CUMULATIVE, SortKey.TIME)
    ps.print_stats()