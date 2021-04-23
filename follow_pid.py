#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
Usgae:
------
Generic use for all the process that reading files.

Notes:
    * You don't need to run the process to follow in background, you can call this script via another terminal
    * If --pid <pid> is not specify, the script will let the user choose the process (stdin)
    * If --fd <fd> is not specify, the script will choose randomly a file that the process is reading.


Example 2:
----------
> grep word ./big_file > /tmp/res &
28194
> python follow_pid.py --pid 28194
// Show progress bar of reading ./big_file

Example 3:
----------
> grep word ./directory/*
28194
> python follow_pid.py --pid 28194 --size 500
// Show progress bar of reading all the files, which their size is bigger 500Mb

Example 3:
----------
terminal 1> some_process --some_flag
terminal 2> python follow_pid.py
// Let you choose the process to follow, and can identify by its command line.

"""

import platform
from argparser import parsing_arguments
from psutil_utils import *
from utils import units
from time import sleep


def main_loop(p: psutil.Process, fd: int, min_file_size: int, bar_len: int):
    current_file = None
    while True:
        # Checking if pid is finished/terminated during the loop:
        if not psutil.pid_exists(p.pid):
            if current_file:
                current_file.close_progress_bar()
            raise psutil.NoSuchProcess(pid=p.pid)

        # Update bar or get new file to follow:
        if current_file is None:
            current_file = get_new_file(p, fd, min_file_size, bar_len)
        else:
            current_file.update_file_position()
            current_file.update_progress_bar()
            if current_file.is_finish_reading() or current_file.is_file_open() is False:
                current_file.close_progress_bar()
                current_file = None

        sleep(0.1)


def main():
    # Parse args:
    parsed_args = parsing_arguments()
    pid = parsed_args.pid
    fd = parsed_args.fd
    user = parsed_args.user
    min_file_size = parsed_args.size * units.MB
    bar_len = parsed_args.bar_len

    # Check os
    if platform.system().upper() == 'WINDOWS':
        print("-E- Windows doesn't supported")
        return

    # Get pid from user, if pid is undefine:
    if pid is None:
        pid = get_pid_from_user(user=user)

    # Start following the process reading files:
    print("-I- Following PID:" + str(pid) + " ...")
    try:
        p = psutil.Process(pid)
        main_loop(p=p, fd=fd, min_file_size=min_file_size, bar_len=bar_len)
    except IOError as e:
        print('-E- ', e)
    except psutil.AccessDenied:
        print('-E- AccessDenied. pid:', pid)
    except psutil.NoSuchProcess:
        print('-I- Process finished/terminated')
    except Exception as e:
        print(e)
        print('-E- Failed')
    finally:
        print("-I- Finish")


if __name__ == '__main__':
    main()
