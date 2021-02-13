from selenium import webdriver
from bs4 import BeautifulSoup as Bs


class BilibiliCore:
    def __init__(self, cookies: list[dict]):
        # set "navigator.webdriver" to undefined
        self.drvProfile = webdriver.FirefoxProfile()
        self.drvProfile.set_preference("dom.webdriver.enabled", False)
        # basic
        self.drv = webdriver.Firefox(firefox_profile=self.drvProfile)
        self.cookies = cookies
        self.isLogin = False
        # method mapping
        self.refresh = self.drv.refresh
        self.clearCookies = self.drv.delete_all_cookies
        self.quit = self.drv.quit
        self.closeWindow = self.drv.close


    def setCookies(self):
        for i in self.cookies:
            self.drv.add_cookie(i)

    def getPageHtml(self):
        bd = self.drv.find_element_by_tag_name("html")
        html: str = bd.get_attribute("outerHTML")
        return Bs(html, "lxml")

    def getLoginStatus(self):
        loginBtn = self.drv.find_elements_by_xpath("//div/span/img[@src='//static.hdslb.com/images/akari.jpg']")
        loginBtn1 = self.drv.find_elements_by_class_name("unlogin-avatar")
        if len(loginBtn) > 0 or len(loginBtn1) > 0:
            return False
        else:
            return True

    def getNickname(self) -> str:
        html = self.getPageHtml()
        lb = html.select_one("p.nickname")
        # lb = self.drv.find_element_by_xpath("//div[@class='vp-container']/p[@class='nickname']")
        # print(lb.text)
        return lb.text

    def _get_money_count(self, href: str):
        html = self.getPageHtml()
        lb = html.select_one(f"a[href=\"{href}\"] > span")
        # lb = self.drv.find_element_by_xpath(f"//a[@href='{href}']/span")
        return float(lb.text)

    def getCoinCount(self):
        return self._get_money_count('https://account.bilibili.com/site/coin')

    def getBCoinCount(self):
        return int(self._get_money_count('https://pay.bilibili.com/paywallet-fe/bb_balance.html'))

    def loginCheck(self):
        self.clearCookies()
        self.drv.get("https://www.bilibili.com/")
        self.setCookies()
        self.refresh()
        return self.getLoginStatus()
