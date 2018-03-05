#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb

class DataBase:
    param = (
        'asgm',
        'sshdspc',
        'pcdxbd',
        'hgzl',
        'gsbqx',
        'epqy',
        'pcbrm'
    )

    def __init__(self):
        # self.symptoms=0
        # self.allegy=0

        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "mysql123654", "mydata", charset='utf8')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

        # db = self.db
        # cursor = self.cursor
        # 如果数据表已经存在使用 execute() 方法删除表。
        # cursor.execute("DROP TABLE IF EXISTS newdata")
        # cursor.execute("DROP TABLE IF EXISTS olddata")
        # 创建数据表newdata的SQL语句
        # sql = """CREATE TABLE newdata (
        #             id int,
        #             property text,
        #             value float )"""
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 提交到数据库执行
        #     db.commit()
        #     print "newdata succefully built"
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()
        #     print "newdata rollback"

        # 创建数据表olddatade的SQL语句
        # sql = """CREATE TABLE olddata (
        #             id int,
        #             property text,
        #             value float )"""
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 提交到数据库执行
        #     db.commit()
        #     print "olddata succefully built"
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()
        #     print "olddata rollback"

    def __del__(self):
        self.db.close()  # 关闭数据库连接

    def clear(self):
        db = self.db
        cursor = self.cursor
        sql = "DROP TABLE IF EXISTS newdata"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 向数据库提交
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        sql = "DROP TABLE IF EXISTS olddata"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 向数据库提交
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

    def create(self):
        # 创建数据表newdata的SQL语句
        db = self.db
        cursor = self.cursor
        sql = """CREATE TABLE newdata (
                            id int,
                            property text,
                            value float )"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print "newdata succefully built"
        except:
            # Rollback in case there is any error
            db.rollback()
            print "newdata rollback"

        # 创建数据表olddatade的SQL语句
        sql = """CREATE TABLE olddata (
                    id int,
                    property text,
                    value float )"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print "olddata succefully built"
        except:
            # Rollback in case there is any error
            db.rollback()
            print "olddata rollback"

    def insert(self,e):
        db = self.db
        cursor = self.cursor
        for i in range(len(e)):
            if e[i] != 0:
                sql = """INSERT INTO newdata (id,property,value)
                        VALUES (%d,'%s',1.0)""" %(i,DataBase.param[i])
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    print "newdata rollback"

        #创建一个相同的表格用来存放fact，方便最后比照
        for i in range(len(e)):
            if e[i] != 0:
                sql = """INSERT INTO olddata (id,property,value)
                        VALUES (%d,'%s',1.0)""" % (i, DataBase.param[i])
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    print "olddata rollback"

    def newdatanum(self):
        cursor = self.cursor
        cursor.execute("SELECT * FROM newdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        return len(rows)

    def pickone(self):
        cursor = self.cursor
        cursor.execute("SELECT * FROM newdata")
        # 选择查看自带的表,不修改数据库数据所以无需commit
        rows = cursor.fetchall()
        fac = [rows[0][1],rows[0][2]]
        return fac

    def ndeleteone(self,fac):
        cursor = self.cursor
        db = self.db
        sql = "DELETE FROM newdata WHERE property = '%s'" % (fac[0])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "rollback"

    def nputone(self,(semi,cf_semi)):
        cursor = self.cursor
        db = self.db
        sql = """INSERT INTO newdata (id,property,value)
                                VALUES (0,'%s',%f)""" %(semi,cf_semi)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "rollback"

    def checksymptom(self,sym):
        cursor = self.cursor
        cursor.execute("SELECT * FROM olddata")
        rows = cursor.fetchall()
        flag = 0
        for i in range(len(rows)):
            if sym == rows[i][1]:
                flag = flag + 1
        return flag





