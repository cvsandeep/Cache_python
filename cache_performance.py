from cache_performance import CachePerformance
from logger import Logger
from cache_opration import CacheOperation
class CachePerformance():
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

    @staticmethod
    def IReadCount():
        ++ self.__IreadCount
        Logger.debugLog(PERFORMANCE, __func__, self.__IreadCount)

    @staticmethod
    def DReadCount():
        ++ self.__DreadCount
        Logger.debugLog(PERFORMANCE, __func__, self.__DReadCount)

    @staticmethod
    def DWriteCount():
        ++ self.__DWriteCount
        Logger.debugLog(PERFORMANCE, __func__, self.__DWriteCount)
    @staticmethod


    @staticmethod
    def HitCount(): print("")

    @staticmethod
    def MissCount(): print("")

    @staticmethod
    def __EvictCount(): print("")

    @staticmethod
    def __parse_read_write():
        while (UpdateTraceOperation()):
            if (op == 0 or op == 2):
                ++ self.__reads_parsed
            elsif(op == 1):
                ++ self.__writes_parsed




    def CachePerformance_result(self):
        TotalHitCount = self.__IreadHitCount + self.__DreadHitCount + self.__DwriteHitCount
        ToatalMissCount = self.__IreadMissCount + self.__DreadMissCount + self.__DwriteMissCount
        TotalEvictMissCount = self.__IreadMissEvictCount + self.__DreadMissEvictCount + self.__DwriteMissEvictCount
        TotalReadOperations = self.__IreadCount + self.__DreadCount
        TotalWriteOperations = self.__DwriteCount
        TotalOperations = self.__IreadCount + self.__DreadCount + self.__DwriteCount

        hit_percentage = (TotalHitCount/(1.0*TotalOperations))*100
        miss_percentage = (ToatalMissCount/(1.0*TotalOperations))*100
        missEvict_percentage = (TotalEvictMissCount/(1.0*TotalOperations))*100
        Logger.debugLog(0, __func__, "")
        def __parse_read_write():
            if(reads_parsed == TotalReadOperations):
                print(msgOut,"Total Number of Reads	      = %d",TotalReadOperations)
                Logger.debugLog(0, __func__, msgOut)
            else:
            print(msgOut,"Total Number of Parsed Reads not equal to Read Operations")
            Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Total Number of Reads = %d",TotalReadOperations)
            Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Total Parsed Reads = %d",reads_parsed)
            Logger.debugLog(0, __func__, msgOut)
            if(writes_parsed == TotalWriteOperations):
                print(msgOut, "Total Number of Writes	      = %d", TotalWriteOperations)
                Logger.debugLog(0, __func__, msgOut)

            else:
                    print(msgOut,"Total Number of Parsed Writes not equal to Write Operations")
                    Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Total Number of Writes   = %d",TotalWriteOperations)
            Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Total Parsed Write = %d",writes_parsed)
            Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Total Number of Cache hits   = %d",TotalHitCount)
            Logger.debugLog(0, __func__, msgOut)

            print(msgOut,"Total Number of Cache misses = %d",(ToatalMissCount+TotalEvictMissCount))
            Logger.debugLog(0, __func__, msgOut)
            print(msgOut,"Cache Hit ratio              = %03.02f%c",hit_percentage,'%')
            Logger.debugLog(0, __func__, msgOut)
            Logger.debugLog(0, __func__, "")

            Logger.debugLog(msgOut,"\t ReadI \t ReadD \t Write \t TOTAL")
            Logger.debugLog(0, __func__, msgOut)

            print(msgOut,"HITS :\t %d \t %d \t %d \t %d \t (%03.02f%c)", self.__IreadHitCount, self.__DreadHitCount, self.__DwriteHitCount, TotalHitCount,hit_percentage,'%')
            Logger.debugLog(0, __func__, msgOut)


            print(msgOut,"MISS :\t %d \t %d \t %d \t %d \t (%03.02f%c)", self.__IreadMissCount, self.__DreadMissCount, self.__DwriteMissCount,ToatalMissCount, miss_percentage,'%')
            Logger.debugLog(0, __func__, msgOut)

            print(msgOut,"EVICT:\t %d \t %d \t %d \t %d \t (%03.02f%c)", self.__IreadMissEvictCount, self.__DreadMissEvictCount, self.__DwriteMissEvictCount,TotalEvictMissCount,missEvict_percentage,'%')
            Logger.debugLog(0, __func__, msgOut)


            print(msgOut,"TOTAL:\t %d \t %d \t %d \t %d", self.__selfIreadCount, self.__DreadCount, self.__DwriteCount,TotalOperations)
            Logger.debugLog(0, __func__, msgOut)
            AMAT = (hit_percentage/100.0) * 5 + ((miss_percentage+missEvict_percentage)/100.0) * 100
            Logger.debugLog(0, __func__, "If we assume Hit time is 5 cycles & Miss time is 100 Cycles")
            print(msgOut,"Average Memory Access Time(AMAT) = %f cycles",AMAT)
            Logger.debugLog(0, __func__, msgOut)



    return
}




