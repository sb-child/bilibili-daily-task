import time
from config import config
from selenium import webdriver


def main():
    drv = webdriver.Firefox()
    # drv.get("https://passport.bilibili.com/login")

    drv.get("https://www.bilibili.com/")
    loginBtn = drv.find_elements_by_xpath("//div/span/img[@src='//static.hdslb.com/images/akari.jpg']")
    loginBtn1 = drv.find_elements_by_class_name("unlogin-avatar")
    if len(loginBtn) > 0 or len(loginBtn1) > 0:
        print("未登录")
    else:
        print("已登录")
    # time.sleep(60)
    drv.delete_all_cookies()
    cks = config.getCookies()
    for i in cks:
        drv.add_cookie(i)
    drv.get("https://www.bilibili.com/")
    loginBtn = drv.find_elements_by_xpath("//div/span/img[@src='//static.hdslb.com/images/akari.jpg']")
    loginBtn1 = drv.find_elements_by_class_name("unlogin-avatar")
    if len(loginBtn) > 0 or len(loginBtn1) > 0:
        print("未登录")
    else:
        print("已登录")

    # drv.get("https://passport.bilibili.com/login")
    # drv.delete_all_cookies()
    # time.sleep(60)
    # ck = drv.get_cookies()
    # print(ck)
    # drv.get("https://www.bilibili.com/")
    # drv.refresh()
    # drv
    time.sleep(1000)
    drv.close()


if __name__ == '__main__':
    main()
