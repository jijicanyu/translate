#! -*- coding:utf-8 -*-

'''
百度翻译API
'''

import requests
import md5
import json

appid="20170222000039660"
keyword="AO5uN4TGq1yynCgkqAKW"
salt="tzc"

def md5_(content):
	m1=md5.new()   
	m1.update(content)   
	content=m1.hexdigest()
	return content

def fanyi(q,types):
	sign=md5_(appid+q+salt+keyword)
	if types: #types=True English-->Chinese
		url="http://api.fanyi.baidu.com/api/trans/vip/translate?q="+q+"&from=en&to=zh&appid="+appid+"&salt="+salt+"&sign="+sign
	else:
		url="http://api.fanyi.baidu.com/api/trans/vip/translate?q="+q+"&from=zh&to=en&appid="+appid+"&salt="+salt+"&sign="+sign
	f=requests.get(url)
	result=json.loads(f.content)
	try:
		result=result['trans_result'][0]['dst']
	except:
		result=""
	return result

if __name__=="__main__":
	print fanyi('蓝色',False)
