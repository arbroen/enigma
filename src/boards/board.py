#!/usr/bin/python
# -*- coding: utf8 -*-
from ..parameters import LimitedIntegerParameter


class GameBoard:
    """
    Limiting the GameBoard size since this will most likely impact performance
    most.
    """
    width = LimitedIntegerParameter(minimal=32, maximum=256, default=64)
    height = LimitedIntegerParameter(minimal=32, maximum=256, default=64)
