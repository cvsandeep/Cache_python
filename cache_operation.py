# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:35:32 2022

@author: venksand
"""
import math
import cache_memory

class CacheOperation:
    __MesiState  = ("I", "S", "E", "M")
    __dirty_str  = (" ", "D")

    def __init__(self):
        self.line_size = 64
        self.associativity = 8
        self.cache_lines = 256
        self.__sets = int(self.cache_lines / self.associativity)
        self.__lines = int(math.log2(self.line_size))
        self.__set = int(math.log2(self.__sets))
        self.__op = -1
        self.offset = 0
        self.__L2 = cache_memory.N_CACHE(self.__sets)

    def DecodeUpdateAddress(self, address, command):
        self.__op = command
        self.offset = address & ((1 << self.__lines) - 1)
        set_index = address >> self.__lines & ((1 << self.__set) - 1)
        tag = address >> (self.__lines + self.__set) & ((1 << (32 - (self.__lines + self.__set))) - 1)
        # debugLog(CACHEOP, __func__, "*******************************************************************");
        # sprintf(msgOut, "Address 0x%x ; Offset 0x%x; set_index 0x%x; tag 0x%x  ", addr, offset, set_index, tag);
        # debugLog(CACHEOP, __func__, msgOut);
        # debugLog(CACHEOP, __func__, "*******************************************************************");

    def ReIntializeCache(self):
        for set in range(self.__sets):
            for plru in range(7):
                self.__L2.set[set].PLRU[plru] = 0

    def readData(self): print("")
    def writeData(self): print("")
    def ReadInstruction(self): print("")
    def SnoopedInvalidate(self): print("")
    def SnoopedRead(self): print("")
    def SnoopedWrite(self): print("")
    def SnoopedReadX(self): print("")
    def ClearAndSet(self): print("")
    def PrintCacheLine(self): print("")
