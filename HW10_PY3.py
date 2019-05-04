#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
import jieba
import string
import re
import imp

from xpinyin import Pinyin


FILE_PATH = "HW10/Autochecker4Chinese-master/token_freq_pos%40350k_jieba.txt"
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += '。，？：；｛｝［］‘“”《》／！％……（）'


def construct_dict( file_path ):
	
	word_freq = {}
	with open(file_path, "rb") as f:
		for line in f:
			info = line.split()
			word = info[0]
			frequency = info[1]
			word_freq[word] = frequency
	
	return word_freq


def load_cn_words_dict( file_path ):
	cn_words_dict = ""
	with open(file_path, "rb") as f:
		for word in f:
			cn_words_dict += word.strip().decode("utf-8")
	return cn_words_dict


def edits1(phrase, cn_words_dict):
	"All edits that are one edit away from `phrase`."
	splits     = [(phrase[:i], phrase[i:])  for i in range(len(phrase) + 1)]
	deletes    = [L + R[1:]                 for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:]   for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]             for L, R in splits if R for c in cn_words_dict]
	inserts    = [L + c + R                 for L, R in splits for c in cn_words_dict]
	return set(deletes + transposes + replaces + inserts)

def known(phrases): return set(phrase for phrase in phrases if phrase.encode("utf-8") in phrase_freq)


def get_candidates( error_phrase ):
	
	candidates_1st_order = []
	candidates_2nd_order = []
	candidates_3nd_order = []

	p = Pinyin()
	error_pinyin = p.get_pinyin(error_phrase)
	re.sub("-", "/", error_pinyin)
	cn_words_dict = load_cn_words_dict( "HW10/Autochecker4Chinese-master/cn_dict.txt" )
	candidate_phrases = list( known(edits1(error_phrase, cn_words_dict)) )
	
	for candidate_phrase in candidate_phrases:
		# candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/").encode("utf-8")
		candidate_pinyin = p.get_pinyin(candidate_phrase)
		re.sub("-", "/", candidate_pinyin)
		if candidate_pinyin == error_pinyin:
			candidates_1st_order.append(candidate_phrase)
		elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
			candidates_2nd_order.append(candidate_phrase)
		else:
			candidates_3nd_order.append(candidate_phrase)
	
	return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def find_max(c1_order):
    maxo = ''
    maxi = 0
    for i in range(0, len(c1_order)):
        if c1_order[i].encode("utf-8") in phrase_freq:
            freq = int(phrase_freq.get(c1_order[i].encode('utf-8')))
            if freq > maxi:
                maxi = freq
                maxo = c1_order[i]
    return maxo

def auto_correct( error_phrase ):
	
	c1_order, c2_order, c3_order = get_candidates(error_phrase)
	if c1_order:
		return find_max(c1_order)
	elif c2_order:
		return find_max(c2_order)
	else:
		return find_max(c3_order)

def auto_correct_sentence( error_sentence, verbose=True):
	jieba_cut = jieba.cut( error_sentence, cut_all=False)
	seg_list = "\t".join(jieba_cut).split("\t")
	
	correct_sentence = ""
	
	for phrase in seg_list:
		
		correct_phrase = phrase
		# check if item is a punctuation
		if phrase not in PUNCTUATION_LIST:
			# check if the phrase in our dict, if not then it is a misspelled phrase
			if phrase.encode('utf-8') not in phrase_freq.keys():
				correct_phrase = auto_correct(phrase)
				if verbose :
					print(phrase, correct_phrase)
	
		correct_sentence += correct_phrase

	return correct_sentence



phrase_freq = construct_dict( FILE_PATH )

def test_case(err_sent_1):
	print('===============')
	correct_sent = auto_correct_sentence( err_sent_1 )
	t1 = "original sentence:" + err_sent_1 + "\n==>\n" + "corrected sentence:" + correct_sent
	print(t1)

def main():
	err_sent_1 = u'机七学习是人工智能领遇最能体现智能的一个分知！'
	test_case(err_sent_1)
	err_sent_1 = u'杭洲是中国的八大古都之一，因风景锈丽，享有"人间天棠"的美誉！'
	test_case(err_sent_1)
	
if __name__=="__main__":
	main()
