#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb

class ConclusionBase:
    param = (
        'fgqw',
        'xssj',
        'mg'
    )

    interpretor = (
        ['fgqw','asgm','pcdxbd','hgzl'],
        ['xssj','gsbq','epqy'],
        ['mg','sshdspc','pcbrm']
    )


    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "mysql123654", "mydata", charset='utf8')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        self.final = []

    def clear(self):
        db = self.db
        cursor = self.cursor
        sql = "DROP TABLE IF EXISTS concdata"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 向数据库提交
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

    def create(self):
        db = self.db
        cursor = self.cursor
        # 创建数据表newdata的SQL语句
        sql = """CREATE TABLE concdata (
                            id int,
                            property text,
                            value float )"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print "concdata succefully built"
        except:
            # Rollback in case there is any error
            db.rollback()
            print "concdata rollback"

        # sql = """CREATE TABLE finaldata (
        #                     id int,
        #                     property text,
        #                     value float )"""
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 提交到数据库执行
        #     db.commit()
        #     print "finaldata succefully built"
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()
        #     print "finaldata rollback"

    def putone(self,(h,cf_h)):
        cursor = self.cursor
        db = self.db
        sql = """INSERT INTO concdata (id,property,value)
                                    VALUES (7,'%s',%f)""" %(h,cf_h)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "rollback"
        cursor.execute("SELECT * FROM concdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        print rows

    def pickkind(self,h):
        cursor = self.cursor
        cursor.execute("SELECT * FROM concdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        kind = []
        l = len(rows)
        print rows
        for i in range(l):
            if rows[i][1] == h:
                kind.append(rows[i])
        return kind

    def deletekind(self,h):
        cursor = self.cursor
        db = self.db
        sql = "DELETE FROM concdata WHERE property = '%s'" % (h)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    def num(self):
        cursor = self.cursor
        cursor.execute("SELECT * FROM concdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        return len(rows)

    def pickone(self,i):
        cursor = self.cursor
        cursor.execute("SELECT * FROM concdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        clu = rows[i][1]
        return clu

    def update(self,(h,es)):
        self.final.append(h)
        for i in range(len(es)):
            self.final.append(es[i])
        self.final.append('/n')

    def getcon(self):
        cursor = self.cursor
        cursor.execute("SELECT * FROM concdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        return rows




