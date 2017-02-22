#! -*- coding:utf-8 -*-

# from translate import Translator

# content="switchself.translator= Translator(to_lang="zh") #设置翻译输出对象为中文。"
# translator= Translator(to_lang="zh") #设置翻译输出对象为中文。
# result=translator.translate(content)
# print result

from baidu_fanyi import fanyi

print fanyi("black",True)
print fanyi("蓝色",False)