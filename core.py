import os

from selenium import webdriver
from bs4 import BeautifulSoup as Bs


class BilibiliCore:
    def __init__(self, cookies: list, headless=False):
        """
        核心, 提供一些底层操作

        :param cookies: cookies列表
        :param headless: 是否启用无头模式
        """
        self.drvProfile = webdriver.FirefoxProfile()
        # set "navigator.webdriver" to undefined
        self.drvProfile.set_preference("dom.webdriver.enabled", False)
        # and mute it
        self.drvProfile.set_preference("media.volume_scale", "0.0")
        self.drvOptions = webdriver.FirefoxOptions()
        if headless:
            # headless mode
            self.drvOptions.add_argument("-headless")
            self.drvOptions.add_argument("-disable-gpu")
        # basic
        self.drv = webdriver.Firefox(
            firefox_profile=self.drvProfile,
            firefox_options=self.drvOptions,
        )
        self.cookies = cookies
        self.isLogin = False
        # method mapping
        self.refresh = self.drv.refresh
        self.clearCookies = self.drv.delete_all_cookies
        self.quit = self.drv.quit
        self.closeWindow = self.drv.close

    def setCookies(self):
        """
        为浏览器设置cookies

        :return: None
        """
        for i in self.cookies:
            self.drv.add_cookie(i)

    def writeCookies(self):
        """
        保存当前cookies到文件

        :return: None
        """
        cfgFile = f"config{os.path.sep}cookie.txt"
        cfgFileObj = open(cfgFile, mode="w")
        for kv in self.drv.get_cookies():
            key = kv["name"]
            val = kv["value"]
            cfgFileObj.write(f"{key}={val};")
        cfgFileObj.close()

    def getPageHtml(self):
        """
        获取当前页面的html

        :return: beautifulSoup对象
        """
        bd = self.drv.find_element_by_tag_name("html")
        html: str = bd.get_attribute("outerHTML")
        return Bs(html, "lxml")

    def getLoginStatus(self):
        """
        获取登录状态

        :return: 是否已登录
        """
        loginBtn = self.drv.find_elements_by_xpath("//div/span/img[@src='//static.hdslb.com/images/akari.jpg']")
        loginBtn1 = self.drv.find_elements_by_class_name("unlogin-avatar")
        if len(loginBtn) > 0 or len(loginBtn1) > 0:
            return False
        else:
            self.writeCookies()
            return True

    def getNickname(self) -> str:
        """
        获取昵称

        :return: str
        """
        html = self.getPageHtml()
        lb = html.select_one("p.nickname")
        return lb.text

    def _get_money_count(self, href: str):
        """
        内部方法: 按照指定规则, 获取元素的文本(转换为数字)

        :return: 数字
        """

        html = self.getPageHtml()
        lb = html.select_one(f"a[href=\"{href}\"] > span")
        return float(lb.text)

    def getCoinCount(self):
        """
        获取硬币数量

        :return: 硬币数量
        """
        return self._get_money_count('https://account.bilibili.com/site/coin')

    def getBCoinCount(self):
        """
        获取B币数量

        :return: B币数量
        """
        return int(self._get_money_count('https://pay.bilibili.com/paywallet-fe/bb_balance.html'))

    def loginCheck(self):
        """
        尝试登录

        :return: 登录结果
        """
        self.clearCookies()
        self.drv.get("https://www.bilibili.com/")
        self.setCookies()
        self.refresh()
        return self.getLoginStatus()
