import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, WordCloud, Map, Scatter, Page
from sqlalchemy import create_engine

# 连接数据库
db = create_engine('mysql+pymysql://root:123456@localhost:3306/video')
sql = 'select * from video_bili'
Data_video = pd.read_sql_query(sql, db)

def barChart():  # 视频投币数分析
    video_coins = Data_video.loc[:, ['coin_count', 'type']].groupby('type').sum()
    x = video_coins.index.tolist()
    y = [i[0] for i in video_coins.values.tolist()]
    bar = (
        Bar()
        .add_xaxis(x)
        .add_yaxis('', y)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='各类型视频投币数分析', pos_left='center'),
            yaxis_opts=opts.AxisOpts(name='投币数'),
            xaxis_opts=opts.AxisOpts(name='视频类型',name_location = 'center',name_gap=25)
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(position='top')
        )
    )
    return bar

# 词云图
def wordCloudChart():  # 视频播放量分析
    video_play = Data_video.loc[:, ['title', 'view_count']]
    w_one = video_play['title']
    w_two = video_play['view_count']
    word = (
        WordCloud()
        .add('', [i for i in zip(w_one, w_two)])
        .set_global_opts(
            title_opts=opts.TitleOpts(title='视频播放量分析', pos_left='center')
        )
    )
    return word

# 绘制地图
def mapChart():
    video_province = Data_video.loc[:, ['title', 'province']].groupby('province').count()
    top_province = video_province.nlargest(10, 'title')
    data = [(index, row['title']) for index, row in top_province.iterrows()]
    for i in range(len(data)):
        province, count = data[i]
        data[i] = (province, int(count))
    municipalities = ['北京', '天津', '上海', '重庆']
    processed_data = [(f"{name}市" if name in municipalities else f"{name}省", count) for name, count in data]
    map = (
        Map()
        .add('', processed_data)
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=300, pos_left='10%', pos_bottom='20%'),
            title_opts=opts.TitleOpts(title='上榜up主全国分布情况', pos_left='center', pos_top='15')
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter='{b}')
        )
    )
    return map

# 饼图
def pieChart():
    video_rankings = Data_video.loc[:, ['view_count', 'type']].groupby('type').sum()
    rankings = video_rankings.sort_values(by='view_count', ascending=False)
    top = rankings.head(int(rankings.count().iloc[0] * 0.4))  # 采取排名前40%的类型
    p_one = top.index.tolist()
    p_two = top.values.tolist()

    pie = (
        Pie()
        .add('', [list(z) for z in zip(p_one, p_two)], radius=[40, 70])
        .set_global_opts(
            title_opts=opts.TitleOpts(title='视频播放量类型前40%占比情况', pos_left='center'),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter='{b}: {d}%')
        )
    )
    return pie
# 绘制散点图
def scatterChart():
    transmit = Data_video.loc[:, ['type', 'share_count']].groupby('type').sum()
    s_one = transmit.index.tolist()
    s_two = transmit.values.tolist()
    scatter = (
        Scatter()
        .add_xaxis(s_one)
        .add_yaxis('', s_two)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='各类型视频转发量', pos_left='center'),
            xaxis_opts=opts.AxisOpts(name='视频类型'),
            yaxis_opts=opts.AxisOpts(name='总转发量')
        )
    )
    return scatter

page = Page(layout=Page.DraggablePageLayout)
page.add(barChart(), wordCloudChart(), pieChart(), mapChart(), scatterChart())
Page.save_resize_html("test.html",
	cfg_file="my_charts.json",
 	dest="my_test1.html")
