from logger import Logger
from cache_types import Cmd

class CachePerformance():
    PERFORMANCE = 0
    op = -1
    __IreadHitCount: int = 0
    __DreadHitCount: int = 0
    __DwriteHitCount: int = 0
    __IreadMissCount: int = 0
    __DreadMissCount: int = 0
    __DwriteMissCount: int = 0
    __IreadMissEvictCount: int = 0
    __DreadMissEvictCount: int = 0
    __DwriteMissEvictCount: int = 0
    __IreadCount: int = 0
    __DreadCount: int = 0
    __DwriteCount: int = 0
    __reads_parsed: int = 0
    __writes_parsed: int = 0

    def IReadCount(self):
        self.__IreadCount += 1
        Logger.debugLog(self, self.PERFORMANCE, __name__, self.__IreadCount)

    def DReadCount(self):
        self.__DreadCount += 1
        Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DreadCount)

    def DWriteCount(self):
        self.__DwriteCount += 1
        Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DwriteCount)

    def HitCount(self):
        if self.op == Cmd.READ_DATA:
            self.__DreadHitCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DreadHitCount)

        elif self.op == Cmd.WRITE_DATA:
            self.__DwriteHitCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DwriteHitCount)

        elif self.op == Cmd.READ_INSTRUCTION:
            self.__IreadHitCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__IreadHitCount)

    def MissCount(self):
        if self.op == Cmd.READ_DATA:
            self.__DreadMissCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DreadMissCount)

        elif self.op == Cmd.WRITE_DATA:
            self.__DwriteMissCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__DwriteMissCount)

        elif self.op == Cmd.READ_INSTRUCTION:
            self.__IreadMissCount += 1
            Logger.debugLog(self, self.PERFORMANCE, __name__, self.__IreadMissCount)

    def __parse_read_write(self):
        with open("trace.file") as fileObj:
            lines = fileObj.readlines()

        for line in lines:
            command, address = line.split()
            command = int(command)
            if (command == 0 or command == 2):
                self.__reads_parsed += 1
            elif(command == 1):
                self.__writes_parsed += 1

    def CachePerformanceResult(self):
        TotalHitCount = self.__IreadHitCount + self.__DreadHitCount + self.__DwriteHitCount
        TotalMissCount = self.__IreadMissCount + self.__DreadMissCount + self.__DwriteMissCount
        TotalEvictMissCount = self.__IreadMissEvictCount + self.__DreadMissEvictCount + self.__DwriteMissEvictCount
        TotalReadOperations = self.__IreadCount + self.__DreadCount
        TotalWriteOperations = self.__DwriteCount
        TotalOperations = self.__IreadCount + self.__DreadCount + self.__DwriteCount

        hit_percentage = (TotalHitCount/(1.0*TotalOperations))*100
        miss_percentage = (TotalMissCount/(1.0*TotalOperations))*100
        missEvict_percentage = (TotalEvictMissCount/(1.0*TotalOperations))*100
        Logger.debugLog(self, 0, __name__, "")
        self.__parse_read_write()
        if(self.__reads_parsed == TotalReadOperations):
            msgOut = "Total Number of Reads	      = %d" %(TotalReadOperations)
            Logger.debugLog(self, 0, __name__, msgOut)
        else:
            msgOut = "Total Number of Parsed Reads not equal to Read Operations"
            Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Total Number of Reads = %d" %(TotalReadOperations)
        Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Total Parsed Reads = %d" %(self.__reads_parsed)
        Logger.debugLog(self, 0, __name__, msgOut)
        if(self.__writes_parsed == TotalWriteOperations):
            msgOut =  "Total Number of Writes	      = %d" %(TotalWriteOperations)
            Logger.debugLog(self, 0, __name__, msgOut)

        else:
            msgOut = "Total Number of Parsed Writes not equal to Write Operations"
            Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Total Number of Writes   = %d" %(TotalWriteOperations)
        Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Total Parsed Write = %d" %(self.__writes_parsed)
        Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Total Number of Cache hits   = %d" %(TotalHitCount)
        Logger.debugLog(self, 0, __name__, msgOut)

        msgOut = "Total Number of Cache misses = %d" %((TotalMissCount+TotalEvictMissCount))
        Logger.debugLog(self, 0, __name__, msgOut)
        msgOut = "Cache Hit ratio              = %03.02f%c" %(hit_percentage,'%')
        Logger.debugLog(self, 0, __name__, msgOut)
        Logger.debugLog(self, 0, __name__, "")

        Logger.debugLog(self, 0, __name__, "\t ReadI \t ReadD \t Write \t TOTAL")
        Logger.debugLog(self, 0, __name__, msgOut)

        msgOut = "HITS :\t %d \t %d \t %d \t %d \t (%03.02f%c)" %( self.__IreadHitCount, self.__DreadHitCount, self.__DwriteHitCount, TotalHitCount,hit_percentage,'%')
        Logger.debugLog(self, 0, __name__, msgOut)

        msgOut = "MISS :\t %d \t %d \t %d \t %d \t (%03.02f%c)" %(self.__IreadMissCount, self.__DreadMissCount, self.__DwriteMissCount,TotalMissCount, miss_percentage,'%')
        Logger.debugLog(self, 0, __name__, msgOut)

        msgOut = "EVICT:\t %d \t %d \t %d \t %d \t (%03.02f%c)" %(self.__IreadMissEvictCount, self.__DreadMissEvictCount, self.__DwriteMissEvictCount,TotalEvictMissCount,missEvict_percentage,'%')
        Logger.debugLog(self, 0, __name__, msgOut)

        msgOut = "TOTAL:\t %d \t %d \t %d \t %d" %(self.__IreadCount, self.__DreadCount, self.__DwriteCount, TotalOperations)
        Logger.debugLog(self, 0, __name__, msgOut)
        AMAT = (hit_percentage/100.0) * 5 + ((miss_percentage+missEvict_percentage)/100.0) * 100
        Logger.debugLog(self, 0, __name__, "If we assume Hit time is 5 cycles & Miss time is 100 Cycles")
        msgOut = "Average Memory Access Time(AMAT) = %f cycles" %(AMAT)
        Logger.debugLog(self, 0, __name__, msgOut)
