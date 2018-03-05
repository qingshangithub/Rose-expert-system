#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb

class KnowledgeBase:
    rules = (
        ['asgm', 'qwz', 0.9],
        ['asgm', 'yjz', -0.3],
        ['asgm', 'gwz', -0.2],
        ['sshdspc', 'qwz', -0.2],
        ['sshdspc', 'yjz', -0.3],
        ['sshdspc', 'gwz', 0.9],
        ['qwz', 'fgqw', 0.4],
        ['yjz', 'xssj', 0.3],
        ['gwz', 'mg', 0.8],
        ['pcdxbd', 'fgqw', 0.5],
        ['hgzl', 'fgqw', 0.8],
        ['gsbqx', 'xssj', 0.7],
        ['epqy', 'xssj', 0.6],
        ['pcbrm', 'mg', 0.8]
    )
    def __init__(self):
        # self.symptoms = 0

        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "mysql123654", "mydata", charset='utf8')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def clear(self):
        db = self.db
        cursor = self.cursor
        sql = "DROP TABLE IF EXISTS konwdata"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 向数据库提交
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            print "rollback"


    def create(self):
        db = self.db
        cursor = self.cursor
        # cursor.execute("DROP TABLE IF EXISTS konwdata")
        # 创建数据表newdata的SQL语句
        sql = """CREATE TABLE konwdata (
                            id int,
                            pre text,
                            suf text,
                            value float )"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print "konwdata succefully built"
        except:
            # Rollback in case there is any error
            db.rollback()
            print "konwdata rollback"

    def insert(self):
        db = self.db
        cursor = self.cursor
        for i in range(len(KnowledgeBase.rules)):
            sql = """INSERT INTO konwdata (id,pre,suf,value)
                            VALUES (%d,'%s','%s',%f)"""%(i,KnowledgeBase.rules[i][0],KnowledgeBase.rules[i][1],KnowledgeBase.rules[i][2])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                print "konwdata rollback"

    def num(self):
        return len(KnowledgeBase.rules)

    def pickone(self,i):
        return KnowledgeBase.rules[i]






