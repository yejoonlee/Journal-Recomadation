import pymysql

conn = pymysql.connect(host='wordvice-db.cimcf1c6lvo2.ap-northeast-1.rds.amazonaws.com',
                       user='essayreview_beta',
                       password='beta',
                       db='test',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'SELECT * from a_journal_crawling_log'
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        # (1, 'test@test.com', 'my-passwd')
finally:
    conn.close()