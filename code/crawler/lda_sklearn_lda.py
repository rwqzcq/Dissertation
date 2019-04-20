# encoding = utf-8
import pymysql
import numpy as np
import lda
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer



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
        #keywords = row[1].replace('传统', '').replace('文化', '')
        # 字符串替换
        # k_list = keywords.split(' ')
        # k_list = [x for x in k_list if x != '']
        k_list = row[1]
        words_ls.append(k_list)       
except:
    print ("Error: unable to fetch data")

corpus = words_ls

vectorizer = CountVectorizer() # 返回一个vectorizer对象
X = vectorizer.fit_transform(corpus) # 返回的是一个 sparse matrix of type
weight = X.toarray() # 转为数组 10 行 15 列的数组
from sklearn.decomposition import LatentDirichletAllocation
n_topic = 20

model = LatentDirichletAllocation(n_topics=n_topic, max_iter=2000, learning_method='batch')
model.fit(X)
# model = lda.LDA(n_topics=10, n_iter=2000, random_state=1)
# model.fit(np.asarray(weight)) # 开始训练

# 文档-主题分布
# print("文档-主体分布")
# doc_topic = model.doc_topic_
# print("type(doc_topic): {}".format(type(doc_topic)))
# print("shape: {}".format(doc_topic.shape))

# # 输出前10篇文章最可能的Topic
# print("输出前10篇文章最可能的Topic")
# label = []
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     label.append(topic_most_pr)
#     print("doc: {} topic: {}".format(n, topic_most_pr))

# topic_word = model.topic_word_
# word = vectorizer.get_feature_names() # 分词的结果

# n = 5
# for i, topic_dist in enumerate(topic_word):  
#     topic_words = np.array(word)[np.argsort(topic_dist)][:-(n+1):-1]  
#     print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words))) 