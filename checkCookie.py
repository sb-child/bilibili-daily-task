import runner
import auto_config


def main():
    run = runner.Runner()
    result = run.start()
    run.biliCore.quit()
    if result == 0:
        print("可以正常登录.")
    print("登录失败. 使用扫码登录更新cookies...")
    auto_config.main()
    print("登录完成. cookies 内容:")
    with open("config/cookie.txt") as f:
        print(f.read())


if __name__ == '__main__':
    main()
