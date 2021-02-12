import time
from config import config
from selenium import webdriver


def main():
    drv = webdriver.Firefox()
    drv.get("https://passport.bilibili.com/login")
    time.sleep(10)
    drv.close()


if __name__ == '__main__':
    main()
