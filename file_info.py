#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Dor Yeheskel. All rights reserved.

"""
API for FileInfo.

"""

import tqdm
import time
from utils import display_time


class FileInfo:
    """
    Class that by given process and file_path that the process read,
    print a progress bar of the reading.
    """

    def __init__(self, p, path, position, old_position, size, bar_len) -> None:
        super().__init__()
        self.p = p
        self.path: str = path
        self.position: int = position
        self.old_position: int = old_position
        self.size: int = size
        self.status = self.get_process_status(p)
        self.bar: tqdm.tqdm = self.create_progress_bar(bar_len)
        self.current_start_time = time.time()
        self.eta = -1
        self.eta_str = '?'
        self.bar_idx = 1

    def is_finish_reading(self):
        if self.position >= self.size:
            return True
        return False

    def is_file_open(self):
        open_files_list = self.get_open_files(self.p)
        for file in open_files_list:
            if file.path == self.path:
                return True
        return False

    def get_time_between_updates(self):
        current_end_time = time.time()
        time_between_updates = current_end_time - self.current_start_time
        self.current_start_time = time.time()
        return time_between_updates

    def update_file_position(self):
        self.old_position = self.position
        open_files_list = self.get_open_files(self.p)
        for file in open_files_list:
            if file.path == self.path:
                self.position = file.position

    def update_eta_of_file(self, step):
        time_between_updates = self.get_time_between_updates()
        if step == 0 and self.position != self.size:
            self.eta = 0
            self.eta_str = 'Done'
        else:
            byte_rate = step / time_between_updates  # step = 100, total_time = 20sec
            bytes_that_left = self.size - self.position  # 1000 - 400        # byte_rate is 5 (5 bytes per sec)
            self.eta = bytes_that_left / byte_rate  # 600/5 = 150sec
            self.eta_str = display_time(self.eta)
            if self.eta_str == '':
                self.eta_str = 'almost done'

    def create_progress_bar(self, bar_len):
        desc = "-I- Status: " + self.status
        r_bar = '| {n_fmt}/{total_fmt} [eta: {unit}]'
        bar_format = "{l_bar}{bar}" + r_bar
        bar_obj = tqdm.tqdm(total=self.size, initial=self.position, unit_scale=True, ncols=bar_len,
                            desc=desc, bar_format=bar_format)
        return bar_obj

    def update_progress_bar(self):
        step = self.position - self.old_position
        self.update_eta_of_file(step)
        self.bar.set_description_str("-I- Status: " + self.get_process_status(self.p))
        self.bar.unit = self.eta_str
        self.bar.update(step)
        self.bar.refresh()
        self.bar_idx += 1

    def close_progress_bar(self):
        self.bar.set_postfix_str('Done', refresh=False)
        self.bar.update(self.size - self.position)
        self.bar.refresh()
        self.bar.close()

    @staticmethod
    def get_process_status(p) -> str:
        status = p.status().upper()
        add_spaces = 12 - len(status)
        status = status + ' ' * add_spaces
        return status

    @staticmethod
    def get_open_files(p):
        open_files = p.open_files()
        return open_files

    def __str__(self):
        """
        Print the instance (for debug)
        """
        return '' + \
               str(self.bar_idx) + ' - ' + \
               'Total: ' + str(self.size) + ' | ' + \
               'Pos: ' + str(self.position) + ' | ' + \
               'O_Pos: ' + str(self.old_position) + ' | ' + \
               'Left: ' + str(self.size - self.position) + ' | ' + \
               'Eta: ' + str(self.eta) + 's | ' + \
               'Status: ' + self.status

    def __eq__(self, other):
        return self.path == other.path and self.p == other.p
