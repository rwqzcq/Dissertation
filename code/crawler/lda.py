# -*- coding: utf-8 -*-
import pymysql
import numpy as np

words_ls = []

db = pymysql.connect("localhost","root","","feiyi")
cursor = db.cursor()
max_id = 3157
current_id = 8
step = 3149
next_id = current_id + step

sql = ''' select `id`, `full_keywords` from `minglu` where `id` >= {0} and `id` <= {1} and `full_keywords` is not null '''.format(current_id, next_id)
try:
# 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        keywords = row[1].replace('传统', '').replace('文化', '')
        # 字符串替换
        k_list = keywords.split(' ')
        k_list = [x for x in k_list if x != '']
        words_ls.append(k_list)       
except:
    print ("Error: unable to fetch data")
# print(words_ls)

from gensim import corpora, models
dictionary = corpora.Dictionary(words_ls)
corpus = [dictionary.doc2bow(words) for words in words_ls]
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=1)
lda.load('./test_lda.model')
# 打印所有主题，每个主题显示4个词
for topic in lda.print_topics(num_words=5):
    print(topic)
#print(lda.inference(corpus))
# topic_number = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}
# topic_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# for e, values in enumerate(lda.inference(corpus)[0]): # e为索引 
#     max_id = np.argmax(values)
#     topic_number[max_id] = topic_number[max_id] + 1
#     #print(values)
#     # print("--" + str(e))
#     # for ee, value in enumerate(values):
#     #     print('\t主题%d推断值%.2f' % (ee, value))
# #[425, 157, 324, 121, 221, 253, 192, 151, 486, 356] 
# # 存储到数据库中
# print(topic_number)

## 统计每一个主题下的文档数



#print(lda.inference(corpus)[0])
# word_id = dictionary.doc2idx(['服饰'])[0]
# for i in lda.get_term_topics(word_id):
#     print('【长途】与【主题%d】的关系值：%.2f%%' % (i[0], i[1]*100))

# 计算文档相似度 https://blog.csdn.net/android_ruben/article/details/75576961
keywords = '正字 本名 正音 中州 官话 唱念 一个多 声腔 古老 稀有 剧种 明初 南戏 一支 传入 粤东 正字 扎根 海陆丰 传播 港澳台 东南亚 正字 戏有 传统 剧目 两千 六百多个 分为 文戏 武戏 两类 文戏 明代 宣德 七年 正字 刘希必 金钗 嘉靖 年间 蔡伯喈 南戏 抄本 一批 较完整 清代 民国 抄本 世纪 年代 记录本 三元 五桂记 满床 月华 四大 喜戏 荆钗记 葵花 琵琶 白兔 四大 苦戏 忠义 千里驹 铁弓缘 马陵道 四大 马戏 统称 十二 本戏 武戏 多为 连台本戏 三国 隋唐 正字 表演 风格 古朴 气魄 宏大 特别 擅演 连台本戏 文戏 唱腔 保留 古老 面貌 曲牌 正音 牌子 杂以 乱弹 小调 正音 曲以 奚琴 领奏 大锣 大鼓 伴奏 牌子 笛子 大小 唢呐 伴奏 正音 曲中 很多 曲牌 继承 弋阳 青阳 古腔 滚唱 较为 昆腔 曲牌 一百多支 一部分 充分体现 北曲 完整 组织 形式 武戏 提纲 少有 唱腔 吹打 牌子 伴奏 渲染 气氛 气氛 热烈 火爆 有抖 靠旗 肌肉 髯口 布马 展示 南派 武功 精彩表演 表现 历史 军事 场景 正字 传统 有红面 乌面 白面 老生 武生 白扇 正旦 花旦 帅主 公末 行当 演出 行当 勾画 脸谱 正字 脸谱 毛面 水龟目 鹰嘴 虎目 两百多种 图案 正字 戏是 古老 南戏 变体 戏曲 声腔 流变 地方 文化 戏曲 影响 研究 提供 证据 正字 生存 危机 抢救 保护'
#keywords = '山东省 特色美食 周村 美食 周村烧饼 烧饼 名片山东'
bow = dictionary.doc2bow(keywords.split(' '))
ndarray = lda.inference([bow])[0]
# print(text5)
topic_similar_index = np.argmax(ndarray)
for e, value in enumerate(ndarray[0]):
    print('\t主题%d推断值%.2f' % (e, value))


for e, values in enumerate(lda.inference(corpus)[0][0:100]): # e为索引 
    max_id = np.argmax(values)
    max_value = values[max_id]
    if max_id == topic_similar_index:
        # 查询数据库
        print(str(e + 9) + '--' + str(max_value))

# 从数据库中