import runner
import bs4
import random
import time
from my_log import MyLog
from selenium.webdriver import ActionChains


class Mod:
    def __init__(self, run: runner.Runner):
        self.coreShell = run
        self.drv = self.coreShell.biliCore.drv
        self.core = self.coreShell.biliCore
        self.log = MyLog("Mod:Coin")
        self.log.info("模块:自动投币模块")

    def getVideoUrlInRecommend(self):
        self.log.info(f"随机获取视频...")
        rootHtml = self.core.getPageHtml()
        self.drv.find_element_by_class_name("change-btn").click()
        time.sleep(0.5)
        videosHtml = rootHtml.select("div.first-screen > div.space-between > div.rcmd-box-wrap > div.rcmd-box > "
                                     "div.video-card-reco")
        videoHtml: bs4.Tag = random.choice(videosHtml)
        videoUrl = "https://" + str(videoHtml.select_one("div.info-box > a").attrs["href"]).lstrip("//")
        self.log.info(f"获取到视频: {videoUrl}")
        return videoUrl

    def coinVideo(self, url: str, coin=True, coin_1=True, share=True):
        self.log.info(f"为视频[{url}]投币...")
        self.log.info(f"投币[{'0' if not coin else '1' if coin_1 else '2'}] 转发[{'x' if share else ' '}]")
        self.drv.get(url)
        time.sleep(5)
        # ----
        # 点击 投币 按钮
        if coin:
            self.drv.find_element_by_class_name("coin").click()
            time.sleep(1)
            # 数量
            if coin_1:
                self.drv.find_element_by_class_name("left-con").click()
            else:
                self.drv.find_element_by_class_name("right-con").click()
            time.sleep(1)
            # 投币
            self.drv.find_element_by_class_name("bi-btn").click()
            time.sleep(1)
        # ----
        # 分享
        if share:
            shareBtn1 = self.drv.find_element_by_class_name("share")
            time.sleep(1)
            act = ActionChains(self.drv)
            act.move_to_element(shareBtn1).perform()
            self.drv.find_element_by_xpath("//div[@class='share-down']/span[1]").click()
            time.sleep(1)
            act.reset_actions()
            ifr = self.drv.find_element_by_xpath("//div/iframe[@name='dynmic-share']")
            # -- into iframe
            self.drv.switch_to.frame(ifr)
            time.sleep(1)
            btn = self.drv.find_element_by_css_selector("div.share-step > div.btn-field > button.share-btn")  # worked
            # fixme: can not click share button
            # bug: 分享 按钮不能点击
            act = ActionChains(self.drv)
            act.move_to_element(btn).perform()
            act.click(btn).perform()
            # ----
            time.sleep(1)
            act.reset_actions()
            self.drv.switch_to.default_content()
            # -- back to default
            time.sleep(1)
        # ----
        # back to index
        self.drv.back()
        self.log.info(f"投币完成")

    def loop(self, count: int):
        self.log.info(f"连续投币{count}次...")
        for i in range(count):
            self.log.info(f"第{i+1}次投币...")
            self.coinVideo(self.getVideoUrlInRecommend(), coin=False)
            time.sleep(1)
