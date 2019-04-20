# coding=utf-8
#  /usr/local/bin/python3 /Users/renweiqiang/Desktop/毕业论文/Dissertation/code/crawler/fenci.py
import pymysql
import time
import jieba
import jieba.analyse


text = '苗族分布在我国西南数省区。按方言划分，大致可分为湘西方言区、黔东方言区、川滇黔方言区。黔东南清水江流域一带是全国苗族最大的聚居区，大致包括凯里、剑河、黄平、台江、雷山、丹寨、施秉、黄平、镇远、三穗，以及广西三江和湖南靖县等地。在此广大苗族聚居区普遍流传着一种以创世为主体内容的诗体神话，俗称“古歌”或“古歌古词”。 苗族古歌内容包罗万象，从宇宙的诞生、人类和物种的起源、开天辟地、初民时期的滔天洪水，到苗族的大迁徙、苗族的古代社会制度和日常生产生活等，无所不包，成为苗族古代神话的总汇。 苗族古歌古词神话大多在鼓社祭、婚丧活动、亲友聚会和节日等场合演唱，演唱者多为中老年人、巫师、歌手等。酒席是演唱古歌的重要场合。苗族的古歌古词神话是一个民族的心灵记忆，是苗族古代社会的百科全书和“经典”，具有史学、民族学、哲学、人类学等多方面价值。今天，这些古歌古词神话还在民间流传唱诵。 但由于受到现代文化和市场经济的冲击，苗族古歌已濒临失传。以台江为例，在全县13万苗族同胞中，能唱完整部古歌的已寥寥无几，目前只有二百余人能唱一些不完整的古歌，而且都是中老年人，传承古歌较多的老人年事已高。如不抓紧抢救保护，苗族古歌这一民族瑰宝将最终在世间消失。'

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath).readlines()]
    return stopwords
def filter_seg_list(seg_list):
    stop_words = stopwordslist('/Users/renweiqiang/Desktop/毕业论文/学习总结/LDA_Python/文本预处理/stop_words.txt')
    filter_seg = []
    for word in seg_list:
        if word not in stop_words:
            filter_seg.append(word)
    filter_seg =  [i for i in filter_seg if i != '']
    return filter_seg
def filter_number_and_single(word):
    if(word.isdigit()):
        return False
    length = len(word)
    if(length not  in [0, 1]):
        return word
    return False

# corpus = []
# corpus.append(" ".join(keywords))
# #print( " ".join(keywords))



def get_keywords(text):
    keywords = filter_seg_list(jieba.cut(text)) # 去除停用词
    keywords = [j for j in keywords if filter_number_and_single(j) != False]
    jieba_keywords_text = " ".join(keywords)
    # topK = 20
    # withWeight = False
    # tags = jieba.analyse.extract_tags(jieba_keywords_text, topK=topK, withWeight=withWeight)
    #return ' '.join(keywords), " ".join(tags)
    return ' '.join(keywords)
# keywords = get_keywords(text)
# print(keywords[0])
# print(keywords[1])

db = pymysql.connect("localhost","root","","feiyi")
cursor = db.cursor()
# sql = "select count(*) from `minglu`"
# cursor.execute(sql)
# count = cursor.fetchone()[0]

# max_id_sql = "select max(id) from `minglu`"
# cursor.execute(sql)
# max_id = cursor.fetchone()[0]
# min_id = 8

# while(max_id <= 3260):
#     content_sql = '''select `content` from `minglu` where `id` in ({0}, {1})'''.format(min_id, max_id)
 
#sql = "select `id`, `content` from `minglu` where `id` > 10"
max_id = 3157
current_id = 8
step = 100

while(current_id <= max_id):
    next_id = current_id + step

    sql = ''' select `id`, `content` from `minglu` where `id` >= {0} and `id` <= {1} '''.format(current_id, next_id)
    try:
    # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            content = row[1]
            if content.strip():
                keywords = get_keywords(content)
                update_sql = ''' update `minglu` set `full_keywords` = "{0}" where `id` = {1} '''.format(keywords, id)
                #print(update_sql)
                print('---' + str(id))        
                try:
                    cursor.execute(update_sql)
                    db.commit()
                except:
                    db.rollback()
            
    except:
        print ("Error: unable to fetch data")

    current_id = current_id + step

    time.sleep(1)



# 关闭数据库连接
db.close()



