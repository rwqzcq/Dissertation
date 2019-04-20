# coding=utf-8
#  /usr/local/bin/python3 /Users/renweiqiang/Desktop/毕业论文/Dissertation/code/crawler/fenci.py
import pymysql
import time
import jieba
import jieba.analyse


text = '苗族分布在我国西南数省区。按方言划分，大致可分为湘西方言区、黔东方言区、川滇黔方言区。黔东南清水江流域一带是全国苗族最大的聚居区，大致包括凯里、剑河、黄平、台江、雷山、丹寨、施秉、黄平、镇远、三穗，以及广西三江和湖南靖县等地。在此广大苗族聚居区普遍流传着一种以创世为主体内容的诗体神话，俗称“古歌”或“古歌古词”。 苗族古歌内容包罗万象，从宇宙的诞生、人类和物种的起源、开天辟地、初民时期的滔天洪水，到苗族的大迁徙、苗族的古代社会制度和日常生产生活等，无所不包，成为苗族古代神话的总汇。 苗族古歌古词神话大多在鼓社祭、婚丧活动、亲友聚会和节日等场合演唱，演唱者多为中老年人、巫师、歌手等。酒席是演唱古歌的重要场合。苗族的古歌古词神话是一个民族的心灵记忆，是苗族古代社会的百科全书和“经典”，具有史学、民族学、哲学、人类学等多方面价值。今天，这些古歌古词神话还在民间流传唱诵。 但由于受到现代文化和市场经济的冲击，苗族古歌已濒临失传。以台江为例，在全县13万苗族同胞中，能唱完整部古歌的已寥寥无几，目前只有二百余人能唱一些不完整的古歌，而且都是中老年人，传承古歌较多的老人年事已高。如不抓紧抢救保护，苗族古歌这一民族瑰宝将最终在世间消失。'

# 对新的文档进行预测
text5 = '正字戏本名正音戏，用中州官话唱念，是一个多声腔的古老稀有剧种。明初南戏的一支传入粤东，形成正字戏，主要扎根于海陆丰地区，后传播到港澳台及东南亚等地 .正字戏有传统剧目两千六百多个，分为文戏和武戏两类。文戏有明代宣德七年的《正字刘希必金钗记》及嘉靖年间的《蔡伯喈》南戏抄本和一批较完整的清代、民国抄本，以及20世纪50年代的记录本。《三元记》、《五桂记》、《满床笏》、《月华缘》“四大喜戏”，《荆钗记》、《葵花记》、《琵琶记》、《白兔记》“四大苦戏”和《忠义烈》、《千里驹》、《铁弓缘》、《马陵道》“四大弓马戏”统称十二真本戏。武戏多为连台本戏，如《三国》、《隋唐》等。正字戏表演风格古朴，气魄宏大，特别擅演连台本戏。文戏的唱腔保留着古老的面貌，以曲牌体的正音曲、唱牌子为主，杂以乱弹、小调等。正音曲以奚琴领奏，大锣、大鼓伴奏，唱牌子以笛子、大小唢呐伴奏。正音曲中有很多曲牌直接继承了弋阳、青阳古腔，滚唱运用得较为普遍。昆腔曲牌有一百多支，其中有一部分充分体现了北曲严格、完整的组织形式。武戏即提纲戏，没有或少有唱腔，用吹打牌子伴奏以渲染气氛，气氛热烈火爆，有抖靠旗、抖肌肉、抖髯口、跑布马、展示南派武功等精彩表演，能很好地表现各种历史、军事场景。正字戏传统有红面、乌面、白面、老生、武生、白扇、正旦、花旦、帅主、公末、婆、丑等12行当，演出中有些行当勾画脸谱。正字戏的脸谱有毛面、水龟目、鹰嘴、虎目等两百多种图案。正字戏是古老南戏的变体，为戏曲声腔的流变和地方文化对戏曲的影响等研究提供有力的证据。目前正字戏的生存出现危机，需要有关方面及时加以抢救和保护。'

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

def get_keywords(text):
    keywords = filter_seg_list(jieba.cut(text)) # 去除停用词
    keywords = [j for j in keywords if filter_number_and_single(j) != False]
    jieba_keywords_text = " ".join(keywords)
    # topK = 20
    # withWeight = False
    # tags = jieba.analyse.extract_tags(jieba_keywords_text, topK=topK, withWeight=withWeight)
    #return ' '.join(keywords), " ".join(tags)
    return ' '.join(keywords)
print(get_keywords(text5))