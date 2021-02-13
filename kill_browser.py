import os


def main():
    if os.name == "nt":
        print("此脚本暂不支持windows系统")
        return 1
    cmd = "netstat -tlp | egrep '(firefox|gecko)'"
    cmdResult = os.popen(cmd).readlines()
    for i in cmdResult:
        j = i.split()[6].split("/")[0]
        os.system(f"kill -9 {j}")
        print(f"结束了进程: {j}")


if __name__ == '__main__':
    main()
