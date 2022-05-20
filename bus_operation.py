from logger import Logger
msgOut = ' '*2048
print(len(msgOut))
res_string = ["NOHIT","HIT","HITM"]
BusOp_string = ["","READ","WRITE","INVALIDATE","RWIM"]
msg_string = ["", "GETLINE","SENDLINE", "INVALIDATELINE", "EVICTLINE"]
BusOp = 0


class BusOperation:
    def busoperation(self, BusOp: int,Address: int,SnoopResult:int):
    # SnoopResult = GetSnoopResult(Address);
        msgOut =  'BusOp: {}, Address:{}, Snoop Result:{}'.format( BusOp_string[BusOp], format(Address,'x'), res_string[SnoopResult])
        Logger.debugLog(self,BusOp, 'busoperation', msgOut)

    def GetSnoopResult(self,Address: int):
        result = 'NOHIT'
        if ((Address & 0x3) == 0) :
            result = 'HIT'
        elif ((Address & 0x3) == 0x01):
            result = 'HITM'
        msgOut = "Address {},result {} ".format(format(Address,"X"), result)
        Logger.debugLog(self,BusOp, 'GetSnoopResult', msgOut)
        return result

    def PutSnoopResult(self,Address: int, SnoopResult: int):
        msgOut = "SnoopResult: Address {} SnoopResult: {}".format(format(Address,'x'), res_string[SnoopResult])
        Logger.debugLog(self,BusOp, 'PutSnoopResult', msgOut)

    def MessageToCache(self, Message: str, Address: int):
        msgOut = "L2->L1: {} {}".foramt(msg_string[Message], Address)
        Logger.debugLog(self, BusOp, 'MessageToCache', msgOut)
