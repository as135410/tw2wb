import json
import time
import mlog
def getConfig(l1, l2):
    with open("conf.json", "r") as f:
        j = f.read()
        dic = json.loads(j)
    f.close()
    return dic[l1][l2]

def msleep(sec, describe):
    strSec = " second" if sec < 2 else " seconds"
    mlog.Logi(describe + "to sleep " + str(sec) + strSec)
    time.sleep(sec)
    mlog.Logi(describe + "sleep end")
