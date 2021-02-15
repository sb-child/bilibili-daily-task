import runner
import bs4
import random
import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from base_mod import BaseMod


class Mod(BaseMod):
    def __init__(self, run: runner.Runner):
        """
        投币模块.\n
        功能: 点赞, 分享, 观看, 投币特定视频

        :param run: Runner
        """
        super().__init__(run, "coin", "自动投币模块")
        self.firstTime = True

    def clickEvent(self, ele: WebElement):
        """
        内部方法: 点击事件

        :param ele: 要点击的元素
        :return: None
        """
        # 确保窗口足够大
        self.drv.set_window_size(1700, 1000)
        self.drv.execute_script("window.scrollTo(0, 0);")
        # 点击
        act = ActionChains(self.drv)
        act.move_to_element(ele)
        act.click(ele).perform()
        self.shortSleep()
        act.reset_actions()

    def getVideoUrlInRecommend(self):
        """
        从页面右侧的推荐中随机选择视频

        :return: 视频url
        """
        self.log.info(f"随机获取视频...")
        for i in range(2):
            self.clickEvent(self.drv.find_element_by_class_name("change-btn"))
            self.sleep()
        rootHtml = self.core.getPageHtml()
        self.sleep()
        videosHtml = rootHtml.select("div.first-screen > div.space-between > div.rcmd-box-wrap > div.rcmd-box > "
                                     "div.video-card-reco")
        videoHtml: bs4.Tag = random.choice(videosHtml)
        videoUrl = "https:" + str(videoHtml.select_one("div.info-box > a").attrs["href"])
        self.log.info(f"获取到视频: {videoUrl}")
        return videoUrl

    def _checkFestivalVideo(self):
        """
        内部方法: 检查当前视频是否是节日视频

        :return: bool
        """
        pageUrl = str(self.drv.current_url)
        if pageUrl.find("festival") == -1:
            return False
        return True

    def _likeVideo(self):
        """
        内部方法: 为当前视频点赞

        :return: None
        """
        self.log.info("点赞中...")
        likeBtn = self.drv.find_element_by_class_name("like")

        def isLiked():
            return str(likeBtn.get_attribute("class")).find("on") != -1

        if not isLiked():
            self.clickEvent(likeBtn)
            self.sleep()
        else:
            self.log.warning("此视频已点过赞")
        likeRetryNum = 5
        while not isLiked():
            self.log.warning("点赞失败, 重试...")
            self.clickEvent(likeBtn)
            self.sleep()
            likeRetryNum -= 1
            if likeRetryNum <= 0:
                self.log.warning("点赞失败, 放弃")
                break
        self.log.info("点赞完成" + (", 但是放弃了" if likeRetryNum <= 0 else ""))

    def _coinVideo(self, coin_1: bool):
        """
        内部方法: 为当前视频投币

        :param coin_1: 数量: True为1个, False为2个
        :return: None
        """
        self.log.info("投币中...")
        self.clickEvent(self.drv.find_element_by_class_name("coin"))
        self.sleep()
        # 数量
        if coin_1:
            self.clickEvent(self.drv.find_element_by_class_name("left-con"))
        else:
            self.clickEvent(self.drv.find_element_by_class_name("right-con"))
        self.sleep()
        # 投币
        self.clickEvent(self.drv.find_element_by_class_name("bi-btn"))
        self.sleep()
        self.log.info("投币完成")

    def _shareVideo(self):
        """
        内部方法: 分享当前视频到动态

        :return: None
        """
        self.log.info("分享中...")
        shareBtn1 = self.drv.find_element_by_class_name("share")
        self.sleep()
        self.clickEvent(shareBtn1)
        self.drv.find_element_by_xpath("//div[@class='share-down']/span[1]").click()
        self.sleep()
        ifr = self.drv.find_element_by_xpath("//div/iframe[@name='dynmic-share']")
        shareUrl = str(ifr.get_attribute("src"))
        # share
        self.drv.get(shareUrl)
        self.sleep()
        btn = self.drv.find_element_by_css_selector("div.share-step > div.btn-field > button.share-btn")
        self.clickEvent(btn)
        self.sleep()
        self.drv.back()
        # share end
        self.sleep()
        self.log.info("分享完成")

    def _watchVideo(self):
        """
        内部方法: 观看此视频

        :return: None
        """
        self.log.info("观看中...")
        while True:
            try:
                loadMask = self.drv.find_element_by_class_name("bilibili-player-video-panel")
            except selenium.common.exceptions.NoSuchElementException:
                self.log.warning("获取加载状态失败")
                self.sleep()
                continue
            loadMaskStyle = str(loadMask.get_attribute("style"))
            if loadMaskStyle.find("none") != -1:
                break
            self.log.info("等待视频加载完成...")
            self.sleep()
        while True:
            try:
                playBtn = self.drv.find_element_by_class_name("bilibili-player-dm-tip-wrap")
                self.clickEvent(playBtn)
                self.longSleep()
                self.clickEvent(playBtn)
            except selenium.common.exceptions.NoSuchElementException:
                self.log.warning("播放失败,重试...")
                self.sleep()
                continue
            break
        self.log.info("观看完成")

    def run(self, url: str, like=True, coin=True, coin_1=True, share=True, watch=True):
        """
        执行操作

        :param watch: 是否观看
        :param share: 是否分享
        :param coin_1: 投币数量: True为1个, False为2个
        :param coin: 是否投币
        :param like: 是否点赞
        :param url: 视频url
        :return: 0: 完成, 1: 跳过节日视频
        """
        self.log.info(f"选定视频[{url}]")
        self.log.info(
            f"点赞[{'x' if like else ' '}] "
            f"投币[{'0' if not coin else '1' if coin_1 else '2'}] "
            f"转发[{'x' if share else ' '}] "
            f"观看[{'x' if watch else ' '}]"
        )
        self.drv.get(url)
        if self.firstTime:
            # 使用缓存加快访问速度, 同时减少出错率
            self.drv.refresh()
            self.firstTime = False
            # self.drv.get(url)
        for i in range(6):
            self.sleep()
        # 不支持节日视频(如:拜年纪)
        if self._checkFestivalVideo():
            self.drv.back()
            self.log.info("节日相关视频, 放弃")
            return 1
        # 点赞
        if like:
            self._likeVideo()
        # 投币
        if coin:
            # try:
            self._coinVideo(coin_1)
            # except selenium.common.exceptions.NoSuchElementException:
            #     self.log.warning("弹出登录对话框, 自动关闭")
            #     # 自动关闭登录对话框
        # 分享
        if share:
            # self.log.warning("分享有已知问题, 暂不执行")
            self._shareVideo()
        # 观看视频 (无头模式下不能正常观看)
        if watch and not self.coreShell.headless:
            self._watchVideo()
        self.drv.back()
        self.log.info("操作完成")
        return 0

    def loop(self, count=5):
        """
        连续执行操作:\n
        分享一次. 观看, 点赞, 投币count次,

        :param count: 执行次数
        :return: None
        """
        self.log.info(f"连续执行{count}次...")
        for i in range(count):
            self.log.info(f"第{i + 1}次执行...")
            # 只分享一次
            while True:
                if self.run(self.getVideoUrlInRecommend(), share=True if i == 0 else False,
                            watch=True, coin=True, coin_1=True, like=True) == 0:
                    break
            self.sleep()
