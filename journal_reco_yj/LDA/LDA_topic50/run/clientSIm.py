import pickle
import time
import csv
import time
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

start_time = time.time()

# # create a blank model
lda = LatentDirichletAllocation()

# load parameters from file
with open ('../resources/elsevier_topicmodeling', 'rb') as fd:
    (features, lda.components_, lda.exp_dirichlet_component_, lda.doc_topic_prior_) = pickle.load(fd)

# the dataset to predict on (first two samples were also in the training set so one can compare)
f_r = open('../resources/test_input_elsevier.csv', 'r', encoding='ISO-8859-1')
rdr=csv.reader(f_r)
data_samples = []
for line in rdr:
    if line:
        data_samples .append(line[3])
    
f_r.close()
print(data_samples)
# Vectorize the training set using the model features as vocabulary
tf_vectorizer = CountVectorizer(vocabulary=features)
tf = tf_vectorizer.fit_transform(data_samples)

# transform method returns a matrix with one line per document, columns being topics weight
predict = lda.transform(tf)
end_time = time.time()
print(str(end_time - start_time) + 's, client predict')

# output array를 list로 변환
list_client_output = predict.tolist()

# client의 topic에 대한 연관도
clientTopic = []
for j in range(0, len(list_client_output)): clientTopic.append(list_client_output[j])

print(len(list_client_output))

# 결과를 csv파일에 한줄씩 입력
f = open('../resources/clientTopic'+'.csv', 'w', encoding='utf-8', newline="")
wr = csv.writer(f)
for row in clientTopic:
    wr.writerow(row)
f.close()

end_time = time.time()
print(str(end_time - start_time) + 's, create_clientTopic_table')