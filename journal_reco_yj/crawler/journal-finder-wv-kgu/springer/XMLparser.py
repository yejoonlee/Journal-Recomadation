from bs4 import BeautifulSoup
from urllib.request import urlopen

#적당한 스프링거 저널 url로 프로토타입 파서 생성
url = "http://www.springer.com/biomed/pharmacology+%26+toxicology/journal/11095"
response = urlopen(url)
plain_text = response.read().decode()


#BeautifulSoup로 HTML을 파싱하기 편한 데이터형으로 변환
soup = BeautifulSoup(plain_text, 'html.parser')


#a 태그와 linkOpenLayer클래스를 통해 범위를 좁혀 저장
lists = soup.find_all('a', class_="linkToOpenLayer")
for item in lists:
    # 키워드인 'Instructions for Authors'를 조건으로 한 문단을 특정하여 onclick값을 받아온다.
    if 'Instructions for Authors' in item.text:
        urlxp = item.get('onclick')

#onclick값중 필요한 부분만 남긴다.
si = urlxp.find("?")
ei = urlxp.find("',")
urla = urlxp[si:ei]

#스프링거 주소와 위에서 얻어낸 값을 이어 XML접근을 위한 url을 얻어낸다.
urlb = "http://www.springer.com/"
urlx = urlb + urla
print(urlx)