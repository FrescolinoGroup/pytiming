#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    11.04.2016 11:50:14 CEST
# File:    test_monitored.py

import time
import pytest

from fsc.timing import monitored

def test_monitored():
    for _ in monitored(range(10)):
        time.sleep(1)
