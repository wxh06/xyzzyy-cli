#!/usr/bin/env python3
  
from json import loads
from urllib.request import urlopen, Request


SITE = input('Site: ')
COOKIE = 'pj=' + input('pj=')

try:
    homeworkList = loads(urlopen(Request(f'{SITE}/data/module/homework/all.asp?sAct=GetHomeworkListByStudent', ('iIsExam=0&iPageBegin=0&iPageCount=' + loads(urlopen(Request(f'{SITE}/data/module/homework/all.asp?sAct=GetHomeworkListByStudent', b'iIsExam=0', headers={'Cookie': COOKIE})).read())['iCount']).encode(), headers={'Cookie': COOKIE})).read())
    assert homeworkList['sRet'] == 'succeeded', homeworkList
    for homework in homeworkList['aHomework']:
        if not homework['sTimeFlag'] and not int(homework['iFinished']):
            courseHomework = loads(urlopen(Request(f'{SITE}/data/module/course/all.asp?sAct=BeginCourseHomework', ('iHomeworkId=' + homework['iHomeworkId']).encode(), headers={'Cookie': COOKIE})).read())
            assert courseHomework['sRet'] == 'succeeded', courseHomework
            courseTrainDetails = loads(urlopen(Request(f'{SITE}/data/module/course/all.asp?sAct=AddCourseTrainDetails', ('iTrainId=' + courseHomework['iTrainId'] + '&iHomeworkId=' + homework['iHomeworkId'] + '&iPageId=' + courseHomework['sQuestionIds'] + '&sSerialIds=' + '0' + '&sAnswers=' + '%0D%0A%09+%09%0D%0A' + '&sSolutions=' + '%0D%0A%09+%09%0D%0A' + '&sScores=' + '100').encode(), headers={'Cookie': COOKIE})).read())
            assert courseTrainDetails['sRet'] == 'succeeded', courseTrainDetails
except KeyboardInterrupt:
    print()
