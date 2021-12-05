import pymysql
pymysql.install_as_MySQLdb()

db = pymysql.connect(host="127.0.0.1", user='root', password='2021mall', db='mall1')

cursor = db.cursor()

cursor.execute('SELECT VERSION()')

data = cursor.fetchone()
print('DATABASE VERSION IS: %s' % data)

db.close()
