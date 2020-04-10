#!/usr/bin/env python3

from json import loads
import re
from urllib.parse import urlencode
from urllib.request import urlopen, Request

from select_menu import Menu


class Session:

    def __init__(self, site, cookie):
        self.site = site
        self.cookie = cookie

        class Data:
            def __init__(self, session):
                self.session = session

            def __getattr__(self, name):
                match = re.fullmatch(r'([a-z]+)_([A-Za-z]+)', name)
                if match:
                    module, sAct = match.groups()

                    def _act(**kwargs):
                        return self.session.act(module, sAct, **kwargs)
                    return _act
                raise AttributeError
        self.data = Data(self)

    def act(self, module, sAct, **kwargs):
        data = loads(urlopen(Request(
            f'{self.site}/data/module/{module}/all.asp?sAct={sAct}',
            urlencode(kwargs).encode(),
            headers={'Cookie': self.cookie}
        )).read())
        assert data['sRet'] == 'succeeded', data
        return data


if __name__ == "__main__":
    s = Session(
        input('站点（http://114.118.97.15）：') or 'http://114.118.97.15',
        'pj=' + (input('Cookie: pj=') or 'sClassIds=&iClassId=102&sGradeIds=&iUserId=10000095&iGroupId=300&sAllGradeIds=16%2C21%2C22%2C23&iGradeId=22&sDatabase=site%5F20180305000000')
    )
    menu = Menu(['Exam', 'Word train'])()
    if menu == 'Exam':
        for exam in s.data.homework_GetHomeworkListByStudent(
            iIsExam=1, iPageCount=s.data.homework_GetHomeworkListByStudent(iIsExam=1)['iCount']
        )['aHomework']:
            examContent = s.data.exam_GetExamContent(iExamId=exam['sQuestionIds'])
            for content in examContent['aContent']:
                print(content['sTitle'])
            for process in examContent['aProcess']:
                print('', process['iOrder'], process['sAnswer'], sep='\t')
            print()
    elif menu == 'Word train':
        unit = input('单元: ')
        try:
            expScore = 0
            while True:
                expScore += int(
                    s.data.word_AddWordTrainDetails(
                        iUnit=unit, iTrainId=s.data.word_BeginWordTrain(
                            sSubmodule='train', sTrainMode='batch', iTrainType='2', iUnit=unit, sSummary='%00'
                        )['iTrainId'],
                        sSerialIds='0', sAnswers='%00', sSolutions='%00', sIsPasses='1', sScores='100'
                    )['iExpScore']
                )
                print('\r' + str(expScore), end='', flush=True)
        except KeyboardInterrupt:
            print()
