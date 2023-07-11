import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root', db='user', charset='utf8', password="1234")

print(db)

cur = db.cursor()
cur.execute("select * from users")
db.commit()
db.close()
print(cur.fetchone())