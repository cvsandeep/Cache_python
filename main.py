# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:12:40 2022

@author: Sandeep
"""
import cache_operation
from enum import Enum


class Cmd(Enum):
    READ_DATA = "0"
    WRITE_DATA = "1"
    READ_INSTRUCTION = "2"
    SNOOPED_INVALIDATE = "3"
    SNOOPED_READ = "4"
    SNOOPED_WRITE = "5"
    SNOOPED_READ_X = "6"
    CLEAR_AND_RESET = "8"
    PRINT_CACHE_LINE = "9"


def main():
    cache = cache_operation.CacheOperation()
    with open("trace.file") as fileObj:
        lines = fileObj.readlines()

    for line in lines:
        command, address = line.split()
        print(command)
        print(address)
        cache.DecodeUpdateAddress(address, command)
        print(Cmd.READ_DATA.value)
        if command == Cmd.READ_DATA.value:
            cache.readData()
            cache.DReadCount()  # CountReads
        elif command == Cmd.WRITE_DATA.value:
            cache.writeData()
            cache.DWriteCount()
        elif command == Cmd.READ_INSTRUCTION.value:
            cache.IReadCount()
            cache.ReadInstruction()
        elif command == Cmd.SNOOPED_INVALIDATE.value:
            cache.SnoopedInvalidate()
        elif command == Cmd.SNOOPED_READ.value:
            cache.SnoopedRead()
        elif command == Cmd.SNOOPED_WRITE.value:
            cache.SnoopedWrite()
        elif command == Cmd.SNOOPED_READ_X.value:
            cache.SnoopedReadX()
        elif command == Cmd.CLEAR_AND_RESET.value:
            cache.ClearAndSet()
        elif command == Cmd.PRINT_CACHE_LINE.value:
            cache.PrintCacheLine()
        else:
            print("Invalid Operation\n")
    cache.CachePerformance()


main()
