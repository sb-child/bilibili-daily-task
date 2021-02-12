import logging
import time
import core
from config import config


class Runner:
    def __init__(self):
        self.log = logging.RootLogger(logging.DEBUG)
        self.logHandler = logging.StreamHandler()
        self.log.addHandler(self.logHandler)
        self.logFmt = logging.Formatter("[%(asctime)s %(levelname)s]:%(message)s")
        self.logHandler.setFormatter(self.logFmt)
        self.biliCore = core.BilibiliCore(config.getCookies())
        self.log.info("Bilibili Daily Task")
        self.log.info("B站每日任务自动完成工具 已初始化完成.")

    def getNickname(self):
        return self.biliCore.getNickname()

    def getCoinCount(self):
        return self.biliCore.getCoinCount()

    def getBCoinCount(self):
        return self.biliCore.getBCoinCount()

    def logAccountInfo(self):
        self.log.info("==账号信息==")
        self.log.info(f"昵称: {self.getNickname()}")
        self.log.info(f"硬币: {self.getCoinCount()}")
        self.log.info(f"B币: {self.getBCoinCount()}")
        self.log.info("===========")

    def loginCheck(self):
        self.log.info("正在登录...")
        r = self.biliCore.loginCheck()
        if r:
            self.log.info("登录成功")
            self.logAccountInfo()
        else:
            self.log.info("登录失败")
            self.log.info("请检查cookies设置")
        return r

    def start(self):
        if not self.loginCheck():
            self.biliCore.quit()
            return
        time.sleep(100)
        self.biliCore.quit()


def main():
    pass


if __name__ == '__main__':
    main()
