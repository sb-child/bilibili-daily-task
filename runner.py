from my_log import MyLog
import time
import core
from config import config


class Runner:
    def __init__(self):
        """
        对core的封装
        """
        self.log = MyLog("Runner")
        self.biliCore = core.BilibiliCore(
            cookies=config.getCookies(),
            headless=config.HEADLESS,
        )
        self.headless = config.HEADLESS
        self.log.info("Bilibili Daily Task")
        self.log.info("B站每日任务自动完成工具" + (" [无头模式, 部分功能将不可用]" if self.headless else ""))
        self.log.info("https://github.com/sb-child/bilibili-daily-task")

    def getNickname(self):
        """
        获取昵称

        :return: str
        """
        return self.biliCore.getNickname()

    def getCoinCount(self):
        """
        获取硬币数量

        :return: 硬币数量
        """
        return self.biliCore.getCoinCount()

    def getBCoinCount(self):
        """
        获取B币数量

        :return: B币数量
        """
        return self.biliCore.getBCoinCount()

    def logAccountInfo(self):
        """
        在日志中输出账号信息

        :return: None
        """
        if self.headless:
            self.log.warning("当前为无头模式, 跳过此步骤")
            return
        self.log.info("==账号信息==")
        self.log.info(f"昵称: {self.getNickname()}")
        self.log.info(f"硬币: {self.getCoinCount()}")
        self.log.info(f"B币: {self.getBCoinCount()}")
        self.log.info("===========")

    def loginCheck(self):
        """
        尝试登录

        :return: 登录结果
        """
        self.log.info("正在登录...")
        r = self.biliCore.loginCheck()
        if r:
            self.log.info("登录成功")
            time.sleep(3)
            self.logAccountInfo()
        else:
            err_title = self.biliCore.drv.title
            err_html = self.biliCore.getPageHtml().prettify()
            self.log.error("标题: " + err_title)
            self.log.error("html:\n" + err_html)
            self.log.error("登录失败.请检查cookies设置")
        return r

    def start(self):
        """
        启动Runner

        :return: 登录结果: 0: 正常, -1: 登录失败
        """
        if not self.loginCheck():
            self.biliCore.quit()
            return -1
        return 0


def main():
    pass


if __name__ == '__main__':
    main()
