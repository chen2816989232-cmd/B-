import requests
import pymysql
from datetime import datetime

url = 'https://api.bilibili.com/x/web-interface/ranking/v2'
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}
dict_a = {
    '动画': 1, '音乐': 3, '舞蹈': 129, '游戏': 4, '知识': 36, '科技': 188, '运动': 234, '汽车': 223,
    '生活': 160, '美食': 211, '动物圈': 217, '鬼畜': 119, '时尚': 155, '娱乐': 5, '影视': 181
}

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='video',
    charset='utf8mb4'
)
try:
    cursor = connection.cursor()
    for a in dict_a:
        params = {'rid': dict_a[a], 'type': 'all'}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data_list = response.json()['data']['list']
            for i in data_list:
                try:
                    province = i['pub_location']
                except:
                    province = 'null'
                else:
                    pubdate = datetime.fromtimestamp(int(i['pubdate'])).strftime('%Y-%m-%d')
                    insert_query = """
                    INSERT INTO video_bili (type, title, pubdate, owner_name, view_count, 
                    coin_count, danmaku_count, favorite_count, like_count, share_count, reply_count, province)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        a,#视频类型
                        i['title'],#标题
                        pubdate,#发布时间
                        i['owner']['name'],#up主
                        i['stat']['view'],#播放量
                        i['stat']['coin'],#投币数
                        i['stat']['danmaku'],#弹幕数
                        i['stat']['favorite'],#收藏数
                        i['stat']['like'],#点赞数
                        i['stat']['share'],#转发量
                        i['stat']['reply'],#评论数
                        province#省份/直辖市
                    ))
            connection.commit()
        except requests.RequestException as e:
            print(f"请求错误：{e}")
finally:
    cursor.close()
    connection.close()
    print("所有排行榜数据已保存到MySQL数据库")
