import runner
from my_log import MyLog


class BaseMod:
    def __init__(self, run: runner.Runner, mod_name: str, mod_info: str):
        self.coreShell = run
        self.drv = self.coreShell.biliCore.drv
        self.core = self.coreShell.biliCore
        self.log = MyLog(f"Mod:{mod_name}")
        self.log.info(f"模块:{mod_info}")

    def reset(self):
        self.drv.get("https://www.bilibili.com/")
