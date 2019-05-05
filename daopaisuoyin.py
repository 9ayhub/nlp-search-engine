#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import string
import jieba
import codecs
import os
from collections import Counter
 
#建立倒排索引(单个文件)
#输入:fenci.txt
#输出:my_index.txt  格式: word [[所在文件，出现次数],[所在文件，出现次数]...] 
def create_inverted_index(filename, page):
    src_data = codecs.open('199801_new.txt','r+',encoding='utf-8').read()#必须事先知道文件的编码格式，这里文件编码是使用的utf-8 
    #去除BOM头
    if src_data[:1].encode('utf-8') == codecs.BOM_UTF8:
        src_data = src_data[1:]

    #注释掉的内容是计算词的位置
    
    #变量说明
    # sub_list = [] #所有词的list,  用来查找去重等
    # word = []     #词表文件
    # result = {}   #输出结果 {单词:index}

    #建立词表
    sp_data = src_data.split()
    # set_data = set(sp_data)	#去重复
    # word = list(set_data) #set转换成list, 否则不能索引
    
    #词频
    words = list(sp_data)
    dic_word_count = Counter(words)
    for word in dic_word_count.keys():
        dic_word_count[word] = [int(page), dic_word_count[word]]
        if word in index.keys():
            index[word].append(dic_word_count[word])
        else:
            index[word] = [dic_word_count[word]]
    
    # #词位置
    # src_list = src_data.split("\n") #分割成单段话vv
    # #建立索引
    # for w in range(0,len(word)):
    #     para_pos = []  #记录段落及段落位置 [(段落号,位置),(段落号,位置)...]
    #     for i in range(0,len(src_list)):  #遍历所有段落 
    #         #print(src_list[i])
    #         sub_list = src_list[i].split()
    #         #print(sub_list)
    #         for j in range(0,len(sub_list)):  #遍历段落中所有单词
    #             #print(sub_list[j])
    #             if sub_list[j] == word[w]:
    #                 para_pos.append((i,j))
    #         result[word[w]] = para_pos



#主函数
def main():
    #遍历data\\page下的文件
    #对于每个文件xx.txt，首先分词，将分词结果写入fenci.txt
    #然后建立倒排索引，将结果与index（总的索引）合并
    fenci_txt = "fenci.txt"
    with codecs.open(fenci_txt, 'w', encoding="UTF-8-SIG") as f:
        path = "data\\page" #文件夹目录
        files= os.listdir(path) #得到文件夹下的所有文件名称
        s = []
        for file in files: #遍历文件夹
            if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
                print('>>>处理', file)
                for line in open(path+"\\"+file,encoding='utf-8',errors='ignore').readlines():
                    #去标点
                    line = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", " ", line)
                    #分词
                    seg_list = jieba.cut(line, cut_all=True)
                    #写入199801_new.txt
                    f.write(" ".join(seg_list)+"\n")        
                #建立倒排索引
                create_inverted_index(fenci_txt, re.sub(r'\D', "", file))
    
    with codecs.open("my_index.txt", 'w', encoding="UTF-8-SIG") as i:
        for key in index.keys():
            i.write(key + str(index[key]) + "\n")

index = {}

#运行
if __name__ == '__main__':
    main()

