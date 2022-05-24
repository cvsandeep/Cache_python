from cache_types import OperationType, SnoopType
from logger import Logger

res_string = ["NOHIT", "HIT", "HITM"]
BusOp_string = ["", "READ", "WRITE", "INVALIDATE", "RWIM"]
msg_string = ["", "GETLINE", "SENDLINE", "INVALIDATELINE", "EVICTLINE"]


class BusOperation():
    def Busoperation(self, BusOp: int, Address: int, SnoopResult:int):
        # SnoopResult = GetSnoopResult(Address);
        msgOut = 'BusOp: {}, Address:{}, Snoop Result:{}'.format(BusOp_string[BusOp], format(Address, 'x'), res_string[SnoopResult])
        Logger.debugLog(self, Logger.BUSOP, 'busoperation', msgOut)

    def GetSnoopResult(self, Address: int):
        result = SnoopType.NOHIT
        if ((Address & 0x3) == 0) :
            result = SnoopType.HIT
        elif ((Address & 0x3) == 0x01):
            result = SnoopType.HITM
        msgOut = "Address {},result {} ".format(format(Address, "X"), result)
        Logger.debugLog(self, Logger.BUSOP, 'GetSnoopResult', msgOut)
        return result

    def PutSnoopResult(self, Address: int, SnoopResult: int):
        msgOut = "SnoopResult: Address {} SnoopResult: {}".format(format(Address, 'x'), res_string[SnoopResult])
        Logger.debugLog(self, Logger.BUSOP, 'PutSnoopResult', msgOut)

    def MessageToCache(self, Message, Address: int):
        msgOut = "L2->L1: %s 0x%08x" %(msg_string[Message], Address)
        Logger.debugLog(self, Logger.BUSOP, 'MessageToCache', msgOut)
