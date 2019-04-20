# 爬起分物质文化遗产名录

# /anaconda3/bin/python /Users/renweiqiang/Desktop/毕业论文/Dissertation/code/crawler/minglu.py
# pip install --upgrade --force-reinstall beautifulsoup4
import requests
from bs4 import BeautifulSoup
import pymysql


def test_parse():
    base_url = 'http://www.ihchina.cn/project_details/12178'
    page = requests.get(base_url).text
    soup = BeautifulSoup(page, 'html.parser')
    # 获取描述 .article-mod2 .text div.p
    name = soup.find('div', class_ = 'h30').get_text()
    print(name)
    pass
    contents = soup.find_all('div', class_ = "p")
    content = contents[7].get_text() # 描述
    type = contents[3].get_text().split("：")[1] # 类型
    area = contents[4].get_text().split("：")[1] # 地区
    apply_area = contents[6].get_text().split("：")[1] # 地区

#test_parse()
# begin_index = 12178

# end_index = 12178 #15330

# base_url = 'http://www.ihchina.cn/project_details/' # 原始链接





# print(base_url)

# 数据库
def insert(db, f_id, name, type, content, area, concrete_area, source_url):
    # db = pymysql.connect("localhost","root","","feiyi")
    cursor = db.cursor()
    sql = """INSERT INTO `minglu`(
                        `f_id`,
                        `name`,
                        `type`,
                        `content`,
                        `area`,
                        `concrete_area`,
                        `source_url`
                    )
        VALUES      ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(f_id, name, type, content, area, concrete_area, source_url)
    try:
    # 执行sql语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
    # 如果发生错误则回滚
        db.rollback()

    # db.close()


begin_index = 12178

end_index = 15330

base_url = 'http://www.ihchina.cn/project_details/' # 原始链接

db = pymysql.connect("localhost","root","","feiyi")

count = 1

while begin_index <= end_index:
    url = base_url + str(begin_index)
    
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    # 获取描述 .article-mod2 .text div.p
    name = soup.find('div', class_ = 'h30').get_text()
    contents = soup.find_all('div', class_ = "p")
    content = contents[7].get_text() # 描述
    type = contents[3].get_text().split("：")[1] # 类型
    area = contents[4].get_text().split("：")[1] # 地区
    concrete_area = contents[6].get_text().split("：")[1] # 地区
    source_url = base_url
    f_id = begin_index

    insert(db, f_id, name, type, content, area, concrete_area, source_url)

    print(name + "--" + str(count))

    begin_index = begin_index + 1

    count = count + 1

db.close()
