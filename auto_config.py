import requests
import qrcode
import time
import os

from requests.cookies import RequestsCookieJar


def getQrUrl(urlbase: str, header: dict) -> dict:
    ret = requests.get(urlbase, headers=header)
    r_json = dict(ret.json())
    if r_json["code"] != 0:
        raise ConnectionError("接口访问失败")
    return r_json


def checkQrStatus(urlbase: str, header: dict, key: str) -> tuple[dict, RequestsCookieJar]:
    ret = requests.post(urlbase, headers=header, data={
        "oauthKey": key
    })
    r_json = dict(ret.json())
    if r_json["data"] == -2 or r_json["data"] == -1:
        raise ConnectionError("超时或其他错误, 重试")
    return r_json, ret.cookies


def getNowStatusString(num: int):
    dic_string = {-1: "密钥错误",
                  -2: "密钥超时",
                  -4: "未扫描",
                  -5: "未确认", }
    return dic_string[num]


def main():
    b_getQrUrl = "https://passport.bilibili.com/qrcode/getLoginUrl"
    b_statusUrl = "https://passport.bilibili.com/qrcode/getLoginInfo"
    my_header = {"User-Agent": "Mozilla/5.0 (linux; none) Gecko/84.0 Firefox/84.0"}
    while True:
        print("Please wait ...")
        r_rep = getQrUrl(b_getQrUrl, my_header)
        r_qrUrl = r_rep["data"]["url"]
        r_authKey = r_rep["data"]["oauthKey"]
        print("访问此地址, 或使用手机扫描此二维码:")
        print(r_qrUrl)
        r_qr = qrcode.QRCode(box_size=1, border=1)
        r_qr.add_data(r_qrUrl, optimize=0)
        r_qr.print_ascii(invert=True)
        print("等待扫描...")
        r_lastStatus = -99
        while True:
            time.sleep(1)
            try:
                r_rep, r_cookies = checkQrStatus(b_statusUrl, my_header, r_authKey)
            except ConnectionError as e:
                print(e)
                break
            r_QrStatus = r_rep["status"]
            if r_QrStatus:
                print("扫码成功, 设置cookies...")
                cfgFile = f"config{os.path.sep}cookie.txt"
                cfgFileObj = open(cfgFile, mode="w")
                for key, val in r_cookies.items():
                    print(f"写入cookie: {key} => {val}")
                    cfgFileObj.write(f"{key}={val};")
                cfgFileObj.close()
                print("完成.")
                return 0
            r_nowStatus = r_rep["data"]
            if r_nowStatus != r_lastStatus:
                print(f"当前状态: {getNowStatusString(r_nowStatus)}")
                r_lastStatus = r_nowStatus


if __name__ == '__main__':
    main()
