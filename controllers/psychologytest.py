#!/usr/bin/env python
# coding: utf-8
import web
from config import settings
import extendlib.simplejson
from extendlib.pyExcelerator import *
import StringIO
render = settings.render
db = settings.db  
session=web.config._session

class Index:
    '''The index page for user portal'''
    def GET(self):
        return render.index()

class Register:
    '''Process with the user register information and store into the database'''
    def GET(self):
        information=web.input()
        #insert the user information into the table user
        session.user_id=db.insert("user",age=information.age, sex=information.sex, major=information.major)

class GetCondition:
    '''query the js global setting data from the databaseand then post the data to the client'''
    def GET(self):
        results = db.select('cond', what="probility_good,bonus_good,bonus_bad,bonus_fix,condition_id", where="is_default=1")
        data=results[0]
        session.condition_id=data.condition_id
        return extendlib.simplejson.dumps(data)

class Group1_1:
    '''Process with the answer of the first question in group 1'''
    def GET(self):
        information=web.input()
        session.group1_1=information.group1_1

class Group1_2:
    '''Process with the answer of the second question in group 1 
        and store the disussion the user make in the experiment into the database'''
    def GET(self):
        information=web.input()
        db.insert("group1",user_id=session.user_id, answer1=session.group1_1, answer2=information.group1_2)

class Group2:
    '''Process with the answer in group 2 
        and store the disussion the user make in the experiment into the database'''
    def GET(self):
        information=web.input()
        db.insert("group2",user_id=session.user_id, answer=information.group2, condition_id=session.condition_id) 
class SaveExcel:
    
    def GET(self):
        web.header('content-type','application/vnd.ms-excel')
        web.header('Content-Disposition','attachment; filename=test.xls')
        s = StringIO.StringIO()
        w = Workbook() #创建一个工作簿        
        ws = w.add_sheet('Hey, Hades') #创建一个工作表       
        ws.write(0,0,'bit') #在1行1列写入bit        
        ws.write(0,1,'huang') #在1行2列写入huang       
        ws.write(1,0,'xuan') #在2行1列写入xuan                
        w.save(s)
        return s.getvalue()
