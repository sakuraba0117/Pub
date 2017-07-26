# -*- coding: utf-8 -*-

import sqlite3

dbname = 'database.db'

conn = sqlite3.connect(dbname)
#sql=u"""create table task(taskname varchar(32),time varchar(32),comment varchar(200));"""
#conn.execute(sql)
sqs=u"""insert into task values('にくやき','11:50-14:30','(´・ω・｀)出火よー');"""
conn.execute(sqs)

sqp=u"""insert into task values (?,?,?)"""
conn.execute(sqp,(u"運搬",u"9:30-11:30",u"木炭濡れないように"))
conn.execute(sqp,(u"買い出し",u"8:00-9:20",u"後で食べる分は確保しておく"))
conn.execute(sqp,(u"返却",u"17:20-19:00",u"早く終わったら片付け手伝い"))
conn.execute(sqp,(u"片付け",u"17:30-19:30",u"来年も使いまわせるものは倉庫内へ"))
c=conn.cursor()
c.execute(u"select * from task")

for row in c:
        print (row[0],row[1],row[2])

conn.commit()

conn.close()
