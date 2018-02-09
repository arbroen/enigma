#!/usr/bin/python
# -*- coding: utf8 -*-
from ..parameters import LimitedIntegerParameter


class GameBoard:
    """
    Limiting the GameBoard size since this will most likely impact performance
    most.

    A board consists of width x height Area's.
    """
    width = LimitedIntegerParameter(minimal=32, maximum=256, default=64)
    height = LimitedIntegerParameter(minimal=32, maximum=256, default=64)
