from urllib.request import HTTPError
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup



class keyword:
    category={}

    # 저널 선택
    category['special_issue']=['special issue']
    category['open_access']=['open access']

    #형식에 따른 논문 수정
    category['the_number_of_column']=['column']
    category['the_number_of_keyword'] = []

    # 논문 제출
    category['submission_fee'] = ['$','USD','page charges']
    category['submittable_period'] = ['period']
    category['additional_fee'] = ['$','USD']

    #논문리뷰
    # !!(정보가 잘 없을 뿐만 아니라 변동성이 큼)


    # 최종투고
    category['publication_fee'] = ['$','USD']
    category['publication_period'] = ['period']

##category 내용 채우기
class completing_category:
    category={}

    # 저널 선택
    category['special_issue'] = []
    category['open_access'] = []

    # 형식에 따른 논문 수정
    category['the_number_of_column'] = []
    category['the_number_of_keyword'] = []

    # 논문 제출
    category['submission_fee'] = []
    category['submittable_period'] = []
    category['additional_fee'] = []

    # 논문리뷰
    # !!(정보가 잘 없을 뿐만 아니라 변동성이 큼)

    # 최종투고
    category['publication_fee'] = []
    category['publication_period'] = []


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

def csv_reader(csv):
    a=[]
    f=open(csv,'r',encoding='utf-8')
    rdr=csv.reader(f)
    for line in rdr:#line의 type : list, string으로 변환할 필요가 있음.[]와 ''도 삭제할 필요가 있음
        processed_line=str(line).translate({ord('['):'',ord(']'):'',ord(''):''})
        a.append(processed_line)
    return a

def url_reader(url):

    response=urlopen(url)
    plain_text=response.read()
    soup = BeautifulSoup(plain_text,'html,parser')
    html=(str(soup))#type을 bs4.beautifulsoup에서 str로 변환

    return html

def saver(key,url):#받는 값 keyword.category
    list=keyword.category[key]#key에 해당하는 value 리스트
    text = url_reader(url)
    for each in list:
        # value 리스트의 요소가 html문서에 존재하지 않을 경우
        if text.count(each)==0:
            continue

        indexes=[]
        # value 리스트의 요소가 html문서에 존재할 경우
        for i in text.count(each):
            indexes.append(text.find(each))