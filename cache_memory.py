# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:12:40 2022

@author: Sandeep
"""


class CACHE_LINE:
    def __init__(self):
        self.valid = 0
        self.dirty = 0
        self.MESI_state = 0
        self.tag = 0


class CACHE_SET_8_WAY:
    def __init__(self):
        self.way = []
        self.PLRU = []
        for x in range(8):
            self.way.append(CACHE_LINE())
        for x in range(7):
            self.PLRU.append(0)


class N_CACHE:
    def __init__(self, sets):
        self.set = []
        for x in range(sets):
            self.set.append(CACHE_SET_8_WAY())

