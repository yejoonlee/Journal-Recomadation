import pickle
import time
import csv
import time
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import pymysql
mydb = pymysql.connect(host='127.0.0.1', user='root', password='imlab506',
                       db='wb_db', charset='utf8')
cursor = mydb.cursor()
# Columns:
# idx int(11) AI PK
# issn varchar(20)
# abstract mediumtext
# title varchar(1500)
# keywords varchar(225)
# history varchar(200)
# publication_date date
# doi varchar(50)
# article_url varchar(100)
# journal_title varchar(255)
# publisher varchar(50)
# category varchar(50)
# indexed_keywords mediumtext
start_time = time.time()

# # create a blank model
lda = LatentDirichletAllocation()

# load parameters from file
with open ('elsevier_topicmodeling', 'rb') as fd:
    (features, lda.components_, lda.exp_dirichlet_component_, lda.doc_topic_prior_) = pickle.load(fd)
# #유일한 저널명 리스트
cursor.execute('select distinct(journal_title) from representative_document where publisher = "elsevier" and category = "recent"')


journal_list=[i[0] for i in cursor.fetchall()]
index=len(journal_list)
#csv파일 말고 데이터 바로 불러오기
data_samples=[]
for journal in journal_list:
    index-=1
    print(index)
    cursor.execute('select * from representative_document where journal_title = "%s"'%journal)
    input=[]
    for row in cursor.fetchall():
        # print(row)
        if row[3]:
            input.append(''.join(row[2:4]))

    if input:
        data_samples.append(''.join(input))


print(data_samples[0:2])
# # the dataset to predict on (first two samples were also in the training set so one can compare)
# f_r = open('../resources/mdpi_input_title.csv', 'r', encoding='ISO-8859-1')
# rdr=csv.reader(f_r)
# data_samples = []
# for line in rdr:
#     data_samples+=list(line)
# f_r.close()

# Vectorize the training set using the model features as vocabulary
tf_vectorizer = CountVectorizer(vocabulary=features)
tf = tf_vectorizer.fit_transform(data_samples)

# transform method returns a matrix with one line per document, columns being topics weight
predict = lda.transform(tf)
end_time = time.time()
print(str(end_time - start_time) + 's, client predict')

# output array를 list로 변환
list_client_output = predict.tolist()

# journal별 topic에 대한 연관도
journalTopic = []
for j in range(0, len(list_client_output)): journalTopic.append(list_client_output[j])

print(len(list_client_output))

# 결과를 csv파일에 한줄씩 입력
f = open('../resources/topic_elsevier'+'.csv', 'w', encoding='utf-8', newline="")
wr = csv.writer(f)
for row in journalTopic:
    wr.writerow(row)
f.close()

end_time = time.time()
print(str(end_time - start_time) + 's, create_journalTopic_table')