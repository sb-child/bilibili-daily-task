import runner
import time
from my_log import MyLog


def _shortSleep():
    time.sleep(0.5)


def _commonSleep():
    time.sleep(1)


def _longSleep():
    time.sleep(5)


class BaseMod:
    def __init__(self, run: runner.Runner, mod_name: str, mod_info: str):
        self.coreShell = run
        self.drv = self.coreShell.biliCore.drv
        self.core = self.coreShell.biliCore
        self.log = MyLog(f"Mod:{mod_name}")
        self.log.info(f"模块:{mod_info}")
        self.shortSleep = _shortSleep
        self.sleep = _commonSleep
        self.longSleep = _longSleep

    def reset(self):
        self.drv.get("https://www.bilibili.com/")
