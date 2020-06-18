from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from enum import Enum
import mlog
import config
import time

class state(Enum):
    LOGIN = 1       #登录界面
    MAIN = 2        #微博主界面
    PUBLISH = 3     #发布界面
    NONE = 4        #非微博界面

class weibo():
    #-------------------------------------------------------------------------
    def __init__(self):
        self._loadConf()
        self.browser_options = Options()
        self.state = state.NONE

        self.updataFuncDic = {
            state.LOGIN     : self._login,
            state.MAIN      : self._inputBut,
            state.PUBLISH   : self._commit,
            state.NONE      : self._launchWeiBo,
        }

        if self.bHeadless:
            self.browser_options.add_argument("--headless")

        if self.bPictureless:
            self.browser_options.add_argument("blink-settings=imagesEnabled=false")

        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browser_options)

        self.publishList = []

    def __del__(self):
        self._closeBrowser()

    def _closeBrowser(self):
        self.browser.close()

    def _loadConf(self):
        self.driverPath = config.getConfig("other", "driverpath")
        self.loginUrl = config.getConfig("weibo", "loginurl")
        self.username = config.getConfig("weibo", "username")
        self.password = config.getConfig("weibo", "password")
        self.bHeadless = config.getConfig("weibo", "headless")
        self.bPictureless = config.getConfig("weibo", "pictureless")
    #------------------------------------------------------------------------
    def _launchWeiBo(self):
        self.browser.get(self.loginUrl)
        config.msleep(3, "进入微博界面")

    def _login(self):
        try:
            usernameText = self._getLoginNameContext()
            usernameText.clear()
            usernameText.send_keys(self.username)
        except:
            mlog.Logw("输入账号出错")
            self.browser.save_screenshot("errorscreenshot/loginerror.png")
            return False

        try:
            passwordText = self._getLoginPassContext()
            passwordText.clear()
            passwordText.send_keys(self.password)
        except:
            mlog.Logw("输入密码出错")
            self.browser.save_screenshot("errorscreenshot/loginerror.png")
            return False

        try:
            loginBut = self._getLoginBut()
            loginBut.click()
            config.msleep(10)
        except:
            mlog.Logw("点击登录按钮出错")
            self.browser.save_screenshot("errorscreenshot/loginerror.png")
            return False

        self.state = state.MAIN
        return True
    #点击发微博按钮
    def _inputBut(self):
        try:
            inputBut = self._getInputBut()
            input.click()
            config.msleep(5, "inputBut")
        except:
            mlog.Logw("没找到输入按钮")
            self.browser.save_screenshot("errorscreenshot/inputerror.png")

    def _commit(self):
        cont = self.publishList.pop()

        contStr = cont["str"]
        contPic = cont["pic"]

        try:
            inputCont = self._getInputContext()
            inputCont.clear()
            inputCont.send_keys(contStr)
            config.msleep(1, "inputContext")
        except:
            mlog.Logw("没找到输入框")
            self.browser.save_screenshot("errorscreenshot/inputconterror.png")

        try:
            a = 1
        except:
            b = 1

        try:
            publishBut = self._getPublishBut()
            publishBut.click()
            config.msleep(5, "publish")
        except:
            mlog.Logw("没找到发送按钮")
            self.browser.save_screenshot("errorscreenshot/publisherror.png")

    #-------------------------------------------------------------------------------------
    #右上角那个发微博的按钮
    def _getInputBut(self):
        return self.browser.find_element_by_xpath('//div[@class="lite-iconf lite-iconf-releas"]')

    #输入框
    def _getInputContext(self):
        return self.browser.find_element_by_xpath('//span[@class="m-wz-def"]/textarea[@placeholder="分享新鲜事…"]')

    #写好了之后的那个发微博的按钮
    def _getPublishBut(self):
        return self.browser.find_element_by_xpath('//a[@class="m-send-btn disabled"]')

    def _getLoginNameContext(self):
        return self.browser.find_element_by_id("loginName")

    def _getLoginPassContext(self):
        return self.browser.find_element_by_id("loginPassword")

    def _getLoginBut(self):
        return self.self.browser.find_element_by_id('loginAction')
    #-------------------------------------------------------------------------------------
    def _getState(self):
        element = self._getLoginBut()
        if len(element) != 0:
            self.state =  state.LOGIN
            return

        element = self._getPublishBut()
        if len(element) != 0:
            self.state = state.PUBLISH
            return 

        element = self._getInputBut()
        if len(element) != 0:
            self.state = state.MAIN
            return
        
        self.state = state.NONE
        return
    #----------------------------------------API-------------------------------------------
    def update(self):
        if len(self.publishCont) == 0:
            return

        self._getState()
        self.updataFuncDic[self.state]()

    def publish(self, str, pic):
        if not isinstance(str, str):
            return

        if not isinstance(pic, tuple):
            return

        cont = {
            "str" : str,
            "pic" : pic,
        }

        self.publishList.insert(cont)