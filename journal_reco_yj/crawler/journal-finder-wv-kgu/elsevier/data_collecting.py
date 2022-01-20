import csv
from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup

##dictionary구축
class keyword:
    category={}


    # 저널 선택
    category['special_issue']=['special issue','special article',]# 언제 특집호가 열리는지는 나오지않음 특집호일때 작성방법만 나옴


    category['open_access']=['open access','choice','publish']
    category['open_access fee' ] = ['open access publication fee','taxes','$','USD','Role of the funding source','Funding body agreements and policies']
    category['green_open_access'] = ['green open access', 'embargo period','share']
    category['green_open_access_embargo period'] = ['green open access', 'embargo period', 'share','day','month','year']

    #형식에 따른 논문 수정
    category['the_length_of_text'] = ['text','maximum','less','exceed','around','more than']
    category['the_number_of_keyword'] = ['keyword','maximum','minimum','more than']
    category['language'] = ['engliish','language','text']
    category['format'] = ['column', 'format', 'word', 'latax', 'pdf', 'processor']
    category['abstract'] = ['abstract ','word', 'exceed','around','more than']

    # 논문 제출
    category['submission_fee'] = ['$','USD','Role of the funding source','Funding body agreements and policies']
    category['submission_date'] = ['submission date','period','day','month','year',]

    #논문리뷰
    # !!(정보가 잘 없을 뿐만 아니라 변동성이 큼)
    category['the_number_of_reviewer'] = ['blind', 'peer review ','review process','reviewer']


    # 최종투고
    category['publication_fee'] = ['$','USD','page charge']
    category['publication_period'] = ['period','month','day']









##  journal_url 들어가서(csv파일을 읽어온다.)

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

# csv 파일에서 url을 가져 온다.
f=open('../resources/url_authorguide.csv','r',encoding='utf-8')
rdr=csv.reader(f)
urls=[]
for line in rdr:
    processed_url=str(line).translate({ord('['): '',ord("'"): '',ord(']'): ''})
    urls.append(processed_url)

# url에서 html문서를 가져와 저장한다.
texts=[]



for url in urls:
    print(url)
    # if url is '':
    #     print('none')
    if url is '':
        texts.append('')
        continue

    if getTitle(url) is None:
        continue
    response=urlopen(url)
    plain_text=response.read()
    soup=BeautifulSoup(plain_text,'html.parser')
    texts.append(soup)

print(texts)
## html에서(txt로 변환?) keyword dictionary를 통해 데이터를 추출한다.

