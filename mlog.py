import time

LogFile = "./LogData/Logs"

def _getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def Logi(str):
    logData = _getTime() + " [INFO] " +  ":" + str
    with open(LogFile, "a+") as f:
        f.write(logData)
        f.close()
    print(logData)

def Logw(str):
    logData = _getTime() + " [WARN] " +  ":" + str
    with open(LogFile, "a+") as f:
        f.write(logData)
        f.close()
    print(logData)

def Loge(str):
    logData = _getTime() + " [ERROR] " +  ":" + str
    with open(LogFile, "a+") as f:
        f.write(logData)
        f.close()
    print(logData)
