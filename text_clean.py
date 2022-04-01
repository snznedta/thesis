import pandas
from snownlp import seg
import jieba
import re
import pandas as pd


# https://blog.nowcoder.net/n/2cedf644b16047e990e98d46a45b569b#%E4%B8%AD%E6%96%87%E6%96%87%E6%9C%AC%E9%A2%84%E5%A4%84%E7%90%86%E6%80%BB%E7%BB%93
# 去除停用词，返回去除停用词后的文本列表
def clean_stopwords(contents):
    contents_list = []
    stopwords = {}.fromkeys([line.rstrip() for line in open('data/baidu_stopwords.txt', encoding="utf-8")])  # 读取停用词表
    stopwords_list = set(stopwords)
    for row in contents:  # 循环去除停用词
        words_list = jieba.lcut(row)
        words = [w for w in words_list if w not in stopwords_list]
        sentence = ''.join(words)  # 去除停用词后组成新的句子
        contents_list.append(sentence)
    return contents_list


def remove_sentiment_character(sentence):
    # pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^，^。^?^？^！^a-z^A-Z^0-9]")  # 只保留中英文、数字和符号，去掉其他东西
    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字和符号，去掉其他东西
    # 若只保留中英文和数字，则替换为
    line = re.sub(pattern, '', sentence)  # 把文本中匹配到的字符替换成空字符
    new_sentence = ''.join(line.split())  # 去除空白
    return new_sentence


# 去除字母数字表情和其它字符
def clear_character(sentence):
    pattern1 = '[a-zA-Z0-9]'
    pattern2 = '\[.*?\]'
    pattern3 = re.compile(u'[^\s1234567890:：' + '\u4e00-\u9fa5]+')
    pattern4 = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    line1 = re.sub(pattern1, '', sentence)  # 去除英文字母和数字
    line2 = re.sub(pattern2, '', line1)  # 去除表情
    line3 = re.sub(pattern3, '', line2)  # 去除其它字符
    line4 = re.sub(pattern4, '', line3)  # 去掉残留的冒号及其它符号
    new_sentence = ''.join(line4.split())  # 去除空白
    return new_sentence


# 将清洗后的文本和标签写入.csv文件中
def after_clean2csv(contents, labels):  # 输入为文本列表和标签列表
    columns = ['contents']
    save_file = pd.DataFrame(columns=columns, data=list(zip(contents)))
    save_file.sort_values("contents", inplace=True)
    save_file.to_csv('data/短评文本2.csv', index=False, encoding="utf-8")


def main():
    df = pandas.read_csv("data/再见爱人-短评2-utf8.csv")
    a = []
    for text in df['短评内容']:
        text = clear_character(text)
        a.append(text)
    b = clean_stopwords(a)
    after_clean2csv(b, [])



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
