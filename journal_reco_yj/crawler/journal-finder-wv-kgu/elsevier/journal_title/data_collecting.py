import csv


##dictionary구축
class keyword:
    category={}


    # 저널 선택
    category['special_issue']=['special issue','special article',]# 언제 특집호가 열리는지는 나오지않음 특집호일때 작성방법만 나옴


    category['open_access']=['open access','choice','publish']
    # Y/N
    category['open_access fee' ] = ['open access publication fee','taxes','$','USD','Role of the funding source','Funding body agreements and policies']
    # number
    category['green_open_access'] = ['green open access', 'embargo period','share']
    # Y/N
    category['green_open_access_embargo period'] = ['green open access', 'embargo period', 'share','day','month','year']
    # number

    #형식에 따른 논문 수정
    category['the_length_of_text'] = ['text','maximum','less','exceed','around','more than']
    # number
    category['the_number_of_keyword'] = ['keyword','maximum','minimum','more than']
    # number
    category['language'] = ['engliish','language','text']
    # ???????
    category['format'] = ['column', 'format', 'word', 'latax', 'pdf', 'processor']
    # ???????
    category['the_length_of_abstract'] = ['abstract ','word', 'exceed','around','more than']

    # 논문 제출
    category['submission_fee'] = ['$','USD','Role of the funding source','Funding body agreements and policies']
    category['submission_date'] = ['submission date','period','day','month','year',]

    #논문리뷰
    # !!(정보가 잘 없을 뿐만 아니라 변동성이 큼)
    category['the_number_of_reviewer'] = ['blind', 'peer review ','review process','reviewer']


    # 최종투고
    category['publication_fee'] = ['$','USD','page charge']
    category['publication_period'] = ['period','month','day']


f = open('../dictionary.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for key, value in keyword.category.items():
    wr.writerow([key,value])

f.close()



