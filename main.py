import runner
import mod_coin
import time


def main():
    br = runner.Runner()
    if br.start() != 0:
        return 1
    mod1 = mod_coin.Mod(br)
    # while True:
    #     time.sleep(3)
    #     pass
    # mod1.loop(1)
    for i in range(5):
        mod1.coinVideo(mod1.getVideoUrlInRecommend(), coin=False, share=True, watch=True)
    time.sleep(3)
    br.biliCore.quit()


if __name__ == '__main__':
    main()
