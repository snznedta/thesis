
import jieba
import pandas as pd
from operator import itemgetter
# 分词词频
def term_freq(contents):
    terms_dict = dict()
    for row in contents:
        row = str(row)
        words_list = jieba.lcut(row)
        for word in words_list:
            if word in terms_dict:
                cnt = terms_dict[word]
                terms_dict[word] = cnt + 1
            else:
                terms_dict[word] = 1
    return sorted(terms_dict.items(), key=itemgetter(1), reverse=True )

# 分析tfidf

def after_clean2csv(contents, labels):  # 输入为文本列表和标签列表
    columns = ['term', 'freq']
    save_file = pd.DataFrame(columns=columns, data=list(zip(contents,labels)))
    save_file.to_csv('data/词频2.csv', index=False, encoding="utf-8")


from wordcloud import WordCloud
import numpy as np
import PIL.Image as Image



def chinese_jieba(text):
    wordlist_jieba = jieba.cut(text)
    space_wordlist = " ".join([str(i) for i in wordlist_jieba])
    return space_wordlist

def word_cloud_gen():
    df = pd.read_csv("data/短评文本2.csv")
    # 读取csv文件

    comment_list = df['contents'].values.tolist()
    text = ""
    for comment in comment_list:
        text = text + " " + chinese_jieba(str(comment))

    # 调用PIL中的open方法，读取图片文件，通过numpy中的array方法生成数组
    # mask_pic = np.array(Image.open("background_love.jpg"))
    wordcloud = WordCloud(font_path="data/simsun.ttf",
                            # mask=mask_pic,
                          background_color='white',
                          max_font_size=150,
                          collocations=False,
                          max_words=200,
                          scale=2
                          # stopwords={i for i in set(stop_words.iloc[:,0])},
                          ).generate(text)
    image = wordcloud.to_image()
    wordcloud.to_file('data/word_cloud.png')
    # wordcloud.to_file(wordcloud_name)
    image.show()


def main():
    word_cloud_gen()
    df = pd.read_csv("data/短评文本2.csv")
    dic = term_freq(df['contents'])
    keys = [x[0] for x in dic]
    vals = [x[1] for x in dic]
    after_clean2csv(keys, vals)




if __name__ == '__main__':
    main()