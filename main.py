import runner
import mod_coin
import time


def main():
    br = runner.Runner()
    if br.start() != 0:
        return 1
    mod1 = mod_coin.Mod(br)
    """
    # 自定义: 不投币, 但转发, 观看, 点赞
    # 执行5次
    for i in range(5):
        while True:
            if mod1.coinVideo(mod1.getVideoUrlInRecommend(), coin=False, share=True, watch=True, like=True) == 0:
                break
    """
    # 默认看5次视频, 点5次赞, 转发1次, 投5个硬币
    mod1.loop()
    time.sleep(3)
    br.biliCore.quit()


if __name__ == '__main__':
    main()
