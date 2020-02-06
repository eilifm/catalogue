import argparse
import os

def cli():
    parser = argparse.ArgumentParser(description='Crawl Filesystem')
    parser.add_argument('system_name', type=str)

    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    args = parser.parse_args()
    # print(args.accumulate(args.integers))
