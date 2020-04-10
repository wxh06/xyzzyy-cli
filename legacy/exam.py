#!/usr/bin/env python3

from json import loads
from urllib.request import urlopen, Request


SITE = input('Site: ')
COOKIE = 'pj=' + input('pj=')

examList = loads(urlopen(Request(f'{SITE}/data/module/homework/all.asp?sAct=GetHomeworkListByStudent&iIsExam=1&iPageCount=' + loads(urlopen(Request(f'{SITE}/data/module/homework/all.asp?sAct=GetHomeworkListByStudent&iIsExam=1', headers={'Cookie': COOKIE})).read())['iCount'], headers={'Cookie': COOKIE})).read())
assert examList['sRet'] == 'succeeded', examList
for exam in examList['aHomework']:
    if not exam['sTimeFlag'] and not int(exam['iFinished']):
        examContent = loads(urlopen(Request(f'{SITE}/data/module/exam/all.asp?sAct=GetExamContent&iExamId=' + exam['sQuestionIds'], headers={'Cookie': COOKIE})).read())
        assert examContent['sRet'] == 'succeeded', examContent
        try:
            for content in examContent['aContent']:
                print(content['sTitle'])
            for process in examContent['aProcess']:
                print(process['iOrder'], process['sAnswer'], sep='\t')
        except IndexError:
            pass
