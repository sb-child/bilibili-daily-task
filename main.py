import runner
import mod_coin
import time


def main():
    br = runner.Runner()
    if br.start() != 0:
        return 1
    mod1 = mod_coin.Mod(br)
    time.sleep(3)
    mod1.loop(2)


if __name__ == '__main__':
    main()
