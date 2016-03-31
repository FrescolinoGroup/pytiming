#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>, Dominik Gresch <greschd@gmx.ch>
# Date:    01.04.2015 12:46:51 CEST
# File:    monitoring.py

import time
import collections

from fsc.termcolor import *
from .io_manip import ms_time_str

__all__ = ['timed', "monitored"]


class timed(object):
    """
    Context manager for timing
    """

    def __init__(self, name='timed', verbose=True):
        self.name = name
        self.verbose = verbose
        self._start = None
        self._end = None

    @property
    def time(self):
        if self._end is not None:
            return self._end - self._start
        else:
            return time.time() - self._start

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, type_, value, traceback):
        self._end = time.time()
        if self.verbose:
            print('{green}{}: {greenb}{:.5f}s{none}'.format(
                self.descr, self.time, **color))


class monitored(object):

    def __init__(self, seq, name="unknown"):
        self.seq = seq
        self.name = name

    def __iter__(self):
        GREENB(self.name)
        print("--- initializing progress bar ---")
        N = len(self)
        eta = collections.deque()
        max_eta = 10
        last_i_x = 0
        for i in range(max_eta):
            eta.append([0, 0])

        n_len = str(len(str(N)))
        format_str = "{renter}({:>" + n_len + \
            "}/{}) {} {yellow}done in {yellowb}{}{none}"

        with timer(silent=True) as t:
            for i_x, x in enumerate(self.seq):
                passed = t.watch
                if passed > 1:
                    p = (i_x + 1.0) / N

                    eta.rotate(-1)
                    eta[-1] = [(i_x - last_i_x), passed]
                    last_i_x = i_x
                    t.reset()
                    idx_per_sec = sum([e[0] for e in eta]) / \
                        sum([e[1] for e in eta])

                    predict = (N - i_x) / idx_per_sec

                    print(format_str.format(i_x + 1, N, progress_bar(p), ms_time_str(predict), **color)
                          )

                yield x

        print("{renter}({}/{}) {} {green}done in {greenb}{}{none}".format(N, N, progress_bar(1), ms_time_str(t.time), **color)
              )

    def __len__(self):
        return len(self.seq)
