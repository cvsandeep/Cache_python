# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:35:32 2022

@author: venksand
"""
import math
import cache_memory
from bus_operation import BusOperation
from cache_performance import CachePerformance
from cache_types import Cmd, OperationType, SnoopType, MessageType, StateType


class CacheOperation(BusOperation, CachePerformance):
    __MesiState = ("I", "S", "E", "M")
    __dirty_str = (" ", "D")

    def __init__(self):
        self.tag = None
        self.line_size = 64
        self.associativity = 8
        self.cache_lines = 256
        self.__sets = int(self.cache_lines / self.associativity)
        self.__lines = int(math.log2(self.line_size))
        self.__set = int(math.log2(self.__sets))
        self.__op: int = -1
        self.__addr = 0
        self.offset = 0
        self.set_index = 0
        self.__L2 = cache_memory.N_CACHE(self.__sets)

    def DecodeUpdateAddress(self, address: int, command: int):
        self.__op = command
        self.__addr = address
        self.offset = address & ((1 << self.__lines) - 1)
        self.set_index = address >> self.__lines & ((1 << self.__set) - 1)
        self.tag = address >> (self.__lines + self.__set) & ((1 << (32 - (self.__lines + self.__set))) - 1)
        # ##debugLog(CACHEop, __func__, "*******************************************************************")
        # msgout = "Address 0x%x  Offset 0x%x self.set_index 0x%x tag 0x%x  ", addr, offset, self.set_index, tag)
        # ##debugLog(CACHEop, __func__, msgOut)
        # ##debugLog(CACHEop, __func__, "*******************************************************************")

    def ReIntializeCache(self):
        for set in range(self.__sets):
            for plru in range(7):
                self.__L2.set[set].PLRU[plru] = 0

    def readData(self):
        evict = 1
        way = 0
        # debugLog(CACHEopX,__func__,"")
        for w in range(self.associativity):
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    self.HitCount()
                    if (self.__op == Cmd.WRITE_DATA):
                        self.__UpdateMESIstate(OperationType.RWIM, w)
                    else:
                        self.__UpdateMESIstate(OperationType.READ, w)
                    self.__UpdatePLRU(self.set_index, w)
                    return
            else:
                if (evict == 1):
                    evict = 0
                    way = w

        # debugLog(CACHEop,__func__, "Data not found in the cache line")

        if (evict):
            # debugLog(CACHEopX,__func__, "Evicting")
            way = self.__WhichWay(self.set_index)
            self.__VoidWay(way)
            self.__EvictCount()
        else:
            self.MissCount()

        msgout = "Set-%d Way-%d Tag-0x%08x" % (self.set_index, way, self.tag)
        # debugLog(CACHEop,__func__,msgOut)
        self.__L2.set[self.set_index].way[way].valid = 1
        self.__L2.set[self.set_index].way[way].dirty = 0
        self.__L2.set[self.set_index].way[way].tag = self.tag
        self.__L2.set[self.set_index].way[way].MESI_state = StateType.INVALID
        if (self.__op == Cmd.WRITE_DATA):
            self.__UpdateMESIstate(OperationType.RWIM, way)
            # MessageToCache(MessageType.GETLINE,self.__addr)
            self.__L2.set[self.set_index].way[way].dirty = 1
        else:
            self.__UpdateMESIstate(OperationType.READ, way)

        self.__UpdatePLRU(self.set_index, way)

    def writeData(self):
        way = 0
        # debugLog(CACHEopX,__func__,"")
        ##debugLog(1,__func__, msgOut)
        for w in range(self.associativity):
            way = w
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    break  # Return data
        if (way == self.associativity):
            self.readData()  # Should this increase any Counts?
        else:
            self.HitCount()
            self.__UpdatePLRU(self.set_index, w)
            self.__UpdateMESIstate(OperationType.WRITE, w)
            self.__L2.set[self.set_index].way[w].dirty = 1

    def ReadInstruction(self):
        # debugLog(2,__func__,"")
        self.readData()

    def SnoopedInvalidate(self):
        for w in range(self.associativity):
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    self.UpdateMESIstateSnoop(OperationType.INVALIDATE, w)
                    # __UpdatePLRU(self.set_index,w)
                    return  # Return data

    def SnoopedRead(self):
        for w in range(self.associativity):
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    self.UpdateMESIstateSnoop(OperationType.READ, w)
                    # __UpdatePLRU(self.set_index,w)

                    return  # Return data
        # debugLog(CACHEopX, __func__, "Data not Found")

    def SnoopedWrite(self):
        for w in range(self.associativity):
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    self.UpdateMESIstateSnoop(OperationType.WRITE,
                                         w)  # No need as there are no any operations for OperationType.WRITE.
                    # __UpdatePLRU(self.set_index,w)
                    return  # Return data

    # debugLog(CACHEopX, __func__, "Data not Found")
    def SnoopedReadX(self):
        for w in range(self.associativity):
            if (self.__L2.set[self.set_index].way[w].valid == 1):  # Check data is valid
                if (self.__L2.set[self.set_index].way[w].tag == self.tag):  # Check tag
                    # debugLog(CACHEop,__func__, "Data found")
                    UpdateMESIstateSnoop(OperationType.RWIM, w)
                    # __UpdatePLRU(self.set_index,w)
                    return  # Return data

        # debugLog(CACHEopX, __func__, "Data not Found")

    def ClearAndSet(self):
        # debugLog(CACHEopX, __func__, "")
        for set in range(self.__sets):
            self.set_index = set
            for w in range(self.associativity):
                self.__VoidWay(w)
                for lru in range(7):
                    self.__L2.set[set].PLRU[lru] = 0

    def PrintCacheLine(self):
        set_filled = 0
        msgOut = " "
        # debugLog(CACHEopX, __func__, "")
        for set in range(self.__sets):
            set_filled = 0
            msgout = "Set-%d:PLRU-" % (set)
            for lru in range(7):
                buf = "%d" % (self.__L2.set[set].PLRU[lru])
                msgout = msgout + buf

            for w in range(self.associativity):
                if (self.__L2.set[set].way[w].valid == 1):  # Check data is valid
                    # len += sizeof(msgOut)
                    buf = " Way-%d: 0x%08x,%s %s" % (
                        w, self.__L2.set[set].way[w].tag, self.__dirty_str[self.__L2.set[set].way[w].dirty],
                        self.__MesiState[self.__L2.set[set].way[w].MESI_state])
                    set_filled = 1

                else:
                    buf = " Way-%d:  -------- ,  I" % (w)

                msgout = msgout + buf

            if (set_filled):
                print("")
                # debugLog(0,__func__, msgOut)

    def __UpdatePLRU(self, set, w):
        """
        This is called during OperationType.WRITE and OperationType.READ for updating PLRU bits
         for 4 and 8 way associative only
        """
        msgOut = "PLRU Bits "
        for lru in range(7):
            msgOut = msgOut + str(self.__L2.set[set].PLRU[lru])
        if self.associativity == 8:
            if w == 0:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 0
                self.__L2.set[set].PLRU[3] = 0
            if w == 1:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 0
                self.__L2.set[set].PLRU[3] = 1
            if w == 2:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 1
                self.__L2.set[set].PLRU[4] = 0
            if w == 3:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 1
                self.__L2.set[set].PLRU[4] = 1
            if w == 4:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 0
                self.__L2.set[set].PLRU[5] = 0
            if w == 5:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 0
                self.__L2.set[set].PLRU[5] = 1
            if w == 6:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 1
                self.__L2.set[set].PLRU[6] = 0
            if w == 7:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 1
                self.__L2.set[set].PLRU[6] = 1

        elif self.associativity == 4:
            if w == 0:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 0
            if w == 1:
                self.__L2.set[set].PLRU[0] = 0
                self.__L2.set[set].PLRU[1] = 1
            if w == 2:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 0
            if w == 3:
                self.__L2.set[set].PLRU[0] = 1
                self.__L2.set[set].PLRU[2] = 1
            msgOut = " Updated To "
        for lru in range(7):
            buf = self.__L2.set[set].PLRU[lru]
            msgOut = buf

    ###debugLog(CACHEopX,__func__, msgOut)

    # """
    #  * This is called to find which way we need to evict
    # """
    def __WhichWay(self, set):
        ###debugLog(CACHEop, __func__, "Evicting")
        if (self.associativity == 8):
            if (self.__L2.set[set].PLRU[0] == 0):
                if (self.__L2.set[set].PLRU[2] == 0):
                    if (self.__L2.set[set].PLRU[6] == 0):
                        return 7
                    else:
                        return 6
                else:
                    if (self.__L2.set[set].PLRU[5] == 0):
                        return 5
                    else:
                        return 4
            else:
                if (self.__L2.set[set].PLRU[1] == 0):
                    if (self.__L2.set[set].PLRU[4] == 0):
                        return 3
                    else:
                        return 2
                else:
                    if (self.__L2.set[set].PLRU[3] == 0):
                        return 1
                    else:
                        return 0
        elif (self.associativity == 4):
            if (self.__L2.set[set].PLRU[0] == 0):
                if (self.__L2.set[set].PLRU[1] == 0):
                    return 3
                else:
                    return 2
            else:
                if (self.__L2.set[set].PLRU[1] == 0):
                    return 1
                else:
                    return 0
        else:
            ###debugLog(CACHEop, __func__, "Not supported")
            return -1

    def __VoidWay(self, way):
        ###debugLog(CACHEopX, __func__, "")
        if (self.__L2.set[self.set_index].way[way].valid == 1):
            if (self.__L2.set[self.set_index].way[way].MESI_state == StateType.MODEFIED):
                self.MessageToCache(MessageType.GETLINE, self.__L2.set[self.set_index].way[way].tag)
            # Getting the line from L1 to check weather its dirty or not
            if (self.__op < 3):  # #Means Evicting
                self.MessageToCache(MessageType.EVICTLINE, self.__L2.set[self.set_index].way[way].tag)
            else:
                # May be need to do this only in StateType.SHARED state.
                self.MessageToCache(MessageType.INVALIDATELINE, self.__L2.set[self.set_index].way[way].tag)
            self.__L2.set[self.set_index].way[way].MESI_state = StateType.INVALID
            if (self.__L2.set[self.set_index].way[way].dirty == 1):
                self.__Flush(way)
        self.__L2.set[self.set_index].way[way].valid = 0
        self.__L2.set[self.set_index].way[way].dirty = 0
        self.__L2.set[self.set_index].way[way].MESI_state = 0
        self.__L2.set[self.set_index].way[way].tag = 0

    # """
    #  * This is used when flush data is required.
    #  * Flushes the data to the DRAM through bus.
    # """
    def __Flush(self, way):
        ###debugLog(CACHEop, __func__, "")
        if (self.__L2.set[self.set_index].way[way].MESI_state == StateType.MODEFIED):
            self.MessageToCache(MessageType.GETLINE, self.__L2.set[self.set_index].way[way].tag)
        # Getting the line from L1 to check weather its dirty or not
        self.Busoperation(OperationType.WRITE, self.__addr, SnoopType.HITM)
        self.__L2.set[self.set_index].way[way].dirty = 0

    # """
    #  * This is used to update the MESI state for all the transactions
    #  * And also performs relevant bus operation.
    # """
    def __UpdateMESIstate(self, optype, way):
        state = self.__L2.set[self.set_index].way[way].MESI_state
        if state == StateType.INVALID:
            if (optype == OperationType.READ):
                res = self.GetSnoopResult(self.__addr)
                self.Busoperation(OperationType.READ, self.__addr, res)
                # OperationType.READ from DRAM
                if (res == SnoopType.HIT or res == SnoopType.HITM):
                    self.__L2.set[self.set_index].way[way].MESI_state = StateType.SHARED
                elif (res == SnoopType.NOHIT):
                    self.__L2.set[self.set_index].way[way].MESI_state = StateType.EXCLUSIVE

            elif (optype == OperationType.WRITE or optype == OperationType.RWIM):
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.MODEFIED
                self.Busoperation(OperationType.RWIM, addr, GetSnoopResult(self.__addr))
                # Send readX command to bus
                # First Time OperationType.WRITE

            self.MessageToCache(MessageType.SENDLINE, self.__addr)  # Sends data to L1

        elif state == StateType.SHARED:
            if (optype == OperationType.READ):
                self.MessageToCache(MessageType.SENDLINE, self.__addr)  # Sends data to L1
            else:
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.MODEFIED
                self.Busoperation(OperationType.INVALIDATE, self.__addr, SnoopType.HITM)
                # Send BusUpgr command to bus
                # First Time OperationType.WRITE

        elif state == StateType.EXCLUSIVE:
            if (optype == OperationType.WRITE):
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.MODEFIED
                # First Time OperationType.WRITE
            elif (optype == OperationType.READ):
                self.MessageToCache(MessageType.SENDLINE, self.__addr)  # Sends data to L1

        elif state == StateType.MODEFIED:
            if (optype == OperationType.READ):
                self.MessageToCache(MessageType.SENDLINE, self.__addr)  # Sends data to L1

            # OperationType.WRITE dosent happens as L1 can only be in StateType.EXCLUSIVE or StateType.SHARED state when self.__L2 is in StateType.MODEFIED state.
        msgOut = "%s->%s" % (
            self.__MesiState[state], self.__MesiState[self.__L2.set[self.set_index].way[way].MESI_state])
        ##debugLog(CACHEop,__func__, msgOut)

    def UpdateMESIstateSnoop(self, this_type, way):
        state = self.__L2.set[self.set_index].way[way].MESI_state
        if state == StateType.INVALID:
            self.PutSnoopResult(self.__addr, SnoopType.NOHIT)

        elif state == StateType.SHARED:
            self.PutSnoopResult(self.__addr, SnoopType.HIT)
            # HitCount()
            if (
                    this_type == OperationType.WRITE or this_type == OperationType.RWIM or this_type == OperationType.INVALIDATE):
                self.__VoidWay(way)
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.INVALID

        elif state == StateType.EXCLUSIVE:
            self.PutSnoopResult(self.__addr, SnoopType.HIT)
            # HitCount()
            if (this_type == OperationType.RWIM or this_type == OperationType.INVALIDATE):
                self.__VoidWay(way)
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.INVALID
            elif (this_type == OperationType.READ):
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.SHARED

        elif state == StateType.MODEFIED:
            self.PutSnoopResult(self.__addr, SnoopType.HITM)
            # HitModifiedLineCount()
            if (this_type == OperationType.READ):
                self.__Flush(way)
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.SHARED
            elif (this_type == OperationType.RWIM or this_type == OperationType.INVALIDATE):
                self.__VoidWay(way)
                self.__L2.set[self.set_index].way[way].MESI_state = StateType.INVALID
        msgOut = "%s->%s" % (
            self.__MesiState[state], self.__MesiState[self.__L2.set[self.set_index].way[way].MESI_state])
        ##debugLog(CACHEop,__func__, msgOut)
