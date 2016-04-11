#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>, Dominik Gresch <greschd@gmx.ch>
# Date:    01.04.2015 12:46:51 CEST
# File:    monitoring.py

import time
import collections

import blessings

from fsc.export import export
#~ from .io_manip import ms_time_str

@export
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
            print('{t.green}{}: {t.green_bold}{:.5f}s{t.normal}'.format(
                self.name, self.time, t=blessings.Terminal()))


@export
class monitored(object):
    """TODO"""
    def __init__(self, seq, name="unknown"):
        self.seq = seq
        self.name = name
        self.term = blessings.Terminal()

    def __iter__(self):
        print(self.term.green(self.name))
        print("--- initializing progress bar ---")
        N = len(self)
        Sample = collections.namedtuple('Sample', ['idx', 'time'])
        samples = collections.deque(maxlen=10)
        

        n_len = str(len(str(N)))
        format_str = "{t.move_up}{t.clear_eol}({:>" + n_len + \
            "}/{}) {} {t.yellow}done in {t.yellow_bold}{}{t.normal}"

        with timed(verbose=False) as t:
            last_idx = 0
            passed = 0
            for idx, x in enumerate(self.seq):
                passed = t.time - passed 
                if passed > 1:
                    samples.append(Sample(idx=(idx - last_idx), time=passed))
                    last_idx = idx
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
                        t=self.term
                    ))

                yield x

        print("{t.move_up}{t.clear_eol}({}/{}) {} {t.green}done in {t.green_bold}{}{t.normal}".format(
            N,
            N,
            progress_bar(1),
            ms_time_str(t.time),
            t=self.term
        ))

    def __len__(self):
        return len(self.seq)
