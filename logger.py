global debug
debug = 5


class Logger():
    BUSOP = 1
    CACHEOP  = 2
    CACHEOPX = 3
    PERFORMANCE = 4
    CONTROL = 5

    def debugLog(self, loginglevel: int, functionName: str, msg: str):
        if loginglevel <= debug:
            print('{}:{}'.format(functionName, msg))
