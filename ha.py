# -*- coding:utf-8 -*-
import sys


start_c={}#开始概率，就是一个字典，state:chance=Word/lines
transport_c={}#转移概率，是字典：字典，state:{state:num,state:num....}   num=num(state1)/num(statess)
emit_c={}#发射概率，也是一个字典，state:{word:num,word,num}  num=num(word)/num(words)
Count_dic = {}  # 一个属性下的所有单词，为了求解emit
state_list = ['Ag', 'a', 'ad', 'an', 'Bg', 'b', 'c', 'Dg',
			  'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l',
			  'Mg', 'm', 'Ng', 'n', 'nr', 'ns', 'nt', 'nx',
			  'nz', 'o', 'p', 'q', 'Rg', 'r', 's','na',
			  'Tg', 't','u', 'Vg', 'v', 'vd', 'vn','vvn',
			  'w', 'Yg', 'y', 'z']
lineCount=-1#句子总数，为了求出开始概率
for state0 in state_list:
    transport_c[state0]={}
    for state1 in state_list:
        transport_c[state0][state1]=0.0
    emit_c[state0]={}
    start_c[state0]=0.0
vocabs=[]
classify=[]
class_count={}
for state in state_list:
    class_count[state]=0.0
with open('corpus_POS.txt') as filess:
    for line in filess:  #一次处理全部的行？？列表可能会影响效率？？
        line=line.strip()
        if not line:continue
        lineCount+=1#应该在有内容的行处加 1
        words=line.split(" ")#分解为多个单词
        for word in words:
            position=word.index('/')  #如果是[中国人民/n]
            if '[' in word and ']' in word:
                vocabs.append(word[1:position])
                vocabs.append(word[position+1:-1])
                break
            if  '[' in word:
                vocabs.append(word[1:position])
                classify.append(word[position+1:])
                break
            if ']' in  word:
                vocabs.append(word[:position])
                classify.append(word[position+1:-1])
                break
            vocabs.append(word[:position])
            classify.append(word[position+1:])

        if  len(vocabs)!=len(classify):
            print('词汇数量与类别数量不一致')
            break  #不一致退出程序
            # start_c = {}  # 开始概率，就是一个字典，state:chance=Word/lines
            # transport_c = {}  # 转移概率，是字典：字典，state:{state:num,state:num....}   num=num(state1)/num(statess)
            # emit_c = {}  # 发射概率，也是一个字典，state:{word:num,word,num}  num=num(word)/num(words)
        else:
            for n in range(0,len(vocabs)):
                class_count[classify[n]]+=1.0
                if vocabs[n] in emit_c[classify[n]]:
                    emit_c[classify[n]][vocabs[n]] += 1.0
                else:
                    emit_c[classify[n]][vocabs[n]] = 1.0
                if n==0:
                    start_c[classify[n]] += 1.0
                else:
                    transport_c[classify[n-1]][classify[n]]+=1.0
        vocabs = []
        classify = []
for state in state_list:
    start_c[state]=start_c[state]*1.0/lineCount
    for li in emit_c[state]:
        emit_c[state][li]=emit_c[state][li]/class_count[state]
    for li in transport_c[state]:
        transport_c[state][li]=transport_c[state][li]/class_count[state]
file0=open('start.txt','w',encoding='utf8')
file0.write(str(start_c))
file1=open('tran.txt','w',encoding='utf8')
file1.write(str(transport_c))
file2=open('emit.txt','w',encoding='utf8')
file2.write(str(emit_c))
file0.close()
file1.close()
file2.close()

