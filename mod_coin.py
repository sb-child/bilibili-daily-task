import runner
import bs4
import random
import time
from selenium.webdriver import ActionChains
from base_mod import BaseMod


class Mod(BaseMod):
    def __init__(self, run: runner.Runner):
        super().__init__(run, "coin", "自动投币模块")

    def getVideoUrlInRecommend(self):
        self.log.info(f"随机获取视频...")
        rootHtml = self.core.getPageHtml()
        self.drv.find_element_by_class_name("change-btn").click()
        time.sleep(0.5)
        videosHtml = rootHtml.select("div.first-screen > div.space-between > div.rcmd-box-wrap > div.rcmd-box > "
                                     "div.video-card-reco")
        videoHtml: bs4.Tag = random.choice(videosHtml)
        videoUrl = "https:" + str(videoHtml.select_one("div.info-box > a").attrs["href"])
        self.log.info(f"获取到视频: {videoUrl}")
        return videoUrl

    def coinVideo(self, url: str, coin=True, coin_1=True, share=True, watch=True):
        self.log.info(f"选定视频[{url}]")
        self.log.info(f"投币[{'0' if not coin else '1' if coin_1 else '2'}] "
                      f"转发[{'x' if share else ' '}] "
                      f"观看[{'x' if watch else ' '}]")
        self.drv.get(url)
        time.sleep(5)
        # ----
        # 点击 投币 按钮
        if coin:
            self.log.info("投币中...")
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
            self.log.info("投币完成")
        # ----
        # 分享
        if share:
            self.log.info("分享中...")
            shareBtn1 = self.drv.find_element_by_class_name("share")
            time.sleep(1)
            act = ActionChains(self.drv)
            act.move_to_element(shareBtn1).perform()
            self.drv.find_element_by_xpath("//div[@class='share-down']/span[1]").click()
            time.sleep(1)
            ifr = self.drv.find_element_by_xpath("//div/iframe[@name='dynmic-share']")
            shareUrl = str(ifr.get_attribute("src"))
            # share
            self.drv.get(shareUrl)
            btn = self.drv.find_element_by_css_selector("div.share-step > div.btn-field > button.share-btn")
            btn.click()
            time.sleep(0.5)
            self.drv.back()
            # share end
            time.sleep(1)
            self.log.info("分享完成")
        # ----
        # back to index
        # 观看视频
        if watch:
            self.log.info("观看中...")
            while True:
                loadMask = self.drv.find_element_by_class_name("bilibili-player-video-panel")
                loadMaskStyle = str(loadMask.get_attribute("style"))
                if loadMaskStyle.find("none") != -1:
                    break
                self.log.info("等待视频加载完成...")
                time.sleep(1)
            playBtn = self.drv.find_element_by_class_name("bilibili-player-dm-tip-wrap")
            act = ActionChains(self.drv)
            act.move_to_element(playBtn).perform()
            playBtn.click()
            time.sleep(5)
            playBtn.click()
            self.log.info("观看完成")
        self.drv.back()
        self.log.info("操作完成")

    def loop(self, count: int):
        self.log.info(f"连续投币{count}次...")
        for i in range(count):
            self.log.info(f"第{i + 1}次投币...")
            # 只分享一次
            self.coinVideo(self.getVideoUrlInRecommend(), share=False if i != 0 else True)
            time.sleep(1)

    def autoLoop(self):
        self.loop(5)
