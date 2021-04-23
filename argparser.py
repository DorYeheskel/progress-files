#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
File for parsing the arguments for the main script file

To see the full usage of these arguments, run:
> python follow_pid.py --help

"""

import argparse
import getpass
from utils import clear_colors


def parsing_arguments():
    parser = argparse.ArgumentParser(
        description='Attach to process and see the progress of reading files.')
    args_with_param = [(('--pid', '-pid'),
                        {'help': 'Pid. If none, choose from the avilable pids',
                         'required': False,
                         'type': int}),
                       (('--fd', '-fd'),
                        {'help': 'fd (default : all available fd for read)',
                         'required': False,
                         'type': int}),
                       (('--user', '-user'),
                        {'help': 'If pid is none, choose avilable pids belong to user (default : current user)',
                         'required': False,
                         'type': str,
                         'default': getpass.getuser()}),
                       (('--size', '-size'),
                        {'help': 'Minimum file size to display in Mb (default : 50Mb)',
                         'required': False,
                         'type': int,
                         'default': 50}),
                       (('--bar_len', '-bar_len'),
                        {'help': 'Bar length, as number of cols (default : 100 cols)',
                         'required': False,
                         'type': int,
                         'default': 100,
                         'choices': [50, 75, 100, 125, 150]})]
    args_bool = [(('--color', '-color'), {'help': 'Print paths with color',
                                          'action': 'store_true',
                                          'default': clear_colors()})]
    all_args = args_with_param + args_bool
    for arg in all_args:
        parser.add_argument(*arg[0], **arg[1])
    return parser.parse_args()
