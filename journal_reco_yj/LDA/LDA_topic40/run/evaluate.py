import csv
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


client_topic=[[0]*20 for i in range(5)]
journal_topic=[[0]*20 for i in range(1619)]
client_belong=[[''] for i in range(len(client_topic))]
top=5

#clientTopic읽어오기
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


with open('../resources/clientTopic.csv','r') as f:
    reader=csv.reader(f)
    index=0
    for client in reader:
        client_topic[index]=list(chunks(client,1))
        index+=1


# print(client_topic[0])

#journalTopic읽어오기
with open('../resources/topic_elsevier.csv','r') as f:
    reader=csv.reader(f)
    index=0
    for journal in reader:
        journal_topic[index]=list(chunks(journal,1))
        index+=1

#client가 어디에 속하는가
with open('../resources/test_input_elsevier.csv','r') as f:
    reader=csv.reader(f)
    index=0
    for test_input in reader:
        print(test_input)
        if test_input:
            client_belong[index] = str(test_input[-1]).lower()
            index += 1


# print(journal_topic[0])
client_max_similarTopic=[['']for i in range(5)]
for i in range(len(client_topic)):
    client_max_similarTopic[i]='topic'+str(client_topic[i].index(max(client_topic[i])))

print(client_max_similarTopic)
print(journal_topic[0])

topic_journal=[[0]*1619 for i in range(20)]
for journal_row in journal_topic:
    for i in range(20):
        topic_journal[i][journal_topic.index(journal_row)]=journal_topic[journal_topic.index(journal_row)][i]

print(topic_journal[0])
print(client_max_similarTopic[-1][-1])

client_recommend=[[0]*top for i in range(len(client_topic))]
client_index=0
for recommend_to_client in client_max_similarTopic:
    origin_similar_list=[''.join(similar) for similar in topic_journal[int(recommend_to_client[-1])]]
    similar_list=[''.join(similar) for similar in topic_journal[int(recommend_to_client[-1])]]
    print(similar_list)
    print(type(similar_list[0]))

    for i in range(top):

        # print(i)
        #저널 추천
        client_recommend[client_index][i]=origin_similar_list.index(max(similar_list))
        # print(client_recommend)
        similar_list.remove(max(similar_list))
    client_index+=1

print(client_recommend)

cursor.execute('select distinct(journal_title) from representative_document where publisher = "elsevier" and category = "recent"')
journal_list=[i[0] for i in cursor.fetchall()]

client_dictionary={}
for i in range(len(client_recommend)):
    client_dictionary[client_belong[i]]=[str(journal_list[n]).lower() for n in client_recommend[i]]

print(client_dictionary)
for key,value in client_dictionary.items():
    print(key, value)
with open('../resources/top_'+str(top)+'.csv','w',encoding='utf-8', newline="") as f:
    wr = csv.DictWriter(f,client_dictionary.keys())
    wr.writeheader()
    wr.writerow(client_dictionary)


for key,value in client_dictionary.items():
    if key in value:
        print(1)
    else:
        print(0)