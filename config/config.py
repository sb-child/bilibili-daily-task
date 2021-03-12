import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# --- 用户设置 ---
# 无头模式
HEADLESS = os.path.exists(f"{SCRIPT_PATH}{os.path.sep}s_headless")
# --- end ---


def getCookies():
    f = open(f"{SCRIPT_PATH}{os.path.sep}cookie.txt")
    cookie_text = f.read()
    f.close()
    c_list = []
    for i in cookie_text.split(";"):
        if i == "":
            continue
        i = i.strip()
        j = i.split("=")
        item = {'name': j[0].strip(), 'value': j[1].strip(), 'path': '/',
                'domain': '.bilibili.com', 'secure': False,
                'httpOnly': False}
        c_list.append(item)
    return c_list


def main():
    print(getCookies())


if __name__ == '__main__':
    main()
