import runner
import bs4
import random
import time
from my_log import MyLog


class Mod:
    def __init__(self, run: runner.Runner):
        self.coreShell = run
        self.log = MyLog("Mod:Coin")
        self.log.info("模块:自动投币模块")

    def getVideoUrl(self):
        self.log.info(f"随机获取视频...")
        rootHtml = self.coreShell.biliCore.getPageHtml()
        self.coreShell.biliCore.drv.find_element_by_class_name("change-btn").click()
        time.sleep(0.5)
        videosHtml = rootHtml.select("div.first-screen > div.space-between > div.rcmd-box-wrap > div.rcmd-box > "
                                     "div.video-card-reco")
        videoHtml: bs4.Tag = random.choice(videosHtml)
        videoUrl = "https://" + str(videoHtml.select_one("div.info-box > a").attrs["href"]).lstrip("//")
        self.log.info(f"获取到视频: {videoUrl}")
        return videoUrl

    def coinVideo(self, url: str):
        self.log.info(f"为视频[{url}]投币...")
        self.coreShell.biliCore.drv.get(url)
        time.sleep(5)
        self.coreShell.biliCore.drv.find_element_by_class_name("coin").click()
        time.sleep(1)
        self.coreShell.biliCore.drv.find_element_by_class_name("bi-btn").click()
        time.sleep(1)
        self.coreShell.biliCore.drv.back()
        self.log.info(f"投币完成")

    def loop(self, count: int):
        self.log.info(f"连续投币{count}次...")
        for i in range(count):
            self.log.info(f"第{i+1}次投币...")
            self.coinVideo(self.getVideoUrl())
            time.sleep(1)
