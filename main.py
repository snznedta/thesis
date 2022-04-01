# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from snownlp import seg
import jieba



def main():
    jieba.add_word("积极心理学")
    mytext = " ".join(jieba.cut("今天我要写完积极心理学的论文大纲"))
    print(mytext)
    for i in range(95, 160):
        print("https://movie.douban.com/subject/35438177/comments?start=" + str(i * 100) + "&limit=100&status=P&sort=new_score" )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
