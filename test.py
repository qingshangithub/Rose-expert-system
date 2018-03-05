#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
# db = MySQLdb.connect("10.10.10.5","root","mysql123654","test")
db = MySQLdb.connect("localhost","root","mysql123654","mydata") #备用IP 127.0.0.1
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SHOW DATABASES")
# 使用 fetchone() 方法获取一条数据。
data = cursor.fetchone()
# 使用 fetchall() 方法获取全部数据。
print "data",data

cursor.execute("DROP TABLE IF EXISTS newdata")
sql = """CREATE TABLE newdata (
                    id int,
                    property text,
                    value float )"""
try:
    cursor.execute(sql)
            # 提交到数据库执行
    db.commit()
    print "newdata succefully built"
except:
    # Rollback in case there is any error
    db.rollback()
    print "newdata rollback"

# sql = """INSERT INTO newdata (id,property,value)
#                         VALUES (1,"1",1.0)"""
u='as'
sql = """INSERT INTO newdata (id,property,value)
                        VALUES (%d,'%s',1.0)""" %(1,u)
# sql = """INSERT INTO newdata (id,property,value)
#                         VALUES (i,'%s',1.0)""" %(DataBase.param[i])
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
sql = """INSERT INTO newdata (id,property,value)
                        VALUES (3,"2",1.0)"""
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
cursor.execute("SELECT * FROM newdata")    #选择查看自带的user这个表  (若要查看自己的数据库中的表先use XX再查看)
rows = cursor.fetchall()
print rows
print len(rows)
# sql = "DELETE FROM newdata WHERE property = '%s'" % (rows[1][1])
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
# cursor.execute("SELECT * FROM newdata")    #选择查看自带的user这个表  (若要查看自己的数据库中的表先use XX再查看)
# rows_2 = cursor.fetchall()
# print rows_2
sym = '0'
cursor.execute("SELECT * FROM newdata")
rows = cursor.fetchall()
flag = 0
for i in range(len(rows)):
    if sym == rows[i][1]:
        flag = flag + 1
print flag
db.close()
