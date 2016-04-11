#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    11.04.2016 11:22:54 CEST
# File:    test_timed.py

import re
import time
from io import StringIO
from contextlib import redirect_stdout

import pytest

from fsc.timing import timed

def test_timed():
    out = StringIO()
    with redirect_stdout(out), timed('foo'):
        time.sleep(0.1)
    out.seek(0)
    out = out.read()
    assert re.match('foo: 0.1[\d]+s', out)
