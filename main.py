# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:12:40 2022

@author: Sandeep
"""
import cache_operation
import cache_performance
from cache_types import Cmd

file = "trace1.txt"


def main():
    global file
    cache = cache_operation.CacheOperation()
    cache.ReIntializeCache()
    with open(file) as fileObj:
        lines = fileObj.readlines()

    for line in lines:
        command, address = line.split()
        address = int(address, 16)
        command = int(command)
        cache_performance.CachePerformance.op = command
        cache.DecodeUpdateAddress(address, command)
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
    cache.CachePerformanceResult()


main()
