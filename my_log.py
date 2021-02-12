import logging


class MyLog:
    def __init__(self, log_type="default"):
        self.logType = log_type
        self.log = logging.RootLogger(logging.DEBUG)
        self.logHandler = logging.StreamHandler()
        self.log.addHandler(self.logHandler)
        self.logFmt = logging.Formatter(f"[%(asctime)s {self.logType} %(levelname)s]:%(message)s")
        self.logHandler.setFormatter(self.logFmt)
        self.info = self.log.info
        self.warning = self.log.warning
        self.debug = self.log.debug
        self.error = self.log.error
