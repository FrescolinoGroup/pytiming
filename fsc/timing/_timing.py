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
    """TODO"""
    def __init__(self, seq, name="unknown"):
        self.seq = seq
        self.name = name

    def __iter__(self):
        print(green(self.name))
        print("--- initializing progress bar ---")
        N = len(self)
        Sample = collections.namedtuple('Sample', ['idx', 'time'])
        samples = collections.deque(
            Sample(idx=0, time=0) for _ in range(10)
        )
        
        last_idx = 0

        n_len = str(len(str(N)))
        format_str = "{renter}({:>" + n_len + \
            "}/{}) {} {yellow}done in {yellowb}{}{none}"

        with timed(verbose=False) as t:
            for idx, x in enumerate(self.seq):
                passed = t.time
                if passed > 1:
                    samples.rotate(-1)
                    samples[-1] = Sample([(idx - last_idx), passed]
                    last_idx = idx
                    t.reset()
                    idx_per_sec = (
                        sum(s.idx for s in samples) / 
                        sum(s.time for s in samples)
                    )

                    predict = (N - idx) / idx_per_sec

                    print(format_str.format(
                        idx + 1,
                        N,
                        progress_bar((idx + 1.0) / N),
                        ms_time_str(predict),
                        **color
                    ))

                yield x

        print("{renter}({}/{}) {} {green}done in {greenb}{}{none}".format(
            N,
            N,
            progress_bar(1),
            ms_time_str(t.time),
            **color
        ))

    def __len__(self):
        return len(self.seq)
