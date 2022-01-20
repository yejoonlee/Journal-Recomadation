from urllib.request import urlopen
import csv
from urllib.request import HTTPError
from bs4 import BeautifulSoup
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


f_w = open('../resources/trial_output.csv', 'w', encoding='utf-8', newline='')
wr=csv.writer(f_w)

url_journal = 'https://www.journals.elsevier.com/biochimie'

if getTitle(url_journal) is None:
    print("none")
    exit()
response_issn = urlopen(url_journal)  # url 열기
plain_text = response_issn.read()  # url text로 읽어오기

soup_issn = BeautifulSoup(plain_text, 'html.parser')  # parser


issn = soup_issn.find('div', class_='issn keyword').text[16:25]

    # url형식 : https://www.journals.elsevier.com/journals/'저널명'(띄어쓰기는 -로)/'issn'/guide-for-authors
url_author_guideline = 'https://www.journals.elsevier.com/journals/%s/%s/guide-for-authors' % ('biochimie', issn)
if url_author_guideline:
    print(url_author_guideline)
    wr.writerow([url_author_guideline])
else:print("none")

f_w.close()