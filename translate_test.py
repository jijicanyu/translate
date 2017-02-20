#! -*- coding:utf-8 -*-
'''
利用 translate 模块进行中英文翻译
https://github.com/terryyin/google-translate-python
'''

from translate import Translator
import speech


translator= Translator(to_lang="zh")
translation = translator.translate("switch")
# speech.say("switch")
print translation


'''
对每次查询的数据进行存储，然后进行查询次数的排名。每天都把前10名的单词列出来，以供记忆学习。
'''

'''
发音设置
'''

'''
GUI可以用wxpython
'''

