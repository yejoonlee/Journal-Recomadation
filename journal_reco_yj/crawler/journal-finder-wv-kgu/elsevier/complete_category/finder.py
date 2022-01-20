from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from operator import itemgetter
import json
import collections
from urllib.request import HTTPError
import requests

def tree(): return collections.defaultdict(tree)

'''def find(keyword)
for문 : url마다
for문 : authorguide에서 dic의 단어가 있는 모든 문장'''



""""""
def csv_reader_for_dic(locate):
    f = open(locate, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    dic = {}
    for line in rdr:
        dic[line[0]] = line[1]
    f.close()
    return dic
'''csv파일 쓰기()'''
def csv_writer(data):
    # a=[]
    f = open('data_til3000.csv', 'w', encoding='utf-8', newline='')
    headers=[]
    headers.append('url')
    for highlight_text in highlight_texts:
        headers.append(highlight_text)
    dict_writer = csv.DictWriter(f,headers, delimiter=',')  # csv.DicWriter(f,delimiter='')
    dict_writer.writeheader()

    rows = []
    for i in data:

        if not i:
            d['url']=''
        for key, row in i.items():
            d = {header: row[header] if header in row else "" for header in headers}
            d['url']=key
            rows.append(d)

    for row_dict in rows:
        dict_writer.writerow(row_dict)

    f.close()





'''bring url (csv파일에서)'''
def csv_reader_for_url(locate):#반환형태 csv파일 내용 리스트, import csv
    a=[]
    f=open(locate,'r',encoding='utf-8')
    rdr=csv.reader(f)
    for line in rdr:#line의 type : list, string으로 변환할 필요가 있음.[]와 ''도 삭제할 필요가 있음
        a.append(''.join(line))
    f.close()
    return a




# class keyword():
#     category = csv_reader_for_dic('dic.csv')



'''필요한함수'''
'''value값과 text를 비교해서 저장하는 함수(text,value) return은 문장(sentence)'''
'''text가져오는 함수(url)return은 text(soup타입)'''



'''정제된text가져오는 함수(url)return은 text(soup타입)'''
def bring_text(url):#import url관련, beautifulSoup

    r = requests.get(url)
    soup1 = BeautifulSoup(r.text, "html.parser")

    findtext=str(soup1.find("article", class_="box-content")).lower()
    return findtext








# for문 url
# for문 keyword

#url불러오기
#저장할 url에 대한 di

locate='url_authorguide_til3000.csv'#url_authorguide

# data_dic=csv_reader_for_dic("dic.csv")

urls = csv_reader_for_url(locate)#list

highlight_texts =['keywords','submission','abstract','your paper yout way','type of paper','submission checklist','open access','peer review','language','special issue']
# 나중에 더 추가할 것@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

data=[]

for url in urls:
    #highlight_texts_list 초기화
    url_dic = tree()
    highlight_texts_dic = {}
    if not url:
        # data[url]= ''
        url_dic[url]={}
        data.append(url_dic)

        # print(highlight_texts_dic)
        continue

    findtext = bring_text(url)
    if findtext == None:
        # data[url] = ''
        url_dic[url]={}
        data.append(url_dic)
        # print(highlight_texts_dic)
        continue


    for i in highlight_texts:


        top_sentence = findtext.find('%s</strong> <br/><br/>' % i)  # 숫자
    # print(top_sentence)
        if top_sentence == -1:
            highlight_texts_dic[i] =''
            continue
        # top_sentence값이 없으면 다음으로 넘어가기
        bottom_sentence = findtext.find('</strong> <br/><br/>', top_sentence + 30)  # 숫자
    # print(bottom_sentence)
        find_highlight_texts = findtext[top_sentence:bottom_sentence]  # 문장
        url_dic[url][i]=find_highlight_texts
        # highligh_texts_list에 저장시키기
    # data[url]=highlight_texts_dic
    data.append(url_dic)

    # print(highlight_texts_list)
# print(dic)
for i in data:
    for key,value in i.items():
        print(key,dict(value))

# for i.iter in data:
#     if not i:
#         print('')
#         continue
#     print(i)
csv_writer(data)

# csv_writer(data_dic)
#
# for url in urls:
#     #highlight_texts_list 초기화
#     highlight_texts_list = []
#     if not url:
#         highlight_texts_list.append('')
#         print(highlight_texts_list)
#         continue
#
#     findtext = bring_text(url)
#     if findtext == None:
#         highlight_texts_list.append('')
#         print(highlight_texts_list)
#         continue
#
#
#     for i in highlight_texts:
#
#
#         top_sentence = findtext.find('%s</strong> <br/><br/>' % i)  # 숫자
#     # print(top_sentence)
#         if top_sentence == -1:
#             continue
#         # top_sentence값이 없으면 다음으로 넘어가기
#         bottom_sentence = findtext.find('</strong> <br/><br/>', top_sentence + 30)  # 숫자
#     # print(bottom_sentence)
#         find_highlight_texts = findtext[top_sentence:bottom_sentence]  # 문장
#
#         highlight_texts_list.append(find_highlight_texts + '-------------------------------------------------------------------')
#         # highligh_texts_list에 저장시키기
#
#     print(highlight_texts_list)




