import twitter
import weibo
import time
import config

#if __name__ == "main":
tw = twitter.twitter()
wb = weibo.weibo()
timeGap = config.getConfig("other", "timegap")

while True:
    newT = tw.getNew()
    if len(newT) > 0:
        print("ready to publish...")
        wb.publishList(newT)
    time.sleep(timeGap)