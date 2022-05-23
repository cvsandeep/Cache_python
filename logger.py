global debug
debug = 10


class Logger():
    def BusOperations(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CacheOperations(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CacheInternalOperations(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def ControlOperations(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CacheLinePrint(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CacheFile(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CacheFilePrint(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CounterPrint(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CounterFile(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def CounterFilePrint(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def ALL(self, functionName, message):
        return '{}:{}'.format(functionName, message)

    def default(self, functionName, message):
        return 'no message to display'

    switcher = {
        0: BusOperations
        , 1: CacheOperations
        , 2: CacheInternalOperations
        , 3: ControlOperations
        , 4: CacheLinePrint
        , 5: CacheFile
        , 6: CacheFilePrint
        , 7: CounterPrint
        , 8: CounterFile
        , 9: CounterFilePrint
        , 10: ALL
    }

    def debugLog(self, loginglevel: int, functionName: str, msg: str):
        def switch(loginglevel):
            return self.switcher.get(loginglevel)

        if loginglevel <= debug:
            print('test {}:{}'.format(functionName, msg))

        ###### for the case statement in the c file uncomment/uncomment the below line
        #print(switch(loginglevel))


## this is the test statements comment when not required
myclass = Logger()
fun_name = 'test_fun'
message = 'success'
myclass.debugLog(3, fun_name, message)

#######################################################################
