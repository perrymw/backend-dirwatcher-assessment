#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dirwatcher - Long Running Program.
A program that watches a given directory for a specified word and also
notifies of any changes to given directory
"""
__author__ = "perrymw with guidance from astephens91"

import signal
import logging
import argparse
import os
import time
import datetime

"""Global Variables"""
exit_flag = False
logger = logging.getLogger(__file__)
magic_text_position = {}

"""Watch directory(args) and logs when files are at all changed in the
directory. Call magic_word_find to search for magic word"""


def dirwatch(args):
    global logger
    global magic_text_position
    # access all created arguments from argparse
    logger.info("Watching directory: {1}\nFile Extension: {0}\n"
                "Magic Text: {2}\nPolling at {3} seconds."
                .format(args.extension, args.dir, args.magic, args.interval))
    absolute_path_directory = os.path.abspath(args.dir)
    files_inside_directory = os.listdir(absolute_path_directory)
    found_files = []
    for files in files_inside_directory:
        if files not in found_files and files.endswith(args.extension):
            # if this is a new file, then log message
            found_files.append(files)
            logger.info("Found file: {}".format(files))
            magic_text_position[files] = 0
    for files in found_files:
        if files not in files_inside_directory:
            found_files.remove(files)
            logger.info("File {} has been removed".format(files))
            del magic_text_position[files]
    for files in found_files:
        magic_word_find(files, args.magic, absolute_path_directory)


def magic_word_find(filename, text, directory):
    global logger
    global magic_text_position
    with open(directory + '/' + filename) as f:
        for line_number, line in enumerate(f.readlines(), 1):
            if text in line and line_number > magic_text_position[filename]:
                logger.info("{} was found on {}".format(text, line_number))
            if line_number > magic_text_position[filename]:
                magic_text_position[filename] += 1


def create_logger():
    """Set up Logger"""
    global logger
    logging.basicConfig(format='%(asctime)s.%(msecs)03d -%(name)s -'
                               '%(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT.
    Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop
    if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global logger
    global exit_flag
    # log the associated signal name (the python3 way)
    # logger.warn('Received ' + signal.Signals(sig_num).name)
    # log the signal name (the python2 way)
    signames = dict((k, v) for v, k in reversed(
                sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signames[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True


def create_parser():
    parser = argparse.ArgumentParser()
    # 1) searched file extension
    parser.add_argument('-e', '--extension', type=str, default='.txt',
                        help='file extension to search for')
    # 2)directory searching
    parser.add_argument('dir', type=str, help='searches directory')
    # 3)magic word
    parser.add_argument('magic', type=str, help='text we are searching for')
    # 4)
    parser.add_argument('-i', '--interval', type=float, default=3,
                        help='interval time between polling for the'
                        'directory and the text')
    return parser


def main():
    create_logger()
    # Hook these two signals from the OS ..
    global exit_flag
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    # Set up parser
    parser = create_parser()
    args = parser.parse_args()

    # App start up time
    app_start = datetime.datetime.now()
    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        "                       {0} Started\n"
        "                        (ﾉ´･ω･)ﾉ ﾐ ┸━┸\n"
        "                       Started at {1}\n"
        "-------------------------------------------------------------------\n"
        .format(__file__, app_start.isoformat())
    )
    while not exit_flag:
        try:
            # call my directory watching function..
            dirwatch(args)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.exception("Unhandled exception: {}".format(e))
        except OSError:
            logger.exception('Directory does not exist')
            time.sleep(args.interval*2)
        except KeyboardInterrupt:
            exit_flag = True
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        # time.sleep(polling_interval)
        time.sleep(args.interval)
    # final exit point happens here
    # Log a message that we are shutting down
    up_time = str(datetime.datetime.now() - app_start)
    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        "                    {0} Ended\n"
        "                       ┬─┬ノ( º _ ºノ)\n"
        "                    Ended at {1}\n"
        "-------------------------------------------------------------------\n"
        .format(__file__, up_time)
    )
    # Include the overall uptime since program start.


if __name__ == '__main__':
    main()
