import argparse
import os
from .crawler import find_files, process
DOCKER_DETECT = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
import logging
logger = logging.getLogger('pycat')
# logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)


def crawl(crawl_path):
    files = find_files(crawl_path)
    for file in process(files):
        print(file)

def cli():
    """
    CLI Should have the following subcommands
    crawl

    server

    proc


    :return:
    """
    parent_parser = argparse.ArgumentParser(description="The parent parser")
    # parent_parser.add_argument("-p", type=int, required=True,
    #                            help="set db parameter")

    subparsers = parent_parser.add_subparsers(title="tools", dest="command", required=True)

    parser_crawl = subparsers.add_parser("crawl")

    parser_crawl.add_argument('system_name', type=str, help="System identifier")
    #
    parser_crawl.add_argument("--crawl_path", default='/mnt/crawldir' if DOCKER_DETECT else None)

    parser_crawl.add_argument("-o", "--outfile"
                              , default='/mnt/crawldir/crawl.txt' if DOCKER_DETECT else None
                              , help='outfile path relative to '
                              )

    if DOCKER_DETECT:
        logger.info("Running in Docker")

    args = parent_parser.parse_args()

    logger.info(args)
    if args.command == 'crawl':
        crawl(args.crawl_path)

    # print(args.accumulate(args.integers))
