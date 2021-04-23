#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
Utility file.

"""

import os
import psutil
import tqdm
from utils import bcolors
from file_info import FileInfo


def get_all_processes_by_user(user: str):
    process_map = dict()
    for proc in psutil.process_iter():
        if proc.username() != user:
            continue
        cmd_line = ' '.join(proc.cmdline())
        pid = proc.pid
        process_map[int(proc.create_time())] = (cmd_line, pid)
    return process_map


def get_all_processes(user: str):
    # Get all processes belong to user:
    proc_list = reversed(list(get_all_processes_by_user(user=user).values()))
    processes_map = dict()
    print("-I- Available processes:")
    for idx, (cmd_line, pid) in enumerate(proc_list, start=1):
        print(idx, " :", cmd_line, "(PID:" + str(pid) + ")")
        processes_map[idx] = pid
    print('0  : exit')
    return processes_map


def get_pid_from_user(user: str):
    # Loop until user choose a process:
    processes_map = get_all_processes(user)
    while True:
        print('-------------------------')
        idx = input('-I- Choose process: ')
        if not (idx.isdigit()):
            print('-E- Value should be number')
            continue
        idx = int(idx)
        if idx in processes_map:
            pid = processes_map[idx]
            return pid
        elif idx == 0:
            exit(-1)
        else:
            print('-E- Wrong number')


def create_file_info(p: psutil.Process, file, bar_len: int) -> FileInfo:
    tqdm.tqdm.write('-I- Read  : ' + bcolors.WARNING + file.path + bcolors.ENDC)
    file_position = file.position
    file_size = os.path.getsize(file.path)
    return FileInfo(p=p,
                    path=file.path,
                    position=file_position,
                    old_position=file_position,
                    size=file_size,
                    bar_len=bar_len)


def get_new_file(p: psutil.Process, fd: int, min_file_size: int, bar_len: int) -> FileInfo:
    # Get the FileInfo instance:
    for file in p.open_files():
        if fd is not None and file.fd != fd:
            continue
        if file.mode != 'r':
            continue
        file_size = os.path.getsize(file.path)
        if file_size < min_file_size:
            continue
        if file.position == file_size:
            continue
        return create_file_info(p, file, bar_len)
