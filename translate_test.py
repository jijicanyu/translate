#! -*- coding:utf-8 -*-

'''
中英文翻译，且可以发音，并且将累计列出翻译量前十名的单词。
'''

__author__="nMask"
__Date__="20170221"

import wx
import threading
from translate import Translator
from wx.lib.embeddedimage import PyEmbeddedImage
import sqlite3
import speech


class myapp(wx.App):
    def __init__(self,redirect):
        wx.App.__init__(self,redirect)
        pass

   
    def OnInit(self):
        frame = myframe(None,-1,'my title')
        frame.SetMaxSize((425,325))
        frame.Show()
        self.SetTopWindow(frame)
        return True
     
class myframe(wx.Frame):
	def __init__(self,parent,id,title):
		wx.Frame.__init__(self,parent,id,title=u"哥哥教你学英语    nMask's Blog http://thief.one ",size=(425,325))
		self.path=""
		self.translator= Translator(to_lang="zh") #设置翻译输出对象为中文。

		panel=wx.Panel(self)
		self.SetIcon(tzc.GetIcon())
		self.content_start=wx.TextCtrl(panel,-1,pos=(10,10),size=(120,40))
		self.fanyi=wx.Button(panel,-1,u"翻译",pos=(140,10),size=(50,40))
		self.yuyin=wx.Button(panel,-1,u"语音",pos=(200,10),size=(50,40))
		self.content_end=wx.TextCtrl(panel,-1,pos=(10,80),size=(250,210),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2)
		self.top_ten=wx.TextCtrl(panel,-1,pos=(260,10),size=(150,280),style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2)


		self.fanyi.Bind(wx.EVT_BUTTON,self.fanyi_run)
		self.yuyin.Bind(wx.EVT_BUTTON,self.yuyin_run)

		db=sqlite3.connect("./db.db")  ##数据库连接配置
		cur=db.cursor()
		self.select(cur) #计算top_10
		cur.close()
		db.close()

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
		db=sqlite3.connect("./db.db")  ##数据库连接配置
		cur=db.cursor()
		result_list=select_data(cur,content)  ##查询数据库

		if len(result_list)==0: #若数据库中没有此条记录，则调用api查询
			try:
				result = self.translator.translate(content)
				insert_data(cur,content,result,"1") #将查询结果保存到数据库
			except:
				result=u"翻译失败，请检查网络是否存在问题！"
		else:
			result=result_list[0][1]
			num=result_list[0][2]
			num=str(int(num)+1)
			update_data(cur,content,num) #更新数据库

		self.content_end.SetValue(result) #将查询结果显示在界面上

		db.commit()  ##提交修改

		self.select(cur)

		cur.close()
		db.close()

	def select(self,cur):
		result_limit_list=select_num(cur)
		content=u"【精彩 Top 10】 \n"
		for i in result_limit_list:
			word=i[0]
			tran_word=i[1]
			num=i[2]
			content+=word+"  "+tran_word+"  "+num+"\n"
		self.top_ten.SetValue(content)

	def yuyin_run(self,event):
		content=self.content_start.GetValue()
		t=threading.Thread(target=self.yuyin_main,args=(content,))
		t.start()

	def yuyin_main(self,content):
		'''
		语音功能
		'''
		try:
			speech.say(content)
		except:
			pass
		pass


def create_table(cur):
	'''
	创建表，字段如下：
	@word 英文单词(或者中文)
	@tran_word 翻译以后的词语
	@num 被翻译次数
	'''
	cur.execute("""create table zydata (word varchar(100),tran_word varchar(100),num varchar(10))""")

def insert_data(cur,word,tran_word,num):
	'''
	插入数据
	'''
	cur.execute("insert into zydata values('"+word+"','"+tran_word+"','"+num+"')")

def update_data(cur,word,num):
	'''
	更新数据
	'''
	cur.execute("update zydata set num='"+num+"' where word = '"+word+"' ")

def delete_data(cur):
	'''
	删除数据
	'''
	cur.execute("delete from zydata")

def select_data(cur,word):
	'''
	查询数据
	'''
	cur.execute("select * from zydata where word='"+word+"'")
	result=cur.fetchall()  #输出列表

	return result
	# print cur.fetchone()  #输出一个结果

def select_num(cur):
	cur.execute("select * from zydata ORDER BY num DESC limit 10")
	result=cur.fetchall()  #输出列表

	return result


if __name__ == '__main__':
	db=sqlite3.connect("./db.db")
	cur=db.cursor()
	# '''
	# 数据库操作
	# '''
	# # create_table(cur) #创建表
	# insert_data(cur,"switch","转换",'1') #插入数据
	# delete_data(cur) #删除表中数据
	# select_data(cur)  #查询表中数据
	# select_num(cur) #排序查询

	db.commit()
	cur.close()
	db.close()

	'''
	运行GUI界面程序
	'''
	tzc = PyEmbeddedImage(
    "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")
	mainapp = myapp(redirect = False)
	mainapp.MainLoop()

      


