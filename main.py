#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import string
import jieba
import codecs
import os
import math
import time
import Correct as correct
from collections import Counter
 
#������������(�����ļ�)
#����:fenci.txt
#���:my_index.txt  ��ʽ: word [[�����ļ������ִ���],[�����ļ������ִ���]...] 
def create_inverted_index(filename, page):
    src_data = codecs.open(filename,'r+',encoding='utf-8').read()#��������֪���ļ��ı����ʽ�������ļ�������ʹ�õ�utf-8 
    #ȥ��BOMͷ
    if src_data[:1].encode('utf-8') == codecs.BOM_UTF8:
        src_data = src_data[1:]

    #�����ʱ�
    sp_data = src_data.split()
    
    #��ƵTF�������ĵ��г��ֵĴ�����
    words = list(sp_data)
    dic_word_count = Counter(words)

    #������index
    for word in dic_word_count.keys():
        dic_word_count[word] = [int(page), dic_word_count[word]]
        if word in index.keys():
            index[word].append(dic_word_count[word])
        else:
            index[word] = [dic_word_count[word]]



#������
def main():
    #����data\\page�µ��ļ�
    #����ÿ���ļ�xx.txt�����ȷִʣ����ִʽ��д��fenci.txt
    #Ȼ���������������������index���ܵ��������ϲ�
    print('>>>������������')
    fenci_txt = "fenci.txt"
    N = 0
    path = "data\\page" #�ļ���Ŀ¼
    files= os.listdir(path) #�õ��ļ����µ������ļ�����
    N = len(files)
    s = []
    for file in files: #�����ļ���
        if not os.path.isdir(file): #�ж��Ƿ����ļ��У������ļ��вŴ�
            #print('>>>����', file)
            f = codecs.open(fenci_txt, 'w', encoding="UTF-8-SIG")
            for line in open(path+"\\"+file,encoding='utf-8',errors='ignore').readlines():
                #ȥ���
                line = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;��:-����+\"\']+|[+��������;:������~@#��%����&*����]+", " ", line)
                #�ִ�
                seg_list = jieba.cut(line, cut_all=True)
                #д��199801_new.txt
                f.write(" ".join(seg_list)+"\n")  
            f.close()      
            #������������
            create_inverted_index(fenci_txt, re.sub(r'\D', "", file))

    print('>>>����tf-idf')
    #�ĵ�Ƶ��df��������t���ĵ���������
    #w = (1 + log(tf))*log_10(N/df)
    i = 0
    for key in index.keys():
        df = len(index[key])
        i += 1
        for file_tf in index[key]:
            tf = file_tf[1]
            w = (1.0 + math.log(tf)) * math.log10(N / df)
            file_tf.append(w)

    # print('>>>���浽my_index.txt')
    # with codecs.open("my_index.txt", 'w', encoding="UTF-8-SIG") as i:
    #     for key in index.keys():
    #         i.write(key + str(index[key]) + "\n")

def search(query):
    time_start=time.time()
    query = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;��:-����+\"\']+|[+��������;:������~@#��%����&*����]+", " ", query)
    #�ִ�
    fenci = jieba.lcut(query)

    pages = {}
    for word in fenci:
        if word in index:
            for page in index[word]:
                if page[0] in pages:
                    pages[page[0]] += page[2]
                else:
                    pages[page[0]] = page[2]
    
    page_list = sorted(pages.items(), key = lambda item:item[1], reverse=True)
    time_end=time.time()
    len_page_list = len(page_list)
    if len_page_list != 0:
        if len_page_list <= 10:
            print("������%s����Ϊ���ҵ�%d�����(��ʱ%.6f��)��" % (query, len_page_list,time_end-time_start))
            i = 1
            for page in page_list:
                print("%d:%d.txt, tf-idf=%f" % (i, page[0], page[1]))
                i += 1
        else:
            print("������%s����Ϊ���ҵ�%d�����(��ʱ%.6f��)��" % (query, len_page_list,time_end-time_start))
            i = 1
            for page in page_list:
                print("%d:%d.txt, tf-idf=%f" % (i, page[0], page[1]))
                i += 1
                if i == 11:
                    yes = input("����ʾǰ10�����Ƿ���ʾ���У�[y/n]")
                    if yes == 'n':
                        break
    else:
        print("�޽��")       

#����
def test():
    query = input('�������������ݣ�')
    #ƴд���
    co_query = correct.auto_correct_sentence(query)
    if query != co_query:
        yes = input("������ʾ��%s���������������Ȼ������%s����[y/n]" % (co_query, query))
        if yes == 'y':
            search(query)
        else:
            search(co_query)
    else:
        search(co_query)

     



index = {}

#����
if __name__ == '__main__':
    print("........................")
    time_start=time.time()
    main()
    time_end=time.time()
    print(">>>��ʼ����ɣ���ʱ%.6f��\n........................"%(time_end-time_start))
    yes = 'y'
    test()
    while yes == 'y':
        yes = input("����������[y/n]")
        if yes == 'y':
            test()
        else:
            break

