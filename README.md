# Bilibili视频数据分析项目
本项目旨在分析Bilibili视频数据，包括视频类型、观看次数、投币数等统计信息。
使用Pythonc程序(get_bilibili.py)从Bilibili API获取数据
存储到MySQL数据库中，并使用pyecharts进行数据可视化。

## 目录
1. [概述](#概述)
2. [设置](#设置)
3. [Python脚本](#python脚本)
   - [get_bilibili.py](#get_bilibilipy)
   - [dataPresentation.py](#datapresentationpy)
4. [MySQL表头字段说明](#MySQL表头字段说明)

## 概述
本项目（项目名称：class_design）提供对Bilibili视频数据的全面分析，重点关注视频类型、观看次数、投币数等多种指标。
数据从Bilibili API获取，存储在MySQL数据库中，并使用pyecharts进行可视化，以便更好地理解和洞察。

## 设置
运行本项目前，请确保已安装以下环境：
- Python 3.9
- MySQL数据库
- Pyecharts库
- SQLAlchemy库
- Requests库
- PyMySQL库
可以使用pip安装所需的Python库：

## Python脚本
- get_bilibili.py
该脚本从Bilibili API获取视频数据并存储到MySQL数据库中。
API URL: https://api.bilibili.com/x/web-interface/ranking/v2
Headers: 包含请求的用户代理。
数据库连接: 连接到名为video的MySQL数据库，用户名root，密码123456。
脚本遍历不同的视频类别，获取数据，并将其插入video_bili表中。

- dataPresentation.py
该脚本负责可视化存储在MySQL数据库中的数据。
柱状图: 分析不同视频类型的投币数。
词云图: 分析视频观看次数。
地图: 显示视频上传在各省的分布情况。
饼图: 展示前40%视频类型的视频观看次数比例。
散点图: 分析不同视频类型的转发量。
使用pyecharts的Page布局将可视化组合成一个HTML页面。

- 数据可视化
可视化结果保存为名为test.html的HTML文件。
图表的布局和大小在my_charts.json文件中配置,my_charts.json文件包含图表布局的配置。
test.html、my_charts.json需要同python程序文件在同一文件夹下（即路径一致）

## MySQL表头字段
- 创建的MySQL数据表表头为自定义变量，此项为对应视频类型：
- type 视频类型
title 标题
pubdate 发布时间
owner_name up主
view_count 播放量
coin_count 投币数
danmaku_count 弹幕数
favorite_count 收藏数
like_count 点赞数
share_count 转发量
reply_count 评论数
province 省份/直辖市
- （MySQL文件参考video_bili.sql）

