from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from journal_reco.yb.LDA.resources.stop import get_my_stop_words
import pickle
import time
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
##topic modeling with combined training data(test data should not be combined.)

#start time : it needs end time
start_time = time.time()
#유일한 title 받아오기
cursor.execute('select distinct(title) from representative_document where publisher = "elsevier" and category = "recent"')
unique=[i[0] for i in cursor.fetchall()]
print(len(unique))
# index=unique
index=len(unique)

#모든문서를 받아 하나의 리스트에 저장
input=[]
cursor.execute('select * from representative_document where publisher = "elsevier" and category = "recent"')
for i in cursor.fetchall():
    input.append(''.join(i[2:4]))
    print(i[2:4])

print(input[0:2])



# infile=open('../journal_reco/yb/LDA/resources/mdpi_combined.txt','r')
# for line in infile:
#     input.append(line)
# infile.close()

# no_features : the number of terms included in the bag of words matrix
# no_topics : the number of topics which represents the word set
no_features = 1000
no_topics = 50
no_top_words = 10

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1, max_features=no_features, stop_words=get_my_stop_words())
tf = tf_vectorizer.fit_transform(input)
tf_feature_names = tf_vectorizer.get_feature_names()
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

# Save all data necessary for later prediction
model = (tf_feature_names, lda.components_, lda.exp_dirichlet_component_, lda.doc_topic_prior_)
with open("elsevier_topicmodeling", 'wb') as fp:
    pickle.dump(model, fp)

# print Topic model
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
display_topics(lda, tf_feature_names, no_top_words)

end_time = time.time()
print(str(end_time - start_time) + 's, lda training')

##결과물 : topicmodel