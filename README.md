<div align="center">
<h1 align="center">
bilibili-daily-task
</h1>
<h2 align="center">
自动完成 <a href="https://bilibili.com">Bilibili</a> 的每日任务(开发中)
</h2>

[![GitHub stars](https://img.shields.io/github/stars/sb-child/bilibili-daily-task?label=stars%2F%E6%98%9F%E6%A0%87&style=flat-square)](https://github.com/sb-child/bilibili-daily-task/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sb-child/bilibili-daily-task?label=forks%2F%E5%88%86%E6%94%AF&style=flat-square)](https://github.com/sb-child/bilibili-daily-task/network)
[![GitHub issues](https://img.shields.io/github/issues/sb-child/bilibili-daily-task?label=issues%2F%E8%AE%AE%E9%A2%98&style=flat-square)](https://github.com/sb-child/bilibili-daily-task/issues)
[![GitHub license](https://img.shields.io/github/license/sb-child/bilibili-daily-task?label=license%2F%E8%AE%B8%E5%8F%AF%E8%AF%81&style=flat-square)](https://github.com/sb-child/bilibili-daily-task/blob/main/LICENSE)
</div>

## 本项目正在逐步完善. 可时刻关注本项目以体验最新的特性和bug修复.

### overview
> 使用`selenium`模块控制浏览器完成每日任务

### todo
- [x] ~修复bug: `分享` 按钮不能点击 [link](https://github.com/sb-child/bilibili-daily-task/blob/main/mod_coin.py#L63)~

### 功能 / functions
- [x] 使用cookies登录
- [x] 自动观看, 点赞, 投币, 分享
- [ ] 正在完善...

### 测试 / test
> 随机获取视频, 点赞转发 5 次 ([link](https://www.sbchild.top/bdt_1.mp4))  
> 额外: 随机获取视频, 点赞转发 50+ 次 (尽可能多的找出潜在的bug)

### 特点 / feature
> - 模拟操控浏览器, 尽可能防止被封杀
> - 移除了`navigator.webdriver`接口
> - 无头模式 (见 配置文件)

### 如何使用 / how to use
#### 安装python环境
> 版本建议 python3.8 +
> 详细步骤参考相关文章

#### 安装依赖库
> 针对linux系统. Windows用户需将`pip3`改为`pip`.
```
pip3 install bs4 urllib3 lxml selenium
```

#### 安装firefox浏览器和driver
> todo...
```
todo
```

#### 设置cookie
> 修改 配置文件

#### 运行
> 针对linux系统. Windows用户需将`python3`改为`python`.
```
python3 main.py
```
> 可自行修改此文件, 定制功能

### 配置文件 / config files
> 配置文件目录:`config/`
> 相关说明在此目录中

### 注意事项 / warning
> - 运行过程中, 不要将鼠标光标放入浏览器网页区域内.
> - 若脚本抛出异常并终止, 导致处于无头模式的浏览器仍在运行, 使用`kill_browser.py`结束后台的浏览器进程(暂不支持windows).
