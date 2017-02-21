#! -*- coding:utf-8 -*-

'''
中英文翻译，且可以发音，并且将累计列出翻译量前十名的单词。
'''

__author__="nMask"
__Date__="20170221"

import wx
import threading
import speech
from translate import Translator
import sqlite3


class myapp(wx.App):
    def __init__(self,redirect):
        wx.App.__init__(self,redirect)
        pass

   
    def OnInit(self):
        frame = myframe(None,-1,'my title')
        frame.SetMaxSize((380,320))
        frame.Show()
        self.SetTopWindow(frame)
        return True
     
class myframe(wx.Frame):
	def __init__(self,parent,id,title):
	    wx.Frame.__init__(self,parent,id,title=u'哥哥教你学英语',size=(380,320))

	    self.path=""
	    self.translator= Translator(to_lang="zh") #设置翻译输出对象为中文。

	    panel=wx.Panel(self)
	    self.content_start=wx.TextCtrl(panel,-1,pos=(10,10),size=(120,40))
	    self.fanyi=wx.Button(panel,-1,u"翻译",pos=(140,10),size=(50,40))
	    self.yuyin=wx.Button(panel,-1,u"语音",pos=(200,10),size=(50,40))
	    self.content_end=wx.TextCtrl(panel,-1,pos=(10,80),size=(350,200),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2)

	    self.fanyi.Bind(wx.EVT_BUTTON,self.fanyi_run)
	    self.yuyin.Bind(wx.EVT_BUTTON,self.yuyin_run)

	def fanyi_run(self,event):
		content=self.content_start.GetValue()
		t=threading.Thread(target=self.fanyi_main,args=(content,))
		t.start()

	def fanyi_main(self,content):
		'''
		翻译功能：
		1.从数据库中获取信息
		2.若数据库中没有，利用google api获取
		3.将获取的数据存入数据库
		4.数据库中进行统计，并选出搜索量前十的单词
		'''
		translation = self.translator.translate(content)
		self.content_end.SetValue(translation)

		



		
	def yuyin_run(self,event):
		content=self.content_start.GetValue()
		t=threading.Thread(target=self.yuyin_main,args=(content,))
		t.start()

	def yuyin_main(self,content):
		'''
		语音功能
		'''
		speech.say(content)


def create_table():
	'''
	创建表，字段如下：
	@id  主键（word加密后生成），唯一标识符
	@word 英文单词(或者中文)
	@tran_word 翻译以后的词语
	@num 被翻译次数
	'''
	cur=db.cursor()
	cur.execute("""create table zydate ( id integer primary key,word varchar(10),tran_word varchar(10),num varchar(10))""")

def insert_data():
	'''
	插入数据
	'''
	pass

def update_data():
	'''
	更新数据
	'''
	pass

def delete_data():
	'''
	删除数据
	'''
	pass

def select_data():
	'''
	查询数据
	'''
	pass




if __name__ == '__main__':
	db=sqlite3.connect("./db.db")
	mainapp = myapp(redirect = False)
	mainapp.MainLoop()

      


