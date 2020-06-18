import requests
import html.parser
import json
import data
import config
import time
htmlparser = html.parser.HTMLParser()

class twitter:
    def __init__(self):
        self.data = data.Data()
        self._loadConf()
        self.seed = 0
        self.lastPicTime = 0

    def _loadConf(self):
        self.url  = config.getConfig("twitter", "url")

        self.dh   = config.getConfig("html", "divh")
        self.dt   = config.getConfig("html", "divt")
        self.ah   = config.getConfig("html", "ah")
        self.at   = config.getConfig("html", "at")
    
    def _findAll(self, src):
        left = 0
        right = 0
        headLen = len(self.dh)
        bUpdate = False
        res = {}
        count = 0
        while True:
            left = src.find(self.dh, right)
            right = src.find(self.dt, left)
            if left == -1 or right == -1:
                break

            #有个推特简介，烦死了
            count += 1
            if count <= 1:
                continue
            
            singRes = {}
            _result = htmlparser.unescape(src[left + headLen:right])  
            _result = self._strDeal(_result)
            if not self.data.exist(_result) :
                self.data.insert(_result)
                res[_result] = True
                bUpdate = True
                
        if bUpdate:
            self.data._write2local()
        return res

    def _strDeal(self, src):
        atLen = len(self.at)
        while True:
            left = src.find(self.ah)
            if left == -1:
                break
            right = src.find(self.at, left)
            if right == -1:
                break
            src = self._spilt(src, left, right + atLen - 1)
        return src

    def _spilt(self, src, left, right):
        lenth = len(src)
        strLeft = src[0:left]
        strRight = src[right+1:lenth]
        return strLeft+strRight

    def _getPicName(self):
        mTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if mTime == self.lastPicTime:
            self.seed += 1
            return mTime + str(self.seed)

        self.seed = 0
        self.lastPicTime = mTime
        return mTime + str(self.seed)

    def getNew(self):
        html_str = requests.get(self.url).text
        return self._findAll(html_str)
