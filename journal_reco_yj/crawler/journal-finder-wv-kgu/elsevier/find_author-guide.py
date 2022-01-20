import csv
from urllib.request import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

# html 예외처리
def getTitle(url):
    try:
      html = urlopen(url)
    except HTTPError as e:
     return None

    try:
      bsObj = BeautifulSoup(html.read(), "html.parser")
      title = bsObj.body.h1
    except AttributeError as e:
      return None

    return title


#journal_title.csv를 list로 입력, 리스트명 : journal_title
f_r = open('../resources/title/journal_title_4501-5000.csv', 'r', encoding='utf-8')
rdr=csv.reader(f_r)

journal_titles = []

for line in rdr:
    processed_line = str(line).translate({ord('['): '',ord("'"): '',ord(']'): ''})
    journal_titles.append(processed_line)

f_r.close()


#journal_title에서 공백을 -로 변경, 리스트명 : changed_title
changed_titles=[]

for journal_title in journal_titles:
    i=journal_title.lower().translate({ord('&'):'and',ord(' '):'-'})
    changed_titles.append(i)


# issn 구하기 : run time 길어지는 구간
url_journals=[]
issns=[]

for changed_title in changed_titles:

    # issn구하기 url은 https://www.journals.elsevier.com/journal_name
    url_journal = 'https://www.journals.elsevier.com/%s' % changed_title

    # 저널url이 유효하지 않을 경우 issn=''
    if getTitle(url_journal) is None:
        # print("none")
        issns.append('')
        continue #다시 for문으로

    # 저널url이 유효한 경우
    response_issn = urlopen(url_journal)  # url 열기
    plain_text = response_issn.read()  # url text로 읽어오기
    soup_issn = BeautifulSoup(plain_text, 'html.parser')  # parser
    # issn = soup_issn.find('div',class_='issn keyword').text[16:25]
    issn_init = soup_issn.find('div', class_='issn keyword')
    if issn_init is None:
        issns.append('')
    else:
        issn=issn_init.text[16:25]
        issns.append(issn)


# url_author_guidelines구하기
url_author_guidelines=[]
a=0
for issn in issns:
    # 1번째 줄은 title에 해당하므로 url_author_guidelines=''

    # url형식 : https://www.elsevier.com/journals/'저널명'(띄어쓰기는 -로)/'issn'/guide-for-authors
    url_author_guideline='https://www.elsevier.com/journals/%s/%s/guide-for-authors'%(changed_titles[a],issns[a])
    url_author_guidelines.append(url_author_guideline.split())

    if issns[a]:
        # print(url_author_guidelines[a])
        a+=1
        continue

    else:
        # print("none")
        url_author_guidelines[a]=''
        a+=1
        continue


# csv파일 쓰기
# for문에 changed_title 하나씩 처리한다. 과정중에 csv파일로 author guideline page url내보낸다.
f_w = open('../resources/authorGuide_url/url_authorguide_4501-5000.csv', 'w', encoding='utf-8', newline='')
wr=csv.writer(f_w)

for url_author_guideline in url_author_guidelines:
    wr.writerow(url_author_guideline)
f_w.close()

exit()

#키워드찾기
guideline = []

def finder():
    response_guideline = urlopen(url_author_guideline)  # csv파일 읽어서 갖고오기
    plain_text = response_issn.read()  # url text로 읽어오기
    soup_guideline = BeautifulSoup(plain_text, 'html.parser')  # parser
    find_money = soup_guideline.find('USD').text[0:4]
    guideline.append(find_money)

