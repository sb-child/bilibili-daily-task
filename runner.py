from my_log import MyLog
import time
import core
from config import config


class Runner:
    def __init__(self):
        self.log = MyLog("Runner")
        self.biliCore = core.BilibiliCore(
            cookies=config.getCookies(),
            headless=config.HEADLESS,
        )
        self.log.info("Bilibili Daily Task")
        self.log.info("B站每日任务自动完成工具")
        self.log.info("https://github.com/sb-child/bilibili-daily-task")

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
            time.sleep(3)
            self.logAccountInfo()
        else:
            self.log.info("登录失败.请检查cookies设置")
        return r

    def start(self):
        if not self.loginCheck():
            self.biliCore.quit()
            return -1
        return 0
        # time.sleep(100)
        # self.biliCore.quit()


def main():
    pass


if __name__ == '__main__':
    main()
