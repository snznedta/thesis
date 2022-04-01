from snownlp import SnowNLP

import pandas as pd


def after_clean2csv(contents, star, g, h,
                    s,
                    a,
                    f,
                    hate,
                    sur):  # 输入为文本列表和标签列表
    columns = ['star', "好",
               "乐",
               "哀",
               "怒",
               "惧",
               "恶",
               "惊",
               'contents']

    save_file = pd.DataFrame(columns=columns, data=list(zip(star, g, h,
                                                            s,
                                                            a,
                                                            f,
                                                            hate,
                                                            sur, contents)))
    save_file.to_csv('data/情绪分析2.csv', index=False, encoding="utf-8")


from cnsenti import Emotion


def emo_to_string(res):
    return "好{},乐{},哀{},怒{},惧{},恶{},惊{}".format(res['好'], res['乐'], res['哀']
                                                , res['怒']
                                                , res['惧']
                                                , res['恶']
                                                , res['惊'])


def normalize(res):
    gcnt = res['好']
    hcnt = res['乐']
    scnt = res['哀']
    acnt = res['怒']
    frcnt = res['惧']
    hatecnt = res['恶']
    surcnt = res['惊']
    sum = gcnt + hcnt + surcnt + scnt + acnt + frcnt + hatecnt
    if sum == 0:
        return res
    for k, v in res.items():
        res[k] = v / float(sum)
    # res = res / float(sum)
    return res


import re


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

def sentinent_ana():
    df = pd.read_csv("data/再见爱人-短评2-utf8.csv")
    score = []
    i =0
    for row in df.iterrows():
        text = row[1]['短评内容']

        text = clear_character(text)
        if not text or len(text) == 0:
            continue
        s = SnowNLP(text)
        score.append(s.sentiments)
        print(i)
        i = i + 1
    print(sum(score))
    print(sum(score) / len(score))

def analysis():
    df = pd.read_csv("data/再见爱人-短评2-utf8.csv")
    dup = set()
    texts = []
    stars = []
    scores = []
    emo = []
    idx = 0
    emotion = Emotion()

    g = []
    h = []
    s = []
    a = []
    f = []
    hate = []
    sur = []

    for row in df.iterrows():
        idx += 1
        text = row[1]['短评内容']
        if text in dup:
            continue
        else:
            dup.add(text)
        text = clear_character(text)
        star = row[1]['星级评分数']

        res = emotion.emotion_count(text)

        g.append(res['好'])
        h.append(res['乐'])
        s.append(res['哀'])
        a.append(res['怒'])
        f.append(res['惧'])
        hate.append(res['恶'])
        sur.append(res['惊'])
        # result = normalize(result)

        # emot = emo_to_string(result)
        texts.append(text)
        stars.append(star)
        # emo.append(emot)
        # scores.append(score)
        print(str(idx) + ": " + str(star) + " " + str(text))
    return {"star": stars, "contents": texts,
            "好": g,
            "乐": h,
            "哀": s,
            "怒": a,
            "惧": f,
            "恶": hate,
            "惊": sur
            }


def top_comment():
    df = pd.read_csv("data/情绪分析2.csv")
    for i in ["好",
              "乐",
              "哀",
              "怒",
              "惧",
              "恶",
              "惊"]:
        df.sort_values(i, ascending=False, inplace=True)
        df.to_csv("data/情绪分析排序2-" + i + ".csv")



def main():
    dic = analysis()

    after_clean2csv(dic['contents'], dic['star'], dic['好'],
                    dic['乐'],
                    dic['哀'],
                    dic['怒'],
                    dic['惧'],
                    dic['恶'],
                    dic['惊'], )
    top_comment()


if __name__ == '__main__':
    # for i in ["好",
    #           "乐",
    #           "哀",
    #           "怒",
    #           "惧",
    #           "恶",
    #           "惊"]:
    #     print("dic['" + i + "'],")
    # main()
    sentinent_ana()